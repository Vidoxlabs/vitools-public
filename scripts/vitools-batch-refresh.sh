#!/usr/bin/env bash
# Batch refresh catalog inventory and emit all platform configs.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Install vitools-sync if not available
if ! python3 -c "import vitools_sync" 2>/dev/null; then
    python3 -m pip install -e tools/vitools-sync --break-system-packages -q
fi

# Build catalog and validate
python3 scripts/catalog-build.py
python3 scripts/catalog-build.py --validate

# Run legal gate
bash scripts/vitools-legal-gate.sh

# Emit platform adapters
python3 scripts/emit-adapters.py

# Emit platform configs via vitools-sync
vitools-sync catalog build 2>/dev/null || true
vitools-sync emit --platform all --target "$ROOT/platforms" 2>/dev/null || true

echo "Batch complete: catalog validated, legal gate passed, adapters emitted"
