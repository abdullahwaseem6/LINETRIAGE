from enum import Enum

from pydantic import BaseModel, ConfigDict

from linetriage.registry import Importance, get_station
from linetriage.schema import FaultReport, FaultType

LONG_DOWNTIME_MINUTES = 30


class Route(str, Enum):
    SAFETY_ALERT = "safety_alert"
    HUMAN_REVIEW = "human_review"
    ESCALATE_QUALITY = "escalate_quality"
    AUTO_TICKET = "auto_ticket"


class Decision(BaseModel):
    model_config = ConfigDict(frozen=True)

    route: Route
    reason: str


def route_report(report: FaultReport) -> Decision:
    """Decide where a report goes. Rules run top to bottom; first match wins."""
    # Rule 1: safety always comes first. Never move or weaken this rule.
    if report.safety_involved or report.fault_type is FaultType.SAFETY:
        where = f" at {report.station_id}" if report.station_id else ""
        return Decision(route=Route.SAFETY_ALERT, reason=f"Safety issue reported{where}.")

    # Rule 2: we can't route reliably without a known station.
    station = get_station(report.station_id)
    if station is None:
        if report.station_id is None:
            reason = "No station given in the report."
        else:
            reason = f"Unknown station {report.station_id!r}."
        return Decision(route=Route.HUMAN_REVIEW, reason=reason)

    sid = station.station_id

    # Rule 3: a fault that keeps coming back.
    if report.recurring:
        return Decision(route=Route.ESCALATE_QUALITY, reason=f"Recurring fault at {sid}.")

    # Rule 4: a long stop on an important station. Unknown downtime skips this rule.
    if (
        station.importance is Importance.HIGH
        and report.downtime_minutes is not None
        and report.downtime_minutes >= LONG_DOWNTIME_MINUTES
    ):
        return Decision(
            route=Route.ESCALATE_QUALITY,
            reason=(
                f"{report.downtime_minutes} min downtime at HIGH-importance station {sid} "
                f"(limit {LONG_DOWNTIME_MINUTES} min)."
            ),
        )

    # Rule 5: a quality problem tied to a specific part.
    if report.fault_type is FaultType.QUALITY and report.affected_part and report.affected_part.strip():
        return Decision(
            route=Route.ESCALATE_QUALITY,
            reason=f"Quality fault on part {report.affected_part.strip()!r} at {sid}.",
        )

    # Rule 6: everything else.
    return Decision(
        route=Route.AUTO_TICKET,
        reason=f"Routine {report.fault_type.value} fault at {sid}; no escalation rule matched.",
    )
