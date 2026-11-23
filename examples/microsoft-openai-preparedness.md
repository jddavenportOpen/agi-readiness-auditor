# AGI Readiness Gap Report: microsoft

**Framework:** OpenAI Preparedness Framework (Tracked Risk Categories)  
**Date:** 2026-07-03  
**Public-claim coverage score:** 33/100 _(share of framework bars met by public claims)_  
**Analysis method:** deterministic keyword fallback  
**Claims analyzed:** 7

> **Scope:** This audits a company's PUBLIC, stated posture: blog posts, frameworks, model/system cards, public statements. It does **not** measure internal practice or whether claims are honored. A high score means the public story is complete. It doesn't mean the company is safe.

## Summary

| Criterion | Rating | Confidence | Method |
|---|---|---|---|
| Cybersecurity | partial | 40% | deterministic |
| CBRN (chem / bio / radiological / nuclear) | substantial | 50% | deterministic |
| Persuasion / Influence | none | 35% | deterministic |
| Model Autonomy / Self-improvement | partial | 40% | deterministic |
| Governance & Stop Conditions | partial | 40% | deterministic |

## Detail

### Cybersecurity (partial)

**Bar:** Public position on model uplift to cyber-offensive operations, with a stated capability threshold above which deployment is gated or mitigated.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> Microsoft's Office of Responsible AI reviews AI products through a Responsible AI Impact Assessment process; high-impact and sensitive use cases require additional review before deployment.
> Source: https://www.microsoft.com/en-us/ai/responsible-ai

> Azure AI Content Safety provides configurable harm-category filters (hate, sexual, violence, self-harm) with severity levels; operators can set thresholds appropriate to their deployment context.
> Source: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/

> Microsoft's AI Red Team tests deployed models and published a 2024 report on red-teaming methodology for generative AI systems, including adversarial probing for jailbreaks and CBRN uplift.
> Source: https://www.microsoft.com/en-us/security/blog/2023/08/07/microsoft-ai-red-team-building-future-of-safer-ai/

**Gap assessment:** Only weak topical overlap; the criterion's key element appears unaddressed.

**Confidence:** 40%

---

### CBRN (chem / bio / radiological / nuclear) (substantial)

**Bar:** Public position on biological/chemical uplift, including a stated threshold (e.g. 'meaningful uplift to a novice') above which the model is restricted.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> Microsoft's AI Red Team tests deployed models and published a 2024 report on red-teaming methodology for generative AI systems, including adversarial probing for jailbreaks and CBRN uplift.
> Source: https://www.microsoft.com/en-us/security/blog/2023/08/07/microsoft-ai-red-team-building-future-of-safer-ai/

> Microsoft publishes Transparency Notes for AI features documenting intended uses, evaluated use cases, and known limitations including reliability failure modes and performance disparities.
> Source: https://learn.microsoft.com/en-us/azure/ai-services/transparency-note

**Gap assessment:** Topic addressed but no clear stated threshold/stop-condition in matched text.

**Confidence:** 50%

---

### Persuasion / Influence (none)

**Bar:** Public position on model-driven persuasion, manipulation, or influence operations, with a stated mitigation or evaluation.

**Framework source:** https://cdn.openai.com/openai-preparedness-framework-beta.pdf

**Evidence:** _none found in corpus._

**Gap assessment:** No public claim in the corpus addresses this criterion.

**Confidence:** 35%

---

### Model Autonomy / Self-improvement (partial)

**Bar:** Public position on autonomous capability (self-exfiltration, self-improvement, resource acquisition), with a stated threshold above which development is gated.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> Copilot and Azure AI agentic features (Copilot Studio agents, Semantic Kernel) include constrained tool-use, human-in-the-loop confirmation defaults, and documented action-scope policies for autonomous task execution.
> Source: https://learn.microsoft.com/en-us/semantic-kernel/overview/

**Gap assessment:** Only weak topical overlap; the criterion's key element appears unaddressed.

**Confidence:** 40%

---

### Governance & Stop Conditions (partial)

**Bar:** A named internal body (e.g. Safety Advisory Group, board) with authority to block deployment, AND a public commitment to halt/hold if a threshold is crossed.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> Azure AI Content Safety provides configurable harm-category filters (hate, sexual, violence, self-harm) with severity levels; operators can set thresholds appropriate to their deployment context.
> Source: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/

> Microsoft Responsible AI Standard v2 (2022) defines six core principles: fairness, reliability and safety, privacy and security, inclusiveness, transparency, and accountability, with detailed requirements and measurement practices for each.
> Source: https://blogs.microsoft.com/on-the-issues/2022/06/21/microsofts-responsible-ai-standard-v2-general-requirements/

> Microsoft's Office of Responsible AI reviews AI products through a Responsible AI Impact Assessment process; high-impact and sensitive use cases require additional review before deployment.
> Source: https://www.microsoft.com/en-us/ai/responsible-ai

**Gap assessment:** Only weak topical overlap; the criterion's key element appears unaddressed.

**Confidence:** 40%

---

## Where the public posture falls short

- **Cybersecurity** (partial): Only weak topical overlap; the criterion's key element appears unaddressed.
- **Persuasion / Influence** (none): No public claim in the corpus addresses this criterion.
- **Model Autonomy / Self-improvement** (partial): Only weak topical overlap; the criterion's key element appears unaddressed.
- **Governance & Stop Conditions** (partial): Only weak topical overlap; the criterion's key element appears unaddressed.

## Methodology & sources

Framework definition: **OpenAI Preparedness Framework (Tracked Risk Categories)**

- https://openai.com/index/updating-our-preparedness-framework/
- https://cdn.openai.com/openai-preparedness-framework-beta.pdf

Ratings, lowest to highest: none, partial, substantial, strong. Each criterion is scored on whether the company's *public claims* meet the framework's *bar*, the specific, citable threshold above. Evidence quotes link to public sources so every claim in this report is independently checkable.

_Generated by [AGI Readiness Auditor](https://github.com/jddavenportOpen/agi-readiness-auditor)._
