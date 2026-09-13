# MCP Tools

MCP (Model Context Protocol) tool interfaces, catalogs, and integration
patterns for the ViTools ecosystem.

## ViTools MCP server

The ViTools catalog exposes an MCP endpoint at
`https://mcp.vidoxlabs.dev/vitools` with these read-only tools:

| Tool | Purpose |
|------|---------|
| `vitools.list` | Filter by kind, category, tag, status |
| `vitools.get` | Return one unit's frontmatter + body URL |
| `vitools.categories` | Category counts |
| `vitools.search` | Keyword over name/description/tags |
| `vitools.install_snippet` | Return platform-specific install text |
| `vitools.manifest` | Full catalog hash + version |

A local reference implementation lives at `tools/mcp-server/`.

## Adding an MCP tool reference

1. Capture the server URL, transport (stdio / http+sse / websocket), and
   auth model (none / api-key / oauth / jwt)
2. Review the tool schemas and security posture
3. Mine the useful patterns into a first-party skill
4. Link the resulting skill in the catalog

## Conventions

- Record the contract: tool surface, auth, failure behavior, observability
- Note transport and deployment requirements
- Prefer stdio for local tools, http+sse for remote
