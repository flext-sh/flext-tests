# AGENTS.md — flext-tests

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_tests` · deps: `flext-cli`, `flext-core`, `flext-infra`

## Overview

Shared test infrastructure for typed matchers, fixtures, builders, and the
generic Make framework. Every FLEXT package test suite consumes it.

## Structure

```text
src/flext_tests/
├── base.py                 # FlextTestsServiceBase, FlextTestsCase
├── tmatchers.py            # public tm (matchers)
├── conftest_plugin.py      # pytest11 plugin registration
├── enforcement.py files.py domains.py docker.py
├── _validator/ _fixtures/ _domains_parts/ _docker_parts/
├── constants.py typings.py protocols.py models.py utilities.py
└── _constants/ _models/ _protocols/ _typings/ _utilities/
```

## Code Map

| Symbol | Kind | Location | Role |
|--------|------|----------|------|
| `tm` | facade | `tmatchers.py` | matchers — `tm.ok` / `tm.that` / `tm.fail` |
| `FlextTestsServiceBase`, `FlextTestsCase` | classes | `base.py` | test service anchors |
| pytest plugin | module | `conftest_plugin.py` | pytest11 entry (fixtures/enforcement) |

There is **no runtime `api.py`** — this is test tooling.

## Conventions (specific to this package)

- Assert via `tm.*`, never bare `assert`. Tests are behavior-only through
  public facades, without mocks or patching the system under test.
- Use `c/t/p/m/u` for typed fixtures and
  `FlextTestsMakeUtilitiesMixin` for the Make domain.

## Anti-Patterns / Gotchas

- `conftest_plugin.py` is the pytest11 entry point. Packages receive fixtures
  and enforcement through it and never duplicate them locally.

## Commands

```bash
make check PROJECT=flext-tests
make test  PROJECT=flext-tests       # tests/{unit,integration,fixtures}
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
