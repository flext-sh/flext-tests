"""Validator rule constants for flext-tests."""

from __future__ import annotations

from enum import StrEnum, unique
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from flext_infra import t


class FlextTestsConstantsValidator:
    """Architecture validator rule constants."""

    @unique
    class ValidatorSeverity(StrEnum):
        """Violation severity levels."""

        CRITICAL = "CRITICAL"
        HIGH = "HIGH"
        MEDIUM = "MEDIUM"
        LOW = "LOW"

    VALIDATOR_RULE_IMPORT_001: Final[t.StrPair] = (
        "HIGH",
        "Lazy import (not at module top)",
    )
    VALIDATOR_RULE_IMPORT_002: Final[t.StrPair] = (
        "HIGH",
        "TYPE_CHECKING block detected",
    )
    VALIDATOR_RULE_IMPORT_003: Final[t.StrPair] = (
        "HIGH",
        "try/except ImportError pattern",
    )
    VALIDATOR_RULE_IMPORT_004: Final[t.StrPair] = (
        "CRITICAL",
        "sys.path manipulation",
    )
    VALIDATOR_RULE_IMPORT_005: Final[t.StrPair] = (
        "MEDIUM",
        "Direct technology import (should use facade)",
    )
    VALIDATOR_RULE_IMPORT_006: Final[t.StrPair] = (
        "HIGH",
        "Non-root import from flext-* package",
    )
    VALIDATOR_RULE_TYPE_001: Final[t.StrPair] = (
        "CRITICAL",
        "type suppression comment",
    )
    VALIDATOR_RULE_TYPE_002: Final[t.StrPair] = (
        "CRITICAL",
        "wildcard type annotation",
    )
    VALIDATOR_RULE_TYPE_003: Final[t.StrPair] = ("MEDIUM", "Unapproved  usage")
    VALIDATOR_RULE_TYPE_004: Final[t.StrPair] = (
        "CRITICAL",
        "legacy typing factory or generic syntax",
    )
    VALIDATOR_RULE_TYPE_005: Final[t.StrPair] = (
        "CRITICAL",
        "legacy typing annotation form",
    )
    VALIDATOR_RULE_TYPE_006: Final[t.StrPair] = (
        "CRITICAL",
        "forbidden object annotation",
    )
    VALIDATOR_RULE_TYPE_007: Final[t.StrPair] = (
        "HIGH",
        "bool-returning is_* helper",
    )
    VALIDATOR_RULE_TEST_001: Final[t.StrPair] = (
        "HIGH",
        "monkeypatch usage detected",
    )
    VALIDATOR_RULE_TEST_002: Final[t.StrPair] = (
        "HIGH",
        "Mock/MagicMock usage detected",
    )
    VALIDATOR_RULE_TEST_003: Final[t.StrPair] = (
        "HIGH",
        "@patch decorator usage detected",
    )
    VALIDATOR_RULE_CONFIG_001: Final[t.StrPair] = (
        "CRITICAL",
        "mypy ignore_errors = true",
    )
    VALIDATOR_RULE_CONFIG_002: Final[t.StrPair] = (
        "HIGH",
        "Custom ruff ignore beyond approved list",
    )
    VALIDATOR_RULE_CONFIG_003: Final[t.StrPair] = (
        "MEDIUM",
        "disallow_incomplete_defs = false",
    )
    VALIDATOR_RULE_CONFIG_004: Final[t.StrPair] = (
        "MEDIUM",
        "warn_return_any = false",
    )
    VALIDATOR_RULE_CONFIG_005: Final[t.StrPair] = (
        "LOW",
        "reportPrivateUsage = false",
    )
    VALIDATOR_RULE_BYPASS_001: Final[t.StrPair] = (
        "MEDIUM",
        "noqa comment detected",
    )
    VALIDATOR_RULE_BYPASS_002: Final[t.StrPair] = (
        "LOW",
        "pragma: no cover (unapproved)",
    )
    VALIDATOR_RULE_BYPASS_003: Final[t.StrPair] = (
        "HIGH",
        "Exception swallowing (bare except or pass)",
    )
    VALIDATOR_RULE_LAYER_001: Final[t.StrPair] = (
        "CRITICAL",
        "Lower layer importing upper layer",
    )
    VALIDATOR_RULE_MD_001: Final[t.StrPair] = (
        "CRITICAL",
        "Python syntax error in markdown code block",
    )
    VALIDATOR_RULE_MD_002: Final[t.StrPair] = (
        "CRITICAL",
        "Forbidden typing import in markdown code block",
    )
    VALIDATOR_RULE_MD_003: Final[t.StrPair] = (
        "MEDIUM",
        "Missing future annotations in markdown code block",
    )
    VALIDATOR_RULE_MD_004: Final[t.StrPair] = (
        "HIGH",
        "Forbidden type annotation in markdown code block",
    )

    @classmethod
    def validator_rule(cls, rule_id: str) -> t.StrPair:
        """Get rule by ID string."""
        attr_name = "VALIDATOR_RULE_" + rule_id.replace("-", "_")
        rule: t.StrPair = getattr(cls, attr_name)
        return rule


__all__: list[str] = ["FlextTestsConstantsValidator"]
