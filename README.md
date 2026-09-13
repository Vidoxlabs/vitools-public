# ViTools

**Public skill, agent, and tool registry for AI engineering.**

ViTools is a clean, installable registry of first-party skills, agents,
and tooling for coding agents (Claude Code, Cursor, Copilot, Codex,
OpenCode). It includes a schema-validated catalog, a legal gate that
enforces license and origin rules, an MCP server, and platform adapters.

## What this repo demonstrates

- **Skill design**: 23 skills across git workflows, evaluation,
  automation, research, data, cloud, design, and documentation — each
  with canonical frontmatter, required sections, and original prose.
- **Agent design**: 4 agents for catalog maintenance, skill authoring,
  legal review, and rewrite orchestration.
- **MCP implementation**: A stdio MCP server (`tools/mcp-server/`) with
  6 read-only tools, pure stdlib, no dependencies.
- **Python CLI**: `tools/vitools-sync/` — 5,400+ lines of Python for
  catalog management, legal overlap checking, and platform emission
  to Cursor, OpenCode, Grok, Devin, Mistral, and Antigravity.
- **Legal discipline**: A legal gate that blocks vendor body text,
  missing licenses, and branding contamination. 180 vendor items
  derived from 15 vendor origins. No vendor body text is included.
- **CI/CD**: Catalog validation, legal gate, and structure checks
  integrated into GitHub Actions.

## Current catalog

Counts are computed from `catalog/vitools.catalog.json`. Run
`python scripts/catalog-build.py` to verify.

| Kind            | Count |
|-----------------|-------|
| Skills          | 102   |
| Agents          | 4     |
| Archived vendor | 0     |

## Repository structure

| Directory           | Purpose                                         |
|---------------------|-------------------------------------------------|
| `skills/`           | First-party Vidoxlabs skills (MIT)              |
| `agents/`           | First-party Vidoxlabs agents (MIT)              |
| `catalog/`          | Machine-readable catalog, schema, and inventory |
| `plugins/`          | Generated platform adapters (Claude, Cursor, Copilot, OpenCode) |
| `tools/mcp-server/` | MCP server stub (stdio, read-only)              |
| `tools/vitools-sync/` | Python CLI for catalog and platform emission  |
| `scripts/`          | Catalog builder, legal gate, adapter emitter     |
| `Instructions/`     | Execution standards governance index             |
| `cookbooks/`        | External reference intake                         |
| `decisions/`        | Architecture decision records                    |

## Install a skill

See `platforms/README.md` for all platform-specific commands. Quick start:

```bash
npx skills add vidoxlabs/vitools-public/skills/<slug>
```

Or connect an MCP client:

```json
{
  "mcpServers": {
    "vidoxlabs-vitools": {
      "command": "python3",
      "args": ["tools/mcp-server/server.py"],
      "cwd": "/path/to/vitools-public"
    }
  }
}
```

## Add a skill

See `CONTRIBUTING.md` for the full guide. Quick summary:

1. Create `skills/<slug>/SKILL.md` using the canonical format.
2. Set `license: MIT`, `metadata.status: promoted`, include all required
   sections.
3. Run `python scripts/catalog-build.py` and
   `bash scripts/vitools-legal-gate.sh`.
4. Commit with message `vitools-public: add <slug> skill`.

## License and archive

- Root `LICENSE` is MIT (Copyright 2024-2026 Vidoxlabs). It covers
  first-party content in `skills/` and `agents/` only.
- `NOTICE.md` documents third-party attributions and the archive policy.
- The legal gate (`scripts/vitools-legal-gate.sh`) enforces license,
  origin, and branding rules in CI.

## Verification

```bash
python scripts/catalog-build.py              # build catalog
python scripts/catalog-build.py --validate   # validate against schema
python scripts/catalog-build.py --check-inventory  # verify completeness
bash scripts/vitools-legal-gate.sh           # license + origin checks
python scripts/emit-adapters.py              # regenerate plugin adapters
```

## Related repositories

- [vilabs](https://github.com/Vidoxlabs/vilabs) — Meta-repo, MCP fleet
- [ViDocs](https://github.com/Vidoxlabs/vidocs) — Documentation system
- [V37_Cluster](https://github.com/Vidoxlabs/v37_cluster) — Infrastructure

---

Vidoxlabs — Sovereign AI Infrastructure
