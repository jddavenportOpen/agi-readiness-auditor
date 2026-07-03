# AGI Readiness Auditor — WORKPLAN

<!-- STATUS-BEGIN -->
Progress: 0 of 3 milestones complete (0%)
Last ship: 31d ago — shipped MVP — Python CLI that diffs a company's public AI-safety claims vs published readiness frameworks (OpenAI 5 Levels / Preparedness, Anthropic RSP), LLM claim->criterion mapping w/ deterministic fallback, markdown gap reports, 4 examples, 5 tests, pushed to github.com/JDDavenport/agi-readiness-auditor main
⚠ STALLED: 31d since last ship
<!-- STATUS-END -->


## Next up (priority order)

1. **Commit and push M1 to GitHub** — done, working, tested
2. **M2: LLM quality upgrade** — wire in Anthropic API directly (it's already in env), upgrade from Kimi shape to native Claude for better claim→criterion reasoning
3. **M3: Web API + hosted compare** — FastAPI endpoint wrapping the CLI so the static index.html can call a real backend instead of being a dummy page

## Milestones
- [ ] M1: Major lab expansion — add Google, Microsoft, Meta, xAI corpora; add DeepMind Frontier Safety Framework; add `--compare` mode for side-by-side multi-company comparison tables; 9 tests passing; 6 example reports
- [ ] M2: LLM quality upgrade — wire Anthropic Claude as primary LLM backend (replace Kimi shape), verify LLM path end-to-end, add `--model` flag to choose provider
- [ ] M3: Web API + hosted compare — FastAPI endpoint (`POST /audit`, `POST /compare`) that calls the Python core; update index.html to call it; deploy to Vercel (Python runtime) or Railway

## Blocked on JD decisions
- (none)

## Follow-ups
- LinkedIn post fodder: the comparison table is the killer feature — "Who has the most complete public AGI-safety story?" is a shareable frame
- Add xAI corpus depth when xAI publishes a real safety framework (currently sparse by design — honest)
