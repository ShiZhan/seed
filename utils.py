#!/usr/bin/python
# -*- coding: utf-8 -*-

"""SEED program utility helper classes and functions

SeedLog:    Global logger for internal use
InitLogger: Configure global logger
Version:    Check code version from local repository
Initialize: Initialize root directory and '.seed' bucket for storing meta data
NodeURI:    Generate node URI for Pyro4 object using ip, port and DefaultID
"""

import os
import time
import logging

# create logger

_SEED_LOG = logging.getLogger('SEED')


def _init_logger():
    """configure global logger"""

    # set level

    _SEED_LOG.setLevel(logging.DEBUG)

    # create console handler and set level to debug

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # create formatter

    formatter = \
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                          )

    # add formatter to console_handler

    console_handler.setFormatter(formatter)

    # add console_handler to logger

    _SEED_LOG.addHandler(console_handler)


def _version():
    """SEED Version"""

    version = ''

    # git or hg-git or hg?

    if os.path.exists('.git'):
        with open('.git/refs/heads/master', mode='r') as git_meta:
            version = ''.join(git_meta.read().split())
    elif os.path.exists('.hg/git'):

        with open('.hg/git/refs/heads/master', mode='r') as hggit_meta:
            version = ''.join(hggit_meta.read().split())
    elif os.path.exists('.hg'):

        with open('.hg/cache/tags', mode='r') as hg_meta:
            version = '.'.join(hg_meta.read()).split()
    else:

        # can't get program version from local repository.
        # use seed script mtime instead

        version = time.ctime(os.stat('seed').st_mtime)

    return version


# program version
VERSION = _version()


# default root directory

DEFAULT_ROOT = os.path.abspath(os.path.join(os.getcwd(), 'storage'))


def _init_root(root):
    """init SEED root"""

    seed_meta_path = os.path.join(root, '.seed')
    if os.path.exists(seed_meta_path):
        _SEED_LOG.warn('already initialized.')
    else:

        os.makedirs(seed_meta_path)

        # setup/update version in self.directory+'/.seed/version'

        version_file_name = seed_meta_path + '/version'
        with open(version_file_name, 'w') as version_file:
            version_file.write(VERSION)

    return


DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 10001

DEFAULT_ID = 'SEED'
DEFAULT_HMAC_KEY = 'SEED indentifier'


def _node_uri(ip_address, port, node_id=DEFAULT_ID):
    """Use ip address, port and (optional) node id to generate Pyro URI,
    create connection without Pyro4 name server"""

    return 'PYRO:' + node_id + '@' + ip_address + ':' + str(port)


