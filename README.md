# ViTools

**Skills, plugins, and tooling repository for the Vidoxlabs AI ecosystem.**

This repository houses the canonical knowledge base, reusable components, and tooling configurations
that power Vidoxlabs' sovereign AI infrastructure.

---

## Repository Structure

| Directory       | Purpose                                                                                           |
| --------------- | ------------------------------------------------------------------------------------------------- |
| `skills/`       | **Skill definitions** — reusable AI capabilities, procedures, and knowledge bases (1,500+ skills) |
| `plugins/`      | **Plugin configurations** — IDE/editor plugin manifests and metadata (170+ plugins)               |
| `Instructions/` | **Execution standards** — procedures, tool conventions, policies, and guardrails                  |
| `cookbooks/`    | **External references** — high-signal repositories and guides mined into Vidoxlabs-native assets  |
| `mcp_tooling/`  | **MCP configurations** — Model Context Protocol tooling and integrations                          |

---

## Quick Reference

### Skills (`skills/`)

Each skill is a self-contained capability with:

- `SKILL.md` — capability definition, usage patterns, examples
- `references/` — linked sources and evidence
- `templates/` — reusable scaffolds (where applicable)

**Conventions:**

- Store subpaths as their own reference rows when the unit of adoption is specific
- Capture **contract + constraints**: dependencies, auth model, rate limits, failure behavior
- Set **Review cadence** with Last Review / Next Review dates

### Plugins (`plugins/`)

IDE/editor plugins following the Windsurf skill plugin format:

- `plugin.json` — plugin manifest
- `skills/` — bundled skill definitions
- `installed_version.json` — version tracking

### Instructions (`Instructions/`)

Governed execution standards for agents and documentation:

- Lifecycle: **Intake → Promoted → Superseded**
- Must have **Guardrails + Examples + Verification** to reach Promoted
- Link to Vive agents (VI/VA/LA/OAI) when agent-specific

### Cookbooks (`cookbooks/`)

External reference intake:

- Status flow: **Inbox → Reviewing → Mined → Integrated → Archived**
- Notes should be actionable: "extract X template", "good eval harness"
- Prefer canonical links (repo root) unless subpath is the meaningful unit

---

## Contributing

1. **Capture** — Add new items with appropriate status (Intake/Inbox)
2. **Draft** — Document procedures, constraints, verification approach
3. **Promote** — Move to Promoted/Integrated when complete and tested
4. **Maintain** — Update review dates; link evidence and sources

---

## License

MIT License — see [LICENSE](./LICENSE)

---

## Related Repositories

- [V37_Cluster](https://github.com/Vidoxlabs/v37_cluster) — Core infrastructure
- [ViLabs](https://github.com/Vidoxlabs/vilabs) — AI platform services
- [ViDocs](https://github.com/Vidoxlabs/vidocs) — Documentation system

---

<p align="center"><sub>Vidoxlabs — Sovereign AI Infrastructure</sub></p>
