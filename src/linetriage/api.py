"""Web API: POST a report, get back the extracted facts, the route, and the
small model's second opinion on safety.

Run it with: uvicorn linetriage.api:app --reload
Then open http://localhost:8000/docs to try it.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from linetriage.extractor import ExtractionError, extract
from linetriage.rules import Route, route_report
from linetriage.schema import FaultReport
from linetriage.second_opinion import SecondOpinion, second_opinion

app = FastAPI(title="LineTriage", description="Factory fault report triage.")

INDEX_HTML = Path(__file__).parent / "static" / "index.html"


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(INDEX_HTML)


class TriageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class TriageResponse(BaseModel):
    facts: FaultReport
    route: Route
    reason: str
    second_opinion: SecondOpinion | None = None


@app.post("/triage", response_model=TriageResponse)
def triage(request: TriageRequest) -> TriageResponse:
    try:
        facts = extract(request.text)
    except ExtractionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    decision = route_report(facts)
    return TriageResponse(
        facts=facts,
        route=decision.route,
        reason=decision.reason,
        second_opinion=second_opinion(request.text),
    )
