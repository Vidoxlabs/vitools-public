from __future__ import annotations

from pathlib import Path


def repo_root(start: Path | None = None) -> Path:
    """Walk up from start (or cwd) to find vitools repo root (has .agents/)."""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".agents").is_dir() and (candidate / "AGENTS.md").exists():
            return candidate
    raise FileNotFoundError("Could not locate vitools repo root (missing .agents/ + AGENTS.md)")


def agents_dir(root: Path) -> Path:
    return root / ".agents"


def skills_dir(root: Path) -> Path:
    return agents_dir(root) / "skills"


def mcp_servers_yaml(root: Path) -> Path:
    return agents_dir(root) / "mcp" / "servers.yaml"


def archive_vendor(root: Path) -> Path:
    return root / "archive" / "vendor"
