# AGI Readiness Auditor

**Pressure-test the public AGI-safety story.** A Python CLI that takes a company's
**public** AI-safety claims — blog posts, safety frameworks, model/system cards,
public statements — and diffs them against a published readiness framework
(OpenAI's *5 Levels of AGI*, OpenAI's *Preparedness Framework*, Anthropic's
*Responsible Scaling Policy*, or Google DeepMind's *Frontier Safety Framework*).
It auto-generates a **gap report**: per-criterion, where the company's stated
posture *meets* the framework's bar vs *falls short* — with the evidence quote,
a gap assessment, and a confidence score. Compare multiple labs side-by-side
with `--compare`.

The point: the big labs publish AGI-readiness frameworks. This tool holds them
(and anyone else) to those same published bars, **on the public record, checkably.**

> **Scope & honesty.** This audits *public claims*, not internal reality. A high
> score means the public story is *complete against the chosen framework* — not
> that the company is safe, and not that it honors its commitments. Every finding
> cites a source URL so you can verify it yourself. This is a starting point for a
> conversation, not a verdict.

## What it does

1. **Encodes real, citable frameworks** as rubrics — each criterion has a `bar`
   (the specific threshold a company must publicly meet) and a `source` URL.
2. **Gathers public claims** — from a bundled corpus (offline, deterministic) or
   by fetching live public URLs you supply (`--url`).
3. **Maps claims → criteria** with an LLM (skeptical, evidence-bound, cites only
   provided claims by index — never invents quotes). Falls back to a deterministic
   keyword analyzer if no LLM key is configured, so it *always* produces a report.
4. **Renders a markdown gap report** with a summary table, per-criterion evidence,
   the gaps, a coverage score, and full source links.

## Frameworks included

| id | framework | criteria | source |
|---|---|---|---|
| `anthropic-rsp` | Anthropic Responsible Scaling Policy (ASL levels) | 5 | [Anthropic](https://www.anthropic.com/news/anthropics-responsible-scaling-policy) |
| `deepmind-fsf` | Google DeepMind Frontier Safety Framework (eval schedules, CBRN, oversight, autonomy, deployment gates) | 5 | [DeepMind, May 2024](https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/) |
| `openai-5-levels` | OpenAI 5 Levels of AGI (Chatbots→Reasoners→Agents→Innovators→Organizations) | 5 | [Bloomberg, Jul 2024](https://www.bloomberg.com/news/articles/2024-07-11/openai-sets-levels-to-track-progress-toward-superintelligent-ai) |
| `openai-preparedness` | OpenAI Preparedness Framework (cyber, CBRN, persuasion, autonomy, governance) | 5 | [OpenAI](https://openai.com/index/updating-our-preparedness-framework/) |

Frameworks are plain JSON in `agi_auditor/frameworks/` — add your own composite rubric by dropping in a file and registering it.

## Bundled corpora

Bundled offline corpora for: **Anthropic, Google, Meta, Microsoft, OpenAI, xAI** — use any as `--company` or in `--compare`.

```
python -m agi_auditor --list-corpus
```

## Install

```bash
git clone https://github.com/JDDavenport/agi-readiness-auditor.git
cd agi-readiness-auditor
pip install -r requirements.txt   # only needed for live --url fetching
```

The core (bundled-corpus + deterministic analysis) needs **only the Python
standard library**. `requirements.txt` (`requests`, `beautifulsoup4`) is for live
URL fetching.

## Run

```bash
# Audit OpenAI against its own 5-levels framework (bundled corpus):
python -m agi_auditor --company "OpenAI" --framework openai-5-levels

# Anthropic against its RSP, write to a file:
python -m agi_auditor --company "Anthropic" --framework anthropic-rsp -o report.md

# Cross-audit: Anthropic held to OpenAI's Preparedness framework:
python -m agi_auditor --company "Anthropic" --framework openai-preparedness

# Compare all 6 major labs side-by-side on the same rubric:
python -m agi_auditor --compare "openai,anthropic,google,microsoft,meta,xai" \
    --framework openai-preparedness -o comparison.md

# Compare on the DeepMind FSF rubric:
python -m agi_auditor --compare "openai,anthropic,google,microsoft,meta,xai" \
    --framework deepmind-fsf -o comparison-fsf.md

# Audit any company from live public URLs:
python -m agi_auditor --company "Acme AI" --framework openai-preparedness \
    --url https://acme.ai/safety --url https://acme.ai/blog/preparedness

# Force the deterministic analyzer (no LLM):
python -m agi_auditor --company "OpenAI" --framework openai-5-levels --no-llm

python -m agi_auditor --list-frameworks
python -m agi_auditor --list-corpus
```

### LLM configuration (optional but recommended)

The claim→criterion mapping uses an LLM. **Anthropic Claude is the primary backend.**
Set your API key (or put it in `~/agent-system/.env`, which the CLI auto-reads):

```bash
# Anthropic (primary — recommended)
export ANTHROPIC_API_KEY=sk-ant-...

# Kimi (alternative — same Anthropic Messages shape)
export KIMI_API_KEY=...
export KIMI_BASE_URL=https://api.kimi.com/coding
```

The CLI auto-discovers the right backend based on which keys are set: Anthropic first,
Kimi second. **No key configured → deterministic fallback**, so the tool runs anywhere.

Use `--model` to pick a specific model:

```bash
# Default (Sonnet, best quality)
python -m agi_auditor --company "OpenAI" --framework openai-5-levels

# Faster/cheaper with Haiku
python -m agi_auditor --company "OpenAI" --framework openai-5-levels \
    --model claude-haiku-4-5-20251001

# Kimi explicitly
python -m agi_auditor --company "OpenAI" --framework openai-5-levels \
    --model kimi-k2-0905-preview

# Skip LLM entirely
python -m agi_auditor --company "OpenAI" --framework openai-5-levels --no-llm
```

## Sample report excerpt

From `examples/openai-5-levels.md` (OpenAI vs its own 5 Levels — coverage **53/100**):

> ### 🟠 Level 5 — Organizations — **partial**
> **Bar:** AI that can do the work of an entire organization. Bar: a public
> governance position on highly autonomous / economically transformative systems —
> control, alignment guarantees, or a stated stop/pause condition.
>
> **Gap assessment:** The Preparedness Framework gates deployment at 'Critical' risk
> and the Safety Advisory Group can recommend blocks, but no public claim specifies a
> governance position, control mechanism, alignment guarantee, or stop/pause condition
> explicitly tied to AI systems capable of performing the work of an entire
> organization (Level 5); the 'Planning for AGI and Beyond' commitment to caution
> remains principled rather than operationalized for this tier.

See [`examples/`](examples/) for full reports:
- [`openai-5-levels.md`](examples/openai-5-levels.md)
- [`openai-preparedness.md`](examples/openai-preparedness.md)
- [`anthropic-rsp.md`](examples/anthropic-rsp.md)
- [`anthropic-vs-openai-preparedness.md`](examples/anthropic-vs-openai-preparedness.md) — Anthropic held to OpenAI's rubric (26/100 — *not because Anthropic is less safe, but because its public posture is structured around its own RSP categories, not OpenAI's*). This is the honest caveat the tool is built around: **scores are framework-relative.**

## How a rating is decided

Each criterion gets one of: 🔴 `none` · 🟠 `partial` · 🟡 `substantial` · 🟢 `strong`.

- **strong** — the bar is clearly and specifically met by a cited public claim.
- **substantial** — mostly met but missing specificity (e.g. no named threshold).
- **partial** — topic acknowledged, but the bar's key element (a stated threshold,
  stop-condition, or named governing body) is absent.
- **none** — no public claim addresses the criterion.

The **coverage score** (0–100) is the average credit across criteria. It measures
*completeness of the public story against the chosen framework* — nothing more.

## Limitations (read these)

- **Public claims only.** It cannot see internal practice, unpublished evals, or
  whether commitments are actually honored. A complete public story can still mask
  a weak internal one — and a terse public story can hide strong internal practice.
- **Framework-relative.** A company scores differently against different rubrics by
  design. A low cross-audit score is a *mapping* result, not a safety verdict.
- **Corpus-bound.** With the bundled corpus, results reflect the specific quotes
  included. For a real audit, feed comprehensive `--url` sources. The bundled
  corpora are illustrative starting sets, not exhaustive.
- **LLM judgment.** The mapping is a language-model assessment; confidence scores
  are the model's, not ground truth. Always read the evidence quotes and verify
  against the linked sources before citing externally.
- **Frameworks evolve.** OpenAI's and Anthropic's documents get revised; the
  encoded bars reflect the cited versions. Check the source URLs for current text.

## Web API (hosted)

**Live:** [agi-readiness-auditor.vercel.app](https://agi-readiness-auditor.vercel.app)

The hosted version exposes a FastAPI backend:

| Endpoint | Method | Description |
|---|---|---|
| `/api/frameworks` | GET | List available frameworks |
| `/api/corpus` | GET | List bundled company corpora |
| `/api/audit` | POST | Audit a company against a framework |
| `/api/compare` | POST | Compare multiple companies side-by-side |

Example:
```bash
# Audit Anthropic against its own RSP
curl -X POST https://agi-readiness-auditor.vercel.app/api/audit \
  -H "Content-Type: application/json" \
  -d '{"company":"anthropic","framework":"anthropic-rsp","no_llm":true}'
```

### Self-host with Railway or any platform

```bash
# Local dev
pip install -r requirements.txt
uvicorn api.app:app --reload

# Railway: push to GitHub and connect at railway.app
# The Procfile and railway.toml configure the start command automatically.
# Set ANTHROPIC_API_KEY in environment variables to enable LLM analysis.
```

## License

MIT — see [LICENSE](LICENSE).
