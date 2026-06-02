# AGI Readiness Gap Report — OpenAI

**Framework:** OpenAI 5 Levels of AGI  
**Date:** 2026-06-02  
**Public-claim coverage score:** 53/100 _(share of framework bars met by public claims)_  
**Analysis method:** LLM (claim→criterion mapping)  
**Claims analyzed:** 8

> **Scope:** This audits a company's PUBLIC, stated posture — blog posts, frameworks, model/system cards, public statements. It does **not** measure internal practice or whether claims are honored. A high score means the public story is complete, not that the company is safe.

## Summary

| Criterion | Rating | Confidence | Method |
|---|---|---|---|
| Level 1 — Chatbots | 🟢 strong | 95% | llm |
| Level 2 — Reasoners | 🟡 substantial | 75% | llm |
| Level 3 — Agents | 🟠 partial | 75% | llm |
| Level 4 — Innovators | 🟠 partial | 75% | llm |
| Level 5 — Organizations | 🟠 partial | 75% | llm |

## Detail

### 🟢 Level 1 — Chatbots — **strong**

**Bar:** AI with conversational language ability. Bar: ships a deployed conversational system AND documents its known limitations / failure modes publicly (e.g. a system card or usage policy).

**Framework source:** https://www.bloomberg.com/news/articles/2024-07-11/openai-sets-levels-to-track-progress-toward-superintelligent-ai

**Evidence (public claims):**
> OpenAI publishes GPT-4 / GPT-4o / o-series system cards documenting capabilities, evaluations, and known limitations including hallucination and jailbreak susceptibility.
> — source: https://openai.com/index/gpt-4o-system-card/

> OpenAI's o1 system card reports chain-of-thought reasoning evaluations and notes the model can still produce confident errors; reasoning reliability is evaluated but not guaranteed.
> — source: https://openai.com/index/openai-o1-system-card/

**Gap assessment:** none — bar met

**Confidence:** 95%

---

### 🟡 Level 2 — Reasoners — **substantial**

**Bar:** Human-level problem solving across domains without tools. Bar: publicly claims reasoning-class models AND publishes evaluations of reasoning reliability, hallucination, or where the reasoning breaks.

**Framework source:** https://www.bloomberg.com/news/articles/2024-07-11/openai-sets-levels-to-track-progress-toward-superintelligent-ai

**Evidence (public claims):**
> OpenAI's o1 system card reports chain-of-thought reasoning evaluations and notes the model can still produce confident errors; reasoning reliability is evaluated but not guaranteed.
> — source: https://openai.com/index/openai-o1-system-card/

**Gap assessment:** Claim [1] establishes reasoning-class models (o1) with evaluations of reasoning reliability and where reasoning breaks ('confident errors'), but lacks explicit cross-domain human-level problem solving without tools and does not comprehensively address hallucination in reasoning contexts; other claims address unrelated frameworks (Preparedness, agents, AGI planning) rather than the Level 2 reasoning bar.

**Confidence:** 75%

---

### 🟠 Level 3 — Agents — **partial**

**Bar:** Systems that can take actions over extended time on a user's behalf. Bar: publicly addresses agentic risk — autonomy controls, action-space limits, oversight / human-in-the-loop, or a stated policy on autonomous action.

**Framework source:** https://www.bloomberg.com/news/articles/2024-07-11/openai-sets-levels-to-track-progress-toward-superintelligent-ai

**Evidence (public claims):**
> OpenAI's Preparedness Framework tracks Cybersecurity, CBRN, Persuasion, and Model Autonomy as risk categories, each scored Low/Medium/High/Critical with deployment gated above High.
> — source: https://openai.com/index/updating-our-preparedness-framework/

> OpenAI ships agentic products (Operator, agent mode) and states it applies oversight, confirmation steps, and constrained action spaces, but publishes limited detail on autonomous-action stop conditions.
> — source: https://openai.com/index/introducing-operator/

**Gap assessment:** While OpenAI acknowledges agentic products with 'oversight, confirmation steps, and constrained action spaces' [5] and tracks 'Model Autonomy' as a risk category in its Preparedness Framework [2], there is no published detail on autonomous-action stop conditions, specific autonomy controls, or a stated policy on limits of autonomous action—claim [5] explicitly notes 'limited detail on autonomous-action stop conditions' and no claim specifies thresholds for agentic risk gating or human-in-the-loop requirements for agentic systems.

**Confidence:** 75%

---

### 🟠 Level 4 — Innovators — **partial**

**Bar:** AI that can aid in invention / generate novel science. Bar: has a public position on AI-driven R&D acceleration risk, including dual-use scientific knowledge (e.g. bio/chem uplift).

**Framework source:** https://www.bloomberg.com/news/articles/2024-07-11/openai-sets-levels-to-track-progress-toward-superintelligent-ai

**Evidence (public claims):**
> OpenAI's Preparedness Framework tracks Cybersecurity, CBRN, Persuasion, and Model Autonomy as risk categories, each scored Low/Medium/High/Critical with deployment gated above High.
> — source: https://openai.com/index/updating-our-preparedness-framework/

> On Innovators-level / scientific uplift, OpenAI's CBRN track addresses bio uplift to novices, but there is no standalone public framework for AI-accelerated R&D risk beyond the CBRN category.
> — source: https://openai.com/index/updating-our-preparedness-framework/

**Gap assessment:** CBRN track addresses bio uplift to novices but lacks a standalone public position on AI-driven R&D acceleration risk broadly, including dual-use scientific knowledge beyond CBRN (e.g., chemistry, materials science, other domains) and no specific threshold or stop-condition for Innovators-level scientific invention capabilities.

**Confidence:** 75%

---

### 🟠 Level 5 — Organizations — **partial**

**Bar:** AI that can do the work of an entire organization. Bar: has a public governance position on highly autonomous / economically transformative systems — control, alignment guarantees, or a stated stop/pause condition.

**Framework source:** https://www.bloomberg.com/news/articles/2024-07-11/openai-sets-levels-to-track-progress-toward-superintelligent-ai

**Evidence (public claims):**
> OpenAI's Preparedness Framework tracks Cybersecurity, CBRN, Persuasion, and Model Autonomy as risk categories, each scored Low/Medium/High/Critical with deployment gated above High.
> — source: https://openai.com/index/updating-our-preparedness-framework/

> OpenAI's Safety Advisory Group (SAG) reviews Preparedness scorecards and can recommend the leadership block deployment; the board retains oversight authority.
> — source: https://openai.com/index/updating-our-preparedness-framework/

> OpenAI's 'Planning for AGI and Beyond' commits in principle to caution and coordination as systems approach transformative capability, but the most concrete stop conditions are tied to Preparedness thresholds rather than the Level 5 'organizations' tier.
> — source: https://openai.com/index/planning-for-agi-and-beyond/

**Gap assessment:** The Preparedness Framework gates deployment at 'Critical' risk levels and the Safety Advisory Group can recommend blocks, but no public claim specifies a governance position, control mechanism, alignment guarantee, or stop/pause condition explicitly tied to AI systems capable of performing the work of an entire organization (Level 5); the 'Planning for AGI and Beyond' commitment to caution remains principled rather than operationalized for this tier.

**Confidence:** 75%

---

## Where the public posture falls short

- **Level 3 — Agents** (partial): While OpenAI acknowledges agentic products with 'oversight, confirmation steps, and constrained action spaces' [5] and tracks 'Model Autonomy' as a risk category in its Preparedness Framework [2], there is no published detail on autonomous-action stop conditions, specific autonomy controls, or a stated policy on limits of autonomous action—claim [5] explicitly notes 'limited detail on autonomous-action stop conditions' and no claim specifies thresholds for agentic risk gating or human-in-the-loop requirements for agentic systems.
- **Level 4 — Innovators** (partial): CBRN track addresses bio uplift to novices but lacks a standalone public position on AI-driven R&D acceleration risk broadly, including dual-use scientific knowledge beyond CBRN (e.g., chemistry, materials science, other domains) and no specific threshold or stop-condition for Innovators-level scientific invention capabilities.
- **Level 5 — Organizations** (partial): The Preparedness Framework gates deployment at 'Critical' risk levels and the Safety Advisory Group can recommend blocks, but no public claim specifies a governance position, control mechanism, alignment guarantee, or stop/pause condition explicitly tied to AI systems capable of performing the work of an entire organization (Level 5); the 'Planning for AGI and Beyond' commitment to caution remains principled rather than operationalized for this tier.

## Methodology & sources

Framework definition: **OpenAI 5 Levels of AGI**

- https://www.bloomberg.com/news/articles/2024-07-11/openai-sets-levels-to-track-progress-toward-superintelligent-ai
- https://openai.com/index/planning-for-agi-and-beyond/

Ratings: 🔴 none · 🟠 partial · 🟡 substantial · 🟢 strong. Each criterion is scored on whether the company's *public claims* meet the framework's *bar* — the specific, citable threshold above. Evidence quotes link to public sources so every claim in this report is independently checkable.

_Generated by [AGI Readiness Auditor](https://github.com/JDDavenport/agi-readiness-auditor)._
