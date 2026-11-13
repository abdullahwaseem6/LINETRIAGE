"""Compare the LLM teacher with the small model on the 150 real test notes.

Needs eval/results/haiku_test_predictions.jsonl, made by:
    python eval/run_real.py --sample data/real/real_test.csv --name haiku_test --save
and models/baseline.joblib, made by training/train_baseline.py.

    python eval/compare_models.py
Writes eval/results/model_comparison.md. No API calls.
"""

import csv
import json
import time
from collections import Counter
from pathlib import Path

import joblib
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "eval" / "results"
FAULTS = ["mechanical", "electrical", "sensor", "quality", "safety", "other"]

# Measured in this project: Haiku costs about $0.39 per 1,000 reports (eval/results/factory_v3.md)
# and takes about 2 s per report.
HAIKU_COST_PER_1K = 0.39


def score(truth_safe, pred_safe, truth_fault, pred_fault) -> dict:
    truth_safe, pred_safe = np.array(truth_safe), np.array(pred_safe)
    return {
        "recall": (pred_safe & truth_safe).sum() / truth_safe.sum(),
        "false_alarms": (pred_safe & ~truth_safe).sum() / (~truth_safe).sum(),
        "missed": int((~pred_safe & truth_safe).sum()),
        "fault_acc": float(np.mean([t == p for t, p in zip(truth_fault, pred_fault)])) if pred_fault else None,
    }


def confusion(truth, pred) -> list[str]:
    labels = [f for f in FAULTS if f in set(truth) | set(pred)]
    counts = Counter(zip(truth, pred))
    rows = ["| label ↓ / predicted → | " + " | ".join(labels) + " |", "|---" * (len(labels) + 1) + "|"]
    for t in labels:
        rows.append(f"| **{t}** | " + " | ".join(str(counts[(t, p)]) or "0" for p in labels) + " |")
    return rows


def main() -> None:
    rows = list(csv.DictReader((ROOT / "data/real/real_test.csv").open(encoding="utf-8")))
    by_id = {r["id"]: r for r in rows}
    texts = [r["text"] for r in rows]
    truth_safe = [r["safety_involved"] == "true" for r in rows]
    truth_fault = [r["fault_type"] for r in rows]

    # Small model: deterministic, so one pass is enough. Time it per note.
    model = joblib.load(ROOT / "models" / "baseline.joblib")
    start = time.perf_counter()
    probs = model["safety"].predict_proba(texts)[:, 1]
    small_fault = list(model["fault"].predict(texts))
    small_ms = (time.perf_counter() - start) / len(texts) * 1000
    small_safe = list(probs >= model["threshold"])
    small = score(truth_safe, small_safe, truth_fault, small_fault)

    # Haiku: 3 runs per note. Score every run, then combine with the small model run by run.
    preds = [json.loads(line) for line in (RESULTS / "haiku_test_predictions.jsonl").open()]
    small_by_id = {r["id"]: s for r, s in zip(rows, small_safe)}
    h_truth_safe = [by_id[p["id"]]["safety_involved"] == "true" for p in preds]
    h_truth_fault = [by_id[p["id"]]["fault_type"] for p in preds]
    h_safe = [bool(p["safety_involved"]) for p in preds]
    haiku = score(h_truth_safe, h_safe, h_truth_fault, [p["fault_type"] for p in preds])
    either = score(h_truth_safe, [h or small_by_id[p["id"]] for h, p in zip(h_safe, preds)], [], [])
    haiku["missed"] /= 3  # per pass over the 150 notes
    either["missed"] /= 3

    missed_small = [r["text"] for r, s, t in zip(rows, small_safe, truth_safe) if t and not s]

    pct = lambda x: f"{100 * x:.1f}%"  # noqa: E731
    lines = [
        "# Model comparison: LLM vs small model",
        "",
        "150 real MaintNorm test notes (`data/real/real_test.csv`), never used for training or tuning the small model.",
        "The small model was trained on 1,076 different real notes labelled by Haiku (distillation).",
        "",
        "| | Safety recall | False safety alarms | Missed dangerous notes | `fault_type` accuracy | Time per note | Cost per 1,000 notes |",
        "|---|---|---|---|---|---|---|",
        f"| **Haiku (LLM teacher)** | **{pct(haiku['recall'])}** | {pct(haiku['false_alarms'])} | {haiku['missed']:.1f} of 56 | {pct(haiku['fault_acc'])} | ~2,000 ms | ${HAIKU_COST_PER_1K:.2f} |",
        f"| **Small model** (TF-IDF + logistic regression) | **{pct(small['recall'])}** | {pct(small['false_alarms'])} | {small['missed']} of 56 | {pct(small['fault_acc'])} | {small_ms:.2f} ms | $0 |",
        f"| **Either flags it** (second opinion) | **{pct(either['recall'])}** | {pct(either['false_alarms'])} | {either['missed']:.1f} of 56 | | ~2,000 ms | ${HAIKU_COST_PER_1K:.2f} |",
        "",
        f"Haiku numbers are averaged over 3 runs. The small model's safety threshold ({model['threshold']}) was picked on the validation set to catch at least 95% of dangerous notes there.",
        "",
        "## Dangerous notes the small model missed",
        "",
        *[f"- {t}" for t in missed_small],
        "",
        "## Fault type: confusion matrix",
        "",
        "Rows are the correct label, columns what the model said. The diagonal is correct.",
        "",
        "**Small model**",
        "",
        *confusion(truth_fault, small_fault),
        "",
        "**Haiku** (all 3 runs)",
        "",
        *confusion(h_truth_fault, [p["fault_type"] for p in preds]),
    ]
    out = RESULTS / "model_comparison.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[5:9]))
    print(f"\nwrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
