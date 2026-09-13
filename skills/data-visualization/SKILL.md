---
name: data-visualization
description: >-
  Create effective data visualizations with Python (matplotlib, seaborn,
  plotly). Use when building charts, choosing the right chart type for
  a dataset, creating publication-quality figures, or applying design
  principles like accessibility and color theory.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: vidoxlabs
  publisher: vidoxlabs
  category: data
  tags: [data, visualization, matplotlib, seaborn, plotly, charts]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: data-visualization
    summary: Create effective charts with Python visualization libraries
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Data Visualization

## When to use

Activate when building charts, choosing the right chart type for a
dataset, creating publication-quality figures, or applying design
principles like accessibility and color theory to visualizations.

## Procedure

1. Identify the data shape: time series, categorical, distribution,
   correlation, or hierarchical.
2. Choose the chart type that matches the question: line for trends,
   bar for comparisons, scatter for correlation, histogram for
   distribution, heatmap for matrices.
3. Use `matplotlib` for static publication-quality figures, `seaborn`
   for statistical visualizations, `plotly` for interactive charts.
4. Apply design principles: clear titles, axis labels with units,
   appropriate color palettes (colorblind-safe), and minimal chart
   junk.
5. Verify accessibility: contrast ratios meet WCAG AA, color is not
   the sole encoding (add labels or patterns), and text is readable
   at the target size.
6. Save at the appropriate resolution: 150 DPI for screen, 300 DPI
   for print.

## Guardrails

- Do not use a pie chart for more than 5 categories. Use a bar chart
  instead.
- Do not use a dual y-axis chart unless both series share a meaningful
  relationship. Dual axes mislead.
- Do not use 3D charts for 2D data. They distort perception.
- Do not truncate the y-axis to exaggerate differences. Start at zero
  for bar charts.

## Examples

### Good

> Created a line chart for monthly revenue with a clear title,
> labeled axes in USD, a colorblind-safe palette, and a 150 DPI
> export. Added a horizontal line for the target. Chart type matches
> the question (trend over time).

### Bad

> Created a 3D pie chart with 12 categories, no axis labels, default
> colors that fail contrast checks, and a truncated y-axis that
> exaggerates a 2% difference into a 50% visual gap.

## Verification

- Chart type matches the data shape and question.
- Axes are labeled with units.
- Color palette is colorblind-safe.
- No 3D effects or truncated axes on bar charts.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/data-visualization
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: data-visualization
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/data-visualization/raw -o .cursor/skills/data-visualization/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/data-visualization.md and install it as a project skill at skills/data-visualization/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
