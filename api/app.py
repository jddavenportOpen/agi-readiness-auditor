"""AGI Readiness Auditor — FastAPI web API.

Routes:
  GET  /api/frameworks    list available frameworks
  GET  /api/corpus        list bundled company corpora
  POST /api/audit         run a single-company audit → JSON
  POST /api/compare       run a multi-company comparison → JSON
  GET  /                  serve index.html (Railway / local dev)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure agi_auditor is importable when invoked from any working dir.
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from agi_auditor import analyzer, corpus, report
from agi_auditor.frameworks import list_frameworks, load_framework


# ---------------------------------------------------------------------------
# Env key loading (mirrors CLI __main__.py; no-ops in prod where envs are set)
# ---------------------------------------------------------------------------

def _load_env_file() -> None:
    _ENV_KEYS = frozenset({
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_API_KEY_SUB1",
        "KIMI_API_KEY",
        "KIMI_BASE_URL",
        "KIMI_MODEL",
        "AGI_AUDITOR_MODEL",
    })
    path = Path("~/agent-system/.env").expanduser()
    if not path.exists():
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                if k in _ENV_KEYS:
                    os.environ.setdefault(k, v.strip().strip('"').strip("'"))
    except OSError:
        pass


_load_env_file()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AGI Readiness Auditor",
    description=(
        "Pressure-test a lab's public AGI-safety story against a published "
        "readiness framework. Audits public claims only."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

_INDEX_HTML = _ROOT / "index.html"


@app.get("/", include_in_schema=False)
async def root() -> FileResponse:
    return FileResponse(str(_INDEX_HTML), media_type="text/html")


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class AuditRequest(BaseModel):
    company: str = Field(..., description="Company slug or name (e.g. 'openai', 'Anthropic')")
    framework: str = Field("openai-5-levels", description="Framework id")
    no_llm: bool = Field(
        False,
        description="Use deterministic keyword analysis instead of LLM (fast, no key needed)",
    )
    model: str = Field(
        "auto",
        description="LLM model override — 'auto', 'claude-sonnet-4-6', 'claude-haiku-4-5-20251001', …",
    )


class CompareRequest(BaseModel):
    companies: list[str] = Field(..., description="2+ company slugs/names to compare")
    framework: str = Field("openai-5-levels", description="Framework id")
    no_llm: bool = Field(False, description="Use deterministic analysis (fast)")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _enrich_results(fw: dict, raw_results: list[dict]) -> list[dict]:
    crit_map = {c["id"]: c for c in fw["criteria"]}
    out = []
    for r in raw_results:
        c = crit_map.get(r["criterion_id"], {})
        out.append({
            "criterion_id": r["criterion_id"],
            "criterion_name": c.get("name", r["criterion_id"]),
            "bar": c.get("bar", ""),
            "source_url": c.get("source", ""),
            "rating": r["rating"],
            "evidence": r["evidence"],
            "gap": r["gap"],
            "confidence": round(r["confidence"], 4),
            "method": r["method"],
        })
    return out


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/frameworks", summary="List available frameworks")
def get_frameworks() -> list[dict]:
    out = []
    for fid in list_frameworks():
        fw = load_framework(fid)
        out.append({
            "id": fid,
            "name": fw["name"],
            "criteria_count": len(fw["criteria"]),
            "sources": fw.get("sources", []),
        })
    return out


@app.get("/api/corpus", summary="List bundled company corpora")
def get_corpus() -> list[str]:
    return corpus.list_bundled()


@app.post("/api/audit", summary="Audit a company's public claims against a framework")
def audit(req: AuditRequest) -> dict:
    try:
        fw = load_framework(req.framework)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        claims = corpus.load_bundled(req.company)
        company_name = corpus.canonical_name(req.company)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    result = analyzer.assess(
        fw, company_name, claims,
        use_llm=not req.no_llm,
        model=req.model,
    )
    score = report.readiness_score(result)

    return {
        "company": result["company"],
        "framework_id": req.framework,
        "framework_name": fw["name"],
        "score": score,
        "claims_count": result["claims_count"],
        "llm_enabled": result["llm_enabled"],
        "llm_model": result.get("llm_model"),
        "results": _enrich_results(fw, result["results"]),
    }


@app.post("/api/compare", summary="Compare multiple companies on one framework")
def compare(req: CompareRequest) -> dict:
    if len(req.companies) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 companies to compare.")

    try:
        fw = load_framework(req.framework)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    all_results: list[tuple[str, dict]] = []
    for slug in req.companies:
        try:
            claims = corpus.load_bundled(slug)
            company_name = corpus.canonical_name(slug)
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        r = analyzer.assess(fw, company_name, claims, use_llm=not req.no_llm)
        all_results.append((company_name, r))

    companies = [name for name, _ in all_results]
    scores: dict[str, float] = {}
    enriched: dict[str, dict[str, dict]] = {}
    for company, r in all_results:
        scores[company] = report.readiness_score(r)
        enriched[company] = {ass["criterion_id"]: ass for ass in r["results"]}

    criteria_rows = []
    for crit in fw["criteria"]:
        row: dict = {
            "criterion_id": crit["id"],
            "criterion_name": crit["name"],
            "bar": crit["bar"],
            "ratings": {},
        }
        for company in companies:
            ass = enriched.get(company, {}).get(crit["id"])
            if ass:
                row["ratings"][company] = {
                    "rating": ass["rating"],
                    "gap": ass["gap"],
                    "confidence": round(ass["confidence"], 4),
                    "evidence": ass["evidence"],
                }
        criteria_rows.append(row)

    return {
        "framework_id": req.framework,
        "framework_name": fw["name"],
        "companies": companies,
        "scores": [{"company": c, "score": scores[c]} for c in companies],
        "criteria": criteria_rows,
    }
