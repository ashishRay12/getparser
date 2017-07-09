

class Response:

    def __init__(self, transport):
        self.transport = transport
        self.status = b'200 OK'
        self.body = None
        self.content_type = None
        self._headers = {}
        self.data = None
        self.content_length = 0
        self._line = None

    def send(self):

        self.transport.write(b"HTTP/1.1 " + self.status + b'\r\n')

        if self.content_type:
            if not isinstance(self.content_type, bytes):
                content_type = self.content_type.encode('utf-8')
                self.content_type = content_type
                self.transport.write(b"content-type:" + self.content_type + b'\r\n')

        if self.body:
            if not isinstance(self.body, bytes):
                body = self.body.encode('utf-8')
                self.data = body
                self.content_length = str(len(body)).encode('utf-8')
                self.transport.write(b'content-length:' + self.content_length + b'\r\n')

        self.transport.write(b"\r\n")
        self.transport.write(self.data)
        self.transport.loseConnection()

    # def built_headers(self):

    #     self._line = b"HTTP/1.1 " + self.status + b'\r\n'
    #     self._line += b"content-type" + self.content_type + b'\r\n'






