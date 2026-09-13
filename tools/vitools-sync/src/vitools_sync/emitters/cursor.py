from __future__ import annotations

from pathlib import Path

from vitools_sync.emitters.base import copy_skills, load_mcp_servers, write_json


def emit_cursor(root: Path, target: Path) -> list[Path]:
    written: list[Path] = []
    written.extend(copy_skills(root, target / "skills"))
    servers = load_mcp_servers(root)
    mcp_servers: dict = {}
    for name, spec in servers.items():
        entry: dict = {}
        transport = spec.get("transport", "stdio")
        if transport == "remote":
            entry["url"] = spec.get("url", "")
            headers = spec.get("headers") or {}
            if headers:
                entry["headers"] = headers
        else:
            entry["command"] = spec.get("command", "npx")
            entry["args"] = spec.get("args", [])
            env = spec.get("env") or {}
            if env:
                entry["env"] = env
        mcp_servers[name] = entry
    written.append(write_json(target / "mcp.json", {"mcpServers": mcp_servers}))
    return written
