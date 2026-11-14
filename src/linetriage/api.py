"""Web API: POST a report, get back the extracted facts, the route, and the
small model's second opinion on safety.

Run it with: uvicorn linetriage.api:app --reload
Then open http://localhost:8000/docs to try it.
"""

import logging
from pathlib import Path

import anthropic
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from linetriage.extractor import ExtractionError, extract
from linetriage.limits import limiter
from linetriage.rules import Route, route_report
from linetriage.schema import FaultReport
from linetriage.second_opinion import SecondOpinion, second_opinion

app = FastAPI(title="LineTriage", description="Factory fault report triage.")

INDEX_HTML = Path(__file__).parent / "static" / "index.html"


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(INDEX_HTML)


@app.get("/health", include_in_schema=False)
def health() -> dict:
    return {"status": "ok"}


class TriageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class TriageResponse(BaseModel):
    facts: FaultReport
    route: Route
    reason: str
    second_opinion: SecondOpinion | None = None


@app.post("/triage", response_model=TriageResponse)
def triage(request: TriageRequest, http: Request) -> TriageResponse:
    # Behind a hosting proxy the visitor's address is the first X-Forwarded-For entry.
    forwarded = http.headers.get("x-forwarded-for", "")
    visitor = forwarded.split(",")[0].strip() or (http.client.host if http.client else "unknown")
    too_many = limiter.check(visitor)
    if too_many:
        raise HTTPException(status_code=429, detail=too_many)
    try:
        facts = extract(request.text)
    except ExtractionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except (anthropic.APIError, anthropic.AuthenticationError, TypeError) as e:
        # Missing or wrong API key, provider outage, out of credit: log it, show a clean message.
        logging.getLogger("linetriage").error("LLM call failed: %s", e)
        raise HTTPException(status_code=503, detail="The AI service is unavailable right now. Please try again later.")
    decision = route_report(facts)
    return TriageResponse(
        facts=facts,
        route=decision.route,
        reason=decision.reason,
        second_opinion=second_opinion(request.text),
    )
