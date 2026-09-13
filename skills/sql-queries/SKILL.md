---
name: sql-queries
description: >-
  Write correct, performant SQL across major data warehouse dialects
  (Snowflake, BigQuery, Databricks, PostgreSQL). Use when writing
  queries, optimizing slow SQL, or translating between dialects.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: data
  tags: [sql, data-warehouse, optimization, postgres, bigquery]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: sql-queries
    summary: Write and optimize SQL across Snowflake, BigQuery, Databricks, PostgreSQL
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# SQL Queries

## When to use

Activate when writing new SQL, debugging a slow query, translating a
query between dialects, or designing a schema change. Use for any task
involving Snowflake, BigQuery, Databricks, or PostgreSQL where
correctness and performance both matter.

## Procedure

1. Identify the target dialect and its version. Note syntax and
   function differences: Snowflake `QUALIFY`, BigQuery `SAFE_CAST`,
   PostgreSQL `DISTINCT ON`, Databricks `OPTIMIZE`.
2. Write the query in the target dialect's idiomatic style. Prefer
   CTEs over nested subqueries for readability.
3. Check for common correctness issues: implicit cross joins, missing
   join conditions, off-by-one in date ranges, NULL handling in
   aggregations, and timezone assumptions.
4. Review the query plan or `EXPLAIN` output if performance is a
   concern. Look for full table scans, absent join keys, and large
   shuffles.
5. Add appropriate filters early in the pipeline. Push predicates
   into CTEs and subqueries to reduce intermediate row counts.
6. If translating between dialects, map function names, quote
   identifiers per dialect rules, and verify date and timestamp
   behavior matches.
7. Test the query against a small sample before running on full
   production data.

## Guardrails

- Do not use `SELECT *` in production queries. List columns explicitly.
- Do not rely on implicit type coercion. Cast explicitly when
  comparing or concatenating.
- Do not assume NULL behaves like a value. Use `IS NULL` and
  `COALESCE` deliberately.
- Do not leave timezone-sensitive logic unspecified. State the
  timezone explicitly in date functions.
- Do not optimize before measuring. Confirm the query is slow before
  rewriting it.

## Examples

### Good

> Translated a PostgreSQL query using `DISTINCT ON` to BigQuery using
> `QUALIFY ROW_NUMBER() OVER (PARTITION BY ...) = 1`. Explicit column
> list, timezone set in the date filter, tested against a 1 percent
> sample before full run.

### Bad

> Wrote `SELECT *` with an implicit cross join between two large
> tables and no date filter. Ran it on production. Timed out after
> 20 minutes.

## Verification

- The query runs without error on the target dialect.
- `EXPLAIN` shows no unexpected full table scans on large tables.
- Column types and timezone behavior match the expected output.
- A sample run produces the expected row count and schema.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/sql-queries
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: sql-queries
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/sql-queries/raw -o .cursor/skills/sql-queries/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/sql-queries.md and install it as a project skill at skills/sql-queries/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
