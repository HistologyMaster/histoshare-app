# Table S1 — Search strategies (paraphysis cerebri review)

_Estrategia equivalente para PubMed, Scopus y Web of Science. Diseñada el 13 oct 2026; aún no ejecutada — validar con el set de control antes de reportar._

Lógica (igual en las tres bases):
- **A (términos inequívocos):** frases que solo pueden referirse al órgano cerebral. Sin filtro.
- **B (término ambiguo + contexto):** paraphysis, paraphyseal, paraphysial o paraphysal, combinado con contexto neuroanatómico o taxonómico. Se le resta el bloque de homónimos.
- **C (solo título):** el término ambiguo en el título, menos los homónimos. Rescata registros antiguos sin resumen (muchos anteriores a 1990 en WoS y Scopus).
- **X (homónimos):** micología/briología/ficología ("paraphyses" del himenio) y ortopedia ("paraphyseal" = región junto a la fisis). Solo se resta a B y C, nunca a A, para no perder, por ejemplo, Nelson et al. 1985 (fracturas tras paraphysectomy).
- **Final:** A OR (B NOT X) OR (C NOT X).
- **D (opcional, reportar aparte):** histogénesis de quistes coloides, para la §7.2.

---

## PubMed (pubmed.ncbi.nlm.nih.gov, Advanced, sin límites de fecha ni idioma)
```
#1 "paraphysis cerebri"[tiab] OR "paraphyseal arch"[tiab] OR "paraphysal arch"[tiab] OR "paraphysial arch"[tiab] OR "pineal-paraphyseal"[tiab] OR "pineal paraphyseal"[tiab] OR "paraphyseal complex"[tiab] OR "paraphysial cyst"[tiab] OR "paraphysial cysts"[tiab] OR "paraphyseal cyst"[tiab] OR "paraphyseal cysts"[tiab] OR paraphysectom*[tiab] OR paraphyse[tiab]

#2 (paraphysis[tiab] OR paraphyseal[tiab] OR paraphysial[tiab] OR paraphysal[tiab]) AND (brain[tiab] OR cerebr*[tiab] OR ventric*[tiab] OR choroid*[tiab] OR pineal*[tiab] OR epiphys*[tiab] OR telenceph*[tiab] OR diencephal*[tiab] OR "roof plate"[tiab] OR "velum transversum"[tiab] OR "dorsal sac"[tiab] OR "saccus dorsalis"[tiab] OR circumventricular[tiab] OR cerebrospinal[tiab] OR "colloid cyst"[tiab] OR "colloid cysts"[tiab] OR neuroepithel*[tiab] OR ependym*[tiab] OR amphibia*[tiab] OR urodel*[tiab] OR anura*[tiab] OR salamand*[tiab] OR newt*[tiab] OR axolotl*[tiab] OR frog*[tiab] OR toad*[tiab] OR tadpole*[tiab] OR reptil*[tiab] OR lizard*[tiab] OR snake*[tiab] OR turtle*[tiab] OR tuatara[tiab] OR gecko*[tiab] OR chick*[tiab] OR avian[tiab] OR teleost*[tiab] OR fish*[tiab] OR shark*[tiab] OR elasmobranch*[tiab] OR lamprey*[tiab] OR lungfish*[tiab] OR embryo*[tiab] OR "Telencephalon"[Mesh] OR "Choroid Plexus"[Mesh] OR "Pineal Gland"[Mesh] OR "Third Ventricle"[Mesh] OR "Colloid Cysts"[Mesh])

#3 paraphysis[ti] OR paraphyseal[ti] OR paraphysial[ti] OR paraphysal[ti]

#4 fungi[tiab] OR fungus[tiab] OR fungal[tiab] OR ascomycet*[tiab] OR basidiomycet*[tiab] OR lichen*[tiab] OR apotheci*[tiab] OR ascospor*[tiab] OR asci[tiab] OR hymeni*[tiab] OR bryophyt*[tiab] OR moss[tiab] OR mosses[tiab] OR alga[tiab] OR algae[tiab] OR phaeophyc*[tiab] OR "sp. nov"[tiab] OR physis[tiab] OR physeal[tiab] OR "growth plate"[tiab] OR "growth plates"[tiab] OR metaphys*[tiab] OR exostos*[tiab] OR osteosarcoma*[tiab] OR "genu varum"[tiab] OR "genu valgum"[tiab] OR "guided growth"[tiab]

#5 #1 OR ((#2 OR #3) NOT #4)
```
Opcional (#6, reportar por separado): `("Colloid Cysts"[Mesh] OR "colloid cyst"[tiab] OR "colloid cysts"[tiab] OR "neuroepithelial cyst"[tiab] OR "neuroepithelial cysts"[tiab]) AND (histogenesis[tiab] OR origin[tiab] OR embryolog*[tiab] OR ultrastruct*[tiab] OR immunohistochem*[tiab] OR endoderm*[tiab] OR paraphys*[tiab])`

## Scopus (Advanced search; todos los años y tipos de documento)
Precedencia en Scopus: OR > AND > AND NOT. Las comillas `" "` hacen una búsqueda de frase laxa (también recuperan plurales).
```
TITLE-ABS-KEY("paraphysis cerebri" OR "paraphyseal arch" OR "paraphysal arch" OR "paraphysial arch" OR "pineal paraphyseal" OR "paraphyseal complex" OR "paraphysial cyst" OR "paraphyseal cyst" OR paraphysectom* OR paraphyse)
OR
( ( TITLE-ABS-KEY( (paraphysis OR paraphyseal OR paraphysial OR paraphysal) AND (brain OR cerebr* OR ventric* OR choroid* OR pineal* OR epiphys* OR telenceph* OR diencephal* OR "roof plate" OR "velum transversum" OR "dorsal sac" OR "saccus dorsalis" OR circumventricular OR cerebrospinal OR "colloid cyst" OR neuroepithel* OR ependym* OR amphibia* OR urodel* OR anura* OR salamand* OR newt* OR axolotl* OR frog* OR toad* OR tadpole* OR reptil* OR lizard* OR snake* OR turtle* OR tuatara OR gecko* OR chick* OR avian OR teleost* OR fish* OR shark* OR elasmobranch* OR lamprey* OR lungfish* OR embryo*) )
    OR TITLE(paraphysis OR paraphyseal OR paraphysial OR paraphysal) )
  AND NOT TITLE-ABS-KEY(fungi OR fungus OR fungal OR ascomycet* OR basidiomycet* OR lichen* OR apotheci* OR ascospor* OR asci OR hymeni* OR bryophyt* OR moss OR mosses OR alga OR algae OR phaeophyc* OR "sp. nov" OR physis OR physeal OR "growth plate" OR metaphys* OR exostos* OR osteosarcoma* OR "genu varum" OR "genu valgum" OR "guided growth") )
```

## Web of Science (Advanced Search; Core Collection, todos los años de la suscripción)
Precedencia en WoS: NEAR > SAME > NOT > AND > OR, de ahí todos los paréntesis. TS = título, resumen, palabras clave del autor y Keywords Plus.
```
#1 TS=("paraphysis cerebri" OR "paraphyseal arch" OR "paraphysal arch" OR "paraphysial arch" OR "pineal paraphyseal" OR "pineal-paraphyseal" OR "paraphyseal complex" OR "paraphysial cyst*" OR "paraphyseal cyst*" OR paraphysectom* OR paraphyse)

#2 TS=((paraphysis OR paraphyseal OR paraphysial OR paraphysal) AND (brain OR cerebr* OR ventric* OR choroid* OR pineal* OR epiphys* OR telenceph* OR diencephal* OR "roof plate" OR "velum transversum" OR "dorsal sac" OR "saccus dorsalis" OR circumventricular OR cerebrospinal OR "colloid cyst*" OR neuroepithel* OR ependym* OR amphibia* OR urodel* OR anura* OR salamand* OR newt* OR axolotl* OR frog* OR toad* OR tadpole* OR reptil* OR lizard* OR snake* OR turtle* OR tuatara OR gecko* OR chick* OR avian OR teleost* OR fish* OR shark* OR elasmobranch* OR lamprey* OR lungfish* OR embryo*))

#3 TI=(paraphysis OR paraphyseal OR paraphysial OR paraphysal)

#4 TS=(fungi OR fungus OR fungal OR ascomycet* OR basidiomycet* OR lichen* OR apotheci* OR ascospor* OR asci OR hymeni* OR bryophyt* OR moss OR mosses OR alga OR algae OR phaeophyc* OR "sp. nov*" OR physis OR physeal OR "growth plate*" OR metaphys* OR exostos* OR osteosarcoma* OR "genu varum" OR "genu valgum" OR "guided growth")

#5 #1 OR ((#2 OR #3) NOT #4)
```
Recomendación: repetir #5 en **Zoological Record** y en **BIOSIS Previews**, si la UAysén tiene acceso. Son las bases que mejor indexan la morfología comparada antigua de anfibios, reptiles y peces.

---

## Verificación (para que el autor la corra)
Probar la sensibilidad con un **set de control**. La cadena final debe recuperar todos los registros indexados en cada base:
- Ariëns Kappers 1955 (J Comp Neurol)
- Kelly 1964
- Fernández‑Llebrez et al. 1982
- Jansen 1985
- Nelson et al. 1985
- Farnesi et al. 1994
- Winkelmann et al. 2004
- Hasunuma et al. 2010
- Joven et al. 2013
- Ringler et al. 2019
- Rivas‑Manzano et al. 2022
- Cevik et al. 2025

Si falta alguno, revisar qué bloque debería haberlo traído. Además:
- Precisión: revisar los primeros 50 títulos; si más del 20 % son homónimos, ampliar #4.
- Registrar fecha, base o plataforma, n de cada línea (#1 a #5) y exportar en RIS. Esto es PRISMA‑S: va a la Tabla S1 y al diagrama de flujo.

## Registro de ejecución (completar)

| Base / plataforma | Fecha | #1 | #2 | #3 | #4 | #5 (final) | Exportado (RIS) | Set de control recuperado (n/12) |
|---|---|---|---|---|---|---|---|---|
| PubMed |  |  |  |  |  |  |  |  |
| Scopus | — | — | — | — | — | (cadena única) |  |  |
| WoS Core Collection |  |  |  |  |  |  |  |  |
| Zoological Record (opcional) |  |  |  |  |  |  |  |  |
| BIOSIS Previews (opcional) |  |  |  |  |  |  |  |  |
