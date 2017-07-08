

class Response:

    def __init__(self, transport):
        self.transport = transport
        self.status = b'200 OK'
        self.body = None
        self.content_type = None
        self._headers = {}
        self.data
        self.content_length = 0

    def send(self):

        if self.body is not None:
            if not isinstance(self.body, bytes):
                body = self.body.encode('utf-8')
                self.data = body
                self.content_length = len(body)
        self.transport.write(b"HTTP/1.1 " + self.status + b'\r\n')
