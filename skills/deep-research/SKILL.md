---
name: deep-research
description: >-
  Perform thorough source-backed investigations using available tools
  and files. Use when a request needs sustained investigation, source
  comparison, or evidence-backed recommendations.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: research
  tags: [research, investigation, sources, analysis, evidence]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: deep-research
    summary: Sustained, source-backed investigation with compared evidence
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Deep Research

## When to use

Activate when a request requires more than a single-file lookup —
cross-referencing multiple sources, comparing implementations,
evaluating trade-offs, or building an evidence-backed recommendation.
Use for architecture evaluations, library comparisons, security
investigations, or any task where the answer depends on synthesizing
multiple inputs.

## Procedure

1. Decompose the question into sub-questions. List what you need to
   know before you can answer the whole.
2. For each sub-question, identify the best available source: local
   code, documentation, test output, web search, or API probes.
3. Gather evidence from each source. Record the source URL, file
   path, or command that produced each piece of evidence.
4. Compare sources against each other. Note agreements and
   contradictions. When sources conflict, prefer primary sources.
5. Synthesize findings into a structured answer: key findings,
   supporting evidence per finding, conflicting evidence, and the
   confidence level.
6. Provide a recommendation only if evidence is sufficient. If not,
   state what is missing and what would close the gap.

## Guardrails

- Do not present a single source as consensus. Triangulate.
- Do not omit contradictory evidence. Surface it and explain the
  discrepancy.
- Do not cite a source you have not read. Summaries of summaries are
  not evidence.
- Do not extend a recommendation beyond what the evidence supports.

## Examples

### Good

> Question: which queue library fits our throughput needs? Sources:
> local benchmark of three libraries, library docs, issue tracker.
> Findings: library A is fastest but has an open issue about message
> loss under load. Recommendation: library B, with evidence and
> confidence level attached.

### Bad

> "Library A is the best choice based on its README." No benchmark,
> no comparison, no issue tracker consulted.

## Verification

- Each finding has at least one cited source.
- Contradictions between sources are explicitly noted.
- The recommendation, if given, is supported by at least two
  independent sources.
- The confidence level reflects the strength of the evidence.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/deep-research
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: deep-research
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/deep-research/raw -o .cursor/skills/deep-research/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/deep-research.md and install it as a project skill at skills/deep-research/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
