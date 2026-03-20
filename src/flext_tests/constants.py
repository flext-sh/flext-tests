"""Constants for FLEXT tests.

Provides FlextTestsConstants, extending FlextConstants with test-specific constants
for Docker operations, container management, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum, unique
from typing import Final, Literal

from flext_core import FlextConstants, FlextModels


class FlextTestsConstants(FlextConstants):
    """Constants for FLEXT tests - extends FlextConstants.

    Architecture layer: Layer 0 foundation constants with test extensions.
    All base constants from FlextConstants are available through inheritance.
    """

    class Tests:
        """Test-specific constants namespace.

        All test-specific constants are organized under this namespace to clearly
        distinguish them from base FlextConstants. Access via c.Tests.*
        """

        class Docker:
            """Docker test infrastructure constants."""

            SHARED_CONTAINERS: Final[Mapping[str, FlextModels.ConfigMap]] = {
                "flext-oracle-db-test": FlextModels.ConfigMap(
                    root={
                        "compose_file": "docker/docker-compose.oracle-db.yml",
                        "service": "oracle-db",
                        "port": 1522,
                        "host": "localhost",
                        "container_name": "flext-oracle-db-test",
                    },
                ),
            }

            @unique
            class ContainerStatus(StrEnum):
                """Container status enumeration for test infrastructure."""

                RUNNING = "running"
                STOPPED = "stopped"
                NOT_FOUND = "not_found"
                ERROR = "error"
                STARTING = "starting"
                STOPPING = "stopping"
                RESTARTING = "restarting"

        class Matcher:
            """Matcher constants for test assertions (tm.* methods).

            Provides error message templates with .format() support.
            Use c.Tests.Matcher.* for access.
            """

            ERR_NOT_STARTSWITH: Final[str] = (
                "Expected '{text}' to start with '{prefix}'"
            )
            ERR_NOT_ENDSWITH: Final[str] = "Expected '{text}' to end with '{suffix}'"
            ERR_NOT_MATCHES: Final[str] = (
                "Expected '{text}' to match pattern '{pattern}'"
            )
            ERR_OK_FAILED: Final[str] = "Expected success but got failure: {error}"
            ERR_FAIL_EXPECTED: Final[str] = (
                "Expected failure but got success with value: {value!r}"
            )
            ERR_TYPE_FAILED: Final[str] = "Expected type {expected} but got {actual}"
            ERR_CONTAINS_FAILED: Final[str] = (
                "Expected {container!r} to contain {item!r}"
            )
            ERR_LACKS_FAILED: Final[str] = (
                "Expected {container!r} to NOT contain {item!r}"
            )
            ERR_LEN_EXACT_FAILED: Final[str] = (
                "Expected length {expected} but got {actual}"
            )
            ERR_LEN_RANGE_FAILED: Final[str] = (
                "Expected length in range [{min}, {max}] but got {actual}"
            )
            ERR_DEEP_PATH_FAILED: Final[str] = (
                "Deep match failed at path '{path}': {reason}"
            )
            ERR_PREDICATE_FAILED: Final[str] = (
                "Custom predicate failed for value: {value!r}"
            )
            ERR_ALL_ITEMS_FAILED: Final[str] = (
                "Not all items match: failed at index {index}"
            )
            ERR_ANY_ITEMS_FAILED: Final[str] = "No items match the predicate"
            ERR_KEYS_MISSING: Final[str] = "Missing required keys: {keys}"
            ERR_KEYS_EXTRA: Final[str] = "Unexpected keys present: {keys}"
            ERR_SCOPE_PATH_NOT_FOUND: Final[str] = (
                "Path '{path}' not found in value: {error}"
            )
            ERR_ERROR_CODE_MISMATCH: Final[str] = (
                "Expected error code {expected!r} but got {actual!r}"
            )
            ERR_ERROR_CODE_NOT_CONTAINS: Final[str] = (
                "Expected error code to contain {expected!r} but got {actual!r}"
            )
            ERR_ERROR_DATA_KEY_MISSING: Final[str] = (
                "Expected error data key {key!r} not found"
            )
            ERR_ERROR_DATA_VALUE_MISMATCH: Final[str] = (
                "Error data key {key!r}: expected {expected!r}, got {actual!r}"
            )
            ERR_SCOPE_CLEANUP_FAILED: Final[str] = (
                "Cleanup function failed in scope: {error}"
            )
            EMAIL_PATTERN: Final[str] = (
                "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
            )

        class Factory:
            """Factory constants for test data generation (tt.* methods).

            Provides default values and error messages
            for FlextTestsFactories. Use c.Tests.Factory.* for access.
            """

            DEFAULT_USER_NAME: Final[str] = "Test User"
            DEFAULT_USER_EMAIL_TEMPLATE: Final[str] = "user_{id}@example.com"
            DEFAULT_USER_ACTIVE: Final[bool] = True
            DEFAULT_SERVICE_TYPE: Final[str] = "api"
            DEFAULT_ENVIRONMENT: Final[str] = "test"
            DEFAULT_DEBUG: Final[bool] = True
            DEFAULT_LOG_LEVEL: Final[str] = "DEBUG"
            DEFAULT_TIMEOUT: Final[int] = FlextConstants.DEFAULT_TIMEOUT_SECONDS
            DEFAULT_MAX_RETRIES: Final[int] = FlextConstants.DEFAULT_MAX_RETRY_ATTEMPTS
            DEFAULT_SERVICE_NAME_TEMPLATE: Final[str] = "Test {type} Service"
            DEFAULT_ENTITY_NAME: Final[str] = "test_entity"
            DEFAULT_BATCH_COUNT: Final[int] = 5
            DEFAULT_BATCH_ENVIRONMENTS: Final[tuple[str, ...]] = (
                "test",
                "staging",
                "production",
            )
            DEFAULT_BATCH_SERVICE_TYPES: Final[tuple[str, ...]] = (
                "api",
                "database",
                "cache",
            )
            ERROR_VALUE_NONE: Final[str] = "Value cannot be None"
            ERROR_DEFAULT: Final[str] = "Operation failed"
            ERROR_VALIDATION: Final[str] = "Validation failed"
            ERROR_NOT_FOUND: Final[str] = "Not found"
            SUCCESS_MESSAGE: Final[str] = "success"

            @classmethod
            def service_name(cls, service_type: str) -> str:
                """Generate service name from template.

                Args:
                    service_type: Type of service.

                Returns:
                    Formatted service name.

                """
                return cls.DEFAULT_SERVICE_NAME_TEMPLATE.format(type=service_type)

            @classmethod
            def user_email(cls, user_id: str) -> str:
                """Generate user email from template.

                Args:
                    user_id: User identifier for email generation.

                Returns:
                    Formatted email address.

                """
                return cls.DEFAULT_USER_EMAIL_TEMPLATE.format(id=user_id)

        class Files:
            """File management constants for test infrastructure.

            Provides format mappings, default values, and error messages
            for FlextTestsFiles. Use c.Tests.Files.* for access.
            """

            class Format(StrEnum):
                """File format enumeration."""

                AUTO = "auto"
                TEXT = "text"
                BIN = "bin"
                JSON = "json"
                YAML = "yaml"
                CSV = "csv"
                UNKNOWN = "unknown"

            class CompareMode(StrEnum):
                """File comparison mode enumeration."""

                CONTENT = "content"
                SIZE = "size"
                HASH = "hash"
                LINES = "lines"

            EXT_TO_FMT: Final[Mapping[str, str]] = {
                ".txt": "text",
                ".log": "text",
                ".md": "text",
                ".rst": "text",
                ".bin": "bin",
                ".dat": "bin",
                ".json": "json",
                ".yaml": "yaml",
                ".yml": "yaml",
                ".csv": "csv",
                ".tsv": "csv",
            }
            DEFAULT_FILENAME: Final[str] = "file"
            DEFAULT_ENCODING: Final[str] = FlextConstants.ENCODING
            DEFAULT_BINARY_ENCODING: Final[str] = "binary"
            DEFAULT_JSON_INDENT: Final[int] = 2
            DEFAULT_CSV_DELIMITER: Final[str] = ","
            DEFAULT_EXTENSION: Final[str] = ".txt"
            PERMISSION_READONLY_FILE: Final[int] = 292
            PERMISSION_WRITABLE_FILE: Final[int] = 420
            PERMISSION_WRITABLE_DIR: Final[int] = 493
            HASH_CHUNK_SIZE: Final[int] = 8192
            SIZE_UNITS: Final[tuple[str, ...]] = ("B", "KB", "MB", "GB", "TB", "PB")
            SIZE_THRESHOLD: Final[int] = 1024
            ERROR_FILE_NOT_FOUND: Final[str] = "File not found: {path}"
            ERROR_INVALID_JSON: Final[str] = "Invalid JSON: {error}"
            ERROR_INVALID_YAML: Final[str] = "Invalid YAML: {error}"
            ERROR_ENCODING: Final[str] = "Encoding error: {error}"
            ERROR_READ: Final[str] = "Read error: {error}"
            ERROR_COMPARE: Final[str] = "Compare error: {error}"
            ERROR_INFO: Final[str] = "Info error: {error}"

            @classmethod
            def format_size(cls, size: int) -> str:
                """Format size in human-readable format.

                Args:
                    size: Size in bytes.

                Returns:
                    Human-readable size string like "1.2 KB".

                """
                for unit in cls.SIZE_UNITS:
                    if size < cls.SIZE_THRESHOLD:
                        return f"{size:.1f} {unit}" if unit != "B" else f"{size} {unit}"
                    size //= cls.SIZE_THRESHOLD
                return f"{size:.1f} PB"

            @classmethod
            def get_format(cls, extension: str) -> str:
                """Get format from file extension.

                Args:
                    extension: File extension (e.g., ".json").

                Returns:
                    Format string or "text" as default.

                """
                return cls.EXT_TO_FMT.get(extension.lower(), "text")

        class Validator:
            """Architecture validator constants.

            Provides rule definitions, severity levels, approved patterns.
            Use c.Tests.Validator.* for access.
            """

            class Severity(StrEnum):
                """Violation severity levels."""

                CRITICAL = "CRITICAL"
                HIGH = "HIGH"
                MEDIUM = "MEDIUM"
                LOW = "LOW"

            type SeverityLiteral = Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]

            class Rules:
                """Rule definitions with (severity, description) tuples.

                Access via c.Tests.Validator.Rules.IMPORT_001, etc.
                Each rule is a tuple of (severity: str, description: str).
                """

                IMPORT_001: Final[tuple[str, str]] = (
                    "HIGH",
                    "Lazy import (not at module top)",
                )
                IMPORT_002: Final[tuple[str, str]] = (
                    "HIGH",
                    "TYPE_CHECKING block detected",
                )
                IMPORT_003: Final[tuple[str, str]] = (
                    "HIGH",
                    "try/except ImportError pattern",
                )
                IMPORT_004: Final[tuple[str, str]] = (
                    "CRITICAL",
                    "sys.path manipulation",
                )
                IMPORT_005: Final[tuple[str, str]] = (
                    "MEDIUM",
                    "Direct technology import (should use facade)",
                )
                IMPORT_006: Final[tuple[str, str]] = (
                    "HIGH",
                    "Non-root import from flext-* package",
                )
                TYPE_001: Final[tuple[str, str]] = (
                    "CRITICAL",
                    "type suppression comment",
                )
                TYPE_002: Final[tuple[str, str]] = (
                    "CRITICAL",
                    "wildcard type annotation",
                )
                TYPE_003: Final[tuple[str, str]] = ("MEDIUM", "Unapproved  usage")
                TEST_001: Final[tuple[str, str]] = (
                    "HIGH",
                    "monkeypatch usage detected",
                )
                TEST_002: Final[tuple[str, str]] = (
                    "HIGH",
                    "Mock/MagicMock usage detected",
                )
                TEST_003: Final[tuple[str, str]] = (
                    "HIGH",
                    "@patch decorator usage detected",
                )
                CONFIG_001: Final[tuple[str, str]] = (
                    "CRITICAL",
                    "mypy ignore_errors = true",
                )
                CONFIG_002: Final[tuple[str, str]] = (
                    "HIGH",
                    "Custom ruff ignore beyond approved list",
                )
                CONFIG_003: Final[tuple[str, str]] = (
                    "MEDIUM",
                    "disallow_incomplete_defs = false",
                )
                CONFIG_004: Final[tuple[str, str]] = (
                    "MEDIUM",
                    "warn_return_any = false",
                )
                CONFIG_005: Final[tuple[str, str]] = (
                    "LOW",
                    "reportPrivateUsage = false",
                )
                BYPASS_001: Final[tuple[str, str]] = ("MEDIUM", "noqa comment detected")
                BYPASS_002: Final[tuple[str, str]] = (
                    "LOW",
                    "pragma: no cover (unapproved)",
                )
                BYPASS_003: Final[tuple[str, str]] = (
                    "HIGH",
                    "Exception swallowing (bare except or pass)",
                )
                LAYER_001: Final[tuple[str, str]] = (
                    "CRITICAL",
                    "Lower layer importing upper layer",
                )

                @classmethod
                def get(
                    cls,
                    rule_id: str,
                ) -> tuple[FlextTestsConstants.Tests.Validator.SeverityLiteral, str]:
                    """Get rule by ID string (e.g., 'IMPORT-001' -> IMPORT_001).

                    Args:
                        rule_id: Rule identifier like "IMPORT-001".

                    Returns:
                        Tuple of (severity, description).

                    Raises:
                        KeyError: If rule_id not found.

                    """
                    attr_name = rule_id.replace("-", "_")
                    rule: tuple[
                        FlextTestsConstants.Tests.Validator.SeverityLiteral,
                        str,
                    ] = getattr(cls, attr_name)
                    return rule

            class Messages:
                """Error message templates supporting .format()."""

                VIOLATION: Final[str] = "{rule_id} at {file}:{line}"
                VIOLATION_DETAIL: Final[str] = (
                    "{rule_id}: {description} at {file}:{line}"
                )
                VIOLATION_WITH_SNIPPET: Final[str] = (
                    "{rule_id}: {description}\n  → {snippet}"
                )
                SCAN_COMPLETE: Final[str] = (
                    "Scanned {count} files, found {violations} violations"
                )
                SCAN_PASSED: Final[str] = (
                    "Validation passed: {count} files, 0 violations"
                )
                SCAN_FAILED: Final[str] = (
                    "Validation failed: {violations} violations in {count} files"
                )
                LAYER_VIOLATION: Final[str] = (
                    "'{current}' L{current_level} -> '{imported}' L{imported_level}"
                )
                IMPORT_TECH: Final[str] = "Direct technology import: {module}"
                IMPORT_NON_ROOT: Final[str] = "Non-root import: from {module}"
                CONFIG_IGNORE: Final[str] = "ignore_errors = true for module '{module}'"
                CONFIG_RUFF: Final[str] = "Custom ruff ignore: {code}"
                TEST_MONKEYPATCH: Final[str] = "monkeypatch usage in function '{func}'"
                TYPE_ANY_ARG: Final[str] = "wildcard type in argument '{arg}'"
                TYPE_ANY_RETURN: Final[str] = "wildcard type in return type"
                BYPASS_EXCEPTION: Final[str] = "Exception swallowing: {pattern}"
                BYPASS_BARE_EXCEPT: Final[str] = "bare except"
                BYPASS_ONLY_PASS: Final[str] = "except with only pass"

            class Defaults:
                """Default values for validator configuration."""

                EXCLUDE_PATTERNS: Final[tuple[str, ...]] = (
                    "**/.venv/**",
                    "**/venv/**",
                    "**/__pycache__/**",
                    "**/build/**",
                    "**/dist/**",
                    "**/.git/**",
                    "**/htmlcov/**",
                    "**/*.pyc",
                )
                INCLUDE_PATTERNS: Final[tuple[str, ...]] = ("**/*.py",)
                VALIDATOR_IMPORTS: Final[str] = "imports"
                VALIDATOR_TYPES: Final[str] = "types"
                VALIDATOR_TESTS: Final[str] = "tests"
                VALIDATOR_CONFIG: Final[str] = "config"
                VALIDATOR_BYPASS: Final[str] = "bypass"
                VALIDATOR_LAYER: Final[str] = "layer"

            class Approved:
                """Approved patterns and exceptions for validators."""

                CAST_PATTERNS: Final[tuple[str, ...]] = (
                    "service\\.py$",
                    "container\\.py$",
                )
                PRAGMA_PATTERNS: Final[tuple[str, ...]] = ("__init__\\.py$",)
                RUFF_IGNORES: Final[frozenset[str]] = frozenset({
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
                TECH_IMPORTS: Final[frozenset[str]] = frozenset({
                    "ldap3",
                    "oracledb",
                    "cx_Oracle",
                    "click",
                    "rich",
                    "typer",
                })
                MOCK_NAMES: Final[frozenset[str]] = frozenset({
                    "Mock",
                    "MagicMock",
                    "AsyncMock",
                    "PropertyMock",
                })
                FLEXT_PACKAGES: Final[frozenset[str]] = frozenset({
                    "flext_core",
                    "flext_cli",
                    "flext_ldap",
                    "flext_ldif",
                    "flext_tests",
                })
                INTERNAL_INIT_PATTERNS: Final[tuple[str, ...]] = (
                    "_[^/]+/__init__\\.py$",
                )

            class LayerHierarchy:
                """Layer hierarchy definitions for LAYER-001 validation.

                Lower number = lower layer (should NOT import higher).
                """

                CONSTANTS: Final[int] = 0
                TYPINGS: Final[int] = 0
                PROTOCOLS: Final[int] = 0
                CONFIG: Final[int] = 1
                RUNTIME: Final[int] = 2
                EXCEPTIONS: Final[int] = 3
                RESULT: Final[int] = 3
                LOGGINGS: Final[int] = 4
                MODELS: Final[int] = 5
                UTILITIES: Final[int] = 5
                MIXINS: Final[int] = 5
                CONTAINER: Final[int] = 6
                SERVICE: Final[int] = 6
                CONTEXT: Final[int] = 6
                HANDLERS: Final[int] = 7
                DISPATCHER: Final[int] = 8
                REGISTRY: Final[int] = 8
                DECORATORS: Final[int] = 9

                @classmethod
                def as_dict(cls) -> Mapping[str, int]:
                    """Get layer hierarchy as dictionary.

                    Returns:
                        Mapping of module name to layer number.

                    """
                    return {
                        "constants": cls.CONSTANTS,
                        "typings": cls.TYPINGS,
                        "protocols": cls.PROTOCOLS,
                        "config": cls.CONFIG,
                        "runtime": cls.RUNTIME,
                        "exceptions": cls.EXCEPTIONS,
                        "result": cls.RESULT,
                        "loggings": cls.LOGGINGS,
                        "models": cls.MODELS,
                        "utilities": cls.UTILITIES,
                        "mixins": cls.MIXINS,
                        "container": cls.CONTAINER,
                        "service": cls.SERVICE,
                        "context": cls.CONTEXT,
                        "handlers": cls.HANDLERS,
                        "dispatcher": cls.DISPATCHER,
                        "registry": cls.REGISTRY,
                        "decorators": cls.DECORATORS,
                    }


c = FlextTestsConstants
__all__ = ["FlextTestsConstants", "c"]
