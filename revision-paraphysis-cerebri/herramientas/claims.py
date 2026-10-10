#!/usr/bin/env python3
"""claims.py <section.md> <out.json> : splits a section into verifiable claims.
Markers: [@R217.3] finding, [@R185.m1] secondary mention, [@R070.t] title-level identification. Several: [@R1.2; @R3.m1].
Output: list of {cid, kind: cited|uncited, text, refs, invalid_refs}. Prints a summary; non-zero exit if invalid markers exist."""
import json, os, re, sys
WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
db = json.load(open(os.path.join(WS, 'extract', 'db.json'), encoding='utf-8'))
valid = set()
for rid, r in db.items():
    valid.add(rid + '.t')
    e = r['extraction'] or {}
    for f in e.get('findings', []): valid.add(f['id'])
    for m in e.get('mentions', []): valid.add(m['id'])
src, out = sys.argv[1], sys.argv[2]
sec = os.path.basename(src).split('.')[0]
text = open(src, encoding='utf-8').read()
MK = re.compile(r'\[@[^\]]+\]')
def refs_of(s):
    r = []
    for m in MK.findall(s):
        r += [x.strip().lstrip('@').strip() for x in m[1:-1].split(';') if x.strip()]
    return [x.lstrip('@') for x in r]
claims = []; n = 0
for line in text.splitlines():
    st = line.strip()
    if not st or st.startswith('#') or st.startswith('<!--') or set(st) <= set('|-: '): continue
    if st.startswith('|'):           # table row: one claim per row
        parts = [st]
    else:
        parts = re.split(r'(?<=[\.\?\!\]])\s+(?=[A-ZÁÉÍÓÚÑ¿¡"\(\[])', st)
        # re-attach a marker-only fragment to the previous sentence
        merged = []
        for p in parts:
            if merged and MK.fullmatch(p.strip()): merged[-1] += ' ' + p
            else: merged.append(p)
        parts = merged
    for p in parts:
        p = p.strip()
        if len(p) < 25: continue
        refs = refs_of(p)
        n += 1
        kind = 'cited' if refs else 'uncited'
        if kind == 'uncited' and (p.startswith('Interpretación') or p.startswith('*Interpretación') or p.startswith('Esta revisión') or p.startswith('En esta revisión')): kind = 'interpretation'
        claims.append({'cid': f'{sec}-{n:03d}', 'kind': kind, 'text': p, 'refs': refs, 'invalid_refs': [x for x in refs if x not in valid]})
json.dump(claims, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
inv = [c for c in claims if c['invalid_refs']]
import collections
print(dict(collections.Counter(c['kind'] for c in claims)), 'invalid-marker claims:', len(inv))
for c in inv: print('  INVALID', c['cid'], c['invalid_refs'])
sys.exit(1 if inv else 0)
