#coding=utf-8
"""SeedShell -- Shell program for SEED storage, 
for accessing storage manually, through command line interface. """
import cmd

class SeedShell(cmd.Cmd):
    """SeedShell"""
    intro = "SEED command processor"
    doc_header = 'available commands'
    misc_header = 'misc help'
    undoc_header = 'getting help'
    ruler = '-'

    def __init__(self, shellhost):
        cmd.Cmd.__init__(self)
        self.host = shellhost
        self.prompt = '[' + shellhost + ']>> '

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

    def do_exit(self, line):
        """exit from shell"""
        return True
