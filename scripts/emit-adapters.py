#!/usr/bin/env python3
"""Emit platform adapter configs from catalog/vitools.catalog.json.

Generates:
  plugins/claude/marketplace.json
  plugins/cursor/plugin.json
  plugins/copilot/README.md
  plugins/opencode/README.md
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "catalog" / "vitools.catalog.json"
PLUGINS_DIR = ROOT / "plugins"


def main() -> None:
    with open(CATALOG_PATH) as f:
        catalog = json.load(f)

    public = [i for i in catalog["items"] if i.get("public")]
    skills = [i for i in public if i["kind"] == "skill"]
    agents = [i for i in public if i["kind"] == "agent"]

    # Claude Code marketplace
    claude_dir = PLUGINS_DIR / "claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    marketplace = {
        "name": "vitools",
        "description": "Vidoxlabs ViTools public skill and agent registry",
        "version": catalog["version"],
        "skills": [
            {"name": s["slug"], "description": s.get("summary", s["title"]), "path": s["path"]}
            for s in skills
        ],
        "agents": [
            {"name": a["slug"], "description": a.get("summary", a["title"]), "path": a["path"]}
            for a in agents
        ],
    }
    with open(claude_dir / "marketplace.json", "w") as f:
        json.dump(marketplace, f, indent=2)

    # Cursor plugin
    cursor_dir = PLUGINS_DIR / "cursor"
    cursor_dir.mkdir(parents=True, exist_ok=True)
    cursor_plugin = {
        "name": "vitools",
        "description": "Vidoxlabs ViTools public skill and agent registry",
        "version": catalog["version"],
        "skills": [
            {"name": s["slug"], "url": f"https://vidoxlabs.dev/vitools/skills/{s['slug']}/raw"}
            for s in skills
        ],
    }
    with open(cursor_dir / "plugin.json", "w") as f:
        json.dump(cursor_plugin, f, indent=2)

    # Copilot instructions
    copilot_dir = PLUGINS_DIR / "copilot"
    copilot_dir.mkdir(parents=True, exist_ok=True)
    copilot_lines = [
        "# ViTools for GitHub Copilot",
        "",
        "Install ViTools skills by fetching the raw SKILL.md from vidoxlabs.dev.",
        "",
        "## Available skills",
        "",
    ]
    for s in skills:
        copilot_lines.append(f"- **{s['slug']}**: {s.get('summary', s['title'])}")
        copilot_lines.append(f"  `curl -fsSL https://vidoxlabs.dev/vitools/skills/{s['slug']}/raw`")
    copilot_lines.extend(["", "## Available agents", ""])
    for a in agents:
        copilot_lines.append(f"- **{a['slug']}**: {a.get('summary', a['title'])}")
    with open(copilot_dir / "README.md", "w") as f:
        f.write("\n".join(copilot_lines) + "\n")

    # OpenCode instructions
    opencode_dir = PLUGINS_DIR / "opencode"
    opencode_dir.mkdir(parents=True, exist_ok=True)
    opencode_lines = [
        "# ViTools for OpenCode",
        "",
        "Install ViTools skills and agents as project instructions.",
        "",
        "## Available skills",
        "",
    ]
    for s in skills:
        opencode_lines.append(f"- **{s['slug']}**: {s.get('summary', s['title'])}")
        opencode_lines.append(f"  Fetch: `https://vidoxlabs.dev/vitools/skills/{s['slug']}/raw`")
    opencode_lines.extend(["", "## Available agents", ""])
    for a in agents:
        opencode_lines.append(f"- **{a['slug']}**: {a.get('summary', a['title'])}")
    with open(opencode_dir / "README.md", "w") as f:
        f.write("\n".join(opencode_lines) + "\n")

    print(f"Generated adapters: claude, cursor, copilot, opencode")
    print(f"  Skills: {len(skills)}, Agents: {len(agents)}")


if __name__ == "__main__":
    main()
