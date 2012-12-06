#!/usr/bin/env python
#coding=utf-8
#
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
import re
from optparse import OptionParser # in python >= 2.7, use argparser instead.
from seedshell import SeedShell
from seeddaemon import SeedDaemon

def main():

  usage = "usage: %prog [options] arg"
  parser = OptionParser(usage)
  # the default option is 'daemon', more options must be explicitly given.
  parser.add_option("-d", "--daemon", action="store", dest="daemonport",
                    default="10001",
                    help="start daemon on specified port")
  parser.add_option("-s", "--shell", action="store", dest="shellhost",
                    help="start shell on specified [host:port]")

  (options, args) = parser.parse_args()

  if options.shellhost:
    # check valid IP
    valid_host = re.compile('^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}:\d+$')
    if valid_host.search(options.shellhost):
      print "connecting to host: %s..." % options.shellhost

      # run the shell with host specified
      SeedShell(options.shellhost).cmdloop()
    else:
      # host invalid, do nothing
      print "invalid parameter: '%s', must be 'IP:port' as '127.0.0.1:10001'." % options.shellhost
  else:
    # check valid port

    print "starting daemon on port: %s..." % options.daemonport
    # run the daemon on specified port

    SeedDaemon('test')

if __name__ == "__main__":
  main()
