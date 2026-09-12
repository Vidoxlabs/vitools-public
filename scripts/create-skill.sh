#!/usr/bin/env bash
# Convenience script for creating a new skill

set -euo pipefail

# Find the vitools repository root
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Check if vitools-sync is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

# Run the skill create command
python3 -m vitools_sync.cli skill create "$@"
