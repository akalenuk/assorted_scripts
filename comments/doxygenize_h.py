#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# searches for ".h" files in a path non-recursively 
# and puts a third slash in comments that begins from new line
#
# Usage: doxygenize [path]

import os

def doxygenize(where = "."):
        ls = os.listdir(where)
        for path in ls: 
                (root, ext) = os.path.splitext( path )
                if ext.upper() == ".H":
                        print path
                        content = ""
                        with open(path, 'r') as content_file:
                            content = content_file.read()
                        content = content.replace('\n// ', '\n/// ')
                        content = content.replace('\n\t// ', '\n\t/// ')
                        with open(path, 'w') as content_file:
                                content_file.write(content)

if len(sys.argv) > 2:
        print "Usage: doxygenize [path]"
        sys.exit(1)

doxygenize(sys.argv[1] if len(sys.argv) > 1 else ".")