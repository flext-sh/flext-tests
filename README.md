# FLEXT-Tests

**FLEXT-Tests** is the shared test infrastructure library for the FLEXT ecosystem. It provides reusable test utilities, builders, factories, matchers, and validation tools used across all FLEXT projects.

**Reviewed**: 2026-03-16 | **Version**: 0.12.0-dev

Part of the [FLEXT](https://github.com/flext-sh/flext) ecosystem.

## Key Components

- **Builders**: Fluent test data builders for constructing complex domain objects.
- **Factories**: Factory Boy factories for generating test fixtures with realistic data.
- **Matchers**: Custom assertion matchers for domain-specific validations.
- **Validators**: Architecture and code quality validation rules (imports, layers, types, settings).
- **Utilities**: Shared test helpers and convenience functions.
- **Docker**: Docker-based test infrastructure helpers.

## Installation

```bash
poetry add --group dev flext-tests
```

## Usage

```python
from flext_tests import c
from flext_tests import tm
from flext_tests import u
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
