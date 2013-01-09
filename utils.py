#coding=utf-8
"""SEED program utility helper classes and functions

SeedLog: Global logger for internal use
InitLogger: Configure global logger
Version: Check code version from local repository
Initialize: Initialize '.seed' bucket for holding meta data
NodeURI: Generate node URI for Pyro4 object using ip, port and DefaultID
"""
import os
import time
import logging

# create logger
SeedLog = logging.getLogger('SEED logger')

def InitLogger():
    """configure global logger"""
    # set level
    SeedLog.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    SeedLog.addHandler(ch)

def Version():
    """SEED Version"""
    version = ''
    
    # git or hg-git or hg?
    if os.path.exists('.git'):
        with open('.git/refs/heads/master', mode='r') as git_meta:
            version = git_meta.read()

    elif os.path.exists('.hg/git'):
        with open('.hg/git/refs/heads/master', mode='r') as hggit_meta:
            version = hggit_meta.read()

    elif os.path.exists('.hg'):
        with open('.hg/cache/tags', mode='r') as hg_meta:
            version = '.'.join(hg_meta.read()).split()

    else:
        # can't get program version from local repository.
        # use seed script mtime instead
        version = time.ctime(os.stat('seed').st_mtime)

    return version

# default root directory
DEFAULT_ROOT = os.path.abspath(os.path.join(os.getcwd(), 's3'))

def Initialize(root):
    """init SEED root"""
    seed_meta_path = os.path.join(root, '.seed')
    if os.path.exists(seed_meta_path):
        SeedLog.warn('already initialized.')

    else:
        os.mkdir(seed_meta_path)
        # setup/update version in self.directory+'/.seed/version'
        version_file_name = seed_meta_path + '/version'
        with open(version_file_name, 'w') as version_file:
            version_file.write(Version())

    return

DEFAULT_ID = "SEED"
DEFAULT_HMAC_KEY = 'SEED indentifier'

def NodeURI(ip, port, id = DEFAULT_ID):
    """Use IP:Port as node name, create connection without Pyro4 name server"""
    return 'PYRO:' + DEFAULT_ID + '@' + ip + ':' + str(port)
