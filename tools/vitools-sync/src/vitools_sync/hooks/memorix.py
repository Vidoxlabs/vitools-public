"""Optional Memorix collection hooks for vitools-sync pipeline events."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _collection_enabled() -> bool:
    return os.environ.get("MEMORIX_VITOOLS_COLLECTION", "0").lower() in ("1", "true", "yes")


def _state_root() -> Path:
    return Path(os.environ.get("MEMORIX_STATE_ROOT", Path.home() / ".memorix")).expanduser()


def _collection_path() -> Path:
    path = _state_root() / "vitools" / "collection.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _append_event(event_type: str, payload: dict[str, Any]) -> None:
    if not _collection_enabled():
        return
    vitools_root = os.environ.get("VITOOLS_ROOT", str(Path.cwd()))
    event = {
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "vitools_root": vitools_root,
        "payload": payload,
        "source": "vitools-sync",
    }
    with _collection_path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")


def log_emit(platform: str, file_count: int, target: str) -> None:
    _append_event("emit_run", {"platform": platform, "file_count": file_count, "target": target})


def log_catalog(entry_count: int, inventory_path: str) -> None:
    _append_event("catalog_built", {"entry_count": entry_count, "inventory_path": inventory_path})


def log_legal_check(skill_path: str, passed: bool, issues: list[str]) -> None:
    _append_event(
        "legal_gate_pass" if passed else "legal_gate_fail",
        {"skill_path": skill_path, "issues": issues},
    )


def log_skill_created(skill_path: str, skill_id: str, lifecycle: str = "Intake") -> None:
    """Log when a new skill is created."""
    _append_event(
        "skill_created",
        {"skill_path": skill_path, "skill_id": skill_id, "lifecycle": lifecycle},
    )


def log_skill_promoted(
    skill_path: str,
    skill_id: str,
    from_state: str,
    to_state: str,
    approver: str | None = None,
) -> None:
    """Log when a skill is promoted to a new lifecycle state."""
    payload = {
        "skill_path": skill_path,
        "skill_id": skill_id,
        "from_state": from_state,
        "to_state": to_state,
    }
    if approver:
        payload["approver"] = approver
    
    _append_event("skill_promoted", payload)


def log_skill_deprecated(skill_path: str, skill_id: str, reason: str) -> None:
    """Log when a skill is deprecated."""
    _append_event(
        "skill_deprecated",
        {"skill_path": skill_path, "skill_id": skill_id, "reason": reason},
    )


def log_concept_card_created(concept_path: str, concept_id: str) -> None:
    """Log when a concept card is created."""
    _append_event(
        "concept_card_created",
        {"concept_path": concept_path, "concept_id": concept_id},
    )


def try_bridge_to_vitools_canonical(event_type: str, payload: dict[str, Any]) -> None:
    """When vilabs tools are on PYTHONPATH, delegate to vitools_canonical.collection."""
    if not _collection_enabled():
        return
    mcp_root = os.environ.get("VILABS_MCP_ROOT")
    if not mcp_root:
        return
    tools = Path(mcp_root) / "vitools" / "tools"
    if not tools.is_dir():
        return
    if str(tools) not in sys.path:
        sys.path.insert(0, str(tools))
    try:
        from vitools_canonical.collection import append_event

        append_event(event_type, payload, vitools_root=os.environ.get("VITOOLS_ROOT"))
    except ImportError:
        _append_event(event_type, payload)
