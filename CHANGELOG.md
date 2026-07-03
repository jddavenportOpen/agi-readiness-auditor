# AGI Readiness Auditor — CHANGELOG

Append-only record of what's shipped for this project. Newest at top.
Run `bash ~/agent-system/scripts/clawd-log.sh agi-readiness-auditor "shipped X"` to append.

---

## 2026-07-03

- 16:30 — M2: Anthropic Claude wired as primary LLM backend (claude-sonnet-4-6), multi-provider routing (_resolve_backend), --model flag, env auto-loads ANTHROPIC_API_KEY_SUB1, 12/12 tests pass, live API verified
- 15:42 — M1 shipped: added Google/Microsoft/Meta/xAI bundled corpora, DeepMind Frontier Safety Framework (deepmind-fsf), --compare side-by-side comparison mode, corpus.canonical_name(), 9 tests passing, 4 new example reports; pushed to github.com/JDDavenport/agi-readiness-auditor main

---

## 2026-06-02

- 07:25 — shipped MVP — Python CLI that diffs a company's public AI-safety claims vs published readiness frameworks (OpenAI 5 Levels / Preparedness, Anthropic RSP), LLM claim->criterion mapping w/ deterministic fallback, markdown gap reports, 4 examples, 5 tests, pushed to github.com/JDDavenport/agi-readiness-auditor main
- 07:16 — Project scaffolded (status: active, domain: growth).
