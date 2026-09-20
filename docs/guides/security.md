<!-- AUTO-GENERATED FILE — regenerate through `make gen` from the workspace root. -->
<!-- Source of truth: `<workspace-root>/docs/guides/security.md`; adjust that workspace source, never this member projection. -->

# flext-tests - Security Guide

> Project profile: `flext-tests`

<!-- TOC START -->

- [Dependabot vulnerability governance](#dependabot-vulnerability-governance)

<!-- TOC END -->

Security practices are governed by project-specific policies and central architecture
ADRs.

Primary references:

- `docs/architecture/adr/README.md`
- `docs/architecture/baseline-v0.13.0.md`
- `docs/reports/dependabot-alerts-2026-06-24.md`

## Dependabot vulnerability governance

- The official security alert inventory is at:
  - `docs/reports/dependabot-alerts-2026-06-24.md`
- O plano atual cobre três frentes:
  - inventariar alertas por gravidade e pacote,
  - agrupar remediações em ondas (critical/high first),
  - ampliar Dependabot para rastrear os módulos Python com `pyproject.toml` no monorepo.
- A execução de segurança deve registrar evidência por ação (alerta, commit de correção
  e status de fechamento) no `bd`, sem "close" sem trilha.
