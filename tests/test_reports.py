import json
from collections import Counter
from pathlib import Path

import pytest

from linetriage.registry import Importance, get_station
from linetriage.rules import LONG_DOWNTIME_MINUTES, Route, route_report
from linetriage.schema import FaultReport

REPORTS_PATH = Path(__file__).parent.parent / "data" / "reports.jsonl"


def load_reports():
    with REPORTS_PATH.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


REPORTS = load_reports()


def to_fault_report(row):
    # The dataset leaves out summary, so add a placeholder to build a full FaultReport.
    return FaultReport.model_validate({**row["expected"], "summary": "placeholder"})


@pytest.mark.parametrize("row", REPORTS, ids=lambda row: row["id"])
def test_expected_is_valid_fault_report(row):
    assert "summary" not in row["expected"]
    to_fault_report(row)


@pytest.mark.parametrize("row", REPORTS, ids=lambda row: row["id"])
def test_route_matches_expected(row):
    decision = route_report(to_fault_report(row))
    assert decision.route is Route(row["expected_route"]), decision.reason


def test_ids_are_r01_to_r20():
    assert [row["id"] for row in REPORTS] == [f"R{n:02d}" for n in range(1, 21)]


def test_every_row_has_only_known_keys():
    for row in REPORTS:
        assert set(row) == {"id", "text", "expected", "expected_route"}
        assert row["text"].strip()


def test_every_route_appears_at_least_three_times():
    counts = Counter(row["expected_route"] for row in REPORTS)
    for route in Route:
        assert counts[route.value] >= 3, f"{route.value}: {counts[route.value]}"


def test_has_exactly_30_minutes_on_high_station():
    assert any(
        row["expected"]["downtime_minutes"] == LONG_DOWNTIME_MINUTES
        and (station := get_station(row["expected"]["station_id"])) is not None
        and station.importance is Importance.HIGH
        for row in REPORTS
    )


def test_has_long_stop_on_low_station():
    assert any(
        (row["expected"]["downtime_minutes"] or 0) >= LONG_DOWNTIME_MINUTES
        and (station := get_station(row["expected"]["station_id"])) is not None
        and station.importance is Importance.LOW
        for row in REPORTS
    )
