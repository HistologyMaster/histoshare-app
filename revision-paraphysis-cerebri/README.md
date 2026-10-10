# Paráfisis cerebral (*paraphysis cerebri*): revisión sistemática narrativa

Revisión bibliográfica sistemática y narrativa sobre la **filogenia, ontogenia, anatomía, histología y fisiología** de la paráfisis cerebral, con un apartado de correlatos clínicos (origen del quiste coloide del tercer ventrículo).

> **Estado: BORRADOR no listo para envío.** Generado con asistencia de inteligencia artificial (búsquedas del 7–8 de octubre de 2026). Cada afirmación empírica remite a un registro de evidencia y fue contrastada por verificadores independientes, que también son agentes de IA. **Ninguna referencia ha sido verificada por una persona frente a la fuente primaria.** Autoría, afiliaciones, financiamiento y conflictos de interés están pendientes y deben completarlos los autores humanos.

## Documento principal

| Archivo | Contenido |
|---|---|
| `revision_paraphysis_cerebri.pdf` | Versión para lectura (≈70 páginas) |
| `revision_paraphysis_cerebri.docx` | Versión editable (Word) |
| `revision_paraphysis_cerebri.html` | Versión web autocontenida |
| `revision_paraphysis_cerebri.md` | Fuente en Markdown |
| `referencias_mapa.csv` | Número de referencia ↔ registro (RID), PMID, DOI y si la referencia fue verificada en PubMed |
| `figuras/` | Figura 1 (diagrama de flujo PRISMA) en SVG y PNG |

## Qué encontrará y qué no

- La base de evidencia es **antigua, heterogénea y poco profunda**: de 113 estudios específicos de la paráfisis, solo 7 se leyeron a texto completo y 44 se conocen únicamente por su título (la literatura clásica no indexada en PubMed no pudo abrirse). El documento lo declara en cada sección ("Vacíos de evidencia").
- El resultado más sólido es conceptual: «paráfisis» **no designa de forma constante la misma estructura** (techo telencefálico frente a diencefálico; saco dorsal; divertículo epitalámico).
- Las referencias que no pudieron confirmarse en PubMed están marcadas como tales en la lista y en el Anexo A/B.

## Trazabilidad (todo reproducible)

```
busqueda/      17 archivos de búsqueda por agente (consultas, fallos y registros), corpus deduplicado (663), registro de consultas (search_log.json), conteos PRISMA
cribado/       decisiones de los dos revisores independientes por lote, adjudicaciones, lista final (A/B), screening_log.csv, kappa
extraccion/    base de extracción (db.json), lotes e*.json y los textos fuente guardados (src/) contra los que se verificó cada cita literal
sintesis/      secciones S1–S7 y partes integradoras, afirmaciones parseadas (afirmaciones/), veredictos de verificación (verificacion/)
herramientas/  scripts de fusión, cribado, verificación de citas, ensamblado y exportación
```

Marcadores de evidencia usados en `sintesis/`: `[@R217.3]` (hallazgo extraído), `[@R185.m1]` (mención secundaria) y `[@R070.t]` (solo identificación por título). El ensamblador (`herramientas/assemble.py`) los convierte en referencias numeradas.

## Limitaciones de acceso declaradas

PubMed/PMC, Wiley Scholar Gateway (30 consultas, cuota gratuita agotada) y una búsqueda web de descubrimiento fueron los únicos canales. Scite (cuota agotada) y Elicit (sin API en el plan) no estuvieron disponibles, y la política de red bloqueó Europe PMC, OpenAlex, Crossref, Semantic Scholar, doi.org, BHL, Internet Archive y varias editoriales. No se consultaron Embase, Scopus ni Web of Science. El detalle está en la sección 2 y en la sección 5 del documento.
