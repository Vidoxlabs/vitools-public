from __future__ import annotations

import json
import shutil
from pathlib import Path

import yaml

from vitools_sync.paths import agents_dir, mcp_servers_yaml, skills_dir


def load_mcp_servers(root: Path) -> dict:
    path = mcp_servers_yaml(root)
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data.get("servers") or {}


def copy_skills(root: Path, target_skills: Path) -> list[Path]:
    written: list[Path] = []
    source = skills_dir(root)
    if not source.exists():
        return written
    target_skills.mkdir(parents=True, exist_ok=True)
    for skill_md in source.glob("*/SKILL.md"):
        dest_dir = target_skills / skill_md.parent.name
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "SKILL.md"
        shutil.copy2(skill_md, dest)
        written.append(dest)
        for extra in skill_md.parent.iterdir():
            if extra.name == "SKILL.md":
                continue
            dest_extra = dest_dir / extra.name
            if extra.is_dir():
                if dest_extra.exists():
                    shutil.rmtree(dest_extra)
                shutil.copytree(extra, dest_extra)
            else:
                shutil.copy2(extra, dest_extra)
                written.append(dest_extra)
    return written


def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path
