#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# counts literally copypaste: strings that occur more than once in a code
#
# Usage: count_copypaste [path]

import os, sys

line_map = {}
total_lines = 0
total_copies = 0

def collect_from(fname):
        global line_map, total_lines, total_copies
        f = open(fname)
        lines = f.readlines()
        f.close()
        for n, line in enumerate(lines):
                sl = line.strip()
                if sl == "" or sl =="{" or sl =="}":
                        continue
                if sl[0] == "#":
                        continue
                if sl[:2] == "//":
                        continue
                total_lines += 1
                if sl in line_map:
                        line_map[ sl ] += [(fname, n)]
                        total_copies += 1
                else:
                        line_map[ sl ] = [(fname, n)]
        
        
def collect_all(where = "."):
        ls = os.listdir(where)
        for l in ls:    
                path = where + '/' + l
                if os.path.isfile( path ):
                        (root, ext) = os.path.splitext( path )
                        if ext.upper() == ".CPP" or ext.upper() == ".H" or ext.upper() == ".C" \
                        or ext.upper() == ".ML" or ext.upper() == ".D" or ext.upper() == ".MLI"\
                        or ext.upper() == ".PY" or ext.upper() == ".HRL" or ext.upper() == ".ERL":
                                sys.stderr.write( path + '\n')
                                collect_from( path )
                if os.path.isdir( path ):
                        collect_all( path )
        

if len(sys.argv) > 2:
        print 'Usage: count_copypaste [path]'
        sys.exit(1)

collect_all(sys.argv[1] if len(sys.argv) > 1 else ".")


print "SLOC: ", total_lines
print "Copied: ", total_copies
print "%: ", 100 * total_copies / total_lines
print 

cps = sorted( [(k, v) for k,v in line_map.items() if len(v) > 1], key = lambda(kv):len(kv[1]))

for k,v in cps:
        print k
        for (fname, n) in v:
                print "\t", fname, n
        print