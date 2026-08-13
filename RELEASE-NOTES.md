# Release Notes

## Unreleased

- Standardized the user-facing product name as `PRD Refiner` in Codex plugin and Skill metadata.

## 1.0.0 — 2026-08-13

Initial private development release.

### Core workflow

- Added explicit `prd-refiner` Skill invocation.
- Added Plan-mode structured clarification for Codex.
- Added hybrid clarification: individual high-impact decisions and groups of 2–3 independent questions.
- Added PRD and optional prototype evidence classification.
- Added conflict handling that requires product-manager confirmation.

### Outputs

- Added `ai-ready-prd.md` template.
- Added `clarification-log.md` template with independent `CL-xxx` records.
- Added `quality-report.md` template.
- Added deterministic requirement-package validation.

### Plugin packaging

- Added Codex plugin packaging and local marketplace installation.
- Added initial adapter scaffolding for Claude Code, Cursor, Kimi Code, OpenCode, Pi, Gemini CLI, Hermes Agent, and Devin.
- Added cross-platform path and version validation.
- Added a future Figma connector contract without declaring an unavailable API integration.

### Validation status

- Codex App / CLI: validated locally.
- Other adapters: structure and syntax prepared; live client validation pending.
