# AGI Readiness Gap Report: Anthropic

**Framework:** Anthropic Responsible Scaling Policy (ASL levels)  
**Date:** 2026-06-02  
**Public-claim coverage score:** 100/100 _(share of framework bars met by public claims)_  
**Analysis method:** LLM (claim→criterion mapping)  
**Claims analyzed:** 7

> **Scope:** This audits a company's PUBLIC, stated posture: blog posts, frameworks, model/system cards, public statements. It does **not** measure internal practice or whether claims are honored. A high score means the public story is complete, not that the company is safe.

## Summary

| Criterion | Rating | Confidence | Method |
|---|---|---|---|
| ASL Capability Thresholds | strong | 95% | llm |
| Deployment Safeguards | strong | 92% | llm |
| Security / Weight Protection | strong | 90% | llm |
| Capability Evaluations & Red-teaming | strong | 95% | llm |
| Pause / Stop Commitment | strong | 95% | llm |

## Detail

### ASL Capability Thresholds (strong)

**Bar:** Publicly defines capability thresholds (analogous to ASL-2/ASL-3) that, when crossed, trigger stronger safeguards. Bar: named, written thresholds, not vibes.

**Framework source:** https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Evidence (public claims):**
> Anthropic's Responsible Scaling Policy defines AI Safety Levels (ASL-2, ASL-3, ...) with named Capability Thresholds that trigger Required Safeguards when crossed.
> Source: https://www.anthropic.com/news/anthropics-responsible-scaling-policy

> Anthropic activated ASL-3 deployment and security standards for Claude Opus 4, citing CBRN uplift potential, including misuse filtering and weight-protection controls.
> Source: https://www.anthropic.com/news/activating-asl3-protections

> The RSP states Anthropic will pause scaling or restrict deployment if a model crosses a Capability Threshold before the corresponding Required Safeguards are in place.
> Source: https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Gap assessment:** none, bar met

**Confidence:** 95%

---

### Deployment Safeguards (strong)

**Bar:** Public commitment to deployment-stage protections (misuse filtering, jailbreak resistance, harm-refusal) tied to capability level.

**Framework source:** https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Evidence (public claims):**
> Anthropic's Responsible Scaling Policy defines AI Safety Levels (ASL-2, ASL-3, ...) with named Capability Thresholds that trigger Required Safeguards when crossed.
> Source: https://www.anthropic.com/news/anthropics-responsible-scaling-policy

> Anthropic activated ASL-3 deployment and security standards for Claude Opus 4, citing CBRN uplift potential, including misuse filtering and weight-protection controls.
> Source: https://www.anthropic.com/news/activating-asl3-protections

> The RSP states Anthropic will pause scaling or restrict deployment if a model crosses a Capability Threshold before the corresponding Required Safeguards are in place.
> Source: https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Gap assessment:** none, bar met

**Confidence:** 92%

---

### Security / Weight Protection (strong)

**Bar:** Public commitment to model-weight security commensurate with capability (preventing theft by non-state / state actors).

**Framework source:** https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Evidence (public claims):**
> Anthropic activated ASL-3 deployment and security standards for Claude Opus 4, citing CBRN uplift potential, including misuse filtering and weight-protection controls.
> Source: https://www.anthropic.com/news/activating-asl3-protections

> The RSP commits to model-weight security measures commensurate with capability, intended to resist theft by sophisticated non-state and eventually state-level actors at higher ASLs.
> Source: https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Gap assessment:** none, bar met

**Confidence:** 90%

---

### Capability Evaluations & Red-teaming (strong)

**Bar:** Public commitment to evaluate models for dangerous capabilities (CBRN, cyber, autonomy) BEFORE and DURING scaling, with red-team disclosure.

**Framework source:** https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Evidence (public claims):**
> Anthropic commits to running dangerous-capability evaluations (CBRN, cyber, autonomy) before and during scaling, and publishes model cards with red-team and eval results.
> Source: https://www.anthropic.com/news/anthropics-responsible-scaling-policy

> Anthropic activated ASL-3 deployment and security standards for Claude Opus 4, citing CBRN uplift potential, including misuse filtering and weight-protection controls.
> Source: https://www.anthropic.com/news/activating-asl3-protections

> Anthropic addresses agentic / autonomous use via computer-use safeguards and the RSP autonomy evaluations, with constrained deployment and oversight guidance for agentic products.
> Source: https://www.anthropic.com/news/developing-computer-use

**Gap assessment:** none, bar met

**Confidence:** 95%

---

### Pause / Stop Commitment (strong)

**Bar:** Explicit public commitment to PAUSE scaling or deployment if safeguards can't keep pace with capability. It has to be a real stop condition, written down.

**Framework source:** https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Evidence (public claims):**
> The RSP states Anthropic will pause scaling or restrict deployment if a model crosses a Capability Threshold before the corresponding Required Safeguards are in place.
> Source: https://www.anthropic.com/news/anthropics-responsible-scaling-policy

**Gap assessment:** none, bar met

**Confidence:** 95%

---

## Where the public posture falls short

- No criterion rated below `substantial` on public claims.

## Methodology & sources

Framework definition: **Anthropic Responsible Scaling Policy (ASL levels)**

- https://www.anthropic.com/news/anthropics-responsible-scaling-policy
- https://www-cdn.anthropic.com/1adf000c8f675958c2ee23805d91aaade1cd4613/responsible-scaling-policy.pdf

Ratings, lowest to highest: none, partial, substantial, strong. Each criterion is scored on whether the company's *public claims* meet the framework's *bar*, the specific, citable threshold above. Evidence quotes link to public sources so every claim in this report is independently checkable.

_Generated by [AGI Readiness Auditor](https://github.com/jddavenportOpen/agi-readiness-auditor)._
