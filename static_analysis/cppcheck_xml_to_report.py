#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# turns Cppcheck output (XML type 2) into report sorted rarest issues first
#
# Usage: xml_to_report <xml_file_name> [> nice_report_file]

import sys

if len(sys.argv) != 2:
        print "Usage: xml_to_report <xml_file_name> [> nice_report_file]"
        sys.exit(1)


f = open(sys.argv[1])
text = f.read()
f.close()

raw_issues = text.split('</error>')[:-1]

id_to_issue = {}
id_to_verbose = {}

def humanize( text ):
        return text.replace('&apos;', '\'').replace('&lt;', '<').replace('&gt;', '>')

for issue in raw_issues:
        issue_id = issue.split('id=\"')[1].split('\"')[0]
        issue_msg = issue.split('msg=\"')[1].split('\"')[0]
        issue_verbose = issue.split('verbose=\"')[1].split('\"')[0]
        issue_file = issue.split('file=\"')[1].split('\"')[0]
        issue_lines = [entry.split('\"')[0] for entry in issue.split('line=\"')[1:]]
        if not issue_id in id_to_issue:
                id_to_issue[issue_id] = [(issue_msg, issue_file, issue_lines)]
                id_to_verbose[issue_id] = issue_verbose
        else:
                id_to_issue[issue_id] += [(issue_msg, issue_file, issue_lines)]

id_and_issues = id_to_issue.items()
id_and_issues.sort(key = lambda (k, v): len(v) )

for (issue_id, issues) in id_and_issues:        
        print '*** ' + issue_id + ' x ' + str(len(issues)) + ' ***'
        print
        print humanize( id_to_verbose[issue_id] )
        print
        for (issue_msg, issue_file, issue_lines) in sorted(issues, key = lambda (m, f, l): f):
                print '\t' + issue_file + ':' + str(issue_lines) + ' - ' + humanize( issue_msg )
        print
        print
        print