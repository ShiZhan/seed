#coding=utf-8
"""Seed.Shell -- Shell program for SEED storage, 
for accessing storage manually, through command line interface. """
import os
from cmd import Cmd
from client import Client

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
        self.connection = Client(server=server, port=port)
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
        response = None
        if "" == line:
            response = self.connection.list_all_my_buckets()
            print 'None' if (None == response) else response.body
        else:
            parameters = line.split()
            if 1 == len(parameters):
                response = self.connection.list_bucket(parameters[0])
                print 'None' if (None == response) else response.body
            elif 2 == len(parameters):
                response = self.connection.head(parameters[0], parameters[1])
                print 'None' if (None == response) else response.body
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
        response = None
        parameters = line.split()
        if len(parameters) < 2:
            print "parameter not enough, need '[bucket] [key]'."
        else:
            response = self.connection.get(parameters[0], parameters[1])
            print "get [bucket: %s], [key: %s]" % (parameters[0], parameters[1])
            print 'None' if (None == response) else response.body

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
            response = None
            if 1 == len(parameters):
                response = self.connection.delete_bucket(parameters[0])
                print 'None' if (None == response) else response.body
            elif 2 == len(parameters):
                response = self.connection.delete(parameters[0], parameters[1])
                print 'None' if (None == response) else response.body
            else:
                print "parameter exceeded, need '[bucket] [key]'."

    def do_version(self, line):
        """show SEED remote server version"""
        response = self.connection.get('.seed', 'version')
        print 'None' if (None == response) else response.body

    def do_status(self, line):
        """show SEED status"""
        response = self.connection.get('.seed', 'status')
        print 'None' if (None == response) else response.body

    def do_exit(self, line):
        """exit from shell"""
        return True
