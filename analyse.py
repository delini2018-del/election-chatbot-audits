"""Pool every published audit of how chatbots answer election and news questions (2023-2026).

Each audit asked different questions and graded differently, so we do not average them blindly.
We keep two measures per study where available:
  strict = the share of answers containing an outright factual error
  broad  = the share with any significant problem (errors, missing or outdated info, bad sourcing, bias)
and tag each study by task: voting procedures, election facts, news questions, or deliberately false claims.
"""
import csv, json, statistics as st

A = list(csv.DictReader(open("data/audits.csv")))
M = list(csv.DictReader(open("data/per_model.csv")))
num = lambda s: float(s) if s not in ("", None) else None
for a in A:
    a["strict_pct"], a["broad_pct"] = num(a["strict_pct"]), num(a["broad_pct"])

by_task = {}
for a in A:
    if a["strict_pct"] is not None:
        by_task.setdefault(a["task"], []).append(a["strict_pct"])
task_median = {k: st.median(v) for k, v in by_task.items()}

us26 = [a for a in A if a["published"].startswith("2026") and a["region"] == "US" and a["task"] != "false news claims"]
strict26 = sorted(a["strict_pct"] for a in us26)
broad26 = sorted(a["broad_pct"] for a in us26 if a["broad_pct"] is not None)

# chance a voter who asks k questions gets at least one bad answer, if answers were independent
def at_least_one(p, k): return 1 - (1 - p / 100) ** k
chance = {f"{p}%": {k: round(100 * at_least_one(p, k), 1) for k in (1, 3, 5, 10)} for p in (2.9, 6, 8.2, 29, 36)}

# ISD ladder: what counts as wrong
isd_ladder = [("Inaccurate", 6), ("+ outdated", 12), ("+ incomplete or unclear", 29)]
forum_ladder = [("Factual error", 36), ("+ bias or poor sourcing", 90)]

# rank flips: same product family, different studies
fam = {"Gemini": ["Gemini", "Gemini 3.5 Flash", "Google AI"], "ChatGPT": ["ChatGPT", "GPT-4", "GPT-5.5"], "Perplexity": ["Perplexity"]}
ranks = []
for study in sorted({m["study"] for m in M}):
    rs = [m for m in M if m["study"] == study]
    order = sorted(rs, key=lambda m: float(m["value_pct"]))
    for i, m in enumerate(order):
        f = next((k for k, v in fam.items() if m["model"] in v), None)
        ranks.append(dict(study=study, year=m["year"], model=m["model"], family=f, value=float(m["value_pct"]), rank=i + 1, of=len(order)))

R = dict(n_studies=len(A), task_median=task_median, strict_2026_us=strict26, broad_2026_us=broad26,
         median_strict_2026_us=st.median(strict26), chance=chance, isd_ladder=isd_ladder, forum_ladder=forum_ladder,
         ranks=ranks, newsguard=[("Aug 2024", 18), ("Aug 2025", 35), ("Jan 2026", 28)],
         isd_lang={"English": 71, "Spanish": 55}, isd_adversarial={"refuted_en": 91, "refuted_es": 89, "affirmed_en": 1, "affirmed_es": 2},
         false_premise_multiplier=4, pew_share_adults=8)
json.dump(R, open("results/results.json", "w"), indent=1)
print("studies", len(A)); print("task medians", task_median); print("2026 US strict", strict26, "median", R["median_strict_2026_us"]); print("broad", broad26)
print(json.dumps(chance, indent=0))
for r in ranks:
    if r["family"]: print(r)
