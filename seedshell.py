#coding=utf-8
import cmd

class SeedShell(cmd.Cmd):
    prompt = '>> '
    intro = "SEED command processor"

    def __init__(self, shellhost):
        cmd.Cmd.__init__(self)
        self.host = shellhost

    def do_greet(self, line):
        print "hello"

    def do_exit(self, line):
        return True
