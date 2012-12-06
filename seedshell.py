#coding=utf-8
import cmd

class SeedShell(cmd.Cmd):
    prompt = '>> '
    intro = "SEED command processor"
    host = '127.0.0.1:10001'

    def do_greet(self, line):
        print "hello"

    def do_exit(self, line):
        return True
