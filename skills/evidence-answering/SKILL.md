---
name: evidence-answering
description: >-
  Ensure responses and decisions are evidence-governed when making claims
  about Vidoxlabs systems. Use when producing conclusions, recommendations,
  or documentation that will be treated as canonical. Require citations,
  links, or artifacts to support each claim.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: docs
  tags: [docs, evidence, citations, guardrails]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: evidence-answering
    summary: Require evidence for claims about Vidoxlabs systems.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Evidence-Governed Answering

## When to use

Use this skill when producing conclusions, recommendations, or changes
that affect operational or engineering truth. Also use when writing
documentation that will be treated as canonical.

## Procedure

1. Identify what claims are being made in the answer or decision.
2. Find sources that support each claim — internal docs, logs, code, or
   test output.
3. If evidence is weak or missing, state the uncertainty explicitly and
   propose the minimum verification step needed.
4. Record sources inline as links or citations in the output.

## Guardrails

- Do not present guesses as facts.
- Prefer "unknown / needs verification" over fabrication.
- A job-description quote can never support an applicant claim.
- Do not skip the evidence step for high-impact claims even when the
  answer seems obvious.

## Examples

### Good

> Based on the [Workers AI model catalog](https://developers.cloudflare.com/workers-ai/models/)
> (retrieved 2026-09-12) and the public repository README, the deployment
> uses `@cf/meta/llama-4-scout-17b-16e-instruct`; verified against the
> official model page, not inferred from a chat answer.

### Bad

> The system does Z. (no source, no link, no verification)

## Verification

- Spot-check at least one primary source for any high-impact claim.
- Confirm links resolve and the cited content actually supports the
  claim as stated.

## Install

Repository installers (`npx skills add`, Claude marketplace) are not advertised for this revision: they follow GitHub default `main`, which is not this curated set.

```bash
curl -fsSL https://vidoxlabs.dev/vitools/raw/skills/evidence-answering.md -o .cursor/skills/evidence-answering/SKILL.md
```

```text
Fetch https://vidoxlabs.dev/vitools/raw/skills/evidence-answering.md and install it as a project skill at skills/evidence-answering/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
