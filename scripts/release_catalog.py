#!/usr/bin/env python3
"""Generate the public ViTools release from catalog/release-admission.json.

The release is the admitted identities only. Skill and agent bodies are read
from the immutable body-source commit. The site catalog-release pin is
recorded and checked, and it is not written into raw URLs. Release files are
replaced only after the admission, pins, digests, and output set all match.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = ROOT / "catalog"
ADMISSION_FILE = CATALOG_DIR / "release-admission.json"
CATALOG_FILE = CATALOG_DIR / "vitools.catalog.json"
CATALOG_MIN_FILE = CATALOG_DIR / "vitools.catalog.min.json"
PLUGINS_DIR = ROOT / "plugins"

MIN_FIELDS = (
    "id",
    "kind",
    "slug",
    "title",
    "summary",
    "category",
    "tags",
    "path",
    "html_url",
    "mcp_uri",
    "install",
)


class ReleaseError(RuntimeError):
    """The release set is not safe to publish."""


def load_admission(path: Path = ADMISSION_FILE) -> dict:
    if not path.is_file():
        raise ReleaseError(f"missing admission source {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    ids = data.get("ids")
    if not isinstance(ids, list) or not ids:
        raise ReleaseError("missing admission ids")
    if len(ids) != len(set(ids)):
        raise ReleaseError("duplicate admission ids")
    bodies = data.get("bodies")
    if not isinstance(bodies, dict) or set(bodies) != set(ids):
        raise ReleaseError("admission body digests do not match the ids")
    for key in ("body_source_commit", "catalog_release_commit", "generated_at"):
        if not data.get(key):
            raise ReleaseError(f"missing admission field {key}")
    return data


def verify_commit(sha: str, root: Path = ROOT) -> str:
    try:
        resolved = subprocess.check_output(
            ["git", "rev-parse", "--verify", f"{sha}^{{commit}}"],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise ReleaseError(f"unresolved pin {sha}") from exc
    return resolved


def verify_ancestor(ancestor: str, descendant: str, root: Path = ROOT) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=root,
        check=False,
    )
    if result.returncode != 0:
        raise ReleaseError(f"{ancestor} is not an ancestor of {descendant}")


def body_bytes(pin: str, path: str, root: Path = ROOT) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "show", f"{pin}:{path}"],
            cwd=root,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as exc:
        raise ReleaseError(f"missing body {path} at {pin}") from exc


def assert_exact(items: list[dict], admission: dict) -> None:
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise ReleaseError("duplicate release ids")
    if ids != admission["ids"]:
        raise ReleaseError("widened or incomplete release output")


def select_items(catalog: dict, admission: dict, root: Path = ROOT) -> list[dict]:
    by_id: dict[str, dict] = {}
    for item in catalog.get("items", []):
        item_id = item.get("id")
        if item_id in by_id:
            raise ReleaseError(f"duplicate catalog id {item_id}")
        by_id[item_id] = item
    body_pin = admission["body_source_commit"]
    site_pin = admission["catalog_release_commit"]
    selected = []
    for item_id in admission["ids"]:
        item = by_id.get(item_id)
        if item is None:
            raise ReleaseError(f"missing admission {item_id}")
        path = item.get("path") or ""
        digest = hashlib.sha256(body_bytes(body_pin, path, root)).hexdigest()
        if digest != admission["bodies"][item_id]:
            raise ReleaseError(f"body digest mismatch for {item_id}")
        raw_url = item.get("raw_url") or ""
        if body_pin not in raw_url or "/main/" in raw_url or site_pin in raw_url:
            raise ReleaseError(f"raw url does not use the body pin for {item_id}")
        if item.get("public") is not True:
            raise ReleaseError(f"{item_id} is not public")
        selected.append(item)
    assert_exact(selected, admission)
    return selected


def build_documents(items: list[dict], admission: dict) -> tuple[dict, dict]:
    assert_exact(items, admission)
    skills = sum(1 for item in items if item["kind"] == "skill")
    agents = sum(1 for item in items if item["kind"] == "agent")
    full = {
        "version": "1.0.0",
        "generated_at": admission["generated_at"],
        "source_commit": admission["body_source_commit"],
        "homepage": "https://vidoxlabs.dev/vitools",
        "mcp": "https://mcp.vidoxlabs.dev/vitools",
        "repo": "https://github.com/Vidoxlabs/vitools-public",
        "counts": {
            "skills": skills,
            "agents": agents,
            "archived_vendor": admission["archived_vendor"],
        },
        "items": items,
    }
    minimal = {
        "version": full["version"],
        "generated_at": full["generated_at"],
        "source_commit": full["source_commit"],
        "counts": full["counts"],
        "items": [{key: item[key] for key in MIN_FIELDS} for item in items],
    }
    return full, minimal


def render_adapters(full: dict) -> dict[str, str]:
    public = [item for item in full["items"] if item.get("public")]
    skills = [item for item in public if item["kind"] == "skill"]
    agents = [item for item in public if item["kind"] == "agent"]
    marketplace = {
        "name": "vitools",
        "description": "Vidoxlabs ViTools public skill and agent registry",
        "version": full["version"],
        "skills": [
            {"name": item["slug"], "description": item.get("summary", item["title"]), "path": item["path"]}
            for item in skills
        ],
        "agents": [
            {"name": item["slug"], "description": item.get("summary", item["title"]), "path": item["path"]}
            for item in agents
        ],
    }
    cursor = {
        "name": "vitools",
        "description": "Vidoxlabs ViTools public skill and agent registry",
        "version": full["version"],
        "skills": [
            {"name": item["slug"], "url": f"https://vidoxlabs.dev/vitools/skills/{item['slug']}/raw"}
            for item in skills
        ],
    }
    copilot = ["# ViTools for GitHub Copilot", "", "Install ViTools skills by fetching the raw SKILL.md from vidoxlabs.dev.", "", "## Available skills", ""]
    for item in skills:
        copilot.append(f"- **{item['slug']}**: {item.get('summary', item['title'])}")
        copilot.append(f"  `curl -fsSL https://vidoxlabs.dev/vitools/skills/{item['slug']}/raw`")
    copilot.extend(["", "## Available agents", ""])
    for item in agents:
        copilot.append(f"- **{item['slug']}**: {item.get('summary', item['title'])}")
    opencode = ["# ViTools for OpenCode", "", "Install ViTools skills and agents as project instructions.", "", "## Available skills", ""]
    for item in skills:
        opencode.append(f"- **{item['slug']}**: {item.get('summary', item['title'])}")
        opencode.append(f"  Fetch: `https://vidoxlabs.dev/vitools/skills/{item['slug']}/raw`")
    opencode.extend(["", "## Available agents", ""])
    for item in agents:
        opencode.append(f"- **{item['slug']}**: {item.get('summary', item['title'])}")
    return {
        "plugins/claude/marketplace.json": json.dumps(marketplace, indent=2) + "\n",
        "plugins/cursor/plugin.json": json.dumps(cursor, indent=2) + "\n",
        "plugins/copilot/README.md": "\n".join(copilot) + "\n",
        "plugins/opencode/README.md": "\n".join(opencode) + "\n",
    }


def render(root: Path = ROOT) -> dict[str, str]:
    admission = load_admission(root / "catalog" / "release-admission.json")
    verify_commit(admission["body_source_commit"], root)
    verify_commit(admission["catalog_release_commit"], root)
    head = verify_commit("HEAD", root)
    verify_ancestor(admission["catalog_release_commit"], head, root)
    verify_ancestor(admission["body_source_commit"], head, root)
    catalog = json.loads((root / "catalog" / "vitools.catalog.json").read_text(encoding="utf-8"))
    items = select_items(catalog, admission, root)
    full, minimal = build_documents(items, admission)
    if full["source_commit"] != admission["body_source_commit"]:
        raise ReleaseError("source commit drifted from the body pin")
    if len(full["items"]) != len(admission["ids"]):
        raise ReleaseError("widened release catalog")
    documents = {
        "catalog/vitools.catalog.json": json.dumps(full, indent=2, ensure_ascii=False) + "\n",
        "catalog/vitools.catalog.min.json": json.dumps(minimal, separators=(",", ":"), ensure_ascii=False) + "\n",
    }
    documents.update(render_adapters(full))
    return documents


def replace_files(documents: dict[str, str], root: Path = ROOT) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for relative, text in documents.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(target.name + ".release-tmp")
            temporary.write_text(text, encoding="utf-8")
            staged.append((temporary, target))
        for temporary, target in staged:
            temporary.replace(target)
    except Exception:
        for temporary, _target in staged:
            temporary.unlink(missing_ok=True)
        raise


def check(root: Path = ROOT) -> None:
    documents = render(root)
    again = render(root)
    if documents != again:
        raise ReleaseError("two release builds were not equivalent")
    mismatches = [
        relative
        for relative, text in documents.items()
        if not (root / relative).is_file() or (root / relative).read_text(encoding="utf-8") != text
    ]
    if mismatches:
        raise ReleaseError("release files differ from the admitted generation: " + ", ".join(mismatches))


def write(root: Path = ROOT) -> None:
    documents = render(root)
    again = render(root)
    if documents != again:
        raise ReleaseError("two release builds were not equivalent")
    replace_files(documents, root)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    try:
        if args == ["--check"]:
            check()
            print("release check passed")
            return 0
        if args == ["--write"]:
            write()
            print("release files replaced")
            return 0
    except ReleaseError as exc:
        print(f"RELEASE REFUSED: {exc}", file=sys.stderr)
        return 1
    print("usage: python3 scripts/release_catalog.py --check|--write", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
