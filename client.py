#coding=utf-8
"""Seed.client -- client program for SEED storage.
Client:
Implementation of a Simplified S3-like storage client based on HTTPClient.
"""
from Pyro4.core import Proxy
from Pyro4 import config as PyroConfig

from utils import _SEED_LOG, _node_uri
from utils import DEFAULT_HMAC_KEY

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 10001

class Client(Proxy):
    """XML RPC Client for accessing SEED"""
    def __init__(self, ip_address=DEFAULT_HOST, port=DEFAULT_PORT):
        PyroConfig.HMAC_KEY = DEFAULT_HMAC_KEY
        Proxy.__init__(self, _node_uri(ip_address, port))

    # local functions
    def put(self, bucket, key, file_name):
        """put local file to remote bucket:key"""
        _SEED_LOG.info("put %s %s %s" % (bucket, key, file_name))
        return

    def get(self, bucket, key):
        """get remote bucket:key to local file"""
        _SEED_LOG.info("get %s %s" % (bucket, key))
        return
