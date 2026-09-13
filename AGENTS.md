---
name: vitools-agents-instructions
title: vitools Agent Instructions
type: doc
date: 2026-09-12
status: active
author: Gavin Lafferty (Vioxniv)
project: vitools
tags:
  - agents
  - instructions
  - catalog
  - mcp
related:
  - decisions/ADR-vitools-public-canonical-layout.md
  - catalog/vitools.catalog.json
---

# ViTools — Agent Operating Context

> **Read this file first** when working in the ViTools public repository.

---

## What ViTools Public Is

ViTools public is the canonical registry of first-party Vidoxlabs skills
and agents, published as installable `SKILL.md` / `AGENT.md` files. The
catalog (`catalog/vitools.catalog.json`) is the source of truth for the
site (`vidoxlabs.dev/vitools`) and MCP worker
(`mcp.vidoxlabs.dev/vitools`).

| Path              | Role                                                                   |
| ----------------- | --------------------------------------------------------------------- |
| `skills/`         | **Canonical** — first-party Vidoxlabs skills (MIT)                     |
| `agents/`         | **Canonical** — first-party Vidoxlabs agents (MIT)                     |
| `catalog/`        | Machine-readable catalog, schema, inventory                             |
| `platforms/`      | Generated install snippets per platform                               |
| `Instructions/`   | Execution standards governance index                                   |
| `decisions/`      | Architecture decision records                                           |

## Canonical Layout

The public canonical tree is `skills/` + `agents/` (first-party MIT
only). The previous `.agents/` canonical layer does not exist in this
repo and is not used. See
`decisions/ADR-vitools-public-canonical-layout.md` for the full decision.

## Before You Edit

1. New skills go in `skills/<slug>/SKILL.md`. New agents go in
   `agents/<slug>/AGENT.md`.
2. Use the canonical frontmatter format. See `skills/skills-template/SKILL.md`
   for the template.
3. Set `license: MIT`, `metadata.status: promoted`, and include all
   required sections (When to use, Procedure, Guardrails, Examples,
   Verification, Install).
4. Never copy vendor body text into first-party files. Use concept cards
   + official docs. See `NOTICE.md` for the archive policy.
5. Run `python scripts/catalog-build.py` and
   `bash scripts/vitools-legal-gate.sh` before committing.

## Validation

```bash
# Build and validate the catalog
python scripts/catalog-build.py
python scripts/catalog-build.py --validate
python scripts/catalog-build.py --check-inventory

# Legal gate (license, origin, branding checks)
bash scripts/vitools-legal-gate.sh

# Markdown lint
npx markdownlint-cli2 "**/*.md"
```

## What Not To Do

- Do not include vendor body text in first-party skills.
- Do not put `claude` or `anthropic` in a first-party skill `name`.
- Do not publish a skill without Guardrails, Examples, and Verification.
- Do not claim counts that do not match `catalog/vitools.catalog.json`.
- Do not reference internal hostnames, IP addresses, or private repos.
