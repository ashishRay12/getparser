
class Request:

    def __init__(self, data):
        self.query_data = data['query_params']
        self.headers_data = data['headers']

    def get_params(self, name):
        return self.query_data[name]

    def get_header(self, name):
        return self.query_data[name]
