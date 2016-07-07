import tornado.ioloop
import tornado.web

import conf
from trie import TrieIndex
from dict_locate import dict_locate

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def encoded_matcher(d, q, offset, encoding='utf-8'):
    """Convert the returned index from unicode to utf-8

    Args:
        d (unicode): dict trie index
        q (unicode): question string in unicode
        offset (int): start to find prefix from the position
        encoding (str): encoding of the original question string byte stream

    Yields:
        int: the ending index of the matched prefix substring in utf-8
    """
    for i in d.matcher(q, offset):
        length = len(q[0:i].encode(encoding))
        yield length

class MatchHandler(tornado.web.RequestHandler):
    """Handle request to the /match route, only GET request is processed."""
    def get(self):
        """Process the GET request.

        GET Args (all are converted to unicode):
            d (str): dict name in utf-8
            q (str): question string in utf-8 which must be url encoded
            offset (int): the starting pos to search

        Return (dict in json):
            errno (int): 0 if success, otherwise other error numbers
            errmsg (str): "ok" if success, otherwise other error messages
            data (list): indices of the ending positions of all possible prefix
        """
        d = self.get_argument('d', default=None)
        q = self.get_argument('q', default=None)
        offset = self.get_argument('offset', default=0)

        if not d or not q:
            self.write({"errno": 1, "errmsg": "parameter is missing"})
            return

        if d not in self.application.dicts:
            self.write({"errno": 2, "errmsg": "specified dict does not exist"})
            return

        # convert to unicode offset
        try:
            u_prefix = (q.encode('utf-8')[0:int(offset)]).decode('utf-8')
            offset = len(u_prefix)
        except:
            self.write({"errno": 3, "errmsg": "utf-8 offset is not valid"})
            return

        d = self.application.dicts[d]
        matches = [i for i in encoded_matcher(d, q, offset, 'utf-8')]
        self.write({"errno":0, "errmsg":"ok", "data":matches})

class TISApp(tornado.web.Application):
    def init_dict(self):
        self.dicts = {}
        for tag in conf.dict_conf:
            dict_file = dict_locate(tag)
            self.dicts[tag] = TrieIndex()
            for line in open(dict_file):
                line = line.decode('utf-8').rstrip()
                self.dicts[tag].add(line)

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
