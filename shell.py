#coding=utf-8
"""Seed.Shell -- Shell program for SEED storage, 
for accessing storage manually, through command line interface. """
import os
from cmd import Cmd
from s3client import AWSAuthConnection
from s3client import CallingFormat

class Shell(Cmd):
    """Seed.Shell"""
    # cmd internal settings
    intro = "SEED command processor"
    doc_header = 'available commands'
    misc_header = 'misc help'
    undoc_header = 'getting help'
    ruler = '-'

    # command parameters
    parameters = []

    def __init__(self, server="127.0.0.1", port=10001):
        Cmd.__init__(self)
        self.prompt = '[' + server + ':' + str(port) + ']>> '
        self.connection = AWSAuthConnection(
            "", "", server=server, port=port, is_secure=False,
            calling_format=CallingFormat.PATH)
        self.connection.check_bucket_exists('.seed')
        print self.connection, " initialized"

    # def __del__(self):
    #     self.connection.__del__()
    #     Cmd.__del__(self)

    # for long help, implement 'def help_greet(self):' instead.
    def do_shell(self, line):
        """Run a shell command"""
        print "running shell command:", line
        # beware of the decode/encode pair, since 'output' may vary between OSes.
        output = os.popen(line).read()
        print output

    def do_ls(self, line):
        """list objects"""
        if "" == line:
            bucket_list = self.connection.list_all_my_buckets()
            print bucket_list.body
        else:
            parameters = line.split()
            if 1 == len(parameters):
                item_list = self.connection.list_bucket(parameters[0])
                print item_list.body
            elif 2 == len(parameters):
                item_head = self.connection.head(parameters[0], parameters[1])
                print item_head.body
            else:
                print "parameter exceeded, need '[bucket] [key]'."

    def do_put(self, line):
        """put objects"""
        parameters = line.split()
        if len(parameters) < 3:
            print "parameter not enough, need '[bucket] [key] [value]'."
        else:
            self.connection.put(parameters[0], parameters[1], parameters[2])
            print "put %s=%s into %s" % (parameters[1], parameters[2], parameters[0])

    def do_get(self, line):
        """get objects"""
        parameters = line.split()
        if len(parameters) < 2:
            print "parameter not enough, need '[bucket] [key]'."
        else:
            item = self.connection.get(parameters[0], parameters[1])
            print "get [bucket: %s], [key: %s]" % (parameters[0], parameters[1])
            print item.body

    def do_create(self, line):
        """create bucket"""
        parameters = line.split()
        if len(parameters) < 1:
            print "parameter not enough, need '[bucket]'."
        else:
            self.connection.create_bucket(parameters[0])
            print "bucket '%s' created" % parameters[0]

    def do_delete(self, line):
        """delete objects"""
        if "" == line:
            print "parameter not enough, need '[bucket] [key]'."
        else:
            parameters = line.split()
            if 1 == len(parameters):
                item_list = self.connection.delete_bucket(parameters[0])
                print item_list.body
            elif 2 == len(parameters):
                item_head = self.connection.delete(parameters[0], parameters[1])
                print item_head.body
            else:
                print "parameter exceeded, need '[bucket] [key]'."

    def do_version(self, line):
        """show SEED remote server version"""
        print "WIP"

    def do_status(self, line):
        """show SEED status"""
        print "WIP"

    def do_exit(self, line):
        """exit from shell"""
        return True
