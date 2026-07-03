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


def test_new_corpora_load_and_have_required_fields():
    for company in ("google", "microsoft", "meta", "xai"):
        claims = corpus.load_bundled(company)
        assert claims, f"{company} corpus empty"
        for cl in claims:
            assert cl["text"] and cl["source"], f"{company}: claim missing text or source"


def test_deepmind_fsf_framework():
    fw = load_framework("deepmind-fsf")
    assert fw["id"] == "deepmind-fsf"
    assert len(fw["criteria"]) == 5
    for c in fw["criteria"]:
        assert c["bar"] and c["source"]


def test_compare_render():
    fw = load_framework("openai-preparedness")
    companies_data = [
        ("openai", "OpenAI"),
        ("anthropic", "Anthropic"),
        ("google", "Google"),
    ]
    results = []
    for slug, name in companies_data:
        claims = corpus.load_bundled(slug)
        r = analyzer.assess(fw, name, claims, use_llm=False)
        results.append(r)
    md = report.render_compare(results)
    assert "AGI Readiness Comparison" in md
    assert "Coverage Scores" in md
    assert "Criterion-by-criterion comparison" in md
    assert "OpenAI" in md and "Anthropic" in md and "Google" in md
    # All scores should be in range
    for r in results:
        s = report.readiness_score(r)
        assert 0 <= s <= 100


def test_new_corpora_deterministic_full_audit():
    fw = load_framework("deepmind-fsf")
    for company_slug, company_name in (
        ("google", "Google"),
        ("microsoft", "Microsoft"),
        ("meta", "Meta"),
        ("xai", "xAI"),
    ):
        claims = corpus.load_bundled(company_slug)
        result = analyzer.assess(fw, company_name, claims, use_llm=False)
        assert len(result["results"]) == len(fw["criteria"])
        for r in result["results"]:
            assert r["rating"] in fw["scale"]
            assert 0.0 <= r["confidence"] <= 1.0
        s = report.readiness_score(result)
        assert 0 <= s <= 100


def test_provider_routing():
    """_resolve_backend routes to the right provider based on model name."""
    from agi_auditor.analyzer import _resolve_backend
    import os

    # kimi model name -> kimi backend (only if keys set)
    saved_kimi_key = os.environ.pop("KIMI_API_KEY", None)
    saved_kimi_url = os.environ.pop("KIMI_BASE_URL", None)
    saved_ant_key = os.environ.pop("ANTHROPIC_API_KEY", None)
    saved_sub1 = os.environ.pop("ANTHROPIC_API_KEY_SUB1", None)
    try:
        # No keys: auto returns (None, None)
        provider, model = _resolve_backend("auto")
        assert provider is None

        # Set anthropic key: auto prefers anthropic
        os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test"
        provider, model = _resolve_backend("auto")
        assert provider == "anthropic"
        assert "claude" in model

        # Explicit claude model: anthropic
        provider, model = _resolve_backend("claude-haiku-4-5-20251001")
        assert provider == "anthropic"
        assert model == "claude-haiku-4-5-20251001"

        # Explicit kimi model without kimi keys: (None, None)
        provider, model = _resolve_backend("kimi-k2-0905-preview")
        assert provider is None

        # Set kimi keys: kimi model -> kimi backend
        os.environ["KIMI_API_KEY"] = "kimi-test"
        os.environ["KIMI_BASE_URL"] = "https://api.kimi.test"
        provider, model = _resolve_backend("kimi-k2-0905-preview")
        assert provider == "kimi"

        # With both keys, auto still prefers anthropic
        provider, model = _resolve_backend(None)
        assert provider == "anthropic"
    finally:
        # Restore env
        for k in ("ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY_SUB1", "KIMI_API_KEY", "KIMI_BASE_URL"):
            os.environ.pop(k, None)
        if saved_kimi_key is not None:
            os.environ["KIMI_API_KEY"] = saved_kimi_key
        if saved_kimi_url is not None:
            os.environ["KIMI_BASE_URL"] = saved_kimi_url
        if saved_ant_key is not None:
            os.environ["ANTHROPIC_API_KEY"] = saved_ant_key
        if saved_sub1 is not None:
            os.environ["ANTHROPIC_API_KEY_SUB1"] = saved_sub1


def test_assess_result_has_llm_model_field():
    """assess() result always has llm_model key (None when deterministic)."""
    fw = load_framework("openai-5-levels")
    claims = corpus.load_bundled("openai")
    result = analyzer.assess(fw, "OpenAI", claims, use_llm=False)
    assert "llm_model" in result
    assert result["llm_model"] is None
    assert result["llm_enabled"] is False


def test_method_field_values():
    """Per-criterion method is one of the expected strings."""
    fw = load_framework("openai-5-levels")
    claims = corpus.load_bundled("openai")
    result = analyzer.assess(fw, "OpenAI", claims, use_llm=False)
    for r in result["results"]:
        assert r["method"] in ("deterministic", "llm:anthropic", "llm:kimi"), r["method"]


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(fns)} tests passed.")
