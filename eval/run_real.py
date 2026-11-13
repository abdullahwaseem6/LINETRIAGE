"""Test the extractor on real maintenance notes (MaintNorm sample).

Usage: python eval/run_real.py [--sample data/real/real_test.csv] [--name real_test] [--runs 3]
Scores only fault_type and safety_involved: real notes don't use our station
registry, so routes would all be HUMAN_REVIEW and aren't meaningful here.
Writes eval/results/<name>.md. Costs about 2 cents per 60 notes with Haiku.
"""

import argparse
import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from linetriage import extractor
from linetriage.extractor import extract

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "eval" / "results"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--sample", type=Path, default=ROOT / "data" / "real" / "real_sample.csv")
    parser.add_argument("--name", default="real_maintnorm")
    args = parser.parse_args()
    out = RESULTS / f"{args.name}.md"

    rows = list(csv.DictReader(args.sample.open(encoding="utf-8")))
    client = extractor._default_client()

    def run(job):
        row, run_no = job
        try:
            facts = extract(row["text"], client=client)
            return row, run_no, facts.fault_type.value, facts.safety_involved
        except Exception:
            return row, run_no, None, None

    jobs = [(row, r) for r in range(1, args.runs + 1) for row in rows]
    print(f"Running {len(rows)} real notes × {args.runs} runs with {extractor.MODEL}...")
    with ThreadPoolExecutor(args.workers) as pool:
        results = list(pool.map(run, jobs))

    n = len(results)
    errors = sum(r[2] is None for r in results)
    fault_ok = sum(r[2] == r[0]["fault_type"] for r in results)
    want_safe = [r for r in results if r[0]["safety_involved"] == "true"]
    caught = sum(r[3] is True for r in want_safe)
    false_alarms = sum(r[3] is True for r in results if r[0]["safety_involved"] != "true")
    not_safe = n - len(want_safe)
    by_note = {}
    for row, _, ft, safe in results:
        by_note.setdefault(row["id"], set()).add((ft, safe))
    consistent = sum(len(v) == 1 for v in by_note.values())

    wrong = sorted(
        {(r[0]["id"], r[0]["text"], r[0]["fault_type"], r[0]["safety_involved"], r[2], str(r[3]).lower())
         for r in results if r[2] != r[0]["fault_type"] or str(r[3]).lower() != r[0]["safety_involved"]}
    )

    def pct(a, b):
        return f"{100 * a / b:.1f}%" if b else "n/a"

    lines = [
        f"# Real-data test: {args.name}",
        "",
        f"{date.today()} · model `{extractor.MODEL}` · `{args.sample.name}` · {len(rows)} real notes × {args.runs} runs = {n} runs",
        "",
        "Real maintenance notes from Australian mining companies ([MaintNorm](https://github.com/nlp-tlp/maintnorm), MIT).",
        "Labels drafted by Claude Opus, pending human review. Only `fault_type` and `safety_involved` are scored.",
        "",
        "| Metric | Result |",
        "|---|---|",
        f"| **Safety recall** | **{pct(caught, len(want_safe))}** ({caught}/{len(want_safe)} runs) |",
        f"| False safety alarms | {pct(false_alarms, not_safe)} ({false_alarms}/{not_safe} runs) |",
        f"| `fault_type` accuracy | {pct(fault_ok, n)} |",
        f"| Same answer on every run | {pct(consistent, len(by_note))} of notes |",
        f"| Failed extractions | {errors} |",
        "",
        "## Disagreements",
        "",
        "| Note | Text | Label (fault, safety) | Haiku (fault, safety) |",
        "|---|---|---|---|",
        *[f"| {i} | {t} | {ft}, {s} | {gft}, {gs} |" for i, t, ft, s, gft, gs in wrong],
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Safety recall {pct(caught, len(want_safe))} · false alarms {pct(false_alarms, not_safe)} "
          f"· fault_type {pct(fault_ok, n)}")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
