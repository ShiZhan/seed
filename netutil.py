#!/usr/bin/python
# -*- coding: utf-8 -*-

"""SEED network utility helper classes and functions

DEFAULT_HOST: Get ip address from host configuration
DEFAULT_PORT: Default port
DEFAULT_ID:   ID for personalize RPC connection
DEFAULT_HMAC_KEY: Key for RPC connection without name server 
_node_uri:    Generate node URI for Pyro4 object using ip, port and DEFAULT_ID
is_valid_ipv4_address, is_valid_ipv6_address: Verify IP address
"""

import socket

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
