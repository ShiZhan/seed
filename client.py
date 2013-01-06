#coding=utf-8
"""Seed.client -- client program for SEED storage.
Client:
Implementation of a Simplified S3-like storage client based on HTTPClient.
"""
from tornado.httpclient import AsyncHTTPClient

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 10001

class Client(AsyncHTTPClient):
    """ClientApplication for accessing SEED"""
    def __init__(self, server=DEFAULT_HOST, port=DEFAULT_PORT):
        AsyncHTTPClient.__init__(self)
        self.url_base = 'http://' + server + ':' + str(port)

    # private methods
    def _request(self, response):
        self.fetch(self.url_base,
                   callback=(yield Callback("_to_get_key")))
        response = yield Wait("_to_get_key")

    # public methods
    def list_all_my_buckets(self):
        self._request(response)
        return response

    def check_bucket_exists(self, bucket):
        self._request(response)
        return response

    def create_bucket(self, bucket):
        self._request(response)
        return response

    def delete_bucket(self, bucket):
        self._request(response)
        return response

    def list_bucket(self, bucket):
        self._request(response)
        return response

    def put(self, bucket, key):
        self._request(response)
        return response

    def get(self, bucket, key):
        self._request(response)
        return response

    def head(self, bucket, key):
        self._request(response)
        return response

    def delete(self, bucket, key):
        self._request(response)
        return response
