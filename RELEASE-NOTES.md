# Release Notes

## Unreleased

- Standardized the user-facing product name as `PRD Refiner` in Codex plugin and Skill metadata.
- Added a standalone twelve-dimension PRD optimization specification for arbitrary source formats.
- Added the ten-stage interactive clarification workflow and a weighted before/after evaluation standard.
- Added a reusable evaluation scorecard template.
- Added `interaction-spec.md` and `traceability-matrix.md` as required outputs, with templates and deterministic validation.
- Made `evaluation-scorecard.md` a required output instead of an optional case-only artifact.
- Added prototype input levels, `UI-xxx` modeling, PRD/prototype conflict rules and conditional asset folders.
- Expanded the synthetic CAD layer batch-state case to a complete six-document requirement package.
- Strengthened validation coverage for methodology resources and example artifacts.
- Documented exact Codex local-marketplace installation and update commands in the README.

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
