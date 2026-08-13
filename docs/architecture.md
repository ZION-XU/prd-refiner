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

### Integration layer

Future Figma, Axure or internal-system integrations should expose read-only evidence to the shared Skill. They do not override product-manager decisions and do not change the core information model.

## Explicit invocation

Unlike always-on methodology plugins, PRD Refiner must not inject itself into every conversation. Each new optimization task begins only after explicit user invocation. Platform adapters should therefore register the Skill but avoid session-start bootstrap hooks.

## Portability rule

Platform differences belong in adapters. If a host lacks multi-question structured input, the same Skill falls back to sequential questions rather than changing the business protocol.
