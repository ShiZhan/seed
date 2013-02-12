#!/usr/bin/python
# -*- coding: utf-8 -*-

"""SEED log functions

SEED_LOG:    Global logger for internal use
init_logger: Configure global logger
"""

import logging

# create logger

SEED_LOG = logging.getLogger('SEED')

def init_logger():
    """configure global logger"""

    # set level

    SEED_LOG.setLevel(logging.DEBUG)

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

    SEED_LOG.addHandler(console_handler)
