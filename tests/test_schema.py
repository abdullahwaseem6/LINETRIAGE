import pytest
from pydantic import ValidationError

from linetriage.schema import FaultReport, FaultType, Language


def valid_report(**overrides):
    data = {
        "station_id": "ST-07",
        "fault_type": "sensor",
        "downtime_minutes": 25,
        "recurring": True,
        "safety_involved": False,
        "language": "hu",
        "summary": "Proximity sensor intermittently fails on station 7.",
    }
    data.update(overrides)
    return data


def test_valid_report_parses():
    report = FaultReport.model_validate(valid_report())
    assert report.fault_type is FaultType.SENSOR
    assert report.language is Language.HU
    assert report.affected_part is None


def test_nullable_fields_accept_none():
    report = FaultReport.model_validate(
        valid_report(station_id=None, downtime_minutes=None)
    )
    assert report.station_id is None
    assert report.downtime_minutes is None


@pytest.mark.parametrize("field", ["station_id", "downtime_minutes"])
def test_nullable_fields_must_still_be_present(field):
    data = valid_report()
    del data[field]
    with pytest.raises(ValidationError):
        FaultReport.model_validate(data)


def test_affected_part_is_optional():
    data = valid_report()
    assert "affected_part" not in data
    assert FaultReport.model_validate(data).affected_part is None


def test_unknown_fault_type_rejected():
    with pytest.raises(ValidationError):
        FaultReport.model_validate(valid_report(fault_type="hydraulic"))


def test_unknown_language_rejected():
    with pytest.raises(ValidationError):
        FaultReport.model_validate(valid_report(language="fr"))


@pytest.mark.parametrize("minutes", [0, 1440])
def test_downtime_bounds_inclusive(minutes):
    report = FaultReport.model_validate(valid_report(downtime_minutes=minutes))
    assert report.downtime_minutes == minutes


@pytest.mark.parametrize("minutes", [-5, 1441, 2000])
def test_downtime_out_of_range_rejected(minutes):
    with pytest.raises(ValidationError):
        FaultReport.model_validate(valid_report(downtime_minutes=minutes))


def test_extra_field_rejected():
    with pytest.raises(ValidationError):
        FaultReport.model_validate(valid_report(priority="high"))


@pytest.mark.parametrize("summary", ["", "x" * 201])
def test_summary_length_enforced(summary):
    with pytest.raises(ValidationError):
        FaultReport.model_validate(valid_report(summary=summary))


def test_parses_llm_json_string():
    text = FaultReport.model_validate(valid_report()).model_dump_json()
    report = FaultReport.model_validate_json(text)
    assert report.station_id == "ST-07"
