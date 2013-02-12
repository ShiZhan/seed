#!/usr/bin/python
# -*- coding: utf-8 -*-

"""SEED program utility helper classes and functions

VERSION:      Check code version from local repository
"""

import os
import time

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
