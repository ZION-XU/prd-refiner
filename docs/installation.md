# Installation

This repository is currently a private development project. Platform installation may require authenticated access to the repository.

## Codex App and CLI

Codex is the current validated environment. This plugin is not published in a public marketplace and is installed from a local source checkout. The repository root contains the installer descriptor in `.agents/plugins/marketplace.json`.

The repository is currently private, so authenticate Git for the GitHub account that has access. Clone the source, register the local checkout with the Codex plugin installer, and install the plugin:

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

To update the source installation:

```powershell
git pull
codex plugin add prd-refiner@prd-refiner-dev
```

The local marketplace registration is only Codex's mechanism for installing a plugin from the checkout; it does not mean the plugin is published in a public marketplace. The checkout only needs to be registered once. Start a new Codex task after every install or update so the refreshed Skill is loaded.

### Company Confluence MCP

The Codex manifest references the root `.mcp.json`, so installing the plugin also registers the `prd-refiner-confluence` stdio server. Credential collection is intentionally a separate, explicit step because plugin installation must not execute arbitrary scripts or capture secrets automatically.

Prerequisites:

- Windows PowerShell;
- `uv` on `PATH`;
- access to `https://confluence.zwcad.com`;
- a personal Confluence username and PAT.

Run once from the plugin root:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File .\integrations\confluence-mcp\configure.ps1
```

The script prompts without echoing the PAT, stores it with Windows current-user DPAPI protection in `%APPDATA%\PRDRefiner\confluence.json`, and warms the pinned MCP runtime. Start a new Agent task afterward. See the root README for PAT creation and manual registration examples for other Agents.

## Claude Code

The repository contains `.claude-plugin/plugin.json` and a development marketplace file. Live installation and slash-command behavior have not yet been verified.

## Cursor

The repository contains `.cursor-plugin/plugin.json` that points to the shared `skills/` directory. Live marketplace installation has not yet been verified.

## Kimi Code

The repository contains `.kimi-plugin/plugin.json` with Skill registration and structured-question tool guidance. Live installation has not yet been verified.

## OpenCode

The root `package.json` points to `.opencode/plugins/prd-refiner.js`. The plugin registers the shared Skill path without automatic chat injection.

After the repository is accessible from the target environment, install it using OpenCode's supported Git/package plugin mechanism and explicitly load or invoke `prd-refiner`.

OpenCode does not currently receive the Confluence server from the Codex manifest. Register the shared `integrations/confluence-mcp/launch.ps1` command as a local stdio MCP server, using the example in the root README. The same encrypted user configuration is reused.

## Pi

The root `package.json` declares the Pi extension and shared Skill path. The extension registers `skills/` through resource discovery and does not auto-inject the workflow.

## Gemini CLI, Hermes Agent, and Devin

Initial manifests and registration adapters are present. Complete a real client installation test before publishing platform-specific commands as supported instructions.

## Security

Do not store private PRDs, Figma tokens, PATs, API keys or generated customer outputs in this repository. The Confluence setup stores only DPAPI-protected material outside the checkout. Do not copy that file between Windows users; rerun setup for each user instead.
