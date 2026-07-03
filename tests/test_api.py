"""Tests for the FastAPI web API (M3).

All tests use no_llm=True so they don't require an API key and run fast.
"""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# GET /api/frameworks
# ---------------------------------------------------------------------------

def test_get_frameworks_returns_list():
    r = client.get("/api/frameworks")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 4


def test_get_frameworks_contains_expected_ids():
    r = client.get("/api/frameworks")
    ids = [fw["id"] for fw in r.json()]
    assert "openai-5-levels" in ids
    assert "openai-preparedness" in ids
    assert "anthropic-rsp" in ids
    assert "deepmind-fsf" in ids


def test_get_frameworks_shape():
    r = client.get("/api/frameworks")
    fw = r.json()[0]
    assert "id" in fw
    assert "name" in fw
    assert "criteria_count" in fw
    assert fw["criteria_count"] > 0


# ---------------------------------------------------------------------------
# GET /api/corpus
# ---------------------------------------------------------------------------

def test_get_corpus_returns_list():
    r = client.get("/api/corpus")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 6


def test_get_corpus_contains_major_labs():
    r = client.get("/api/corpus")
    data = r.json()
    for slug in ("openai", "anthropic", "google", "microsoft", "meta", "xai"):
        assert slug in data, f"Expected '{slug}' in corpus, got: {data}"


# ---------------------------------------------------------------------------
# POST /api/audit
# ---------------------------------------------------------------------------

def test_audit_single_company_deterministic():
    r = client.post("/api/audit", json={
        "company": "openai",
        "framework": "openai-5-levels",
        "no_llm": True,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["company"] == "OpenAI"
    assert data["framework_id"] == "openai-5-levels"
    assert 0 <= data["score"] <= 100
    assert data["claims_count"] > 0
    assert data["llm_enabled"] is False
    assert len(data["results"]) == 5


def test_audit_result_shape():
    r = client.post("/api/audit", json={
        "company": "anthropic",
        "framework": "anthropic-rsp",
        "no_llm": True,
    })
    assert r.status_code == 200
    result = r.json()["results"][0]
    for key in ("criterion_id", "criterion_name", "bar", "rating", "evidence", "gap", "confidence", "method"):
        assert key in result, f"Missing key '{key}' in result"
    assert result["rating"] in ("none", "partial", "substantial", "strong")
    assert 0.0 <= result["confidence"] <= 1.0


def test_audit_all_bundled_companies():
    for slug in ("openai", "anthropic", "google", "microsoft", "meta", "xai"):
        r = client.post("/api/audit", json={
            "company": slug,
            "framework": "openai-5-levels",
            "no_llm": True,
        })
        assert r.status_code == 200, f"Failed for {slug}: {r.text}"


def test_audit_all_frameworks():
    for framework in ("openai-5-levels", "openai-preparedness", "anthropic-rsp", "deepmind-fsf"):
        r = client.post("/api/audit", json={
            "company": "openai",
            "framework": framework,
            "no_llm": True,
        })
        assert r.status_code == 200, f"Failed for {framework}: {r.text}"


def test_audit_invalid_company_404():
    r = client.post("/api/audit", json={
        "company": "nonexistent-company-xyz",
        "framework": "openai-5-levels",
        "no_llm": True,
    })
    assert r.status_code == 404


def test_audit_invalid_framework_400():
    r = client.post("/api/audit", json={
        "company": "openai",
        "framework": "nonexistent-framework",
        "no_llm": True,
    })
    assert r.status_code == 400


# ---------------------------------------------------------------------------
# POST /api/compare
# ---------------------------------------------------------------------------

def test_compare_two_companies():
    r = client.post("/api/compare", json={
        "companies": ["openai", "anthropic"],
        "framework": "openai-5-levels",
        "no_llm": True,
    })
    assert r.status_code == 200
    data = r.json()
    assert len(data["companies"]) == 2
    assert len(data["scores"]) == 2
    assert len(data["criteria"]) == 5


def test_compare_all_labs():
    r = client.post("/api/compare", json={
        "companies": ["openai", "anthropic", "google", "microsoft", "meta", "xai"],
        "framework": "openai-preparedness",
        "no_llm": True,
    })
    assert r.status_code == 200
    data = r.json()
    assert len(data["companies"]) == 6
    assert len(data["scores"]) == 6


def test_compare_result_shape():
    r = client.post("/api/compare", json={
        "companies": ["openai", "anthropic"],
        "framework": "openai-5-levels",
        "no_llm": True,
    })
    data = r.json()
    assert "framework_id" in data
    assert "framework_name" in data
    assert "companies" in data
    assert "scores" in data
    assert "criteria" in data
    crit = data["criteria"][0]
    assert "criterion_id" in crit
    assert "criterion_name" in crit
    assert "bar" in crit
    assert "ratings" in crit
    assert isinstance(crit["ratings"], dict)


def test_compare_too_few_companies_400():
    r = client.post("/api/compare", json={
        "companies": ["openai"],
        "framework": "openai-5-levels",
        "no_llm": True,
    })
    assert r.status_code == 400


def test_compare_invalid_company_404():
    r = client.post("/api/compare", json={
        "companies": ["openai", "no-such-company"],
        "framework": "openai-5-levels",
        "no_llm": True,
    })
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

def test_root_returns_html():
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert b"AGI Readiness" in r.content
