"""Architecture validator constants for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from enum import StrEnum, unique
from typing import ClassVar, Final

from flext_tests import t


class FlextTestsValidatorConstantsMixin:
    """Architecture validator constants mixin."""

    @unique
    class ValidatorSeverity(StrEnum):
        """Violation severity levels."""

        CRITICAL = "CRITICAL"
        HIGH = "HIGH"
        MEDIUM = "MEDIUM"
        LOW = "LOW"

    # Rules
    VALIDATOR_RULE_IMPORT_001: Final[tuple[str, str]] = (
        "HIGH",
        "Lazy import (not at module top)",
    )
    VALIDATOR_RULE_IMPORT_002: Final[tuple[str, str]] = (
        "HIGH",
        "TYPE_CHECKING block detected",
    )
    VALIDATOR_RULE_IMPORT_003: Final[tuple[str, str]] = (
        "HIGH",
        "try/except ImportError pattern",
    )
    VALIDATOR_RULE_IMPORT_004: Final[tuple[str, str]] = (
        "CRITICAL",
        "sys.path manipulation",
    )
    VALIDATOR_RULE_IMPORT_005: Final[tuple[str, str]] = (
        "MEDIUM",
        "Direct technology import (should use facade)",
    )
    VALIDATOR_RULE_IMPORT_006: Final[tuple[str, str]] = (
        "HIGH",
        "Non-root import from flext-* package",
    )
    VALIDATOR_RULE_TYPE_001: Final[tuple[str, str]] = (
        "CRITICAL",
        "type suppression comment",
    )
    VALIDATOR_RULE_TYPE_002: Final[tuple[str, str]] = (
        "CRITICAL",
        "wildcard type annotation",
    )
    VALIDATOR_RULE_TYPE_003: Final[tuple[str, str]] = ("MEDIUM", "Unapproved  usage")
    VALIDATOR_RULE_TYPE_004: Final[tuple[str, str]] = (
        "CRITICAL",
        "legacy typing factory or generic syntax",
    )
    VALIDATOR_RULE_TYPE_005: Final[tuple[str, str]] = (
        "CRITICAL",
        "legacy typing annotation form",
    )
    VALIDATOR_RULE_TYPE_006: Final[tuple[str, str]] = (
        "CRITICAL",
        "forbidden object annotation",
    )
    VALIDATOR_RULE_TYPE_007: Final[tuple[str, str]] = (
        "HIGH",
        "bool-returning is_* helper",
    )
    VALIDATOR_RULE_TEST_001: Final[tuple[str, str]] = (
        "HIGH",
        "monkeypatch usage detected",
    )
    VALIDATOR_RULE_TEST_002: Final[tuple[str, str]] = (
        "HIGH",
        "Mock/MagicMock usage detected",
    )
    VALIDATOR_RULE_TEST_003: Final[tuple[str, str]] = (
        "HIGH",
        "@patch decorator usage detected",
    )
    VALIDATOR_RULE_CONFIG_001: Final[tuple[str, str]] = (
        "CRITICAL",
        "mypy ignore_errors = true",
    )
    VALIDATOR_RULE_CONFIG_002: Final[tuple[str, str]] = (
        "HIGH",
        "Custom ruff ignore beyond approved list",
    )
    VALIDATOR_RULE_CONFIG_003: Final[tuple[str, str]] = (
        "MEDIUM",
        "disallow_incomplete_defs = false",
    )
    VALIDATOR_RULE_CONFIG_004: Final[tuple[str, str]] = (
        "MEDIUM",
        "warn_return_any = false",
    )
    VALIDATOR_RULE_CONFIG_005: Final[tuple[str, str]] = (
        "LOW",
        "reportPrivateUsage = false",
    )
    VALIDATOR_RULE_BYPASS_001: Final[tuple[str, str]] = (
        "MEDIUM",
        "noqa comment detected",
    )
    VALIDATOR_RULE_BYPASS_002: Final[tuple[str, str]] = (
        "LOW",
        "pragma: no cover (unapproved)",
    )
    VALIDATOR_RULE_BYPASS_003: Final[tuple[str, str]] = (
        "HIGH",
        "Exception swallowing (bare except or pass)",
    )
    VALIDATOR_RULE_LAYER_001: Final[tuple[str, str]] = (
        "CRITICAL",
        "Lower layer importing upper layer",
    )
    VALIDATOR_RULE_MD_001: Final[tuple[str, str]] = (
        "CRITICAL",
        "Python syntax error in markdown code block",
    )
    VALIDATOR_RULE_MD_002: Final[tuple[str, str]] = (
        "CRITICAL",
        "Forbidden typing import in markdown code block",
    )
    VALIDATOR_RULE_MD_003: Final[tuple[str, str]] = (
        "MEDIUM",
        "Missing future annotations in markdown code block",
    )
    VALIDATOR_RULE_MD_004: Final[tuple[str, str]] = (
        "HIGH",
        "Forbidden type annotation in markdown code block",
    )

    @classmethod
    def validator_rule(
        cls,
        rule_id: str,
    ) -> tuple[FlextTestsValidatorConstantsMixin.ValidatorSeverity, str]:
        """Get rule by ID string (e.g., 'IMPORT-001' -> VALIDATOR_RULE_IMPORT_001)."""
        attr_name = "VALIDATOR_RULE_" + rule_id.replace("-", "_")
        rule: tuple[FlextTestsValidatorConstantsMixin.ValidatorSeverity, str] = getattr(
            cls, attr_name
        )
        return rule

    # Messages
    VALIDATOR_MSG_VIOLATION: Final[str] = "{rule_id} at {file}:{line}"
    VALIDATOR_MSG_VIOLATION_DETAIL: Final[str] = (
        "{rule_id}: {description} at {file}:{line}"
    )
    VALIDATOR_MSG_VIOLATION_WITH_SNIPPET: Final[str] = (
        "{rule_id}: {description}\n  → {snippet}"
    )
    VALIDATOR_MSG_SCAN_COMPLETE: Final[str] = (
        "Scanned {count} files, found {violations} violations"
    )
    VALIDATOR_MSG_SCAN_PASSED: Final[str] = (
        "Validation passed: {count} files, 0 violations"
    )
    VALIDATOR_MSG_SCAN_FAILED: Final[str] = (
        "Validation failed: {violations} violations in {count} files"
    )
    VALIDATOR_MSG_LAYER_VIOLATION: Final[str] = (
        "'{current}' L{current_level} -> '{imported}' L{imported_level}"
    )
    VALIDATOR_MSG_IMPORT_TECH: Final[str] = "Direct technology import: {module}"
    VALIDATOR_MSG_IMPORT_NON_ROOT: Final[str] = "Non-root import: from {module}"
    VALIDATOR_MSG_CONFIG_IGNORE: Final[str] = (
        "ignore_errors = true for module '{module}'"
    )
    VALIDATOR_MSG_CONFIG_RUFF: Final[str] = "Custom ruff ignore: {code}"
    VALIDATOR_MSG_TEST_MONKEYPATCH: Final[str] = (
        "monkeypatch usage in function '{func}'"
    )
    VALIDATOR_MSG_TYPE_ANY_ARG: Final[str] = "wildcard type in argument '{arg}'"
    VALIDATOR_MSG_TYPE_ANY_RETURN: Final[str] = "wildcard type in return type"
    VALIDATOR_MSG_TYPE_LEGACY_FACTORY: Final[str] = (
        "legacy typing factory or generic syntax '{name}'"
    )
    VALIDATOR_MSG_TYPE_LEGACY_ANNOTATION: Final[str] = (
        "legacy typing annotation '{name}'"
    )
    VALIDATOR_MSG_TYPE_OBJECT_ANNOTATION: Final[str] = (
        "forbidden object annotation in {location}"
    )
    VALIDATOR_MSG_TYPE_BOOL_IS_HELPER: Final[str] = (
        "bool-returning is_* helper '{name}'"
    )
    VALIDATOR_MSG_BYPASS_EXCEPTION: Final[str] = "Exception swallowing: {pattern}"
    VALIDATOR_MSG_BYPASS_BARE_EXCEPT: Final[str] = "bare except"
    VALIDATOR_MSG_BYPASS_ONLY_PASS: Final[str] = "except with only pass"
    VALIDATOR_MSG_MD_SYNTAX: Final[str] = "SyntaxError in code block: {msg}"
    VALIDATOR_MSG_MD_FORBIDDEN_IMPORT: Final[str] = "Forbidden import: {import_name}"
    VALIDATOR_MSG_MD_MISSING_FUTURE: Final[str] = (
        "Missing: from __future__ import annotations"
    )
    VALIDATOR_MSG_MD_FORBIDDEN_ANNOTATION: Final[str] = (
        "Forbidden annotation: {annotation} (use t.* contracts)"
    )

    # Markdown validation
    VALIDATOR_MD_OPTION_DOCS: Final[str] = "--markdown-docs"
    VALIDATOR_MD_PYTHON_BLOCK_RE: ClassVar[re.Pattern[str]] = re.compile(
        r"^```python\s*$\n(.*?)^```\s*$",
        re.MULTILINE | re.DOTALL,
    )
    VALIDATOR_MD_OBJECT_ANNOTATION_RE: ClassVar[re.Pattern[str]] = re.compile(
        r"(?::\s*object\b|->.*\bobject\b)",
    )
    VALIDATOR_MD_FUTURE_ANNOTATIONS_MARKER: Final[str] = (
        "from __future__ import annotations"
    )
    VALIDATOR_MD_TYPING_IMPORT_PREFIX: Final[str] = "from typing import"
    VALIDATOR_MD_FORBIDDEN_TYPING_NAMES: Final[frozenset[str]] = frozenset({
        "Any",
        "Optional",
        "Union",
    })

    # Defaults
    VALIDATOR_EXCLUDE_PATTERNS: Final[tuple[str, ...]] = (
        "**/.venv/**",
        "**/venv/**",
        "**/__pycache__/**",
        "**/build/**",
        "**/dist/**",
        "**/.git/**",
        "**/htmlcov/**",
        "**/*.pyc",
    )
    VALIDATOR_INCLUDE_PATTERNS: Final[tuple[str, ...]] = ("**/*.py",)
    VALIDATOR_IMPORTS_KEY: Final[str] = "imports"
    VALIDATOR_TYPES_KEY: Final[str] = "types"
    VALIDATOR_TESTS_KEY: Final[str] = "tests"
    VALIDATOR_CONFIG_KEY: Final[str] = "settings"
    VALIDATOR_BYPASS_KEY: Final[str] = "bypass"
    VALIDATOR_LAYER_KEY: Final[str] = "layer"
    VALIDATOR_MARKDOWN_KEY: Final[str] = "markdown"

    # Approved
    VALIDATOR_APPROVED_CAST_PATTERNS: Final[tuple[str, ...]] = (
        "service\\.py$",
        "container\\.py$",
    )
    VALIDATOR_LEGACY_FACTORY_NAMES: Final[frozenset[str]] = frozenset({
        "ParamSpec",
        "TypeAlias",
        "TypeVar",
    })
    VALIDATOR_LEGACY_BASE_NAMES: Final[frozenset[str]] = frozenset({"Generic"})
    VALIDATOR_LEGACY_ANNOTATION_NAMES: Final[frozenset[str]] = frozenset({
        "Dict",
        "FrozenSet",
        "List",
        "Optional",
        "Set",
        "Tuple",
        "TypeAliasType",
        "TypeGuard",
        "Union",
    })
    VALIDATOR_APPROVED_PRAGMA_PATTERNS: Final[tuple[str, ...]] = ("__init__\\.py$",)
    VALIDATOR_APPROVED_RUFF_IGNORES: Final[frozenset[str]] = frozenset({
        "BLE001",
        "COM812",
        "CPY001",
        "D203",
        "D213",
        "D401",
        "D417",
        "DOC201",
        "DOC202",
        "DOC402",
        "DOC501",
        "DOC502",
        "E501",
        "ERA001",
        "FBT003",
        "G004",
        "N813",
        "N816",
        "PLR0904",
        "PLR0911",
        "PLR0912",
        "PLR0913",
        "PLR0914",
        "PLR0915",
        "PLR0917",
        "PLR6301",
        "PYI042",
        "Q000",
        "RUF001",
        "RUF002",
        "RUF003",
        "RUF005",
        "S608",
        "TC001",
        "TC002",
        "TC003",
        "TRY003",
        "TRY300",
        "TRY301",
        "UP007",
        "UP040",
        "W293",
    })
    VALIDATOR_APPROVED_TECH_IMPORTS: Final[frozenset[str]] = frozenset({
        "ldap3",
        "oracledb",
        "cx_Oracle",
        "click",
        "rich",
        "typer",
    })
    VALIDATOR_APPROVED_MOCK_NAMES: Final[frozenset[str]] = frozenset({
        "Mock",
        "MagicMock",
        "AsyncMock",
        "PropertyMock",
    })
    VALIDATOR_APPROVED_FLEXT_PACKAGES: Final[frozenset[str]] = frozenset({
        "flext_core",
        "flext_cli",
        "flext_ldap",
        "flext_ldif",
        "flext_tests",
    })
    VALIDATOR_APPROVED_INTERNAL_INIT_PATTERNS: Final[tuple[str, ...]] = (
        "_[^/]+/__init__\\.py$",
    )

    # LayerHierarchy
    LAYER_CONSTANTS: Final[int] = 0
    LAYER_TYPINGS: Final[int] = 0
    LAYER_PROTOCOLS: Final[int] = 0
    LAYER_CONFIG: Final[int] = 1
    LAYER_RUNTIME: Final[int] = 2
    LAYER_EXCEPTIONS: Final[int] = 3
    LAYER_RESULT: Final[int] = 3
    LAYER_LOGGINGS: Final[int] = 4
    LAYER_MODELS: Final[int] = 5
    LAYER_UTILITIES: Final[int] = 5
    LAYER_MIXINS: Final[int] = 5
    LAYER_CONTAINER: Final[int] = 6
    LAYER_SERVICE: Final[int] = 6
    LAYER_CONTEXT: Final[int] = 6
    LAYER_HANDLERS: Final[int] = 7
    LAYER_DISPATCHER: Final[int] = 8
    LAYER_REGISTRY: Final[int] = 8
    LAYER_DECORATORS: Final[int] = 9

    @classmethod
    def layer_dict(cls) -> t.IntMapping:
        """Get layer hierarchy as dictionary."""
        return {
            "constants": cls.LAYER_CONSTANTS,
            "typings": cls.LAYER_TYPINGS,
            "protocols": cls.LAYER_PROTOCOLS,
            "settings": cls.LAYER_CONFIG,
            "runtime": cls.LAYER_RUNTIME,
            "exceptions": cls.LAYER_EXCEPTIONS,
            "result": cls.LAYER_RESULT,
            "loggings": cls.LAYER_LOGGINGS,
            "models": cls.LAYER_MODELS,
            "utilities": cls.LAYER_UTILITIES,
            "mixins": cls.LAYER_MIXINS,
            "container": cls.LAYER_CONTAINER,
            "service": cls.LAYER_SERVICE,
            "context": cls.LAYER_CONTEXT,
            "handlers": cls.LAYER_HANDLERS,
            "dispatcher": cls.LAYER_DISPATCHER,
            "registry": cls.LAYER_REGISTRY,
            "decorators": cls.LAYER_DECORATORS,
        }
