"""
MCP Fleet Skill Generator for ViTools.

Automatically generates skills for MCP tools in the fleet from the MANIFEST.json
and servers.yaml configuration.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

from vitools_sync.paths import repo_root
from vitools_sync.skill.concept import create_concept_card, ConceptCardConfig
from vitools_sync.skill.create import create_skill_from_template, CreateSkillConfig
from vitools_sync.skill.validate import validate_skill, ValidationConfig
from vitools_sync.legal.overlap import check_skill_overlap
from vitools_sync.catalog.inventory import build_inventory, write_inventory


@dataclass
class MCPToolInfo:
    """Information about an MCP tool from the fleet."""

    name: str
    transport: str
    command: Optional[str] = None
    url: Optional[str] = None
    args: list[str] = field(default_factory=list)
    env: dict = field(default_factory=dict)
    evidence: Optional[str] = None
    license: str = "MIT"
    owner: str = "vidoxlabs"
    description: str = ""
    domain: str = "MCP Tools"


@dataclass
class MCPFleetConfig:
    """Configuration for MCP fleet skill generation."""

    # Source configuration
    manifest_path: Optional[Path] = None  # Path to MANIFEST.json
    servers_yaml_path: Optional[Path] = None  # Path to servers.yaml
    repo_path: Optional[Path] = None  # Repository root

    # Generation options
    tools: list[str] = field(default_factory=list)  # Specific tools to generate
    all_tools: bool = False  # Generate for all tools
    overwrite: bool = False  # Overwrite existing skills
    create_concept_cards: bool = True  # Create concept cards first
    template: str = "mcp-tool"  # Template to use

    # Output options
    output_dir: Optional[Path] = None  # Output directory for skills
    dry_run: bool = False  # Don't actually create files
    
    # Validation options
    run_validation: bool = True  # Run skill validation on generated skills
    run_legal_check: bool = True  # Run legal overlap check on generated skills
    strict_validation: bool = False  # Treat warnings as errors
    
    # Catalog options
    update_catalog: bool = True  # Update catalog inventory after generation


def load_mcp_manifest(path: Optional[Path] = None) -> dict:
    """Load the MCP fleet manifest from vendor/MANIFEST.json."""
    repo = repo_root()
    if path is None:
        manifest_path = repo / "archive" / "vendor" / "MANIFEST.json"
    else:
        manifest_path = path

    if not manifest_path.exists():
        raise FileNotFoundError(f"MANIFEST.json not found: {manifest_path}")

    with open(manifest_path) as f:
        manifest = json.load(f)

    return manifest


def load_servers_yaml(path: Optional[Path] = None) -> dict:
    """Load the MCP servers configuration from catalog/vitools.catalog.json."""
    repo = repo_root()
    if path is None:
        servers_path = repo / "catalog" / "vitools.catalog.json"
    else:
        servers_path = path

    if not servers_path.exists():
        return {"servers": {}}

    with open(servers_path) as f:
        servers = yaml.safe_load(f) or {}

    return servers


def get_mcp_tool_info(tool_name: str, manifest: dict, servers: dict) -> Optional[MCPToolInfo]:
    """Get information about a specific MCP tool from manifest and servers.yaml."""
    # Check manifest for tool info
    mcp_fleet = manifest.get("mcp_fleet_inventory", [])
    tool_info = None
    for tool in mcp_fleet:
        if tool.get("name") == tool_name:
            tool_info = tool
            break

    # Check servers.yaml for transport info
    server_info = servers.get("servers", {}).get(tool_name, {})

    if not tool_info and not server_info:
        return None

    # Build MCPToolInfo
    info = MCPToolInfo(
        name=tool_name,
        transport=server_info.get("transport", "stdio"),
        command=server_info.get("command"),
        url=server_info.get("url"),
        args=server_info.get("args", []),
        env=server_info.get("env", {}),
        evidence=server_info.get("evidence"),
    )

    # Add info from manifest
    if tool_info:
        if "license" in tool_info:
            info.license = tool_info["license"]
        if "owner" in tool_info:
            info.owner = tool_info["owner"]
        if "note" in tool_info:
            info.description = tool_info["note"]

    return info


def get_all_mcp_tools(manifest: dict, servers: dict) -> list[MCPToolInfo]:
    """Get all MCP tools from the manifest and servers.yaml."""
    tools = []
    mcp_fleet = manifest.get("mcp_fleet_inventory", [])

    for tool_info in mcp_fleet:
        tool_name = tool_info.get("name")
        if tool_name:
            info = get_mcp_tool_info(tool_name, manifest, servers)
            if info:
                tools.append(info)

    # Also check servers.yaml for tools not in manifest
    server_tools = servers.get("servers", {})
    for tool_name in server_tools:
        if not any(t.name == tool_name for t in tools):
            info = MCPToolInfo(
                name=tool_name,
                transport=server_tools[tool_name].get("transport", "stdio"),
                command=server_tools[tool_name].get("command"),
                url=server_tools[tool_name].get("url"),
                args=server_tools[tool_name].get("args", []),
                env=server_tools[tool_name].get("env", {}),
                evidence=server_tools[tool_name].get("evidence"),
            )
            tools.append(info)

    return tools


def generate_tool_description(tool_info: MCPToolInfo) -> str:
    """Generate a description for an MCP tool skill."""
    transport = tool_info.transport
    
    if transport == "remote":
        return f"MCP server for {tool_info.name} providing remote access to {tool_info.name} functionality"
    elif transport == "stdio":
        return f"MCP server for {tool_info.name} providing stdio-based access to {tool_info.name} capabilities"
    else:
        return f"MCP server integration for {tool_info.name}"


def generate_tool_summary(tool_info: MCPToolInfo) -> str:
    """Generate a summary for an MCP tool skill."""
    return f"Interact with {tool_info.name} via MCP to perform operations"


def generate_tool_triggers(tool_info: MCPToolInfo) -> list[str]:
    """Generate triggers for an MCP tool skill."""
    return [
        f"User needs to interact with {tool_info.name}",
        f"User requests {tool_info.name} operations",
        f"User wants to use {tool_info.name} capabilities",
    ]


def generate_tool_inputs(tool_info: MCPToolInfo) -> list[str]:
    """Generate inputs for an MCP tool skill."""
    inputs = ["MCP client connection"]
    
    if tool_info.transport == "stdio":
        if tool_info.command:
            inputs.append(f"Command: {tool_info.command}")
        if tool_info.args:
            inputs.append(f"Args: {tool_info.args}")
    elif tool_info.transport == "remote":
        if tool_info.url:
            inputs.append(f"URL: {tool_info.url}")
    
    inputs.append("Method name (optional)")
    inputs.append("Parameters (optional)")
    
    return inputs


def generate_tool_outputs(tool_info: MCPToolInfo) -> list[str]:
    """Generate outputs for an MCP tool skill."""
    return [
        "Method results",
        "Resource listings",
        "Tool-specific responses",
        "Error messages",
    ]


def generate_tool_procedure(tool_info: MCPToolInfo) -> str:
    """Generate procedure for an MCP tool skill."""
    transport = tool_info.transport
    
    procedure = f"""1. Connect to {tool_info.name} MCP server
2. List available resources and tools
3. Call specific methods with parameters
4. Receive and parse responses
5. Return formatted results"""
    
    if transport == "stdio":
        if tool_info.command:
            procedure += f"\n\nTransport: stdio via `{tool_info.command}`"
        if tool_info.args:
            procedure += f"\nArgs: {tool_info.args}"
    elif transport == "remote":
        if tool_info.url:
            procedure += f"\n\nTransport: remote at {tool_info.url}"
    
    return procedure


def generate_tool_guardrails(tool_info: MCPToolInfo) -> str:
    """Generate guardrails for an MCP tool skill."""
    return f"""- Always validate method names and parameters
- Handle connection errors gracefully
- Respect rate limits
- Never expose sensitive data
- Validate all inputs before making calls
- Handle timeouts appropriately"""


def generate_tool_good_examples(tool_info: MCPToolInfo) -> str:
    """Generate good examples for an MCP tool skill."""
    return f"""User: "List all resources from {tool_info.name}"
Agent: Calls list_resources method
Output: Returns formatted list of available resources

User: "Get information about a specific resource"
Agent: Calls read_resource with resource URI
Output: Returns resource content and metadata"""


def generate_tool_bad_examples(tool_info: MCPToolInfo) -> str:
    """Generate bad examples for an MCP tool skill."""
    return f"""User: "Execute arbitrary code on {tool_info.name}"
Agent: Attempts to execute code
Output: Blocked by guardrails

User: "Access sensitive data from {tool_info.name}"
Agent: Returns sensitive data without validation
Output: Data leakage prevented by guardrails"""


def generate_tool_verification(tool_info: MCPToolInfo) -> str:
    """Generate verification commands for an MCP tool skill."""
    commands = [
        "# Check skill structure",
        f"vitools-sync skill validate skills/{tool_info.name}-mcp/SKILL.md",
        "",
        "# Check for legal compliance",
        f"vitools-sync legal check skills/{tool_info.name}-mcp/SKILL.md",
        "",
        "# Verify MCP server connectivity (when available)",
        f"# vilabs mcp list | grep {tool_info.name}",
    ]
    
    return "\n".join(commands)


def generate_concept_card_for_tool(tool_info: MCPToolInfo) -> ConceptCardConfig:
    """Generate a concept card configuration for an MCP tool."""
    return ConceptCardConfig(
        name=f"{tool_info.name}-mcp",
        domain="MCP Tools",
        intent_patterns=[
            f"interact with {tool_info.name}",
            f"use {tool_info.name} capabilities",
            f"access {tool_info.name} via MCP",
        ],
        triggers=[
            f"user needs {tool_info.name} functionality",
            f"user requests {tool_info.name} operations",
            f"user wants to use {tool_info.name}",
        ],
        procedure_pattern=f"Connect to {tool_info.name} MCP server. List resources. Call methods. Return results.",
        description=f"MCP integration for {tool_info.name}",
        evidence_urls=[tool_info.evidence] if tool_info.evidence else [],
        related_tools=[tool_info.name],
        priority="high",
        tags=["mcp", tool_info.name],
    )


def generate_skill_config_for_tool(tool_info: MCPToolInfo) -> CreateSkillConfig:
    """Generate a skill configuration for an MCP tool."""
    return CreateSkillConfig(
        name=f"{tool_info.name}-mcp",
        template="mcp-tool",
        description=generate_tool_description(tool_info),
        domain="MCP Tools",
        owner=tool_info.owner,
        skill_type="MCP Integration",
        lifecycle="Intake",
        summary=generate_tool_summary(tool_info),
        triggers=generate_tool_triggers(tool_info),
        inputs=generate_tool_inputs(tool_info),
        outputs=generate_tool_outputs(tool_info),
        procedure=generate_tool_procedure(tool_info),
        guardrails=generate_tool_guardrails(tool_info),
        good_examples=generate_tool_good_examples(tool_info),
        bad_examples=generate_tool_bad_examples(tool_info),
        verification=generate_tool_verification(tool_info),
        evidence_urls=[tool_info.evidence] if tool_info.evidence else [],
        related_tools=[tool_info.name],
    )


def generate_mcp_tool_skill(
    tool_name: str,
    config: MCPFleetConfig,
) -> dict:
    """
    Generate a skill for a single MCP tool.
    
    Args:
        tool_name: Name of the MCP tool
        config: Generation configuration
    
    Returns:
        dict: Result with status and paths
    """
    repo = repo_root(config.repo_path)
    result = {
        "success": False,
        "tool": tool_name,
        "errors": [],
        "warnings": [],
    }

    try:
        # Load source data
        manifest = load_mcp_manifest(config.manifest_path)
        servers = load_servers_yaml(config.servers_yaml_path)
        tool_info = get_mcp_tool_info(tool_name, manifest, servers)

        if not tool_info:
            result["errors"].append(f"Tool '{tool_name}' not found in manifest or servers.yaml")
            return result

        # Generate concept card if requested
        concept_path = None
        if config.create_concept_cards:
            concept_config = generate_concept_card_for_tool(tool_info)
            concept_result = create_concept_card(concept_config, repo)
            if concept_result["success"]:
                concept_path = Path(concept_result["path"])
                result["concept_card"] = str(concept_path)
            else:
                result["warnings"].extend(concept_result.get("errors", []))

        # Generate skill
        skill_config = generate_skill_config_for_tool(tool_info)
        skill_config.concept_card_path = concept_path

        if config.dry_run:
            result["success"] = True
            result["dry_run"] = True
            result["skill_config"] = skill_config.__dict__
            return result

        skill_result = create_skill_from_template(
            name=skill_config.name,
            template=skill_config.template,
            description=skill_config.description,
            domain=skill_config.domain,
            summary=skill_config.summary,
            triggers=skill_config.triggers,
            inputs=skill_config.inputs,
            outputs=skill_config.outputs,
            procedure=skill_config.procedure,
            guardrails=skill_config.guardrails,
            good_examples=skill_config.good_examples,
            bad_examples=skill_config.bad_examples,
            verification=skill_config.verification,
            evidence_urls=skill_config.evidence_urls,
            related_tools=skill_config.related_tools,
            concept_card_path=concept_path,
        )

        if skill_result["success"]:
            result.update(skill_result)
            result["success"] = True
            
            # Run validation and legal checks if requested and not dry run
            if not config.dry_run and result.get("skill_path"):
                skill_full_path = Path(result["skill_path"]) / "SKILL.md"
                
                # Run validation if requested
                if config.run_validation and skill_full_path.exists():
                    validation_config = ValidationConfig(
                        strict=config.strict_validation,
                        check_legal=False,
                    )
                    validation_result = validate_generated_skill(
                        skill_full_path, validation_config
                    )
                    result["validation"] = validation_result
                    if not validation_result["passed"]:
                        result["warnings"].extend(validation_result.get("warnings", []))
                        if config.strict_validation:
                            result["errors"].extend(validation_result.get("errors", []))
                            result["success"] = False
                
                # Run legal check if requested
                if config.run_legal_check and skill_full_path.exists():
                    legal_result = check_legal_generated_skill(
                        skill_full_path, config.repo_path
                    )
                    result["legal_check"] = legal_result
                    if not legal_result["passed"]:
                        result["warnings"].extend(
                            [f"Legal issue: {issue}" for issue in legal_result.get("issues", [])]
                        )
                        result["success"] = False
        else:
            result["errors"].extend(skill_result.get("errors", []))
            result["warnings"].extend(skill_result.get("warnings", []))

    except Exception as e:
        result["errors"].append(str(e))

    return result


def generate_all_mcp_tool_skills(config: MCPFleetConfig) -> dict:
    """
    Generate skills for all MCP tools in the fleet.
    
    Args:
        config: Generation configuration
    
    Returns:
        dict: Summary result with all tool results
    """
    repo = repo_root(config.repo_path)
    result = {
        "success": False,
        "total": 0,
        "generated": 0,
        "failed": 0,
        "validated": 0,
        "validation_failed": 0,
        "legal_checked": 0,
        "legal_failed": 0,
        "results": {},
        "errors": [],
        "warnings": [],
        "catalog_updated": False,
        "catalog_path": None,
    }

    try:
        # Load source data
        manifest = load_mcp_manifest(config.manifest_path)
        servers = load_servers_yaml(config.servers_yaml_path)
        tools = get_all_mcp_tools(manifest, servers)

        result["total"] = len(tools)

        # Filter to specific tools if requested
        if config.tools:
            tools = [t for t in tools if t.name in config.tools]

        # Validation config
        validation_config = ValidationConfig(
            strict=config.strict_validation,
            check_legal=False,  # We'll do legal check separately
        )

        # Generate skills for each tool
        for tool_info in tools:
            tool_result = generate_mcp_tool_skill(tool_info.name, config)
            result["results"][tool_info.name] = tool_result

            if tool_result["success"]:
                result["generated"] += 1
                
                # Get the skill path for validation and legal checks
                skill_path = tool_result.get("skill_path")
                if skill_path and not config.dry_run:
                    skill_full_path = Path(skill_path) / "SKILL.md"
                    
                    # Run validation if requested
                    if config.run_validation and skill_full_path.exists():
                        validation_result = validate_generated_skill(
                            skill_full_path, validation_config
                        )
                        tool_result["validation"] = validation_result
                        if validation_result["passed"]:
                            result["validated"] += 1
                        else:
                            result["validation_failed"] += 1
                            result["errors"].extend(validation_result.get("errors", []))
                            tool_result["warnings"].extend(validation_result.get("warnings", []))
                    
                    # Run legal check if requested
                    if config.run_legal_check and skill_full_path.exists():
                        legal_result = check_legal_generated_skill(
                            skill_full_path, config.repo_path
                        )
                        tool_result["legal_check"] = legal_result
                        if legal_result["passed"]:
                            result["legal_checked"] += 1
                        else:
                            result["legal_failed"] += 1
                            result["errors"].extend(legal_result.get("issues", []))
                            tool_result["warnings"].extend(
                                [f"Legal issue: {issue}" for issue in legal_result.get("issues", [])]
                            )
            else:
                result["failed"] += 1
                result["errors"].extend(tool_result.get("errors", []))

        # Update catalog if requested and we generated skills
        if config.update_catalog and result["generated"] > 0 and not config.dry_run:
            try:
                inventory = build_inventory(repo)
                catalog_path = write_inventory(repo, inventory)
                result["catalog_updated"] = True
                result["catalog_path"] = str(catalog_path)
            except Exception as e:
                result["warnings"].append(f"Catalog update failed: {e}")

        result["success"] = (
            result["failed"] == 0 and 
            result["validation_failed"] == 0 and 
            result["legal_failed"] == 0
        )

    except Exception as e:
        result["errors"].append(str(e))

    return result


def update_servers_yaml(
    tool_name: str,
    transport: str,
    evidence_url: Optional[str] = None,
    command: Optional[str] = None,
    args: Optional[list[str]] = None,
    url: Optional[str] = None,
    repo_path: Optional[Path] = None,
) -> bool:
    """Add or update an MCP server entry in servers.yaml."""
    repo = repo_root(repo_path)
    servers_path = repo / "catalog" / "vitools.catalog.json"

    # Load existing servers
    if servers_path.exists():
        with open(servers_path) as f:
            servers = yaml.safe_load(f) or {}
    else:
        servers = {"schema_version": "1.0.0", "owner": "vidoxlabs", "servers": {}}

    # Update server entry
    server_entry = {
        "transport": transport,
    }
    
    if evidence_url:
        server_entry["evidence"] = evidence_url
    if command:
        server_entry["command"] = command
    if args:
        server_entry["args"] = args
    if url:
        server_entry["url"] = url

    servers["servers"][tool_name] = server_entry

    # Write back
    servers_path.parent.mkdir(parents=True, exist_ok=True)
    with open(servers_path, "w") as f:
        yaml.dump(servers, f, sort_keys=False)

    return True


def validate_generated_skill(
    skill_path: Path,
    config: ValidationConfig,
) -> dict:
    """Validate a generated skill file."""
    result = {
        "passed": False,
        "errors": [],
        "warnings": [],
    }
    
    try:
        validation_result = validate_skill(skill_path, config)
        result["passed"] = validation_result.passed
        result["errors"] = validation_result.errors
        result["warnings"] = validation_result.warnings
    except Exception as e:
        result["errors"].append(f"Validation error: {e}")
    
    return result


def check_legal_generated_skill(
    skill_path: Path,
    repo_path: Optional[Path] = None,
) -> dict:
    """Check legal overlap for a generated skill."""
    result = {
        "passed": False,
        "issues": [],
    }
    
    try:
        repo = repo_root(repo_path)
        overlap_result = check_skill_overlap(repo, skill_path)
        result["passed"] = overlap_result.passed
        result["issues"] = overlap_result.issues
    except Exception as e:
        result["issues"].append(f"Legal check error: {e}")
    
    return result
