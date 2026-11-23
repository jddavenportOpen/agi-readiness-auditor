# AGI Readiness Gap Report: OpenAI

**Framework:** OpenAI Preparedness Framework (Tracked Risk Categories)  
**Date:** 2026-06-02  
**Public-claim coverage score:** 53/100 _(share of framework bars met by public claims)_  
**Analysis method:** LLM (claim→criterion mapping)  
**Claims analyzed:** 8

> **Scope:** This audits a company's PUBLIC, stated posture: blog posts, frameworks, model/system cards, public statements. It does **not** measure internal practice or whether claims are honored. A high score means the public story is complete. It doesn't mean the company is safe.

## Summary

| Criterion | Rating | Confidence | Method |
|---|---|---|---|
| Cybersecurity | partial | 75% | llm |
| CBRN (chem / bio / radiological / nuclear) | substantial | 75% | llm |
| Persuasion / Influence | partial | 85% | llm |
| Model Autonomy / Self-improvement | substantial | 75% | llm |
| Governance & Stop Conditions | substantial | 75% | llm |

## Detail

### Cybersecurity (partial)

**Bar:** Public position on model uplift to cyber-offensive operations, with a stated capability threshold above which deployment is gated or mitigated.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> OpenAI's Preparedness Framework tracks Cybersecurity, CBRN, Persuasion, and Model Autonomy as risk categories, each scored Low/Medium/High/Critical with deployment gated above High.
> Source: https://openai.com/index/updating-our-preparedness-framework/

**Gap assessment:** Claim [2] confirms Cybersecurity is tracked with a High/Critical gating threshold, but no public claim specifies what capability level in cyber-offensive operations triggers that gate, and no concrete threshold for 'uplift to cyber-offensive operations' is stated.

**Confidence:** 75%

---

### CBRN (chem / bio / radiological / nuclear) (substantial)

**Bar:** Public position on biological/chemical uplift, including a stated threshold (e.g. 'meaningful uplift to a novice') above which the model is restricted.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> OpenAI's Preparedness Framework tracks Cybersecurity, CBRN, Persuasion, and Model Autonomy as risk categories, each scored Low/Medium/High/Critical with deployment gated above High.
> Source: https://openai.com/index/updating-our-preparedness-framework/

> On Innovators-level / scientific uplift, OpenAI's CBRN track addresses bio uplift to novices, but there is no standalone public framework for AI-accelerated R&D risk beyond the CBRN category.
> Source: https://openai.com/index/updating-our-preparedness-framework/

**Gap assessment:** Claim [6] states CBRN addresses 'bio uplift to novices' but does not confirm this is the formal threshold for restriction gating; claim [2] confirms CBRN is tracked with High/Critical gates but omits the specific uplift threshold language required by the bar.

**Confidence:** 75%

---

### Persuasion / Influence (partial)

**Bar:** Public position on model-driven persuasion, manipulation, or influence operations, with a stated mitigation or evaluation.

**Framework source:** https://cdn.openai.com/openai-preparedness-framework-beta.pdf

**Evidence (public claims):**
> OpenAI's Preparedness Framework tracks Cybersecurity, CBRN, Persuasion, and Model Autonomy as risk categories, each scored Low/Medium/High/Critical with deployment gated above High.
> Source: https://openai.com/index/updating-our-preparedness-framework/

> OpenAI states that for Persuasion the framework was de-emphasized in the 2025 update, handled via usage policies rather than a capability gate.
> Source: https://openai.com/index/updating-our-preparedness-framework/

**Gap assessment:** While Persuasion is named as a tracked risk category, the 2025 update explicitly de-emphasized it with no capability gate, no stated mitigation specifics, and no evaluation methodology disclosed. It only hands off to usage policies.

**Confidence:** 85%

---

### Model Autonomy / Self-improvement (substantial)

**Bar:** Public position on autonomous capability (self-exfiltration, self-improvement, resource acquisition), with a stated threshold above which development is gated.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> OpenAI's Preparedness Framework tracks Cybersecurity, CBRN, Persuasion, and Model Autonomy as risk categories, each scored Low/Medium/High/Critical with deployment gated above High.
> Source: https://openai.com/index/updating-our-preparedness-framework/

**Gap assessment:** The framework names Model Autonomy as a tracked risk category with a High/Critical threshold gating deployment, but no public claim specifies what autonomous capabilities (self-exfiltration, self-improvement, resource acquisition) are evaluated, what concrete metrics define the threshold, or what self-improvement scenarios trigger the gate.

**Confidence:** 75%

---

### Governance & Stop Conditions (substantial)

**Bar:** A named internal body (e.g. Safety Advisory Group, board) with authority to block deployment, AND a public commitment to halt/hold if a threshold is crossed.

**Framework source:** https://openai.com/index/updating-our-preparedness-framework/

**Evidence (public claims):**
> OpenAI's Preparedness Framework tracks Cybersecurity, CBRN, Persuasion, and Model Autonomy as risk categories, each scored Low/Medium/High/Critical with deployment gated above High.
> Source: https://openai.com/index/updating-our-preparedness-framework/

> OpenAI's Safety Advisory Group (SAG) reviews Preparedness scorecards and can recommend the leadership block deployment; the board retains oversight authority.
> Source: https://openai.com/index/updating-our-preparedness-framework/

**Gap assessment:** Missing explicit public commitment to halt/hold with named specific threshold values; the 'High' gate is referenced but not concretely defined in public, and board authority is mentioned but not as an automatic stop mechanism.

**Confidence:** 75%

---

## Where the public posture falls short

- **Cybersecurity** (partial): Claim [2] confirms Cybersecurity is tracked with a High/Critical gating threshold, but no public claim specifies what capability level in cyber-offensive operations triggers that gate, and no concrete threshold for 'uplift to cyber-offensive operations' is stated.
- **Persuasion / Influence** (partial): While Persuasion is named as a tracked risk category, the 2025 update explicitly de-emphasized it with no capability gate, no stated mitigation specifics, and no evaluation methodology disclosed. It only hands off to usage policies.

## Methodology & sources

Framework definition: **OpenAI Preparedness Framework (Tracked Risk Categories)**

- https://openai.com/index/updating-our-preparedness-framework/
- https://cdn.openai.com/openai-preparedness-framework-beta.pdf

Ratings, lowest to highest: none, partial, substantial, strong. Each criterion is scored on whether the company's *public claims* meet the framework's *bar*, the specific, citable threshold above. Evidence quotes link to public sources so every claim in this report is independently checkable.

_Generated by [AGI Readiness Auditor](https://github.com/jddavenportOpen/agi-readiness-auditor)._
