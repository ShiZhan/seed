#coding=utf-8
"""SEED program utility helper classes and functions

Version: Check code version from local repository
Initialize: Initialize '.seed' bucket for holding meta data
"""
import os
import time

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

def Initialize(root):
    """init SEED root"""
    seed_meta_path = root + '/.seed'
    if os.path.exists(seed_meta_path):
        print 'already initialized.'

    else:
        os.mkdir(seed_meta_path)
        # setup/update version in self.directory+'/.seed/version'
        version_file_name = seed_meta_path + '/version'
        with open(version_file_name, 'w') as version_file:
            version_file.write(Version())
    pass

