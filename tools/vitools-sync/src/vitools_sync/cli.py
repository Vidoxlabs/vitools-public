from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional

import typer

from vitools_sync.catalog.inventory import build_inventory, write_inventory
from vitools_sync.emitters import emit_platform, emit_all
from vitools_sync.emitters.validate import validate_platform_export, PLATFORM_VALIDATORS
from vitools_sync.hooks.memorix import (
    log_catalog,
    log_emit,
    log_legal_check,
    log_skill_created,
    log_skill_promoted,
    log_skill_deprecated,
    log_concept_card_created,
)
from vitools_sync.install import install_platform
from vitools_sync.legal.overlap import check_skill_overlap
from vitools_sync.legal.monitor import check_archive_contamination
from vitools_sync.paths import repo_root
from vitools_sync.skill.concept import (
    create_concept_card,
    validate_concept_card,
    list_concept_cards,
    promote_concept_card,
    ConceptCardConfig,
)
from vitools_sync.skill.create import create_skill_from_template, CreateSkillConfig
from vitools_sync.skill.validate import validate_skill, ValidationConfig
from vitools_sync.skill.mcp_gen import (
    MCPFleetConfig,
    load_mcp_manifest,
    load_servers_yaml,
    get_mcp_tool_info,
    get_all_mcp_tools,
    generate_mcp_tool_skill,
    generate_all_mcp_tool_skills,
)
from vitools_sync.skill.docs_import import (
    DocsImportConfig,
    generate_from_docs,
    generate_from_context7,
    batch_generate_from_urls,
    fetch_from_url,
    extract_from_text,
)
from vitools_sync.skill.lifecycle import (
    LifecycleState,
    LifecycleConfig,
    promote_skill,
    list_skills_by_lifecycle,
    get_lifecycle_history,
    get_skill_lifecycle,
)

app = typer.Typer(help="Emit Vidoxlabs skills/ + agents/ canonical layer to agent platforms.")
emit_app = typer.Typer(help="Emit platform configs from skills/ + agents/")
catalog_app = typer.Typer(help="Catalog and inventory operations.")
legal_app = typer.Typer(help="Legal gate checks.")
install_app = typer.Typer(help="Install emitted configs to user paths.")
skill_app = typer.Typer(help="Skill creation and management.")
concept_app = typer.Typer(help="Concept card management.")
mcp_app = typer.Typer(help="MCP fleet skill generation.")

app.add_typer(emit_app, name="emit")
app.add_typer(catalog_app, name="catalog")
app.add_typer(legal_app, name="legal")
app.add_typer(install_app, name="install")
app.add_typer(skill_app, name="skill")
app.add_typer(concept_app, name="concept")
app.add_typer(mcp_app, name="mcp")
docs_app = typer.Typer(help="Documentation import operations.")
app.add_typer(docs_app, name="docs")


class Platform(str, Enum):
    cursor = "cursor"
    devin = "devin"
    opencode = "opencode"
    grok = "grok"
    mistral = "mistral"
    antigravity = "antigravity"
    all = "all"


@emit_app.callback(invoke_without_command=True)
def emit(
    ctx: typer.Context,
    platform: Platform = typer.Option(Platform.cursor, "--platform", "-p"),
    target: Optional[Path] = typer.Option(None, "--target", "-t", help="Output directory"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Emit platform configuration from skills/ + agents/."""
    if ctx.invoked_subcommand is not None:
        return
    repo = repo_root(root)
    out = target or (repo / "platforms" / platform.value)
    if platform == Platform.all:
        results = emit_all(repo, repo / "platforms")
        for name, files in results.items():
            typer.echo(f"{name}: {len(files)} file(s) written")
        log_emit("all", sum(len(f) for f in results.values()), str(repo / "platforms"))
    else:
        files = emit_platform(repo, platform.value, out)
        typer.echo(f"Wrote {len(files)} file(s) to {out}")
        log_emit(platform.value, len(files), str(out))


@emit_app.command("validate")
def emit_validate(
    platform: Platform = typer.Option(..., "--platform", "-p", help="Platform to validate"),
    target: Path = typer.Option(..., "--target", "-t", help="Path to exported platform directory"),
) -> None:
    """Validate an exported platform configuration."""
    platform_name = platform.value if platform != Platform.all else ""
    
    if platform == Platform.all:
        typer.echo("Error: Cannot validate 'all' platforms at once. Specify a single platform.", err=True)
        raise typer.Exit(1)
    
    if not target.exists():
        typer.echo(f"Error: Target directory does not exist: {target}", err=True)
        raise typer.Exit(1)
    
    result = validate_platform_export(platform_name, target)
    
    if result.passed:
        typer.echo(f"✓ PASS: {platform_name} export at {target}")
    else:
        typer.echo(f"✗ FAIL: {platform_name} export at {target}")
    
    # Print errors
    if result.errors:
        typer.echo(f"\nErrors ({len(result.errors)}):")
        for error in result.errors:
            typer.echo(f"  - {error}", err=True)
    
    # Print warnings
    if result.warnings:
        typer.echo(f"\nWarnings ({len(result.warnings)}):")
        for warning in result.warnings:
            typer.echo(f"  - {warning}")
    
    # Print check summary
    typer.echo(f"\nChecks: {sum(result.checks.values())}/{len(result.checks)} passed")
    
    raise typer.Exit(0 if result.passed else 1)


@catalog_app.command("build")
def catalog_build(
    root: Optional[Path] = typer.Option(None, "--root"),
    output: Optional[Path] = typer.Option(None, "--output"),
) -> None:
    """Build catalog inventory.json from MANIFEST and plugin indexes."""
    repo = repo_root(root)
    inventory = build_inventory(repo)
    path = write_inventory(repo, inventory, output)
    log_catalog(len(inventory), str(path))
    typer.echo(f"Inventory written: {path} ({len(inventory)} entries)")


@legal_app.command("check")
def legal_check(
    skill_path: Path = typer.Argument(..., help="Path to SKILL.md"),
    root: Optional[Path] = typer.Option(None, "--root"),
) -> None:
    """Check skill text for overlap with vendor content."""
    repo = repo_root(root)
    result = check_skill_overlap(repo, skill_path)
    if result.passed:
        typer.echo(f"PASS: {skill_path}")
        log_legal_check(str(skill_path), True, [])
        raise typer.Exit(0)
    for issue in result.issues:
        typer.echo(f"FAIL: {issue}")
    log_legal_check(str(skill_path), False, result.issues)
    raise typer.Exit(1)


@legal_app.command("monitor")
def legal_monitor(
    no_content: bool = typer.Option(False, "--no-content", help="Skip content similarity scanning (faster)"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Monitor skills/ + agents/ layer for vendor contamination."""
    repo = repo_root(root)
    result = check_archive_contamination(repo, check_content=not no_content)
    
    if result.passed:
        typer.echo(f"✓ PASS: No archive contamination detected")
    else:
        typer.echo(f"✗ FAIL: Archive contamination detected")
    
    # Print errors
    if result.errors:
        typer.echo(f"\nErrors ({len(result.errors)}):")
        for error in result.errors:
            typer.echo(f"  - {error}", err=True)
    
    # Print warnings
    if result.warnings:
        typer.echo(f"\nWarnings ({len(result.warnings)}):")
        for warning in result.warnings:
            typer.echo(f"  - {warning}")
    
    # Print check summary
    typer.echo(f"\nChecks: {sum(result.checks.values())}/{len(result.checks)} passed")
    
    raise typer.Exit(0 if result.passed else 1)


@legal_app.command("check-advanced")
def legal_check_advanced(
    skill_path: Path = typer.Argument(..., help="Path to SKILL.md or directory"),
    ngram_threshold: float = typer.Option(0.15, "--ngram", help="N-gram overlap threshold (0.0-1.0)"),
    lcs_threshold: int = typer.Option(80, "--lcs", help="Longest common substring threshold"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Advanced legal check with configurable thresholds."""
    repo = repo_root(root)
    
    # Handle directory or single file
    if skill_path.is_dir():
        # Check all SKILL.md files in directory
        skill_files = list(skill_path.rglob("SKILL.md"))
        if not skill_files:
            typer.echo(f"No SKILL.md files found in: {skill_path}", err=True)
            raise typer.Exit(1)
        
        all_passed = True
        for skill_file in skill_files:
            result = check_skill_overlap(repo, skill_file, 
                                       ngram_threshold=ngram_threshold, 
                                       lcs_threshold=lcs_threshold)
            if result.passed:
                typer.echo(f"✓ PASS: {skill_file}")
            else:
                typer.echo(f"✗ FAIL: {skill_file}")
                all_passed = False
                for issue in result.issues:
                    typer.echo(f"    - {issue}", err=True)
        
        raise typer.Exit(0 if all_passed else 1)
    else:
        # Single file
        result = check_skill_overlap(repo, skill_path,
                                   ngram_threshold=ngram_threshold,
                                   lcs_threshold=lcs_threshold)
        
        if result.passed:
            typer.echo(f"✓ PASS: {skill_path}")
            typer.echo(f"  N-gram overlap: {result.ngram_overlap_ratio:.1%}")
            typer.echo(f"  Longest match: {result.longest_match} chars")
            raise typer.Exit(0)
        else:
            typer.echo(f"✗ FAIL: {skill_path}")
            typer.echo(f"  N-gram overlap: {result.ngram_overlap_ratio:.1%} (threshold: {ngram_threshold:.0%})")
            typer.echo(f"  Longest match: {result.longest_match} chars (threshold: {lcs_threshold})")
            for issue in result.issues:
                typer.echo(f"    - {issue}", err=True)
            raise typer.Exit(1)


@install_app.callback(invoke_without_command=True)
def install(
    ctx: typer.Context,
    platform: Platform = typer.Option(..., "--platform", "-p"),
    user: bool = typer.Option(False, "--user", help="Install to user home paths"),
    dry_run: bool = typer.Option(True, "--dry-run/--apply", help="Preview only unless --apply"),
    root: Optional[Path] = typer.Option(None, "--root"),
) -> None:
    """Install emitted platform configs to project or user paths."""
    if ctx.invoked_subcommand is not None:
        return
    if platform == Platform.all:
        typer.echo("Use --platform with a specific target for install")
        raise typer.Exit(2)
    repo = repo_root(root)
    actions = install_platform(repo, platform.value, user=user, dry_run=dry_run)
    for action in actions:
        typer.echo(action)
    typer.echo(f"{'Dry-run' if dry_run else 'Applied'}: {len(actions)} action(s)")


# ============================================================================
# Skill Commands
# ============================================================================


class TemplateType(str, Enum):
    mcp_tool = "mcp-tool"
    api_integration = "api-integration"
    procedure = "procedure"
    research = "research"
    validation = "validation"


@skill_app.command("create")
def skill_create(
    name: str = typer.Argument(..., help="Name of the skill to create"),
    template: TemplateType = typer.Option(
        TemplateType.mcp_tool, "--template", "-t", help="Template type to use"
    ),
    description: str = typer.Option("", "--description", "-d", help="Skill description"),
    domain: str = typer.Option("MCP Tools", "--domain", help="Skill domain"),
    concept_card: Optional[Path] = typer.Option(
        None, "--concept-card", "-c", help="Path to concept card YAML file"
    ),
    output: bool = typer.Option(False, "--output/--no-output", help="Print the created skill"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Create a new skill from a template."""
    result = create_skill_from_template(
        name=name,
        template=template.value,
        target_dir=root,
        concept_card_path=concept_card,
        description=description,
        domain=domain,
    )

    if result["success"]:
        typer.echo(f"✓ Skill created: {result['message']}")
        typer.echo(f"  Path: {result['skill_path']}")
        if result.get("files_created"):
            typer.echo(f"  Files: {', '.join(result['files_created'])}")
        if result.get("warnings"):
            for warning in result["warnings"]:
                typer.echo(f"  ⚠ {warning}", err=True)

        # Log to Memorix
        skill_path = Path(result["skill_path"])
        log_skill_created(
            str(skill_path / "SKILL.md"),
            skill_path.name,
            "Intake"
        )

        if output and result.get("skill_path"):
            skill_file = Path(result["skill_path"]) / "SKILL.md"
            if skill_file.exists():
                typer.echo(f"\n--- Generated Skill Content ---")
                typer.echo(skill_file.read_text())

        raise typer.Exit(0)
    else:
        for error in result.get("errors", []):
            typer.echo(f"✗ Error: {error}", err=True)
        raise typer.Exit(1)


@skill_app.command("validate")
def skill_validate(
    path: Path = typer.Argument(..., help="Path to SKILL.md file"),
    strict: bool = typer.Option(False, "--strict", help="Treat warnings as errors"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Validate a skill against Vidoxlabs standards."""
    config = ValidationConfig(strict=strict)
    result = validate_skill(path, config)

    if result.passed:
        typer.echo(f"✓ PASS: {result.path}")
    else:
        typer.echo(f"✗ FAIL: {result.path}")

    # Print errors
    if result.errors:
        typer.echo(f"\nErrors ({len(result.errors)}):")
        for error in result.errors:
            typer.echo(f"  - {error}", err=True)

    # Print warnings
    if result.warnings:
        typer.echo(f"\nWarnings ({len(result.warnings)}):")
        for warning in result.warnings:
            typer.echo(f"  - {warning}")

    # Print check summary
    typer.echo(f"\nChecks: {sum(result.checks.values())}/{len(result.checks)} passed")

    if result.passed:
        raise typer.Exit(0)
    else:
        raise typer.Exit(1)


@skill_app.command("list-templates")
def skill_list_templates(
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """List available skill templates."""
    from vitools_sync.skill.create import TEMPLATE_TYPES

    typer.echo("Available Skill Templates:")
    typer.echo("")
    for name, info in TEMPLATE_TYPES.items():
        typer.echo(f"  {name}:")
        typer.echo(f"    Domain: {info['default_domain']}")
        typer.echo(f"    Type: {info['default_skill_type']}")
        typer.echo("")


# ============================================================================
# Lifecycle Commands
# ============================================================================


class StateType(str, Enum):
    intake = "Intake"
    draft = "Draft"
    review = "Review"
    promoted = "Promoted"
    deprecated = "Deprecated"


@skill_app.command("promote")
def skill_promote(
    path: Path = typer.Argument(..., help="Path to SKILL.md file"),
    to: StateType = typer.Option(..., "--to", "-t", help="Target lifecycle state"),
    force: bool = typer.Option(False, "--force", "-f", help="Bypass validation checks"),
    reason: str = typer.Option("", "--reason", "-r", help="Reason for state change (required for Deprecated)"),
    approver: str = typer.Option("", "--approver", "-a", help="Approver name (required for Promoted)"),
    no_validation: bool = typer.Option(False, "--no-validation", help="Skip skill validation"),
    no_legal: bool = typer.Option(False, "--no-legal", help="Skip legal check"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Promote a skill to a new lifecycle state."""
    config = LifecycleConfig(
        to_state=LifecycleState(to.value),
        force=force,
        reason=reason if reason else None,
        approver=approver if approver else None,
        run_validation=not no_validation,
        run_legal_check=not no_legal,
        strict_validation=True,
    )

    try:
        result = promote_skill(path, to.value, config)

        if result.success:
            typer.echo(f"✓ Skill promoted: {result.from_state} → {result.to_state}")
            typer.echo(f"  Path: {result.skill_path}")
            
            if result.checks_passed:
                typer.echo(f"  Quality gates passed: {len(result.checks_passed)}")
            
            # Log to Memorix
            skill_dir = path.parent
            skill_id = skill_dir.name
            if to.value == "Deprecated":
                log_skill_deprecated(str(path), skill_id, reason or "No reason provided")
            else:
                log_skill_promoted(str(path), skill_id, result.from_state or "Unknown", to.value, approver if approver else None)
            
            # Show updated lifecycle info
            history = get_lifecycle_history(path)
            if history.get("current"):
                typer.echo(f"  Current state: {history['current']}")
            if history.get("updated"):
                typer.echo(f"  Updated: {history['updated']}")
            if history.get("promoted"):
                typer.echo(f"  Promoted: {history['promoted']}")
            if history.get("promoted_by"):
                typer.echo(f"  Promoted by: {history['promoted_by']}")
            if history.get("deprecated"):
                typer.echo(f"  Deprecated: {history['deprecated']}")
            if history.get("deprecated_reason"):
                typer.echo(f"  Deprecation reason: {history['deprecated_reason']}")

            raise typer.Exit(0)
        else:
            typer.echo(f"✗ Failed to promote skill to {to.value}", err=True)
            
            if result.errors:
                typer.echo("\nErrors:")
                for error in result.errors:
                    typer.echo(f"  - {error}", err=True)
            
            if result.checks_failed:
                typer.echo(f"\nQuality gate failures ({len(result.checks_failed)}):")
                for check in result.checks_failed:
                    typer.echo(f"  - {check}", err=True)

            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


@skill_app.command("lifecycle")
def skill_lifecycle(
    path: Path = typer.Argument(..., help="Path to SKILL.md file"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Show the lifecycle state and history of a skill."""
    try:
        history = get_lifecycle_history(path)
        
        if not history:
            typer.echo(f"✗ No lifecycle information found for: {path}", err=True)
            raise typer.Exit(1)
        
        typer.echo(f"Lifecycle History: {path}")
        typer.echo(f"  Current state: {history.get('current', 'Unknown')}")
        typer.echo(f"  Created: {history.get('created', 'N/A')}")
        typer.echo(f"  Updated: {history.get('updated', 'N/A')}")
        
        if history.get("promoted"):
            typer.echo(f"  Promoted: {history['promoted']}")
        if history.get("promoted_by"):
            typer.echo(f"  Promoted by: {history['promoted_by']}")
        if history.get("deprecated"):
            typer.echo(f"  Deprecated: {history['deprecated']}")
        if history.get("deprecated_reason"):
            typer.echo(f"  Deprecation reason: {history['deprecated_reason']}")
        
        raise typer.Exit(0)

    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


@skill_app.command("list-by-lifecycle")
def skill_list_by_lifecycle(
    state: Optional[StateType] = typer.Option(None, "--state", "-s", help="Filter by lifecycle state"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """List skills grouped by lifecycle state."""
    repo = repo_root(root)
    skills_dir = repo / "skills"
    
    try:
        if state:
            skills = list_skills_by_lifecycle(skills_dir, state.value)
        else:
            skills = list_skills_by_lifecycle(skills_dir)
        
        if not skills:
            typer.echo("No skills found.")
            raise typer.Exit(0)
        
        typer.echo("Skills by Lifecycle State:")
        typer.echo("")
        
        for lifecycle_state, skill_names in sorted(skills.items()):
            typer.echo(f"  {lifecycle_state} ({len(skill_names)}):")
            for name in sorted(skill_names):
                typer.echo(f"    - {name}")
            typer.echo("")
        
        typer.echo(f"Total: {sum(len(v) for v in skills.values())} skills")
        raise typer.Exit(0)

    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


@skill_app.command("deprecate")
def skill_deprecate(
    path: Path = typer.Argument(..., help="Path to SKILL.md file"),
    reason: str = typer.Option(..., "--reason", "-r", help="Reason for deprecation"),
    force: bool = typer.Option(False, "--force", "-f", help="Bypass validation checks"),
    no_validation: bool = typer.Option(False, "--no-validation", help="Skip skill validation"),
    no_legal: bool = typer.Option(False, "--no-legal", help="Skip legal check"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Deprecate a skill with a reason."""
    config = LifecycleConfig(
        to_state=LifecycleState.DEPRECATED,
        force=force,
        reason=reason,
        approver=None,
        run_validation=not no_validation,
        run_legal_check=not no_legal,
        strict_validation=True,
    )

    try:
        result = promote_skill(path, "Deprecated", config)

        if result.success:
            typer.echo(f"✓ Skill deprecated: {path}")
            typer.echo(f"  Reason: {reason}")
            
            # Show deprecation info
            history = get_lifecycle_history(path)
            if history.get("deprecated"):
                typer.echo(f"  Deprecated on: {history['deprecated']}")
            if history.get("deprecated_reason"):
                typer.echo(f"  Reason: {history['deprecated_reason']}")

            raise typer.Exit(0)
        else:
            typer.echo(f"✗ Failed to deprecate skill", err=True)
            
            if result.errors:
                typer.echo("\nErrors:")
                for error in result.errors:
                    typer.echo(f"  - {error}", err=True)
            
            if result.checks_failed:
                typer.echo(f"\nQuality gate failures ({len(result.checks_failed)}):")
                for check in result.checks_failed:
                    typer.echo(f"  - {check}", err=True)

            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


# ============================================================================
# Concept Card Commands
# ============================================================================


@concept_app.command("create")
def concept_create(
    name: str = typer.Argument(..., help="Name of the concept card"),
    domain: str = typer.Argument(..., help="Domain/category"),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Create interactively"
    ),
    intent_patterns: list[str] = typer.Option(
        [], "--intent", help="Intent patterns (can be specified multiple times)"
    ),
    triggers: list[str] = typer.Option(
        [], "--trigger", help="Triggers (can be specified multiple times)"
    ),
    procedure: str = typer.Option("", "--procedure", "-p", help="Procedure pattern"),
    description: str = typer.Option("", "--description", "-d", help="Description"),
    evidence_url: list[str] = typer.Option(
        [], "--evidence", help="Evidence URLs (can be specified multiple times)"
    ),
    related_tool: list[str] = typer.Option(
        [], "--tool", help="Related MCP tools (can be specified multiple times)"
    ),
    priority: str = typer.Option("medium", "--priority", help="Priority (low/medium/high)"),
    output: bool = typer.Option(False, "--output/--no-output", help="Print the created concept card"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Create a new concept card."""
    if interactive:
        result = create_concept_card_interactive()
    else:
        # Validate required fields
        if not intent_patterns:
            typer.echo("Error: At least one --intent pattern is required", err=True)
            raise typer.Exit(1)
        if not triggers:
            typer.echo("Error: At least one --trigger is required", err=True)
            raise typer.Exit(1)
        if not procedure:
            typer.echo("Error: --procedure pattern is required", err=True)
            raise typer.Exit(1)

        config = ConceptCardConfig(
            name=name,
            domain=domain,
            intent_patterns=intent_patterns,
            triggers=triggers,
            procedure_pattern=procedure,
            description=description,
            evidence_urls=evidence_url,
            related_tools=related_tool,
            priority=priority,
        )
        result = create_concept_card(config, root)

    if result["success"]:
        typer.echo(f"✓ Concept card created: {result['message']}")
        typer.echo(f"  Path: {result['path']}")
        if result.get("warnings"):
            for warning in result["warnings"]:
                typer.echo(f"  ⚠ {warning}", err=True)

        if output and result.get("path"):
            typer.echo(f"\n--- Generated Concept Card Content ---")
            with open(result["path"]) as f:
                typer.echo(f.read())

        raise typer.Exit(0)
    else:
        for error in result.get("errors", []):
            typer.echo(f"✗ Error: {error}", err=True)
        raise typer.Exit(1)


@concept_app.command("validate")
def concept_validate(
    path: Path = typer.Argument(..., help="Path to concept card YAML file"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Validate a concept card against the schema."""
    is_valid, errors = validate_concept_card(path)

    if is_valid:
        typer.echo(f"✓ PASS: {path}")
        raise typer.Exit(0)
    else:
        typer.echo(f"✗ FAIL: {path}")
        for error in errors:
            typer.echo(f"  - {error}", err=True)
        raise typer.Exit(1)


@concept_app.command("list")
def concept_list(
    domain: Optional[str] = typer.Option(None, "--domain", help="Filter by domain"),
    status: Optional[str] = typer.Option(None, "--status", help="Filter by status"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """List all concept cards."""
    concept_cards = list_concept_cards(root, status=status, domain=domain)

    if not concept_cards:
        typer.echo("No concept cards found.")
        raise typer.Exit(0)

    typer.echo(f"Found {len(concept_cards)} concept card(s):\n")

    for card in concept_cards:
        typer.echo(f"  {card.get('id', 'unknown')}")
        typer.echo(f"    Name: {card.get('name', 'N/A')}")
        typer.echo(f"    Domain: {card.get('domain', 'N/A')}")
        typer.echo(f"    Status: {card.get('status', 'unknown')}")
        typer.echo(f"    Path: {card.get('_path', 'unknown')}")
        typer.echo("")


@concept_app.command("promote")
def concept_promote(
    concept_id: str = typer.Argument(..., help="ID of the concept card to promote"),
    template: Optional[TemplateType] = typer.Option(
        None, "--template", "-t", help="Template type to use (auto-detected if not provided)"
    ),
    output: bool = typer.Option(False, "--output/--no-output", help="Print the created skill"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Promote a concept card to a skill."""
    template_str = template.value if template else None
    result = promote_concept_card(concept_id, root, template_str)

    if result.get("success", False):
        typer.echo(f"✓ Skill created from concept card: {result['message']}")
        typer.echo(f"  Path: {result['skill_path']}")
        if result.get("files_created"):
            typer.echo(f"  Files: {', '.join(result['files_created'])}")
        if result.get("warnings"):
            for warning in result["warnings"]:
                typer.echo(f"  ⚠ {warning}", err=True)

        if output and result.get("skill_path"):
            skill_file = Path(result["skill_path"]) / "SKILL.md"
            if skill_file.exists():
                typer.echo(f"\n--- Generated Skill Content ---")
                typer.echo(skill_file.read_text())

        raise typer.Exit(0)
    else:
        typer.echo(f"✗ Error: {result.get('error', 'Unknown error')}", err=True)
        raise typer.Exit(1)


@concept_app.command("show")
def concept_show(
    concept_id: str = typer.Argument(..., help="ID of the concept card"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Show a concept card's details."""
    from vitools_sync.skill.concept import load_concept_card

    repo = repo_root(root)
    concept_dir = repo / "tools" / "concept-cards"
    concept_path = concept_dir / f"{concept_id}.yaml"

    if not concept_path.exists():
        typer.echo(f"✗ Concept card '{concept_id}' not found", err=True)
        raise typer.Exit(1)

    try:
        concept = load_concept_card(concept_path)
        typer.echo(f"Concept Card: {concept_id}")
        typer.echo(f"Path: {concept_path}\n")

        # Pretty print the YAML
        yaml_str = yaml.dump(concept, sort_keys=False, default_flow_style=False)
        typer.echo(yaml_str)

        raise typer.Exit(0)
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


# Import interactive function
from vitools_sync.skill.concept import create_concept_card_interactive


# ============================================================================
# Documentation Import Commands
# ============================================================================


class DocsTemplate(str, Enum):
    mcp_tool = "mcp-tool"
    api_integration = "api-integration"
    procedure = "procedure"
    research = "research"
    validation = "validation"


@docs_app.command("import")
def docs_import(
    url: str = typer.Argument(..., help="URL to import documentation from"),
    template: DocsTemplate = typer.Option(
        DocsTemplate.api_integration, "--template", "-t", help="Template type to use"
    ),
    no_concept_card: bool = typer.Option(False, "--no-concept-card", help="Skip concept card creation"),
    no_skill: bool = typer.Option(False, "--no-skill", help="Skip skill creation"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be created without creating files"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Import documentation from a URL and generate concept cards and skills."""
    config = DocsImportConfig(
        url=url,
        template=template.value,
        generate_concept_card=not no_concept_card,
        generate_skill=not no_skill,
        output_dir=root,
        dry_run=dry_run,
    )

    try:
        result = generate_from_docs(config)

        if result["success"]:
            typer.echo(f"✓ Documentation imported from: {url}")
            if result.get("concept_card"):
                typer.echo(f"  Concept card: {result['concept_card']}")
            if result.get("skill"):
                typer.echo(f"  Skill: {result['skill']}")
            if result.get("warnings"):
                for warning in result["warnings"]:
                    typer.echo(f"  ⚠ {warning}")
        else:
            typer.echo(f"✗ Failed to import documentation from: {url}", err=True)
            for error in result.get("errors", []):
                typer.echo(f"  - {error}", err=True)

        raise typer.Exit(0 if result["success"] else 1)

    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


@docs_app.command("batch-import")
def docs_batch_import(
    urls: list[str] = typer.Argument(..., help="URLs to import documentation from"),
    template: DocsTemplate = typer.Option(
        DocsTemplate.api_integration, "--template", "-t", help="Template type to use"
    ),
    no_concept_cards: bool = typer.Option(False, "--no-concept-cards", help="Skip concept card creation"),
    no_skills: bool = typer.Option(False, "--no-skills", help="Skip skill creation"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be created without creating files"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Import documentation from multiple URLs and generate concept cards and skills."""
    config_template = DocsImportConfig(
        template=template.value,
        generate_concept_card=not no_concept_cards,
        generate_skill=not no_skills,
        output_dir=root,
        dry_run=dry_run,
    )

    try:
        result = batch_generate_from_urls(urls, config_template)

        typer.echo(f"Batch Documentation Import Summary")
        typer.echo(f"=" * 50)
        typer.echo(f"Total URLs: {result.get('total', 0)}")
        typer.echo(f"Generated: {result.get('generated', 0)}")
        typer.echo(f"Failed: {result.get('failed', 0)}")

        if result.get("errors"):
            typer.echo("\nErrors:")
            for error in result["errors"]:
                typer.echo(f"  - {error}", err=True)

        if dry_run:
            typer.echo("\nDry run mode - no files were created")

        raise typer.Exit(0 if result["success"] else 1)

    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


# ============================================================================
# MCP Fleet Commands
# ============================================================================


@mcp_app.command("generate-skills")
def mcp_generate_skills(
    tool: list[str] = typer.Argument(None, help="Specific tool(s) to generate skills for"),
    all_tools: bool = typer.Option(False, "--all", "-a", help="Generate skills for all MCP tools"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be generated without creating files"),
    no_concept_cards: bool = typer.Option(False, "--no-concept-cards", help="Skip concept card creation"),
    output: bool = typer.Option(False, "--output/--no-output", help="Print generated skill content"),
    no_validation: bool = typer.Option(False, "--no-validation", help="Skip skill validation"),
    no_legal: bool = typer.Option(False, "--no-legal", help="Skip legal overlap check"),
    strict: bool = typer.Option(False, "--strict", help="Treat validation warnings as errors"),
    no_catalog: bool = typer.Option(False, "--no-catalog", help="Skip catalog inventory update"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Generate skills for MCP tools in the fleet."""
    if not tool and not all_tools:
        typer.echo("Error: Must specify --all or at least one tool name", err=True)
        raise typer.Exit(1)

    config = MCPFleetConfig(
        repo_path=root,
        tools=tool if tool else [],
        all_tools=all_tools,
        dry_run=dry_run,
        create_concept_cards=not no_concept_cards,
        run_validation=not no_validation,
        run_legal_check=not no_legal,
        strict_validation=strict,
        update_catalog=not no_catalog,
    )

    if dry_run:
        typer.echo("Dry run mode - no files will be created\n")

    try:
        if all_tools or not tool:
            # Generate for all tools
            result = generate_all_mcp_tool_skills(config)
            typer.echo(f"MCP Fleet Skill Generation Summary")
            typer.echo(f"=" * 50)
            typer.echo(f"Total tools: {result.get('total', 0)}")
            typer.echo(f"Generated: {result.get('generated', 0)}")
            typer.echo(f"Failed: {result.get('failed', 0)}")
            typer.echo(f"Validated: {result.get('validated', 0)}")
            typer.echo(f"Validation failed: {result.get('validation_failed', 0)}")
            typer.echo(f"Legal checked: {result.get('legal_checked', 0)}")
            typer.echo(f"Legal failed: {result.get('legal_failed', 0)}")
            
            if result.get("catalog_updated"):
                typer.echo(f"Catalog updated: {result.get('catalog_path', 'N/A')}")

            if result.get("errors"):
                typer.echo("\nErrors:")
                for error in result["errors"]:
                    typer.echo(f"  - {error}", err=True)

            if result.get("warnings"):
                typer.echo("\nWarnings:")
                for warning in result["warnings"]:
                    typer.echo(f"  - {warning}")

            if dry_run:
                for tool_name, tool_result in result.get("results", {}).items():
                    typer.echo(f"\n[DRY RUN] Would generate skill for: {tool_name}")
                    if "skill_config" in tool_result:
                        skill_config = tool_result["skill_config"]
                        typer.echo(f"  Template: {skill_config.get('template')}")
                        typer.echo(f"  Name: {skill_config.get('name')}")
        else:
            # Generate for specific tools
            for tool_name in tool:
                result = generate_mcp_tool_skill(tool_name, config)
                if result["success"]:
                    typer.echo(f"✓ Generated skill for: {tool_name}")
                    
                    # Show validation results if available
                    if result.get("validation"):
                        val = result["validation"]
                        if val.get("passed"):
                            typer.echo(f"  ✓ Validation passed")
                        else:
                            typer.echo(f"  ✗ Validation failed: {len(val.get('errors', []))} errors")
                    
                    # Show legal check results if available
                    if result.get("legal_check"):
                        legal = result["legal_check"]
                        if legal.get("passed"):
                            typer.echo(f"  ✓ Legal check passed")
                        else:
                            typer.echo(f"  ✗ Legal check failed: {len(legal.get('issues', []))} issues")
                    
                    if result.get("skill_path") and output:
                        skill_file = Path(result["skill_path"]) / "SKILL.md"
                        if skill_file.exists():
                            typer.echo(f"\n--- {tool_name} Skill ---")
                            typer.echo(skill_file.read_text())
                else:
                    typer.echo(f"✗ Failed to generate skill for: {tool_name}", err=True)
                    for error in result.get("errors", []):
                        typer.echo(f"  - {error}", err=True)

        if not dry_run and result.get("generated", 0) > 0:
            typer.echo("\nAll skills generated successfully!")

        raise typer.Exit(0 if result.get("success", True) else 1)

    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


@mcp_app.command("list-tools")
def mcp_list_tools(
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """List all MCP tools in the fleet."""
    try:
        manifest = load_mcp_manifest(None)
        servers = load_servers_yaml(None)
        tools = get_all_mcp_tools(manifest, servers)

        if not tools:
            typer.echo("No MCP tools found in fleet.")
            raise typer.Exit(0)

        typer.echo(f"Found {len(tools)} MCP tool(s) in fleet:\n")

        for tool in tools:
            typer.echo(f"  {tool.name}:")
            typer.echo(f"    Transport: {tool.transport}")
            if tool.command:
                typer.echo(f"    Command: {tool.command}")
            if tool.url:
                typer.echo(f"    URL: {tool.url}")
            if tool.evidence:
                typer.echo(f"    Evidence: {tool.evidence}")
            typer.echo()

        raise typer.Exit(0)

    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


@mcp_app.command("show-tool")
def mcp_show_tool(
    tool_name: str = typer.Argument(..., help="Name of the MCP tool"),
    root: Optional[Path] = typer.Option(None, "--root", help="Vitools repo root"),
) -> None:
    """Show details about a specific MCP tool."""
    try:
        manifest = load_mcp_manifest(None)
        servers = load_servers_yaml(None)
        tool_info = get_mcp_tool_info(tool_name, manifest, servers)

        if not tool_info:
            typer.echo(f"✗ MCP tool '{tool_name}' not found in fleet", err=True)
            raise typer.Exit(1)

        typer.echo(f"MCP Tool: {tool_info.name}")
        typer.echo(f"Transport: {tool_info.transport}")
        typer.echo(f"License: {tool_info.license}")
        typer.echo(f"Owner: {tool_info.owner}")
        
        if tool_info.command:
            typer.echo(f"Command: {tool_info.command}")
        if tool_info.args:
            typer.echo(f"Args: {tool_info.args}")
        if tool_info.url:
            typer.echo(f"URL: {tool_info.url}")
        if tool_info.env:
            typer.echo(f"Env: {tool_info.env}")
        if tool_info.evidence:
            typer.echo(f"Evidence: {tool_info.evidence}")
        if tool_info.description:
            typer.echo(f"Description: {tool_info.description}")

        raise typer.Exit(0)

    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)
