#!/usr/bin/env python3
"""Helper for search agents. Usage:
  known.py list                      -> compact digest of every record already collected
  known.py check [--pmid X] [--doi Y] [--title "..."]  -> prints KNOWN <file> or NEW
  known.py validate <file>           -> validates a raw file written by an agent
"""
import json, glob, os, re, sys, argparse
RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw')
def norm(t): return re.sub(r'[^a-z0-9]+', ' ', (t or '').lower()).strip()
def load():
    out = []
    for f in sorted(glob.glob(os.path.join(RAW, '*.json'))):
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print('!! unreadable', f, e, file=sys.stderr); continue
        for r in d.get('records', []):
            out.append((os.path.basename(f), r))
    return out
def validate(path):
    d = json.load(open(path, encoding='utf-8'))
    assert isinstance(d, dict) and 'records' in d and 'queries' in d and 'label' in d, 'need keys label, queries, records'
    req = ['title', 'year', 'source_db', 'query', 'access', 'bibliographic_verified', 'relevance']
    for i, r in enumerate(d['records']):
        miss = [k for k in req if k not in r]
        assert not miss, f'record {i} missing {miss}'
    print('OK', len(d['records']), 'records')
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('arg', nargs='?')
    ap.add_argument('--pmid'); ap.add_argument('--doi'); ap.add_argument('--title')
    a = ap.parse_args()
    if a.cmd == 'validate': return validate(a.arg)
    recs = load()
    if a.cmd == 'list':
        seen = set()
        for f, r in recs:
            k = r.get('pmid') or r.get('doi') or norm(r.get('title'))
            if k in seen: continue
            seen.add(k)
            au = (r.get('authors') or '').split(',')[0][:20]
            print(f"{r.get('year')}|{au}|{(r.get('title') or '')[:90]}|{r.get('relevance')}|pmid={r.get('pmid') or '-'}|doi={r.get('doi') or '-'}")
        print('unique:', len(seen))
    elif a.cmd == 'check':
        for f, r in recs:
            if (a.pmid and r.get('pmid') == a.pmid) or (a.doi and (r.get('doi') or '').lower() == a.doi.lower()) or (a.title and norm(a.title) == norm(r.get('title'))):
                print('KNOWN', f); return
        print('NEW')
main()
