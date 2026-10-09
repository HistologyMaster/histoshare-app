#!/usr/bin/env python3
"""screen_check.py <file> -> validates a screening decision file."""
import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
assert 'batch' in d and 'reviewer' in d and 'decisions' in d
ok = {'include_A', 'include_B', 'exclude', 'uncertain'}
for x in d['decisions']:
    assert x['decision'] in ok, x
    assert x.get('reason'), x
print('OK', len(d['decisions']))
