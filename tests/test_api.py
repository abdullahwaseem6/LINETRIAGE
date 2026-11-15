"""API tests. extract() is replaced with a fake, so no real LLM call is made."""

import pytest
from fastapi.testclient import TestClient

from linetriage import api
from linetriage.extractor import ExtractionError
from linetriage.access import SAMPLES, Access
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


@pytest.fixture(autouse=True)
def fresh_limits(monkeypatch):
    api.limiter.reset()
    api.sample_cache.clear()
    monkeypatch.setattr(api, "access", Access())  # open by default, like local use


@pytest.fixture
def locked(monkeypatch):
    monkeypatch.setattr(api, "access", Access(owner_code="owner-secret", member_codes=["guest-pass"]))


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


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_per_visitor_limit(fake_extract, monkeypatch):
    monkeypatch.setattr(api.limiter, "per_minute", 2)
    codes = [client.post("/triage", json={"text": "x"}).status_code for _ in range(3)]
    assert codes == [200, 200, 429]
    assert len(fake_extract) == 2  # the blocked request never reached the LLM


def test_visitors_are_counted_separately(fake_extract, monkeypatch):
    monkeypatch.setattr(api.limiter, "per_minute", 1)
    a = client.post("/triage", json={"text": "x"}, headers={"x-forwarded-for": "1.1.1.1"})
    b = client.post("/triage", json={"text": "x"}, headers={"x-forwarded-for": "2.2.2.2"})
    assert (a.status_code, b.status_code) == (200, 200)


def test_daily_limit(fake_extract, monkeypatch):
    monkeypatch.setattr(api.limiter, "per_day", 1)
    client.post("/triage", json={"text": "x"}, headers={"x-forwarded-for": "1.1.1.1"})
    blocked = client.post("/triage", json={"text": "x"}, headers={"x-forwarded-for": "2.2.2.2"})
    assert blocked.status_code == 429
    assert "today" in blocked.json()["detail"]


def test_llm_outage_returns_clean_503(monkeypatch):
    def broken(text):
        raise TypeError("Could not resolve authentication method")

    monkeypatch.setattr(api, "extract", broken)
    response = client.post("/triage", json={"text": "st5 broke"})
    assert response.status_code == 503
    assert "unavailable" in response.json()["detail"]


def test_console_page_and_assets_are_served():
    page = client.get("/console")
    assert page.status_code == 200 and "Console" in page.text
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/static/style.css").status_code == 200


def test_samples_endpoint():
    assert client.get("/samples").json() == SAMPLES


def test_open_mode_allows_any_note(fake_extract):
    assert client.post("/access", json={"code": ""}).json() == {"role": "open"}
    assert client.post("/triage", json={"text": "my own note"}).status_code == 200


def test_locked_guest_can_run_samples_only(fake_extract, locked):
    sample = SAMPLES[0]["text"]
    assert client.post("/triage", json={"text": sample}).status_code == 200
    blocked = client.post("/triage", json={"text": "my own note"})
    assert blocked.status_code == 401
    assert fake_extract == [sample]  # the blocked note never reached the LLM


def test_access_codes_and_roles(fake_extract, locked):
    assert client.post("/access", json={"code": "nope"}).json() == {"role": "guest"}
    assert client.post("/access", json={"code": "guest-pass"}).json() == {"role": "member"}
    assert client.post("/access", json={"code": "owner-secret"}).json() == {"role": "owner"}
    ok = client.post("/triage", json={"text": "my own note"}, headers={"x-access-code": "guest-pass"})
    assert ok.status_code == 200


def test_owner_skips_rate_limits(fake_extract, locked, monkeypatch):
    monkeypatch.setattr(api.limiter, "per_minute", 1)
    headers = {"x-access-code": "owner-secret"}
    codes = [client.post("/triage", json={"text": "note"}, headers=headers).status_code for _ in range(3)]
    assert codes == [200, 200, 200]


def test_members_are_rate_limited(fake_extract, locked, monkeypatch):
    monkeypatch.setattr(api.limiter, "per_minute", 1)
    headers = {"x-access-code": "guest-pass"}
    codes = [client.post("/triage", json={"text": "note"}, headers=headers).status_code for _ in range(2)]
    assert codes == [200, 429]


def test_sample_results_are_cached(fake_extract):
    sample = SAMPLES[3]["text"]
    first = client.post("/triage", json={"text": sample}).json()
    second = client.post("/triage", json={"text": sample}).json()
    assert first == second
    assert fake_extract == [sample]  # the LLM was called once
