"""AGI Readiness Auditor — CLI.

Examples:
  python -m agi_auditor --company "OpenAI" --framework openai-5-levels
  python -m agi_auditor --company "Anthropic" --framework anthropic-rsp -o examples/anthropic.md
  python -m agi_auditor --company "Acme" --framework openai-preparedness \
      --url https://acme.ai/safety --url https://acme.ai/blog/preparedness
  python -m agi_auditor --list-frameworks
"""
from __future__ import annotations

import argparse
import os
import sys

from . import __version__, analyzer, corpus, report
from .frameworks import list_frameworks, load_framework


def _load_env_file() -> None:
    """Best-effort: load KIMI_* from ~/agent-system/.env if not already set.

    The tool works WITHOUT this (deterministic fallback). This is a convenience
    for local runs. It never prints or logs the key.
    """
    if os.environ.get("KIMI_API_KEY"):
        return
    path = os.path.expanduser("~/agent-system/.env")
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                if k in ("KIMI_API_KEY", "KIMI_BASE_URL", "AGI_AUDITOR_MODEL"):
                    os.environ.setdefault(k, v.strip().strip('"').strip("'"))
    except OSError:
        pass


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="agi_auditor",
        description="Diff a company's PUBLIC AI-safety claims against a published readiness framework.",
    )
    p.add_argument("--company", help="Company name (e.g. 'OpenAI').")
    p.add_argument(
        "--framework",
        default="openai-5-levels",
        help=f"Framework id. One of: {', '.join(list_frameworks())}",
    )
    p.add_argument(
        "--url",
        action="append",
        default=[],
        metavar="URL",
        help="Public URL to fetch claims from (repeatable). If omitted, uses bundled corpus.",
    )
    p.add_argument(
        "--claims-file",
        help="Path to a plain-text file of claims (one per sentence) to analyze.",
    )
    p.add_argument("-o", "--out", help="Write report to this file instead of stdout.")
    p.add_argument(
        "--no-llm",
        action="store_true",
        help="Force the deterministic keyword analyzer (skip the LLM).",
    )
    p.add_argument("-v", "--verbose", action="store_true", help="Print per-criterion progress.")
    p.add_argument("--list-frameworks", action="store_true", help="List frameworks and exit.")
    p.add_argument("--list-corpus", action="store_true", help="List bundled company corpora and exit.")
    p.add_argument("--version", action="version", version=f"agi_auditor {__version__}")
    args = p.parse_args(argv)

    if args.list_frameworks:
        for fid in list_frameworks():
            fw = load_framework(fid)
            print(f"{fid:24s}  {fw['name']}  ({len(fw['criteria'])} criteria)")
        return 0

    if args.list_corpus:
        for c in corpus.list_bundled():
            print(c)
        return 0

    if not args.company:
        p.error("--company is required (or use --list-frameworks / --list-corpus)")

    _load_env_file()

    try:
        framework = load_framework(args.framework)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    # Gather claims
    claims: list[dict] = []
    if args.url:
        print(f"Fetching {len(args.url)} URL(s)...", file=sys.stderr)
        claims = corpus.fetch_urls(args.url)
    elif args.claims_file:
        claims = corpus.load_text_file(args.claims_file)
    else:
        try:
            claims = corpus.load_bundled(args.company)
            print(f"Using bundled corpus for '{args.company}'.", file=sys.stderr)
        except FileNotFoundError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2

    if not claims:
        print("error: no claims gathered — nothing to audit.", file=sys.stderr)
        return 3

    print(
        f"Auditing {args.company} against '{framework['name']}' "
        f"({len(claims)} claims)...",
        file=sys.stderr,
    )
    result = analyzer.assess(
        framework,
        args.company,
        claims,
        use_llm=not args.no_llm,
        verbose=args.verbose,
    )
    md = report.render(result)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
        score = report.readiness_score(result)
        print(f"Wrote {args.out}  (coverage score: {score}/100)", file=sys.stderr)
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
