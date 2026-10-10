#!/usr/bin/env python3
"""Builds extract/db.json: all included records with extraction (or title-only stub) + bibliographic metadata."""
import json, glob, os, re
WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
C = {m['rid']: m for m in json.load(open(os.path.join(WS, 'corpus.json'), encoding='utf-8'))}
F = json.load(open(os.path.join(WS, 'screen', 'final.json')))
plan = json.load(open(os.path.join(WS, 'screen', 'extraction_plan.json')))
ex = {}
for f in sorted(glob.glob(os.path.join(WS, 'extract', 'e[AB]*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    for r in d['records']: ex[r['rid']] = r
db = {}
for rid, fin in F.items():
    if fin.get('final') not in ('A', 'B'): continue
    m = C[rid]
    rec = {'rid': rid, 'tier': fin['final'], 'screen_reason': fin.get('reason'), 'bib': {k: m.get(k) for k in ('title', 'authors', 'year', 'journal', 'volume', 'pages', 'doi', 'pmid', 'pmcid', 'language', 'bibliographic_verified', 'verified_via', 'access_best', 'as_cited_in')}}
    if rid in ex:
        rec['extraction'] = ex[rid]
    elif rid in plan['stubA']:
        rec['extraction'] = {'rid': rid, 'data_depth': 'metadata_only', 'about_paraphysis': 'title_only', 'study_type': 'unknown', 'findings': [], 'mentions': [], 'include_in_synthesis': 'identified_only', 'caveats': 'Only bibliographic metadata (title/authors/year/journal) available; content NOT verified. May be cited as an identified work, never for findings.', 'duplicate_of': ''}
    else:
        rec['extraction'] = None
    e = rec['extraction']
    if e:
        for i, mm in enumerate(e.get('mentions', []), 1): mm['id'] = f'{rid}.m{i}'
    db[rid] = rec
json.dump(db, open(os.path.join(WS, 'extract', 'db.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
import collections
print('records', len(db), 'with extraction', sum(1 for v in db.values() if v['extraction']), 'missing', [k for k, v in db.items() if not v['extraction']])
print(collections.Counter((v['tier'], (v['extraction'] or {}).get('include_in_synthesis')) for v in db.values()))
