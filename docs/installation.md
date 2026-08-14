# Installation

This repository is currently a private development project. Platform installation may require authenticated access to the repository.

## Codex App and CLI

Codex is the current validated environment. The repository root contains the marketplace definition in `.agents/plugins/marketplace.json`.

The repository is currently private, so authenticate Git for the GitHub account that has access. Register the GitHub repository as a marketplace and install the plugin:

```powershell
codex plugin marketplace add ZION-XU/prd-refiner --ref main
codex plugin add prd-refiner@prd-refiner-dev
```

For local development, clone the repository and register the checkout instead. Choose either the GitHub marketplace or the local checkout; do not register both under the same marketplace name.

```powershell
git clone https://github.com/ZION-XU/prd-refiner.git
cd prd-refiner
codex plugin marketplace add .
codex plugin add prd-refiner@prd-refiner-dev
```

After installation, start a new task and explicitly invoke:

```text
$prd-refiner
```

Switch to Plan mode before the structured clarification phase. Reinstall after a manifest cachebuster update, and use a new task so the updated Skill is loaded.

To update an installation backed by the GitHub marketplace:

```powershell
codex plugin marketplace upgrade prd-refiner-dev
codex plugin add prd-refiner@prd-refiner-dev
```

To update a local development checkout:

```powershell
git pull
codex plugin add prd-refiner@prd-refiner-dev
```

The marketplace only needs to be registered once for the same checkout. Start a new Codex task after every install or update so the refreshed Skill is loaded.

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
