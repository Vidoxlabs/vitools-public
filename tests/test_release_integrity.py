#!/usr/bin/env python3
"""Mission 14 public-release integrity: 5+4 admission, provenance, install URLs."""

from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = [
    "data-loss-prevention",
    "evidence-answering",
    "skill-mining",
    "skills-template",
    "v37-validation",
]
AGENTS = [
    "legal-gate",
    "rewrite-orchestrator",
    "skill-author",
    "vitools-catalog-maintainer",
]
# Post-repair body hashes (canonical /vitools/raw Install sections).
GOLDEN_BODIES = {
    (
        "skill",
        "data-loss-prevention",
    ): "39ec2e75e411375ffbfc6f9b14763cfbf0f326fe3b77c7a9151c1f38094e36ef",
    (
        "skill",
        "evidence-answering",
    ): "d5e550bb8b3f0ef5f0a46bc207f557bc84ab26e3c33f3c68e461daf746064130",
    (
        "skill",
        "skill-mining",
    ): "0bf551e3c64b7c1e2ad006124ba9d0969bba43048132e0abcc408879bb850569",
    (
        "skill",
        "skills-template",
    ): "e854d9d96ad4d5c26d8f416e57d3c3f75283a92b63c6609c1af6694c8e5e0fec",
    (
        "skill",
        "v37-validation",
    ): "9866aebe942f3508f63c165f2ed46ad73525b34f30e65fb13ee3c630b31c038f",
    (
        "agent",
        "legal-gate",
    ): "53d9b4dc504aeef27a0dfe3e7306e9558236350431717424929dd7e1e53cae74",
    (
        "agent",
        "rewrite-orchestrator",
    ): "41fb9aff15e69cfb0008165c40bb9cf9e1e2b9cda1bc9eab02d6168ee3035c7c",
    (
        "agent",
        "skill-author",
    ): "5ec96c890511a1aba6690c73eaa4d86c11d509541680e75f1feb820f2c0e5e0f",
    (
        "agent",
        "vitools-catalog-maintainer",
    ): "c59b66cd5ff036dd79b0c8fdf1bd8edb33de96e3eb0a714a0ac6b95556a1a36a",
}
# Preflight hash of tools/MCP_Tools.md on origin/main (7bd4ba9). Must not change.
PROTECTED_MCP = "75ef686c05cbeb9e25b8ef693cc1585b2226af8d9794cde577d740c4d24c4d15"

LEGACY_404 = re.compile(
    r"https://vidoxlabs\.dev/vitools/(?:skills|agents)/[a-z0-9-]+(?:/raw|\.md)"
)
CANONICAL_RAW = re.compile(
    r"^https://vidoxlabs\.dev/vitools/raw/(skills|agents)/([a-z0-9-]+)\.md$"
)
MOVING_MAIN = re.compile(
    r"https://raw\.githubusercontent\.com/Vidoxlabs/vitools-public/main/"
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def catalog() -> dict:
    return json.loads((ROOT / "catalog/vitools.catalog.json").read_text())


def body_path(kind: str, slug: str) -> Path:
    if kind == "skill":
        return ROOT / "skills" / slug / "SKILL.md"
    return ROOT / "agents" / slug / "AGENT.md"


class ReleaseIntegrityTests(unittest.TestCase):
    def test_admission_is_exactly_the_nine_approved_slugs(self):
        skill_dirs = sorted(
            p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()
        )
        agent_dirs = sorted(
            p.name for p in (ROOT / "agents").iterdir() if (p / "AGENT.md").is_file()
        )
        self.assertEqual(skill_dirs, SKILLS)
        self.assertEqual(agent_dirs, AGENTS)
        items = catalog()["items"]
        public = [i for i in items if i.get("public") and i.get("status") == "promoted"]
        self.assertEqual(
            sorted(i["slug"] for i in public if i["kind"] == "skill"), SKILLS
        )
        self.assertEqual(
            sorted(i["slug"] for i in public if i["kind"] == "agent"), AGENTS
        )
        self.assertEqual(len(public), 9)
        self.assertEqual(catalog()["counts"]["skills"], 5)
        self.assertEqual(catalog()["counts"]["agents"], 4)

    def test_every_catalog_path_exists_and_matches_recorded_sha256(self):
        for (kind, slug), expected in GOLDEN_BODIES.items():
            path = body_path(kind, slug)
            self.assertTrue(path.is_file(), f"missing {path}")
            self.assertEqual(
                sha256_file(path), expected, f"hash mismatch {kind}:{slug}"
            )

    def test_vendor_archive_quarantine_never_enter_catalog(self):
        for item in catalog()["items"]:
            path = item.get("path", "")
            self.assertFalse(path.startswith("archive/"), item)
            self.assertFalse(path.startswith("plugins/"), item)
            self.assertNotIn("quarantine", path)
            self.assertNotEqual(item.get("status"), "unreviewed")

    def test_protected_mcp_tools_byte_identical(self):
        path = ROOT / "tools/MCP_Tools.md"
        self.assertTrue(path.is_file())
        self.assertEqual(sha256_file(path), PROTECTED_MCP)

    def test_bodies_contain_no_legacy_404_install_urls(self):
        failures = []
        for kind, slug in GOLDEN_BODIES:
            text = body_path(kind, slug).read_text()
            hits = LEGACY_404.findall(text)
            if hits:
                failures.append(f"{kind}:{slug} {hits}")
        self.assertEqual(
            failures, [], "legacy 404 install URLs in bodies:\n" + "\n".join(failures)
        )

    def test_catalog_contains_no_legacy_404_install_urls(self):
        failures = []
        for item in catalog()["items"]:
            blob = json.dumps(item.get("install") or {})
            if LEGACY_404.search(blob):
                failures.append(item["slug"])
            if MOVING_MAIN.search(item.get("raw_url") or ""):
                failures.append(f"{item['slug']} moving-main raw_url")
        self.assertEqual(failures, [], f"broken catalog URIs: {failures}")

    def test_url_installs_use_canonical_site_raw_route(self):
        failures = []
        for item in catalog()["items"]:
            kind_dir = "skills" if item["kind"] == "skill" else "agents"
            expected = f"https://vidoxlabs.dev/vitools/raw/{kind_dir}/{item['slug']}.md"
            install = item.get("install") or {}
            for key in ("cursor", "agent_prompt", "raw", "download"):
                if key not in install:
                    continue
                if expected not in install[key]:
                    failures.append(f"{item['slug']}.{key} missing canonical raw route")
            raw_url = item.get("raw_url") or ""
            match = CANONICAL_RAW.match(raw_url)
            if (
                not match
                or match.group(1) != kind_dir
                or match.group(2) != item["slug"]
            ):
                failures.append(f"{item['slug']} raw_url={raw_url!r}")
        self.assertEqual(failures, [], "\n".join(failures))

    def test_unverified_repo_installers_are_not_actionable(self):
        """npx/marketplace depend on GitHub default main; must not be copyable until main is 5+4."""
        failures = []
        for item in catalog()["items"]:
            install = item.get("install") or {}
            for banned in ("generic", "claude-code"):
                if banned in install and str(install[banned]).strip():
                    failures.append(f"{item['slug']} still advertises {banned}")
        self.assertEqual(failures, [], "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
