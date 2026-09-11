# AGI Readiness Gap Report — Anthropic

**Framework:** OpenAI Preparedness Framework (Tracked Risk Categories)  
**Date:** 2026-06-02  
**Public-claim coverage score:** 26/100 _(share of framework bars met by public claims)_  
**Analysis method:** LLM (claim→criterion mapping)  
**Claims analyzed:** 7

> **Scope:** This audits a company's PUBLIC, stated posture — blog posts, frameworks, model/system cards, public statements. It does **not** measure internal practice or whether claims are honored. A high score means the public story is complete, not that the company is safe.

## Summary

| Criterion | Rating | Confidence | Method |
|---|---|---|---|
| Cybersecurity | 🟠 partial | 75% | llm |
| CBRN (chem / bio / radiological / nuclear) | 🟠 partial | 75% | llm |
| Persuasion / Influence | 🔴 none | 95% | llm |
| Model Autonomy / Self-improvement | 🟠 partial | 75% | llm |
| Governance & Stop Conditions | 🟠 partial | 75% | llm |

## Detail

### 🟠 Cybersecurity — **partial**

**Bar:** Public position on model uplift to cyber-offensive operations, with a stated capability threshold above which deployment is gated or mitigated.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> Anthropic commits to running dangerous-capability evaluations (CBRN, cyber, autonomy) before and during scaling, and publishes model cards with red-team and eval results.
> — source: https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Gap assessment:** While Anthropic commits to running cyber capability evaluations and publishes results, no public claim specifies a named capability threshold for cyber-offensive operations above which deployment is gated or mitigated — the RSP's ASL framework names CBRN but not a distinct cyber-offensive threshold.

**Confidence:** 75%

---

### 🟠 CBRN (chem / bio / radiological / nuclear) — **partial**

**Bar:** Public position on biological/chemical uplift, including a stated threshold (e.g. 'meaningful uplift to a novice') above which the model is restricted.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> Anthropic activated ASL-3 deployment and security standards for Claude Opus 4, citing CBRN uplift potential, including misuse filtering and weight-protection controls.
> — source: https://www.anthropic.com/news/activating-asl3-protections

**Gap assessment:** Claim [1] acknowledges CBRN uplift as a factor in activating ASL-3 protections, but no public claim states a specific quantitative or qualitative threshold (e.g., 'meaningful uplift to a novice') above which models are restricted; the 'Capability Thresholds' in [0] are named but not defined in the provided text.

**Confidence:** 75%

---

### 🔴 Persuasion / Influence — **none**

**Bar:** Public position on model-driven persuasion, manipulation, or influence operations, with a stated mitigation or evaluation.

**Framework source:** https://cdn.openai.com/openai-preparedness-framework-beta.pdf

**Evidence:** _none found in corpus._

**Gap assessment:** No public claim addresses persuasion, manipulation, or influence operations specifically; the RSP and model cards discuss CBRN, cyber, autonomy, and general safety evaluations but omit any stated position on model-driven persuasion or influence mitigation/evaluation.

**Confidence:** 95%

---

### 🟠 Model Autonomy / Self-improvement — **partial**

**Bar:** Public position on autonomous capability (self-exfiltration, self-improvement, resource acquisition), with a stated threshold above which development is gated.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> Anthropic commits to running dangerous-capability evaluations (CBRN, cyber, autonomy) before and during scaling, and publishes model cards with red-team and eval results.
> — source: https://www.anthropic.com/news/anthropics-responsible-scaling-policy

> Anthropic addresses agentic / autonomous use via computer-use safeguards and the RSP autonomy evaluations, with constrained deployment and oversight guidance for agentic products.
> — source: https://www.anthropic.com/news/developing-computer-use

**Gap assessment:** Autonomy is mentioned as an evaluation category and agentic deployment has safeguards, but no specific Capability Threshold or gating condition for self-improvement, self-exfiltration, or resource acquisition is publicly named with a concrete stop-condition.

**Confidence:** 75%

---

### 🟠 Governance & Stop Conditions — **partial**

**Bar:** A named internal body (e.g. Safety Advisory Group, board) with authority to block deployment, AND a public commitment to halt/hold if a threshold is crossed.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> The RSP states Anthropic will pause scaling or restrict deployment if a model crosses a Capability Threshold before the corresponding Required Safeguards are in place.
> — source: https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Gap assessment:** No named internal body with authority to block deployment is identified in any claim; while [4] describes a pause/restriction commitment triggered by capability thresholds, it does not specify who has decision-making authority to enforce this stop condition.

**Confidence:** 75%

---

## Where the public posture falls short

- **Cybersecurity** (partial): While Anthropic commits to running cyber capability evaluations and publishes results, no public claim specifies a named capability threshold for cyber-offensive operations above which deployment is gated or mitigated — the RSP's ASL framework names CBRN but not a distinct cyber-offensive threshold.
- **CBRN (chem / bio / radiological / nuclear)** (partial): Claim [1] acknowledges CBRN uplift as a factor in activating ASL-3 protections, but no public claim states a specific quantitative or qualitative threshold (e.g., 'meaningful uplift to a novice') above which models are restricted; the 'Capability Thresholds' in [0] are named but not defined in the provided text.
- **Persuasion / Influence** (none): No public claim addresses persuasion, manipulation, or influence operations specifically; the RSP and model cards discuss CBRN, cyber, autonomy, and general safety evaluations but omit any stated position on model-driven persuasion or influence mitigation/evaluation.
- **Model Autonomy / Self-improvement** (partial): Autonomy is mentioned as an evaluation category and agentic deployment has safeguards, but no specific Capability Threshold or gating condition for self-improvement, self-exfiltration, or resource acquisition is publicly named with a concrete stop-condition.
- **Governance & Stop Conditions** (partial): No named internal body with authority to block deployment is identified in any claim; while [4] describes a pause/restriction commitment triggered by capability thresholds, it does not specify who has decision-making authority to enforce this stop condition.

## Methodology & sources

Framework definition: **OpenAI Preparedness Framework (Tracked Risk Categories)**

- https://openai.com/index/updating-our-preparedness-framework/
- https://cdn.openai.com/openai-preparedness-framework-beta.pdf

Ratings: 🔴 none · 🟠 partial · 🟡 substantial · 🟢 strong. Each criterion is scored on whether the company's *public claims* meet the framework's *bar* — the specific, citable threshold above. Evidence quotes link to public sources so every claim in this report is independently checkable.

_Generated by [AGI Readiness Auditor](https://github.com/jddavenportOpen/agi-readiness-auditor)._
