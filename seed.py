#!/usr/bin/env python
#coding=utf-8

#  Copyright 2012 Shi.Zhan
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys
import cmd
from optparse import OptionParser

class SeedShell(cmd.Cmd):
    prompt = '>> '
    intro = "SEED command processor"

    def do_greet(self, line):
        print "hello"

    def do_exit(self, line):
        return True

def main():  
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-d", "--daemon", action="store", dest="daemonport",
                      default="10001",
                      help="start daemon on specified port.")
    parser.add_option("-s", "--shell", action="store", dest="shellhost",
                      help="start shell on specified [host:port].")

    (options, args) = parser.parse_args()  

    if options.shellhost:
        print "connecting to host: %s..." % options.shellhost
        SeedShell().cmdloop()
    else:
        print "starting daemon on port: %s..." % options.daemonport

if __name__ == "__main__":  
    main()
