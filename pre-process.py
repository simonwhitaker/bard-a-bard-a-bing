#!/usr/bin/env python3

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

if len(sys.argv) > 1:
    filename = sys.argv[1]
    fh = open(filename, 'r')
else:
    fh = sys.stdin

with fh:
    for line in fh:
        if re_sonnet_start.match(line):
            is_reading_sonnets = True
        elif re_sonnet_end.match(line):
            is_reading_sonnets = False
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
