---
name: bigquery-development
description: >-
  BigQuery development patterns: query optimization, partitioning, clustering, materialized views, and cost management. Use when writing or optimizing SQL for BigQuery.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: data
  tags: [bigquery, sql, partitioning, clustering, cost-optimization]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: bigquery-development
    summary: BigQuery query optimization and cost management
  derived_from:
    - name: developing-with-bigquery
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# BigQuery Development

## When to use

Activate when writing, reviewing, or optimizing SQL for BigQuery. Use when queries are slow, expensive, or scanning too much data.

## Procedure

1. Check query cost with EXPLAIN or bytes processed.
2. Filter on partition columns first to prune partitions.
3. Add clustering on columns used in WHERE, GROUP BY, or JOIN.
4. Replace repeated subqueries with materialized views.
5. Avoid SELECT *. Name columns explicitly.
6. Use WITH (CTEs) for readability.
7. Verify with EXPLAIN ANALYZE that bytes processed is within budget.

## Guardrails

- Do not run SELECT * on large tables. Always project specific columns.
- Do not skip partition filters. Set require_partition_filter = true.
- Do not use cross-joins without a join condition.
- Do not create materialized views that refresh too frequently.

## Examples

### Good

> Query filters on partition_date, selects 4 of 30 columns, uses a materialized view. Bytes: 50 MB. Time: 2 seconds.

### Bad

> SELECT * FROM huge_table with no partition filter. Bytes: 2 TB. Cost: $10 per run.

## Verification

- EXPLAIN ANALYZE shows bytes processed within budget.
- Partition pruning is active.
- No SELECT * on tables larger than 1 GB.
- Materialized views refresh at an appropriate interval.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/bigquery-development
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: bigquery-development
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/bigquery-development/raw -o .cursor/skills/bigquery-development/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/bigquery-development.md and install it as a project skill at skills/bigquery-development/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```