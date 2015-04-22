#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# counts lines in text files found recursively in the given path by their masks
#
# Usage: count_lines <path> <mask1> [mask2] ... [maskN]

import sys
import os

def match(pattern, line):       # works for '*' and '?'
        def find_with_question(pattern, line, start = 0):
                if len(pattern) > len(line):
                        return -1
                differences = [1 for (a,b) in zip(pattern, line) if a != b and a != '?']
                if differences == []:
                        return start
                return find_with_question(pattern, line[1:], start+1)

        chunks = ('\0' + pattern + '\0').split("*") 
        
        def check_order(chunks, line):
                if chunks == []:
                        return True
                n = find_with_question(chunks[0], line)
                if n < 0:
                        return False
                return check_order(chunks[1:], line[n + len(chunks[0]):])
        
        return check_order(chunks, '\0' + line + '\0')

        
def count_all( where, masks ):
        lines_count = 0
        ls = os.listdir(where)
        names = []
        for arg in masks:
                names += [name for name in ls if match(arg, name)]
        for name in ls:
                path = where + '/' + name
                if os.path.isfile( path ) and name in names:
                        f = open(path)
                        lines_count += len(f.readlines())
                        f.close()                       
                if os.path.isdir( path ):
                        lines_count += count_all(path, masks)
        return lines_count
        

if len(sys.argv) < 3:
        print "Usage: count_lines <path> <mask1> [mask2] ... [maskN]"
else:
        print count_all(sys.argv[1], sys.argv[2:])