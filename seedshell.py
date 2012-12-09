#coding=utf-8
"""SeedShell -- Shell program for SEED storage, 
for accessing storage manually, through command line interface. """
import cmd
from tornado import httpclient

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
        self.http_client = httpclient.HTTPClient()

    def __del__(self):
        self.http_client.close()
        cmd.Cmd.__del__(self)

    def do_ls(self, line):
        """list objects"""
        print "objects: ", line

    def do_put(self, line):
        """put objects"""
        print "objects: ", line

    def do_get(self, line):
        """get objects"""
        print "objects: ", line

    def do_post(self, line):
        """post object"""
        print "objects: ", line

    def do_delete(self, line):
        """delete objects"""
        print "objects: ", line

    def do_version(self, line):
        """show SEED version"""
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
