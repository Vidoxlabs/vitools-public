#!/usr/bin/env bash
# Batch refresh catalog inventory and emit all platform configs.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
pip install -e tools/vitools-sync -q
vitools-sync catalog build
vitools-sync emit --platform all --target "$ROOT/platforms"
echo "Batch complete: inventory + platform emits refreshed"
