from __future__ import annotations

import json
from pathlib import Path

import pytest

from vitools_sync.emitters.cursor import emit_cursor
from vitools_sync.paths import repo_root


@pytest.fixture
def root() -> Path:
    return repo_root(Path(__file__).resolve().parents[3])


def test_emit_cursor_writes_skills_and_mcp(tmp_path: Path, root: Path) -> None:
    written = emit_cursor(root, tmp_path)
    assert (tmp_path / "mcp.json").exists()
    payload = json.loads((tmp_path / "mcp.json").read_text())
    assert "mcpServers" in payload
    assert "tavily" in payload["mcpServers"]
    skill_files = list((tmp_path / "skills").glob("*/SKILL.md"))
    assert len(skill_files) >= 5


def test_emit_cursor_remote_mcp_url(tmp_path: Path, root: Path) -> None:
    emit_cursor(root, tmp_path)
    payload = json.loads((tmp_path / "mcp.json").read_text())
    assert payload["mcpServers"]["tavily"]["url"] == "https://mcp.tavily.com/mcp"
