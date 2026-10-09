#!/usr/bin/env python3
"""Consolidates dual screening -> screen/final.json, included_A.json, included_B.json, screening_log.csv, prisma_final.json"""
import json, glob, os, csv, collections
WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
S = os.path.join(WS, 'screen')
C = {m['rid']: m for m in json.load(open(os.path.join(WS, 'corpus.json'), encoding='utf-8'))}
excl_id = json.load(open(os.path.join(S, 'prescreen_excluded.json')))['excluded_identification']
rids_all = json.load(open(os.path.join(S, 'rids_to_screen.json')))
dec = collections.defaultdict(dict)
for f in sorted(glob.glob(os.path.join(S, 'b*-[AB].json'))):
    d = json.load(open(f, encoding='utf-8'))
    for x in d['decisions']: dec[x['rid']][d['reviewer']] = x
adj = {}
for f in sorted(glob.glob(os.path.join(S, 'adj*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    for x in d['decisions']: adj[x['rid']] = x
norm = {'include_A': 'A', 'include_B': 'B', 'exclude': 'X', 'uncertain': 'U'}
final, rows = {}, []
agree = 0; pairs = []
missing = []
for r in rids_all:
    a = dec[r].get('A'); b = dec[r].get('B')
    if not a or not b: missing.append(r)
    da = norm.get(a['decision']) if a else None; db = norm.get(b['decision']) if b else None
    if da and db: pairs.append((da, db))
    if da and db and da == db and da != 'U':
        f = a; src = 'agreement'; agree += 1
    elif r in adj:
        f = adj[r]; src = 'adjudicated'
    else:
        f = None; src = 'UNRESOLVED'
    if f is None:
        final[r] = {'rid': r, 'final': 'UNRESOLVED', 'source': src}; continue
    fin = norm[f['decision']]
    final[r] = {'rid': r, 'final': fin, 'source': src, 'reason_code': f.get('reason_code'), 'reason': f.get('reason'), 'dims': f.get('dims') or [], 'data_depth': f.get('data_depth'), 'A': da, 'B': db}
# kappa (3 categories A/B/X, U kept as its own)
cats = ['A', 'B', 'X', 'U']
n = len(pairs)
po = sum(1 for p in pairs if p[0] == p[1]) / n if n else 0
pa = {c: sum(1 for p in pairs if p[0] == c) / n for c in cats}; pb = {c: sum(1 for p in pairs if p[1] == c) / n for c in cats}
pe = sum(pa[c] * pb[c] for c in cats)
kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
# include-vs-exclude binary kappa
def binar(c): return 'I' if c in ('A', 'B') else ('X' if c == 'X' else 'U')
bp = [(binar(a), binar(b)) for a, b in pairs]
cb = ['I', 'X', 'U']
pob = sum(1 for p in bp if p[0] == p[1]) / n if n else 0
pab = {c: sum(1 for p in bp if p[0] == c) / n for c in cb}; pbb = {c: sum(1 for p in bp if p[1] == c) / n for c in cb}
peb = sum(pab[c] * pbb[c] for c in cb)
kappa_bin = (pob - peb) / (1 - peb) if peb < 1 else 1.0
json.dump(final, open(os.path.join(S, 'final.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for tier in ('A', 'B'):
    lst = [{'rid': r, **{k: v for k, v in final[r].items() if k != 'rid'}, 'year': C[r]['year'], 'authors': C[r]['authors'], 'title': C[r]['title']} for r in rids_all if final[r]['final'] == tier]
    json.dump(lst, open(os.path.join(S, f'included_{tier}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(os.path.join(S, 'screening_log.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['rid', 'year', 'authors', 'title', 'reviewer_A', 'reviewer_B', 'final', 'source', 'reason_code', 'reason', 'dims', 'data_depth'])
    for r in excl_id: w.writerow([r, C[r]['year'], C[r]['authors'], C[r]['title'], '-', '-', 'X', 'excluded_at_identification', 'homonym', 'non-neural homonym / off-topic', '', ''])
    for r in rids_all:
        f = final[r]; w.writerow([r, C[r]['year'], C[r]['authors'], C[r]['title'], f.get('A'), f.get('B'), f['final'], f['source'], f.get('reason_code'), f.get('reason'), ';'.join(f.get('dims') or []), f.get('data_depth')])
cnt = collections.Counter(f['final'] for f in final.values())
acc = collections.Counter(C[r]['access_best'] for r in rids_all if final[r]['final'] in ('A', 'B'))
out = {'identified_unique': len(C), 'excluded_at_identification': len(excl_id), 'screened': len(rids_all), 'agreement_initial': agree, 'adjudicated': sum(1 for f in final.values() if f['source'] == 'adjudicated'), 'unresolved': cnt.get('UNRESOLVED', 0), 'missing_decisions': missing, 'final_counts': dict(cnt), 'cohen_kappa_4cat': round(kappa, 3), 'cohen_kappa_include_vs_exclude': round(kappa_bin, 3), 'percent_agreement_initial': round(100 * po, 1), 'included_access_depth': dict(acc)}
json.dump(out, open(os.path.join(WS, 'prisma_final.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
