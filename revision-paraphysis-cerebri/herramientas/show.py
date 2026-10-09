#!/usr/bin/env python3
"""show.py R001,R002,...  -> prints compact records from corpus.json for screening/extraction.
   show.py --range R001 R030   -> prints a contiguous range."""
import json, os, sys
WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
C = json.load(open(os.path.join(WS, 'corpus.json'), encoding='utf-8'))
by = {m['rid']: m for m in C}
a = sys.argv[1:]
if a and a[0] == '--range':
    lo, hi = int(a[1][1:]), int(a[2][1:]); rids = [f'R{i:03d}' for i in range(lo, hi + 1)]
else:
    rids = [x.strip() for x in ','.join(a).split(',') if x.strip()]
for r in rids:
    m = by.get(r)
    if not m: print(r, 'NOT FOUND'); continue
    print(f"--- {m['rid']} | {m['year']} | {m['authors'][:80]}")
    print(f"TITLE: {m['title']}")
    print(f"JOURNAL: {m['journal']} {m['volume']}:{m['pages']} | PMID={m['pmid'] or '-'} DOI={m['doi'] or '-'} PMC={m.get('pmcid') or '-'}")
    print(f"ACCESS: {m['access_best']} | verified={m['bibliographic_verified']} | finder-relevance votes={m['relevance_votes']} | dims={m['dims']}")
    if m.get('notes'): print('FINDER NOTES:', ' || '.join(m['notes'][:3])[:500])
    if m.get('as_cited_in'): print('AS CITED IN:', '; '.join(m['as_cited_in'])[:200])
    print('EXCERPT:', (m.get('excerpt') or '(none)')[:700])
