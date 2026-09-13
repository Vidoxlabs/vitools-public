# Instructions — Execution Standards

Governed execution standards for agents and documentation in the ViTools
ecosystem.

## Lifecycle

Every instruction follows this lifecycle:

1. **Intake** — draft or exploratory, not safe to rely on
2. **Promoted** — ready for agents; must have Guardrails, Examples, and
   Verification complete
3. **Superseded** — historical; link the replacement

## What belongs here

- Procedures for agent workflows
- Tool-use conventions
- Policies and guardrails
- Reusable patterns and templates

## Requirements for promotion

An instruction reaches Promoted only when it has:

- **Guardrails** — what not to do, safety boundaries
- **Examples** — good and bad cases
- **Verification** — how to confirm the instruction was followed

## Linking

- Link an instruction to a skill or agent when it is specific to that unit
- Otherwise rely on category and tags for discovery

## Review cadence

- Set Next Review when promoting
- Update Last Review whenever materially reviewed or changed