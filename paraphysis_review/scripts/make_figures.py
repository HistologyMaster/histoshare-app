"""Figures for the paraphysis cerebri review.

Fig. 1  PRISMA-style flow diagram (counts from search/search_log.md).
Fig. 2  Distribution of the paraphysis across vertebrate clades (cladogram).
Fig. 3  Schematic midsagittal map of the forebrain roof (generalised anamniote/sauropsid).
"""
import pathlib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = pathlib.Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})

# Okabe-Ito palette (colour-blind safe)
C_PRESENT, C_TRANSIENT, C_VARIABLE, C_UNCLEAR = "#009E73", "#56B4E9", "#E69F00", "#999999"


def box(ax, x, y, w, h, text, fc="white", ec="black", fs=7.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.015",
                                fc=fc, ec=ec, lw=0.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", wrap=True)


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=8, lw=0.8))


# ---------------- Fig. 1 PRISMA ----------------
fig, ax = plt.subplots(figsize=(7.1, 7.6))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
side = "#F2F2F2"
box(ax, 0.02, 0.86, 0.56, 0.12,
    "Records identified in PubMed/MEDLINE (5 queries, searched 10 Oct 2026)\n"
    "Q1 core 'paraphysis/paraphyseal' n = 71; Q2 n = 55; Q3 n = 76;\n"
    "Q4 n = 63; Q5 n = 5  (total n = 270)")
box(ax, 0.62, 0.86, 0.36, 0.12,
    "Records identified via other sources\n(citation chaining, web search of\nhistorical literature) n = 6", fc=side)
box(ax, 0.02, 0.70, 0.56, 0.10,
    "Duplicates removed n = 61\nRecords beyond relevance cut-off (Q3, Q4) not screened n = 49")
box(ax, 0.02, 0.55, 0.56, 0.10, "Records screened (title/abstract) n = 160")
box(ax, 0.62, 0.55, 0.36, 0.10,
    "Excluded n = 89\n(homonyms: fungal/algal 'paraphyses',\nbone 'paraphyseal'; unrelated CNS topics)", fc=side)
box(ax, 0.02, 0.38, 0.56, 0.11, "Reports assessed for eligibility n = 71")
box(ax, 0.62, 0.38, 0.36, 0.11,
    "Excluded n = 12\nno paraphysis/histogenesis data n = 7\nno morphological data or not\nretrievable n = 5", fc=side)
box(ax, 0.62, 0.70, 0.36, 0.10, "Other-source reports not retrievable n = 2\nassessed n = 4", fc=side)
box(ax, 0.02, 0.18, 0.96, 0.13,
    "Studies included in the narrative synthesis n = 63\n"
    "Phylogeny / comparative n = 21 · Ontogeny n = 14 · Anatomy & vasculature n = 13 ·\n"
    "Histology, ultrastructure & histochemistry n = 17 · Function n = 15 · Human remnant / colloid cyst n = 16\n"
    "(studies may contribute to more than one theme)", fc="#E8F4EA", bold=False)
arrow(ax, 0.30, 0.86, 0.30, 0.80); arrow(ax, 0.30, 0.70, 0.30, 0.65)
arrow(ax, 0.58, 0.60, 0.62, 0.60); arrow(ax, 0.30, 0.55, 0.30, 0.49)
arrow(ax, 0.58, 0.435, 0.62, 0.435); arrow(ax, 0.30, 0.38, 0.30, 0.31)
arrow(ax, 0.80, 0.86, 0.80, 0.80); arrow(ax, 0.80, 0.70, 0.80, 0.31)
ax.text(0.0, 0.10, "Scopus and Web of Science could not be queried from the drafting environment; the "
        "equivalent search strings are provided in Table S1\nand must be run before submission (see Limitations).",
        fontsize=6.8, style="italic", va="top")
fig.savefig(OUT / "Fig1_PRISMA.png", dpi=600, bbox_inches="tight")
fig.savefig(OUT / "Fig1_PRISMA.pdf", bbox_inches="tight")
plt.close(fig)

# ---------------- Fig. 2 Cladogram ----------------
taxa = [
    ("Cyclostomes (lampreys, hagfishes)", C_UNCLEAR, "Not documented as a discrete organ"),
    ("Chondrichthyans (sharks, rays)", C_PRESENT, "Present; tubular-saccular (Scyliorhinus, Mustelus)"),
    ("Actinopterygians (ray-finned fishes)", C_VARIABLE, "Variable: present in osteoglossomorphs, Bathylagus;\nabsent in Nezumia and many teleosts"),
    ("Dipnoans (lungfishes)", C_UNCLEAR, "Disputed: paraphysis (Dorn 1957)\nvs. dorsal sac (Tsuneki 1986)"),
    ("Amphibians (urodeles, anurans)", C_PRESENT, "Maximal development: branched tubular gland\nwith sinusoidal portal bed"),
    ("Lepidosaurs & turtles", C_PRESENT, "Large, multisaccular; often fused with pineal\n('pineal-paraphyseal complex')"),
    ("Birds", C_TRANSIENT, "Embryonic primordium; regresses or rudimentary"),
    ("Mammals (incl. human)", C_TRANSIENT, "Transient embryonic evagination\n(human: Carnegie stage 18 onwards)"),
]
fig, ax = plt.subplots(figsize=(7.1, 4.4))
ax.set_xlim(0, 10); ax.set_ylim(-0.6, len(taxa) - 0.4); ax.axis("off")
ys = list(range(len(taxa)))[::-1]
tip_x = 3.0
# topology: (Cyc,(Chond,(Act,(Dip,(Amph,((Lep+Tur,Birds),Mammals))))))
nodes = {}
def hline(x1, x2, y): ax.plot([x1, x2], [y, y], color="black", lw=1)
def vline(x, y1, y2): ax.plot([x, x], [y1, y2], color="black", lw=1)
y = {i: ys[i] for i in range(len(taxa))}
# amniotes
n_sb = 2.6; vline(n_sb, y[5], y[6]); hline(n_sb, tip_x, y[5]); hline(n_sb, tip_x, y[6]); sb = (y[5] + y[6]) / 2
n_am = 2.2; vline(n_am, sb, y[7]); hline(n_am, n_sb, sb); hline(n_am, tip_x, y[7]); am = (sb + y[7]) / 2
n_te = 1.8; vline(n_te, y[4], am); hline(n_te, tip_x, y[4]); hline(n_te, n_am, am); te = (y[4] + am) / 2
n_sa = 1.4; vline(n_sa, y[3], te); hline(n_sa, tip_x, y[3]); hline(n_sa, n_te, te); sa = (y[3] + te) / 2
n_os = 1.0; vline(n_os, y[2], sa); hline(n_os, tip_x, y[2]); hline(n_os, n_sa, sa); os_ = (y[2] + sa) / 2
n_gn = 0.6; vline(n_gn, y[1], os_); hline(n_gn, tip_x, y[1]); hline(n_gn, n_os, os_); gn = (y[1] + os_) / 2
n_v = 0.2; vline(n_v, y[0], gn); hline(n_v, tip_x, y[0]); hline(n_v, n_gn, gn)
for i, (name, col, note) in enumerate(taxa):
    ax.scatter([tip_x + 0.12], [y[i]], s=70, color=col, edgecolor="black", lw=0.5, zorder=3)
    ax.text(tip_x + 0.35, y[i], name, va="center", fontsize=7.5, fontweight="bold")
    ax.text(6.25, y[i], note, va="center", fontsize=6.6)
for lab, col in [("Present in adult", C_PRESENT), ("Transient/embryonic", C_TRANSIENT),
                 ("Variable within clade", C_VARIABLE), ("Absent, undocumented or disputed", C_UNCLEAR)]:
    pass
handles = [plt.Line2D([0], [0], marker="o", ls="", markerfacecolor=c, markeredgecolor="black", ms=7, label=l)
           for l, c in [("Present in adult", C_PRESENT), ("Transient / embryonic", C_TRANSIENT),
                        ("Variable within clade", C_VARIABLE), ("Undocumented or disputed", C_UNCLEAR)]]
ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=4, frameon=False, fontsize=6.8)
ax.text(n_te - 0.05, te + 0.18, "Tetrapoda", fontsize=6, ha="right", style="italic")
ax.text(n_am - 0.05, am + 0.18, "Amniota", fontsize=6, ha="right", style="italic")
fig.savefig(OUT / "Fig2_phylogeny.png", dpi=600, bbox_inches="tight")
fig.savefig(OUT / "Fig2_phylogeny.pdf", bbox_inches="tight")
plt.close(fig)

# ---------------- Fig. 3 Forebrain roof map ----------------
fig, ax = plt.subplots(figsize=(7.1, 3.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 4.2); ax.axis("off")
import numpy as np
xs = np.linspace(0.6, 9.4, 400)
roof = 2.0 + 0.25 * np.sin((xs - 0.6) / 8.8 * np.pi)
ax.plot(xs, roof, color="black", lw=1.4)
ax.text(0.4, 1.55, "rostral", fontsize=7, style="italic"); ax.text(9.0, 1.55, "caudal", fontsize=7, style="italic")
ax.text(5.0, 1.25, "third ventricle / telencephalon impar", ha="center", fontsize=7, color="#555555")
ax.annotate("", xy=(9.5, 1.45), xytext=(0.5, 1.45), arrowprops=dict(arrowstyle="<->", lw=0.6, color="#555555"))
structs = [  # x, label, height, colour, territory
    (1.0, "Lamina\nterminalis", 0.0, "#DDDDDD", "tel"),
    (2.3, "PARAPHYSIS", 1.25, C_PRESENT, "tel"),
    (3.6, "Velum\ntransversum", -0.55, "#CC79A7", "border"),
    (4.9, "Dorsal sac\n(saccus dorsalis)", 0.95, "#E69F00", "di"),
    (6.2, "Habenular\ncommissure", 0.0, "#DDDDDD", "di"),
    (7.3, "Pineal / parietal\norgans", 1.05, "#56B4E9", "di"),
    (8.6, "Posterior\ncommissure (SCO)", 0.0, "#DDDDDD", "di"),
]
for x, lab, h, col, terr in structs:
    y0 = 2.0 + 0.25 * np.sin((x - 0.6) / 8.8 * np.pi)
    if h > 0:
        ax.add_patch(FancyBboxPatch((x - 0.32, y0), 0.64, h, boxstyle="round,pad=0.02,rounding_size=0.25",
                                    fc=col, ec="black", lw=0.8, alpha=0.9))
        ax.text(x, y0 + h + 0.15, lab, ha="center", va="bottom", fontsize=6.8,
                fontweight="bold" if lab == "PARAPHYSIS" else "normal")
    elif h < 0:
        ax.add_patch(FancyBboxPatch((x - 0.12, y0 + h), 0.24, -h, boxstyle="round,pad=0.01,rounding_size=0.1",
                                    fc=col, ec="black", lw=0.8))
        ax.text(x, y0 + 0.2, lab, ha="center", va="bottom", fontsize=6.8)
    else:
        ax.plot([x], [y0], marker="s", color="black", ms=4)
        ax.text(x, y0 - 0.35, lab, ha="center", va="top", fontsize=6.4)
ax.plot([3.6, 3.6], [0.3, 4.1], ls="--", lw=0.7, color="#CC79A7")
ax.text(2.0, 0.35, "TELENCEPHALIC roof plate", ha="center", fontsize=7, fontweight="bold")
ax.text(6.4, 0.35, "DIENCEPHALIC roof plate", ha="center", fontsize=7, fontweight="bold")
fig.savefig(OUT / "Fig3_roof_map.png", dpi=600, bbox_inches="tight")
fig.savefig(OUT / "Fig3_roof_map.pdf", bbox_inches="tight")
plt.close(fig)
print("figures written to", OUT)
