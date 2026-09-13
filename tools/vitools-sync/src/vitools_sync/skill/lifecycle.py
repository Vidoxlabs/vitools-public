"""
Lifecycle Management for ViTools Skills.

Provides functionality to manage skill lifecycle states and transitions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml


class LifecycleState(str, Enum):
    """Valid lifecycle states for skills."""
    INTAKE = "Intake"
    DRAFT = "Draft"
    REVIEW = "Review"
    PROMOTED = "Promoted"
    DEPRECATED = "Deprecated"


# Valid state transitions
VALID_TRANSITIONS = {
    LifecycleState.INTAKE: [LifecycleState.DRAFT, LifecycleState.DEPRECATED],
    LifecycleState.DRAFT: [LifecycleState.REVIEW, LifecycleState.DEPRECATED],
    LifecycleState.REVIEW: [LifecycleState.PROMOTED, LifecycleState.DRAFT, LifecycleState.DEPRECATED],
    LifecycleState.PROMOTED: [LifecycleState.DEPRECATED],
    LifecycleState.DEPRECATED: [],  # No transitions out of deprecated
}


@dataclass
class LifecycleConfig:
    """Configuration for lifecycle state transitions."""
    
    # Target state
    to_state: LifecycleState
    
    # Options
    force: bool = False  # Bypass validation checks
    reason: Optional[str] = None  # Reason for state change (required for deprecation)
    approver: Optional[str] = None  # Who approved the change (required for Promoted)
    
    # Quality gate options
    run_validation: bool = True  # Run skill validation before promotion
    run_legal_check: bool = True  # Run legal check before promotion
    strict_validation: bool = True  # Treat warnings as errors for promotion


@dataclass
class TransitionResult:
    """Result of a lifecycle state transition."""
    success: bool = False
    from_state: Optional[str] = None
    to_state: Optional[str] = None
    skill_path: Optional[str] = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks_passed: list[str] = field(default_factory=list)
    checks_failed: list[str] = field(default_factory=list)


def get_skill_lifecycle(skill_path: Path) -> Optional[str]:
    """Get the current lifecycle state from a skill's frontmatter."""
    try:
        with open(skill_path) as f:
            content = f.read()
        
        # Extract frontmatter
        if not content.startswith("---"):
            return None
        
        # Find the frontmatter block
        end_frontmatter = content.find("---", 3)
        if end_frontmatter == -1:
            return None
        
        frontmatter_str = content[3:end_frontmatter].strip()
        frontmatter = yaml.safe_load(frontmatter_str) or {}
        
        return frontmatter.get("Lifecycle")
    except Exception:
        return None


def set_skill_lifecycle(
    skill_path: Path,
    new_state: str,
    reason: Optional[str] = None,
    approver: Optional[str] = None,
) -> bool:
    """Update the lifecycle state in a skill's frontmatter."""
    try:
        with open(skill_path) as f:
            content = f.read()
        
        # Extract frontmatter
        if not content.startswith("---"):
            return False
        
        end_frontmatter = content.find("---", 3)
        if end_frontmatter == -1:
            return False
        
        frontmatter_str = content[3:end_frontmatter].strip()
        frontmatter = yaml.safe_load(frontmatter_str) or {}
        
        # Update lifecycle
        frontmatter["Lifecycle"] = new_state
        
        # Update timestamps
        frontmatter["Updated"] = datetime.now().strftime("%Y-%m-%d")
        
        # Add promotion/deprecation timestamps
        if new_state == "Promoted":
            frontmatter["Promoted"] = datetime.now().strftime("%Y-%m-%d")
            if approver:
                frontmatter["PromotedBy"] = approver
        elif new_state == "Deprecated":
            frontmatter["Deprecated"] = datetime.now().strftime("%Y-%m-%d")
            if reason:
                frontmatter["DeprecatedReason"] = reason
        
        # Write back
        new_frontmatter_str = yaml.dump(frontmatter, sort_keys=False, default_flow_style=False)
        new_content = f"---\n{new_frontmatter_str}---\n{content[end_frontmatter + 3:]}"
        
        with open(skill_path, "w") as f:
            f.write(new_content)
        
        return True
    except Exception:
        return False


def validate_transition(
    from_state: Optional[str],
    to_state: str,
) -> tuple[bool, list[str]]:
    """Validate if a state transition is allowed."""
    errors = []
    
    if from_state is None:
        errors.append("Cannot determine current lifecycle state")
        return False, errors
    
    try:
        from_enum = LifecycleState(from_state)
        to_enum = LifecycleState(to_state)
    except ValueError:
        errors.append(f"Invalid lifecycle state: {from_state} or {to_state}")
        return False, errors
    
    valid_transitions = VALID_TRANSITIONS.get(from_enum, [])
    if to_enum not in valid_transitions:
        errors.append(
            f"Invalid transition: {from_state} → {to_state}. "
            f"Valid transitions from {from_state}: {', '.join(t.value for t in valid_transitions)}"
        )
        return False, errors
    
    return True, errors


def run_pre_promotion_checks(
    skill_path: Path,
    config: LifecycleConfig,
) -> tuple[bool, list[str], list[str]]:
    """Run quality gate checks before promoting a skill."""
    passed = []
    failed = []
    
    # Check 1: Skill file exists
    if not skill_path.exists():
        failed.append("Skill file does not exist")
        return False, passed, failed
    
    # Check 2: Required sections present
    try:
        from vitools_sync.skill.validate import validate_skill, ValidationConfig
        
        if config.run_validation:
            validation_config = ValidationConfig(
                strict=config.strict_validation,
                check_legal=config.run_legal_check,
            )
            result = validate_skill(skill_path, validation_config)
            
            if result.passed:
                passed.append("structure_validation")
                passed.append("sections_validation")
                passed.append("content_validation")
            else:
                failed.extend([f"validation_{e}" for e in result.errors])
                if config.strict_validation:
                    failed.extend([f"warning_{w}" for w in result.warnings])
    except Exception as e:
        failed.append(f"validation_error: {str(e)}")
    
    # Check 3: Legal compliance
    if config.run_legal_check:
        try:
            from vitools_sync.legal.overlap import check_skill_overlap
            from vitools_sync.paths import repo_root
            
            repo = repo_root()
            result = check_skill_overlap(repo, skill_path)
            
            if result.passed:
                passed.append("legal_compliance")
            else:
                failed.extend([f"legal_{issue}" for issue in result.issues])
        except Exception as e:
            failed.append(f"legal_error: {str(e)}")
    
    # Check 4: Required frontmatter fields
    try:
        with open(skill_path) as f:
            content = f.read()
        
        # Extract frontmatter
        if content.startswith("---"):
            end_frontmatter = content.find("---", 3)
            if end_frontmatter != -1:
                frontmatter_str = content[3:end_frontmatter].strip()
                frontmatter = yaml.safe_load(frontmatter_str) or {}
                
                required_fields = ["name", "description", "Domain"]
                for field in required_fields:
                    if field in frontmatter:
                        passed.append(f"frontmatter_{field}")
                    else:
                        failed.append(f"frontmatter_missing_{field}")
    except Exception:
        failed.append("frontmatter_parsing_error")
    
    # Check 5: Examples section has Good and Bad
    try:
        with open(skill_path) as f:
            content = f.read()
        
        has_good = "### Good" in content or "#### Good" in content
        has_bad = "### Bad" in content or "#### Bad" in content
        
        if has_good and has_bad:
            passed.append("examples_structure")
        else:
            if not has_good:
                failed.append("examples_missing_good")
            if not has_bad:
                failed.append("examples_missing_bad")
    except Exception:
        failed.append("examples_check_error")
    
    # Check 6: Guardrails section exists
    try:
        with open(skill_path) as f:
            content = f.read()
        
        if "## Guardrails" in content or "# Guardrails" in content:
            passed.append("guardrails_present")
        else:
            failed.append("guardrails_missing")
    except Exception:
        failed.append("guardrails_check_error")
    
    # Check 7: Verification section exists
    try:
        with open(skill_path) as f:
            content = f.read()
        
        if "## Verification" in content or "# Verification" in content:
            passed.append("verification_present")
        else:
            failed.append("verification_missing")
    except Exception:
        failed.append("verification_check_error")
    
    return len(failed) == 0, passed, failed


def promote_skill(
    skill_path: Path,
    to_state: str,
    config: Optional[LifecycleConfig] = None,
) -> TransitionResult:
    """Promote a skill to a new lifecycle state."""
    if config is None:
        config = LifecycleConfig(to_state=LifecycleState(to_state))
    
    result = TransitionResult(
        skill_path=str(skill_path),
        to_state=to_state,
    )
    
    # Get current state
    current_state = get_skill_lifecycle(skill_path)
    result.from_state = current_state
    
    # Validate transition
    is_valid, errors = validate_transition(current_state, to_state)
    if not is_valid and not config.force:
        result.errors.extend(errors)
        result.success = False
        return result
    
    # Run pre-promotion checks for certain transitions
    if to_state in ["Review", "Promoted"]:
        checks_passed, passed, failed = run_pre_promotion_checks(
            skill_path, config
        )
        result.checks_passed = passed
        result.checks_failed = failed
        
        if not checks_passed and not config.force:
            result.errors.append(
                f"Quality gate checks failed ({len(failed)} failures). "
                "Use --force to bypass."
            )
            result.errors.extend(failed)
            result.success = False
            return result
    
    # Special requirements for Promoted state
    if to_state == "Promoted" and not config.force:
        if not config.approver:
            result.errors.append("Approver name is required for promotion to Promoted state")
            result.success = False
            return result
    
    # Special requirements for Deprecated state
    if to_state == "Deprecated" and not config.force:
        if not config.reason:
            result.errors.append("Deprecation reason is required for Deprecated state")
            result.success = False
            return result
    
    # Update the lifecycle state
    success = set_skill_lifecycle(
        skill_path,
        to_state,
        reason=config.reason if to_state == "Deprecated" else None,
        approver=config.approver if to_state == "Promoted" else None,
    )
    
    if not success:
        result.errors.append("Failed to update skill lifecycle state")
        result.success = False
        return result
    
    result.success = True
    return result


def list_skills_by_lifecycle(
    skills_dir: Path,
    lifecycle: Optional[str] = None,
) -> dict[str, list[str]]:
    """List skills grouped by lifecycle state."""
    skills_by_lifecycle = {}
    
    if not skills_dir.exists():
        return skills_by_lifecycle
    
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        
        lifecycle_state = get_skill_lifecycle(skill_file)
        if lifecycle_state is None:
            lifecycle_state = "Unknown"
        
        if lifecycle_state not in skills_by_lifecycle:
            skills_by_lifecycle[lifecycle_state] = []
        
        skills_by_lifecycle[lifecycle_state].append(skill_dir.name)
    
    # Filter by specific lifecycle if requested
    if lifecycle:
        return {lifecycle: skills_by_lifecycle.get(lifecycle, [])}
    
    return skills_by_lifecycle


def get_lifecycle_history(skill_path: Path) -> dict:
    """Get lifecycle history from a skill's frontmatter."""
    history = {}
    
    try:
        with open(skill_path) as f:
            content = f.read()
        
        # Extract frontmatter
        if not content.startswith("---"):
            return history
        
        end_frontmatter = content.find("---", 3)
        if end_frontmatter == -1:
            return history
        
        frontmatter_str = content[3:end_frontmatter].strip()
        frontmatter = yaml.safe_load(frontmatter_str) or {}
        
        # Extract lifecycle-related fields
        history["current"] = frontmatter.get("Lifecycle")
        history["created"] = frontmatter.get("Created")
        history["updated"] = frontmatter.get("Updated")
        history["promoted"] = frontmatter.get("Promoted")
        history["promoted_by"] = frontmatter.get("PromotedBy")
        history["deprecated"] = frontmatter.get("Deprecated")
        history["deprecated_reason"] = frontmatter.get("DeprecatedReason")
        
    except Exception:
        pass
    
    return history
