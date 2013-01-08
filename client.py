#coding=utf-8
"""Seed.client -- client program for SEED storage.
Client:
Implementation of a Simplified S3-like storage client based on HTTPClient.
"""
from xmlrpclib import ServerProxy

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 10001

class Client(ServerProxy):
    """XML RPC Client for accessing SEED"""
    def __init__(self, server=DEFAULT_HOST, port=DEFAULT_PORT):
        ServerProxy.__init__(self,
            'http://' + server + ':' + str(port) + '/')

    def put(self, bucket, key, value):
        return

    def get(self, bucket, key):
        return
