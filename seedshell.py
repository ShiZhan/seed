#coding=utf-8
"""SeedShell -- Shell program for SEED storage, 
for accessing storage manually, through command line interface. """
import cmd

class SeedShell(cmd.Cmd):
    """SeedShell"""
    intro = "SEED command processor"
    doc_header = 'command usage'
    misc_header = 'misc help'
    undoc_header = 'available commands'
    ruler = '-'

    def __init__(self, shellhost):
        cmd.Cmd.__init__(self)
        self.host = shellhost
        self.prompt = '[' + shellhost + ']>> '

    def do_greet(self, line):
        """greet testing command"""
        print "hello", line

    def do_version(self, line):
        """show SEED version"""
        print "WIP"

    def do_exit(self, line):
        """exit from shell"""
        return True
