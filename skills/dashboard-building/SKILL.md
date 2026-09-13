---
name: dashboard-building
description: >-
  Build interactive HTML dashboards with charts, filters, and tables. Self-contained, browser-openable, no server required. Use when creating executive overviews, team monitoring, or data reports.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: data
  tags: [dashboards, html, charts, visualization, reporting]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: dashboard-building
    summary: Self-contained interactive HTML dashboards
  derived_from:
    - name: cowork-build-dashboard-create-viz
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Dashboard Building

## When to use

Activate when building an interactive dashboard for stakeholders. Use for executive overviews, team monitoring snapshots, or self-contained data reports.

## Procedure

1. Identify the audience and the 3-5 key metrics they need to see.
2. Choose the layout: KPI cards at top, trend charts in middle, detail tables at bottom.
3. Build as a single HTML file with embedded CSS and JS. No server, no build step.
4. Use Chart.js, ECharts, or D3 for visualizations. Include filters for date range and segment.
5. Load data from an embedded JSON or a fetch call to an API.
6. Add interactivity: clickable filters, sortable tables, hover tooltips.
7. Test by opening the file in a browser. Verify all charts render and filters work.

## Guardrails

- Do not require a server or build step. The dashboard must open directly in a browser.
- Do not embed sensitive data in the HTML. Use API calls with auth.
- Do not use more than 5 chart types. Focus on clarity.
- Do not forget mobile responsiveness. Test at 768px width.

## Examples

### Good

> Built a single-file HTML dashboard with 4 KPI cards, 2 trend charts, and a sortable table. Opens in any browser, filters by date range, loads data from an API with auth. 45 KB total.

### Bad

> Built a React app with 20 dependencies, a build step, and a Node server. Takes 30 seconds to load. Charts require a specific browser version.

## Verification

- Dashboard opens in any browser without a server or build step.
- All charts render and filters work.
- File size is under 500 KB.
- Mobile layout is tested at 768px.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/dashboard-building
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: dashboard-building
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/dashboard-building/raw -o .cursor/skills/dashboard-building/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/dashboard-building.md and install it as a project skill at skills/dashboard-building/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```