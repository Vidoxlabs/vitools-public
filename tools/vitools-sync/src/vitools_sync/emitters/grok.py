from __future__ import annotations

from pathlib import Path

from vitools_sync.emitters.base import copy_skills, load_mcp_servers, write_json


def emit_grok(root: Path, target: Path) -> list[Path]:
    written: list[Path] = []
    written.extend(copy_skills(root, target / "skills"))
    servers = load_mcp_servers(root)
    grok_servers: dict = {}
    for name, spec in servers.items():
        if spec.get("transport") == "remote":
            grok_servers[name] = {"url": spec.get("url", "")}
        else:
            entry: dict = {"command": spec.get("command", "npx")}
            args = spec.get("args") or []
            if args:
                entry["args"] = args
            env = spec.get("env") or {}
            if env:
                entry["env"] = env
            grok_servers[name] = entry
    written.append(write_json(target / "mcp.json", {"servers": grok_servers}))
    return written
