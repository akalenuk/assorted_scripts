#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# searches for ".c", ".cpp", and ".h" files recursively and
# changes C++ style comments "//" to C style comments "/* */"
#
# Usage: cpp_to_c [path]

import os, sys


def do_one_line(line):
        line = line.replace('*//*', '*/ /*')
        if line.find('//') == -1:
                return line.rstrip()
        while line.find('///') >=0:
                line = line.replace('///', '//')
        left_right = line.rstrip().split('//')
        return left_right[0] + '/*' + '//'.join(left_right[1:]) + ' */'

def do_one(path):
        lines = []
        for line in open(path):
                lines += [do_one_line(line)]
        f = open(path, 'w')
        f.write('\n'.join(lines))
        f.close()

def do_all(where = "."):
        ls = os.listdir(where)
        for l in ls:    
                path = where + '/' + l
                if os.path.isfile( path ):
                        (root, ext) = os.path.splitext( path )
                        if ext.upper() == ".C" or ext.upper() == ".H":
                                print path 
                                do_one( path )
                if os.path.isdir( path ):
                        do_all( path )
                
if len(sys.argv) > 2:
        print "Usage: cpp_to_c [path]"
        sys.exit(1)

do_all(sys.argv[1] if len(sys.argv) > 1 else ".")