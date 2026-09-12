---
name: vitools-memorix-integration
title: ViTools Memorix Integration Plan
type: doc
date: 2026-06-17
status: active
author: Gavin Lafferty (Vioxniv)
project: vitools
tags:
  - vitools
  - memorix
  - integration
related:
  - ../vilabs/tools/vilabs_mcp/vitools/tools/vitools_canonical/INTEGRATION.md
  - 2026-06-17-vitools-rewrite-implementation-progress.md
---

# ViTools Memorix Integration — Completed Work

## Summary

Bridged the vitools `.agents/` canonical layer to Memorix collection, indexing, retrieval, and
temporal tracking via `vilabs_mcp/vitools/tools/vitools_canonical/`.

## Surfaces

| Surface            | Entry points                                                                          |
| ------------------ | ------------------------------------------------------------------------------------- | ---- | ------- | ----------- | --------- | ------- |
| MCP                | `memorix.vitools.index`, `.emit`, `.catalog`, `.legal_check`, `.recommend`, `.events` |
| CLI                | `vilabs memorix vitools index                                                         | emit | catalog | legal-check | recommend | events` |
| vitools-sync hooks | `MEMORIX_VITOOLS_COLLECTION=1` logs emit/catalog/legal events                         |

## Studio follow-ups (deferred)

1. Canonical skill inventory card in Memorix compartment
2. Recent emit history timeline widget
3. UI trigger for `vilabs memorix vitools emit` and legal-check
