"""
Skill creation module for ViTools.

Provides functionality to create new skills from templates and concept cards.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

from vitools_sync.paths import repo_root


@dataclass
class CreateSkillConfig:
    """Configuration for creating a new skill."""

    # Required
    name: str
    template: str = "mcp-tool"

    # Optional - from concept card or user input
    description: str = ""
    domain: str = "MCP Tools"
    owner: str = "vidoxlabs"
    skill_type: str = "MCP Integration"
    lifecycle: str = "Intake"

    # Optional - additional metadata
    custom_title: Optional[str] = None
    summary: str = ""
    triggers: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    procedure: str = ""
    guardrails: str = ""
    good_examples: str = ""
    bad_examples: str = ""
    verification: str = ""
    evidence_urls: list[str] = field(default_factory=list)
    related_tools: list[str] = field(default_factory=list)

    # Paths
    target_dir: Optional[Path] = None
    concept_card_path: Optional[Path] = None

    @property
    def slug(self) -> str:
        """Generate slug from name."""
        # Convert to lowercase, replace spaces with hyphens
        slug = self.name.lower().strip()
        # Remove special characters (keep alphanumeric, space, underscore, hyphen)
        slug = re.sub(r"[^a-z0-9\s_-]", "", slug)
        # Replace spaces and underscores with hyphens
        slug = re.sub(r"[\s_]", "-", slug)
        # Remove consecutive hyphens
        slug = re.sub(r"-+", "-", slug)
        # Remove leading/trailing hyphens
        slug = slug.strip("-")
        return slug

    @property
    def title(self) -> str:
        """Generate title from name if not provided."""
        if self.custom_title:
            return self.custom_title
        # Convert slug to title case
        return " ".join(word.capitalize() for word in self.name.split("-"))


# Template definitions
TEMPLATE_TYPES = {
    "mcp-tool": {
        "path": "skills-template/mcp-tool",
        "default_domain": "MCP Tools",
        "default_skill_type": "MCP Integration",
    },
    "api-integration": {
        "path": "skills-template/api-integration",
        "default_domain": "API Integrations",
        "default_skill_type": "API Integration",
    },
    "procedure": {
        "path": "skills-template/procedure",
        "default_domain": "Procedures",
        "default_skill_type": "Procedure",
    },
    "research": {
        "path": "skills-template/research",
        "default_domain": "Research",
        "default_skill_type": "Research",
    },
    "validation": {
        "path": "skills-template/validation",
        "default_domain": "Quality Assurance",
        "default_skill_type": "Validation",
    },
}

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


def load_template(template_type: str, repo_path: Path) -> tuple[str, dict]:
    """Load a skill template and its metadata."""
    if template_type not in TEMPLATE_TYPES:
        raise ValueError(
            f"Unknown template type: {template_type}. "
            f"Available types: {', '.join(TEMPLATE_TYPES.keys())}"
        )

    template_info = TEMPLATE_TYPES[template_type]
    template_dir = repo_path / "skills" / template_info["path"]
    template_file = template_dir / "SKILL.md.template"
    metadata_file = template_dir / "metadata.yaml"

    if not template_file.exists():
        raise FileNotFoundError(f"Template file not found: {template_file}")

    # Load template content
    template_content = template_file.read_text()

    # Load metadata
    metadata = {}
    if metadata_file.exists():
        with open(metadata_file) as f:
            metadata = yaml.safe_load(f) or {}

    return template_content, metadata


def load_concept_card(path: Path) -> dict:
    """Load a concept card YAML file."""
    if not path.exists():
        raise FileNotFoundError(f"Concept card not found: {path}")

    with open(path) as f:
        concept = yaml.safe_load(f)

    if not concept:
        raise ValueError(f"Empty concept card: {path}")

    return concept


def config_from_concept_card(concept: dict, config: CreateSkillConfig) -> CreateSkillConfig:
    """Update config from concept card data."""
    # Map concept card fields to config
    updated_config = CreateSkillConfig(**config.__dict__)

    if "name" in concept:
        updated_config.name = concept["name"]
    if "description" in concept:
        updated_config.description = concept["description"]
    if "domain" in concept:
        updated_config.domain = concept["domain"]
    
    # Handle triggers - can be from triggers field or intent_patterns
    triggers = []
    if "triggers" in concept and isinstance(concept["triggers"], list):
        triggers = concept["triggers"]
    elif "intent_patterns" in concept and isinstance(concept["intent_patterns"], list):
        triggers = concept["intent_patterns"]
    if triggers:
        updated_config.triggers = triggers
    
    # Handle procedure
    if "procedure_pattern" in concept:
        updated_config.procedure = concept["procedure_pattern"]
    
    if "evidence_urls" in concept:
        updated_config.evidence_urls = concept["evidence_urls"]
    if "related_tools" in concept:
        updated_config.related_tools = concept["related_tools"]

    # Note: Template is already set from the config parameter
    # Don't override it based on concept card domain unless it's the default
    # The caller can explicitly pass the template they want

    return updated_config


def render_template(
    template_content: str, config: CreateSkillConfig, metadata: dict
) -> str:
    """Render a template with the provided configuration."""
    from string import Template

    # Prepare template variables
    date = datetime.now().strftime("%Y-%m-%d")

    # Format YAML lists
    def format_yaml_list(items: list[str], indent: int = 2) -> str:
        if not items:
            return ""
        lines = []
        for item in items:
            if isinstance(item, str):
                lines.append(f"- {item}")
            else:
                lines.append(f"- {str(item)}")
        return "\n".join(lines)

    # Format multi-line strings - preserve existing formatting
    def format_multiline(text: str, indent: int = 0) -> str:
        if not text:
            return ""
        # If text already has newlines, preserve it as-is
        if "\n" in text:
            return text
        # Single line - just return as-is
        return text

    # Prepare replacements
    replacements = {
        "{{name}}": config.slug,
        "{{title}}": config.title,
        "{{description}}": config.description,
        "{{domain}}": config.domain,
        "{{lifecycle}}": config.lifecycle,
        "{{owner}}": config.owner,
        "{{skill_type}}": config.skill_type,
        "{{date}}": date,
        "{{summary}}": config.summary or "",
        "{{triggers}}": format_multiline("\n".join([f"- {t}" for t in config.triggers]))
        if config.triggers
        else "",
        "{{inputs}}": format_multiline(
            "\n".join([f"- {i}" for i in config.inputs]) if config.inputs else ""
        ),
        "{{outputs}}": format_multiline(
            "\n".join([f"- {o}" for o in config.outputs]) if config.outputs else ""
        ),
        "{{procedure}}": format_multiline(config.procedure),
        "{{guardrails}}": format_multiline(config.guardrails),
        "{{good_examples}}": format_multiline(config.good_examples),
        "{{bad_examples}}": format_multiline(config.bad_examples),
        "{{verification}}": config.verification or "echo \"Skill verified\"",
        "{{evidence_urls}}": format_yaml_list(config.evidence_urls),
        "{{related_tools}}": format_yaml_list(config.related_tools),
    }

    # Add template-specific variables from metadata
    template_vars = metadata.get("defaults", {})
    for key, value in template_vars.items():
        if key not in replacements:
            replacements[f"{{{{{key}}}}}"] = str(value)

    # Replace placeholders
    rendered = template_content
    for placeholder, replacement in replacements.items():
        rendered = rendered.replace(placeholder, replacement)

    # Remove empty placeholders
    rendered = re.sub(r"\{\{[^}]+\}\}", "", rendered)

    return rendered


def create_skill(config: CreateSkillConfig) -> dict:
    """
    Create a new skill from a template and optional concept card.

    Args:
        config: Configuration for the skill

    Returns:
        dict: Result with paths created and status
    """
    repo = repo_root(config.target_dir)
    result = {
        "success": False,
        "skill_path": None,
        "files_created": [],
        "errors": [],
        "warnings": [],
    }

    try:
        # Determine slug
        slug = config.slug
        if not slug:
            raise ValueError("Could not generate slug from name")

        # Load concept card if provided
        if config.concept_card_path:
            concept = load_concept_card(config.concept_card_path)
            config = config_from_concept_card(concept, config)
            # Update slug from concept card name
            slug = config.slug

        # Load template
        template_content, metadata = load_template(config.template, repo)

        # Determine skill directory
        skills_dir = repo / "skills"
        skill_dir = skills_dir / slug

        # Create skill directory
        skill_dir.mkdir(parents=True, exist_ok=True)
        result["skill_path"] = str(skill_dir)

        # Render template
        skill_content = render_template(template_content, config, metadata)

        # Write SKILL.md
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(skill_content)
        result["files_created"].append(f"SKILL.md")

        # Create references directory if there are evidence URLs
        if config.evidence_urls:
            ref_dir = skill_dir / "references"
            ref_dir.mkdir(exist_ok=True)
            result["files_created"].append("references/")

        # Run legal check
        try:
            from vitools_sync.legal.overlap import check_skill_overlap

            check_result = check_skill_overlap(repo, skill_file)
            if not check_result.passed:
                result["warnings"].append(
                    f"Legal check warnings: {len(check_result.issues)} issues"
                )
                for issue in check_result.issues:
                    result["warnings"].append(f"  - {issue}")
        except Exception as e:
            result["warnings"].append(f"Legal check skipped: {e}")

        # Validate the created skill
        try:
            from vitools_sync.skill.validate import validate_skill, ValidationConfig
            validation = validate_skill(skill_file)
            if not validation.passed:
                result["warnings"].append(
                    f"Validation warnings: {len(validation.errors)} errors, "
                    f"{len(validation.warnings)} warnings"
                )
                for error in validation.errors:
                    result["warnings"].append(f"  - {error}")
        except Exception as e:
            result["warnings"].append(f"Validation skipped: {e}")

        result["success"] = True
        result["message"] = f"Skill '{slug}' created successfully"

    except Exception as e:
        result["errors"].append(str(e))
        result["success"] = False

    return result


def create_skill_from_template(
    name: str,
    template: str = "mcp-tool",
    target_dir: Optional[Path] = None,
    concept_card_path: Optional[Path] = None,
    **kwargs,
) -> dict:
    """
    Convenience function to create a skill from a template.

    Args:
        name: Name of the skill
        template: Template type to use
        target_dir: Repository root (defaults to current working directory)
        concept_card_path: Path to concept card YAML file
        **kwargs: Additional configuration options

    Returns:
        dict: Result with paths created and status
    """
    config = CreateSkillConfig(
        name=name,
        template=template,
        target_dir=target_dir,
        concept_card_path=concept_card_path,
        **kwargs,
    )
    return create_skill(config)
