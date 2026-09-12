# Skill Mining From Repos

Domain: Skills
Lifecycle: Intake
Owner: Vioxniv
Skill Type: Procedure

<aside>
🧩

This is an **Intake** skill. Complete Examples + Verification before promoting.

</aside>

## Summary

- Procedure for mining external skill repositories into Vidoxlabs-native skills.

## When to Use (Triggers)

- Adding a new repo/path to Skills References
- Converting a reference into an internal Skill

## Inputs

- Skills Reference row (repo/path URL)
- Target agent(s) that will consume the skill (optional)

## Outputs

- A new internal Skill page with standardized structure and optional Evidence links

## Procedure / Steps

1. Capture the external reference (repo/path) in **Skills References** with Status = Inbox/Reviewing.
2. Review the reference and extract: intent, triggers, steps, guardrails, examples, verification.
3. Create an internal Skill using the canonical template.
4. Link the reference row via **Evidence** (optional but preferred).
5. Keep the internal skill scoped and agent-agnostic unless explicitly agent-specific.

## Guardrails

- Do not import vendor-specific assumptions without noting constraints.
- Avoid copying large blobs; extract the reusable pattern.

## Examples

### Good

- “Extracted a 10-step workflow + guardrails; linked sources; added verification.”

### Bad

- “Copied README content wholesale with no internal framing.”

## Verification

- Confirm the internal skill can be followed as-written without needing the original repo open.

## Sources / Evidence (Optional)

- Link the Skills References row and any key docs.