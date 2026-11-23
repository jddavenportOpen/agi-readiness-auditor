"""Claim corpus loading.

Two input paths:
  1. Bundled offline corpus  (agi_auditor/corpus/<company>.json). Default, deterministic.
  2. Live fetch of public URLs (--url ...). Pulls text and extracts candidate claim
     sentences. Best-effort; requires `requests` + `beautifulsoup4`.

Each claim is a dict: {"text": str, "source": str}.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

_CORPUS_DIR = Path(__file__).parent / "corpus"

# Sentences mentioning these signal safety/governance/capability posture.
_SIGNAL = re.compile(
    r"\b(safety|safeguard|responsible|preparedness|risk|threshold|capabilit|"
    r"autonom|cbrn|cyber|persuasion|red[- ]?team|evaluat|deploy|misuse|"
    r"alignment|governance|oversight|pause|halt|system card|model card|ASL)\b",
    re.IGNORECASE,
)


def list_bundled() -> list[str]:
    return sorted(p.stem for p in _CORPUS_DIR.glob("*.json"))


def load_bundled(company: str) -> list[dict[str, str]]:
    slug = company.strip().lower().replace(" ", "-")
    path = _CORPUS_DIR / f"{slug}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"No bundled corpus for '{company}' (looked for {path.name}). "
            f"Bundled: {', '.join(list_bundled()) or '(none)'}. "
            f"Use --url to supply public pages instead."
        )
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["claims"]


def canonical_name(company: str) -> str:
    """Return the canonical company name from the bundled corpus JSON, or the input unchanged."""
    slug = company.strip().lower().replace(" ", "-")
    path = _CORPUS_DIR / f"{slug}.json"
    if not path.exists():
        return company
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("company", company)
    except (OSError, json.JSONDecodeError):
        return company


def fetch_urls(urls: list[str], max_claims_per_url: int = 12) -> list[dict[str, str]]:
    """Fetch each URL, extract candidate claim sentences. Best-effort."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError as e:  # pragma: no cover
        raise RuntimeError(
            "Live fetch needs `requests` and `beautifulsoup4`. "
            "Install with: pip install requests beautifulsoup4"
        ) from e

    claims: list[dict[str, str]] = []
    headers = {"User-Agent": "agi-readiness-auditor/0.1 (+research; respects robots)"}
    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
        except Exception as e:  # noqa: BLE001
            print(f"  [warn] could not fetch {url}: {e}")
            continue
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
        sentences = re.split(r"(?<=[.!?])\s+", text)
        picked = 0
        for s in sentences:
            s = " ".join(s.split())
            if 40 <= len(s) <= 400 and _SIGNAL.search(s):
                claims.append({"text": s, "source": url})
                picked += 1
                if picked >= max_claims_per_url:
                    break
    return claims


def load_text_file(path: str, source_label: str | None = None) -> list[dict[str, str]]:
    """Load a plain-text file of claims, one signal-bearing sentence per claim."""
    src = source_label or path
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    out: list[dict[str, str]] = []
    for s in re.split(r"(?<=[.!?])\s+", raw):
        s = " ".join(s.split())
        if 40 <= len(s) <= 500 and _SIGNAL.search(s):
            out.append({"text": s, "source": src})
    return out
