# 🏛 ARCHITECT BRIEFING (read before you build)

**What this system is:** **SOURCE OF TRUTH for "what did we do" / "what's been built":** `~/clawd/CHANGELOG.md`. Read it first. Answer JD from there, not from chat history.

**Hard conventions (do not violate — the architect gates these at sign-off):**
- Root-cause first, never bandaid — fix the process that generated the bug, then the symptom.
- Ship to prod: you open the PR, wait for CI, merge, deploy, smoke-test prod. JD reviews in prod, never PRs.
- Parallel/background sub-agents MUST run in a git worktree (isolation), never the shared checkout.
- Inventory before spawning — reuse an existing agent/capability before building a new one.
- RUNBOOK/tooling first — check for an existing generator before hand-writing output.
- File-based state over conversation memory. Log material work via clawd-log.sh.
- Surgical, scope-disciplined changes — don't refactor adjacent code outside the task.

**Capabilities that ALREADY EXIST (reuse, don't duplicate):**
  agents: jd (Founder / Sole Decision Maker); clawd (CEO Orchestrator); family (Family Domain); school (Academic Domain (BYU MBA)); siemens (Corporate Domain (Siemens Internship)); consulting (Consulting Domain (Pipeline + Delivery)); growth (Growth Domain (Socrates X / LinkedIn / Newsletter)); ai-foundry (AI Foundry Domain (BYU AI Foundry program)); health (Health Domain (Garmin + sleep + weight + workouts)); life-ops (Life Ops Domain (catch-all + system health)); chief-of-staff (Cadence + Verification (peer of CEO)); architect (Product-Coherence Governor (peer of CEO)); design (Shared Service (UI/UX, diagrams, infographics)); dev-team (Shared Service (full-stack builds, API dev, CI/CD)); presentation (Shared Service (slides, pitch decks)); research (Shared Service (web research, competitive intel)); budget-analyst (Family Specialist (envelope budgeting + hard-stop)); health-coach (Family Specialist (originally) — now folded into Health domain); family-mgr (Family Specialist (Sam + kids coordination)); todo-enforcer (Family Specialist (GTD enforcement)); master-tutor (School Specialist (subject tutoring on demand)); assignment-tracker (School Specialist (Canvas deadline tracking)); study-scheduler (School Specialist (calendar block proposals)); onboarding-prep (Siemens Specialist); network-builder (Siemens Specialist (LinkedIn outreach)); proposal-writer (Consulting Specialist); research-analyst (Consulting Specialist); sentinel (Growth Specialist (social monitoring)); broadcast (Growth Specialist (X / LinkedIn posting)); newsletter-writer (Growth Specialist); analytics-tracker (Growth Specialist); seo-watcher (Growth Specialist); curriculum-designer (AI Foundry Specialist); funding-tracker (AI Foundry Specialist); professor (School Specialist (course-expert agents)); analytics-suite (School Specialist (MBA Business Analytics)); counselor (School Specialist (advising)); tax-strategist (Consulting Specialist); deck-architect-v4 (Growth Specialist (presentation building)); synthetic-users (AI Foundry Specialist (UX research at scale))
  projects: leland-coaching [active]; x-agent-socrates [planning]; second-brain-infra [active]; plaud-pipeline [archived]; consulting-pipeline [idea]; newsletter-agent-brief [active]; ai-foundry-program [active]; siemens-onboarding [active]; family-budget [archived]; nerve-center-v5 [active]; jarvis-ai-os [archived]; agent-tree-hub [active]; agent-tree-collab [active]; openclaw-marketplace [active]; deck-architect-v4 [planning]; school-overhaul [archived]; byu-alumni-portal [active]; ai-os-system-audit [active]; creditoclaro-demo [active]; loanamigo-demo [paused]; mba-bidding-reviews; slopes-mortgage [paused]; adsbybitcoin [paused]; quanta [complete]; mba-course-catalog-courserank [complete]; study-aide [archived]; voiceclaw [archived]; acquisitor [complete]; pitchgrade [archived]; venture-val [archived]

### Project: agi-readiness-auditor
**Goal:** TBD — finish this sentence: "When this project is done, we will have ______."
**Open milestones:**
  - [ ] M1: TBD
  - [ ] M2: TBD
  - [ ] M3: TBD
**Recently shipped:**
  - 07:16 — Project scaffolded (status: active, domain: growth).

**This change vs origin/main:** SIGNIFICANT — 23 file(s) touch: api-interface, auth, db-migration, infra-config
  ⚠ [api-interface] apps/hivehood/src/app/api/admin/content/route.ts — API route / interface / schema — public contract other code depends on
  ⚠ [api-interface] apps/hivehood/src/app/api/admin/events/[id]/hide/route.ts — API route / interface / schema — public contract other code depends on
  ⚠ [api-interface] apps/hivehood/src/app/api/admin/events/[id]/route.ts — API route / interface / schema — public contract other code depends on
  ⚠ [api-interface] apps/hivehood/src/app/api/admin/events/route.ts — API route / interface / schema — public contract other code depends on
  ⚠ [api-interface] apps/hivehood/src/app/api/assistant/route.ts — API route / interface / schema — public contract other code depends on
  ⚠ [api-interface] apps/hivehood/src/app/api/auth/logout/route.ts — API route / interface / schema — public contract other code depends on
  ⚠ [api-interface] apps/hivehood/src/app/api/auth/request/route.ts — API route / interface / schema — public contract other code depends on
  ⚠ [api-interface] apps/hivehood/src/app/api/auth/verify/route.ts — API route / interface / schema — public contract other code depends on
  ⚠ [api-interface] apps/hivehood/src/app/api/events/route.ts — API route / interface / schema — public contract other code depends on
  ⚠ [auth] apps/hivehood/src/components/LoginForm.tsx — authentication / authorization / middleware — security contract
  ⚠ [auth] apps/hivehood/src/lib/auth.ts — authentication / authorization / middleware — security contract
  ⚠ [auth] apps/hivehood/src/lib/session.ts — authentication / authorization / middleware — security contract

Reuse what exists. Follow the conventions. Significant (shared-contract) changes will be hard-gated by the architect at sign-off — build coherent from the start so you don't get blocked.
