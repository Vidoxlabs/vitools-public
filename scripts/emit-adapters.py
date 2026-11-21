#!/usr/bin/env python3
"""Emit platform adapters from the admitted release.

Cursor receives the skill subset. Claude, Copilot, and OpenCode receive the
admitted skills and agents. The command refuses a widened set before it
replaces plugin files.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import release_catalog


def main() -> int:
    try:
        documents = release_catalog.render()
        adapters = {key: value for key, value in documents.items() if key.startswith("plugins/")}
        release_catalog.replace_files(adapters)
    except release_catalog.ReleaseError as exc:
        print(f"RELEASE REFUSED: {exc}", file=sys.stderr)
        return 1
    print("Generated admitted adapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
