# AGI Readiness Auditor — Smoke QA PRD

**Target:** <fill in the deployed/local URL the qa_agent tests>
**Mode:** smoke

Each user story below becomes an automated check (qa_agent parses these).

## US-1 — <surface> renders
- **AC-1.1** Navigating to `/` produces a page whose body contains `<expected text>`.
- **AC-1.2** Exactly 0 elements match `text=Application error`.
