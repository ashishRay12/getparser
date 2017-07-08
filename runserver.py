from twisted.internet import reactor, protocol, endpoints
from io import StringIO
import re
import six
# from getparser import HTTP_METHODS


class App:

    _route = {}

    def __init__(self):
        self.factory = WebsFactory()

    def add_route(self, uri_template, resource):
        if not isinstance(uri_template, six.string_types):
            raise TypeError('uri_template is not a string')

        if not uri_template.startswith('/'):
            raise ValueError("uri_template must start with '/'")

        if '//' in uri_template:
            raise ValueError("uri_template may not contain '//'")

        if not hasattr(resource, 'method_get'):
            raise AttributeError("resource must contain method_get")

        self._route[uri_template] = resource

    def run_server(self):
        websEndpoint = endpoints.serverFromString(reactor, "tcp:8080")
        websEndpoint.listen(WebsFactory())
        reactor.run()


class MyWebs(protocol.Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("connectionMade")

    def dataReceived(self, data):
        data = StringIO(data.decode("utf-8"), newline='\n')
        self.parseData(data)

    def parseData(self, data):

        first_header_line = data.readline().split('\r\n')[0]
        if self.factory.get_pettern.match(first_header_line):
            self.parseHeader(data)
            self.sendResponse()
        else:
            self.transport.write(b"HTTP/1.1 404 Not Found\r\n")
            self.transport.loseConnection()

    def parseHeader(self, data):
        head = True
        headers = {}
        body = False
        r_body = ""
        for i in data:
            if i == "\r\n":
                head = False
                body = True
            if head:
                try:
                    s = i.split(': ')
                    headers[s[0]] = s[1].split("\r\n")[0]
                except IndexError:
                    print("first line: %s" % (i))
            if body:
                r_body = r_body + "".join(i.split("\r\n"))
        # print(headers)
        # print(r_body)
        self.headers = headers
        self.body = body

    def sendResponse(self):
        self.transport.write(b"HTTP/1.1 200 OK\r\n")
        self.transport.write(b"Content-Type: text/html; charset=utf-8\r\n")
        self.transport.write(b"\n")
        responseBody = b"<html><body><h1>You said: bla bla</h1></body></html>"
        self.transport.write(responseBody)
        self.transport.loseConnection()


class WebsFactory(protocol.ServerFactory):
    get_pettern = re.compile(r'GET\s/.*\sHTTP/1.1')

    def buildProtocol(self, addr):
        print(addr)
        return MyWebs(self)

app = App()
app.run_server()

# websEndpoint = endpoints.serverFromString(reactor, "tcp:8080")
# websEndpoint.listen(WebsFactory())
# reactor.run()
