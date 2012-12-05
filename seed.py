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
import json
from optparse import OptionParser

def main():  
    usage = "usage: %prog [options] arg"  
    parser = OptionParser(usage)  
    parser.add_option("-f", "--file", dest="filename",  
                      help="read data from FILENAME")  
    parser.add_option("-v", "--verbose",  
                      action="store_true", dest="verbose")  
    parser.add_option("-q", "--quiet",  
                      action="store_false", dest="verbose")  

    (options, args) = parser.parse_args()  
    if len(args) != 1:  
        parser.error("incorrect number of arguments")  
    if options.verbose:  
        print "reading %s..." % options.filename  
  
if __name__ == "__main__":  
    main()
