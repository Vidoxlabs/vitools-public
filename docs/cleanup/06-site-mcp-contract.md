---
title: Phase 6 — Site/MCP contract handoff
date: 2026-09-12
author: ViTools cleanup agent
phase: 6
status: complete
audience: vidoxlabs.dev agent
---

# Site/MCP contract — handoff note

This document defines the contract between the `vitools-public` repo and
the `vidoxlabs.dev` site + `mcp.vidoxlabs.dev` worker. The site and worker
are implemented in a separate task. This document is the binding spec.

## Data source

The site and worker consume `catalog/vitools.catalog.json` from this repo.
Two options for the site:

1. **Build-time fetch**: the Astro build fetches
   `https://raw.githubusercontent.com/Vidoxlabs/vitools-public/main/catalog/vitools.catalog.json`
   at build time. Good for static rendering.
2. **Worker KV snapshot**: a Cloudflare Worker periodically fetches the
   catalog and stores it in KV. Good for the MCP worker and dynamic pages.

Either approach works. The catalog is the single source of truth.

## Routes

| Route | Purpose |
|-------|---------|
| `/vitools` | Landing page: catalog summary, category filter, search |
| `/vitools/skills` | All public skills (grid or list) |
| `/vitools/skills/[slug]` | Single skill: rendered markdown, install buttons, download |
| `/vitools/agents` | All public agents |
| `/vitools/agents/[slug]` | Single agent: rendered markdown, install buttons, download |

## Page UI per item

Each skill/agent page renders:

1. **Title and description** from the catalog item.
2. **Rendered markdown** from the raw file (fetch from `raw_url`).
3. **Category and tags** as filter chips.
4. **Install section** with copy buttons:
   - Generic command (copy)
   - Claude Code command (copy)
   - Cursor command (copy)
   - Agent prompt snippet (copy)
5. **MCP connect JSON** (copy button).
6. **Download links**:
   - Raw markdown: `/vitools/skills/<slug>/raw`
   - Zip folder: `/vitools/skills/<slug>.zip`

## What NOT to scrape

- No vendor content is in this repository.
- `catalog/inventory.json` — internal, includes quarantined items.
- `.plans/`, `docs/cleanup/` — governance, not catalog units.
- `plugins/` — currently contains only git ref stubs, not in the catalog.

## MCP worker contract

Endpoint: `https://mcp.vidoxlabs.dev/vitools`

Tools (all read-only):

| Tool | Input | Output |
|------|-------|--------|
| `vitools.list` | `kind?`, `category?`, `tag?`, `status?` | Array of catalog items (public only) |
| `vitools.get` | `slug` or `mcp_uri` | Single item: frontmatter + body URL |
| `vitools.categories` | none | Category counts: `{category: count}` |
| `vitools.search` | `query` (keyword) | Array of matching items |
| `vitools.install_snippet` | `slug`, `platform` | Platform-specific install text string |
| `vitools.manifest` | none | `{version, generated_at, source_commit, counts}` |

The worker reads `catalog/vitools.catalog.json` (or the compact
`vitools.catalog.min.json`). No write tools. No authentication required
for read.

## Catalog item shape (for the worker)

Each item in `catalog.vitools.catalog.json[].items[]` has:

```json
{
  "id": "skill:data-loss-prevention",
  "kind": "skill",
  "slug": "data-loss-prevention",
  "name": "data-loss-prevention",
  "title": "Data Loss Prevention",
  "description": "...",
  "summary": "Halt and confirm before destructive commands",
  "license": "MIT",
  "origin": "derived",
  "status": "promoted",
  "public": true,
  "category": "safety",
  "tags": ["safety", "git", "cloud", "confirmation"],
  "platforms": ["claude-code", "cursor", "copilot", "opencode", "generic"],
  "path": "skills/data-loss-prevention/SKILL.md",
  "html_url": "https://vidoxlabs.dev/vitools/skills/data-loss-prevention",
  "raw_url": "https://raw.githubusercontent.com/Vidoxlabs/vitools-public/main/skills/data-loss-prevention/SKILL.md",
  "mcp_uri": "vitools://skill/data-loss-prevention",
  "install": {
    "generic": "npx skills add vidoxlabs/vitools-public/skills/data-loss-prevention",
    "claude-code": "/plugin marketplace add Vidoxlabs/vitools-public\n# then enable: data-loss-prevention",
    "cursor": "curl -fsSL https://vidoxlabs.dev/vitools/skills/data-loss-prevention/raw -o .cursor/skills/data-loss-prevention/SKILL.md",
    "agent_prompt": "Fetch https://vidoxlabs.dev/vitools/skills/data-loss-prevention.md ..."
  }
}
```

Filter by `public: true` for all site and MCP rendering. Items with
`public: false` are hidden from the site and MCP.

## Schema validation

The catalog validates against `catalog/schema.json`. Run:

```bash
python scripts/catalog-build.py --validate
```

The schema enforces required fields, category vocabulary, and mcp_uri
format. The site and worker can assume the catalog is valid if CI passes.
