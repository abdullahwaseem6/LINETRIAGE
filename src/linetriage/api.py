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
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from linetriage.access import SAMPLE_TEXTS, SAMPLES, access
from linetriage.extractor import ExtractionError, extract
from linetriage.limits import limiter
from linetriage.rules import Route, route_report
from linetriage.schema import FaultReport
from linetriage.second_opinion import SecondOpinion, second_opinion

app = FastAPI(title="LineTriage", description="Factory fault report triage.")

STATIC = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC), name="static")

# Sample results are kept after the first run, so repeat clicks cost nothing.
sample_cache: dict[str, "TriageResponse"] = {}


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/console", include_in_schema=False)
def console() -> FileResponse:
    return FileResponse(STATIC / "console.html")


@app.get("/samples")
def samples() -> list[dict]:
    return SAMPLES


class AccessRequest(BaseModel):
    code: str = Field(default="", max_length=200)


@app.post("/access")
def check_access(request: AccessRequest) -> dict:
    return {"role": access.role(request.code)}


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
    role = access.role(http.headers.get("x-access-code", ""))
    is_sample = request.text in SAMPLE_TEXTS
    if role == "guest" and not is_sample:
        raise HTTPException(status_code=401, detail="Your own notes need an access code. The free samples work without one.")
    if is_sample and request.text in sample_cache:
        return sample_cache[request.text]
    if role != "owner":
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
    result = TriageResponse(
        facts=facts,
        route=decision.route,
        reason=decision.reason,
        second_opinion=second_opinion(request.text),
    )
    if is_sample:
        sample_cache[request.text] = result
    return result
