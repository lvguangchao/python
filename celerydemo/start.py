#coding=utf-8
import tornado
from tornado.options import define, options, parse_command_line
from tornado.log import enable_pretty_logging
import tcelery
from app import TestHandler
import tornado.httpserver

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

urls = [(r"/api/task/test", TestHandler)]

def server_start():
    app = tornado.web.Application(urls, debug=options.debug)
    enable_pretty_logging()
    parse_command_line()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(options.port)
    server.start()
    tcelery.setup_nonblocking_producer(limit=2)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    server_start()