"""Claim -> criterion analysis.

For each framework criterion, decide how well the company's public claims meet
the `bar`. Produces a per-criterion assessment:

  {
    "criterion_id": str,
    "rating": one of framework["scale"],   # e.g. none/partial/substantial/strong
    "evidence": [{"text": str, "source": str}, ...],   # supporting quotes
    "gap": str,        # what's missing vs the bar
    "confidence": float 0..1,
    "method": "llm:anthropic" | "llm:kimi" | "deterministic",
  }

Primary path: Anthropic Claude (claude-sonnet-4-6) via the native Messages API.
Kimi (Anthropic Messages shape) is retained as a secondary option — useful if you
only have KIMI_API_KEY configured. Deterministic keyword analysis is the fallback
when no LLM key is available — so the tool ALWAYS produces a report.

Provider selection (--model flag maps to this):
  "auto"               -> try anthropic, then kimi
  "claude-*"           -> anthropic backend
  "kimi-*"             -> kimi backend
  any other string     -> anthropic backend with that model name
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
import urllib.error
from typing import Any

# ---------------------------------------------------------------------------
# Backend: Anthropic Claude (primary)
# ---------------------------------------------------------------------------

_DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-6"


def _anthropic_key() -> str:
    """Return the best available Anthropic API key, or empty string."""
    return os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY_SUB1", "")


def _anthropic_available() -> bool:
    return bool(_anthropic_key())


def _call_claude(system: str, user: str, model: str | None = None, max_tokens: int = 1500) -> str:
    key = _anthropic_key()
    model = model or _DEFAULT_CLAUDE_MODEL
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("content-type", "application/json")
    req.add_header("x-api-key", key)
    req.add_header("anthropic-version", "2023-06-01")
    with urllib.request.urlopen(req, timeout=90) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    parts = body.get("content", [])
    return "".join(p.get("text", "") for p in parts if p.get("type") == "text")


# ---------------------------------------------------------------------------
# Backend: Kimi (legacy / alternative)
# ---------------------------------------------------------------------------

_DEFAULT_KIMI_MODEL = os.environ.get("AGI_AUDITOR_MODEL", "kimi-k2-0905-preview")


def _kimi_available() -> bool:
    return bool(os.environ.get("KIMI_API_KEY") and os.environ.get("KIMI_BASE_URL"))


def _call_kimi(system: str, user: str, model: str | None = None, max_tokens: int = 1500) -> str:
    base = os.environ["KIMI_BASE_URL"].rstrip("/")
    url = f"{base}/v1/messages"
    payload = {
        "model": model or _DEFAULT_KIMI_MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("content-type", "application/json")
    req.add_header("x-api-key", os.environ["KIMI_API_KEY"])
    req.add_header("anthropic-version", "2023-06-01")
    with urllib.request.urlopen(req, timeout=90) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    parts = body.get("content", [])
    return "".join(p.get("text", "") for p in parts if p.get("type") == "text")


# ---------------------------------------------------------------------------
# Provider resolution
# ---------------------------------------------------------------------------

def _resolve_backend(model: str | None) -> tuple[str | None, str | None]:
    """Return (provider, model_id) or (None, None) if no LLM backend is available.

    model="auto" or None  -> prefer anthropic, fall back to kimi
    model="claude-*"      -> anthropic (error if key absent)
    model="kimi-*"        -> kimi (error if key absent)
    model=<other>         -> anthropic with that exact model string
    """
    explicit = model and model != "auto"
    if explicit:
        if model.startswith("kimi"):
            return ("kimi", model) if _kimi_available() else (None, None)
        # Treat any non-kimi explicit model as an Anthropic model
        return ("anthropic", model) if _anthropic_available() else (None, None)
    # Auto: prefer anthropic
    if _anthropic_available():
        return "anthropic", _DEFAULT_CLAUDE_MODEL
    if _kimi_available():
        return "kimi", _DEFAULT_KIMI_MODEL
    return None, None


# ---------------------------------------------------------------------------
# LLM assessment
# ---------------------------------------------------------------------------

def _llm_assess(
    framework: dict,
    company: str,
    claims: list[dict],
    criterion: dict,
    model: str | None = None,
) -> dict | None:
    provider, actual_model = _resolve_backend(model)
    if provider is None:
        return None

    scale = framework["scale"]
    claim_block = "\n".join(
        f"[{i}] {c['text']}  (source: {c['source']})" for i, c in enumerate(claims)
    )
    system = (
        "You are a rigorous AI-governance auditor. You assess a company's PUBLIC claims "
        "against a single readiness-framework criterion. You are skeptical and evidence-bound: "
        "you only credit a claim if its text actually supports the criterion's bar. You NEVER "
        "invent quotes — you cite only by the [index] of provided claims. Output STRICT JSON only."
    )
    user = (
        f"COMPANY: {company}\n"
        f"FRAMEWORK: {framework['name']}\n\n"
        f"CRITERION: {criterion['name']}\n"
        f"BAR (what the company must publicly meet): {criterion['bar']}\n\n"
        f"COMPANY PUBLIC CLAIMS (cite by index):\n{claim_block}\n\n"
        f"Rate how well the public claims meet the bar. rating must be one of: {scale}.\n"
        "Rules:\n"
        "- 'strong' = bar clearly and specifically met by cited claim(s).\n"
        "- 'substantial' = bar mostly met but missing specificity (e.g. no named threshold).\n"
        "- 'partial' = topic acknowledged but the bar's key element (threshold/stop-condition/"
        "named body) is absent.\n"
        "- 'none' = no public claim addresses this criterion.\n"
        "Return JSON: {\"rating\": <scale>, \"evidence_indices\": [int,...], "
        "\"gap\": \"one sentence: what is missing vs the bar, or 'none — bar met' \", "
        "\"confidence\": 0.0-1.0}\n"
        "evidence_indices must reference only claims that genuinely support the rating. "
        "If rating is 'none', evidence_indices = []."
    )
    try:
        if provider == "anthropic":
            raw = _call_claude(system, user, actual_model)
        else:
            raw = _call_kimi(system, user, actual_model)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None
    parsed = _extract_json(raw)
    if not parsed:
        return None
    rating = parsed.get("rating")
    if rating not in scale:
        return None
    idxs = parsed.get("evidence_indices", []) or []
    evidence = [
        {"text": claims[i]["text"], "source": claims[i]["source"]}
        for i in idxs
        if isinstance(i, int) and 0 <= i < len(claims)
    ]
    try:
        conf = float(parsed.get("confidence", 0.5))
    except (TypeError, ValueError):
        conf = 0.5
    return {
        "criterion_id": criterion["id"],
        "rating": rating,
        "evidence": evidence,
        "gap": str(parsed.get("gap", "")).strip() or "(no gap statement)",
        "confidence": max(0.0, min(1.0, conf)),
        "method": f"llm:{provider}",
    }


def _extract_json(raw: str) -> dict | None:
    raw = raw.strip()
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# Deterministic fallback path (keyword overlap)
# ---------------------------------------------------------------------------

_STOP = set(
    "the a an and or of to in for on with at by is are be as that this it its their "
    "company public must bar above which level stated has have not no e.g".split()
)


def _keywords(text: str) -> set[str]:
    toks = re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", text.lower())
    return {t for t in toks if t not in _STOP}


def _deterministic_assess(framework: dict, company: str, claims: list[dict], criterion: dict) -> dict:
    scale = framework["scale"]
    bar_kw = _keywords(criterion["bar"]) | _keywords(criterion["name"])
    scored = []
    for c in claims:
        overlap = bar_kw & _keywords(c["text"])
        if overlap:
            scored.append((len(overlap), c))
    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        return {
            "criterion_id": criterion["id"],
            "rating": scale[0],  # none
            "evidence": [],
            "gap": "No public claim in the corpus addresses this criterion.",
            "confidence": 0.35,
            "method": "deterministic",
        }

    top = scored[: min(3, len(scored))]
    best_overlap = top[0][0]
    hard = re.compile(r"\b(threshold|will pause|halt|gate|named|commit|standard|ASL-?\d|score)\b", re.I)
    has_hard = any(hard.search(c["text"]) for _, c in top)

    if best_overlap >= 4 and has_hard:
        rating = scale[3] if len(scale) > 3 else scale[-1]  # strong
        gap = "Keyword + hard-commitment signal present (deterministic). Verify specificity manually."
        conf = 0.55
    elif best_overlap >= 3:
        rating = scale[2] if len(scale) > 2 else scale[-1]  # substantial
        gap = "Topic addressed but no clear stated threshold/stop-condition in matched text."
        conf = 0.5
    else:
        rating = scale[1] if len(scale) > 1 else scale[0]  # partial
        gap = "Only weak topical overlap; the criterion's key element appears unaddressed."
        conf = 0.4

    return {
        "criterion_id": criterion["id"],
        "rating": rating,
        "evidence": [{"text": c["text"], "source": c["source"]} for _, c in top],
        "gap": gap,
        "confidence": conf,
        "method": "deterministic",
    }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def assess(
    framework: dict,
    company: str,
    claims: list[dict],
    use_llm: bool = True,
    verbose: bool = False,
    model: str | None = None,
) -> dict[str, Any]:
    """Run the full audit. Returns a results dict ready for rendering.

    model: provider/model selection — "auto" (default), "claude-sonnet-4-6",
           "claude-haiku-4-5-20251001", "kimi-k2-0905-preview", etc.
    """
    provider, actual_model = _resolve_backend(model) if use_llm else (None, None)
    llm_on = use_llm and provider is not None

    results = []
    methods: dict[str, int] = {}
    for crit in framework["criteria"]:
        r = None
        if llm_on:
            r = _llm_assess(framework, company, claims, crit, model)
            if r is None and verbose:
                print(f"  [info] LLM assess failed for {crit['id']} -> deterministic fallback")
        if r is None:
            r = _deterministic_assess(framework, company, claims, crit)
        methods[r["method"]] = methods.get(r["method"], 0) + 1
        results.append(r)
        if verbose:
            print(f"  [{r['method']}] {crit['id']}: {r['rating']} (conf {r['confidence']:.2f})")

    any_llm = any(r["method"].startswith("llm") for r in results)
    return {
        "company": company,
        "framework": framework,
        "claims_count": len(claims),
        "results": results,
        "method_summary": methods,
        "llm_enabled": any_llm,
        "llm_model": actual_model if any_llm else None,
    }
