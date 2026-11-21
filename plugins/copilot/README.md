# ViTools for GitHub Copilot

Install ViTools skills by fetching the raw SKILL.md from vidoxlabs.dev.

## Available skills

- **data-loss-prevention**: Halt and confirm before destructive commands
  `curl -fsSL https://vidoxlabs.dev/vitools/skills/data-loss-prevention/raw`
- **evidence-answering**: Require evidence for claims about Vidoxlabs systems.
  `curl -fsSL https://vidoxlabs.dev/vitools/skills/evidence-answering/raw`
- **skill-mining**: Mine external repos into Vidoxlabs-native skills
  `curl -fsSL https://vidoxlabs.dev/vitools/skills/skill-mining/raw`
- **skills-template**: Canonical formatting standard for Vidoxlabs skills
  `curl -fsSL https://vidoxlabs.dev/vitools/skills/skills-template/raw`
- **v37-validation**: Validate changes against operational expectations
  `curl -fsSL https://vidoxlabs.dev/vitools/skills/v37-validation/raw`

## Available agents

- **legal-gate**: Reviews license and origin of skill and agent files. Checks for vendor branding, missing licenses, and vendor archive co
- **rewrite-orchestrator**: Coordinates catalog, concept extraction, rewrite, legal, and verification sub-agents for the ViTools rewrite pipeline.
- **skill-author**: Writes a first-party SKILL.md from a concept card or external reference. Produces original Vidoxlabs prose with required
- **vitools-catalog-maintainer**: Builds, validates, and maintains the ViTools public catalog. Runs the catalog builder, legal gate, and inventory checks.
