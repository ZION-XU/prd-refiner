# PRD Refiner Repository Instructions

## Source of truth

- Treat `skills/prd-refiner/` as the only business-logic source of truth.
- Never copy or fork `SKILL.md`, requirement rules, or output templates into platform adapter directories.
- Put platform-specific installation, tool mapping, and skill-registration logic in the corresponding adapter directory.

## Product invariants

- Require explicit user invocation. Do not add automatic PRD-context triggering or session-start injection.
- Require Plan mode before Codex structured clarification.
- Ask high-impact or dependent decisions individually.
- Group only 2–3 independent questions whose answers do not change one another.
- Never turn model inference into a confirmed product decision.
- Preserve source links and independent `CL-xxx` records for every decision.
- Keep the three required outputs: `ai-ready-prd.md`, `clarification-log.md`, and `quality-report.md`.

## Platform adapters

- A platform adapter may register the shared `skills/` directory and map native tools.
- Do not claim a platform is verified until a real installation and interaction test has been completed.
- Do not add a manifest field for a connector, MCP server, hook, or app unless the corresponding implementation exists.
- Keep Figma and other prototype integrations read-only by default; authentication belongs to the host environment.

## Validation

After changing core Skill content, run the Skill validator and cross-platform validator. After changing the Codex manifest, also run the Codex plugin validator. Run syntax checks for any adapter code changed.

## Repository hygiene

- Never commit credentials, access tokens, private PRDs, generated customer requirement packages, or local installation caches.
- Keep examples synthetic or fully anonymized.
- Update `RELEASE-NOTES.md` for user-visible behavior changes.
