---
name: data-quality
description: >-
  Data quality assessment and cleaning. Profile datasets, detect anomalies, and automate quality checks. Use when onboarding new data sources or setting up continuous quality monitoring.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: data
  tags: [data-quality, profiling, anomalies, cleaning, validation]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: data-quality
    summary: Profile, clean, and monitor dataset quality
  derived_from:
    - name: data-autocleaning
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Data Quality

## When to use

Activate when onboarding a new data source, setting up quality monitoring, or investigating data issues downstream.

## Procedure

1. Profile the dataset: row count, column types, null rates, unique values, min/max.
2. Detect anomalies: statistical outliers, unexpected nulls, type mismatches, duplicates.
3. Classify: hard errors, soft warnings, informational.
4. Write cleaning rules: impute or drop nulls, clip outliers, fix types, deduplicate.
5. Automate as tests: Great Expectations, dbt tests, or custom SQL.
6. Report: pass/fail per check and rows affected.

## Guardrails

- Do not silently drop rows. Log every dropped or modified row with the reason.
- Do not apply cleaning rules without profiling first.
- Do not hardcode thresholds without documentation.
- Do not skip referential integrity checks.

## Examples

### Good

> Profiled 50k rows: found 2% nulls, 15 duplicates, 200 outliers. Cleaned with documented rules, wrote 8 dbt tests. Report shows 0 hard errors.

### Bad

> Dropped all rows with nulls, clipped age to 18-65 without checking distribution. No tests. Downstream shows 30% fewer rows.

## Verification

- Quality report shows zero hard errors after cleaning.
- Every cleaning rule is documented.
- Automated tests run in CI and fail on regression.
- Row-level log of changes is available.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/data-quality
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: data-quality
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/data-quality/raw -o .cursor/skills/data-quality/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/data-quality.md and install it as a project skill at skills/data-quality/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```