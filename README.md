# election-chatbot-audits

Data and code for the Medium article **"Voters Will Ask AI Chatbots About Tuesday's Election. I Checked Every Test of How Often They're Wrong."** by Delini.

Fifteen published audits of chatbots on election and news questions (2023–2026) put on one scale, sorted by the kind of question asked and by how strictly "wrong" was defined.

## Files

- `data/audits.csv`: one row per audit, with publisher, dates, region, task type, strict error rate (outright factual errors), broad rate (any significant problem), sample size and source URL
- `data/per_model.csv`: per-chatbot results where a study reported them
- `analyse.py`: medians by task type, the compounding calculation, cross-study model ranks. Writes `results/results.json`
- `make_charts.py`: the four article figures, written to `charts/`
- `cover/cover.py`: the code-drawn cover (no AI image generation)
- `election_chatbot_audits.ipynb`: the same steps as a Colab notebook

## Run

```
pip install -r requirements.txt
python analyse.py
python make_charts.py
```

## Notes

Studies use different questions, graders and definitions, so rates are compared side by side, not averaged. Some figures come from news coverage of a report, as noted in `source_url`. Chance of at least one wrong answer in k questions at error rate p is 1 - (1 - p)^k, assuming independence.

MIT licence.
