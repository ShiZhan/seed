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
        self.register_function(self.list_all_my_buckets, "list_all_my_buckets")
        self.register_function(self.check_bucket_exists, "check_bucket_exists")
        self.register_function(self.create_bucket, "create_bucket")
        self.register_function(self.delete_bucket, "delete_bucket")
        self.register_function(self.list_bucket, "list_bucket")
        self.register_function(self.head, "head")
        self.register_function(self.delete, "delete")
        self.register_function(self.version, "version")
        self.register_function(self.status, "status")
        self.serve_forever()

    # s3-like functions
    def list_all_my_buckets(self):
        names = os.listdir(self.directory)
        buckets = []
        for name in names:
            path = os.path.join(self.directory, name)
            info = os.stat(path)
            buckets.append(
                "Name: " + name + " CreationDate: " +
                datetime.datetime.utcfromtimestamp(info.st_ctime).ctime()
            )
        return '\n'.join(buckets)

    def check_bucket_exists(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or not os.path.isdir(path):
            return 404
        else:
            return 200

    def create_bucket(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or os.path.exists(path):
            return 403
        else:
            os.makedirs(path)
            return 200

    def delete_bucket(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or not os.path.isdir(path):
            return 404
        if len(os.listdir(path)) > 0:
            return 403
        os.rmdir(path)
        return 204

    def list_bucket(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or not os.path.isdir(path):
            return ''
        object_names = []
        for root, dirs, files in os.walk(path):
            for file_name in files:
                object_names.append(os.path.join(root, file_name))
        return '\n'.join(object_names)

    def head(self, bucket, key):
        path = os.path.abspath(os.path.join(self.directory, bucket, key))
        if not path.startswith(self.directory) or not os.path.isfile(path):
            return 404
        else:
            return 200

    def delete(self, bucket, key):
        path = os.path.abspath(os.path.join(self.directory, bucket, key))
        if not path.startswith(self.directory) or not os.path.isfile(path):
            return 404
        os.unlink(path)
        return 204

    # system functions
    def version(self):
        path = os.path.abspath(os.path.join(self.directory, '.seed/version'))
        if not path.startswith(self.directory) or not os.path.isfile(path):
            return "error while getting version info"
        else:
            response = open(path).read()
            return response

    def status(self):
        return "not implemented"
