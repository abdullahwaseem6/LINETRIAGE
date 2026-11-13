"""Run every labelled report through extractor + rules and score the results.

Usage: python eval/run_eval.py [--runs 3] [--workers 5] [--name baseline]
Writes eval/results/<name>.md (the table) and <name>_errors.jsonl (every wrong answer).
This calls the real API and costs money (Haiku: about 2 cents for 60 reports x 3 runs).
"""

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from linetriage import extractor
from linetriage.extractor import Usage, extract
from linetriage.metrics import FIELDS, summarize, wrong_fields
from linetriage.rules import route_report

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "data" / "reports.jsonl"
RESULTS = ROOT / "eval" / "results"

# US dollars per million tokens (Claude Haiku 5.5, prompts under 100K tokens).
PRICE_IN = 0.10
PRICE_OUT = 0.50


def run_one(row: dict, run: int, client) -> tuple[dict, Usage]:
    usage = Usage()
    start = time.perf_counter()
    try:
        facts = extract(row["text"], client=client, usage=usage)
        got = facts.model_dump(mode="json")
        route = route_report(facts).route.value
        error = None
    except Exception as e:  # any failure is recorded, not fatal
        got, route, error = None, None, f"{type(e).__name__}: {e}"
    result = {
        "id": row["id"],
        "run": run,
        "text": row["text"],
        "expected": row["expected"],
        "expected_route": row["expected_route"],
        "got": got,
        "route": route,
        "error": error,
        "latency": time.perf_counter() - start,
    }
    return result, usage


def pct(x: float | None) -> str:
    return "n/a" if x is None else f"{100 * x:.1f}%"


def write_report(name: str, s: dict, cost_per_1k: float, runs: int, errors: list[dict]) -> Path:
    lines = [
        f"# Evaluation: {name}",
        "",
        f"{date.today()} · model `{extractor.MODEL}` · {s['reports']} reports × {runs} runs = {s['runs']} runs",
        "",
        "## Headline",
        "",
        "| Metric | Result |",
        "|---|---|",
        f"| **Safety recall** | **{pct(s['safety_recall'])}** ({s['safety_caught']}/{s['safety_total']} safety runs caught) |",
        f"| False safety alarms | {s['false_alarms']} runs |",
        f"| Route accuracy | {pct(s['route_accuracy'])} |",
        f"| Same route on every run | {pct(s['consistent_route'])} of reports |",
        f"| Same facts on every run | {pct(s['consistent_facts'])} of reports |",
        f"| Failed extractions | {s['errors']} runs |",
        f"| Latency | {s['latency_mean']:.1f}s average, {s['latency_p95']:.1f}s p95 |",
        f"| Cost per 1,000 reports | ${cost_per_1k:.2f} |",
        "",
        "## Accuracy per field",
        "",
        "| Field | Accuracy |",
        "|---|---|",
        *[f"| `{f}` | {pct(s['field_accuracy'][f])} |" for f in FIELDS],
        "",
        f"## Wrong answers ({len(errors)})",
        "",
        "Every run with a wrong route or at least one wrong field. Full details in "
        f"`{name}_errors.jsonl`.",
        "",
        "| Report | Run | Route (expected → got) | Wrong fields |",
        "|---|---|---|---|",
    ]
    for e in errors:
        route = e["expected_route"] if e["route"] == e["expected_route"] else f"**{e['expected_route']} → {e['route']}**"
        if e["got"] is None:
            detail = e["error"]
        else:
            detail = "; ".join(
                f"`{f}`: {e['expected'][f]!r} → {e['got'][f]!r}" for f in wrong_fields(e["expected"], e["got"])
            )
        lines.append(f"| {e['id']} | {e['run']} | {route} | {detail} |")
    path = RESULTS / f"{name}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--name", default="baseline")
    args = parser.parse_args()

    rows = [json.loads(line) for line in REPORTS.read_text(encoding="utf-8").splitlines() if line.strip()]
    client = extractor._default_client()
    jobs = [(row, run) for run in range(1, args.runs + 1) for row in rows]

    print(f"Running {len(rows)} reports × {args.runs} runs with {extractor.MODEL}...")
    results, total = [], Usage()
    with ThreadPoolExecutor(args.workers) as pool:
        for i, (result, usage) in enumerate(pool.map(lambda j: run_one(*j, client), jobs), 1):
            results.append(result)
            total.input_tokens += usage.input_tokens
            total.output_tokens += usage.output_tokens
            print(f"\r{i}/{len(jobs)}", end="", flush=True)
    print()

    results.sort(key=lambda r: (r["id"], r["run"]))
    summary = summarize(results)
    cost = (total.input_tokens * PRICE_IN + total.output_tokens * PRICE_OUT) / 1_000_000
    cost_per_1k = cost / len(results) * 1000

    errors = [
        r for r in results
        if r["got"] is None or r["route"] != r["expected_route"] or wrong_fields(r["expected"], r["got"])
    ]
    RESULTS.mkdir(parents=True, exist_ok=True)
    with (RESULTS / f"{args.name}_errors.jsonl").open("w", encoding="utf-8") as f:
        for e in errors:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    path = write_report(args.name, summary, cost_per_1k, args.runs, errors)

    print(f"Safety recall {pct(summary['safety_recall'])} · route accuracy {pct(summary['route_accuracy'])} "
          f"· this run cost ${cost:.4f}")
    print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
