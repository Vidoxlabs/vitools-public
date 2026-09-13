---
name: data-analysis
description: >-
  Answer data questions from quick lookups to full analyses. Use when
  looking up a metric, investigating a trend, comparing segments over
  time, or preparing a data report for stakeholders.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: data
  tags: [data, analysis, metrics, trends, reporting, pandas]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: data-analysis
    summary: Answer data questions from lookups to full analyses
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Data Analysis

## When to use

Activate when the user provides data or asks about trends, patterns,
anomalies, statistics, comparisons, metrics, cohorts, rankings, or
data quality. Use for quick metric lookups or full investigative
analyses.

## Procedure

1. Understand the question. Is it a lookup (single value), a
   comparison (two or more groups), or an investigation (why did
   something change)?
2. Load the data using the appropriate tool: SQL for warehouses,
   `pandas` for files, or an API for services.
3. For lookups: query the specific metric with the right filters.
   Report the value with context (time period, segment).
4. For comparisons: compute the metric for each group, then compute
   the difference and percentage change.
5. For investigations: decompose the change into contributing factors.
   Use segmentation, time-series decomposition, or cohort analysis.
6. Sanity-check results: do the numbers make sense given domain
   knowledge? Flag anomalies.
7. Present results with the answer first, then the supporting data.

## Guardrails

- Do not report a number without its context: time period, segment,
  and unit.
- Do not conflate correlation with causation. State what the data
  shows, not why it happened, unless you have evidence for the cause.
- Do not hide uncertainty. If the data is incomplete or the sample is
  small, say so.
- Do not round in ways that obscure meaningful differences.

## Examples

### Good

> Question: "Why did revenue drop last week?" Investigation found
> revenue dropped 12% week-over-week. Decomposed by segment: the
> enterprise segment dropped 30% due to one churned account. SMB
> grew 5%. Conclusion: the drop is concentrated in one account, not
> a broad trend.

### Bad

> "Revenue went down last week." No number, no segment, no cause,
> no context.

## Verification

- The answer addresses the specific question asked.
- Numbers include time period, segment, and unit.
- Uncertainty or data quality issues are flagged.
- The conclusion is supported by the data shown.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/data-analysis
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: data-analysis
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/data-analysis/raw -o .cursor/skills/data-analysis/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/data-analysis.md and install it as a project skill at skills/data-analysis/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
