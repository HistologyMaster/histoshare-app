#!/usr/bin/env python3
import json, os, sys, collections
WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
out = sys.argv[1]
pc = json.load(open(os.path.join(WS, 'prisma_counts.json'))); pf = json.load(open(os.path.join(WS, 'prisma_final.json')))
db = json.load(open(os.path.join(WS, 'extract', 'db.json')))
A_ext = sum(1 for r in db.values() if r['tier'] == 'A' and r['extraction']['data_depth'] != 'metadata_only')
A_tit = sum(1 for r in db.values() if r['tier'] == 'A' and r['extraction']['data_depth'] == 'metadata_only')
B_ext = sum(1 for r in db.values() if r['tier'] == 'B' and r['extraction']['data_depth'] != 'metadata_only')
B_tit = sum(1 for r in db.values() if r['tier'] == 'B' and r['extraction']['data_depth'] == 'metadata_only')
W, H = 1000, 980
c = {'ink': '#1f2933', 'box': '#eef3f8', 'edge': '#3b5b7a', 'side': '#fbf3e6', 'sedge': '#a9742c', 'inc': '#e6f3ea', 'iedge': '#2f7a4d'}
def box(x, y, w, h, lines, kind='box'):
    f, s = {'box': (c['box'], c['edge']), 'side': (c['side'], c['sedge']), 'inc': (c['inc'], c['iedge'])}[kind]
    t = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{f}" stroke="{s}" stroke-width="2"/>'
    n = len(lines); y0 = y + h / 2 - (n - 1) * 11 + 5
    for i, (txt, b) in enumerate(lines):
        t += f'<text x="{x + w / 2}" y="{y0 + i * 22}" text-anchor="middle" font-size="16" font-weight="{"700" if b else "400"}" fill="{c["ink"]}">{txt}</text>'
    return t
def arrow(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["edge"]}" stroke-width="2" marker-end="url(#a)"/>'
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, Arial, sans-serif">',
 f'<defs><marker id="a" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><polygon points="0 0, 10 4, 0 8" fill="{c["edge"]}"/></marker></defs>',
 f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
 f'<text x="{W/2}" y="34" text-anchor="middle" font-size="20" font-weight="700" fill="{c["ink"]}">Figura 1. Diagrama de flujo (PRISMA 2020 adaptado)</text>']
s.append(box(60, 70, 520, 92, [('IDENTIFICACIÓN', True), (f'Registros brutos de PubMed, PMC, Wiley y búsqueda web', False), (f'n = {pc["raw_records"]}  (búsquedas 7-8 oct 2026)', False)]))
s.append(box(640, 70, 300, 92, [('Duplicados eliminados', True), (f'n = {pc["duplicates_removed"]}', False)], 'side'))
s.append(arrow(580, 116, 640, 116))
s.append(arrow(320, 162, 320, 205))
s.append(box(60, 205, 520, 70, [('Registros únicos', True), (f'n = {pc["unique_records"]}', False)]))
s.append(box(640, 205, 300, 92, [('Excluidos en la identificación', True), ('homónimos no neurales', False), (f'n = {pf["excluded_at_identification"]}', False)], 'side'))
s.append(arrow(580, 240, 640, 240))
s.append(arrow(320, 275, 320, 330))
s.append(box(60, 330, 520, 92, [('CRIBADO', True), ('Título/resumen/extracto; dos revisores independientes', False), (f'n = {pf["screened"]}  (acuerdo {str(pf["percent_agreement_initial"]).replace(".", ",")} %, κ = {str(pf["cohen_kappa_4cat"]).replace(".", ",")})', False)]))
s.append(box(640, 330, 300, 114, [('Excluidos tras el cribado', True), (f'n = {pf["final_counts"]["X"]}', False), (f'(adjudicados: {pf["adjudicated"]})', False)], 'side'))
s.append(arrow(580, 376, 640, 376))
s.append(arrow(320, 422, 320, 480))
s.append(box(60, 480, 520, 92, [('INCLUIDOS', True), (f'Nivel A (específicos de la paráfisis): n = {pf["final_counts"]["A"]}', False), (f'Nivel B (contexto necesario): n = {pf["final_counts"]["B"]}', False)], 'inc'))
s.append(arrow(200, 572, 200, 640)); s.append(arrow(440, 572, 440, 640))
s.append(box(60, 640, 280, 110, [('EXTRACCIÓN', True), (f'Con contenido leído', False), (f'A: n = {A_ext};  B: n = {B_ext}', False)], 'inc'))
s.append(box(380, 640, 280, 110, [('Solo título/metadatos', True), (f'A: n = {A_tit};  B: n = {B_tit}', False), ('sin atribución de hallazgos', False)], 'side'))
s.append(arrow(200, 750, 200, 810))
s.append(box(60, 810, 520, 110, [('SÍNTESIS NARRATIVA', True), ('7 dominios; cada afirmación con marcador de evidencia', False), ('verificada por revisores independientes', False)], 'inc'))
s.append(f'<text x="60" y="960" font-size="13" fill="{c["ink"]}">Nivel A = paráfisis como objeto principal o con datos/análisis explícitos; Nivel B = contexto necesario para interpretarla.</text>')
s.append('</svg>')
open(out, 'w', encoding='utf-8').write('\n'.join(s)); print('ok', A_ext, A_tit, B_ext, B_tit)
