#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# removes ".svn" folders recursively
#
# Usage: cleaning_all_svn [path]

import os
import sys
import shutil

        
def clean_all_svn(where = "."):
        ls = os.listdir(where)
        for l in ls:    
                path = where + '/' + l
                if os.path.isdir( path ):
                        if l == '.svn':
                                print path
                                shutil.rmtree(path)
                        else:
                                clean_all_svn( path )

if len(sys.argv) > 2:
        print 'Usage: cleaning_all_svn [path]'
        sys.exit(1)

clean_all_svn(sys.argv[1] if len(sys.argv) > 1 else ".")


