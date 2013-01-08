#coding=utf-8
"""Seed.server -- metadata and data server program for SEED storage.
Daemon:
Implementation of a Simplified S3-like storage server based on local files.
"""
import os
import datetime
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

class Daemon(SimpleXMLRPCServer):
    """XML RPC Server for SEED"""
    def __init__(self, port=10001, root_directory='/tmp/s3'):
        SimpleXMLRPCServer.__init__(self, ("localhost", port))
        self.directory = os.path.abspath(root_directory)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
    def run(self):
        self.register_function(self.is_even, "is_even")
        self.serve_forever()

    def is_even(self, n):
        return n%2 == 0


# from tornado.ioloop import IOLoop
# from tornado import web

# class BasicHandler(web.RequestHandler):
#     """BasicHandler implements common functions for all handlers"""
#     SUPPORTED_METHODS = ("PUT", "GET", "DELETE", "HEAD")


# class RootHandler(BasicHandler):
#     def get(self):
#         names = os.listdir(self.application.directory)
#         buckets = []
#         for name in names:
#             path = os.path.join(self.application.directory, name)
#             info = os.stat(path)
#             buckets.append(
#                 "Name: " + name + " CreationDate: " +
#                 datetime.datetime.utcfromtimestamp(info.st_ctime).ctime()
#             )
#         self.finish('<br/>'.join(buckets))


# class BucketHandler(BasicHandler):
#     def get(self, bucket_name):
#         path = os.path.abspath(os.path.join(self.application.directory,
#                                             bucket_name))
#         if not path.startswith(self.application.directory) or \
#            not os.path.isdir(path):
#             raise web.HTTPError(404)
#         object_names = []
#         for root, dirs, files in os.walk(path):
#             for file_name in files:
#                 object_names.append(os.path.join(root, file_name))
#         self.finish('\n'.join(object_names))

#     def put(self, bucket_name):
#         path = os.path.abspath(os.path.join(
#             self.application.directory, bucket_name))
#         if not path.startswith(self.application.directory) or \
#            os.path.exists(path):
#             raise web.HTTPError(403)
#         os.makedirs(path)
#         self.finish()

#     def delete(self, bucket_name):
#         path = os.path.abspath(os.path.join(
#             self.application.directory, bucket_name))
#         if not path.startswith(self.application.directory) or \
#            not os.path.isdir(path):
#             raise web.HTTPError(404)
#         if len(os.listdir(path)) > 0:
#             raise web.HTTPError(403)
#         os.rmdir(path)
#         self.set_status(204)
#         self.finish()

#     def head(self, bucket_name):
#         path = os.path.abspath(os.path.join(self.application.directory,
#                                             bucket_name))
#         if not path.startswith(self.application.directory) or \
#            not os.path.isdir(path):
#             raise web.HTTPError(404)
#         self.finish(bucket_name)


# class ObjectHandler(BasicHandler):
#     def get(self, bucket, object_name):
#         object_name = urllib.unquote(object_name)
#         path = os.path.abspath(os.path.join(
#             self.application.directory, bucket, object_name))
#         if not path.startswith(self.application.directory) or \
#            not os.path.isfile(path):
#             raise web.HTTPError(404)
#         object_file = open(path, "r")
#         try:
#             self.finish(object_file.read())
#         finally:
#             object_file.close()

#     def put(self, bucket, object_name):
#         object_name = urllib.unquote(object_name)
#         bucket_dir = os.path.abspath(os.path.join(
#             self.application.directory, bucket))
#         if not bucket_dir.startswith(self.application.directory) or \
#            not os.path.isdir(bucket_dir):
#             raise web.HTTPError(404)
#         path = os.path.abspath(os.path.join(
#             self.application.directory, bucket, object_name))
#         if not path.startswith(bucket_dir) or os.path.isdir(path):
#             raise web.HTTPError(403)
#         directory = os.path.dirname(path)
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#         object_file = open(path, "w")
#         object_file.write(self.request.body)
#         object_file.close()
#         self.finish()

#     def delete(self, bucket, object_name):
#         object_name = urllib.unquote(object_name)
#         path = os.path.abspath(os.path.join(
#             self.application.directory, bucket, object_name))
#         if not path.startswith(self.application.directory) or \
#            not os.path.isfile(path):
#             raise web.HTTPError(404)
#         os.unlink(path)
#         self.set_status(204)
#         self.finish()

#     def head(self, bucket, object_name):
#         object_name = urllib.unquote(object_name)
#         path = os.path.abspath(os.path.join(
#             self.application.directory, bucket, object_name))
#         if not path.startswith(self.application.directory) or \
#            not os.path.isfile(path):
#             raise web.HTTPError(404)
#         self.finish(object_name)


# class Daemon(web.Application):
#     """tornado application for RESTful file service"""
#     def __init__(self, port=10001, root_directory='/tmp/s3'):
#         web.Application.__init__(self, [
#             (r"/", RootHandler),
#             (r"/([^/]+)/", BucketHandler),
#             (r"/([^/]+)/(.+)", ObjectHandler),
#         ])
#         self.port = port
#         self.directory = os.path.abspath(root_directory)
#         if not os.path.exists(self.directory):
#             os.makedirs(self.directory)
        
#     def run(self):
#         self.listen(self.port)
#         IOLoop.instance().start()
