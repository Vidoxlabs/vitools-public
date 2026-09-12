from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitools_sync.catalog.inventory import build_inventory
from vitools_sync.emitters import emit_all
from vitools_sync.paths import repo_root


@pytest.fixture
def root() -> Path:
    return repo_root(Path(__file__).resolve().parents[3])


def test_build_inventory_has_entries(root: Path) -> None:
    inventory = build_inventory(root)
    assert len(inventory) > 0
    kinds = {e["kind"] for e in inventory}
    assert "canonical_skill" in kinds
    assert "concept_card" in kinds


def test_emit_all_platforms(tmp_path: Path, root: Path) -> None:
    results = emit_all(root, tmp_path)
    assert set(results.keys()) == {"cursor", "devin", "opencode", "grok", "mistral", "antigravity"}
    cursor_mcp = tmp_path / "cursor" / "mcp.json"
    assert cursor_mcp.exists()
    grok_mcp = tmp_path / "grok" / "mcp.json"
    grok_payload = json.loads(grok_mcp.read_text())
    assert "servers" in grok_payload
