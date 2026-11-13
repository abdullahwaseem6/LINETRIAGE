"""Build the raw training set: real MaintNorm notes labelled by the LLM (the "teacher").

Picks notes from MaintNorm's *train* split only (never the test split, which our
dev and test sets come from), runs the extractor on each, and saves the labels.
Safe to re-run: notes already in the output file are skipped.

    python scripts/label_training.py --n 1500
Writes data/training/raw.jsonl. Costs about $0.60 with Haiku for 1,500 notes.
"""

import argparse
import json
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from linetriage import extractor
from linetriage.extractor import Usage, extract

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sample_real import RISKY, read_notes  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "real" / "maintnorm" / "train.norm"
OUT = ROOT / "data" / "training" / "raw.jsonl"

# Haiku 5.5 prices, US dollars per million tokens.
PRICE_IN, PRICE_OUT = 0.10, 0.50


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--n", type=int, default=1500)
    parser.add_argument("--risky-share", type=float, default=1 / 3,
                        help="share picked from notes with risk words, so safety cases aren't too rare")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    notes = sorted(set(read_notes(SOURCE)))
    rng = random.Random(args.seed)
    n_risky = round(args.n * args.risky_share)
    risky = [n for n in notes if RISKY.search(n)]
    picked = rng.sample(risky, n_risky)
    chosen = set(picked)
    picked += rng.sample([n for n in notes if n not in chosen], args.n - n_risky)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if OUT.exists():
        done = {json.loads(line)["text"] for line in OUT.open(encoding="utf-8")}
    todo = [t for t in picked if t not in done]
    print(f"{len(notes)} notes in train split · picked {len(picked)} · {len(done)} already labelled · {len(todo)} to go")

    client = extractor._default_client()
    usage = Usage()

    def label(text: str) -> dict:
        try:
            facts = extract(text, client=client, usage=usage)
            return {"text": text, "fault_type": facts.fault_type.value,
                    "safety_involved": facts.safety_involved, "error": None}
        except Exception as e:  # recorded and dropped later in cleaning
            return {"text": text, "fault_type": None, "safety_involved": None,
                    "error": f"{type(e).__name__}: {e}"}

    with OUT.open("a", encoding="utf-8") as f, ThreadPoolExecutor(args.workers) as pool:
        for i, row in enumerate(pool.map(label, todo), 1):
            row["picked_as"] = "risky" if RISKY.search(row["text"]) else "random"
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            if i % 100 == 0 or i == len(todo):
                print(f"{i}/{len(todo)}", flush=True)

    cost = (usage.input_tokens * PRICE_IN + usage.output_tokens * PRICE_OUT) / 1_000_000
    print(f"Done. {usage.calls} calls · ${cost:.2f} · wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
