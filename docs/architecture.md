# Architecture

## Design goal

PRD Refiner separates product-domain behavior from host-specific installation and tool APIs. The core workflow should evolve once and be consumed by every supported AI Agent.

```text
Platform marketplace or package manager
                 ↓
        Platform adapter/manifest
                 ↓
        Shared skills/prd-refiner
                 ↓
     PRD rules, templates, validation
```

## Layers

### Plugin distribution layer

Platform manifests make the project installable, versioned and discoverable. They may declare UI metadata, Skill paths and native tool mappings. They must not contain copies of the PRD optimization workflow.

### Shared Skill layer

`skills/prd-refiner/SKILL.md` owns the workflow:

- explicit startup;
- source parsing and evidence classification;
- Plan-mode structured clarification;
- decision recording;
- demand-document generation;
- final quality checks.

Supporting references, templates and scripts live beside the Skill so they travel with every plugin distribution.

The method is intentionally more important than the input layout:

- `references/prd-optimization-spec.md` normalizes arbitrary PRD formats into a twelve-dimension information model;
- `references/interactive-workflow.md` defines the ten-stage clarification and delivery loop;
- `references/prototype-analysis.md` defines prototype input levels, `UI-xxx` interaction modeling and source-conflict handling;
- `references/evaluation-standard.md` provides the same weighted scale for before/after comparison;
- templates and validators make the method repeatable but do not replace product-manager decisions.

### Integration layer

Figma and prototype integrations should expose read-only evidence to the shared Skill. They do not override product-manager decisions and do not change the core information model.

The Confluence integration is an optional delivery adapter. The plugin ships a stdio MCP descriptor plus a Windows launcher. The launcher reads a current-user DPAPI-protected PAT from `%APPDATA%\PRDRefiner\confluence.json`, fixes the company URL to `https://confluence.zwcad.com`, and starts a dependency-pinned `mcp-atlassian` runtime through a process-local wrapper that disables generated heading Anchor macros. Credentials stay outside the repository and requirement packages. Confluence writes occur only after local package generation, a write preview and explicit product-manager confirmation.

## Explicit invocation

Unlike always-on methodology plugins, PRD Refiner must not inject itself into every conversation. Each new optimization task begins only after explicit user invocation. Platform adapters should therefore register the Skill but avoid session-start bootstrap hooks.

## Portability rule

Platform differences belong in adapters. If a host lacks multi-question structured input, the same Skill falls back to sequential questions rather than changing the business protocol.
