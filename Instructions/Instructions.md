**Instructions = execution standards.** This page governs how Vidoxlabs agents and documentation should behave: procedures, tool-use conventions, policies/guardrails, and reusable patterns.

**Reference intake is now unified.** Add new Instruction sources in **ViTools References** (Category = Instructions). Legacy Instructions reference DBs are in Archive (Legacy).

</aside>

## What this contains

- **Canonical internal artifacts:** Internal Artifacts → By Type (filter Type = Instruction)
- **Canonical reference intake:** References → Instruction Sources
- A governed internal **Instructions** database (canonical, agent-consumable execution standards).
- A curated database of **instruction-related sources/refs** (one row per reference) used as evidence/provenance.
- Metadata for fast filtering and review:
    - **Domain** (Skills / Prompts / Tools / Plugins / MCP Tools / Agents / ViDocs)
    - **Instruction Type** (Procedure / Tool Capability / Policy/Guardrail / Template/Pattern)
    - **Lifecycle** (Intake → Promoted → Superseded)
    - **Owner** + **Review cadence** (Last Review / Next Review)

## How to use it (operating loop)

1. **Capture**: add an Instruction row (or a reference row) and set **Lifecycle = Intake** (or **Status = Inbox** in References).
2. **Draft**: write the procedure/guardrails/examples/verification. Link evidence as needed.
3. **Promote**: move to **Promoted** only when Guardrails + Examples + Verification are complete (especially for production-impacting behavior).
4. **Maintain**: set **Next Review**; update **Last Review** whenever materially reviewed/changed.

## Conventions

- Store **subpaths** as their own reference rows when the unit of adoption is a specific section/package/path.
- Notes should capture **contract + constraints**: dependencies, auth model, rate limits, failure behavior, and verification approach.

## Internal Instructions — usage conventions

### Lifecycle meaning

- **Intake**: draft / exploratory / not safe to rely on.
- **Promoted**: ready for internal agents; must have **Guardrails + Examples + Verification** complete.
- **Superseded**: historical; link the replacement instruction in the page body.

### Linking rules

- Link an instruction to at least one Vive agent (VI/VA/LA/OAI) when it’s agent-specific.
- Otherwise leave agent relations empty and rely on **Domain** + **Instruction Type** for discovery.

### Evidence policy (optional but encouraged)

- Prefer linking curated sources via **Evidence** (relation to Instructions References).
- Use **Source URL** for ad-hoc provenance when no reference row exists.

### Review cadence

- Set **Next Review** when promoting a skill.
- Update **Last Review** whenever the skill is reviewed or materially changed.

---

Instructions Database