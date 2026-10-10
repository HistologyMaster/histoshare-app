#!/usr/bin/env python3
"""assemble.py : builds the final Markdown review from verified sections, front matter, tables and a Vancouver reference list.
Usage: assemble.py <out_dir>
Inputs  (in WS/synth): S1..S7.md, front/*.md (title, resumen, abstract, intro, results_intro, discusion, limitaciones, conclusiones, declaraciones), methods.md
Markers: [@R217.3; @R246.1] -> [n,m] by order of first appearance of the RID; [@M1].. -> methodological references."""
import json, os, re, sys, glob, csv, collections

WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SY = os.path.join(WS, 'synth')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WS, 'final')
os.makedirs(OUT, exist_ok=True)
db = json.load(open(os.path.join(WS, 'extract', 'db.json'), encoding='utf-8'))
corpus = {m['rid']: m for m in json.load(open(os.path.join(WS, 'corpus.json'), encoding='utf-8'))}

METH = {
 'M1': 'Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71. doi:10.1136/bmj.n71. PMID: 33782057.',
 'M2': 'Baethge C, Goldbeck-Wood S, Mertens S. SANRA—a scale for the quality assessment of narrative review articles. Res Integr Peer Rev. 2019;4:5. doi:10.1186/s41073-019-0064-8. PMID: 30962953.',
 'M3': 'Tomaszewski KA, Henry BM, Kumar Ramakrishnan P, Roy J, Vikse J, Loukas M, et al. Development of the Anatomical Quality Assurance (AQUA) checklist: guidelines for reporting original anatomical studies. Clin Anat. 2017;30(1):14-20. doi:10.1002/ca.22800. PMID: 27801507.',
 'M4': 'Kassis T, Agarwal V, He Y, Patel D, Brueckner AM. Scientific Agent Skills: a library of procedural knowledge for research agents. arXiv:2609.00065. 2026. doi:10.48550/arXiv.2609.00065. [Metadatos confirmados mediante búsqueda web; no verificados en la fuente.]',
}

# duplicate map
dup = {rid: r['extraction'].get('duplicate_of') for rid, r in db.items() if r['extraction'] and r['extraction'].get('duplicate_of')}
def canon(rid):
    seen = set()
    while rid in dup and dup[rid] and rid not in seen:
        seen.add(rid); rid = dup[rid]
    return rid

MK = re.compile(r'\[@[^\]]+\]')
order = []                      # canonical keys in order of first appearance
def key_of(tok):
    tok = tok.strip().lstrip('@').strip()
    if re.fullmatch(r'M\d+', tok): return tok
    return canon(tok.split('.')[0])
def collapse(nums):
    nums = sorted(set(nums)); out = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        out.append(f'{nums[i]}-{nums[j]}' if j - i >= 2 else (f'{nums[i]},{nums[j]}' if j - i == 1 else str(nums[i])))
        i = j + 1
    return ','.join(out)
def cite(m):
    toks = [t for t in m.group(0)[1:-1].split(';') if t.strip()]
    keys = []
    for t in toks:
        k = key_of(t)
        if k not in order: order.append(k)
        keys.append(order.index(k) + 1)
    return '[' + collapse(keys) + ']'
def convert(text): return MK.sub(cite, text)

def vanc(rid):
    b = db[rid]['bib']
    au = (b['authors'] or '').strip()
    parts = [x.strip() for x in au.split(',')] if au else []
    if len(parts) > 6: au = ', '.join(parts[:6]) + ', et al'
    title = (b['title'] or '').strip().rstrip('.')
    j = (b['journal'] or '').strip()
    yr = b['year'] or 's. f.'
    vol = (b['volume'] or '').strip(); pg = (b['pages'] or '').strip()
    head = f'{au}. ' if au else ''
    body = f'{title}. ' if title else '[Título no verificado]. '
    cit = ''
    if j: cit += f'{j}. '
    cit += f'{yr}'
    if vol: cit += f';{vol}'
    if pg: cit += f':{pg}'
    cit += '.'
    s = head + body + cit
    if b['doi']: s += f" doi:{b['doi']}."
    if b['pmid']: s += f" PMID: {b['pmid']}."
    if not b['bibliographic_verified']: s += ' [Datos bibliográficos no verificados en PubMed; obra identificada por fuente secundaria.]'
    return s

def read(path):
    return open(path, encoding='utf-8').read() if os.path.exists(path) else ''

# ---- numbers for placeholders
log = json.load(open(os.path.join(WS, 'search_log.json'), encoding='utf-8'))
q = collections.Counter((x.get('db') or '').lower() for x in log['queries'])
pc = json.load(open(os.path.join(WS, 'prisma_counts.json'))); pf = json.load(open(os.path.join(WS, 'prisma_final.json')))
claims_n = 0; ver_rows = []
SEC = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7']
for s in SEC + ['F']:
    cf = os.path.join(SY, 'claims', f'{s}.json')
    if not os.path.exists(cf): continue
    cl = json.load(open(cf, encoding='utf-8')); claims_n += len(cl)
vals = {
 'N_QUERIES': log['queries'] and len(log['queries']), 'N_Q_PUBMED': q['pubmed'] + q['pubmed_related'], 'N_Q_PMC': q['pmc'], 'N_Q_WILEY': q['wiley'], 'N_Q_WEB': q['web'] + q['websearch'],
 'N_RAW': pc['raw_records'], 'N_UNIQUE': pc['unique_records'], 'N_SCREENED': pf['screened'], 'PCT_AGREE': str(pf['percent_agreement_initial']).replace('.', ','),
 'KAPPA4': str(pf['cohen_kappa_4cat']).replace('.', ','), 'KAPPA2': str(pf['cohen_kappa_include_vs_exclude']).replace('.', ','), 'N_ADJ': pf['adjudicated'],
 'N_CLAIMS': claims_n,
}
extra = os.path.join(SY, 'placeholders.json')
if os.path.exists(extra): vals.update(json.load(open(extra, encoding='utf-8')))
def fill(t):
    for k, v in vals.items(): t = t.replace('{{' + k + '}}', str(v))
    return t

# ---- tables
def tbl(header, rows):
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(['---'] * len(header)) + '|']
    out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)
depth_label = {'full_text': 'Texto completo', 'abstract': 'Resumen completo', 'excerpt_only': 'Extracto parcial', 'secondary_snippet': 'Instantánea web (no verificada)', 'metadata_only': 'Solo título/metadatos'}
cnt = collections.Counter((r['tier'], r['extraction']['data_depth']) for r in db.values())
rows = []
for d in ['full_text', 'abstract', 'excerpt_only', 'secondary_snippet', 'metadata_only']:
    a, b = cnt[('A', d)], cnt[('B', d)]
    rows.append([depth_label[d], a, b, a + b])
rows.append(['**Total**', sum(cnt[('A', d)] for d in depth_label), sum(cnt[('B', d)] for d in depth_label), len(db)])
T_DEPTH = tbl(['Profundidad de lectura', 'Nivel A (específicos)', 'Nivel B (contexto)', 'Total'], rows)

about = collections.Counter((r['tier'], r['extraction']['about_paraphysis']) for r in db.values())
lab = {'principal': 'Principal', 'substantive': 'Sustancial', 'passing_mention': 'Mención circunstancial', 'none': 'Ninguna', 'title_only': 'No evaluable (solo título)'}
rows = [[lab[k], about[('A', k)], about[('B', k)], about[('A', k)] + about[('B', k)]] for k in ['principal', 'substantive', 'passing_mention', 'none', 'title_only']]
T_ABOUT = tbl(['Tratamiento de la paráfisis tras la lectura', 'Nivel A', 'Nivel B', 'Total'], rows)

dec = collections.Counter()
for r in db.values():
    y = r['bib']['year']
    dec['s. f.' if not y else (f'{y // 10 * 10}s' if y >= 1900 else 'Siglo XIX')] += 1
orderd = ['Siglo XIX', '1900s', '1910s', '1920s', '1930s', '1940s', '1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s', 's. f.']
T_DEC = tbl(['Período', 'Registros incluidos'], [[d, dec[d]] for d in orderd if dec[d]])

grp = collections.Counter()
for r in db.values():
    e = r['extraction']
    if e.get('include_in_synthesis') in ('yes', 'context_only') and e['data_depth'] != 'metadata_only':
        gs = {t['group'] for t in e.get('taxa', []) if t.get('group') not in (None, 'not_applicable')}
        for g in gs: grp[g] += 1
glab = {'cyclostome': 'Ciclóstomos', 'chondrichthyan': 'Condrictios', 'actinopterygian': 'Actinopterigios', 'dipnoan': 'Dipnoos', 'coelacanth': 'Celacanto', 'urodele': 'Urodelos', 'anuran': 'Anuros', 'caecilian': 'Ápodos', 'squamate': 'Escamosos', 'tuatara': 'Tuátara', 'chelonian': 'Quelonios', 'crocodilian': 'Cocodrilianos', 'bird': 'Aves', 'monotreme': 'Monotremas', 'marsupial': 'Marsupiales', 'eutherian': 'Euterios', 'human': 'Humanos', 'multiple': 'Varios grupos'}
T_TAXA = tbl(['Grupo taxonómico', 'Registros con lectura de contenido que lo mencionan'], [[glab.get(g, g), n] for g, n in sorted(grp.items(), key=lambda x: -x[1])])

flow = [
 ['Registros identificados (brutos, todos los canales)', pc['raw_records']],
 ['Duplicados eliminados (PMID, DOI, título normalizado)', pc['duplicates_removed']],
 ['Registros únicos', pc['unique_records']],
 ['Excluidos en la identificación (homónimos no neurales)', pf['excluded_at_identification']],
 ['Registros cribados (título/resumen/extracto; dos revisores independientes)', pf['screened']],
 ['Excluidos tras el cribado', pf['final_counts']['X']],
 ['Incluidos: Nivel A (específicos de la paráfisis)', pf['final_counts']['A']],
 ['Incluidos: Nivel B (contexto necesario)', pf['final_counts']['B']],
 ['Registros con contenido extraíble (resumen, texto o extracto)', sum(1 for r in db.values() if r['extraction']['data_depth'] != 'metadata_only')],
 ['Obras identificadas solo por título o metadatos (sin contenido verificable)', sum(1 for r in db.values() if r['extraction']['data_depth'] == 'metadata_only')],
]
T_FLOW = tbl(['Etapa', 'n'], flow)
T_SEARCH = tbl(['Canal', 'Consultas registradas', 'Registros brutos aportados'], [
 ['PubMed (incl. expansión por artículos relacionados)', vals['N_Q_PUBMED'], pc['raw_by_source_db'].get('pubmed', 0)],
 ['PubMed Central (texto completo)', vals['N_Q_PMC'], pc['raw_by_source_db'].get('pmc', 0)],
 ['Wiley Scholar Gateway (30 consultas efectivas; cuota gratuita agotada)', vals['N_Q_WILEY'], pc['raw_by_source_db'].get('wiley', 0)],
 ['Búsqueda web (descubrimiento; resultados no verificados)', vals['N_Q_WEB'], pc['raw_by_source_db'].get('web', 0)],
 ['**Total**', vals['N_QUERIES'], pc['raw_records']],
])
# verification table (rounds: 1 = first draft; 3 = full pass over the near-final text; 4 = re-check of corrected claims)
def vstats(sec, rnd):
    k = bad = 0
    pats = glob.glob(os.path.join(SY, 'verify', f'{sec}-r{rnd}-*.json')) if rnd < 4 else glob.glob(os.path.join(SY, 'verify', f'r{rnd}-*.json'))
    for f in pats:
        for x in json.load(open(f, encoding='utf-8')):
            if rnd >= 4 and not x['cid'].startswith(sec + '-'): continue
            k += 1
            if x['verdict'] not in ('supported', 'ok_uncited'): bad += 1
    return k, bad
vrows = []; tot = collections.Counter()
for s in SEC + ['F']:
    cf = os.path.join(SY, 'claims', f'{s}.json')
    if not os.path.exists(cf): continue
    n = len(json.load(open(cf, encoding='utf-8')))
    r1 = vstats(s, 1) if s != 'F' else (0, 0); r3 = vstats(s, 3); r4 = vstats(s, 4); r5 = vstats(s, 5)
    vrows.append([s if s != 'F' else 'F (intro., discusión, conclusiones, resúmenes)', n, f'{r1[0]} / {r1[1]}' if r1[0] else '—', f'{r3[0]} / {r3[1]}', f'{r4[0]} / {r4[1]}' if r4[0] else '—', f'{r5[0]} / {r5[1]}' if r5[0] else '—'])
    tot['n'] += n; tot['r1k'] += r1[0]; tot['r1b'] += r1[1]; tot['r3k'] += r3[0]; tot['r3b'] += r3[1]; tot['r4k'] += r4[0]; tot['r4b'] += r4[1]; tot['r5k'] += r5[0]; tot['r5b'] += r5[1]
vrows.append(['**Total**', tot['n'], f"{tot['r1k']} / {tot['r1b']}", f"{tot['r3k']} / {tot['r3b']}", f"{tot['r4k']} / {tot['r4b']}", f"{tot['r5k']} / {tot['r5b']}"])
T_VERIF = tbl(['Sección', 'Afirmaciones en el texto final', 'Ronda 1 (borrador): verificadas / señaladas', 'Ronda 3 (pasada completa): verificadas / señaladas', 'Ronda 4 (reescritas): verificadas / señaladas', 'Ronda 5 (reescritas): verificadas / señaladas'], vrows)
vals.update({'V_R3_N': tot['r3k'], 'V_R3_BAD': tot['r3b'], 'V_R4_N': tot['r4k'], 'V_R4_BAD': tot['r4b'], 'V_R5_N': tot['r5k'], 'V_R5_BAD': tot['r5b']})
TABS = {'T_DEPTH': T_DEPTH, 'T_ABOUT': T_ABOUT, 'T_DEC': T_DEC, 'T_TAXA': T_TAXA, 'T_FLOW': T_FLOW, 'T_SEARCH': T_SEARCH, 'T_VERIF': T_VERIF}
def fill_tabs(t):
    for k, v in TABS.items(): t = t.replace('{{' + k + '}}', v)
    return fill(t)

# ---- assemble body
def demote(text, base_num=None):
    out = []
    for ln in text.splitlines():
        if ln.startswith('### '): ln = '#' + ln
        elif ln.startswith('## ') and base_num: ln = f'### {base_num} ' + ln[3:]
        out.append(ln)
    return '\n'.join(out)

fr = os.path.join(SY, 'front')
parts = []
parts.append(read(os.path.join(fr, 'title.md')).strip())
for name in ['resumen', 'abstract']:
    parts.append(read(os.path.join(fr, f'{name}.md')).strip())
parts.append('## 1. Introducción\n\n' + re.sub(r'^## .*\n+', '', read(os.path.join(fr, 'intro.md')).strip()))
parts.append(re.sub(r'^## Métodos', '## 2. Métodos', read(os.path.join(SY, 'methods.md')).strip()))
res = ['## 3. Resultados', re.sub(r'^## .*\n+', '', read(os.path.join(fr, 'results_intro.md')).strip())]
titles = {}
TAB_OFFSET = 6   # Tablas 1-6 pertenecen a 3.1-3.2
for i, s in enumerate(SEC):
    p = os.path.join(SY, f'{s}.md')
    if not os.path.exists(p): continue
    txt = read(p).strip()
    loc = [int(x) for x in re.findall(r'Tabla (\d+)', txt)]
    mx = max(loc) if loc else 0
    txt = re.sub(r'Tabla (\d+)', lambda m: f'Tabla {int(m.group(1)) + TAB_OFFSET}', txt)
    TAB_OFFSET += mx
    res.append(demote(txt, f'3.{i + 3}'))
parts.append('\n\n'.join(res))
parts.append('## 4. Discusión\n\n' + re.sub(r'^## .*\n+', '', read(os.path.join(fr, 'discusion.md')).strip()))
parts.append('## 5. Limitaciones de esta revisión\n\n' + re.sub(r'^## .*\n+', '', read(os.path.join(fr, 'limitaciones.md')).strip()))
parts.append('## 6. Conclusiones\n\n' + re.sub(r'^## .*\n+', '', read(os.path.join(fr, 'conclusiones.md')).strip()))
parts.append(read(os.path.join(fr, 'declaraciones.md')).strip())
body = '\n\n'.join(p for p in parts if p)
body = fill_tabs(body)
body = convert(body)

# references
refs = []
for i, k in enumerate(order, 1):
    refs.append(f'{i}. ' + (METH[k] if k in METH else vanc(k)))
refs_md = '## Referencias\n\n' + '\n'.join(refs)

# annexes
def short(t, n=95): t = (t or '').strip(); return t if len(t) <= n else t[:n - 1] + '…'
rowsA = []
for rid, r in sorted(db.items(), key=lambda x: (x[1]['bib']['year'] or 9999, x[0])):
    if r['extraction']['data_depth'] == 'metadata_only':
        b = r['bib']; rowsA.append([rid, (b['authors'] or '—')[:40], b['year'] or 's. f.', short(b['title']), ('sí' if b['bibliographic_verified'] else 'no')])
AX_A = '## Anexo A. Obras identificadas solo por título o metadatos\n\nObras incluidas en el cribado cuyo contenido no pudo leerse (sin resumen en PubMed o sin acceso al texto). Se citan únicamente para registrar su existencia; **no se les atribuye ningún hallazgo**. La columna "Verificada" indica si los datos bibliográficos se confirmaron en PubMed.\n\n' + tbl(['ID', 'Autores', 'Año', 'Título', 'Verificada'], rowsA)
rowsB = []
for rid, r in sorted(db.items(), key=lambda x: (x[1]['bib']['year'] or 9999, x[0])):
    e = r['extraction']
    if e['data_depth'] == 'metadata_only': continue
    b = r['bib']; ck = canon(rid)
    n = order.index(ck) + 1 if ck in order else '—'
    rowsB.append([rid, n, (b['authors'] or '—').split(',')[0][:24], b['year'] or 's. f.', r['tier'], depth_label[e['data_depth']], lab.get(e['about_paraphysis'], e['about_paraphysis']), {'yes': 'núcleo', 'context_only': 'contexto', 'no': 'no usado'}.get(e['include_in_synthesis'], e['include_in_synthesis'])])
AX_B = '## Anexo B. Registros con contenido extraído\n\nProfundidad real de lectura y uso en la síntesis. "N.º ref." remite a la lista de referencias (— = no citado en el texto).\n\n' + tbl(['ID', 'N.º ref.', 'Primer autor', 'Año', 'Nivel', 'Profundidad', 'Paráfisis en la fuente', 'Uso'], rowsB)
AX_C = '## Anexo C. Verificación independiente de afirmaciones\n\nCada oración con contenido empírico fue contrastada por un verificador independiente (agente de IA distinto del redactor) con el hallazgo extraído, la cita literal y el texto fuente guardado. "Señaladas" son las afirmaciones con veredicto distinto de *supported* u *ok_uncited* (excesivas, parcialmente respaldadas, mal atribuidas, sin matiz o sin cita). El proceso tuvo cinco rondas: (1) verificación del borrador y reescritura de lo señalado; (2) reverificación de las secciones reescritas (parcialmente reejecutada por interrupciones de sesión, por lo que no se tabula); (3) pasada completa y limpia sobre el texto casi definitivo de todas las secciones y de las partes integradoras, con verificadores nuevos; y (4–5) reverificación de las afirmaciones reescritas tras la ronda 3 (la ronda 4 señaló {{V_R4_BAD}} de {{V_R4_N}} y la ronda 5, {{V_R5_BAD}} de {{V_R5_N}}). La ronda 3 señaló {{V_R3_BAD}} de {{V_R3_N}} afirmaciones, casi todas por exclusividad o cuantificación sin respaldo ("el único", "la mayor parte") o por generalizar de una especie al conjunto; todas se reescribieron. Tras la ronda 5, una afirmación (la del párrafo de ontogenia de la Discusión sobre Pax7, ahora «en al menos tres trabajos») se ajustó con la redacción sugerida por el propio verificador y no se sometió a una ronda adicional.\n\n' + T_VERIF + '\n'
final = body + '\n\n' + refs_md + '\n\n' + AX_A + '\n\n' + AX_B + '\n\n' + fill(AX_C) + '\n'
open(os.path.join(OUT, 'revision_paraphysis_cerebri.md'), 'w', encoding='utf-8').write(final)
with open(os.path.join(OUT, 'referencias_mapa.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['n', 'rid', 'pmid', 'doi', 'verificada'])
    for i, k in enumerate(order, 1):
        if k in METH: w.writerow([i, k, '', '', 'sí']); continue
        b = db[k]['bib']; w.writerow([i, k, b['pmid'], b['doi'], b['bibliographic_verified']])
print('refs cited:', len(order), '| words ~', len(final.split()))
print('unverified refs cited:', sum(1 for k in order if k not in METH and not db[k]['bib']['bibliographic_verified']))
