---
name: vitools-rewrite-plan-alignment-review
title: ViTools Rewrite Plan Alignment Review
type: doc
date: 2026-06-17
status: active
author: Gavin Lafferty (Vioxniv)
project: vitools
tags:
  - vitools
  - memorix
  - vilabs-studio
  - alignment-review
  - rewrite
related:
  - 2026-06-17-vitools-rewrite-agent.md
  - decisions/0003-vitools-rewrite-scope-clarification.md
---

# ViTools Rewrite Plan — Alignment Review (ViLabs Studio + Memorix)

**Date:** 2026-06-17 **Context:** Post-CRS consolidation (`vilabs_cli.crs` inlined; `vilabs_crs`
submodule retired). **Reviewed plan:** ViTools Rewrite Agent and Cross-Platform Sync (original
draft).

---

## Executive Summary

The original rewrite plan correctly identified legal-first quarantine and a `.agents/` canonical
layer, but **scope drift** treated the vitools git repo’s broad skills/plugins mirror (~37 vendored
packages, ~500 `SKILL.md` files) as the primary target. The **actual stable vitools surface** in
production is the **MCP tooling fleet** at `vilabs/tools/vilabs_mcp/vitools/` (26 integrations,
Vidoxlabs-native MIT). Delivery should be **Memorix-primary** via `vilabs_cli` +
`vilabs_mcp/vitools/memorix`, with cross-platform emitters as optional Studio exports—not a
standalone `vitools-sync` CLI.

---

## Strengths (keep from original plan)

1. **Legal-first model** — concept cards + official docs, not vendor text copying; overlap gates.
2. **`.agents/` canonical boundary** — clean separation between reference archive and agent-facing
   artifacts.
3. **Vidoxlabs skill template** — Summary, Triggers, Guardrails, Examples, Verification aligned with
   Instructions governance.
4. **Phased delivery** — foundation before batch rewrite.
5. **MCP source-of-truth schema** — `servers.yaml` as neutral MCP definition layer.

---

## Scope Drift (correct in adjusted plan)

| Original assumption                       | Actual state (2026-06-17)                                                                                     |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| vitools repo = primary MCP fleet          | MCP fleet lives in `vilabs/tools/vilabs_mcp/vitools/`; vitools git repo holds skills/plugins reference mirror |
| Quarantine 37 vendored plugins in Phase 0 | MCP fleet tools are **Vidoxlabs-native** (MIT); no third-party plugin vendoring in scope                      |
| Standalone `vitools-sync` CLI             | CRS consolidated into `vilabs_cli`; delivery extends `vilabs memorix` + MCP tools under `vilabs_mcp/vitools/` |
| Cross-platform sync as primary            | Memorix indexing + Studio orchestration is primary; Cursor/Devin/Grok/etc. are optional exports               |
| `vilabs drift scan`                       | Command is `vilabs drift analyze` (no `scan` subcommand)                                                      |

---

## Five Recommendations

### 1. Scope Phase 0 to the stable MCP fleet

Limit legal foundation and MANIFEST provenance to `vilabs/tools/vilabs_mcp/vitools/`. Defer broad
`skills/` and `plugins/` vendoring quarantine to a **separate future workstream** documented in
ADR-0003.

### 2. Make Memorix the primary consumer of `.agents/`

Index `.agents/skills/`, `.agents/mcp/servers.yaml`, and concept cards via Memorix working-set
ingest and temporal horizons. Cross-platform emitters read the same canonical layer but are not the
default delivery path.

### 3. Extend `vilabs_cli memorix` instead of a new CLI

Add rewrite/sync/export capabilities under the existing `vilabs memorix` command group (e.g.
`vilabs memorix sync plan`, future `vilabs memorix export --platform cursor`). New MCP tools for
rewrite orchestration belong in `vilabs_mcp/vitools/tools/` or `memorix/`—not a top-level
`vitools-sync` binary.

### 4. Studio orchestrates rewrites; emitters are optional

ViLabs Studio (via `vilabs_web` agent_intel / Memorix UI) visualizes the skill graph, triggers
rewrite-orchestrator runs, and surfaces legal-gate decisions. Platform-specific configs are export
targets selected in Studio—not auto-synced on every commit.

### 5. Shift Phase 0 when no vendored content exists in MCP scope

Drift analysis on 2026-06-17 found **no third-party vendored plugin trees** inside the MCP fleet.
Phase 0 focus becomes: **native authoring pipeline + Memorix hooks + `.agents/` skeleton + CI legal
gate**—not large-scale `archive/vendor/` moves.

---

## Memorix / Studio Integration Points

| Layer            | Path / command                             | Role                                                              |
| ---------------- | ------------------------------------------ | ----------------------------------------------------------------- |
| Canonical skills | `.agents/skills/`                          | Memorix indexes for context retrieval and skill suggestions       |
| Canonical MCP    | `.agents/mcp/servers.yaml`                 | Neutral MCP registry; Memorix links tools to evidence URLs        |
| Concept cards    | `.agents/concept-cards/`                   | Provenance-only inspiration metadata (no vendor excerpts)         |
| Memorix MCP      | `vilabs_mcp/vitools/memorix/`              | Tri-cluster memory: search, query, ingest, projection             |
| CLI plane        | `vilabs memorix status\|health\|sync plan` | Operator sync and validation                                      |
| CRS drift        | `vilabs drift analyze`                     | Scope confirmation; output under `runtime/reports/drift-analysis` |
| Studio UI        | `vilabs_web` Memorix API routes            | Skill graph visualization, rewrite orchestration                  |
| Legal gate       | `.github/workflows/vitools-legal-gate.yml` | Block `archive/vendor/**` → `.agents/` or `platforms/` paths      |

---

## Additional Success Criteria (Memorix / Studio)

1. **Memorix indexes `.agents/`** — skills and MCP entries discoverable via `vilabs memorix`
   query/search after ingest.
2. **Rewrite decisions are logged** — orchestrator and legal-gate outcomes recorded in Memorix
   execution collection for temporal analysis.
3. **Studio can trigger export** — optional platform emitters invocable from Studio without being
   the default install path.

---

## Evidence (2026-06-17)

- `vilabs drift analyze` → `review_packets=0 implementation_sweeps=0`; report dir:
  `vilabs/tools/vilabs_cli/runtime/reports/drift-analysis`
- MCP fleet license scan: 24/26 tool dirs carry Vidoxlabs MIT `LICENSE`; `memorix` and `standards`
  have no LICENSE file (Vidoxlabs-native code)
- CRS consolidation record: `vilabs/tools/doc/vilabs-crs-consolidation-change-record-2026-06-17.md`
