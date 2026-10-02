"""Enforcement dispatch constants for flext-tests (data-only facade)."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from flext_infra import t


class FlextTestsConstantsValidator:
    """Workspace discovery and engine-finding keys of the enforcement dispatch."""

    ENFORCEMENT_WORKSPACE_MARKERS: ClassVar[t.StrSequence] = (
        "AGENTS.md",
        "flext-core",
        "flext-tests",
    )
    ENFORCEMENT_PROJECT_PREFIX: ClassVar[str] = "flext-"
    VALIDATOR_EXCLUDE_PATTERNS: ClassVar[t.StrSequence] = (
        "**/.venv/**",
        "**/venv/**",
        "**/__pycache__/**",
        "**/build/**",
        "**/dist/**",
        "**/.git/**",
        "**/htmlcov/**",
        "**/*.pyc",
        "**/.hypothesis/**",
    )
    VALIDATOR_INCLUDE_PATTERNS: ClassVar[t.StrSequence] = ("**/*.py",)
    VALIDATOR_IMPORTS_KEY: ClassVar[str] = "imports"
    VALIDATOR_TYPES_KEY: ClassVar[str] = "types"
    VALIDATOR_TESTS_KEY: ClassVar[str] = "tests"
    VALIDATOR_CONFIG_KEY: ClassVar[str] = "settings"
    VALIDATOR_BYPASS_KEY: ClassVar[str] = "bypass"
    VALIDATOR_LAYER_KEY: ClassVar[str] = "layer"
    VALIDATOR_MARKDOWN_KEY: ClassVar[str] = "markdown"
    VALIDATOR_APPROVED_CAST_SERVICE_PATTERN: ClassVar[str] = "service\\.py$"
    VALIDATOR_APPROVED_CAST_CONTAINER_PATTERN: ClassVar[str] = "container\\.py$"
    VALIDATOR_APPROVED_PRAGMA_PATTERN: ClassVar[str] = "__init__\\.py$"
    VALIDATOR_APPROVED_INTERNAL_INIT_PATTERN: ClassVar[str] = "_[^/]+/__init__\\.py$"
    VALIDATOR_APPROVED_PROTOCOLS_PATTERN: ClassVar[str] = (
        "protocols/(brand|domain)\\.py$"
    )
    VALIDATOR_APPROVED_CAST_SERVICE_RE: ClassVar[t.RegexPattern] = re.compile(
        VALIDATOR_APPROVED_CAST_SERVICE_PATTERN
    )
    VALIDATOR_APPROVED_CAST_CONTAINER_RE: ClassVar[t.RegexPattern] = re.compile(
        VALIDATOR_APPROVED_CAST_CONTAINER_PATTERN
    )
    VALIDATOR_APPROVED_PRAGMA_RE: ClassVar[t.RegexPattern] = re.compile(
        VALIDATOR_APPROVED_PRAGMA_PATTERN
    )
    VALIDATOR_APPROVED_INTERNAL_INIT_RE: ClassVar[t.RegexPattern] = re.compile(
        VALIDATOR_APPROVED_INTERNAL_INIT_PATTERN
    )
    VALIDATOR_APPROVED_PROTOCOLS_RE: ClassVar[t.RegexPattern] = re.compile(
        VALIDATOR_APPROVED_PROTOCOLS_PATTERN
    )
    VALIDATOR_APPROVED_PATH_REGEX_BY_PATTERN: ClassVar[
        t.MappingKV[str, t.RegexPattern]
    ] = MappingProxyType({
        VALIDATOR_APPROVED_CAST_SERVICE_PATTERN: VALIDATOR_APPROVED_CAST_SERVICE_RE,
        VALIDATOR_APPROVED_CAST_CONTAINER_PATTERN: VALIDATOR_APPROVED_CAST_CONTAINER_RE,
        VALIDATOR_APPROVED_PRAGMA_PATTERN: VALIDATOR_APPROVED_PRAGMA_RE,
        VALIDATOR_APPROVED_INTERNAL_INIT_PATTERN: VALIDATOR_APPROVED_INTERNAL_INIT_RE,
        VALIDATOR_APPROVED_PROTOCOLS_PATTERN: VALIDATOR_APPROVED_PROTOCOLS_RE,
    })
    VALIDATOR_APPROVED_CAST_PATTERNS: ClassVar[t.StrSequence] = (
        VALIDATOR_APPROVED_CAST_SERVICE_PATTERN,
        VALIDATOR_APPROVED_CAST_CONTAINER_PATTERN,
    )
    VALIDATOR_LEGACY_FACTORY_NAMES: ClassVar[frozenset[str]] = frozenset({
        "ParamSpec",
        "TypeAlias",
        "TypeVar",
    })
    VALIDATOR_LEGACY_BASE_NAMES: ClassVar[frozenset[str]] = frozenset({"Generic"})
    VALIDATOR_LEGACY_ANNOTATION_NAMES: ClassVar[frozenset[str]] = frozenset({
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
    VALIDATOR_APPROVED_PRAGMA_PATTERNS: ClassVar[t.StrSequence] = (
        VALIDATOR_APPROVED_PRAGMA_PATTERN,
    )
    VALIDATOR_APPROVED_MOCK_NAMES: ClassVar[frozenset[str]] = frozenset({
        "Mock",
        "MagicMock",
        "AsyncMock",
        "PropertyMock",
    })
    VALIDATOR_APPROVED_INTERNAL_INIT_PATTERNS: ClassVar[t.StrSequence] = (
        VALIDATOR_APPROVED_INTERNAL_INIT_PATTERN,
    )
    LAYER_CONSTANTS: ClassVar[int] = 0
    LAYER_TYPINGS: ClassVar[int] = 0
    LAYER_PROTOCOLS: ClassVar[int] = 0
    LAYER_CONFIG: ClassVar[int] = 1
    LAYER_RUNTIME: ClassVar[int] = 2
    LAYER_EXCEPTIONS: ClassVar[int] = 3
    LAYER_RESULT: ClassVar[int] = 3
    LAYER_LOGGINGS: ClassVar[int] = 4
    LAYER_MODELS: ClassVar[int] = 5
    LAYER_UTILITIES: ClassVar[int] = 5
    LAYER_MIXINS: ClassVar[int] = 5
    LAYER_CONTAINER: ClassVar[int] = 6
    LAYER_SERVICE: ClassVar[int] = 6
    LAYER_CONTEXT: ClassVar[int] = 6
    LAYER_HANDLERS: ClassVar[int] = 7
    LAYER_DISPATCHER: ClassVar[int] = 8
    LAYER_REGISTRY: ClassVar[int] = 8
    LAYER_DECORATORS: ClassVar[int] = 9
    ENFORCEMENT_FINDING_SEVERITY_KEY: ClassVar[str] = "severity"
    """ast-grep JSON finding key carrying the rule severity."""
    ENFORCEMENT_FINDING_MESSAGE_KEY: ClassVar[str] = "message"
    """ast-grep JSON finding key carrying the rule message."""


__all__: list[str] = ["FlextTestsConstantsValidator"]
