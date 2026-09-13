from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from vitools_sync.paths import archive_vendor


@dataclass
class OverlapResult:
    passed: bool
    issues: list[str]
    ngram_overlap_ratio: float = 0.0
    longest_match: int = 0


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _ngrams(tokens: list[str], n: int = 5) -> set[tuple[str, ...]]:
    if len(tokens) < n:
        return set()
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def _longest_common_substring(a: str, b: str) -> int:
    if not a or not b:
        return 0
    best = 0
    for i in range(len(a)):
        for j in range(len(b)):
            length = 0
            while i + length < len(a) and j + length < len(b) and a[i + length] == b[j + length]:
                length += 1
            best = max(best, length)
    return best


def check_skill_overlap(root: Path, skill_path: Path, *, ngram_threshold: float = 0.15, lcs_threshold: int = 80) -> OverlapResult:
    issues: list[str] = []
    if not skill_path.exists():
        return OverlapResult(False, [f"Skill not found: {skill_path}"])

    skill_text = skill_path.read_text(encoding="utf-8", errors="ignore")
    skill_tokens = _tokenize(skill_text)
    skill_ngrams = _ngrams(skill_tokens)

    archive = archive_vendor(root)
    if not archive.exists():
        return OverlapResult(True, [])

    max_overlap = 0.0
    max_lcs = 0
    archive_files = list(archive.rglob("*.md")) + list(archive.rglob("SKILL.md"))

    for ref in archive_files:
        ref_text = ref.read_text(encoding="utf-8", errors="ignore")
        ref_ngrams = _ngrams(_tokenize(ref_text))
        if skill_ngrams and ref_ngrams:
            shared = len(skill_ngrams & ref_ngrams)
            ratio = shared / max(len(skill_ngrams), 1)
            max_overlap = max(max_overlap, ratio)
        lcs = _longest_common_substring(skill_text.lower(), ref_text.lower())
        max_lcs = max(max_lcs, lcs)

    if max_overlap > ngram_threshold:
        issues.append(f"5-gram overlap {max_overlap:.1%} exceeds {ngram_threshold:.0%} threshold")
    if max_lcs > lcs_threshold:
        issues.append(f"Longest common substring {max_lcs} chars exceeds {lcs_threshold} threshold")

    return OverlapResult(
        passed=len(issues) == 0,
        issues=issues,
        ngram_overlap_ratio=max_overlap,
        longest_match=max_lcs,
    )
