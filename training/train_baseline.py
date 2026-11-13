"""Train the small model: TF-IDF features + logistic regression.

Two classifiers, trained on the teacher-labelled real notes (data/training/train.jsonl):
  - safety: dangerous or safe
  - fault:  fault_type

The safety threshold is picked on the validation set (data/training/val.jsonl) to
catch at least TARGET_RECALL of dangerous notes, because missing danger is worse
than a false alarm. The real test sets are never touched here.

    python training/train_baseline.py
Saves models/baseline.joblib. Runs in seconds on a laptop, no API calls.
"""

import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score
from sklearn.pipeline import FeatureUnion, Pipeline

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "training"
MODEL = ROOT / "models" / "baseline.joblib"
TARGET_RECALL = 0.95


def load(name: str) -> list[dict]:
    return [json.loads(line) for line in (DATA / f"{name}.jsonl").open(encoding="utf-8")]


def features() -> FeatureUnion:
    # Character pieces (2-5 letters) cope with typos and abbreviations like "u/s" and "REPL";
    # whole words and word pairs catch phrases like "brake fault".
    return FeatureUnion([
        ("chars", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), lowercase=True, sublinear_tf=True)),
        ("words", TfidfVectorizer(analyzer="word", ngram_range=(1, 2), lowercase=True, sublinear_tf=True)),
    ])


def make(labels_are_balanced: bool) -> Pipeline:
    return Pipeline([
        ("features", features()),
        ("clf", LogisticRegression(max_iter=2000, C=4.0,
                                   class_weight=None if labels_are_balanced else "balanced")),
    ])


def pick_threshold(probs: np.ndarray, truth: np.ndarray, target: float) -> float:
    """Highest threshold that still catches `target` of dangerous notes on validation."""
    for t in np.arange(0.95, 0.04, -0.01):
        if recall_score(truth, probs >= t) >= target:
            return float(round(t, 2))
    return 0.05


def main() -> None:
    train, val = load("train"), load("val")
    X_train, X_val = [r["text"] for r in train], [r["text"] for r in val]
    y_safe_train = np.array([r["safety_involved"] for r in train])
    y_safe_val = np.array([r["safety_involved"] for r in val])

    safety = make(labels_are_balanced=True).fit(X_train, y_safe_train)
    probs = safety.predict_proba(X_val)[:, 1]
    threshold = pick_threshold(probs, y_safe_val, TARGET_RECALL)
    pred = probs >= threshold
    print(f"safety  · threshold {threshold} · val recall {recall_score(y_safe_val, pred):.3f} "
          f"· val false alarms {(pred & ~y_safe_val).sum() / (~y_safe_val).sum():.3f}")

    fault = make(labels_are_balanced=False).fit(X_train, [r["fault_type"] for r in train])
    acc = accuracy_score([r["fault_type"] for r in val], fault.predict(X_val))
    print(f"fault   · val accuracy {acc:.3f}")

    MODEL.parent.mkdir(exist_ok=True)
    joblib.dump({"safety": safety, "threshold": threshold, "fault": fault}, MODEL)
    print(f"saved {MODEL.relative_to(ROOT)} ({MODEL.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
