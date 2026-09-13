---
title: ADR-vitools-public-canonical-layout
type: decision-record
status: accepted
owner: vidoxlabs
created: 2026-09-12
updated: 2026-09-12
tags: [adr, vitools, catalog, license, layout]
related:
  - decisions/0003-vitools-rewrite-scope-clarification.md
  - docs/cleanup/00-inventory.md
  - catalog/inventory.json
---

# ADR: ViTools public canonical layout and license policy

## Status

Accepted — 2026-09-12. Supersedes ADR 0003's deferral of skills/plugins
cleanup. ADR 0003 scoped the rewrite to the MCP fleet and `.agents/` layer;
this ADR picks up the deferred workstream for the public `skills/` and
`plugins/` trees.

## Context

Phase 0 inventory (`docs/cleanup/00-inventory.md`) confirmed:

- `skills/` contains 214 entries (206 with SKILL.md), not "1,500+" as the
  README claims. Origins include Google (Apache-2.0), Anthropic
  (LICENSE.txt, branding-locked), Compound Engineering (no license),
  Cloudflare, Figma, HuggingFace, Firebase, Fastly, Cursor, and others.
- `plugins/` contains 22 directories (not "170+"), most of which are git
  ref stubs with no actual plugin content.
- `.agents/` does not exist despite AGENTS.md declaring it canonical.
- `mcp_tooling/` does not exist despite the README listing it.
- Root `LICENSE` is MIT (Copyright 2024–2026 Vidoxlabs) but does not cover
  vendored Apache, proprietary, or branding-locked files in `skills/` and
  `plugins/`.
- No vendor content is in this repository. Derived skills reference sources via `derived_from`.

The repo is legally dishonest: it claims MIT over content that is Apache,
proprietary, or branding-locked. It is also numerically dishonest (1,500+
skills, 170+ plugins).

## Decision

### 1. Public canonical tree

```text
vitools-public/
  AGENTS.md                         # public catalog is source of truth
  README.md                         # honest counts, install, MCP, site
  LICENSE                           # MIT for first-party only
  NOTICE.md                         # third-party attributions + archive policy
  catalog/
    inventory.json                  # every discovered unit, including quarantined
    vitools.catalog.json            # public, site/MCP facing
    vitools.catalog.min.json        # compact variant
    schema.json                     # JSON Schema for catalog records
  skills/                           # FIRST-PARTY ONLY (Vidoxlabs MIT)
    <slug>/
      SKILL.md
      references/                   # optional
      scripts/                      # optional
      templates/                    # optional
  agents/                           # FIRST-PARTY ONLY
    <slug>/
      AGENT.md
      references/                   # optional
  plugins/                          # generated thin adapters (optional)
    claude/
    cursor/
    copilot/
    opencode/
  platforms/                        # generated install snippets
  scripts/
    catalog-build.py
    legal-gate.sh
    emit-adapters.py
    phase0-inventory.py
  .github/workflows/ci.yml          # catalog validate + legal gate + markdownlint
```

Governance directories that stay: `Instructions/`, `cookbooks/`,
`decisions/`, `docs/`, `tools/`.

### 2. `.agents/` resolution

`.agents/` does not exist in this repo. AGENTS.md references it as the
canonical Memorix-indexed layer, but that layer was never created here.
Decision: do not create `.agents/` in the public repo. The public canonical
layout is `skills/` + `agents/` (first-party only). If `.agents/` exists in
the private vitools tree, it remains the authoring source there; the public
repo emits into `skills/` + `agents/` for the public layout.

### 3. Skill vs agent vs plugin definitions

| Kind | Path | Entry file | Frontmatter `metadata.kind` |
|------|------|------------|-----------------------------|
| skill | `skills/<slug>/SKILL.md` | SKILL.md | `skill` |
| agent | `agents/<slug>/AGENT.md` | AGENT.md | `agent` |
| plugin | `plugins/<platform>/` | generated | `plugin` |

Skills and agents share the same frontmatter family. Plugins are generated
thin adapters, never hand-authored canonical content.

### 4. License policy

| Class | Test | Disposition |
|-------|------|-------------|
| A — First-party Vidoxlabs | Author is Vidoxlabs/Vioxniv, MIT, no vendor branding, no copied body | Keep in `skills/` or `agents/`. Normalize frontmatter. |
| B — Permissively licensed vendor | Apache-2.0 / MIT / BSD AND no branding lock AND NOTICE can be preserved | Move original to `archive/vendor/<origin>/<slug>/`. Rewrite short Vidoxlabs skill from concept only. Link `derived_from`. Preserve Apache NOTICE in `NOTICE.md`. |
| C — Branding-locked or proprietary | Instructs "keep Anthropic branding", reserved names, non-redistributable license, missing license | Archive original. Do NOT republish body. Optional 20–40 line Vidoxlabs rewrite of the procedure idea if generic. |
| D — Compound Engineering / unknown vendor | `ce-*` prefix or no license, unknown origin | Archive vendor. Review each individually. |
| E — Broken / incomplete | No SKILL.md, Notion export, empty directory | Do not catalog. |

Root `LICENSE` (MIT) covers first-party content only. `NOTICE.md`
documents third-party attributions and the archive policy. Vendored files
are documented in each skill's `derived_from` frontmatter field.

### 5. Catalog + MCP + site contract

The repo produces `catalog/vitools.catalog.json` as the single machine-readable
artifact consumed by:
- `https://vidoxlabs.dev/vitools` (Astro site renders from catalog)
- `https://mcp.vidoxlabs.dev/vitools` (MCP worker lists/filters/fetches)

The catalog contains only `public: true` items with `status: promoted`.
Every public item must pass legal-gate + required sections + catalog
validation.

MCP tools (read-only, defined in the contract but implemented later):
`vitools.list`, `vitools.get`, `vitools.categories`, `vitools.search`,
`vitools.install_snippet`, `vitools.manifest`.

### 6. What stays private

- Private sibling repos (`vilabs`, `vidocs`, `vitools` private) are not
  edited from this repo. Changes that belong there get a pointer in the
  cleanup report.
- No vendor body text is included anywhere in this repository.
- Internal hostnames, Infisical paths, cluster IPs, Discord guild IDs,
  operator traces — never appear in public skills or catalog.

## Consequences

- `skills/` and `plugins/` are no longer "legacy mirrors out of scope."
  They are the public canonical tree, actively cleaned and curated.
- ADR 0003's deferral is resolved.
- AGENTS.md must be rewritten to reflect the new canonical layout.
- README.md must be rewritten with honest counts from the catalog.
- The legal gate script must be expanded beyond symlink checks to
  frontmatter and content validation.
- CI must validate the catalog, not just lint markdown.

## References

- Phase 0 inventory: `docs/cleanup/00-inventory.md`
- Structured inventory: `catalog/inventory.json`
- Prior scope decision: `decisions/0003-vitools-rewrite-scope-clarification.md`
- Cleanup agent prompt: `docs/cleanup/` (governing prompt)
