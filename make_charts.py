"""Figures for the chatbot election-accuracy article, from data/ and results/results.json."""
import csv, json
from datetime import date
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.text as mtext
mtext.Text._preprocess_math = lambda self, s: (s, False)

R = json.load(open("results/results.json"))
A = list(csv.DictReader(open("data/audits.csv")))
INK, INK2, GRID, BG = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
BLUE, ORANGE, AQUA, YELLOW, MAG = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "figure.facecolor": BG, "axes.facecolor": BG})
def title(fig, t, sub):
    fig.text(0.02, 0.965, t, ha="left", va="top", fontsize=15, color=INK, weight="bold")
    fig.text(0.02, 0.905, sub, ha="left", va="top", fontsize=11, color=INK2)

GROUP = {"voting procedures": ("Basic voting questions", AQUA), "local political issues": ("Basic voting questions", AQUA),
         "election facts": ("Election facts", BLUE), "election facts & fact-checks": ("Election facts", BLUE),
         "news questions": ("News questions", YELLOW), "identify news article source": ("News questions", YELLOW),
         "election news questions": ("News questions", YELLOW), "false news claims": ("Deliberately false claims", ORANGE)}
SHORT = {"aw23": "AlgorithmWatch", "aidp24": "AI Democracy\nProjects", "gt24": "GroundTruthAI", "ri24": "Reuters Inst.", "ng24": "NewsGuard",
         "bbc25": "BBC", "tow25": "Tow Center", "ng25": "NewsGuard", "ebu25": "EBU + BBC", "su25": "States United", "ng26": "NewsGuard",
         "su26": "States United", "forum26": "Forum AI", "isd26": "ISD", "srch26": "Searchable"}
def d(s):
    p = [int(x) for x in s.split("-")] + [15]
    return date(p[0], p[1], min(p[2], 28))

# ---------- 1: every audit on one timeline ----------
fig, ax = plt.subplots(figsize=(11.5, 6.4))
off = {"aw23": (8, 4), "aidp24": (8, -14), "gt24": (8, -4), "ri24": (8, -4), "ng24": (-8, -14), "bbc25": (8, -4), "tow25": (8, 0),
       "ng25": (8, 0), "ebu25": (8, -4), "su25": (-8, 10), "ng26": (8, 0), "su26": (8, -2), "forum26": (-8, 4), "isd26": (8, -2), "srch26": (8, 4)}
for a in A:
    lab, col = GROUP[a["task"]]; x = d(a["published"])
    s, b = (float(a["strict_pct"]) if a["strict_pct"] else None), (float(a["broad_pct"]) if a["broad_pct"] else None)
    if a["id"] == "aidp24": b = None   # its second figure is 'harmful', not a superset of 'inaccurate'

    if s is not None and b is not None:
        ax.plot([x, x], [s, b], color=col, lw=1.4, alpha=0.6)
    if s is not None:
        ax.plot(x, s, "o", ms=10, color=col, mec=BG, mew=1.5)
    if b is not None:
        ax.plot(x, b, "o", ms=10, mfc=BG, mec=col, mew=2)
    y = s if s is not None else b
    dx, dy = off[a["id"]]
    ax.annotate(SHORT[a["id"]].replace("\n", " "), (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=8.5, color=INK2,
                ha="left" if dx > 0 else "right", va="center")
for lab, col in (("Basic voting questions", AQUA), ("Election facts", BLUE), ("News questions", YELLOW), ("Deliberately false claims", ORANGE)):
    ax.plot([], [], "o", ms=9, color=col, label=lab)
ax.plot([], [], "o", ms=9, color=INK2, label="Outright factual errors (filled)")
ax.plot([], [], "o", ms=9, mfc=BG, mec=INK2, mew=2, label="Any significant problem (hollow)")
ax.axvline(date(2026, 11, 3), color=INK, lw=1, ls=":"); ax.text(date(2026, 10, 20), 96, "US midterms\n3 Nov 2026", ha="right", va="top", fontsize=9.5, color=INK)
ax.set_ylim(-3, 100); ax.set_xlim(date(2023, 9, 1), date(2027, 1, 15))
ax.set_ylabel("Share of chatbot answers (%)"); ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="upper left", fontsize=9.5, ncol=2)
title(fig, "Fifteen audits, error rates from 0% to 90%. The question decides the answer",
      "Every published test of chatbots on election and news questions I could find, 2023–2026, by publication date")
fig.subplots_adjust(top=0.84, left=0.07, right=0.98, bottom=0.08)
fig.savefig("charts/01_all_audits.png", dpi=200); plt.close(fig)

# ---------- 2: what counts as wrong ----------
fig, ax = plt.subplots(figsize=(11, 4.8))
rows = [("ISD, June 2026\n2,400 voting answers", [(6, "inaccurate", ORANGE), (6, "outdated", YELLOW), (17, "incomplete or unclear", "#c9c7c0")]),
        ("Forum AI, May 2026\nelection news answers", [(36, "factual error", ORANGE), (54, "bias or poor sourcing only", "#c9c7c0")])]
from matplotlib.patches import Patch
seen, handles = set(), []
for i, (lab, parts) in enumerate(rows):
    left = 0
    for v, name, col in parts:
        ax.barh(i, v, left=left, color=col, height=0.55, edgecolor=BG, lw=1)
        ax.text(left + v / 2, i, f"{v}%", ha="center", va="center", fontsize=10.5, color=INK)
        if name not in seen: handles.append(Patch(color=col, label=name)); seen.add(name)
        left += v
    ax.text(left + 1.2, i, f"{left}% flagged", va="center", fontsize=11, weight="bold", color=INK)
ax.legend(handles=handles, frameon=False, loc="upper right", fontsize=10, ncol=2)
ax.set_yticks(range(len(rows)), [r[0] for r in rows]); ax.invert_yaxis(); ax.set_xlim(0, 105)
ax.set_xlabel("Share of answers (%)"); ax.grid(axis="x", color=GRID); ax.set_axisbelow(True)
ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
title(fig, "The headline number depends on what you count as wrong",
      "Same answers, different definitions: outright errors versus every problem the researchers flagged (ISD parts rounded)")
fig.subplots_adjust(top=0.8, left=0.22, right=0.97, bottom=0.14)
fig.savefig("charts/02_definitions.png", dpi=200); plt.close(fig)

# ---------- 3: ISD per model, English vs Spanish ----------
eng = {"GPT-5.5": 89, "Gemini 3.5 Flash": 84, "Grok 4.3": 66, "Sonnet 4.6": 64, "DeepSeek V4 Pro": 63, "Muse Spark": 61}
spa = {"GPT-5.5": 82, "DeepSeek V4 Pro": 40, "Muse Spark": 38}
fig, ax = plt.subplots(figsize=(11, 5.4))
models = list(eng); y = np.arange(len(models))
for yi, m in zip(y, models):
    if m in spa:
        ax.plot([spa[m], eng[m]], [yi, yi], color=GRID, lw=4, zorder=1)
        ax.plot(spa[m], yi, "o", ms=12, color=ORANGE, mec=BG, mew=2, zorder=3); ax.text(spa[m] - 2.5, yi, f"{spa[m]}%", ha="right", va="center", fontsize=10, color=ORANGE)
    else:
        ax.text(eng[m] - 2.5, yi, "Spanish: not reported" if m.startswith("Gemini") else "Spanish: under 60%", ha="right", va="center", fontsize=9, color=INK2, style="italic")
    ax.plot(eng[m], yi, "o", ms=12, color=BLUE, mec=BG, mew=2, zorder=3); ax.text(eng[m] + 2.5, yi, f"{eng[m]}%", va="center", fontsize=10, color=BLUE)
ax.plot([], [], "o", ms=10, color=BLUE, label="English"); ax.plot([], [], "o", ms=10, color=ORANGE, label="Spanish")
ax.set_yticks(y, models); ax.invert_yaxis(); ax.set_xlim(20, 100)
ax.set_xlabel("Answers to basic voting questions that were accurate, specific and complete (%)")
ax.grid(axis="x", color=GRID); ax.set_axisbelow(True); ax.legend(frameon=False, loc="lower right", fontsize=10.5)
ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
title(fig, "The chatbot you pick, and the language you ask in, matter more than the year",
      "ISD test, June 2026: 400 voting questions per chatbot across ten states, with web search on (Spanish shown where the report gives a figure)")
fig.subplots_adjust(top=0.84, left=0.17, right=0.97, bottom=0.12)
fig.savefig("charts/03_models_language.png", dpi=200); plt.close(fig)

# ---------- 4: chance of at least one bad answer ----------
fig, ax = plt.subplots(figsize=(11, 5.4))
k = np.arange(1, 11)
for p, col, lab in ((2.9, AQUA, "2.9%: best tool, Searchable test"), (8.2, BLUE, "8.2%: average, Searchable test"),
                    (29, YELLOW, "29%: ISD, any problem"), (36, ORANGE, "36%: Forum AI, factual errors")):
    v = 100 * (1 - (1 - p / 100) ** k)
    ax.plot(k, v, color=col, lw=2.6, marker="o", ms=6, mec=BG)
    ax.text(10.25, v[-1] + {36: 2.2, 29: -2.2}.get(p, 0), lab, va="center", fontsize=10, color=col)
ax.axvline(5, color=INK2, ls=":", lw=1); ax.text(5.1, 4, "5 questions", fontsize=9.5, color=INK2)
ax.set_xticks(k); ax.set_xlim(0.7, 14.6); ax.set_ylim(0, 103)
ax.set_xlabel("Number of election questions one voter asks"); ax.set_ylabel("Chance at least one answer is wrong (%)")
ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
title(fig, "Small error rates add up over a conversation",
      "If each answer is wrong independently at the rate an audit measured, the chance a voter meets at least one bad answer")
fig.subplots_adjust(top=0.84, left=0.08, right=0.98, bottom=0.12)
fig.savefig("charts/04_compounding.png", dpi=200); plt.close(fig)
print("ok")
