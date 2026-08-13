# Installation

This repository is currently a private development project. Platform installation may require authenticated access to the repository.

## Codex App and CLI

Codex is the current validated environment. During local development, expose the plugin through a local marketplace whose entry points to this repository root, then install `prd-refiner` from that marketplace.

After installation, start a new task and explicitly invoke:

```text
$prd-refiner
```

Switch to Plan mode before the structured clarification phase. Reinstall after a manifest cachebuster update, and use a new task so the updated Skill is loaded.

## Claude Code

The repository contains `.claude-plugin/plugin.json` and a development marketplace file. Live installation and slash-command behavior have not yet been verified.

## Cursor

The repository contains `.cursor-plugin/plugin.json` that points to the shared `skills/` directory. Live marketplace installation has not yet been verified.

## Kimi Code

The repository contains `.kimi-plugin/plugin.json` with Skill registration and structured-question tool guidance. Live installation has not yet been verified.

## OpenCode

The root `package.json` points to `.opencode/plugins/prd-refiner.js`. The plugin registers the shared Skill path without automatic chat injection.

After the repository is accessible from the target environment, install it using OpenCode's supported Git/package plugin mechanism and explicitly load or invoke `prd-refiner`.

## Pi

The root `package.json` declares the Pi extension and shared Skill path. The extension registers `skills/` through resource discovery and does not auto-inject the workflow.

## Gemini CLI, Hermes Agent, and Devin

Initial manifests and registration adapters are present. Complete a real client installation test before publishing platform-specific commands as supported instructions.

## Security

Do not store private PRDs, Figma tokens, API keys or generated customer outputs in this repository. Host applications should own authentication and secret storage.
