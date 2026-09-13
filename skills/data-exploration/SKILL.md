---
name: data-exploration
description: >-
  Profile and explore datasets to understand shape, quality, and patterns. Use when encountering a new dataset, validating data quality, or preparing for analysis.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: data
  tags: [data, exploration, profiling, quality, patterns]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: data-exploration
    summary: Profile and explore datasets before analysis
  derived_from:
    - name: cowork-explore-data-analyze-validate
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Data Exploration

## When to use

Activate when encountering a new dataset for the first time, validating data quality, or preparing for deeper analysis.

## Procedure

1. Load the dataset and report basic stats: row count, column count, column types, memory size.
2. Check for missing values: null rate per column, patterns in missingness.
3. Compute summary statistics: mean, median, std, min, max, quartiles for numerics; frequency for categoricals.
4. Detect duplicates: exact row duplicates and near-duplicates on key columns.
5. Identify outliers: z-score or IQR method for numerics, rare categories for categoricals.
6. Check distributions: histogram for numerics, bar chart for categoricals.
7. Report findings: data shape, quality issues, interesting patterns, and recommendations for cleaning.

## Guardrails

- Do not skip the null check. Missing data affects every downstream analysis.
- Do not assume column types are correct. Verify and cast.
- Do not load the entire dataset into memory for profiling. Sample if needed.
- Do not report statistics without context. Flag what is surprising.

## Examples

### Good

> Profiled a 50k-row dataset: found 3 columns with 15% nulls, 200 duplicate rows, a bimodal distribution in the revenue column, and a suspicious outlier in age (value 999). Report recommends cleaning steps.

### Bad

> Loaded the dataset, printed df.describe(), and said it looks fine. No null check, no duplicate check, no distribution analysis.

## Verification

- Basic stats (row count, column types, memory) are reported.
- Null rates per column are documented.
- Duplicates are identified and counted.
- Outliers and distribution patterns are noted.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/data-exploration
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: data-exploration
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/data-exploration/raw -o .cursor/skills/data-exploration/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/data-exploration.md and install it as a project skill at skills/data-exploration/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```