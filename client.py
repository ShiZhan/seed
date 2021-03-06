#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Seed.client -- client program for SEED storage.
Client:
Implementation of a Simplified S3-like storage client based on Pyro4 RPC.
"""

from Pyro4.core import Proxy
from Pyro4 import config as PyroConfig

from hashring import HashRing

from log import SEED_LOG
from netutil import DEFAULT_HMAC_KEY, DEFAULT_HOST, DEFAULT_PORT, node_uri


class Client(Proxy):

    """XML RPC Client for accessing SEED"""

    def __init__(self, ip_address=DEFAULT_HOST, port=DEFAULT_PORT):
        PyroConfig.HMAC_KEY = DEFAULT_HMAC_KEY
        Proxy.__init__(self, node_uri(ip_address, port))

    # local functions

    def put(self, bucket, key, file_name):
        """put local file to remote bucket:key"""

        SEED_LOG.info('put %s %s %s' % (bucket, key, file_name))

        # 1. write the file to local cache (use memory as many as possible)
        # 2. contact server to decide how to do striping and encoding
        #    in the form of a dict, which is stored in both client and server
        # 3. do the encoding
        # 4. add encoded chunks to transferring queue
        # 5. sync with (multiple) servers
        self.put_meta()

        return

    def get(self, bucket, key):
        """get remote bucket:key to local file"""

        SEED_LOG.info('get %s %s' % (bucket, key))

        # 1. contact server to decide where to get the chunks and do decoding
        #    in the form of a dict, which is then cached in client
        # 2. download chunks to local cache (use memory as many as possible)
        # 3. do the decoding and save the file
        self.get_meta()

        return


