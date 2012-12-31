#coding=utf-8
"""SEED program utility helper classes and functions

Version: Check code version from local repository
"""
import os
import time

class Version(object):
    """SEED Version"""
    def __init__(self):
        super(Version, self).__init__()
        self.version = ''
        
        # git or hg-git or hg?
        if os.path.exists('.git'):
            with open('.git/refs/heads/master', mode='r') as git_meta:
                self.version = git_meta.read()

        elif os.path.exists('.hg/git'):
            with open('.hg/git/refs/heads/master', mode='r') as hggit_meta:
                self.version = hggit_meta.read()

        elif os.path.exists('.hg'):
            with open('.hg/cache/tags', mode='r') as hg_meta:
                self.version = '.'.join(hg_meta.read()).split()

        else:
            # can't get program version from local repository.
            # use seed script mtime instead
            self.version = time.ctime(os.stat('seed').st_mtime)
