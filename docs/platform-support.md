# Platform Support

## Status definitions

- **Validated**: installed in the real client and exercised through the core interaction flow.
- **Prepared**: manifest or adapter exists and passes local syntax/structure checks, but has not completed a real client test.
- **Planned**: architecture boundary is documented, but implementation does not yet exist.

| Platform | Status | Entry point | Remaining verification |
|---|---|---|---|
| ChatGPT desktop app (Codex plugin mechanism) | Validated | `.codex-plugin/plugin.json` | Regression-test future releases |
| Codex CLI | Prepared | `.codex-plugin/plugin.json` | Install and explicit invocation in the CLI client |
| Claude Code | Prepared | `.claude-plugin/plugin.json` | Install, explicit invocation, multi-turn behavior |
| Cursor | Prepared | `.cursor-plugin/plugin.json` | Marketplace install and Skill discovery |
| Kimi Code | Prepared | `.kimi-plugin/plugin.json` | `AskUserQuestion` grouping and custom input |
| OpenCode | Prepared | `.opencode/plugins/prd-refiner.js` | Git install, Skill path registration, TUI clarification |
| Pi | Prepared | `.pi/extensions/prd-refiner.ts` | Package install and native Skill discovery |
| Gemini CLI | Prepared | `gemini-extension.json` | Extension install and explicit invocation guard |
| Hermes Agent | Prepared | `.hermes-plugin/__init__.py` | Plugin install and Skill registration |
| Devin | Prepared | `.devin-plugin/plugin.json` | Plugin install and Skill discovery |
| Company Confluence MCP | Validated for text, page hierarchy, mixed text/image bodies and attachment upload | `.mcp.json`, `integrations/confluence-mcp/` | Additional Agent clients |
| Figma API/MCP | Planned | `references/figma-integration.md` | Authentication, read-only connector, evidence mapping |

Only the ChatGPT desktop app has completed a real installation and interaction test. Every other adapter is Prepared: it exists and passes structure checks, and must not be described as supported.

## Promotion checklist

A prepared platform becomes validated only after confirming:

1. the plugin installs through the platform's supported mechanism;
2. the shared Skill is discovered without copying it;
3. ordinary PRD conversation does not auto-trigger the workflow;
4. explicit invocation starts the workflow;
5. structured or fallback clarification works across multiple turns;
6. all six output documents can be produced;
7. no platform adapter silently changes product decisions or evidence rules.

For Confluence delivery, validation additionally requires a write preview, explicit confirmation, page read-back, attachment read-back when applicable, and a recorded partial-failure state. The current evidence covers Confluence 7.19.4 page search, read, existing-page update, child-page creation/update, parent-child and ancestor checks, Markdown-table HTML rendering, native cross-page attachment references in tables/body, attachment upload through the pinned MCP's own tool, and mixed text/image page bodies verified on the project test page. Authenticated attachment download URLs still do not work as external `ri:url` images, so body images must be referenced as `<ri:attachment>` on the page that owns them.
