#coding=utf-8
"""SeedShell -- Shell program for SEED storage, 
for accessing storage manually, through command line interface. """
import cmd
import os
from tornado.httpclient import HTTPClient
# For running HTTP requests in cmd, rather than AsyncHTTPClient,
# sync method seems to be better.

class SeedShell(cmd.Cmd):
    """SeedShell"""
    intro = "SEED command processor"
    doc_header = 'available commands'
    misc_header = 'misc help'
    undoc_header = 'getting help'
    ruler = '-'

    def __init__(self, shellhost):
        cmd.Cmd.__init__(self)
        self.host = 'http://' + shellhost + '/'
        self.prompt = '[' + shellhost + ']>> '
        self.http_client = HTTPClient()

    def __del__(self):
        self.http_client.close()
        cmd.Cmd.__del__(self)

    def do_shell(self, line):
        """Run a shell command"""
        print "running shell command:", line
        # beware of the decode/encode pair, since 'output' may vary between OSes.
        output = os.popen(line).read()
        print output

    def do_ls(self, line):
        """list objects"""
        # for long help, implement 'def help_greet(self):' instead.
        print "objects: ", line

    def do_put(self, line):
        """put objects"""
        print "objects: ", line

    def do_get(self, line):
        """get objects"""
        try:
            response = self.http_client.fetch(self.host)
            print response.body
        except httpclient.HTTPError, e:
            print "Error:", e

    def do_post(self, line):
        """post object"""
        print "objects: ", line

    def do_delete(self, line):
        """delete objects"""
        print "objects: ", line

    def do_version(self, line):
        """show SEED remote server version"""
        print "WIP"

    def do_status(self, line):
        """show SEED status"""
        try:
            response = self.http_client.fetch(self.host)
            print response.body
        except httpclient.HTTPError, e:
            print "Error:", e

    def do_exit(self, line):
        """exit from shell"""
        return True
