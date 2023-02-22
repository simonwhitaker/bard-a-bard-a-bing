#!/usr/bin/env python3
#
# This script reads the text of Shakespeare's complete works from a file or
# STDIN, and outputs a JSON document containing the sonnets in line-by-line
# granularity.
#
# The text this script expects as input is available from the MIT OpenCourseWare
# website:
# https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt
#
# The general form of the text is:
#
# THE SONNETS
#
# by William Shakespeare
#
#                      1
#   From fairest creatures we desire increase,
#   That thereby beauty's rose might never die,
#   But as the riper should by time decease,
#   His tender heir might bear his memory:
#   ...etc

import json
import re
import sys

re_sonnet_start = re.compile(r'^THE SONNETS$')
re_sonnet_end = re.compile(r'^THE END$')
re_sonnet_number = re.compile(r'^\s+(\d+)\s*$')
re_sonnet_line = re.compile(r'^\s+(\S.*)$')

is_reading_sonnets = False
sonnet_number = 0
line_number = 0
index = 0
documents = []

# Read from a file if a filename is provided on the command line, else from
# STDIN
if len(sys.argv) > 1:
    filename = sys.argv[1]
    fh = open(filename, 'r')
else:
    fh = sys.stdin

with fh:
    for line in fh:
        if re_sonnet_start.match(line):
            is_reading_sonnets = True
        elif is_reading_sonnets and re_sonnet_end.match(line):
            # We only care about sonnets for now
            break
        elif is_reading_sonnets:
            result = re_sonnet_number.search(line)
            if result:
                sonnet_number = int(result.group(1))
                line_number = 0
                continue
            result = re_sonnet_line.search(line)
            if result:
                line_number += 1
                index += 1
                documents.append({
                    'id': index,
                    'sonnet_number': sonnet_number,
                    'line_number': line_number,
                    'text': result.group(1)
                })

print(json.dumps(documents, indent=2))
