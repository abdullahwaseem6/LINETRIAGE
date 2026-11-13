"""Write notebooks/cleaning.ipynb. Run it with:

    jupyter nbconvert --to notebook --execute --inplace notebooks/cleaning.ipynb
"""

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent

CELLS = [
    ("md", """# Cleaning the training data

Input: `data/training/raw.jsonl`, real MaintNorm notes (train split) labelled by the LLM teacher.
Output: `clean.jsonl`, split into `train.jsonl` (80%) and `val.jsonl` (20%), plus `cleaning_log.md`.

Every step logs how many rows it removes."""),
    ("code", """import json
import random
import re
from pathlib import Path

import pandas as pd
from rapidfuzz import fuzz, process

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
DATA = ROOT / "data" / "training"
raw = pd.read_json(DATA / "raw.jsonl", lines=True)
log = []

def step(name, before, after, why):
    log.append({"step": name, "rows_in": before, "removed": before - after, "rows_out": after, "why": why})
    print(f"{name}: {before} -> {after} (removed {before - after})")

df = raw.copy()
print(len(df), "raw rows")"""),
    ("md", "## 1. Normalise whitespace and stray symbols\nCollapse repeated spaces and strip leading junk characters like a stray backtick. Nothing is removed here."),
    ("code", """df["text"] = df["text"].str.replace(r"\\s+", " ", regex=True).str.strip().str.lstrip("`'\\"-=* ")
step("normalise whitespace", len(df), len(df), "formatting only")"""),
    ("md", "## 2. Drop failed labels\nRows where the teacher couldn't produce a valid label."),
    ("code", """n = len(df)
df = df[df["error"].isna() & df["fault_type"].notna()]
step("drop failed labels", n, len(df), "teacher returned no valid label")"""),
    ("md", "## 3. Drop too-short notes\nNotes under 2 words (for example just an equipment ID) carry no fault information."),
    ("code", """n = len(df)
df = df[df["text"].str.split().str.len() >= 2]
step("drop too-short notes", n, len(df), "fewer than 2 words")"""),
    ("md", "## 4. Drop exact duplicates\nSame text ignoring upper/lower case. Real work orders repeat a lot (\\\"REPLACE BUCKET TOOTH\\\")."),
    ("code", """n = len(df)
df["key"] = df["text"].str.lower()
df = df.drop_duplicates("key")
step("drop exact duplicates", n, len(df), "same text, ignoring case")"""),
    ("md", "## 5. Drop near-duplicates\nNotes that differ only by an ID or a typo (similarity ≥ 95 out of 100), keeping the first. Uses `rapidfuzz`, a fast fuzzy text-matching library. IDs like `CC708` are removed before comparing."),
    ("code", """n = len(df)
def strip_ids(t):
    return re.sub(r"\\b[a-z]{1,4}\\d{2,6}[a-z]?\\b|\\b\\d+\\b", "", t).strip()

df["key_noid"] = df["key"].map(strip_ids)
keys = df["key_noid"].tolist()
scores = process.cdist(keys, keys, scorer=fuzz.ratio, score_cutoff=95, workers=-1)
drop = set()
for i in range(len(keys)):
    if i in drop:
        continue
    for j in range(i + 1, len(keys)):
        if scores[i][j] >= 95:
            drop.add(j)
df = df.iloc[[i for i in range(len(df)) if i not in drop]]
step("drop near-duplicates", n, len(df), "similarity >= 95 after removing IDs")"""),
    ("md", "## 6. Remove test-set leaks\nAny training note that is the same as, or very similar to (≥ 90), one of our 210 real dev/test notes is removed. Otherwise the model could memorise exam answers, which is called **data leakage**."),
    ("code", """n = len(df)
test_texts = pd.concat([pd.read_csv(ROOT / "data/real/real_sample.csv"), pd.read_csv(ROOT / "data/real/real_test.csv")])["text"]
test_keys = [strip_ids(t.lower()) for t in test_texts]
leak_scores = process.cdist(df["key_noid"].tolist(), test_keys, scorer=fuzz.ratio, score_cutoff=90, workers=-1)
leak = leak_scores.max(axis=1) >= 90
print("examples removed:", df.loc[leak, "text"].head(8).tolist())
df = df[~leak]
step("remove test-set leaks", n, len(df), "same or similar (>= 90) to a dev/test note")"""),
    ("md", "## 7. Check class balance\nHow many examples of each label. Rare classes are hard for a small model to learn."),
    ("code", """df["safety_involved"] = df["safety_involved"].astype(bool)
balance_safety = df["safety_involved"].value_counts().rename({True: "dangerous", False: "safe"})
balance_fault = df["fault_type"].value_counts()
print(balance_safety, "\\n")
print(balance_fault)"""),
    ("md", "## 8. Hand-check sample\n100 random rows are saved to `hand_check.csv` for a person to check. The error rate found there is the estimated label noise of the teacher."),
    ("code", """sample = df.sample(min(100, len(df)), random_state=1)[["text", "fault_type", "safety_involved"]]
sample.assign(correct="", comment="").to_csv(DATA / "hand_check.csv", index=False)
print("wrote", len(sample), "rows to hand_check.csv")"""),
    ("md", "## 9. Split 80/20\nSplit so both parts have the same share of dangerous notes (a **stratified** split)."),
    ("code", """rng = random.Random(42)
train_idx, val_idx = [], []
for _, group in df.groupby("safety_involved"):
    idx = list(group.index)
    rng.shuffle(idx)
    cut = round(len(idx) * 0.8)
    train_idx += idx[:cut]
    val_idx += idx[cut:]
cols = ["text", "fault_type", "safety_involved", "picked_as"]
clean, train, val = df[cols], df.loc[train_idx, cols], df.loc[val_idx, cols]
for name, part in [("clean", clean), ("train", train), ("val", val)]:
    part.to_json(DATA / f"{name}.jsonl", orient="records", lines=True, force_ascii=False)
print(f"clean {len(clean)} · train {len(train)} · val {len(val)}")
print("dangerous share: train", round(train.safety_involved.mean(), 3), "· val", round(val.safety_involved.mean(), 3))"""),
    ("md", "## Cleaning log"),
    ("code", """log_df = pd.DataFrame(log)
lines = [
    "# Cleaning log", "",
    f"Raw rows: {len(raw)} real MaintNorm notes (train split), labelled by the teacher (`claude-haiku-5-5`).", "",
    "| Step | Rows in | Removed | Rows out | Why |", "|---|---|---|---|---|",
    *[f"| {r.step} | {r.rows_in} | {r.removed} | {r.rows_out} | {r.why} |" for r in log_df.itertuples()],
    "", f"**Clean: {len(clean)}** · train {len(train)} · val {len(val)}", "",
    "## Class balance (clean)", "",
    "| Label | Count |", "|---|---|",
    *[f"| {k} | {v} |" for k, v in balance_safety.items()],
    *[f"| `{k}` | {v} |" for k, v in balance_fault.items()],
    "", "Hand-check sample: `hand_check.csv` (100 rows), not yet checked by a person.",
]
(DATA / "cleaning_log.md").write_text("\\n".join(lines) + "\\n", encoding="utf-8")
log_df"""),
]


def main() -> None:
    nb = nbf.v4.new_notebook()
    nb.cells = [nbf.v4.new_markdown_cell(s) if kind == "md" else nbf.v4.new_code_cell(s) for kind, s in CELLS]
    out = ROOT / "notebooks" / "cleaning.ipynb"
    out.parent.mkdir(exist_ok=True)
    nbf.write(nb, out)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
