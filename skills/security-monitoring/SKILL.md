---
name: security-monitoring
description: >-
  Set up and manage security monitoring: detection rules, alert tuning, case management, and incident response workflows. Use when configuring SIEM rules, managing alerts, or responding to security incidents.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: security
  tags: [security, monitoring, siem, detection-rules, incident-response]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: security-monitoring
    summary: Security detection rules and incident response
  derived_from:
    - name: elastic-security-detection-case-management
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Security Monitoring

## When to use

Activate when setting up security monitoring, configuring detection rules, managing security alerts, or responding to incidents.

## Procedure

1. Define detection rules for known threat patterns: brute force, privilege escalation, data exfiltration, anomalous access.
2. Configure alert actions: notify (Slack/email), create a case, or auto-block based on severity.
3. Tune rules to reduce false positives: set thresholds, add allow-lists for known benign patterns.
4. Set up case management workflow: triage, investigate, assign, resolve.
5. Define incident response playbooks: containment, eradication, recovery, post-mortem.
6. Test rules with simulated attacks to verify detection.
7. Review and update rules monthly based on threat intelligence.

## Guardrails

- Do not enable auto-block rules without testing for false positives first.
- Do not alert on every event. Tune to actionable signals.
- Do not skip post-mortem after an incident. Document root cause and prevention.
- Do not leave detection rules stale. Threat patterns evolve.

## Examples

### Good

> Configured 15 detection rules across 4 severity levels, tested with simulated brute-force and exfiltration attacks, tuned 3 rules for false positives, set up Slack alerts and case management workflow.

### Bad

> Enabled every available detection rule with default settings. Inbox flooded with 500 alerts per day, all false positives. Team ignores alerts.

## Verification

- Detection rules are tested with simulated attacks.
- False positive rate is below 10% of total alerts.
- Case management workflow is defined and documented.
- Incident response playbooks exist for each severity level.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/security-monitoring
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: security-monitoring
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/security-monitoring/raw -o .cursor/skills/security-monitoring/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/security-monitoring.md and install it as a project skill at skills/security-monitoring/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```