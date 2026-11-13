"""Scoring for the evaluation: compare the system's answers with the labels.

Each result is one run of one report:
    {"id", "run", "expected", "expected_route", "got", "route", "error", "latency"}
where "got" is the extracted facts as a dict (None if extraction failed).
"""

import statistics

FIELDS = [
    "station_id",
    "fault_type",
    "downtime_minutes",
    "recurring",
    "safety_involved",
    "affected_part",
    "language",
]

SAFETY = "safety_alert"


def wrong_fields(expected: dict, got: dict) -> list[str]:
    return [f for f in FIELDS if got.get(f) != expected[f]]


def _share(hits: int, total: int) -> float | None:
    return hits / total if total else None


def summarize(results: list[dict]) -> dict:
    ok = [r for r in results if r["got"] is not None]

    field_accuracy = {
        f: _share(sum(r["got"][f] == r["expected"][f] for r in ok), len(ok)) for f in FIELDS
    }

    route_hits = sum(r["route"] == r["expected_route"] for r in results)

    # Safety recall: of the runs that SHOULD be a safety alert, how many were?
    should_alert = [r for r in results if r["expected_route"] == SAFETY]
    caught = sum(r["route"] == SAFETY for r in should_alert)
    # False alarms: safety alerts on reports that aren't safety issues.
    false_alarms = sum(
        r["route"] == SAFETY for r in results if r["expected_route"] != SAFETY
    )

    # Consistency: did every run of the same report give the same answer?
    by_report: dict[str, list[dict]] = {}
    for r in results:
        by_report.setdefault(r["id"], []).append(r)
    same_route = sum(len({r["route"] for r in runs}) == 1 for runs in by_report.values())
    same_facts = sum(
        len({tuple((r["got"] or {}).get(f) for f in FIELDS) for r in runs}) == 1
        for runs in by_report.values()
    )

    latencies = sorted(r["latency"] for r in results)
    p95 = latencies[min(len(latencies) - 1, int(0.95 * len(latencies)))] if latencies else None

    return {
        "runs": len(results),
        "reports": len(by_report),
        "errors": len(results) - len(ok),
        "field_accuracy": field_accuracy,
        "route_accuracy": _share(route_hits, len(results)),
        "safety_recall": _share(caught, len(should_alert)),
        "safety_caught": caught,
        "safety_total": len(should_alert),
        "false_alarms": false_alarms,
        "consistent_route": _share(same_route, len(by_report)),
        "consistent_facts": _share(same_facts, len(by_report)),
        "latency_mean": statistics.mean(latencies) if latencies else None,
        "latency_p95": p95,
    }
