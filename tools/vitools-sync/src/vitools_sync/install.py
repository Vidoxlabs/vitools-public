from __future__ import annotations

import shutil
from pathlib import Path

from vitools_sync.emitters import emit_platform
from vitools_sync.paths import repo_root

USER_PATHS = {
    "cursor": {
        "skills": Path.home() / ".cursor" / "skills",
        "mcp": Path.home() / ".cursor" / "mcp.json",
    },
    "devin": {
        "skills": Path.home() / ".devin" / "skills",
        "mcp": Path.home() / ".codeium" / "windsurf" / "mcp_config.json",
    },
    "grok": {
        "skills": Path.home() / ".grok" / "skills",
        "mcp": Path.home() / ".grok" / "mcp.json",
    },
    "mistral": {
        "skills": Path.home() / ".vibe" / "skills",
    },
    "antigravity": {
        "skills": Path.home() / ".gemini" / "skills",
        "mcp": Path.home() / ".gemini" / "config" / "mcp_config.json",
    },
    "opencode": {
        "skills": Path.home() / ".config" / "opencode" / "skills",
    },
}


def install_platform(
    root: Path | None,
    platform: str,
    *,
    user: bool,
    dry_run: bool,
) -> list[str]:
    root = root or repo_root()
    staging = root / "platforms" / platform
    emit_platform(root, platform, staging)
    actions: list[str] = []
    if not user:
        actions.append(f"Project emit refreshed at {staging}")
        return actions

    paths = USER_PATHS.get(platform, {})
    for key, dest in paths.items():
        if key == "skills":
            source = staging / "skills"
            if source.exists():
                if dry_run:
                    actions.append(f"Would copy {source} -> {dest}")
                else:
                    dest.mkdir(parents=True, exist_ok=True)
                    for item in source.iterdir():
                        target = dest / item.name
                        if item.is_dir():
                            if target.exists():
                                shutil.rmtree(target)
                            shutil.copytree(item, target)
                        else:
                            shutil.copy2(item, target)
                    actions.append(f"Copied skills to {dest}")
        elif key == "mcp":
            for candidate in ["mcp.json", "mcp_config.json", "opencode.json"]:
                source = staging / candidate
                if source.exists():
                    if dry_run:
                        actions.append(f"Would copy {source} -> {dest}")
                    else:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, dest)
                        actions.append(f"Copied MCP config to {dest}")
                    break
    return actions
