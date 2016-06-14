from __future__ import print_function
import threading
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class LikeHandler(tornado.web.RequestHandler):

    def initialize(self, queue):
        self.queue = queue

    def get(self):
        self.queue.put("HEART")
        self.render("index.html")


class Server:
    def __init__(self, queue):
        self.thread = None
        self.queue = queue
        self.app = tornado.web.Application(
            [
                (r"/", MainHandler),
                (r"/a/like", LikeHandler, {"queue": queue}),
            ],
            template_path=os.path.join(os.path.dirname(__file__), "www"),
            static_path=os.path.join(os.path.dirname(__file__), "assets"),
            debug=False,
        )

    def start(self, port):
        self.app.listen(port)
        self.thread = threading.Thread(target=tornado.ioloop.IOLoop.current().start)
        self.thread.daemon = True
        self.thread.start()
        return self.thread

    def stop(self):
        if self.thread is not None:
            self.thread.stop()


if __name__ == "__main__":
    from Queue import Queue
    queue = Queue()
    server = Server(queue)
    print("Starting server")
    server.start(9999)
    print("Start polling queue")
    while True:
        if not queue.empty():
            print(queue.get_nowait())
