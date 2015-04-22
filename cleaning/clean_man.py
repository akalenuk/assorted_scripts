#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# cleans up a unix `man` command output for reading as a plain text
#
# Usage: clean_man <some_man_output>

import sys
import time

n = 0
if len(sys.argv) != 2:
        print "Usage: clean_man <some_man_output>"
else:
        for line in open(sys.argv[1], 'rb'):
                new_line = ''
                for c in line:
                        if ord(c) == 8:
                             new_line = new_line[:-1]
                        else:
                             if ord(c) != 10:           
                                     new_line += c
                print new_line
