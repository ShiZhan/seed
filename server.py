#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Seed.server -- metadata and data server program for SEED storage.

Server:
Implementation of a Simplified S3-like storage server based on local files.
"""

import os
from datetime import datetime

from Pyro4.core import Daemon
from Pyro4 import config as PyroConfig

from model import Graph
from model import URIRef, Literal, BNode
from model import RDF, RDFS, OWL, XSD
from model import SEED_BASE

from log import _SEED_LOG
from netutil import DEFAULT_ID, DEFAULT_HMAC_KEY


class Server(Daemon):

    """XML RPC Server for SEED"""

    def __init__(self, ip_address, port, model_file):
        PyroConfig.HMAC_KEY = DEFAULT_HMAC_KEY
        Daemon.__init__(self, host=ip_address, port=port)

        # register(Obj, ID) 2nd parameter 'ID' cannot be empty

        uri = self.register(S3Handler(model_file), DEFAULT_ID)

        _SEED_LOG.info('Server URI: %s' % uri)

    def run(self):
        """enter server loop"""

        _SEED_LOG.info('Request loop ...')

        self.requestLoop()


class S3Handler(object):

    """SEED handler class for remote invoking"""

    def __init__(self, model_file):
        # try to load node model
        self._model = Graph()

        try:
            self._model.load(model_file)

        except Exception, e:

            _SEED_LOG.error('Loading Exception: %s' % e)

            _SEED_LOG.info('try "seed -i" to reinitialize model')

            raise e

        self._base_uri = \
            self._model.value(predicate=RDF.type, object=OWL.Ontology)

        _SEED_LOG.info('Server model: %s' % self._base_uri)

        self._version = \
            self._model.value(subject=self._base_uri, predicate=OWL.versionInfo)

        _SEED_LOG.info('Server version: %s' % self._version)

    # s3-like functions

    def list_all_my_buckets(self):
        names = os.listdir(self.directory)
        buckets = []
        for name in names:
            path = os.path.join(self.directory, name)
            info = os.stat(path)
            buckets.append('Name: ' + name + ' CreationDate: '
                           + datetime.utcfromtimestamp(info.st_ctime).ctime())
        return '\n'.join(buckets)

    def check_bucket_exists(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or not os.path.isdir(path):
            response = 404
        else:
            response = 200

        return response

    def create_bucket(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or os.path.exists(path):
            response = 403
        else:
            os.makedirs(path)
            response = 200

        return response

    def delete_bucket(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or not os.path.isdir(path):
            response = 404
        elif len(os.listdir(path)) > 0:
            response = 403
        else:
            os.rmdir(path)
            response = 204

        return response

    def list_bucket(self, bucket):
        path = os.path.abspath(os.path.join(self.directory, bucket))
        if not path.startswith(self.directory) or not os.path.isdir(path):
            return ''
        object_names = []
        for (root, dirs, files) in os.walk(path):
            for file_name in files:
                object_names.append(os.path.join(root, file_name))

        return '\n'.join(object_names)

    def head(self, bucket, key):
        path = os.path.abspath(os.path.join(self.directory, bucket, key))
        if not path.startswith(self.directory) or not os.path.isfile(path):
            response = 404
        else:
            response = 200

        return response

    def delete(self, bucket, key):
        path = os.path.abspath(os.path.join(self.directory, bucket, key))
        if not path.startswith(self.directory) or not os.path.isfile(path):
            response = 404
        else:
            os.unlink(path)
            response = 204

        return response

    # get/put functions, metadata phase

    def get_meta():
        return

    def put_meta():
        return

    # chunk transferring functions

    def get_trunk():
        return

    def put_trunk():
        return

    # system functions

    def version(self):
        """show server version"""
        return self._version

    def status(self):
        """show server status"""
        return 'OK'

