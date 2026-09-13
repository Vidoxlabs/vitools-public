#!/usr/bin/env bash
# Convenience script for creating a new skill
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

# Install vitools-sync if not available
if ! python3 -c "import vitools_sync" 2>/dev/null; then
    python3 -m pip install -e tools/vitools-sync --break-system-packages -q
fi

python3 -m vitools_sync.cli skill create "$@"
