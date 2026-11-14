"""API tests. extract() is replaced with a fake, so no real LLM call is made."""

import pytest
from fastapi.testclient import TestClient

from linetriage import api
from linetriage.extractor import ExtractionError
from linetriage.schema import FaultReport

client = TestClient(api.app)

SAFETY_FACTS = FaultReport(
    station_id="ST-02",
    fault_type="safety",
    downtime_minutes=0,
    recurring=False,
    safety_involved=True,
    language="en",
    summary="Guard removed on robot cell.",
)


@pytest.fixture
def fake_extract(monkeypatch):
    calls = []

    def fake(text):
        calls.append(text)
        return SAFETY_FACTS

    monkeypatch.setattr(api, "extract", fake)
    monkeypatch.setattr(api, "second_opinion", lambda text: None)
    return calls


def test_triage_returns_facts_route_and_reason(fake_extract):
    response = client.post("/triage", json={"text": "guard off on st2 lol"})
    assert response.status_code == 200
    body = response.json()
    assert body["facts"]["station_id"] == "ST-02"
    assert body["route"] == "safety_alert"
    assert body["reason"] == "Safety issue reported at ST-02."
    assert fake_extract == ["guard off on st2 lol"]


@pytest.mark.parametrize("payload", [{}, {"text": ""}, {"text": "x" * 2001}, {"txt": "hi"}])
def test_bad_request_is_rejected_before_calling_llm(fake_extract, payload):
    response = client.post("/triage", json=payload)
    assert response.status_code == 422
    assert fake_extract == []


def test_extraction_failure_returns_502(monkeypatch):
    def failing(text):
        raise ExtractionError("Invalid output after retry")

    monkeypatch.setattr(api, "extract", failing)
    response = client.post("/triage", json={"text": "st5 broke"})
    assert response.status_code == 502
    assert "Invalid output" in response.json()["detail"]


def test_home_page_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "LineTriage" in response.text


def test_second_opinion_is_included(fake_extract, monkeypatch):
    from linetriage.second_opinion import SecondOpinion

    opinion = SecondOpinion(danger_score=0.83, threshold=0.18, dangerous=True, milliseconds=0.9)
    monkeypatch.setattr(api, "second_opinion", lambda text: opinion)
    body = client.post("/triage", json={"text": "guard off"}).json()
    assert body["second_opinion"]["dangerous"] is True
    assert body["route"] == "safety_alert"  # the second opinion never changes the route


def test_works_without_trained_model(fake_extract):
    body = client.post("/triage", json={"text": "guard off"}).json()
    assert body["second_opinion"] is None
