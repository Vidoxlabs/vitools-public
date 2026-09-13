# Contributing to ViTools

## Add a skill

1. Create `skills/<slug>/SKILL.md` using the canonical format. See
   `skills/skills-template/SKILL.md` for the template.
2. Set frontmatter:
   - `name`: kebab-case, matches the directory slug
   - `description`: what it does and when to use it (with trigger phrases)
   - `license: MIT`
   - `metadata.kind: skill`
   - `metadata.status: promoted`
   - `metadata.origin: vidoxlabs` (or `derived` if based on an external concept)
   - `metadata.category`: one of the controlled vocabulary categories
3. Include all required body sections: When to use, Procedure,
   Guardrails, Examples (good and bad), Verification, Install.
4. Run the catalog builder: `python scripts/catalog-build.py`
5. Run the legal gate: `bash scripts/vitools-legal-gate.sh`
6. If both pass, commit with message `vitools-public: add <slug> skill`.

## Add an agent

Same process but at `agents/<slug>/AGENT.md` with `metadata.kind: agent`.
Body sections: When to use, Role, Operating loop, Guardrails,
Verification, Install.

## Legal rules

- Never copy vendor body text into a first-party skill. Use concept
  cards and official documentation only.
- Never put `claude` or `anthropic` in a skill `name`.
- Every public skill must have `license: MIT` in frontmatter.
- No vendor body text is included in this repository. Derived skills reference
  their source in the `derived_from` frontmatter field.

## Verification commands

```bash
python scripts/catalog-build.py              # build catalog
python scripts/catalog-build.py --validate   # validate against schema
python scripts/catalog-build.py --check-inventory  # verify completeness
bash scripts/vitools-legal-gate.sh           # license + origin checks
python scripts/emit-adapters.py             # regenerate plugin adapters
```

## Commit discipline

- One concern per commit.
- Message format: `vitools-public: <action> <slug> <noun>`
- Do not force-push to main.
- Do not commit `__pycache__/`, secrets, or generated minified copies.
