from __future__ import annotations

from pathlib import Path

import pytest

from vitools_sync.legal.overlap import check_skill_overlap
from vitools_sync.paths import repo_root


@pytest.fixture
def root() -> Path:
    return repo_root(Path(__file__).resolve().parents[3])


def test_native_skill_passes_legal_gate(root: Path) -> None:
    skill = root / ".agents/skills/skill-mining/SKILL.md"
    result = check_skill_overlap(root, skill)
    assert result.passed, result.issues


def test_missing_skill_fails(root: Path) -> None:
    result = check_skill_overlap(root, root / ".agents/skills/nonexistent/SKILL.md")
    assert not result.passed
