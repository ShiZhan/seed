#coding=utf-8
"""Seed.client -- client program for SEED storage.
Client:
Implementation of a Simplified S3-like storage client based on HTTPClient.
"""
import urllib
from tornado.httpclient import HTTPClient
from tornado.httpclient import HTTPError

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 10001

class Client(object):
    """ClientApplication for accessing SEED"""
    def __init__(self, server=DEFAULT_HOST, port=DEFAULT_PORT):
        self.http_client = HTTPClient()
        self.url_base = 'http://' + server + ':' + str(port) + '/'

    # private methods
    def _request(self, url, method='GET', body=None):
        response = None

        try:
            response = self.http_client.fetch(url, method=method, body=body)
        except HTTPError, e:
            print "Error:", e

        return response

    # public methods
    def list_all_my_buckets(self):
        return self._request(self.url_base)

    def check_bucket_exists(self, bucket):
        url_bucket = self.url_base + bucket + '/'
        return self._request(url_bucket, method='HEAD')

    def create_bucket(self, bucket):
        url_bucket = self.url_base + bucket + '/'
        return self._request(url_bucket, method='PUT')

    def delete_bucket(self, bucket):
        url_bucket = self.url_base + bucket + '/'
        return self._request(url_bucket, method='DELETE')

    def list_bucket(self, bucket):
        url_bucket = self.url_base + bucket + '/'
        return self._request(url_bucket)

    def put(self, bucket, key, value):
        url_key = self.url_base + bucket + '/' + key
        data = urllib.urlencode(value)
        return self._request(url_key, method='PUT', body=data)

    def get(self, bucket, key):
        url_key = self.url_base + bucket + '/' + key
        return self._request(url_key)

    def head(self, bucket, key):
        url_key = self.url_base + bucket + '/' + key
        return self._request(url_key, method='HEAD')

    def delete(self, bucket, key):
        url_key = self.url_base + bucket + '/' + key
        return self._request(url_key, method='DELETE')
