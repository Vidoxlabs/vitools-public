from __future__ import annotations

from pathlib import Path

from vitools_sync.emitters.base import copy_skills, load_mcp_servers, write_json


def emit_opencode(root: Path, target: Path) -> list[Path]:
    written: list[Path] = []
    written.extend(copy_skills(root, target / "skills"))
    servers = load_mcp_servers(root)
    mcp: dict = {}
    for name, spec in servers.items():
        if spec.get("transport") == "remote":
            mcp[name] = {
                "type": "remote",
                "url": spec.get("url", ""),
                "enabled": True,
            }
            oauth = spec.get("oauth")
            if oauth:
                mcp[name]["oauth"] = oauth
        else:
            command = spec.get("command", "npx")
            args = spec.get("args") or []
            mcp[name] = {
                "type": "local",
                "command": [command, *args],
                "enabled": True,
            }
            env = spec.get("env") or {}
            if env:
                mcp[name]["env"] = env
    written.append(write_json(target / "opencode.json", {"$schema": "https://opencode.ai/config.json", "mcp": mcp}))
    return written
