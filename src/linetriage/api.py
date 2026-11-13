"""Web API: POST a report, get back the extracted facts and the route.

Run it with: uvicorn linetriage.api:app --reload
Then open http://localhost:8000/docs to try it.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from linetriage.extractor import ExtractionError, extract
from linetriage.rules import Route, route_report
from linetriage.schema import FaultReport

app = FastAPI(title="LineTriage", description="Factory fault report triage.")


class TriageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class TriageResponse(BaseModel):
    facts: FaultReport
    route: Route
    reason: str


@app.post("/triage", response_model=TriageResponse)
def triage(request: TriageRequest) -> TriageResponse:
    try:
        facts = extract(request.text)
    except ExtractionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    decision = route_report(facts)
    return TriageResponse(facts=facts, route=decision.route, reason=decision.reason)
