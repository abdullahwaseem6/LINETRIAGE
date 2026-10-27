from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class FaultType(str, Enum):
    MECHANICAL = "mechanical"
    ELECTRICAL = "electrical"
    SENSOR = "sensor"
    QUALITY = "quality"
    SAFETY = "safety"
    OTHER = "other"


class Language(str, Enum):
    EN = "en"
    HU = "hu"
    DE = "de"
    MIXED = "mixed"


class FaultReport(BaseModel):
    """Facts extracted from one operator report. Facts only, no decisions."""

    model_config = ConfigDict(extra="forbid")

    station_id: str | None
    fault_type: FaultType
    downtime_minutes: int | None = Field(ge=0, le=1440)
    recurring: bool
    safety_involved: bool
    affected_part: str | None = None
    language: Language
    summary: str = Field(min_length=1, max_length=200)