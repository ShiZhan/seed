#!/usr/bin/python
# -*- coding: utf-8 -*-

"""SEED program utility helper classes and functions

_SEED_LOG:    Global logger for internal use
_init_logger: Configure global logger
VERSION:      Check code version from local repository
DEFAULT_HOST: Get ip address from host configuration
DEFAULT_PORT: Default port
DEFAULT_ID:   ID for personalize RPC connection
DEFAULT_HMAC_KEY: Key for RPC connection without name server 
_node_uri:    Generate node URI for Pyro4 object using ip, port and DEFAULT_ID
is_valid_ipv4_address, is_valid_ipv6_address: Verify IP address
"""

import logging
import os
import time
import socket

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


def _get_ip():
    """get ip address"""
    (hostname, aliaslist, ipaddrlist) = \
        socket.gethostbyname_ex(socket.gethostname())
    return ipaddrlist[0]


DEFAULT_HOST = _get_ip()
DEFAULT_PORT = 10001

DEFAULT_ID = 'SEED'
DEFAULT_HMAC_KEY = 'SEED indentifier'

def _node_uri(ip_address, port, node_id=DEFAULT_ID):
    """Use ip address, port and (optional) node id to generate Pyro URI,
    create connection without Pyro4 name server"""

    return 'PYRO:' + node_id + '@' + ip_address + ':' + str(port)

def is_valid_ipv4_address(ip_address):
    """Verify IPv4 address"""
    try:
        addr = socket.inet_pton(socket.AF_INET, ip_address)
    except AttributeError: # no inet_pton here, sorry
        try:
            addr = socket.inet_aton(ip_address)
        except socket.error:
            return False
        return ip_address.count('.') == 3
    except socket.error: # not a valid address
        return False

    return True

def is_valid_ipv6_address(ip_address):
    """Verify IPv6 address"""
    try:
        addr = socket.inet_pton(socket.AF_INET6, ip_address)
    except socket.error: # not a valid address
        return False
    return True

