# AGI Readiness Auditor

The big AI labs publish frameworks for how they'll handle more capable models: OpenAI's Preparedness Framework, Anthropic's Responsible Scaling Policy, Google DeepMind's Frontier Safety Framework. I wanted to check what each lab says in public against those frameworks, including each other's, with a quote and a source behind every finding.

This is a Python CLI that does that. You pick a company and a framework. It gathers the company's public claims (from a bundled set or from URLs you give it), maps each claim to a criterion in the framework, and writes a markdown gap report. Every rating comes with the quote it rests on and the link to check it.

```bash
git clone https://github.com/jddavenportOpen/agi-readiness-auditor.git
cd agi-readiness-auditor
python -m agi_auditor --company "OpenAI" --framework openai-5-levels --no-llm
```

That runs offline on the Python standard library. Add an LLM key (below) for better mapping.

> **Scope & honesty.** This audits *public claims*, not internal reality. A high
> score means the public story is *complete against the chosen framework*, not
> that the company is safe, and not that it honors its commitments. Every finding
> cites a source URL so you can verify it yourself. This is a starting point for a
> conversation, not a verdict.

Scores also depend on the framework you pick. Anthropic scores 26/100 against OpenAI's Preparedness rubric mostly because its public writing is organized around its own RSP categories.

Moved here from my private working repo in July 2026. Most of this code was written by Claude Code agents I run. I pick what gets built, set the tests it has to pass, and check it by using it.

## Sample results

All six bundled labs against the DeepMind Frontier Safety Framework, using the offline keyword analyzer (`examples/comparison-all-labs-deepmind-fsf.md`):

| Company | Coverage score |
|---|---|
| Google | 86/100 |
| Anthropic | 73/100 |
| xAI | 53/100 |
| OpenAI | 40/100 |
| Microsoft | 40/100 |
| Meta | 40/100 |

The keyword analyzer is rough. Read it as "how much of this framework the bundled quotes touch", and read the evidence before quoting a number anywhere.

## What it does

1. **Encodes real, citable frameworks** as rubrics. Each criterion has a `bar`
   (the specific threshold a company must publicly meet) and a `source` URL.
2. **Gathers public claims** from a bundled corpus (offline, deterministic) or
   by fetching live public URLs you supply (`--url`).
3. **Maps claims to criteria** with an LLM that cites only the claims it was given,
   by index, so it can't make up a quote. With no LLM key it falls back to a
   keyword analyzer, so it always produces a report.
4. **Writes a markdown gap report** with a summary table, per-criterion evidence,
   the gaps, a coverage score, and full source links.

## Frameworks included

| id | framework | criteria | source |
|---|---|---|---|
| `anthropic-rsp` | Anthropic Responsible Scaling Policy (ASL levels) | 5 | [Anthropic](https://www.anthropic.com/news/anthropics-responsible-scaling-policy) |
| `deepmind-fsf` | Google DeepMind Frontier Safety Framework (eval schedules, CBRN, oversight, autonomy, deployment gates) | 5 | [DeepMind, May 2024](https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/) |
| `openai-5-levels` | OpenAI 5 Levels of AGI (Chatbots, Reasoners, Agents, Innovators, Organizations) | 5 | [Bloomberg, Jul 2024](https://www.bloomberg.com/news/articles/2024-07-11/openai-sets-levels-to-track-progress-toward-superintelligent-ai) |
| `openai-preparedness` | OpenAI Preparedness Framework (cyber, CBRN, persuasion, autonomy, governance) | 5 | [OpenAI](https://openai.com/index/updating-our-preparedness-framework/) |

Frameworks are plain JSON in `agi_auditor/frameworks/`. Add your own composite rubric by dropping in a file and registering it.

## Bundled corpora

Bundled offline corpora for **Anthropic, Google, Meta, Microsoft, OpenAI and xAI**. Use any as `--company` or in `--compare`.

```
python -m agi_auditor --list-corpus
```

## Install

```bash
git clone https://github.com/jddavenportOpen/agi-readiness-auditor.git
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

The claim-to-criterion mapping calls any endpoint that speaks the **Anthropic Messages API**.
I ran the examples on Kimi, so the variables are named for it. Set two env vars, or put them
in a `.env` file in the directory you run from:

```bash
export KIMI_API_KEY=...        # your key, never logged or echoed
export KIMI_BASE_URL=https://api.kimi.com/coding
# optional: export AGI_AUDITOR_MODEL=kimi-k2-0905-preview
```

It POSTs to `{KIMI_BASE_URL}/v1/messages` with `x-api-key` + `anthropic-version: 2023-06-01`.
To use Anthropic directly, set `KIMI_BASE_URL=https://api.anthropic.com`, your Anthropic key,
and `AGI_AUDITOR_MODEL` to a Claude model id. With no key set, it uses the keyword analyzer.

## Sample report excerpt

From `examples/openai-5-levels.md` (OpenAI against its own 5 Levels, LLM mapping, coverage **53/100**):

> ### Level 5: Organizations (partial)
> **Bar:** AI that can do the work of an entire organization. Bar: a public
> governance position on highly autonomous / economically transformative systems:
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
- [`anthropic-vs-openai-preparedness.md`](examples/anthropic-vs-openai-preparedness.md): Anthropic held to OpenAI's rubric (26/100). Its public writing follows its own RSP categories, so it maps poorly onto OpenAI's. Scores only mean something relative to the framework.

## How a rating is decided

Each criterion gets one of `none`, `partial`, `substantial` or `strong`.

- **strong**: the bar is clearly and specifically met by a cited public claim.
- **substantial**: mostly met but missing specificity (e.g. no named threshold).
- **partial**: topic acknowledged, but the bar's key element (a stated threshold,
  stop-condition, or named governing body) is absent.
- **none**: no public claim addresses the criterion.

The **coverage score** (0 to 100) is the average credit across criteria. It measures
*completeness of the public story against the chosen framework*, nothing more.

## Limitations (read these)

- **Public claims only.** It cannot see internal practice, unpublished evals, or
  whether commitments are actually honored. A complete public story can still mask
  a weak internal one, and a terse public story can hide strong internal practice.
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

## License

MIT. See [LICENSE](LICENSE).
