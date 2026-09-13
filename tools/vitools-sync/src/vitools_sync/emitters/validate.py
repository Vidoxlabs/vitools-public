"""
Platform Export Validation for ViTools.

Provides validation functionality for exported platform configurations.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class PlatformValidationResult:
    """Result of validating a platform export."""
    platform: str
    passed: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)


def validate_cursor_export(target: Path) -> PlatformValidationResult:
    """Validate Cursor platform export."""
    result = PlatformValidationResult(platform="cursor")
    
    # Check mcp.json exists and is valid JSON
    mcp_file = target / "mcp.json"
    if not mcp_file.exists():
        result.add_error("mcp.json not found")
    else:
        try:
            with open(mcp_file) as f:
                mcp_data = json.load(f)
            if "mcpServers" not in mcp_data:
                result.add_error("mcp.json missing 'mcpServers' key")
            else:
                result.add_check("mcp_config_valid", True)
        except json.JSONDecodeError as e:
            result.add_error(f"mcp.json is not valid JSON: {e}")
    
    # Check skills directory exists
    skills_dir = target / "skills"
    if not skills_dir.exists():
        result.add_error("skills/ directory not found")
    else:
        result.add_check("skills_dir_exists", True)
        
        # Check at least one skill exists
        skill_count = 0
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill_count += 1
        
        if skill_count == 0:
            result.add_warning("No skills found in skills/ directory")
        else:
            result.add_check("skills_exist", True)
    
    return result


def validate_devin_export(target: Path) -> PlatformValidationResult:
    """Validate Devin platform export."""
    result = PlatformValidationResult(platform="devin")
    
    # Check mcp_config.json exists and is valid JSON
    mcp_file = target / "mcp_config.json"
    if not mcp_file.exists():
        result.add_error("mcp_config.json not found")
    else:
        try:
            with open(mcp_file) as f:
                mcp_data = json.load(f)
            if "mcpServers" not in mcp_data:
                result.add_error("mcp_config.json missing 'mcpServers' key")
            else:
                result.add_check("mcp_config_valid", True)
        except json.JSONDecodeError as e:
            result.add_error(f"mcp_config.json is not valid JSON: {e}")
    
    # Check skills directory exists
    skills_dir = target / "skills"
    if not skills_dir.exists():
        result.add_error("skills/ directory not found")
    else:
        result.add_check("skills_dir_exists", True)
        
        # Check at least one skill exists
        skill_count = 0
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill_count += 1
        
        if skill_count == 0:
            result.add_warning("No skills found in skills/ directory")
        else:
            result.add_check("skills_exist", True)
    
    return result


def validate_grok_export(target: Path) -> PlatformValidationResult:
    """Validate Grok platform export."""
    result = PlatformValidationResult(platform="grok")
    
    # Check mcp.json exists and is valid JSON
    mcp_file = target / "mcp.json"
    if not mcp_file.exists():
        result.add_error("mcp.json not found")
    else:
        try:
            with open(mcp_file) as f:
                mcp_data = json.load(f)
            if "servers" not in mcp_data:
                result.add_error("mcp.json missing 'servers' key")
            else:
                result.add_check("mcp_config_valid", True)
        except json.JSONDecodeError as e:
            result.add_error(f"mcp.json is not valid JSON: {e}")
    
    # Check skills directory exists
    skills_dir = target / "skills"
    if not skills_dir.exists():
        result.add_error("skills/ directory not found")
    else:
        result.add_check("skills_dir_exists", True)
        
        # Check at least one skill exists
        skill_count = 0
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill_count += 1
        
        if skill_count == 0:
            result.add_warning("No skills found in skills/ directory")
        else:
            result.add_check("skills_exist", True)
    
    return result


def validate_opencode_export(target: Path) -> PlatformValidationResult:
    """Validate OpenCode platform export."""
    result = PlatformValidationResult(platform="opencode")
    
    # Check opencode.json exists and is valid JSON
    config_file = target / "opencode.json"
    if not config_file.exists():
        result.add_error("opencode.json not found")
    else:
        try:
            with open(config_file) as f:
                config_data = json.load(f)
            if "mcp" not in config_data:
                result.add_error("opencode.json missing 'mcp' key")
            else:
                result.add_check("mcp_config_valid", True)
                
                # Check schema
                if "$schema" not in config_data:
                    result.add_warning("opencode.json missing '$schema' key")
        except json.JSONDecodeError as e:
            result.add_error(f"opencode.json is not valid JSON: {e}")
    
    # Check skills directory exists
    skills_dir = target / "skills"
    if not skills_dir.exists():
        result.add_error("skills/ directory not found")
    else:
        result.add_check("skills_dir_exists", True)
        
        # Check at least one skill exists
        skill_count = 0
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill_count += 1
        
        if skill_count == 0:
            result.add_warning("No skills found in skills/ directory")
        else:
            result.add_check("skills_exist", True)
    
    return result


def validate_mistral_export(target: Path) -> PlatformValidationResult:
    """Validate Mistral Vibe platform export."""
    result = PlatformValidationResult(platform="mistral")
    
    # Check config.toml.fragment exists
    config_file = target / "config.toml.fragment"
    if not config_file.exists():
        result.add_error("config.toml.fragment not found")
    else:
        try:
            with open(config_file) as f:
                content = f.read()
            
            # Check for TOML structure
            if "[[mcp_servers]]" not in content:
                result.add_error("config.toml.fragment missing '[[mcp_servers]]' sections")
            else:
                result.add_check("mcp_config_valid", True)
            
            # Check for header comment
            if "# Generated by vitools-sync" not in content:
                result.add_warning("config.toml.fragment missing generated header")
                
        except Exception as e:
            result.add_error(f"Error reading config.toml.fragment: {e}")
    
    # Check skills directory exists
    skills_dir = target / "skills"
    if not skills_dir.exists():
        result.add_error("skills/ directory not found")
    else:
        result.add_check("skills_dir_exists", True)
        
        # Check at least one skill exists
        skill_count = 0
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill_count += 1
        
        if skill_count == 0:
            result.add_warning("No skills found in skills/ directory")
        else:
            result.add_check("skills_exist", True)
    
    return result


def validate_antigravity_export(target: Path) -> PlatformValidationResult:
    """Validate Antigravity platform export."""
    result = PlatformValidationResult(platform="antigravity")
    
    # Check mcp_config.json exists and is valid JSON
    mcp_file = target / "mcp_config.json"
    if not mcp_file.exists():
        result.add_error("mcp_config.json not found")
    else:
        try:
            with open(mcp_file) as f:
                mcp_data = json.load(f)
            if "mcpServers" not in mcp_data:
                result.add_error("mcp_config.json missing 'mcpServers' key")
            else:
                result.add_check("mcp_config_valid", True)
                
                # Check serverUrl in entries
                for name, server in mcp_data.get("mcpServers", {}).items():
                    if "serverUrl" not in server and "command" not in server:
                        result.add_warning(f"Server {name} missing 'serverUrl' or 'command'")
                        
        except json.JSONDecodeError as e:
            result.add_error(f"mcp_config.json is not valid JSON: {e}")
    
    # Check skills directory exists
    skills_dir = target / "skills"
    if not skills_dir.exists():
        result.add_error("skills/ directory not found")
    else:
        result.add_check("skills_dir_exists", True)
        
        # Check at least one skill exists
        skill_count = 0
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill_count += 1
        
        if skill_count == 0:
            result.add_warning("No skills found in skills/ directory")
        else:
            result.add_check("skills_exist", True)
    
    return result


# Map platform names to validation functions
PLATFORM_VALIDATORS = {
    "cursor": validate_cursor_export,
    "devin": validate_devin_export,
    "grok": validate_grok_export,
    "opencode": validate_opencode_export,
    "mistral": validate_mistral_export,
    "antigravity": validate_antigravity_export,
}


def validate_platform_export(
    platform: str,
    target: Path,
) -> PlatformValidationResult:
    """Validate an exported platform configuration."""
    validator = PLATFORM_VALIDATORS.get(platform)
    if validator is None:
        return PlatformValidationResult(
            platform=platform,
            passed=False,
            errors=[f"Unknown platform: {platform}"],
        )
    return validator(target)


def add_error(self: PlatformValidationResult, check_name: str, message: str) -> None:
    """Add an error to the result."""
    self.errors.append(f"[{check_name}] {message}")
    self.checks[check_name] = False
    self.passed = False


def add_warning(self: PlatformValidationResult, check_name: str, message: str) -> None:
    """Add a warning to the result."""
    self.warnings.append(f"[{check_name}] {message}")
    self.checks[check_name] = True


def add_check(self: PlatformValidationResult, check_name: str, passed: bool, message: str = "") -> None:
    """Add a check result."""
    self.checks[check_name] = passed
    if not passed:
        self.errors.append(f"[{check_name}] {message}")
        self.passed = False


# Monkey-patch the methods onto the dataclass
PlatformValidationResult.add_error = add_error
PlatformValidationResult.add_warning = add_warning
PlatformValidationResult.add_check = add_check