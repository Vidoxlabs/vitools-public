"""
Concept card module for ViTools.

Provides functionality for creating, validating, and managing concept cards.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

import yaml

from vitools_sync.paths import repo_root


@dataclass
class ConceptCardConfig:
    """Configuration for creating a concept card."""

    # Required fields
    name: str
    domain: str
    intent_patterns: list[str]
    triggers: list[str]
    procedure_pattern: str

    # Optional fields
    id: Optional[str] = None
    description: str = ""
    evidence_urls: list[str] = field(default_factory=list)
    related_tools: list[str] = field(default_factory=list)
    related_skills: list[str] = field(default_factory=list)
    priority: str = "medium"
    tags: list[str] = field(default_factory=list)
    notes: str = ""
    status: str = "intake"

    # Metadata
    created_by: str = "vidoxlabs"
    version: str = "1.0.0"
    lifecycle: str = "intake"

    # Paths
    target_dir: Optional[Path] = None


# Valid domains
VALID_DOMAINS = [
    "Research",
    "MCP Tools",
    "API Integrations",
    "Procedures",
    "Validation",
    "Development",
    "Deployment",
    "Data",
    "Security",
    "Monitoring",
]

# Valid priorities
VALID_PRIORITIES = ["low", "medium", "high"]

# Valid statuses
VALID_STATUSES = ["intake", "approved", "rejected"]

# Valid lifecycles
VALID_LIFECYCLES = ["intake", "draft", "review", "promoted", "deprecated"]

# Required fields
REQUIRED_FIELDS = ["id", "name", "domain", "intent_patterns", "triggers", "procedure_pattern"]


def generate_id(name: str) -> str:
    """Generate a concept card ID from a name."""
    # Slugify the name
    slug = name.lower().strip()
    slug = "".join(c if c.isalnum() or c in ["-", "_"] else "-" for c in slug)
    slug = "-".join(part for part in slug.split("-") if part)
    
    # Append a short UUID for uniqueness
    short_uuid = str(uuid4())[:8]
    return f"{slug}-{short_uuid}"


def validate_concept_card_data(data: dict) -> tuple[bool, list[str]]:
    """Validate concept card data against the schema."""
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            if field == "intent_patterns" or field == "triggers":
                if not data.get(field) or len(data[field]) == 0:
                    errors.append(f"Required field '{field}' is empty or missing")
            else:
                errors.append(f"Required field '{field}' is missing")

    # Check field types
    if "intent_patterns" in data and not isinstance(data["intent_patterns"], list):
        errors.append("intent_patterns must be a list")

    if "triggers" in data and not isinstance(data["triggers"], list):
        errors.append("triggers must be a list")

    if "evidence_urls" in data and not isinstance(data["evidence_urls"], list):
        errors.append("evidence_urls must be a list")

    if "related_tools" in data and not isinstance(data["related_tools"], list):
        errors.append("related_tools must be a list")

    # Check domain
    if "domain" in data and data["domain"] not in VALID_DOMAINS:
        errors.append(
            f"Invalid domain '{data['domain']}'. Valid domains: {', '.join(VALID_DOMAINS)}"
        )

    # Check priority
    if "priority" in data and data["priority"] not in VALID_PRIORITIES:
        errors.append(
            f"Invalid priority '{data['priority']}'. Valid priorities: {', '.join(VALID_PRIORITIES)}"
        )

    # Check status
    if "status" in data and data["status"] not in VALID_STATUSES:
        errors.append(
            f"Invalid status '{data['status']}'. Valid statuses: {', '.join(VALID_STATUSES)}"
        )

    # Check lifecycle
    if "lifecycle" in data and data["lifecycle"] not in VALID_LIFECYCLES:
        errors.append(
            f"Invalid lifecycle '{data['lifecycle']}'. Valid lifecycles: {', '.join(VALID_LIFECYCLES)}"
        )

    # Check name format
    if "name" in data:
        name = data["name"]
        if not name.islower() or not all(c.isalnum() or c in ["-", "_"] for c in name):
            errors.append(
                "name must be lowercase with only alphanumeric characters, hyphens, and underscores"
            )

    # Check for forbidden content
    forbidden_patterns = [
        "archive/vendor",
        "skills/",
        "plugins/",
    ]
    
    for field, value in data.items():
        if isinstance(value, str):
            for pattern in forbidden_patterns:
                if pattern in value:
                    errors.append(
                        f"Forbidden pattern '{pattern}' found in field '{field}'"
                    )

    return len(errors) == 0, errors


def create_concept_card(
    config: ConceptCardConfig,
    target_dir: Optional[Path] = None,
) -> dict:
    """
    Create a new concept card.

    Args:
        config: Configuration for the concept card
        target_dir: Target directory (defaults to repo root)

    Returns:
        dict: Result with path and status
    """
    repo = repo_root(target_dir)
    result = {
        "success": False,
        "path": None,
        "errors": [],
        "warnings": [],
    }

    try:
        # Generate ID if not provided
        if not config.id:
            config.id = generate_id(config.name)

        # Set timestamps
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        config.created_at = now
        config.updated_at = now

        # Build concept card data
        concept = {
            "schema_version": "1.0.0",
            "id": config.id,
            "name": config.name,
            "domain": config.domain,
            "intent_patterns": config.intent_patterns,
            "triggers": config.triggers,
            "procedure_pattern": config.procedure_pattern,
        }

        # Add optional fields
        if config.description:
            concept["description"] = config.description
        if config.evidence_urls:
            concept["evidence_urls"] = config.evidence_urls
        if config.related_tools:
            concept["related_tools"] = config.related_tools
        if config.related_skills:
            concept["related_skills"] = config.related_skills
        if config.priority:
            concept["priority"] = config.priority
        if config.tags:
            concept["tags"] = config.tags
        if config.notes:
            concept["notes"] = config.notes
        if config.status:
            concept["status"] = config.status

        # Add metadata
        concept["created_by"] = config.created_by
        concept["created_at"] = now
        concept["updated_at"] = now
        concept["version"] = config.version
        concept["lifecycle"] = config.lifecycle

        # Validate
        is_valid, errors = validate_concept_card_data(concept)
        if not is_valid:
            result["errors"].extend(errors)
            return result

        # Determine path
        concept_dir = repo / ".agents" / "concept-cards"
        concept_dir.mkdir(parents=True, exist_ok=True)
        concept_path = concept_dir / f"{config.id}.yaml"

        # Check if already exists
        if concept_path.exists():
            result["warnings"].append(f"Concept card '{config.id}' already exists, overwriting")

        # Write concept card
        with open(concept_path, "w") as f:
            yaml.dump(concept, f, sort_keys=False)

        result["success"] = True
        result["path"] = str(concept_path)
        result["message"] = f"Concept card '{config.id}' created successfully"

    except Exception as e:
        result["errors"].append(str(e))

    return result


def create_concept_card_interactive() -> dict:
    """
    Create a concept card interactively by prompting the user.

    Returns:
        dict: Result with path and status
    """
    print("Creating a new concept card interactively...")
    print("Press Enter to accept defaults, Ctrl+C to cancel.\n")

    # Get required fields
    name = input("Name (slugified, lowercase hyphen-case): ").strip()
    if not name:
        name = "my-concept"

    print(f"\nAvailable domains: {', '.join(VALID_DOMAINS)}")
    domain = input("Domain: ").strip()
    if not domain:
        domain = "Research"
    if domain not in VALID_DOMAINS:
        print(f"Warning: '{domain}' not in valid domains, using 'Research'")
        domain = "Research"

    print("\nIntent patterns (what the user wants to do):")
    intent_patterns = []
    while True:
        pattern = input(f"  Pattern {len(intent_patterns) + 1} (or Enter to finish): ").strip()
        if not pattern:
            if not intent_patterns:
                print("  At least one pattern is required")
                continue
            break
        intent_patterns.append(pattern)

    print("\nTriggers (when to use this concept):")
    triggers = []
    while True:
        trigger = input(f"  Trigger {len(triggers) + 1} (or Enter to finish): ").strip()
        if not trigger:
            if not triggers:
                print("  At least one trigger is required")
                continue
            break
        triggers.append(trigger)

    print("\nProcedure pattern (high-level procedure):")
    procedure_pattern = input("  ").strip()
    if not procedure_pattern:
        procedure_pattern = "Use MCP tool to perform operation"

    # Get optional fields
    description = input("\nDescription (optional): ").strip()
    
    evidence_urls = []
    url = input("\nEvidence URL 1 (optional, or Enter to skip): ").strip()
    if url:
        evidence_urls.append(url)
        while True:
            url = input("Evidence URL (or Enter to finish): ").strip()
            if not url:
                break
            evidence_urls.append(url)

    related_tools = []
    tool = input("\nRelated MCP tool 1 (optional, or Enter to skip): ").strip()
    if tool:
        related_tools.append(tool)
        while True:
            tool = input("Related MCP tool (or Enter to finish): ").strip()
            if not tool:
                break
            related_tools.append(tool)

    priority = input("\nPriority (low/medium/high, default: medium): ").strip()
    if priority not in VALID_PRIORITIES:
        priority = "medium"

    tags = []
    tag = input("\nTag 1 (optional, or Enter to skip): ").strip()
    if tag:
        tags.append(tag)
        while True:
            tag = input("Tag (or Enter to finish): ").strip()
            if not tag:
                break
            tags.append(tag)

    notes = input("\nNotes (optional): ").strip()

    # Create config
    config = ConceptCardConfig(
        name=name,
        domain=domain,
        intent_patterns=intent_patterns,
        triggers=triggers,
        procedure_pattern=procedure_pattern,
        description=description,
        evidence_urls=evidence_urls,
        related_tools=related_tools,
        priority=priority,
        tags=tags,
        notes=notes,
    )

    return create_concept_card(config)


def load_concept_card(path: Path) -> dict:
    """Load a concept card from a YAML file."""
    if not path.exists():
        raise FileNotFoundError(f"Concept card not found: {path}")

    with open(path) as f:
        concept = yaml.safe_load(f)

    if not concept:
        raise ValueError(f"Empty concept card: {path}")

    return concept


def validate_concept_card(path: Path) -> tuple[bool, list[str]]:
    """
    Validate a concept card file.

    Args:
        path: Path to the concept card YAML file

    Returns:
        tuple: (is_valid, errors)
    """
    try:
        concept = load_concept_card(path)
        return validate_concept_card_data(concept)
    except Exception as e:
        return False, [str(e)]


def list_concept_cards(
    repo_path: Optional[Path] = None,
    status: Optional[str] = None,
    domain: Optional[str] = None,
) -> list[dict]:
    """
    List all concept cards.

    Args:
        repo_path: Repository root path
        status: Filter by status
        domain: Filter by domain

    Returns:
        list: List of concept card data
    """
    repo = repo_root(repo_path)
    concept_dir = repo / ".agents" / "concept-cards"
    concept_cards = []

    if not concept_dir.exists():
        return concept_cards

    for yaml_file in concept_dir.glob("*.yaml"):
        if yaml_file.name == "SCHEMA.yaml" or yaml_file.name == "TEMPLATE.yaml":
            continue

        try:
            concept = load_concept_card(yaml_file)
            
            # Filter by status
            if status and concept.get("status") != status:
                continue

            # Filter by domain
            if domain and concept.get("domain") != domain:
                continue

            concept["_path"] = str(yaml_file.relative_to(repo))
            concept_cards.append(concept)
        except Exception:
            continue

    return concept_cards


def promote_concept_card(
    concept_id: str,
    repo_path: Optional[Path] = None,
    template: Optional[str] = None,
) -> dict:
    """
    Promote a concept card to a skill.

    Args:
        concept_id: ID of the concept card
        repo_path: Repository root path
        template: Template type to use (auto-detected if not provided)

    Returns:
        dict: Result of skill creation
    """
    from vitools_sync.skill.create import create_skill, CreateSkillConfig

    repo = repo_root(repo_path)
    concept_dir = repo / ".agents" / "concept-cards"
    concept_path = concept_dir / f"{concept_id}.yaml"

    if not concept_path.exists():
        return {
            "success": False,
            "error": f"Concept card '{concept_id}' not found",
        }

    concept = load_concept_card(concept_path)

    # Auto-detect template from domain
    if not template:
        domain_to_template = {
            "MCP Tools": "mcp-tool",
            "API Integrations": "api-integration",
            "Procedures": "procedure",
            "Research": "research",
            "Validation": "validation",
        }
        template = domain_to_template.get(concept.get("domain", ""), "mcp-tool")

    # Create config from concept card
    config = CreateSkillConfig(
        name=concept.get("name", concept_id),
        template=template,
        description=concept.get("description", ""),
        domain=concept.get("domain", "MCP Tools"),
        owner=concept.get("created_by", "vidoxlabs"),
        skill_type=concept.get("skill_type", "Procedure"),
        lifecycle="Intake",
        triggers=concept.get("triggers", []),
        procedure=concept.get("procedure_pattern", ""),
        evidence_urls=concept.get("evidence_urls", []),
        related_tools=concept.get("related_tools", []),
        concept_card_path=concept_path,
    )

    return create_skill(config)
