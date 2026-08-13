# Platform Support

## Status definitions

- **Validated**: installed in the real client and exercised through the core interaction flow.
- **Prepared**: manifest or adapter exists and passes local syntax/structure checks, but has not completed a real client test.
- **Planned**: architecture boundary is documented, but implementation does not yet exist.

| Platform | Status | Entry point | Remaining verification |
|---|---|---|---|
| Codex App / CLI | Validated | `.codex-plugin/plugin.json` | Regression-test future releases |
| Claude Code | Prepared | `.claude-plugin/plugin.json` | Install, explicit invocation, multi-turn behavior |
| Cursor | Prepared | `.cursor-plugin/plugin.json` | Marketplace install and Skill discovery |
| Kimi Code | Prepared | `.kimi-plugin/plugin.json` | `AskUserQuestion` grouping and custom input |
| OpenCode | Prepared | `.opencode/plugins/prd-refiner.js` | Git install, Skill path registration, TUI clarification |
| Pi | Prepared | `.pi/extensions/prd-refiner.ts` | Package install and native Skill discovery |
| Gemini CLI | Prepared | `gemini-extension.json` | Extension install and explicit invocation guard |
| Hermes Agent | Prepared | `.hermes-plugin/__init__.py` | Plugin install and Skill registration |
| Devin | Prepared | `.devin-plugin/plugin.json` | Plugin install and Skill discovery |
| Figma API/MCP | Planned | `references/figma-integration.md` | Authentication, read-only connector, evidence mapping |

## Promotion checklist

A prepared platform becomes validated only after confirming:

1. the plugin installs through the platform's supported mechanism;
2. the shared Skill is discovered without copying it;
3. ordinary PRD conversation does not auto-trigger the workflow;
4. explicit invocation starts the workflow;
5. structured or fallback clarification works across multiple turns;
6. all three output documents can be produced;
7. no platform adapter silently changes product decisions or evidence rules.
