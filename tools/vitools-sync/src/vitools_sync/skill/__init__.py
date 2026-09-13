"""
Skill creation and management module for ViTools.

This module provides functionality for:
- Creating new skills from templates
- Generating concept cards
- Validating skills
- Managing skill lifecycle
- Batch MCP fleet skill generation
"""

from vitools_sync.skill.create import create_skill, CreateSkillConfig, create_skill_from_template
from vitools_sync.skill.concept import create_concept_card, validate_concept_card, ConceptCardConfig
from vitools_sync.skill.validate import validate_skill, ValidationResult, ValidationConfig
from vitools_sync.skill.mcp_gen import (
    MCPToolInfo,
    MCPFleetConfig,
    load_mcp_manifest,
    load_servers_yaml,
    get_mcp_tool_info,
    get_all_mcp_tools,
    generate_mcp_tool_skill,
    generate_all_mcp_tool_skills,
    update_servers_yaml,
)
from vitools_sync.skill.lifecycle import (
    LifecycleState,
    LifecycleConfig,
    TransitionResult,
    get_skill_lifecycle,
    set_skill_lifecycle,
    validate_transition,
    promote_skill,
    list_skills_by_lifecycle,
    get_lifecycle_history,
    run_pre_promotion_checks,
)

__all__ = [
    "create_skill",
    "CreateSkillConfig",
    "create_skill_from_template",
    "create_concept_card",
    "ConceptCardConfig",
    "validate_concept_card",
    "validate_skill",
    "ValidationResult",
    "ValidationConfig",
    "MCPToolInfo",
    "MCPFleetConfig",
    "load_mcp_manifest",
    "load_servers_yaml",
    "get_mcp_tool_info",
    "get_all_mcp_tools",
    "generate_mcp_tool_skill",
    "generate_all_mcp_tool_skills",
    "update_servers_yaml",
    "LifecycleState",
    "LifecycleConfig",
    "TransitionResult",
    "get_skill_lifecycle",
    "set_skill_lifecycle",
    "validate_transition",
    "promote_skill",
    "list_skills_by_lifecycle",
    "get_lifecycle_history",
    "run_pre_promotion_checks",
]
