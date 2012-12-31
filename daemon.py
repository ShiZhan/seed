#coding=utf-8
"""Seed.Daemon -- Daemon program for SEED storage, 
client, name server and data server all-in-one.
"""
from s3server import S3Application
from tornado import httpserver
from tornado import ioloop

import logging

class Daemon(S3Application):
    """Seed.Daemon -- Providing an S3-like storage server based on local files.
    """
    def __init__(self, port=10001, root_directory='/tmp/s3', bucket_depth=0):
        S3Application.__init__(self, root_directory, bucket_depth)
        self.port = port

    def run(self):
        """run server loop on the given port at the given path."""
        logging.info('Serving HTTP on 0.0.0.0 port %d ...', self.port)
        http_server = httpserver.HTTPServer(self)
        http_server.listen(self.port)
        ioloop.IOLoop.instance().start()
