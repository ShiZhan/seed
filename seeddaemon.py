#coding=utf-8
"""SeedDaemon -- Daemon program for SEED storage, 
client, name server and data server all-in-one. """

class SeedDaemon(object):
    """SeedDaemon"""
    def __init__(self, arg):
        super(SeedDaemon, self).__init__()
        self.arg = arg
