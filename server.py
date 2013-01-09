#coding=utf-8
"""Seed.server -- metadata and data server program for SEED storage.
Daemon:
Implementation of a Simplified S3-like storage server based on local files.
"""
import os
import datetime
from Pyro4.core import Daemon
from Pyro4 import config as PyroConfig

from utils import NodeName
from utils import Initialize

class Server(Daemon):
    """XML RPC Server for SEED"""
    def __init__(self, ip, port, root_directory):
        Daemon.__init__(self)
        self.directory = os.path.abspath(root_directory)
        if not os.path.exists(self.directory):
            # root not initiailized, use '-i' first.
            Initialize(self.directory)
        self.config = PyroConfig
        self.config.HMAC_KEY = 'SEED indentifier'
        self.config.HOST = ip
        self.config.
        self.register(S3Handler(), NodeName(ip, port))

    def run(self):
        self.requestLoop()

class S3Handler(object):
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
        handle.done('\n'.join(buckets))

    def check_bucket_exists(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or not os.path.isdir(path):
            response = 404
        else:
            response = 200

        handle.done(response)

    def create_bucket(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or os.path.exists(path):
            response = 403
        else:
            os.makedirs(path)
            response = 200

        handle.done(response)

    def delete_bucket(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or not os.path.isdir(path):
            response = 404
        elif len(os.listdir(path)) > 0:
            response = 403
        else:
            os.rmdir(path)
            response = 204

        handle.done(response)

    def list_bucket(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or not os.path.isdir(path):
            return ''
        object_names = []
        for root, dirs, files in os.walk(path):
            for file_name in files:
                object_names.append(os.path.join(root, file_name))

        handle.done('\n'.join(object_names))

    def head(self, bucket, key):
        path = os.path.abspath(os.path.join(self.directory, bucket, key))
        if not path.startswith(self.directory) or not os.path.isfile(path):
            response = 404
        else:
            response = 200

        handle.done(response)

    def delete(self, bucket, key):
        path = os.path.abspath(os.path.join(self.directory, bucket, key))
        if not path.startswith(self.directory) or not os.path.isfile(path):
            response = 404
        else:
            os.unlink(path)
            response = 204

        handle.done(response)

    # system functions
    def version(self):
        path = os.path.abspath(os.path.join(self.directory, '.seed/version'))
        if not path.startswith(self.directory) or not os.path.isfile(path):
            response = "error while getting version info"
        else:
            response = open(path).read()

        handle.done(response)

    def status(self):
        handle.done("not implemented")
