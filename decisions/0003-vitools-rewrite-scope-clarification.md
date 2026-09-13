---
title: 0003-vitools-rewrite-scope-clarification
type: decision-record
status: active
owner: vidoxlabs
created: 2026-06-17
updated: 2026-06-17
tags: [adr, vitools, memorix, scope]
related:
  - .plans/superpowers/plans/2026/06/17/2026-06-17-vitools-rewrite-agent.md
  - .plans/superpowers/plans/2026/06/17/2026-06-17-vitools-rewrite-plan-alignment-review.md
---

# ADR 0003: ViTools Rewrite Scope Clarification

## Status

**Superseded** by `ADR-vitools-public-canonical-layout.md` (2026-09-12).

Accepted — 2026-06-17

## Context

The initial ViTools Rewrite Agent plan assumed the vitools git repository’s `skills/` and `plugins/` trees (37 vendored packages) were the primary rewrite target. Post-CRS consolidation review and MCP fleet inventory show:

- Production MCP tooling lives at `vilabs/tools/vilabs_mcp/vitools/` (26 Vidoxlabs-native integrations).
- The vitools git repo holds a skills/plugins **reference mirror**, not the stable MCP fleet.
- Memorix + ViLabs Studio are the intended primary delivery plane—not cross-platform auto-sync.

## Decision

1. **Scope the rewrite plan to the MCP fleet** and `.agents/` canonical authoring in the vitools git repo.
2. **Do not bulk-quarantine** `skills/` or `plugins/` in Phase 0; defer to a separate future workstream if needed.
3. **Memorix indexes `.agents/`** as the canonical layer; platform emitters are optional Studio exports.
4. **Extend `vilabs_cli memorix`** and `vilabs_mcp/vitools/` MCP tools—no standalone `vitools-sync` CLI.
5. Phase 0 establishes preventive legal CI and Memorix hooks when no vendored content exists in MCP scope.

## Consequences

- Phase 0 artifacts: legal-gate CI, catalog schema.
- Stable MCP Python workers are enhanced—not replaced.
- Broad plugin mirror quarantine requires a new ADR and plan if pursued later.

## References

- [Rewrite plan](../.plans/superpowers/plans/2026/06/17/2026-06-17-vitools-rewrite-agent.md)
- [Alignment review](../.plans/superpowers/plans/2026/06/17/2026-06-17-vitools-rewrite-plan-alignment-review.md)
- CRS consolidation: `vilabs/tools/doc/vilabs-crs-consolidation-change-record-2026-06-17.md`
