
import getparser
app = getparser.App()


class MyApi:

    def on_get(self, req, resp):

        resp.status = getparser.HTTP_200
        resp.send()

app.add_route('/get', MyApi())
app.run_server('127.0.0.1', 8000)
