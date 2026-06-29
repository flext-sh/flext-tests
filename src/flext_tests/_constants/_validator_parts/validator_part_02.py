"""Validator message and regex constants for flext-tests."""

from __future__ import annotations

import re
from typing import ClassVar, Final

from flext_tests import t
from flext_tests._constants._validator_parts.validator_part_01 import (
    FlextTestsConstantsValidator as FlextTestsConstantsValidatorPart01,
)


class FlextTestsConstantsValidator(FlextTestsConstantsValidatorPart01):
    """Architecture validator message and regex constants."""

    VALIDATOR_MSG_LAYER_VIOLATION: Final[str] = (
        "'{current}' L{current_level} -> '{imported}' L{imported_level}"
    )
    VALIDATOR_MSG_CONFIG_IGNORE: Final[str] = (
        "ignore_errors = true for module '{module}'"
    )
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
    VALIDATOR_TYPE_IGNORE_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"#\s*type:\s*ignore",
    )
    VALIDATOR_NOQA_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"#\s*noqa",
        re.IGNORECASE,
    )
    VALIDATOR_PRAGMA_NO_COVER_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"#\s*pragma:\s*no\s*cover",
        re.IGNORECASE,
    )
    VALIDATOR_CAST_USAGE_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"\b(?:typing\.)?cast\s*\(",
    )
    VALIDATOR_LEGACY_FACTORY_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"\b(?P<name>ParamSpec|TypeVar)\s*\(",
    )
    VALIDATOR_TYPE_ALIAS_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r":\s*(?:typing\.)?TypeAlias\b",
    )
    VALIDATOR_GENERIC_BASE_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*class\s+\w+\s*\([^)]*\b(?:typing\.)?Generic\s*\[",
    )
    VALIDATOR_LEGACY_ANNOTATION_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"(?:[:(,]\s*|->\s*)(?:typing\.)?(?P<name>Dict|FrozenSet|List|Optional|Set|Tuple|TypeAliasType|TypeGuard|Union)\b",
    )
    VALIDATOR_FUNCTION_DEF_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*(?:async\s+def|def)\s+(?P<name>[A-Za-z_]\w*)",
    )
    VALIDATOR_ANY_ARG_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"(?P<arg>[A-Za-z_]\w*)\s*:\s*(?:typing\.)?Any\b",
    )
    VALIDATOR_ANY_RETURN_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"->\s*(?:typing\.)?Any\b",
    )
    VALIDATOR_ANY_VAR_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*[A-Za-z_]\w*\s*:\s*(?:typing\.)?Any\b",
    )
    VALIDATOR_OBJECT_ARG_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"(?P<arg>[A-Za-z_]\w*)\s*:\s*(?:builtins\.)?object\b",
    )
    VALIDATOR_OBJECT_RETURN_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"->\s*(?:builtins\.)?object\b",
    )
    VALIDATOR_OBJECT_VAR_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*[A-Za-z_]\w*\s*:\s*(?:builtins\.)?object\b",
    )
    VALIDATOR_BOOL_IS_HELPER_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*(?:async\s+def|def)\s+(?P<name>is_[A-Za-z_]\w*)\b.*->\s*bool\b",
    )
    VALIDATOR_INDENTED_IMPORT_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]+(?:from\s+\S+\s+import\b|import\s+\S+)",
    )
    VALIDATOR_IMPORT_ERROR_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*except\b.*\b(?:ImportError|ModuleNotFoundError)\b.*:\s*(?:#.*)?$",
    )
    VALIDATOR_BARE_EXCEPT_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*except\s*:\s*(?:#.*)?$",
    )
    VALIDATOR_EXCEPT_HEADER_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^(?P<indent>[ \t]*)except\b.*:\s*(?:#.*)?$",
    )
    VALIDATOR_PASS_OR_ELLIPSIS_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^(?:pass|\.\.\.)\s*(?:#.*)?$",
    )
    VALIDATOR_SYS_PATH_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"\bsys\.path(?:\s*\[|\.(?:append|extend|insert|pop|remove)\s*\()",
    )
    VALIDATOR_FLEXT_FROM_IMPORT_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*from\s+(?P<module>flext_[A-Za-z0-9_.]+)\s+import\b",
    )
    VALIDATOR_FLEXT_IMPORT_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*import\s+(?P<module>flext_[A-Za-z0-9_.]+)\b",
    )
    VALIDATOR_FROM_IMPORT_LINE_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*from\s+(?P<module>\.*[A-Za-z_][\w.]*)\s+import\s+(?P<names>[^#]+)",
    )
    VALIDATOR_IMPORT_LINE_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*import\s+(?P<modules>[^#]+)",
    )
    VALIDATOR_MONKEYPATCH_ACCESS_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"\bmonkeypatch\.(?P<attr>[A-Za-z_]\w*)\b",
    )
    VALIDATOR_MOCK_CALL_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"\b(?P<name>AsyncMock|MagicMock|Mock|PropertyMock)\s*\(",
    )
    VALIDATOR_PATCH_DECORATOR_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^[ \t]*@(?:[A-Za-z_]\w*\.)*patch(?:\b|\s*\(|\.)",
    )
    VALIDATOR_MD_OPTION_DOCS: Final[str] = "--markdown-docs"
    VALIDATOR_MD_PYTHON_BLOCK_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
        r"^```python\s*$\n(.*?)^```\s*$",
        re.MULTILINE | re.DOTALL,
    )
    VALIDATOR_MD_OBJECT_ANNOTATION_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
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


__all__: list[str] = ["FlextTestsConstantsValidator"]
