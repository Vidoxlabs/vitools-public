---
name: bigquery-dbt
description: >-
  Use dbt with BigQuery for transformation pipelines. Models, tests, seeds, and snapshots. Use when building or maintaining a dbt project on BigQuery.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: data
  tags: [dbt, bigquery, transformations, models, testing]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: bigquery-dbt
    summary: dbt transformation pipelines on BigQuery
  derived_from:
    - name: dbt-bigquery
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# BigQuery dbt

## When to use

Activate when building or maintaining a dbt project on BigQuery. Use when creating models, writing tests, or setting up snapshots.

## Procedure

1. Initialize: dbt init. Configure profiles.yml with BigQuery adapter.
2. Define sources in sources.yml with descriptions and freshness checks.
3. Build staging models (stg_) that select and rename from sources.
4. Build intermediate models (int_) for business logic.
5. Build mart models (fct_, dim_) for downstream queries.
6. Write tests: unique, not_null, relationships, custom SQL.
7. Run: dbt run, dbt test, or dbt build.
8. Add snapshots for slowly changing dimensions.

## Guardrails

- Do not query sources directly in mart models. Always go through staging.
- Do not skip tests on primary keys. unique and not_null are minimum.
- Do not use persistent materializations without a refresh schedule.
- Do not hardcode project or dataset IDs. Use variables.

## Examples

### Good

> Staging casts types, intermediate joins orders and users, mart aggregates revenue. Tests on order_id (unique, not_null). dbt build passes.

### Bad

> Mart model directly queries a raw source. No tests. Dataset ID hardcoded to dev project. Production fails.

## Verification

- dbt build completes with zero errors.
- All primary keys have unique and not_null tests.
- No mart model references a source directly.
- Environments use different datasets via variables.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/bigquery-dbt
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: bigquery-dbt
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/bigquery-dbt/raw -o .cursor/skills/bigquery-dbt/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/bigquery-dbt.md and install it as a project skill at skills/bigquery-dbt/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```