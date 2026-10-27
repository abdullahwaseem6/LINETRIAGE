import pytest
from pydantic import ValidationError

from linetriage.registry import (
    STATIONS,
    Importance,
    Station,
    get_station,
    normalize_station_id,
)


def test_registry_has_ten_stations():
    assert list(STATIONS) == [f"ST-{n:02d}" for n in range(1, 11)]


def test_every_station_has_name_and_importance():
    for station_id, station in STATIONS.items():
        assert station.station_id == station_id
        assert station.name
        assert isinstance(station.importance, Importance)


@pytest.mark.parametrize(
    "raw",
    ["st6", "ST6", "Station 6", "station6", "6", "06", "ST-06", "st-6",
     "ST_06", "st 6", "  st6  ", "Station #6"],
)
def test_normalize_messy_ids(raw):
    assert normalize_station_id(raw) == "ST-06"


def test_normalize_two_digit_id():
    assert normalize_station_id("station 10") == "ST-10"


@pytest.mark.parametrize("raw", [None, "", "   ", "abc", "st", "line 6", "6a", "st-6-2"])
def test_normalize_rejects_garbage(raw):
    assert normalize_station_id(raw) is None


def test_normalize_does_not_check_existence():
    assert normalize_station_id("st99") == "ST-99"


def test_get_station_finds_existing():
    station = get_station("Station 7")
    assert isinstance(station, Station)
    assert station.station_id == "ST-07"
    assert station.importance is Importance.HIGH


@pytest.mark.parametrize("raw", ["st99", "0", "ST-11", "garbage", None])
def test_get_station_returns_none_when_missing(raw):
    assert get_station(raw) is None


def test_stations_are_read_only():
    with pytest.raises(ValidationError):
        STATIONS["ST-01"].importance = Importance.LOW
