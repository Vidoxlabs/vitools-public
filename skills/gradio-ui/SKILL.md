---
name: gradio-ui
description: >-
  Build Gradio web UIs for ML model demos. Interfaces, blocks, event handlers, and deployment to Spaces. Use when creating interactive model demonstrations or prototypes.
license: MIT
version: 1.0.0
metadata:
  kind: skill
  status: promoted
  origin: derived
  publisher: vidoxlabs
  category: web
  tags: [gradio, ml-demos, web-ui, huggingface-spaces, prototyping]
  platforms: [claude-code, cursor, copilot, opencode, generic]
  site:
    slug: gradio-ui
    summary: Build Gradio web UIs for ML model demos
  derived_from:
    - name: huggingface-gradio
      license: Apache-2.0
      url: https://github.com/anthropics/skills
      note: Concept only. Body rewritten.
  review:
    last: 2026-09-12
    next: 2027-01-12
---

# Gradio UI

## When to use

Activate when building an interactive web interface for an ML model or data pipeline. Use for demos, prototypes, and internal tools.

## Procedure

1. Install Gradio: pip install gradio.
2. Choose API: gradio.Interface for simple demos, gradio.Blocks for complex layouts.
3. Define the prediction function: takes inputs, runs model, returns outputs.
4. Build UI components and wire with click() event handlers.
5. Add examples with gr.Examples for common inputs.
6. Launch locally: demo.launch().
7. Deploy to Hugging Face Spaces: push app file and requirements.txt.

## Guardrails

- Do not load the model at request time. Load once at startup.
- Do not block the event loop. Use async for streaming.
- Do not hardcode file paths. Use relative paths or env vars.
- Do not expose sensitive endpoints. Demos are public on Spaces.

## Examples

### Good

> Blocks interface with image input, confidence slider, results gallery. Model loaded at startup. Three examples. Deployed to Space, loads in 5 seconds.

### Bad

> Interface loads model on every request (30-second cold start). File path hardcodes local dir. No examples. Public Space with no rate limiting.

## Verification

- App launches locally without errors.
- Prediction function returns correct output for test inputs.
- Model loads once at startup.
- Deployed Space loads and responds.

## Install

```bash
npx skills add vidoxlabs/vitools-public/skills/gradio-ui
```

```text
# Claude Code
/plugin marketplace add Vidoxlabs/vitools-public
# then enable: gradio-ui
```

```bash
# Cursor
curl -fsSL https://vidoxlabs.dev/vitools/skills/gradio-ui/raw -o .cursor/skills/gradio-ui/SKILL.md
```

```text
# Agent prompt
Fetch https://vidoxlabs.dev/vitools/skills/gradio-ui.md and install it as a project skill at skills/gradio-ui/SKILL.md. Follow its Procedure. Do not modify Guardrails.
```