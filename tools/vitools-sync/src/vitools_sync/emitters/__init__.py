from __future__ import annotations

from pathlib import Path

from vitools_sync.emitters import antigravity, cursor, devin, grok, mistral, opencode

EMITTERS = {
    "cursor": cursor.emit_cursor,
    "devin": devin.emit_devin,
    "opencode": opencode.emit_opencode,
    "grok": grok.emit_grok,
    "mistral": mistral.emit_mistral,
    "antigravity": antigravity.emit_antigravity,
}


def emit_platform(root: Path, platform: str, target: Path) -> list[Path]:
    emitter = EMITTERS.get(platform)
    if emitter is None:
        raise ValueError(f"Unknown platform: {platform}")
    return emitter(root, target)


def emit_all(root: Path, platforms_root: Path) -> dict[str, list[Path]]:
    results: dict[str, list[Path]] = {}
    for name in EMITTERS:
        target = platforms_root / name
        results[name] = emit_platform(root, name, target)
    return results
