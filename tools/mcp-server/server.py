#!/usr/bin/env python3
"""ViTools MCP Server — read-only catalog access via stdio.

Implements the MCP tool contract from docs/cleanup/06-site-mcp-contract.md.
Reads catalog/vitools.catalog.json and exposes list, get, categories,
search, install_snippet, and manifest tools.

Usage:
    python tools/mcp-server/server.py

Protocol: JSON-RPC over stdio (MCP stdio transport).
No external dependencies beyond Python 3.11+ stdlib.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parent.parent.parent / "catalog" / "vitools.catalog.json"


def load_catalog() -> dict:
    with open(CATALOG_PATH) as f:
        return json.load(f)


def handle_list(params: dict) -> list[dict]:
    catalog = load_catalog()
    items = [i for i in catalog["items"] if i.get("public", False)]
    kind = params.get("kind")
    if kind:
        items = [i for i in items if i["kind"] == kind]
    category = params.get("category")
    if category:
        items = [i for i in items if i.get("category") == category]
    tag = params.get("tag")
    if tag:
        items = [i for i in items if tag in i.get("tags", [])]
    return [
        {
            "id": i["id"],
            "kind": i["kind"],
            "slug": i["slug"],
            "title": i["title"],
            "summary": i.get("summary", ""),
            "category": i.get("category", ""),
            "tags": i.get("tags", []),
            "mcp_uri": i.get("mcp_uri", ""),
        }
        for i in items
    ]


def handle_get(params: dict) -> dict | None:
    catalog = load_catalog()
    slug = params.get("slug") or ""
    mcp_uri = params.get("mcp_uri") or ""
    for i in catalog["items"]:
        if not i.get("public"):
            continue
        if slug and i["slug"] == slug:
            return i
        if mcp_uri and i.get("mcp_uri") == mcp_uri:
            return i
    return None


def handle_categories() -> dict:
    catalog = load_catalog()
    counts: dict[str, int] = {}
    for i in catalog["items"]:
        if i.get("public"):
            cat = i.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1
    return counts


def handle_search(params: dict) -> list[dict]:
    catalog = load_catalog()
    query = params.get("query", "").lower()
    if not query:
        return []
    results = []
    for i in catalog["items"]:
        if not i.get("public"):
            continue
        haystack = " ".join([
            i.get("name", ""),
            i.get("title", ""),
            i.get("description", ""),
            i.get("summary", ""),
            " ".join(i.get("tags", [])),
        ]).lower()
        if query in haystack:
            results.append({
                "id": i["id"],
                "slug": i["slug"],
                "title": i["title"],
                "summary": i.get("summary", ""),
                "category": i.get("category", ""),
            })
    return results


def handle_install_snippet(params: dict) -> str:
    catalog = load_catalog()
    slug = params.get("slug", "")
    platform = params.get("platform", "generic")
    for i in catalog["items"]:
        if i.get("public") and i["slug"] == slug:
            return i.get("install", {}).get(platform, i.get("install", {}).get("generic", ""))
    return f"Skill '{slug}' not found."


def handle_manifest() -> dict:
    catalog = load_catalog()
    return {
        "version": catalog["version"],
        "generated_at": catalog["generated_at"],
        "source_commit": catalog["source_commit"],
        "counts": catalog["counts"],
    }


TOOL_DEFINITIONS = [
    {
        "name": "vitools_list",
        "description": "List public skills and agents. Optional filters: kind, category, tag.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": ["skill", "agent"]},
                "category": {"type": "string"},
                "tag": {"type": "string"},
            },
        },
    },
    {
        "name": "vitools_get",
        "description": "Get a single skill or agent by slug or mcp_uri.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string"},
                "mcp_uri": {"type": "string"},
            },
        },
    },
    {
        "name": "vitools_categories",
        "description": "Get category counts for public items.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "vitools_search",
        "description": "Search public items by keyword over name, description, and tags.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "vitools_install_snippet",
        "description": "Get the install command for a specific skill and platform.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string"},
                "platform": {"type": "string", "enum": ["generic", "claude-code", "cursor", "agent_prompt"]},
            },
            "required": ["slug"],
        },
    },
    {
        "name": "vitools_manifest",
        "description": "Get the catalog manifest: version, timestamp, commit, counts.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def handle_request(request: dict) -> dict:
    method = request.get("method", "")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "vitools-mcp", "version": "1.0.0"},
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOL_DEFINITIONS},
        }

    if method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        if tool_name == "vitools_list":
            result = handle_list(arguments)
        elif tool_name == "vitools_get":
            result = handle_get(arguments)
        elif tool_name == "vitools_categories":
            result = handle_categories()
        elif tool_name == "vitools_search":
            result = handle_search(arguments)
        elif tool_name == "vitools_install_snippet":
            result = handle_install_snippet(arguments)
        elif tool_name == "vitools_manifest":
            result = handle_manifest()
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
            },
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"},
    }


def main() -> None:
    if not CATALOG_PATH.exists():
        print(json.dumps({"error": f"Catalog not found at {CATALOG_PATH}"}), file=sys.stderr)
        sys.exit(1)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        else:
            response = handle_request(request)
        print(json.dumps(response))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
