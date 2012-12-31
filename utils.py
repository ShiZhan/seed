#coding=utf-8
"""SEED program utility helper classes and functions

Version: Check code version from local repository
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
    if os.path.exists(root + '.seed'):
        print 'already initialized.'

    else:
        # setup/update version in self.directory+'.seed/version'
        print Version()
    pass

