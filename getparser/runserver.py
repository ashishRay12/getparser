from twisted.internet import reactor, protocol, endpoints
from io import StringIO
import re
import six
from __init__ import HTTP_METHODS, METHODS_MAP
from routing import map_route, get_route
from request import Request
from response import Response


class App:

    def __init__(self):
        self.factory = WebsFactory()

    def add_route(self, uri_template, resource):
        if not isinstance(uri_template, six.string_types):
            raise TypeError('uri_template is not a string')

        if not uri_template.startswith('/'):
            raise ValueError("uri_template must start with '/'")

        if '//' in uri_template:
            raise ValueError("uri_template may not contain '//'")

        map_route(uri_template, resource)

    def route_req(self, data):
        pass

    def run_server(self):
        websEndpoint = endpoints.serverFromString(reactor, "tcp:8080")
        websEndpoint.listen(WebsFactory())
        reactor.run()


def route_req(data, transport):
    request_obj = Request(data)
    response_obj = Response(transport)

    try:
        resource = get_route(data['path'])
        method = data['method']
        resource_method = getattr(resource, METHODS_MAP[method])
        resource_method(req=request_obj, resp=response_obj)
    except (AttributeError, KeyError):
        transport.write(b"HTTP/1.1 404 Not Found\r\n")
        transport.loseConnection()


class MyWebs(protocol.Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("connectionMade")

    def dataReceived(self, data):

        # self.sendResponse()
        data = data.decode("utf-8")
        data = data.split('\r\n', 1)
        self.parseData(data)

    def parseData(self, data):

        data_dict = {}
        first_header_line = data[0]
        if self.factory.get_pettern.match(first_header_line):

            data_dict.update(self.parseMethod(first_header_line))
            data_dict.update(self.parseHeader(data[1]))
            route_req(data_dict, self.transport)
            # self.sendResponse()
        else:
            self.transport.write(b"HTTP/1.1 404 Not Found\r\n")
            self.transport.loseConnection()

    def parseMethod(self, line):

        method_dict = {}
        line_list = line.split(' ')
        method_dict['method'] = line_list[0]
        full_path_list = line_list[1].split('?')
        method_dict['path'] = full_path_list[0]
        try:
            query_parm_list = self.factory.query_pattern.findall(full_path_list[1])
            query_params = {}
            for key_val in query_parm_list:
                if key_val[0] in query_params:
                    query_params[key_val[0]].append(key_val[1])
                else:
                    query_params[key_val] = []
            method_dict['query_params'] = query_params
        except IndexError:
            # if there is no query paramete
            method_dict['query_params'] = {}
        return method_dict

    def parseHeader(self, data):

        raw_headers = data.split('\r\n\r\n', 1)[0]
        headers_dict = {}
        headers_dict['headers'] = dict(self.factory.headers_pattern.findall(raw_headers))
        return headers_dict


class WebsFactory(protocol.ServerFactory):
    get_pettern = re.compile(r'GET\s/.*\sHTTP/1.1')
    query_pattern = re.compile(r'(\w+)[=](\w+)')
    headers_pattern = re.compile(r'(\w+)[:](\w+)')

    def buildProtocol(self, addr):
        print(addr)
        return MyWebs(self)
