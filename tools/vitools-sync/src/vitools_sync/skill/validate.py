"""
Skill validation module for ViTools.

Provides validation functionality for skills against the Vidoxlabs template.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class ValidationResult:
    """Result of validating a skill."""

    path: str
    passed: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)

    def add_error(self, check_name: str, message: str) -> None:
        """Add an error to the result."""
        self.errors.append(f"[{check_name}] {message}")
        self.checks[check_name] = False
        self.passed = False

    def add_warning(self, check_name: str, message: str) -> None:
        """Add a warning to the result."""
        self.warnings.append(f"[{check_name}] {message}")
        self.checks[check_name] = True

    def add_check(self, check_name: str, passed: bool, message: str = "") -> None:
        """Add a check result."""
        self.checks[check_name] = passed
        if not passed:
            self.errors.append(f"[{check_name}] {message}")
            self.passed = False


# Required sections in a Vidoxlabs skill
REQUIRED_SECTIONS = [
    "Summary",
    "When to Use (Triggers)",
    "Inputs",
    "Outputs",
    "Procedure / Steps",
    "Guardrails",
    "Examples",
    "Verification",
    "Sources / Evidence",
]

# Recommended sections
RECOMMENDED_SECTIONS = [
    "# ",  # Title
    "---",  # Frontmatter separator
]

# Sections that should have subsections
SECTIONS_WITH_SUBS = {
    "Examples": ["### Good", "### Bad"],
}

# Frontmatter required fields
REQUIRED_FRONTMATTER_FIELDS = ["name", "description"]

# Forbidden patterns (archive/vendor references)
# Block references to archive/vendor paths
FORBIDDEN_PATTERNS = [
    r"archive/vendor",
    r"archive\\vendor",
]


@dataclass
class ValidationConfig:
    """Configuration for validation."""

    strict: bool = False  # If True, warnings become errors
    check_legal: bool = True  # Check for archive/vendor references
    check_structure: bool = True  # Check document structure
    check_frontmatter: bool = True  # Check YAML frontmatter
    check_sections: bool = True  # Check required sections


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from a markdown file."""
    frontmatter = {}
    remaining = content

    # Match frontmatter - more flexible pattern
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            frontmatter = {}
        remaining = match.group(2)

    return frontmatter, remaining


def extract_sections(content: str) -> dict[str, list[str]]:
    """Extract sections from markdown content.
    
    Returns a dict mapping section titles to lists of content lines.
    """
    sections = {}
    current_section = None
    current_lines = []

    for line in content.split("\n"):
        # Match heading
        match = re.match(r"^(#+)\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()

            # Save previous section
            if current_section and current_lines:
                sections[current_section] = current_lines

            if level == 1:
                current_section = title
                current_lines = []
            elif level == 2:
                current_section = title
                current_lines = []
            elif level >= 3 and current_section:
                # Subsection - keep parent section but note the subsection
                current_section = f"{current_section}/{title}"
                current_lines = []
            continue

        # Add line to current section
        if current_section is not None:
            current_lines.append(line)

    # Save last section
    if current_section and current_lines:
        sections[current_section] = current_lines

    return sections


def get_section_titles(content: str) -> list[str]:
    """Get all section titles (level 1 and 2) from markdown content.
    
    Only matches lines that are actual markdown headers, not comments inside code blocks.
    """
    titles = []
    in_code_block = False
    
    for line in content.split("\n"):
        # Track code block state
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        
        # Skip if inside code block
        if in_code_block:
            continue
        
        # Match markdown headers
        match = re.match(r"^(#{1,2})\s+(.+)$", line)
        if match:
            titles.append(match.group(2).strip())
    
    return titles


def check_required_sections(content: str, result: ValidationResult) -> None:
    """Check that all required sections are present."""
    section_titles = get_section_titles(content)

    for required in REQUIRED_SECTIONS:
        if required not in section_titles:
            result.add_error(
                "required_sections",
                f"Missing required section: '{required}'",
            )


def check_examples_section(content: str, result: ValidationResult) -> None:
    """Check that Examples section has both Good and Bad subsections."""
    # Check for Examples section
    if "## Examples" in content or "# Examples" in content:
        has_good = "### Good" in content or "#### Good" in content
        has_bad = "### Bad" in content or "#### Bad" in content

        if not has_good:
            result.add_warning(
                "examples_structure",
                "Examples section should have a 'Good' subsection",
            )
        if not has_bad:
            result.add_warning(
                "examples_structure",
                "Examples section should have a 'Bad' subsection",
            )
    else:
        result.add_warning(
            "examples_structure",
            "Examples section should exist with Good and Bad subsections",
        )


def check_frontmatter(content: str, result: ValidationResult) -> dict:
    """Check YAML frontmatter."""
    frontmatter, _ = extract_frontmatter(content)

    if not frontmatter:
        result.add_error(
            "frontmatter",
            "Missing YAML frontmatter (--- at start of file)",
        )
        return frontmatter

    # Check required fields
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in frontmatter:
            result.add_error(
                "frontmatter",
                f"Missing required frontmatter field: '{field}'",
            )

    return frontmatter


def check_archive_references(content: str, result: ValidationResult) -> None:
    """Check for forbidden archive/vendor references."""
    for pattern in FORBIDDEN_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            result.add_error(
                "legal_contamination",
                f"Forbidden pattern detected: '{pattern}' ({len(matches)} occurrences)",
            )


def check_legal_overlap(path: Path, result: ValidationResult) -> None:
    """Run legal overlap check."""
    try:
        from vitools_sync.legal.overlap import check_skill_overlap

        check_result = check_skill_overlap(Path(path).parent.parent.parent.parent, Path(path))
        if not check_result.passed:
            for issue in check_result.issues:
                result.add_error("legal_overlap", issue)
    except Exception as e:
        result.add_warning("legal_overlap", f"Legal check skipped: {e}")


def check_structure(content: str, result: ValidationResult) -> None:
    """Check document structure."""
    # Check for title
    if "# " not in content:
        result.add_error("structure", "Missing title (H1 heading)")

    # Check for frontmatter separator
    if "---" not in content:
        result.add_warning("structure", "No frontmatter separator found")

    # Check heading hierarchy
    lines = content.split("\n")
    prev_level = 0
    for i, line in enumerate(lines):
        match = re.match(r"^(#+)\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            if level > prev_level + 1:
                result.add_warning(
                    "structure",
                    f"Heading level jump: from H{prev_level} to H{level} at line {i+1}",
                )
            prev_level = level


def check_content_quality(content: str, result: ValidationResult) -> None:
    """Check content quality heuristics."""
    # Check for very short sections by looking at content between headers
    lines = content.split("\n")
    current_section = None
    section_lines = []
    in_code_block = False
    
    for i, line in enumerate(lines):
        # Track code block state
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            if current_section:
                section_lines.append(line)
            continue
        
        # Skip if inside code block for header detection
        if in_code_block:
            if current_section:
                section_lines.append(line)
            continue
        
        match = re.match(r"^(#{1,2})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            
            # Save previous section
            if current_section and section_lines and current_section in REQUIRED_SECTIONS:
                # Count non-empty, non-whitespace lines
                content_lines = [l for l in section_lines if l.strip()]
                if len(content_lines) < 2:  # At least 2 lines of content
                    text_content = " ".join(content_lines).strip()
                    if len(text_content) < 20:  # At least 20 characters
                        result.add_warning(
                            "content_quality",
                            f"Section '{current_section}' appears to be very short",
                        )
            current_section = title
            section_lines = []
            continue
        
        if current_section:
            section_lines.append(line)
    
    # Check last section
    if current_section and section_lines and current_section in REQUIRED_SECTIONS:
        content_lines = [l for l in section_lines if l.strip()]
        if len(content_lines) < 2:
            text_content = " ".join(content_lines).strip()
            if len(text_content) < 20:
                result.add_warning(
                    "content_quality",
                    f"Section '{current_section}' appears to be very short",
                )


def validate_skill(
    path: Path,
    config: Optional[ValidationConfig] = None,
) -> ValidationResult:
    """
    Validate a skill file against Vidoxlabs standards.

    Args:
        path: Path to the SKILL.md file
        config: Optional validation configuration

    Returns:
        ValidationResult with all check results
    """
    if config is None:
        config = ValidationConfig()

    result = ValidationResult(path=str(path))

    # Read content
    try:
        content = path.read_text()
    except Exception as e:
        result.add_error("file_read", str(e))
        return result

    # Check frontmatter
    if config.check_frontmatter:
        check_frontmatter(content, result)

    # Check structure
    if config.check_structure:
        check_structure(content, result)

    # Check required sections
    if config.check_sections:
        check_required_sections(content, result)
        check_examples_section(content, result)

    # Check content quality
    check_content_quality(content, result)

    # Check for archive/vendor references
    if config.check_legal:
        check_archive_references(content, result)

    # Check legal overlap
    if config.check_legal:
        try:
            check_legal_overlap(path, result)
        except Exception:
            pass  # Skip if legal check fails

    return result


def validate_skill_from_string(
    content: str,
    path: str = "SKILL.md",
    config: Optional[ValidationConfig] = None,
) -> ValidationResult:
    """
    Validate skill content from a string.

    Args:
        content: The skill content as a string
        path: Path to report in results
        config: Optional validation configuration

    Returns:
        ValidationResult with all check results
    """
    if config is None:
        config = ValidationConfig()

    result = ValidationResult(path=path)

    # Check frontmatter
    if config.check_frontmatter:
        check_frontmatter(content, result)

    # Check structure
    if config.check_structure:
        check_structure(content, result)

    # Check required sections
    if config.check_sections:
        check_required_sections(content, result)
        check_examples_section(content, result)

    # Check content quality
    check_content_quality(content, result)

    # Check for archive/vendor references
    if config.check_legal:
        check_archive_references(content, result)

    return result
