#!/usr/bin/env python3
"""conflicts.py R001,R002,... -> prints both reviewers' decisions+reasons for those RIDs (from screen/b*-A.json and b*-B.json)."""
import json, glob, os, sys
WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
dec = {}
for f in sorted(glob.glob(os.path.join(WS, 'screen', 'b*-[AB].json'))):
    d = json.load(open(f, encoding='utf-8'))
    for x in d['decisions']:
        dec.setdefault(x['rid'], {})[d['reviewer']] = x
for r in [x.strip() for x in ','.join(sys.argv[1:]).split(',') if x.strip()]:
    print('===', r)
    for rv in ('A', 'B'):
        x = dec.get(r, {}).get(rv)
        print(f"  reviewer {rv}:", (f"{x['decision']} [{x.get('reason_code')}] {x.get('reason')} (dims={x.get('dims')}, depth={x.get('data_depth')})") if x else 'MISSING')
