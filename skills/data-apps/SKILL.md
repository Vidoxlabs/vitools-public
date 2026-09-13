---
name: data-apps
description: >-
  Build data applications with React or Streamlit. Connect to data sources, create dashboards, and integrate AI chat. Use when creating interactive interfaces over structured data.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: data
  tags: [data-apps, react, streamlit, dashboards, ai-chat]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: data-apps
    summary: Build interactive data apps and dashboards
  derived_from:
    - name: building-data-apps
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Data Apps

## When to use

Activate when building an interactive interface over structured data. Use when stakeholders need a dashboard or AI chat over a data source.

## Procedure

1. Choose framework: Streamlit for Python prototyping, React for production.
2. Connect to data source with parameterized queries and connection pooling.
3. Design layout: sidebar filters, main charts, optional AI chat.
4. Implement filters that flow into query parameters.
5. Add visualizations with Plotly, Altair, or Recharts.
6. Integrate AI chat: send question and schema context, return answer or SQL.
7. Deploy: Streamlit Cloud, Cloud Run, or static host.

## Guardrails

- Do not embed credentials in app code. Use env vars or secrets manager.
- Do not allow raw user input in SQL without parameterization.
- Do not load the entire dataset into memory. Query and paginate.
- Do not ship without rate limiting on the AI chat endpoint.

## Examples

### Good

> Streamlit app with sidebar filters, three charts backed by parameterized BigQuery queries, AI chat that generates SQL. Credentials from Secret Manager.

### Bad

> React app fetches a 5 GB CSV on load, builds SQL with string concatenation, API key hardcoded. Crashes on filter.

## Verification

- Filters update charts without full page reload.
- Queries are parameterized; no string concatenation.
- No credentials in source code.
- AI chat returns results or a helpful error.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/data-apps
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: data-apps
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/data-apps/raw -o .cursor/skills/data-apps/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/data-apps.md and install it as a project skill at skills/data-apps/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```