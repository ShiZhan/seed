#coding=utf-8
"""Seed.client -- client program for SEED storage.
Client:
Implementation of a Simplified S3-like storage client based on HTTPClient.
"""
from tornado.httpclient import AsyncHTTPClient

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 10001

class Client(object):
    """ClientApplication for accessing SEED"""
    def __init__(self, server=DEFAULT_HOST, port=DEFAULT_PORT):
        self.http_client = AsyncHTTPClient()
        self.url_base = 'http://' + server + ':' + str(port)

    # private methods
    def _request(self, body):
        self.http_client.fetch(self.url_base,
                               callback=(yield Callback("_to_get_key")))
        response = yield Wait("_to_get_key")
        body = response.body

    # public methods
    def list_all_my_buckets(self):
        body = ''
        self._request(body)
        return body

    def check_bucket_exists(self, bucket):
        body = ''
        self._request(body)
        return body

    def create_bucket(self, bucket):
        body = ''
        self._request(body)
        return body

    def delete_bucket(self, bucket):
        body = ''
        self._request(body)
        return body

    def list_bucket(self, bucket):
        body = ''
        self._request(body)
        return body

    def put(self, bucket, key):
        body = ''
        self._request(body)
        return body

    def get(self, bucket, key):
        body = ''
        self._request(body)
        return body

    def head(self, bucket, key):
        body = ''
        self._request(body)
        return body

    def delete(self, bucket, key):
        body = ''
        self._request(body)
        return body
