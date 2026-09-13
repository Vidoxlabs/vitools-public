"""
Archive Monitoring for ViTools Legal Compliance.

Detects and blocks accidental contamination from vendor to skills/ + agents/ layer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class MonitorResult:
    """Result of monitoring archive contamination."""
    passed: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)
    
    def add_issue(self, check_name: str, message: str, is_error: bool = True) -> None:
        """Add an issue to the result."""
        if is_error:
            self.errors.append(f"[{check_name}] {message}")
            self.checks[check_name] = False
            self.passed = False
        else:
            self.warnings.append(f"[{check_name}] {message}")
            self.checks[check_name] = True


@dataclass
class ContaminationIssue:
    """A single contamination issue found."""
    severity: str  # "error" or "warning"
    check_type: str
    message: str
    source_path: str
    target_path: Optional[str] = None


# Patterns to detect vendor references
ARCHIVE_REFERENCE_PATTERNS = [
    r"vendor",
    r"archive\\vendor",
    r"/vendor/",
    r"\.\./vendor",
]

# Patterns to detect import/require statements referencing archive
IMPORT_PATTERNS = [
    r"from archive\.vendor",
    r"import archive\.vendor",
    r"require\(['\"]vendor",
    r"from \.\./archive",
]

# File extensions to check for imports
CODE_EXTENSIONS = {
    ".py": True,
    ".js": True,
    ".ts": True,
    ".jsx": True,
    ".tsx": True,
}


def check_symlinks(root: Path) -> list[ContaminationIssue]:
    """Check for symlinks pointing to vendor."""
    issues = []
    archive = root / "archive" / "vendor"
    agents = root / "skills"
    
    if not archive.exists():
        return issues
    
    # Check all symlinks in skills/ + agents/
    for path in agents.rglob("*"):
        if path.is_symlink():
            target = path.resolve()
            if archive in target.parents:
                issues.append(ContaminationIssue(
                    severity="error",
                    check_type="symlink_detection",
                    message=f"Symlink points to vendor: {path} -> {target}",
                    source_path=str(path),
                    target_path=str(target),
                ))
    
    return issues


def check_content_similarity(
    content: str,
    archive_files: list[Path],
    ngram_threshold: float = 0.15,
    lcs_threshold: int = 80,
) -> list[ContaminationIssue]:
    """Check content similarity against archive files."""
    issues = []
    
    import re
    from vitools_sync.legal.overlap import _tokenize, _ngrams, _longest_common_substring
    
    content_tokens = _tokenize(content)
    content_ngrams = _ngrams(content_tokens)
    
    if not content_ngrams:
        return issues
    
    max_overlap = 0.0
    max_lcs = 0
    matching_file = None
    
    for ref_file in archive_files:
        try:
            ref_text = ref_file.read_text(encoding="utf-8", errors="ignore")
            ref_ngrams = _ngrams(_tokenize(ref_text))
            
            if content_ngrams and ref_ngrams:
                shared = len(content_ngrams & ref_ngrams)
                ratio = shared / max(len(content_ngrams), 1)
                max_overlap = max(max_overlap, ratio)
                
            lcs = _longest_common_substring(content.lower(), ref_text.lower())
            max_lcs = max(max_lcs, lcs)
            
            if max_overlap > ngram_threshold or max_lcs > lcs_threshold:
                matching_file = str(ref_file.relative_to(ref_file.parent.parent.parent))
        except Exception:
            continue
    
    if max_overlap > ngram_threshold:
        issues.append(ContaminationIssue(
            severity="error",
            check_type="ngram_overlap",
            message=f"5-gram overlap {max_overlap:.1%} exceeds {ngram_threshold:.0%} threshold",
            source_path=matching_file or "unknown",
        ))
    
    if max_lcs > lcs_threshold:
        issues.append(ContaminationIssue(
            severity="error",
            check_type="longest_common_substring",
            message=f"Longest common substring {max_lcs} chars exceeds {lcs_threshold} threshold",
            source_path=matching_file or "unknown",
        ))
    
    return issues


def check_archive_references(content: str, path: Path) -> list[ContaminationIssue]:
    """Check for direct vendor references in content."""
    issues = []
    
    for pattern in ARCHIVE_REFERENCE_PATTERNS:
        matches = re.findall(pattern, content)
        for match in matches:
            issues.append(ContaminationIssue(
                severity="error",
                check_type="archive_reference",
                message=f"Found vendor reference: '{match}'",
                source_path=str(path),
            ))
    
    return issues


def check_import_statements(content: str, path: Path) -> list[ContaminationIssue]:
    """Check for import/require statements referencing archive."""
    issues = []
    
    for pattern in IMPORT_PATTERNS:
        matches = re.findall(pattern, content)
        for match in matches:
            issues.append(ContaminationIssue(
                severity="error",
                check_type="archive_import",
                message=f"Found archive import/require: '{match}'",
                source_path=str(path),
            ))
    
    return issues


def check_path_references(content: str, path: Path, agents_dir: Path) -> list[ContaminationIssue]:
    """Check for path references that might point to archive."""
    issues = []
    
    # Check for relative paths that might point to archive
    relative_patterns = [
        r"\.\./\.\./archive",
        r"\.\./archive",
        r"\../archive",
    ]
    
    for pattern in relative_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            issues.append(ContaminationIssue(
                severity="warning",
                check_type="relative_path_reference",
                message=f"Found relative path to archive: '{match}'",
                source_path=str(path),
            ))
    
    return issues


def get_archive_files(archive_path: Path) -> list[Path]:
    """Get all files in vendor to check against."""
    archive_files = []
    
    if not archive_path.exists():
        return archive_files
    
    # Get all markdown and text files
    archive_files.extend(list(archive_path.rglob("*.md")))
    archive_files.extend(list(archive_path.rglob("SKILL.md")))
    archive_files.extend(list(archive_path.rglob("*.txt")))
    archive_files.extend(list(archive_path.rglob("*.yaml")))
    archive_files.extend(list(archive_path.rglob("*.yml")))
    archive_files.extend(list(archive_path.rglob("*.json")))
    
    return archive_files


def monitor_file(
    file_path: Path,
    archive_path: Path,
    agents_path: Path,
) -> list[ContaminationIssue]:
    """Monitor a single file for archive contamination."""
    issues = []
    
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return issues
    
    # Check for archive references
    issues.extend(check_archive_references(content, file_path))
    
    # Check for import statements (if code file)
    if file_path.suffix in CODE_EXTENSIONS:
        issues.extend(check_import_statements(content, file_path))
    
    # Check for path references
    issues.extend(check_path_references(content, file_path, agents_path))
    
    return issues


def monitor_directory(
    dir_path: Path,
    archive_path: Path,
    agents_path: Path,
    check_content: bool = True,
) -> MonitorResult:
    """Monitor a directory for archive contamination."""
    result = MonitorResult()
    
    # Check for symlinks
    symlink_issues = check_symlinks(agents_path)
    for issue in symlink_issues:
        result.add_issue(issue.check_type, issue.message, is_error=(issue.severity == "error"))
    
    # Check content if requested
    if check_content:
        archive_files = get_archive_files(archive_path)
        
        if archive_files:
            # Only check text files
            text_extensions = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".js", ".ts"}
            
            for file_path in dir_path.rglob("*"):
                if file_path.is_file() and file_path.suffix in text_extensions:
                    # Check content similarity
                    content_issues = check_content_similarity(
                        file_path.read_text(encoding="utf-8", errors="ignore"),
                        archive_files,
                    )
                    for issue in content_issues:
                        result.add_issue(issue.check_type, issue.message, is_error=(issue.severity == "error"))
                    
                    # Check for references
                    ref_issues = monitor_file(file_path, archive_path, agents_path)
                    for issue in ref_issues:
                        result.add_issue(issue.check_type, issue.message, is_error=(issue.severity == "error"))
    
    return result


def monitor_agents_layer(
    root: Path,
    check_content: bool = True,
) -> MonitorResult:
    """Monitor the entire skills/ + agents/ layer for archive contamination."""
    result = MonitorResult()
    
    archive = root / "archive" / "vendor"
    agents = root / "skills"
    
    if not agents.exists():
        result.add_issue("agents_not_found", "skills/ + agents/ directory not found", is_error=False)
        return result
    
    # Check for symlinks
    symlink_issues = check_symlinks(root)
    for issue in symlink_issues:
        result.add_issue(issue.check_type, issue.message, is_error=(issue.severity == "error"))
    
    # Monitor all subdirectories in skills/ + agents/
    for subdir in agents.iterdir():
        if subdir.is_dir():
            dir_result = monitor_directory(subdir, archive, agents, check_content)
            result.errors.extend(dir_result.errors)
            result.warnings.extend(dir_result.warnings)
            result.checks.update(dir_result.checks)
            if not dir_result.passed:
                result.passed = False
    
    return result


def monitor_archive_layer(
    root: Path,
) -> MonitorResult:
    """Monitor changes in vendor that might affect agents."""
    result = MonitorResult()
    
    archive = root / "archive" / "vendor"
    
    if not archive.exists():
        result.add_issue("archive_not_found", "vendor/ directory not found", is_error=False)
        return result
    
    # For now, just note that archive exists
    result.add_issue("archive_exists", "vendor/ exists", is_error=False)
    
    return result


def check_archive_contamination(
    root: Path,
    check_content: bool = True,
) -> MonitorResult:
    """Full archive contamination check."""
    result = MonitorResult()
    
    # Monitor skills/ + agents/ layer
    agents_result = monitor_agents_layer(root, check_content)
    if not agents_result.passed:
        result.passed = False
        result.errors.extend(agents_result.errors)
        result.warnings.extend(agents_result.warnings)
        result.checks.update(agents_result.checks)
    
    # Monitor for vendor content contamination
    archive_result = monitor_archive_layer(root)
    if not archive_result.passed:
        result.passed = False
        result.errors.extend(archive_result.errors)
        result.warnings.extend(archive_result.warnings)
        result.checks.update(archive_result.checks)
    
    return result