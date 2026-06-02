"""Smoke + correctness tests for the deterministic core (no network/LLM needed).

Run: python -m pytest -q   (or: python tests/test_core.py)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agi_auditor import analyzer, corpus, report
from agi_auditor.frameworks import list_frameworks, load_framework


def test_all_frameworks_load_and_validate():
    fids = list_frameworks()
    assert fids, "no frameworks registered"
    for fid in fids:
        fw = load_framework(fid)
        assert fw["criteria"], f"{fid} has no criteria"
        for c in fw["criteria"]:
            assert c["bar"] and c["source"], f"{fid}:{c['id']} missing bar/source"


def test_bundled_corpus_loads():
    for company in corpus.list_bundled():
        claims = corpus.load_bundled(company)
        assert claims, f"{company} corpus empty"
        for cl in claims:
            assert cl["text"] and cl["source"]


def test_deterministic_assess_produces_full_report():
    fw = load_framework("openai-5-levels")
    claims = corpus.load_bundled("openai")
    result = analyzer.assess(fw, "OpenAI", claims, use_llm=False)
    # one result per criterion
    assert len(result["results"]) == len(fw["criteria"])
    for r in result["results"]:
        assert r["rating"] in fw["scale"]
        assert 0.0 <= r["confidence"] <= 1.0
        assert r["method"] == "deterministic"
    md = report.render(result)
    assert "AGI Readiness Gap Report" in md
    assert "## Summary" in md
    assert "## Methodology" in md


def test_score_bounds():
    fw = load_framework("anthropic-rsp")
    claims = corpus.load_bundled("anthropic")
    result = analyzer.assess(fw, "Anthropic", claims, use_llm=False)
    s = report.readiness_score(result)
    assert 0 <= s <= 100


def test_evidence_indices_never_fabricate():
    # deterministic evidence must come from the provided claims
    fw = load_framework("openai-preparedness")
    claims = corpus.load_bundled("openai")
    claim_texts = {c["text"] for c in claims}
    result = analyzer.assess(fw, "OpenAI", claims, use_llm=False)
    for r in result["results"]:
        for ev in r["evidence"]:
            assert ev["text"] in claim_texts, "evidence not traceable to a real claim"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(fns)} tests passed.")
