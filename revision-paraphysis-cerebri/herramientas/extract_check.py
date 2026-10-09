#!/usr/bin/env python3
"""extract_check.py <extract/eNN.json> [--strict] : validates schema and verifies every verbatim 'support' quote against src/<rid>.txt or corpus excerpt."""
import json, sys, os, re
WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
C = {m['rid']: m for m in json.load(open(os.path.join(WS, 'corpus.json'), encoding='utf-8'))}
def norm(t):
    t = (t or '').lower()
    t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-').replace('‐', '-').replace('‑', '-')
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()
path = sys.argv[1]
d = json.load(open(path, encoding='utf-8'))
assert 'batch' in d and 'records' in d
bad = 0; total = 0
req = ['rid', 'data_depth', 'about_paraphysis', 'study_type', 'findings', 'include_in_synthesis']
for r in d['records']:
    miss = [k for k in req if k not in r]
    assert not miss, (r.get('rid'), 'missing', miss)
    rid = r['rid']; assert rid in C, rid
    srcf = os.path.join(WS, 'extract', 'src', rid + '.txt')
    src = norm(open(srcf, encoding='utf-8').read()) if os.path.exists(srcf) else ''
    src += ' ' + norm(C[rid].get('excerpt'))
    for f in list(r['findings']) + [dict(m, support=m.get('quote')) for m in r.get('mentions', [])]:
        q = f.get('support')
        if not q: continue
        total += 1
        nq = norm(q)
        ok = nq in src
        if not ok:
            # tolerate ellipsis-joined quotes: each fragment must be present
            frs = [norm(x) for x in re.split(r'\.\.\.|…|\[\.\.\.\]', q) if len(norm(x)) > 12]
            ok = bool(frs) and all(x in src for x in frs)
        f['quote_verified'] = ok
        if not ok:
            bad += 1; print('QUOTE NOT FOUND in source text:', rid, '|', q[:110])
json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'OK schema; quotes checked={total}, not found={bad}')
