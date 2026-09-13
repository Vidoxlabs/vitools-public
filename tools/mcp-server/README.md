# ViTools MCP Server

Read-only MCP server that exposes the ViTools catalog over stdio.

## Usage

```bash
# Run the server (reads catalog/vitools.catalog.json from repo root)
python tools/mcp-server/server.py
```

## Protocol

JSON-RPC 2.0 over stdio (MCP stdio transport). No external dependencies
beyond Python 3.11+ stdlib.

## Tools

| Tool | Input | Output |
|------|-------|--------|
| `vitools_list` | `kind?`, `category?`, `tag?` | Array of public items |
| `vitools_get` | `slug` or `mcp_uri` | Single item with full metadata |
| `vitools_categories` | none | Category counts |
| `vitools_search` | `query` | Matching items |
| `vitools_install_snippet` | `slug`, `platform?` | Install command string |
| `vitools_manifest` | none | Catalog version, timestamp, commit, counts |

All tools are read-only. No write tools.

## Example session

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python tools/mcp-server/server.py
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | python tools/mcp-server/server.py
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"vitools_categories","arguments":{}}}' | python tools/mcp-server/server.py
```

## MCP client config

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

For the remote deployment, use the URL form:

```json
{
  "mcpServers": {
    "vidoxlabs-vitools": {
      "url": "https://mcp.vidoxlabs.dev/vitools"
    }
  }
}
```
