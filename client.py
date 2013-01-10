#coding=utf-8
"""Seed.client -- client program for SEED storage.
Client:
Implementation of a Simplified S3-like storage client based on HTTPClient.
"""
from Pyro4.core import Proxy
from Pyro4 import config as PyroConfig

from utils import NodeURI, DEFAULT_HMAC_KEY

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 10001

class Client(Proxy):
    """XML RPC Client for accessing SEED"""
    def __init__(self, ip=DEFAULT_HOST, port=DEFAULT_PORT):
        PyroConfig.HMAC_KEY = DEFAULT_HMAC_KEY
        Proxy.__init__(self, NodeURI(ip, port))

    # local functions
    def put(self, bucket, key, value):
        return

    def get(self, bucket, key):
        return
