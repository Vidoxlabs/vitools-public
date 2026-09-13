---
name: mcp-server-building
description: >-
  Build production-ready MCP (Model Context Protocol) servers with tool
  definitions, OAuth authentication, and deployment. Use when creating
  MCP servers to expose tools, resources, or prompts to AI clients.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: mcp
  tags: [mcp, server, tools, oauth, protocol, api]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: mcp-server-building
    summary: Build and deploy MCP servers with tools and auth
  derived_from:
    - name: cloudflare-building-mcp-server-on-cloudflare
      license: Apache-2.0
      url: https://github.com/cloudflare/workers-mcp
      note: Concept only. Body rewritten.
    - name: anthropic-mcp-builder
      license: Proprietary
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# MCP Server Building

## When to use

Use this skill when building an MCP server to expose tools, resources,
or prompts to AI clients. Covers server design, tool definitions,
authentication (OAuth), and deployment.

## Procedure

1. Define the tools your server exposes: name, description, input
   schema (JSON Schema), and handler function.
2. Choose the transport: stdio for local servers, HTTP+SSE for remote.
3. Implement the MCP protocol: `initialize`, `tools/list`,
   `tools/call` handlers. Return results as structured content.
4. For remote servers: add OAuth authentication. Define the auth
   flow, token validation, and scope checking.
5. Test the server locally with an MCP client (e.g., Claude Desktop)
   before deploying.
6. Deploy: stdio servers run as local processes; remote servers deploy
   to Workers, Lambda, or any HTTP host.
7. Document the server's tools and configuration in a README.

## Guardrails

- Do not expose write tools without authentication. Read-only tools
  may be public, but mutating tools require auth.
- Do not return unstructured text as the sole output. Use structured
  content (JSON) so clients can parse it.
- Do not skip the input schema validation. Validate every tool call's
  arguments against the schema.
- Do not block on long operations. Use async handlers and return
  progress if the operation takes more than a few seconds.

## Examples

### Good

> Built an MCP server with 3 read-only tools (list, get, search) and
> 1 write tool (create) requiring OAuth. Stdio transport for local dev,
> HTTP+SSE for remote. Tested with Claude Desktop, deployed to Workers.

### Bad

> Built an MCP server that returns plain text, no input validation,
> write tools with no auth, and no documentation.

## Verification

- `tools/list` returns all defined tools with correct schemas.
- `tools/call` validates input and returns structured content.
- Auth-protected tools reject unauthenticated calls.
- Server runs without errors on the target transport.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/mcp-server-building
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: mcp-server-building
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/mcp-server-building/raw -o .cursor/skills/mcp-server-building/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/mcp-server-building.md and install it as a project skill at skills/mcp-server-building/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```
