"""Validator approved-pattern and layer constants for flext-tests."""

from __future__ import annotations

import re
from types import MappingProxyType
from typing import ClassVar, Final

from flext_tests import t
from flext_tests._constants._validator_parts.validator_part_02 import (
    FlextTestsConstantsValidator as FlextTestsConstantsValidatorPart02,
)


class FlextTestsConstantsValidator(FlextTestsConstantsValidatorPart02):
    """Architecture validator approved-pattern and layer constants."""

    ENFORCEMENT_WORKSPACE_MARKERS: Final[t.StrSequence] = (
        "AGENTS.md",
        "flext-core",
        "flext-tests",
    )
    VALIDATOR_EXCLUDE_PATTERNS: Final[t.StrSequence] = (
        "**/.venv/**",
        "**/venv/**",
        "**/__pycache__/**",
        "**/build/**",
        "**/dist/**",
        "**/.git/**",
        "**/htmlcov/**",
        "**/*.pyc",
    )
    VALIDATOR_INCLUDE_PATTERNS: Final[t.StrSequence] = ("**/*.py",)
    VALIDATOR_IMPORTS_KEY: Final[str] = "imports"
    VALIDATOR_TYPES_KEY: Final[str] = "types"
    VALIDATOR_TESTS_KEY: Final[str] = "tests"
    VALIDATOR_CONFIG_KEY: Final[str] = "settings"
    VALIDATOR_BYPASS_KEY: Final[str] = "bypass"
    VALIDATOR_LAYER_KEY: Final[str] = "layer"
    VALIDATOR_MARKDOWN_KEY: Final[str] = "markdown"
    VALIDATOR_APPROVED_CAST_SERVICE_PATTERN: Final[str] = "service\\.py$"
    VALIDATOR_APPROVED_CAST_CONTAINER_PATTERN: Final[str] = "container\\.py$"
    VALIDATOR_APPROVED_PRAGMA_PATTERN: Final[str] = "__init__\\.py$"
    VALIDATOR_APPROVED_INTERNAL_INIT_PATTERN: Final[str] = "_[^/]+/__init__\\.py$"
    VALIDATOR_APPROVED_CAST_SERVICE_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        VALIDATOR_APPROVED_CAST_SERVICE_PATTERN,
    )
    VALIDATOR_APPROVED_CAST_CONTAINER_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        VALIDATOR_APPROVED_CAST_CONTAINER_PATTERN,
    )
    VALIDATOR_APPROVED_PRAGMA_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        VALIDATOR_APPROVED_PRAGMA_PATTERN,
    )
    VALIDATOR_APPROVED_INTERNAL_INIT_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        VALIDATOR_APPROVED_INTERNAL_INIT_PATTERN,
    )
    VALIDATOR_APPROVED_PATH_REGEX_BY_PATTERN: ClassVar[
        t.MappingKV[str, t.Infra.RegexPattern]
    ] = MappingProxyType({
        VALIDATOR_APPROVED_CAST_SERVICE_PATTERN: VALIDATOR_APPROVED_CAST_SERVICE_RE,
        VALIDATOR_APPROVED_CAST_CONTAINER_PATTERN: VALIDATOR_APPROVED_CAST_CONTAINER_RE,
        VALIDATOR_APPROVED_PRAGMA_PATTERN: VALIDATOR_APPROVED_PRAGMA_RE,
        VALIDATOR_APPROVED_INTERNAL_INIT_PATTERN: VALIDATOR_APPROVED_INTERNAL_INIT_RE,
    })
    VALIDATOR_APPROVED_CAST_PATTERNS: Final[t.StrSequence] = (
        VALIDATOR_APPROVED_CAST_SERVICE_PATTERN,
        VALIDATOR_APPROVED_CAST_CONTAINER_PATTERN,
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
    VALIDATOR_APPROVED_PRAGMA_PATTERNS: Final[t.StrSequence] = (
        VALIDATOR_APPROVED_PRAGMA_PATTERN,
    )
    VALIDATOR_APPROVED_MOCK_NAMES: Final[frozenset[str]] = frozenset({
        "Mock",
        "MagicMock",
        "AsyncMock",
        "PropertyMock",
    })
    VALIDATOR_APPROVED_INTERNAL_INIT_PATTERNS: Final[t.StrSequence] = (
        VALIDATOR_APPROVED_INTERNAL_INIT_PATTERN,
    )
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
    def path_pattern_matches(cls, value: str, pattern: str) -> bool:
        """Check whether one validator path pattern matches value."""
        compiled_pattern = cls.VALIDATOR_APPROVED_PATH_REGEX_BY_PATTERN.get(pattern)
        return compiled_pattern.search(value) is not None if compiled_pattern else False

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


__all__: list[str] = ["FlextTestsConstantsValidator"]
