# LineTriage

Turns messy factory fault reports, in English, Hungarian or German, into checked facts and a recommended route. The AI only extracts facts, tested rules make the decision, and a human approves.

## The problem

Operators write quick shift notes like *"st 5 conveyor jammed couple of times today"* or *"2es hegesztonel a vesz-stop gomb beragadt, de megy a gep"* (the emergency stop is stuck, but the machine is running). Someone has to read every note and decide what happens next. That's slow, and hidden safety issues get missed.

## How it works

```
operator note
   │
   ▼
extractor.py   Claude Haiku reads the note and returns facts only
   │           (station, fault type, downtime, recurring, safety risk, part, language)
   ▼
schema.py      Pydantic checks every fact: allowed values, ranges, no invented fields
   │
   ▼
rules.py       Plain, tested Python picks the route. First match wins:
   │             1. Safety risk                    → SAFETY_ALERT
   │             2. Unknown or missing station     → HUMAN_REVIEW
   │             3. Recurring fault                → ESCALATE_QUALITY
   │             4. ≥ 30 min down on a HIGH station → ESCALATE_QUALITY
   │             5. Quality fault on a named part  → ESCALATE_QUALITY
   │             6. Otherwise                      → AUTO_TICKET
   ▼
human approves or overrides
```

**Design rules**
- The AI never decides a route. Routing lives only in `rules.py`, where it is tested.
- Safety always goes to a human. That rule comes first and can't be weakened.
- Report text is treated as untrusted data, never as instructions.

## Results

60 handwritten test reports (English, Hungarian, German, mixed; typos, slang, vague times, hidden safety issues), each run 3 times with Claude Haiku 5.5:

| Metric | Result |
|---|---|
| **Safety recall** | **100%** (45/45 safety runs caught) |
| Route accuracy | 97.2% |
| Latency | 2.0s average |
| Cost per 1,000 reports | $0.39 |

A schema review raised route accuracy from 95.0% to 98.3% and cut wrong answers from 56 to 17. Adding rules for real heavy-equipment notes (below) cost a little here: 98.3% → 97.2%, safety recall unchanged. See [the before/after write-up](eval/results/schema_review.md).

**On real notes** ([MaintNorm](https://github.com/nlp-tlp/maintnorm): mining maintenance work orders), safety recall was only **63.5%** at first: calm notes like "Replace brake hose" weren't seen as risks. After adding rules learned from a separate dev set, recall on 150 unseen real notes rose to **about 90–93%** (it varies between runs), at the cost of more false alarms (11–13%). See [the real-data write-up](eval/results/real_data.md).

**Own model vs the LLM** (150 real test notes): a small TF-IDF + logistic regression model, trained in 3 seconds on 1,076 real notes labelled by Haiku, runs in under 1 ms for free. At Haiku's false-alarm level it catches 75% of dangerous notes against Haiku's 92%. Used as a second opinion (flag if either says dangerous), recall rises to **98.2%**. See [the model comparison](eval/results/model_comparison.md).

## What still fails

- Notes describing two faults keep only the more serious one (the schema holds one fault).
- One false safety alarm: "let it cool" is read as overheating. It errs on the safe side.
- Slang like "pc is dead dead" is sometimes classed as `other` instead of `electrical`. The route is still correct.
- On real notes, safety recall is about 90–93%, not 100%: specialised safety equipment (gas testers, interlock switches) is still missed.
- The 60 factory reports and station registry are synthetic; the real notes are English mining work orders, labelled by Claude Opus and not yet reviewed by a human.

## Run it

Needs Python 3.11+ and an [Anthropic API key](https://console.anthropic.com).

```bash
git clone https://github.com/abdullahwaseem6/LINETRIAGE.git
cd LINETRIAGE
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env          # then put your API key in .env

pytest                                   # 219 tests, offline, free
uvicorn linetriage.api:app --reload      # web page at http://localhost:8000
python eval/run_eval.py                  # full evaluation (about 6 cents)
```

## Project layout

| Path | What it is |
|---|---|
| `src/linetriage/schema.py` | The facts model (Pydantic) |
| `src/linetriage/registry.py` | 10 stations with HIGH/MEDIUM/LOW importance |
| `src/linetriage/rules.py` | The routing rules |
| `src/linetriage/extractor.py` | The only file that calls the LLM |
| `src/linetriage/api.py` | FastAPI: `POST /triage` and the web page |
| `src/linetriage/metrics.py` | Scoring for the evaluation |
| `data/reports.jsonl` | 60 labelled test reports |
| `data/LABELLING.md` | How each field is labelled |
| `eval/run_eval.py` | Runs the evaluation and writes `eval/results/` |
| `eval/run_real.py` | Tests on real MaintNorm notes |
| `data/real/` | Real notes: 60 dev + 150 test, labelled |
| `data/training/` | 1,345 cleaned training notes + cleaning log |
| `notebooks/cleaning.ipynb` | The cleaning steps |
| `training/train_baseline.py` | Trains the small model |
| `eval/compare_models.py` | LLM vs small model on the real test set |

## Roadmap

- [x] Rules, schema and test reports
- [x] LLM extraction, API and web page
- [x] Evaluation and baseline
- [x] 1,345 real training notes (MaintNorm), labelled by the LLM and cleaned ([log](data/training/cleaning_log.md))
- [x] Train a small model and compare it with the LLM
- [ ] Fine-tune a multilingual transformer (XLM-RoBERTa)
- [ ] Attack the system with prompt injection, harden it, re-test
- [ ] Human review UI with decision log
