import pytest
from pydantic import ValidationError

from linetriage.rules import LONG_DOWNTIME_MINUTES, Decision, Route, route_report
from linetriage.schema import FaultReport

# Station importance from registry.py: ST-01 HIGH, ST-05 MEDIUM, ST-08 LOW.


def make_report(**overrides):
    data = {
        "station_id": "ST-05",
        "fault_type": "mechanical",
        "downtime_minutes": 10,
        "recurring": False,
        "safety_involved": False,
        "affected_part": None,
        "language": "en",
        "summary": "Conveyor belt slipping.",
    }
    data.update(overrides)
    return FaultReport.model_validate(data)


# Rule 1: safety

def test_safety_involved_is_safety_alert():
    decision = route_report(make_report(safety_involved=True))
    assert decision.route is Route.SAFETY_ALERT
    assert "ST-05" in decision.reason


def test_safety_fault_type_is_safety_alert():
    assert route_report(make_report(fault_type="safety")).route is Route.SAFETY_ALERT


def test_safety_wins_when_every_other_rule_also_matches():
    report = make_report(
        station_id="nonexistent",
        fault_type="safety",
        safety_involved=True,
        recurring=True,
        downtime_minutes=600,
        affected_part="bracket",
    )
    assert route_report(report).route is Route.SAFETY_ALERT


def test_safety_with_zero_downtime_is_still_safety_alert():
    report = make_report(safety_involved=True, downtime_minutes=0)
    assert route_report(report).route is Route.SAFETY_ALERT


def test_safety_with_no_station_is_still_safety_alert():
    decision = route_report(make_report(safety_involved=True, station_id=None))
    assert decision.route is Route.SAFETY_ALERT
    assert decision.reason == "Safety issue reported."


# Rule 2: unknown station

@pytest.mark.parametrize("station_id", ["ST-99", "garbage"])
def test_unknown_station_goes_to_human_review(station_id):
    decision = route_report(make_report(station_id=station_id))
    assert decision.route is Route.HUMAN_REVIEW
    assert station_id in decision.reason


def test_missing_station_goes_to_human_review():
    decision = route_report(make_report(station_id=None))
    assert decision.route is Route.HUMAN_REVIEW
    assert decision.reason == "No station given in the report."


def test_messy_station_id_is_still_found():
    assert route_report(make_report(station_id="station 5")).route is Route.AUTO_TICKET


# Rule 3: recurring

def test_recurring_fault_escalates():
    decision = route_report(make_report(recurring=True))
    assert decision.route is Route.ESCALATE_QUALITY
    assert decision.reason == "Recurring fault at ST-05."


# Rule 4: long downtime on HIGH station

def test_long_downtime_threshold_is_30():
    assert LONG_DOWNTIME_MINUTES == 30


def test_29_minutes_on_high_station_is_auto_ticket():
    report = make_report(station_id="ST-01", downtime_minutes=29)
    assert route_report(report).route is Route.AUTO_TICKET


def test_30_minutes_on_high_station_escalates():
    decision = route_report(make_report(station_id="ST-01", downtime_minutes=30))
    assert decision.route is Route.ESCALATE_QUALITY
    assert "ST-01" in decision.reason
    assert "30 min" in decision.reason


def test_long_stop_on_low_station_is_auto_ticket():
    report = make_report(station_id="ST-08", downtime_minutes=600)
    assert route_report(report).route is Route.AUTO_TICKET


def test_long_stop_on_medium_station_is_auto_ticket():
    report = make_report(station_id="ST-05", downtime_minutes=600)
    assert route_report(report).route is Route.AUTO_TICKET


def test_unknown_downtime_does_not_crash():
    decision = route_report(make_report(station_id="ST-01", downtime_minutes=None))
    assert decision.route is Route.AUTO_TICKET


# Rule 5: quality fault with a part

def test_quality_fault_with_part_escalates():
    decision = route_report(make_report(fault_type="quality", affected_part="bracket"))
    assert decision.route is Route.ESCALATE_QUALITY
    assert "bracket" in decision.reason


@pytest.mark.parametrize("part", [None, "", "   "])
def test_quality_fault_without_part_is_auto_ticket(part):
    report = make_report(fault_type="quality", affected_part=part)
    assert route_report(report).route is Route.AUTO_TICKET


def test_part_without_quality_fault_is_auto_ticket():
    report = make_report(fault_type="mechanical", affected_part="bracket")
    assert route_report(report).route is Route.AUTO_TICKET


# Rule 6: default

def test_routine_fault_is_auto_ticket():
    decision = route_report(make_report())
    assert decision.route is Route.AUTO_TICKET
    assert "ST-05" in decision.reason


# Decision itself

def test_every_route_has_a_reason():
    reports = [
        make_report(safety_involved=True),
        make_report(station_id=None),
        make_report(recurring=True),
        make_report(station_id="ST-01", downtime_minutes=45),
        make_report(fault_type="quality", affected_part="bracket"),
        make_report(),
    ]
    routes = set()
    for report in reports:
        decision = route_report(report)
        assert decision.reason.strip()
        routes.add(decision.route)
    assert routes == set(Route)


def test_decision_is_frozen():
    decision = route_report(make_report())
    with pytest.raises(ValidationError):
        decision.route = Route.SAFETY_ALERT


def test_decision_type():
    assert isinstance(route_report(make_report()), Decision)
