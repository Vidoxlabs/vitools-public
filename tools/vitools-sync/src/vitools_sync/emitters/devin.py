from __future__ import annotations

from pathlib import Path

from vitools_sync.emitters.base import copy_skills, load_mcp_servers, write_json


def emit_devin(root: Path, target: Path) -> list[Path]:
    written: list[Path] = []
    written.extend(copy_skills(root, target / "skills"))
    servers = load_mcp_servers(root)
    mcp_servers: dict = {}
    for name, spec in servers.items():
        entry: dict = {}
        if spec.get("transport") == "remote":
            entry["url"] = spec.get("url", "")
            entry["transport"] = spec.get("http_transport", "http")
        else:
            entry["command"] = spec.get("command", "npx")
            entry["args"] = spec.get("args", [])
            env = spec.get("env") or {}
            if env:
                entry["env"] = env
        mcp_servers[name] = entry
    written.append(write_json(target / "mcp_config.json", {"mcpServers": mcp_servers}))
    return written
