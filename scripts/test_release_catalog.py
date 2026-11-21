#!/usr/bin/env python3
"""Negative and equivalence checks for the admitted ViTools release."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import release_catalog as release


ROOT = Path(__file__).resolve().parent.parent


def expect_error(fn) -> None:
    try:
        fn()
    except release.ReleaseError:
        return
    raise SystemExit(f"expected ReleaseError from {fn}")


def test_duplicate_admission() -> None:
    data = release.load_admission()
    data["ids"] = [data["ids"][0], data["ids"][0]]
    data["bodies"] = {data["ids"][0]: data["bodies"][data["ids"][0]]}

    def load() -> dict:
        text = json.dumps(data)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            handle.write(text)
            path = Path(handle.name)
        try:
            return release.load_admission(path)
        finally:
            path.unlink()

    expect_error(load)


def test_missing_admission_file() -> None:
    expect_error(lambda: release.load_admission(ROOT / "catalog" / "missing-admission.json"))


def test_unresolved_pin() -> None:
    expect_error(lambda: release.verify_commit("0" * 40))


def test_widened_output_does_not_replace_files() -> None:
    admission = release.load_admission()
    widened = [{"id": item_id} for item_id in admission["ids"]]
    widened.append({"id": "skill:not-admitted"})
    sentinel = ROOT / "catalog" / "vitools.catalog.json.release-tmp"
    if sentinel.exists():
        sentinel.unlink()
    expect_error(lambda: release.assert_exact(widened, admission))
    if sentinel.exists():
        raise SystemExit("widened output replaced a release file")


def test_two_builds_match_and_check_passes() -> None:
    first = release.render()
    second = release.render()
    if first != second:
        raise SystemExit("two clean builds differed")
    release.check()
    cursor = json.loads(first["plugins/cursor/plugin.json"])
    claude = json.loads(first["plugins/claude/marketplace.json"])
    if len(cursor["skills"]) != 5 or "agents" in cursor:
        raise SystemExit("cursor adapter is not the skill subset")
    if len(claude["skills"]) != 5 or len(claude["agents"]) != 4:
        raise SystemExit("claude adapter is not the admitted set")
    catalog = json.loads(first["catalog/vitools.catalog.json"])
    if [item["id"] for item in catalog["items"]] != release.load_admission()["ids"]:
        raise SystemExit("catalog order drifted")
    if catalog["source_commit"] != "270d02569d2a5073356c6042bf9539b61ea16b21":
        raise SystemExit("body pin drifted")
    if "179ac7d7dfd4026bc27c737ed4e373838708fe74" in json.dumps(catalog):
        raise SystemExit("site pin was written into the catalog")


def test_default_builder_does_not_scan() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/catalog-build.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        raise SystemExit("unscoped catalog build was allowed")
    if "release_catalog.py" not in result.stdout + result.stderr:
        raise SystemExit(result.stderr or result.stdout)


def main() -> int:
    test_duplicate_admission()
    test_missing_admission_file()
    test_unresolved_pin()
    test_widened_output_does_not_replace_files()
    test_two_builds_match_and_check_passes()
    test_default_builder_does_not_scan()
    print("release catalog tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
