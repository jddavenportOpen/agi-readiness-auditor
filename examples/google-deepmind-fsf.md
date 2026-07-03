# AGI Readiness Gap Report — google

**Framework:** Google DeepMind Frontier Safety Framework (FSF)  
**Date:** 2026-07-03  
**Public-claim coverage score:** 86/100 _(share of framework bars met by public claims)_  
**Analysis method:** deterministic keyword fallback  
**Claims analyzed:** 8

> **Scope:** This audits a company's PUBLIC, stated posture — blog posts, frameworks, model/system cards, public statements. It does **not** measure internal practice or whether claims are honored. A high score means the public story is complete, not that the company is safe.

## Summary

| Criterion | Rating | Confidence | Method |
|---|---|---|---|
| Scheduled dangerous-capability evaluations | 🟢 strong | 55% | deterministic |
| CBRN uplift prevention | 🟡 substantial | 50% | deterministic |
| Oversight preservation | 🟢 strong | 55% | deterministic |
| Unsanctioned autonomy / power-seizure prevention | 🟡 substantial | 50% | deterministic |
| Threshold-based deployment halt | 🟢 strong | 55% | deterministic |

## Detail

### 🟢 Scheduled dangerous-capability evaluations — **strong**

**Bar:** Run pre-deployment and in-deployment evaluations for dangerous capabilities (CBRN, cyber, autonomy) on a defined schedule. Bar: publicly state a commitment to scheduled model evaluations for dangerous capabilities before deployment and at defined capability checkpoints.

**Framework source:** https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

**Evidence (public claims):**
> The FSF commits to running model evaluations for dangerous capabilities including CBRN uplift, cyber offense, and unsanctioned autonomy on a defined schedule before and during model deployment.
> — source: https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

> Google DeepMind's Frontier Safety Framework (FSF, May 2024) defines two concern levels: Level 1 (enhanced monitoring) and Level 2 (deployment/development halt) triggered by dangerous-capability evaluations on pre-defined thresholds.
> — source: https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

> Google DeepMind publishes the Gemini 1.5 and Gemini 1.0 technical reports and system cards documenting capability evaluations, safety red-teaming, and known failure modes including hallucination.
> — source: https://storage.googleapis.com/deepmind-media/gemini/gemini_1_5_report.pdf

**Gap assessment:** Keyword + hard-commitment signal present (deterministic). Verify specificity manually.

**Confidence:** 55%

---

### 🟡 CBRN uplift prevention — **substantial**

**Bar:** Commit to not providing serious uplift toward creation of weapons capable of mass casualties (CBRN: chemical, biological, radiological, nuclear). Bar: a named, public prohibition on CBRN-uplifting use cases backed by a stated detection/filtering mechanism.

**Framework source:** https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

**Evidence (public claims):**
> The FSF's critical safety behaviors include: not providing serious uplift to CBRN weapons, not undermining the ability of principals to oversee and correct AI models, not engaging or assisting attempts to seize unprecedented societal control.
> — source: https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

> The FSF commits to running model evaluations for dangerous capabilities including CBRN uplift, cyber offense, and unsanctioned autonomy on a defined schedule before and during model deployment.
> — source: https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

> Google's Secure AI Framework (SAIF) defines six core elements: expand strong security foundations, extend detection and response, automate defenses, harmonize controls, adapt existing frameworks, and contextualize AI risk.
> — source: https://safety.google/cybersecurity-advancements/saif/

**Gap assessment:** Topic addressed but no clear stated threshold/stop-condition in matched text.

**Confidence:** 50%

---

### 🟢 Oversight preservation — **strong**

**Bar:** Commit to not undermining human ability to oversee, correct, or shut down AI models. Bar: a public statement affirming that the company will not deploy or support systems that actively evade correction or oversight mechanisms, with a stated mechanism for this.

**Framework source:** https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

**Evidence (public claims):**
> The FSF's critical safety behaviors include: not providing serious uplift to CBRN weapons, not undermining the ability of principals to oversee and correct AI models, not engaging or assisting attempts to seize unprecedented societal control.
> — source: https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

> Google AI Principles (published 2018, updated 2023) commit to being socially beneficial, avoiding unfair bias, being built and tested for safety, being accountable to people, incorporating privacy, upholding high scientific excellence, and being made available for uses that accord with these principles.
> — source: https://ai.google/responsibility/principles/

**Gap assessment:** Keyword + hard-commitment signal present (deterministic). Verify specificity manually.

**Confidence:** 55%

---

### 🟡 Unsanctioned autonomy / power-seizure prevention — **substantial**

**Bar:** Commit to preventing AI from engaging in or assisting attempts to seize unprecedented societal control or accumulate resources beyond sanctioned limits. Bar: public policy or framework language explicitly covering autonomous action limits and power-accumulation safeguards.

**Framework source:** https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

**Evidence (public claims):**
> The FSF's critical safety behaviors include: not providing serious uplift to CBRN weapons, not undermining the ability of principals to oversee and correct AI models, not engaging or assisting attempts to seize unprecedented societal control.
> — source: https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

> Google Gemini's agentic features (Project Mariner, Jules) include constrained action spaces, task confirmation steps, and usage policy restrictions on autonomous actions in high-stakes domains.
> — source: https://deepmind.google/technologies/project-mariner/

> The FSF commits to running model evaluations for dangerous capabilities including CBRN uplift, cyber offense, and unsanctioned autonomy on a defined schedule before and during model deployment.
> — source: https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

**Gap assessment:** Topic addressed but no clear stated threshold/stop-condition in matched text.

**Confidence:** 50%

---

### 🟢 Threshold-based deployment halt — **strong**

**Bar:** Define pre-specified concern levels where development or deployment pauses until safeguards are in place. Bar: a public commitment to halt or restrict deployment when a named threshold (capability evaluation result, concern level, or equivalent) is crossed, before safeguards exist.

**Framework source:** https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

**Evidence (public claims):**
> Google DeepMind's Frontier Safety Framework (FSF, May 2024) defines two concern levels: Level 1 (enhanced monitoring) and Level 2 (deployment/development halt) triggered by dangerous-capability evaluations on pre-defined thresholds.
> — source: https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

> The FSF commits to running model evaluations for dangerous capabilities including CBRN uplift, cyber offense, and unsanctioned autonomy on a defined schedule before and during model deployment.
> — source: https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

> Google DeepMind publishes the Gemini 1.5 and Gemini 1.0 technical reports and system cards documenting capability evaluations, safety red-teaming, and known failure modes including hallucination.
> — source: https://storage.googleapis.com/deepmind-media/gemini/gemini_1_5_report.pdf

**Gap assessment:** Keyword + hard-commitment signal present (deterministic). Verify specificity manually.

**Confidence:** 55%

---

## Where the public posture falls short

- No criterion rated below `substantial` on public claims.

## Methodology & sources

Framework definition: **Google DeepMind Frontier Safety Framework (FSF)**

- https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/

Ratings: 🔴 none · 🟠 partial · 🟡 substantial · 🟢 strong. Each criterion is scored on whether the company's *public claims* meet the framework's *bar* — the specific, citable threshold above. Evidence quotes link to public sources so every claim in this report is independently checkable.

_Generated by [AGI Readiness Auditor](https://github.com/JDDavenport/agi-readiness-auditor)._
