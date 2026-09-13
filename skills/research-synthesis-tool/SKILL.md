---
name: research-synthesis-tool
description: >-
  Synthesize research from multiple sources into a coherent summary with key findings, evidence, and recommendations. Use when consolidating research from multiple investigations.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: research
  tags: [research, synthesis, findings, evidence, consolidation]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: research-synthesis-tool
    summary: Synthesize research findings into coherent summaries
  derived_from:
    - name: cowork-research-synthesis
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Research Synthesis

## When to use

Activate when consolidating findings from multiple research sessions, literature reviews, or investigations into a single coherent summary.

## Procedure

1. Collect all research artifacts: notes, documents, links, and data from each session.
2. Extract key findings from each artifact. Tag by theme and confidence level.
3. Cross-reference findings: identify agreements, contradictions, and gaps.
4. Group findings by theme. Merge overlapping points. Note conflicts explicitly.
5. Write a synthesis: lead with the strongest findings, support with evidence, flag uncertainties.
6. Provide recommendations only where evidence is sufficient. Note what would close remaining gaps.
7. Cite sources for every finding.

## Guardrails

- Do not cherry-pick findings. Include contradictory evidence.
- Do not present a single source as consensus. Triangulate.
- Do not omit the confidence level. Some findings are stronger than others.
- Do not produce recommendations beyond what the evidence supports.

## Examples

### Good

> Synthesized 5 research sessions into a 3-page summary: 8 key findings grouped by theme, 2 contradictions flagged, 3 recommendations with high confidence, 2 gaps noted with what would close them.

### Bad

> Summarized 5 research sessions into a paragraph saying the topic is interesting and needs more study.

## Verification

- Every finding has at least one cited source.
- Contradictions between sources are explicitly noted.
- Confidence levels are stated for each finding.
- Recommendations are bounded by evidence strength.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/research-synthesis-tool
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: research-synthesis-tool
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/research-synthesis-tool/raw -o .cursor/skills/research-synthesis-tool/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/research-synthesis-tool.md and install it as a project skill at skills/research-synthesis-tool/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```