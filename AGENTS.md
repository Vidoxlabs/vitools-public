---
name: vitools-agents-instructions
title: vitools Agent Instructions
type: doc
date: 2026-06-17
status: active
author: Gavin Lafferty (Vioxniv)
project: vitools
tags:
  - agents
  - instructions
  - mcp
  - tooling
related:
  - .plans/NAVIGATION.md
---

# ViTools — Agent Operating Context

> **Read this file first** when working in the ViTools repository. For MCP fleet runtime context,
> see `vilabs/tools/vilabs_mcp/vitools/AGENTS.md` in the ViLabs monorepo.

---

## What ViTools Is

ViTools is Vidoxlabs’ repository for **agent knowledge, skills governance, and the `.agents/`
canonical layer** that Memorix indexes. The **stable MCP tooling fleet** (FastMCP servers) lives in
the ViLabs meta-repo at `tools/vilabs_mcp/vitools/` — not in this repo’s `skills/` or `plugins/`
trees.

| Path              | Role                                                                              |
| ----------------- | --------------------------------------------------------------------------------- |
| `.agents/`        | **Canonical** — Memorix-primary skills, MCP registry, agents (Vidoxlabs MIT only) |
| `archive/vendor/` | Reference-only quarantine (not synced to agents)                                  |
| `skills/`         | Legacy/reference skill mirror — **out of scope** for current rewrite plan         |
| `plugins/`        | Legacy/reference plugin mirror — **out of scope** for current rewrite plan        |
| `Instructions/`   | Execution standards governance index                                              |
| `.plans/`         | Plans, alignment reviews, daily notes                                             |
| `decisions/`      | Architecture decision records                                                     |

## Alignment

- **Memorix-primary:** `.agents/` is indexed by Memorix for context retrieval and skill suggestions.
- **Studio orchestration:** ViLabs Studio triggers rewrites and optional platform exports.
- **Delivery:** `vilabs memorix vitools` + `memorix.vitools.*` MCP tools — see
  `vilabs/tools/vilabs_mcp/vitools/tools/vitools_canonical/INTEGRATION.md`.
- **Legal gate:** Never copy vendored text into `.agents/`; use concept cards + official docs.

Active plan:
[.plans/superpowers/plans/2026/06/17/2026-06-17-vitools-rewrite-agent.md](.plans/superpowers/plans/2026/06/17/2026-06-17-vitools-rewrite-agent.md)

## Before You Edit

1. Confirm scope: MCP fleet changes belong in `vilabs/tools/vilabs_mcp/vitools/`.
2. New agent-facing content goes in `.agents/` only — not `archive/vendor/`.
3. Follow the Vidoxlabs skill template: `skills/skills-template/reference/TEMPLATE.md`.
4. Add new plans to `.plans/NAVIGATION.md` and `.plans/INDEX.md`.

## Validation

From a machine with `vilabs_cli` installed:

```bash
# vitools-sync (local)
cd tools/vitools-sync && pip install -e .
vitools-sync catalog build
vitools-sync emit --platform all --target ../../platforms
vitools-sync legal check .agents/skills/skill-mining/SKILL.md

# Memorix integration (vilabs monorepo)
export VITOOLS_ROOT=~/Repositories/vitools
vilabs memorix vitools index
vilabs memorix vitools recommend "web research citations"
vilabs memorix vitools events --limit 10
# MCP: memorix.vitools.index | .recommend | .emit | .legal_check
```

Local CI equivalents:

```bash
# Markdown lint (matches .github/workflows/ci.yml)
npx markdownlint-cli2 "**/*.md"

# Legal gate script (local)
bash scripts/vitools-legal-gate.sh
```

## What Not To Do

- Do not emit `archive/vendor/**` content into `.agents/` or platform configs.
- Do not add a standalone `vitools-sync` CLI — extend `vilabs memorix` instead.
- Do not bulk-move `skills/` or `plugins/` without a new ADR and plan.
- Do not promote skills without Guardrails, Examples, and Verification sections.

## Related Repositories

- [vilabs](https://github.com/Vidoxlabs/vilabs) — Meta-repo; MCP fleet at
  `tools/vilabs_mcp/vitools/`
- [vilabs_cli](https://github.com/Vidoxlabs/vilabs_cli) — `vilabs memorix` command group
- [V37_Cluster](https://github.com/Vidoxlabs/v37_cluster) — Infrastructure
- [ViDocs](https://github.com/Vidoxlabs/vidocs) — Documentation corpus
