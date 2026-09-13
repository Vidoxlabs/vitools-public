#!/usr/bin/env python3
"""ViTools catalog builder.

Builds catalog/vitools.catalog.json from skills/ and agents/ directories.
Validates against catalog/schema.json. Checks inventory completeness.

Usage:
  python scripts/catalog-build.py              # build catalog
  python scripts/catalog-build.py --validate   # validate catalog against schema
  python scripts/catalog-build.py --check-inventory  # verify inventory completeness
"""

import os
import re
import sys
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = ROOT / "catalog"
CATALOG_FILE = CATALOG_DIR / "vitools.catalog.json"
CATALOG_MIN_FILE = CATALOG_DIR / "vitools.catalog.min.json"
SCHEMA_FILE = CATALOG_DIR / "schema.json"
INVENTORY_FILE = CATALOG_DIR / "inventory.json"

HOMEPAGE = "https://vidoxlabs.dev/vitools"
MCP_URL = "https://mcp.vidoxlabs.dev/vitools"
REPO = "https://github.com/Vidoxlabs/vitools-public"

VALID_CATEGORIES = {
    "agents",
    "automation",
    "cloud",
    "data",
    "design",
    "docs",
    "eval",
    "git",
    "infra",
    "mcp",
    "research",
    "safety",
    "security",
    "web",
}

REQUIRED_SECTIONS = ["when", "procedure", "guardrails", "examples", "verification"]


def extract_frontmatter(content):
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            return content[3:end].strip(), content[end + 3 :]
    return "", content


def fm_get(fm, key):
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else ""


def fm_get_yaml_block(fm, key):
    """Extract a YAML block value (for metadata: section)."""
    m = re.search(rf"^{re.escape(key)}:\s*\n((?:\s+.+\n?)+)", fm, re.M)
    return m.group(1) if m else ""


def has_section(body, *patterns):
    for p in patterns:
        if re.search(p, body, re.I):
            return True
    return False


def get_git_sha():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def canonical_raw_url(slug, kind):
    path_prefix = "skills" if kind == "skill" else "agents"
    return f"https://vidoxlabs.dev/vitools/raw/{path_prefix}/{slug}.md"


def generate_install_snippets(slug, kind):
    """Proven URL-based install strings only.

    Repository installers (npx skills add, Claude marketplace) follow GitHub
    default main and are omitted until that revision equals this admission set.
    """
    path_prefix = "skills" if kind == "skill" else "agents"
    entry_file = "SKILL.md" if kind == "skill" else "AGENT.md"
    raw = canonical_raw_url(slug, kind)
    dest = (
        f".cursor/skills/{slug}/{entry_file}"
        if kind == "skill"
        else f".cursor/agents/{slug}/{entry_file}"
    )
    follow = "Procedure" if kind == "skill" else "Operating loop"
    noun = "skill" if kind == "skill" else "agent"
    return {
        "cursor": f"curl -fsSL {raw} -o {dest}",
        "agent_prompt": (
            f"Fetch {raw} and install it as a project {noun} at "
            f"{path_prefix}/{slug}/{entry_file}. Follow its {follow}. "
            f"Do not modify Guardrails."
        ),
    }


def check_required_sections(body):
    """Check for required body sections."""
    checks = {
        "when": has_section(body, r"## (When to use|When to Use|Usage)"),
        "procedure": has_section(
            body, r"## (Procedure|Process|Workflow|Mandatory Procedure)"
        ),
        "guardrails": has_section(
            body, r"## (Guardrails?|Guidelines|Mandatory Guidelines)"
        ),
        "examples": has_section(body, r"## Examples?"),
        "verification": has_section(body, r"## Verification"),
    }
    return checks


def parse_skill(slug, skill_md_path):
    """Parse a SKILL.md file and return a catalog item or None."""
    with open(skill_md_path, "r", errors="replace") as f:
        content = f.read()
    fm, body = extract_frontmatter(content)

    name = fm_get(fm, "name")
    license_val = fm_get(fm, "license")
    description_m = re.search(
        r"description:\s*[>|]?\s*\n?(.*?)(?:\n[a-z_-]+:|\n---|\Z)",
        fm,
        re.S,
    )
    description = description_m.group(1).strip() if description_m else ""

    # Parse metadata block
    meta_block = fm_get_yaml_block(fm, "metadata")
    kind = "skill"
    status = "intake"
    origin = "vidoxlabs"
    category = "automation"
    tags = []
    platforms = ["generic"]
    summary = ""

    if meta_block:
        kind_m = re.search(r"kind:\s*(\w+)", meta_block)
        if kind_m:
            kind = kind_m.group(1)
        status_m = re.search(r"status:\s*(\w+)", meta_block)
        if status_m:
            status = status_m.group(1)
        origin_m = re.search(r"origin:\s*(\w+)", meta_block)
        if origin_m:
            origin = origin_m.group(1)
        cat_m = re.search(r"category:\s*(\w+)", meta_block)
        if cat_m:
            category = cat_m.group(1)
        tags_m = re.search(r"tags:\s*\[([^\]]*)\]", meta_block)
        if tags_m:
            tags = [t.strip() for t in tags_m.group(1).split(",")]
        plat_m = re.search(r"platforms:\s*\[([^\]]*)\]", meta_block)
        if plat_m:
            platforms = [p.strip() for p in plat_m.group(1).split(",")]
        sum_m = re.search(r"summary:\s*(.+)", meta_block)
        if sum_m:
            summary = sum_m.group(1).strip()

    # Check required sections
    sections = check_required_sections(body)
    all_sections_present = all(sections.values())

    # Determine public status
    is_public = status == "promoted" and all_sections_present and license_val == "MIT"

    # Title from first heading
    title_m = re.search(r"^#\s+(.+)$", body, re.M)
    title = title_m.group(1).strip() if title_m else slug.replace("-", " ").title()

    # Validate category
    if category not in VALID_CATEGORIES:
        category = "automation"

    item = {
        "id": f"{kind}:{slug}",
        "kind": kind,
        "slug": slug,
        "name": name or slug,
        "title": title,
        "description": description[:1024],
        "summary": summary or description[:120],
        "license": license_val or "MIT",
        "origin": origin,
        "status": status,
        "public": is_public,
        "category": category,
        "tags": tags,
        "platforms": platforms,
        "path": f"skills/{slug}/SKILL.md",
        "html_url": f"{HOMEPAGE}/skills/{slug}",
        "raw_url": canonical_raw_url(slug, "skill"),
        "mcp_uri": f"vitools://skill/{slug}",
        "install": generate_install_snippets(slug, "skill"),
    }

    # Parse derived_from if present
    derived_m = re.search(r"derived_from:\s*\n((?:\s+-\s+.+\n?)+)", meta_block, re.M)
    if derived_m:
        item["derived_from"] = []
        for line in derived_m.group(1).strip().split("\n"):
            name_m2 = re.search(r"name:\s*(.+)", line)
            if name_m2:
                item["derived_from"].append(
                    {
                        "name": name_m2.group(1).strip(),
                        "license": "Apache-2.0",
                    }
                )

    return item


def parse_agent(slug, agent_md_path):
    """Parse an AGENT.md file and return a catalog item."""
    with open(agent_md_path, "r", errors="replace") as f:
        content = f.read()
    fm, body = extract_frontmatter(content)

    name = fm_get(fm, "name")
    description_m = re.search(r"description:\s*(.+)", fm, re.S)
    description = description_m.group(1).strip() if description_m else ""

    title_m = re.search(r"^#\s+(.+)$", body, re.M)
    title = title_m.group(1).strip() if title_m else slug.replace("-", " ").title()

    # Agents have different required sections
    sections = {
        "when": has_section(body, r"## (When to use|When to Use|Role)"),
        "guardrails": has_section(body, r"## Guardrails"),
        "verification": has_section(body, r"## Verification"),
    }
    all_present = all(sections.values())

    is_public = all_present

    return {
        "id": f"agent:{slug}",
        "kind": "agent",
        "slug": slug,
        "name": name or slug,
        "title": title,
        "description": description[:1024],
        "summary": description[:120],
        "license": "MIT",
        "origin": "vidoxlabs",
        "status": "promoted" if is_public else "intake",
        "public": is_public,
        "category": "agents",
        "tags": ["agents"],
        "platforms": ["claude-code", "cursor", "copilot", "opencode", "generic"],
        "path": f"agents/{slug}/AGENT.md",
        "html_url": f"{HOMEPAGE}/agents/{slug}",
        "raw_url": canonical_raw_url(slug, "agent"),
        "mcp_uri": f"vitools://agent/{slug}",
        "install": generate_install_snippets(slug, "agent"),
    }


def build_catalog():
    """Build the catalog from skills/ and agents/ directories."""
    items = []

    # Skills
    skills_dir = ROOT / "skills"
    if skills_dir.is_dir():
        for entry in sorted(os.listdir(skills_dir)):
            skill_md = skills_dir / entry / "SKILL.md"
            if not skill_md.is_file():
                continue
            item = parse_skill(entry, skill_md)
            if item:
                items.append(item)

    # Agents
    agents_dir = ROOT / "agents"
    if agents_dir.is_dir():
        for entry in sorted(os.listdir(agents_dir)):
            agent_md = agents_dir / entry / "AGENT.md"
            if not agent_md.is_file():
                # Try .md file directly in agents/
                agent_md = agents_dir / entry
                if not agent_md.is_file() or not entry.endswith(".md"):
                    continue
                slug = entry.replace(".md", "")
                item = parse_agent(slug, agent_md)
                if item:
                    items.append(item)
            else:
                item = parse_agent(entry, agent_md)
                if item:
                    items.append(item)

    # Archived vendor count is 0 (vendor originals not in repo)
    archived_count = 0

    # Count public items
    public_skills = sum(1 for i in items if i["kind"] == "skill" and i["public"])
    public_agents = sum(1 for i in items if i["kind"] == "agent" and i["public"])

    catalog = {
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_commit": get_git_sha(),
        "homepage": HOMEPAGE,
        "mcp": MCP_URL,
        "repo": REPO,
        "counts": {
            "skills": public_skills,
            "agents": public_agents,
            "archived_vendor": archived_count,
        },
        "items": items,
    }

    # Write full catalog
    with open(CATALOG_FILE, "w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"Built {CATALOG_FILE}")
    print(f"  Public skills: {public_skills}")
    print(f"  Public agents: {public_agents}")
    print(f"  Archived vendor: {archived_count}")
    print(f"  Total items (including non-public): {len(items)}")

    # Write minimal catalog (public items only, compact)
    min_catalog = {
        "version": catalog["version"],
        "generated_at": catalog["generated_at"],
        "source_commit": catalog["source_commit"],
        "counts": catalog["counts"],
        "items": [
            {
                "id": i["id"],
                "kind": i["kind"],
                "slug": i["slug"],
                "title": i["title"],
                "summary": i["summary"],
                "category": i["category"],
                "tags": i["tags"],
                "path": i["path"],
                "html_url": i["html_url"],
                "mcp_uri": i["mcp_uri"],
                "install": i["install"],
            }
            for i in items
            if i["public"]
        ],
    }
    with open(CATALOG_MIN_FILE, "w") as f:
        json.dump(min_catalog, f, separators=(",", ":"))
    print(f"Built {CATALOG_MIN_FILE}")

    return catalog


def validate_catalog():
    """Validate catalog against schema.json (basic structural check)."""
    if not CATALOG_FILE.exists():
        print("ERROR: catalog/vitools.catalog.json does not exist. Run build first.")
        return False

    with open(CATALOG_FILE) as f:
        catalog = json.load(f)

    errors = []

    # Check top-level fields
    for field in [
        "version",
        "generated_at",
        "source_commit",
        "homepage",
        "mcp",
        "repo",
        "counts",
        "items",
    ]:
        if field not in catalog:
            errors.append(f"missing top-level field: {field}")

    # Check counts match
    public_skills = sum(
        1 for i in catalog["items"] if i.get("kind") == "skill" and i.get("public")
    )
    public_agents = sum(
        1 for i in catalog["items"] if i.get("kind") == "agent" and i.get("public")
    )
    if catalog.get("counts", {}).get("skills") != public_skills:
        errors.append(
            f"counts.skills ({catalog['counts']['skills']}) != actual public skills ({public_skills})"
        )
    if catalog.get("counts", {}).get("agents") != public_agents:
        errors.append(
            f"counts.agents ({catalog['counts']['agents']}) != actual public agents ({public_agents})"
        )

    # Check each item
    for item in catalog["items"]:
        if item.get("public"):
            # Public items must have required fields
            for field in [
                "id",
                "kind",
                "slug",
                "name",
                "title",
                "description",
                "license",
                "origin",
                "status",
                "public",
                "category",
                "tags",
                "platforms",
                "path",
                "html_url",
                "raw_url",
                "mcp_uri",
                "install",
            ]:
                if field not in item:
                    errors.append(
                        f"item {item.get('slug', '?')}: missing field {field}"
                    )

            # Category must be valid
            if item.get("category") not in VALID_CATEGORIES:
                errors.append(
                    f"item {item['slug']}: invalid category '{item.get('category')}'"
                )

            # mcp_uri format
            mcp_uri = item.get("mcp_uri", "")
            if not re.match(r"^vitools://(skill|agent)/[a-z0-9-]+$", mcp_uri):
                errors.append(f"item {item['slug']}: invalid mcp_uri '{mcp_uri}'")

    if errors:
        print(f"VALIDATION FAILED: {len(errors)} error(s)")
        for e in errors:
            print(f"  - {e}")
        return False

    print("VALIDATION PASSED")
    return True


def check_inventory():
    """Verify inventory completeness — every skill/plugin/agent dir is in inventory.json."""
    if not INVENTORY_FILE.exists():
        print("ERROR: catalog/inventory.json does not exist.")
        return False

    with open(INVENTORY_FILE) as f:
        inv = json.load(f)

    inv_paths = {i["path"] for i in inv.get("items", [])}

    missing = []

    # Check skills/
    skills_dir = ROOT / "skills"
    if skills_dir.is_dir():
        for entry in sorted(os.listdir(skills_dir)):
            path = f"skills/{entry}"
            if path not in inv_paths:
                # Could be a file or dir
                full = skills_dir / entry
                if full.is_dir():
                    skill_md = full / "SKILL.md"
                    if skill_md.exists():
                        missing.append(f"{path}/ (has SKILL.md)")
                    else:
                        missing.append(f"{path}/ (no SKILL.md)")
                else:
                    missing.append(path)

    # Check plugins/
    plugins_dir = ROOT / "plugins"
    if plugins_dir.is_dir():
        for entry in sorted(os.listdir(plugins_dir)):
            path = f"plugins/{entry}"
            if path not in inv_paths:
                missing.append(path)

    # Check agents/
    agents_dir = ROOT / "agents"
    if agents_dir.is_dir():
        for entry in sorted(os.listdir(agents_dir)):
            path = f"agents/{entry}"
            if path not in inv_paths:
                missing.append(path)

    if missing:
        print(
            f"INVENTORY INCOMPLETE: {len(missing)} item(s) missing from inventory.json"
        )
        for m in missing:
            print(f"  - {m}")
        return False

    print(f"INVENTORY COMPLETE: {len(inv_paths)} items accounted for")
    return True


def main():
    if "--validate" in sys.argv:
        ok = validate_catalog()
        sys.exit(0 if ok else 1)
    elif "--check-inventory" in sys.argv:
        ok = check_inventory()
        sys.exit(0 if ok else 1)
    else:
        build_catalog()


if __name__ == "__main__":
    main()
