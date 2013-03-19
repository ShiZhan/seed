#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Seed.shell -- Shell program for SEED storage, 
for accessing storage manually, through command line interface. """

import os
from cmd import Cmd
from client import Client


class Shell(Cmd):

    """Seed.Shell"""

    # cmd internal settings

    intro = 'SEED command processor'
    doc_header = 'available commands'
    misc_header = 'misc help'
    undoc_header = 'getting help'
    ruler = '-'

    # command parameters

    parameters = []

    def __init__(self, ip_address, port):
        Cmd.__init__(self)
        self.prompt = '[' + ip_address + ':' + str(port) + ']>> '
        self.client = Client(ip_address=ip_address, port=port)
        result = self.client.status()
        print 'server report: %s' % result

    # def __del__(self):
    #     self.client.__del__()
    #     Cmd.__del__(self)

    # for long help, implement 'def help_greet(self):' instead.

    def do_shell(self, line):
        """Run a shell command"""

        print 'running shell command:', line

        # beware of the encoding, since 'output' may vary between shell/OSes.

        output = os.popen(line).read()
        print output

    def do_ls(self, line):
        """list objects"""

        if '' == line:
            print self.client.list_all_my_buckets()
        else:
            parameters = line.split()
            if 1 == len(parameters):
                print self.client.list_bucket(parameters[0])
            elif 2 == len(parameters):
                print self.client.head(parameters[0], parameters[1])
            else:
                print "parameter exceeded, need '[bucket] [key]'."

    def do_put(self, line):
        """put objects"""

        parameters = line.split()
        if len(parameters) < 3:
            print "parameter not enough, need '[bucket] [key] [value]'."
        else:
            self.client.put(parameters[0], parameters[1], parameters[2])
            print 'put %s=%s into %s' % (parameters[1], parameters[2],
                    parameters[0])

    def do_get(self, line):
        """get objects"""

        parameters = line.split()
        if len(parameters) < 2:
            print "parameter not enough, need '[bucket] [key]'."
        else:
            self.client.get(parameters[0], parameters[1])
            print 'get [bucket: %s], [key: %s]' % (parameters[0],
                    parameters[1])

    def do_create(self, line):
        """create bucket"""

        parameters = line.split()
        if len(parameters) < 1:
            print "parameter not enough, need '[bucket]'."
        else:
            self.client.create_bucket(parameters[0])
            print "bucket '%s' created" % parameters[0]

    def do_delete(self, line):
        """delete objects"""

        if '' == line:
            print "parameter not enough, need '[bucket] [key]'."
        else:
            parameters = line.split()
            if 1 == len(parameters):
                self.client.delete_bucket(parameters[0])
                print "bucket '%s' deleted" % parameters[0]
            elif 2 == len(parameters):
                self.client.delete(parameters[0], parameters[1])
                print "key '%s::%s' deleted" % (parameters[0],
                        parameters[1])
            else:
                print "parameter exceeded, need '[bucket] [key]'."

    def do_version(self, line):
        """show SEED remote server version"""

        print self.client.version()

    def do_status(self, line):
        """show SEED status"""

        print self.client.status()

    def do_exit(self, line):
        """exit from shell"""

        return True


