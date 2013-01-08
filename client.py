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

    # private methods
    def _request(self):
        return self.is_even(1)

    # public methods
    def list_all_my_buckets(self):
        return None

    def check_bucket_exists(self, bucket):
        return self._request()

    def create_bucket(self, bucket):
        return None

    def delete_bucket(self, bucket):
        return None

    def list_bucket(self, bucket):
        return None

    def put(self, bucket, key, value):
        return None

    def get(self, bucket, key):
        return None

    def head(self, bucket, key):
        return None

    def delete(self, bucket, key):
        return None
