# ViTools Rewrite Design Specification

**Date:** 2026-06-17
**Status:** Approved for implementation
**Owner:** vidoxlabs

## Goal

Establish a legal-first pipeline that produces Vidoxlabs-native skills and MCP metadata in `.agents/`, with optional emission to Cursor, Devin, OpenCode, Grok, Mistral Vibe, and Antigravity.

## Architecture

- **Canonical layer:** `.agents/skills/`, `.agents/mcp/servers.yaml`, `.agents/concept-cards/`, `.agents/agents/`
- **Reference archive:** `archive/vendor/` (read-only; CI blocks emission)
- **Sync CLI:** `tools/vitools-sync/` (`vitools-sync emit|install|catalog|legal`)
- **Orchestrator:** `agents/rewrite-orchestrator.md`

## Legal model

1. Concept cards capture intent only—no vendor excerpts.
2. Rewrites use official documentation as primary evidence.
3. Automated overlap gate: >15% 5-gram overlap or >80 char identical substring vs archive → block.

## Platform emission

| Platform | Output |
| -------- | ------ |
| Cursor | `mcp.json` (`mcpServers`), `skills/` |
| Devin | `mcp_config.json`, `skills/` |
| OpenCode | `opencode.json` (`mcp` typed entries), `skills/` |
| Grok | `mcp.json` (`servers`), `skills/` |
| Mistral | `config.toml.fragment`, `skills/` |
| Antigravity | `mcp_config.json` (`serverUrl`), `skills/` |

## Phases

1. **Phase 0:** Archive scaffold, MANIFEST, legal-gate CI, `.agents/` skeleton
2. **Phase 1:** vitools-sync CLI, Cursor emitter, migrate 5 native skills
3. **Phase 2:** Orchestrator, concept cards, legal overlap, pilot rewrites (tavily, context7, create-plugin)
4. **Phase 3:** All platform emitters + install command
5. **Phase 4:** Catalog inventory batch processing and Instructions lifecycle promotion

## Success criteria

1. Zero agent-facing artifacts from `archive/vendor/` (CI enforced)
2. Canonical skills pass template + legal gate before Promoted
3. Same skill installable on all six platforms via `vitools-sync`
4. Docs-first MCP skill authoring without vendor skill reference
5. Provenance: concept card + evidence URL per artifact
