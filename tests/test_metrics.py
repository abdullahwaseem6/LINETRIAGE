import pytest

from linetriage.metrics import summarize, wrong_fields

EXPECTED = {
    "station_id": "ST-02",
    "fault_type": "safety",
    "downtime_minutes": 0,
    "recurring": False,
    "safety_involved": True,
    "affected_part": None,
    "language": "en",
}


def result(id_, run, expected_route, route, got=EXPECTED, latency=1.0):
    return {
        "id": id_,
        "run": run,
        "expected": EXPECTED,
        "expected_route": expected_route,
        "got": got,
        "route": route,
        "error": None if got is not None else "failed",
        "latency": latency,
    }


def test_wrong_fields_lists_mismatches():
    got = {**EXPECTED, "downtime_minutes": 60, "language": "mixed"}
    assert wrong_fields(EXPECTED, got) == ["downtime_minutes", "language"]


def test_perfect_results():
    s = summarize([result("R1", 1, "safety_alert", "safety_alert")])
    assert s["route_accuracy"] == 1.0
    assert s["safety_recall"] == 1.0
    assert s["false_alarms"] == 0
    assert all(v == 1.0 for v in s["field_accuracy"].values())


def test_missed_safety_lowers_recall():
    s = summarize([
        result("R1", 1, "safety_alert", "safety_alert"),
        result("R2", 1, "safety_alert", "auto_ticket"),
    ])
    assert s["safety_recall"] == 0.5
    assert (s["safety_caught"], s["safety_total"]) == (1, 2)


def test_false_alarm_counted():
    s = summarize([result("R1", 1, "auto_ticket", "safety_alert")])
    assert s["false_alarms"] == 1
    assert s["safety_recall"] is None


def test_inconsistent_runs_detected():
    s = summarize([
        result("R1", 1, "auto_ticket", "auto_ticket"),
        result("R1", 2, "auto_ticket", "escalate_quality"),
        result("R2", 1, "auto_ticket", "auto_ticket"),
        result("R2", 2, "auto_ticket", "auto_ticket"),
    ])
    assert s["consistent_route"] == 0.5


def test_failed_extraction_counts_as_wrong_route_but_not_field():
    s = summarize([
        result("R1", 1, "auto_ticket", None, got=None),
        result("R2", 1, "auto_ticket", "auto_ticket"),
    ])
    assert s["errors"] == 1
    assert s["route_accuracy"] == 0.5
    assert s["field_accuracy"]["station_id"] == 1.0


def test_latency():
    s = summarize([result("R1", r, "auto_ticket", "auto_ticket", latency=r) for r in (1, 2, 3)])
    assert s["latency_mean"] == pytest.approx(2.0)
    assert s["latency_p95"] == 3
