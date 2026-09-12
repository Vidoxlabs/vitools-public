**Skills = execution patterns.** This page tracks external skill repositories and skill frameworks we mine into Vidoxlabs-native execution guides (skills), tool conventions, and reusable scaffolds.

**Reference intake is now unified.** Add new Skill sources in **ViTools References** (Category = Skills). Legacy Skills reference DBs are in Archive (Legacy).

</aside>

## What this contains

- **Canonical internal artifacts:** Internal Artifacts → By Type (filter Type = Skill)
- **Canonical reference intake:** References → Skill Sources
- A curated database of **skills-related repos/paths** (one row per reference).
- A governed internal **Skills** database for Vidoxlabs-native skills (agent-consumable execution patterns).
- Metadata for fast filtering and review:
    - **Vendor** (who maintains it)
    - **Artifact Type** (skills repo, starter pack, subpath, templates, examples)
    - **Topic / Tags** (skills, agents, copilot, studio, tooling, extensions)
    - **Status** (Inbox → Reviewing → Mined → Integrated → Archived)
    - **Review date** (when to revisit)

## How to use it (operating loop)

1. **Capture**: add a repo/path link, set **Status = Inbox**.
2. **Review**: open the row and capture the skill format, assumptions, and interface conventions.
3. **Mine**: extract reusable patterns (tool schemas, prompt/instruction conventions, testing/evals).
4. **Integrate**: once implemented internally, set **Integrated** and link the internal artifact/work.

## Conventions

- Store **subpaths** as their own rows when the skill set lives under `/skills` (treat it as the unit of adoption).
- Notes should capture **portability**: dependencies, runtime constraints, auth model, and how to validate correctness.

## Internal Skills — usage conventions

### Lifecycle meaning

- **Intake**: draft / exploratory / not safe to rely on.
- **Promoted**: ready for internal agents; must have **Guardrails + Examples + Verification** complete.
- **Superseded**: historical; link the replacement skill in the page body.

### Linking rules

- Link a skill to at least one Vive agent (VI/VA/LA/OAI) when it’s agent-specific.
- Otherwise leave agent relations empty and rely on **Domain** + **Skill Type** for discovery.

### Evidence policy (optional but encouraged)

- Prefer linking curated sources via **Evidence** (relation to Skills References).
- Use **Source URL** for ad-hoc provenance when no reference row exists.

### Review cadence

- Set **Next Review** when promoting a skill.
- Update **Last Review** whenever the skill is reviewed or materially changed.

---

Skills Database