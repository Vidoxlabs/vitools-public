# vitools-sync

CLI for emitting Vidoxlabs canonical `.agents/` content to agent platforms.

## Install

```bash
cd tools/vitools-sync
pip install -e .
```

## Usage

```bash
# Emit Cursor configs to platforms/cursor/
vitools-sync emit --platform cursor --target ../../platforms/cursor

# Emit all platforms
vitools-sync emit --platform all --target ../../platforms

# Install to user paths (dry-run by default)
vitools-sync install --platform cursor --user --dry-run

# Catalog inventory from archive MANIFEST + plugins index
vitools-sync catalog build

# Legal overlap check on a skill
vitools-sync legal check .agents/skills/skill-mining/SKILL.md
```

Reads only from `.agents/` and `.agents/mcp/servers.yaml`. Never emits `archive/vendor/`.
