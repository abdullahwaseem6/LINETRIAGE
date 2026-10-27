import re
from enum import Enum

from pydantic import BaseModel, ConfigDict


class Importance(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Station(BaseModel):
    model_config = ConfigDict(frozen=True)

    station_id: str
    name: str
    importance: Importance


STATIONS: dict[str, Station] = {
    s.station_id: s
    for s in [
        Station(station_id="ST-01", name="Press Line", importance=Importance.HIGH),
        Station(station_id="ST-02", name="Welding Cell", importance=Importance.HIGH),
        Station(station_id="ST-03", name="Paint Booth", importance=Importance.MEDIUM),
        Station(station_id="ST-04", name="CNC Machining", importance=Importance.HIGH),
        Station(station_id="ST-05", name="Assembly Line A", importance=Importance.MEDIUM),
        Station(station_id="ST-06", name="Assembly Line B", importance=Importance.MEDIUM),
        Station(station_id="ST-07", name="Quality Inspection", importance=Importance.HIGH),
        Station(station_id="ST-08", name="Packaging", importance=Importance.LOW),
        Station(station_id="ST-09", name="Warehouse Conveyor", importance=Importance.LOW),
        Station(station_id="ST-10", name="Tool Crib", importance=Importance.LOW),
    ]
}

# Optional "st" / "station" prefix, optional separators, then the number.
_ID_PATTERN = re.compile(r"^(?:st(?:ation)?)?[\s\-_#]*(\d+)$", re.IGNORECASE)


def normalize_station_id(raw: str | None) -> str | None:
    """Turn messy IDs like "st6", "Station 6" or "6" into "ST-06".

    Returns None if the text doesn't look like a station ID at all.
    Does not check that the station exists; use get_station for that.
    """
    if raw is None:
        return None
    match = _ID_PATTERN.match(raw.strip())
    if match is None:
        return None
    return f"ST-{int(match.group(1)):02d}"


def get_station(raw: str | None) -> Station | None:
    """Look up a station by any spelling of its ID. None if it doesn't exist."""
    station_id = normalize_station_id(raw)
    if station_id is None:
        return None
    return STATIONS.get(station_id)
