---
name: vitools-rewrite-implementation-progress
title: ViTools Rewrite Implementation Progress
type: doc
date: 2026-06-17
status: active
author: Gavin Lafferty (Vioxniv)
project: vitools
tags:
  - vitools
  - rewrite
  - memorix
  - progress
related:
  - 2026-06-17-vitools-rewrite-agent.md
  - 2026-06-17-vitools-memorix-integration.md
---

# ViTools Rewrite — Implementation Progress (2026-06-17)

## Completed

| Phase | Deliverable                                  | Location                                                                                                        |
| ----- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 0     | Legal gate CI, archive scaffold, MANIFEST    | `archive/vendor/`, `.github/workflows/vitools-legal-gate.yml`                                                   |
| 0     | `.agents/` canonical skeleton                | `.agents/`                                                                                                      |
| 1     | `vitools-sync` CLI                           | `tools/vitools-sync/`                                                                                           |
| 1     | 5 native skills migrated                     | `.agents/skills/` (skill-mining, skills-template, evidence-answering, v37-validation, vidoxlabs-core-architect) |
| 2     | Rewrite orchestrator + vitools-rewrite skill | `agents/rewrite-orchestrator.md`, `.agents/skills/vitools-rewrite/`                                             |
| 2     | 3 concept cards + pilot skills               | `.agents/concept-cards/`, tavily-research, context7-library-docs, create-cursor-plugin                          |
| 3     | 6 platform emitters + install                | `tools/vitools-sync/src/vitools_sync/emitters/`, `platforms/`                                                   |
| 4     | Catalog inventory (271 entries)              | `tools/vitools-sync/catalog/inventory.json`                                                                     |
| 4     | Design spec                                  | `docs/superpowers/specs/2026-06-17-vitools-rewrite-design.md`                                                   |

## Canonical layer snapshot

- **9 skills** in `.agents/skills/`
- **3 concept cards** in `.agents/concept-cards/`
- **2 MCP servers** in `.agents/mcp/servers.yaml` (tavily, context7)
- **6 tests passing** in vitools-sync

## Next: Memorix integration

Bridge canonical layer to Memorix collection, indexing, retrieval, and temporal tracking via
`vilabs_mcp/vitools/tools/vitools_canonical/` and `vilabs memorix vitools` subcommands.
