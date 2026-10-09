#!/usr/bin/env python3
"""dbshow.py [--dims d1,d2] [--rids R1,R2] [--identified] [--no-context]
Prints the extraction database for writers. Records with findings in the requested dims, plus title-only identified works (with --identified)."""
import json, os, sys, argparse
WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
db = json.load(open(os.path.join(WS, 'extract', 'db.json'), encoding='utf-8'))
ap = argparse.ArgumentParser(); ap.add_argument('--dims'); ap.add_argument('--rids'); ap.add_argument('--identified', action='store_true'); ap.add_argument('--all', action='store_true')
a = ap.parse_args()
dims = set(a.dims.split(',')) if a.dims else None
rids = set(a.rids.split(',')) if a.rids else None
def head(r):
    b = r['bib']; au = (b['authors'] or '').split(',')[0].strip()
    return f"[{r['rid']}] {au} {b['year'] or 's.f.'} | {b['journal'] or ''} | {(b['title'] or '')[:110]}"
n = 0
for rid, r in sorted(db.items()):
    e = r['extraction']
    if not e: continue
    if rids and rid not in rids: continue
    stub = e.get('include_in_synthesis') == 'identified_only'
    if stub:
        if a.identified or (rids and rid in rids) or a.all:
            print(head(r)); print('   IDENTIFIED ONLY (title/metadata; content unverified) - cite only to state that the work exists / its title scope. screen note:', (r.get('screen_reason') or '')[:160]); n += 1
        continue
    if e.get('include_in_synthesis') == 'no' and not rids and not a.all: continue
    fs = [f for f in e.get('findings', []) if (not dims or f['dim'] in dims)]
    ms = e.get('mentions', []) if (not dims or a.all or rids) else []
    if dims and not fs and not (ms and 'terminology' in dims): continue
    b = r['bib']
    print(head(r))
    print(f"   tier={r['tier']} depth={e['data_depth']} about={e['about_paraphysis']} type={e['study_type']} bib_verified={b['bibliographic_verified']} PMID={b['pmid'] or '-'} DOI={b['doi'] or '-'}")
    print('   taxa:', '; '.join(f"{t['name']} ({t['group']})" for t in e.get('taxa', [])) or '-', '| stage:', e.get('stage') or '-')
    if e.get('terminology'): print('   terminology:', e['terminology'])
    for f in fs:
        qv = f.get('quote_verified')
        print(f"   - ({f['id']}) [{f['dim']}; {f['strength']}; quote_verified={qv}] {f['statement']}\n       \"{f.get('support','')}\" ({f.get('locator')})")
    for m in ms:
        print(f"   * mentions {m.get('work')}: {m.get('claim')} | \"{m.get('quote','')}\" [secondary_report; quote_verified={m.get('quote_verified')}]")
    if e.get('caveats'): print('   caveats:', e['caveats'])
    ap_ = e.get('appraisal') or {}
    print('   appraisal:', ap_.get('specimens'), '/', ap_.get('methods'), '/', ap_.get('claims_support'), '-', ap_.get('note', ''))
    n += 1
print(f'# {n} records printed')
