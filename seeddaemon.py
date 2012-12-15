#coding=utf-8
"""SeedDaemon -- Daemon program for SEED storage, 
client, name server and data server all-in-one. """
import os

import tornado.web
import tornado.ioloop

class SeedHandler(tornado.web.RequestHandler):
    def get(self):
        """ GET method """

        self.write('get')

    def post(self):
        """ POST method """

        self.write('post')

    def put(self):
        """ PUT method """

        self.write('put')

    def delete(self):
        """ DELETE method """

        self.write('delete')

class SeedDaemon(object):
    """SeedDaemon"""
    def __init__(self, daemonport):
        super(SeedDaemon, self).__init__()
        self.port = daemonport

    def run(self):
        """run server loop"""
        current_path = os.getcwd()

        application = tornado.web.Application([(r"/", SeedHandler),])

        application.listen(self.port)

        print 'Serving HTTP on 0.0.0.0 port %d ...' % self.port
        tornado.ioloop.IOLoop.instance().start()
