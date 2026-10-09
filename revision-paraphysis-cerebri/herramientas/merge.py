#!/usr/bin/env python3
"""Deterministic merge/dedupe of raw search files -> corpus.json, corpus.csv, search_log.json, prisma_counts.json"""
import json, glob, os, re, csv, sys, collections
WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
RAW = os.path.join(WS, 'raw')
REL_ORDER = {'core': 3, 'relevant': 2, 'peripheral': 1, 'irrelevant': 0}
def norm(t): return re.sub(r'[^a-z0-9]+', ' ', (t or '').lower()).strip()
def pm(r): return re.sub(r'\D', '', str(r.get('pmid') or ''))
def dd(r):
    d = (r.get('doi') or '').strip().lower()
    d = re.sub(r'^https?://(dx\.)?doi\.org/', '', d)
    return d
def keyset(r):
    ks = []
    if pm(r): ks.append('pmid:' + pm(r))
    if dd(r): ks.append('doi:' + dd(r))
    t = norm(r.get('title'))
    if t: ks.append('t:' + t + '|' + str(r.get('year') or ''))
    return ks
files = sorted(glob.glob(os.path.join(RAW, '*.json')))
raws, queries, failures, per_file = [], [], [], {}
for f in files:
    try: d = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        print('UNREADABLE', f, e, file=sys.stderr); continue
    lab = d.get('label') or os.path.basename(f)
    per_file[lab] = len(d.get('records', []))
    for q in d.get('queries', []): queries.append({'label': lab, 'channel': d.get('channel'), **q})
    for x in d.get('failures', []): failures.append({'label': lab, 'failure': x})
    for r in d.get('records', []):
        r = dict(r); r['_file'] = lab; raws.append(r)
# union-find over key sets
parent = {}
def find(x):
    while parent.setdefault(x, x) != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b): parent[find(a)] = find(b)
for i, r in enumerate(raws):
    ks = keyset(r)
    node = f'rec{i}'; find(node)
    for k in ks: union(node, k)
groups = collections.defaultdict(list)
for i, r in enumerate(raws): groups[find(f'rec{i}')].append(r)
def best(vals):
    vals = [v for v in vals if v not in (None, '', 0)]
    return max(vals, key=lambda v: len(str(v))) if vals else ''
merged = []
for g in groups.values():
    g_sorted = sorted(g, key=lambda r: (not r.get('bibliographic_verified'), -len(r.get('excerpt') or '')))
    m = {}
    for fld in ['title', 'authors', 'journal', 'volume', 'pages', 'doi', 'pmid', 'pmcid', 'language', 'excerpt', 'verified_via']:
        m[fld] = best([r.get(fld) for r in g_sorted]) if fld != 'excerpt' else (g_sorted[0].get('excerpt') or best([r.get('excerpt') for r in g]))
    yrs = [r.get('year') for r in g if r.get('year')]
    m['year'] = max(set(yrs), key=yrs.count) if yrs else 0
    m['doi'] = dd(m)
    m['pmid'] = pm(m)
    m['bibliographic_verified'] = any(r.get('bibliographic_verified') for r in g)
    m['relevance_votes'] = [r.get('relevance') for r in g]
    m['relevance_max'] = max((r.get('relevance') for r in g), key=lambda x: REL_ORDER.get(x, 0))
    m['dims'] = sorted({d for r in g for d in (r.get('dims') or [])})
    m['source_dbs'] = sorted({r.get('source_db') for r in g if r.get('source_db')})
    m['access_best'] = sorted({r.get('access') for r in g}, key=lambda a: ['pmc_fulltext', 'wiley_passage', 'pubmed_abstract', 'web_snippet', 'metadata_only'].index(a) if a in ['pmc_fulltext', 'wiley_passage', 'pubmed_abstract', 'web_snippet', 'metadata_only'] else 9)[0]
    m['notes'] = [r.get('note') for r in g if r.get('note')][:6]
    m['as_cited_in'] = sorted({r.get('as_cited_in') for r in g if r.get('as_cited_in')})
    m['queries'] = sorted({r.get('query') for r in g if r.get('query')})[:12]
    m['found_by'] = sorted({r['_file'] for r in g})
    merged.append(m)
merged.sort(key=lambda m: (m['year'] or 9999, norm(m['authors'])[:30], norm(m['title'])[:30]))
for i, m in enumerate(merged, 1): m['rid'] = f'R{i:03d}'
json.dump(merged, open(os.path.join(WS, 'corpus.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({'queries': queries, 'failures': failures, 'per_file': per_file}, open(os.path.join(WS, 'search_log.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(os.path.join(WS, 'corpus.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['rid', 'year', 'authors', 'title', 'journal', 'pmid', 'doi', 'access', 'verified', 'relevance_max', 'dims', 'found_by'])
    for m in merged: w.writerow([m['rid'], m['year'], m['authors'], m['title'], m['journal'], m['pmid'], m['doi'], m['access_best'], m['bibliographic_verified'], m['relevance_max'], ';'.join(m['dims']), ';'.join(m['found_by'])])
c = collections.Counter(m['relevance_max'] for m in merged)
by_db = collections.Counter(r.get('source_db') for r in raws)
counts = {'files': len(files), 'raw_records': len(raws), 'unique_records': len(merged), 'duplicates_removed': len(raws) - len(merged), 'relevance_max': dict(c), 'raw_by_source_db': dict(by_db), 'n_queries_logged': len(queries), 'verified': sum(m['bibliographic_verified'] for m in merged), 'access': dict(collections.Counter(m['access_best'] for m in merged))}
json.dump(counts, open(os.path.join(WS, 'prisma_counts.json'), 'w'), indent=1)
print(json.dumps(counts, indent=1))
