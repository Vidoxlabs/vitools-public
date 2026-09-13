from __future__ import annotations

import json
import yaml
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from vitools_sync.paths import archive_vendor, repo_root


def extract_lifecycle_from_skill(skill_file: Path) -> dict[str, Any]:
    """Extract lifecycle information from a skill's frontmatter."""
    lifecycle_info = {}
    
    try:
        with open(skill_file) as f:
            content = f.read()
        
        # Extract frontmatter
        if not content.startswith("---"):
            return lifecycle_info
        
        end_frontmatter = content.find("---", 3)
        if end_frontmatter == -1:
            return lifecycle_info
        
        frontmatter_str = content[3:end_frontmatter].strip()
        frontmatter = yaml.safe_load(frontmatter_str) or {}
        
        # Extract lifecycle-related fields, converting dates to strings
        lifecycle_info["lifecycle"] = str(frontmatter.get("Lifecycle", "")) if frontmatter.get("Lifecycle") else None
        
        # Convert date/datetime objects to strings
        for field in ["Created", "Updated", "Promoted", "Deprecated"]:
            value = frontmatter.get(field)
            if value is not None:
                lifecycle_info[field.lower()] = str(value)
            else:
                lifecycle_info[field.lower()] = None
        
        lifecycle_info["promoted_by"] = str(frontmatter.get("PromotedBy", "")) if frontmatter.get("PromotedBy") else None
        lifecycle_info["deprecated_reason"] = str(frontmatter.get("DeprecatedReason", "")) if frontmatter.get("DeprecatedReason") else None
        
    except Exception:
        pass
    
    return lifecycle_info


@dataclass
class InventoryEntry:
    id: str
    kind: str
    path: str
    status: str
    source_url: str | None = None
    upstream_license: str | None = None
    lifecycle: str | None = None  # Lifecycle state for skills
    created: str | None = None  # Creation date
    updated: str | None = None  # Last update date
    promoted: str | None = None  # Promotion date
    promoted_by: str | None = None  # Who promoted
    deprecated: str | None = None  # Deprecation date
    deprecated_reason: str | None = None  # Reason for deprecation


def build_inventory(root: Path | None = None) -> list[dict]:
    root = root or repo_root()
    entries: list[InventoryEntry] = []

    manifest_path = archive_vendor(root) / "MANIFEST.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for pkg in manifest.get("archived_packages") or []:
            entries.append(
                InventoryEntry(
                    id=pkg.get("id", pkg.get("name", "unknown")),
                    kind="archived_package",
                    path=pkg.get("archive_path", ""),
                    status=pkg.get("status", "pending"),
                    source_url=pkg.get("source_url"),
                    upstream_license=pkg.get("upstream_license"),
                )
            )
        for tool in manifest.get("mcp_fleet_inventory") or []:
            entries.append(
                InventoryEntry(
                    id=f"mcp-{tool['name']}",
                    kind="mcp_tool",
                    path=f"vilabs/tools/vilabs_mcp/vitools/{tool['name']}",
                    status="native",
                    upstream_license=tool.get("license"),
                )
            )

    plugins_dir = root / "plugins"
    if plugins_dir.is_dir():
        for plugin_dir in sorted(plugins_dir.iterdir()):
            if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
                continue
            entries.append(
                InventoryEntry(
                    id=f"plugin-{plugin_dir.name}",
                    kind="plugin",
                    path=str(plugin_dir.relative_to(root)),
                    status="pending",
                )
            )

    skills_dir = root / "skills"
    if skills_dir.is_dir():
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
                continue
            native = skill_dir.name in {
                "skill-mining",
                "skills-template",
                "evidence-answering",
                "v37-validation",
                "vidoxlabs-core-architect",
            }
            
            # Extract lifecycle information
            skill_file = skill_dir / "SKILL.md"
            lifecycle_info = extract_lifecycle_from_skill(skill_file)
            
            # Determine status
            status = "promoted" if native else "pending"
            if lifecycle_info.get("lifecycle"):
                status = lifecycle_info["lifecycle"].lower()
            
            entries.append(
                InventoryEntry(
                    id=f"skill-{skill_dir.name}",
                    kind="skill",
                    path=str(skill_dir.relative_to(root)),
                    status=status,
                    lifecycle=lifecycle_info.get("lifecycle"),
                    created=lifecycle_info.get("created"),
                    updated=lifecycle_info.get("updated"),
                    promoted=lifecycle_info.get("promoted"),
                    promoted_by=lifecycle_info.get("promoted_by"),
                    deprecated=lifecycle_info.get("deprecated"),
                    deprecated_reason=lifecycle_info.get("deprecated_reason"),
                )
            )

    concept_dir = root / "tools" / "concept-cards"
    if concept_dir.is_dir():
        for card in sorted(concept_dir.glob("*.yaml")):
            entries.append(
                InventoryEntry(
                    id=f"concept-{card.stem}",
                    kind="concept_card",
                    path=str(card.relative_to(root)),
                    status="concept_extracted",
                )
            )

    agents_skills = root / "skills"
    if agents_skills.is_dir():
        for skill_dir in sorted(agents_skills.iterdir()):
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                # Extract lifecycle information
                lifecycle_info = extract_lifecycle_from_skill(skill_file)
                
                # Determine status based on lifecycle
                status = "rewritten"
                if lifecycle_info.get("lifecycle"):
                    status = lifecycle_info["lifecycle"].lower()
                
                entries.append(
                    InventoryEntry(
                        id=f"canonical-{skill_dir.name}",
                        kind="canonical_skill",
                        path=str(skill_dir.relative_to(root)),
                        status=status,
                        lifecycle=lifecycle_info.get("lifecycle"),
                        created=lifecycle_info.get("created"),
                        updated=lifecycle_info.get("updated"),
                        promoted=lifecycle_info.get("promoted"),
                        promoted_by=lifecycle_info.get("promoted_by"),
                        deprecated=lifecycle_info.get("deprecated"),
                        deprecated_reason=lifecycle_info.get("deprecated_reason"),
                    )
                )

    return [asdict(e) for e in entries]


def write_inventory(root: Path, inventory: list[dict], output: Path | None = None) -> Path:
    path = output or (root / "tools" / "vitools-sync" / "catalog" / "inventory.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"entries": inventory}, indent=2) + "\n", encoding="utf-8")
    return path
