import tornado.ioloop
import tornado.web

import conf

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class MatchHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class TISApp(tornado.web.Application):
    def init_dict(self):
        self.dicts = {}

def make_app():
    app = TISApp([
        (r"/", MainHandler),
        (r"/match", MatchHandler),
        ])

    app.init_dict()
    return app

if __name__ == "__main__":
    app = make_app()
    app.listen(conf.listening_port)
    tornado.ioloop.IOLoop.current().start()
