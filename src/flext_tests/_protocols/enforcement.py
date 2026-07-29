"""Enforcement protocols for flext_tests."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_infra import p
from flext_tests._constants.validator import FlextTestsConstantsValidator

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

    from flext_tests import t


class FlextTestsEnforcementProtocolsMixin:
    """Protocols for enforcement dispatch boundaries."""

    class PytestTimeoutPolicy(Protocol):
        """Read-only timeout decisions parsed from production config."""

        @property
        def required_configured_cap_count(self) -> int:
            """Required number of configured timeout caps."""
            ...

        @property
        def allow_timeout_func_only(self) -> bool:
            """Whether fixture setup and teardown may be excluded."""
            ...

        @property
        def timeout_owned_ini_keys(
            self,
        ) -> frozenset[FlextTestsConstantsValidator.PytestTimeoutIniKey]:
            """INI keys protected from runtime replacement."""
            ...

    class EnforcementRuleSource(Protocol):
        """Read-only source discriminator consumed by dispatch."""

        @property
        def kind(self) -> str:
            """Canonical source kind."""
            ...

    class EnforcementRuleSpec(Protocol):
        """Read-only enforcement rule consumed by flext-tests."""

        @property
        def id(self) -> str:
            """Stable rule identifier."""
            ...

        @property
        def description(self) -> str:
            """Human-readable rule description."""
            ...

        @property
        def severity(self) -> str:
            """Rule severity."""
            ...

        @property
        def source(self) -> FlextTestsEnforcementProtocolsMixin.EnforcementRuleSource:
            """Rule dispatch source."""
            ...

        @property
        def enabled(self) -> bool:
            """Whether the rule participates in enforcement."""
            ...

        @property
        def promote_to_error_when_strict(self) -> bool:
            """Whether strict mode promotes the runtime warning."""
            ...

    class EnforcementBuildContext(Protocol):
        """Read-only inputs shared by enforcement builders."""

        @property
        def infra_report(self) -> p.AttributeProbe | None:
            """Optional namespace report."""
            ...

        @property
        def validator_targets(self) -> tuple[Path, ...]:
            """Validator targets collected for the session."""
            ...

        @property
        def workspace_root(self) -> Path | None:
            """Resolved workspace root."""
            ...

    class EnforcementViolation(Protocol):
        """Read-only violation surface used by pytest items."""

        @property
        def rule_id(self) -> str:
            """Rule identifier."""
            ...

        @property
        def file_path(self) -> Path | str:
            """Offending file path."""
            ...

        @property
        def line_number(self) -> int:
            """One-based source line."""
            ...

    class EnforcementDispatcherConfig(Protocol):
        """Read-only shape consumed by the enforcement dispatcher."""

        @property
        def active(self) -> bool:
            """Whether enforcement is active."""
            ...

        @property
        def strict(self) -> bool:
            """Whether runtime warnings are promoted."""
            ...

        @property
        def include(self) -> frozenset[str]:
            """Rule identifiers explicitly included."""
            ...

        @property
        def exclude(self) -> frozenset[str]:
            """Rule identifiers explicitly excluded."""
            ...

        @property
        def workspace_root(self) -> Path | None:
            """Resolved workspace root."""
            ...

        @property
        def warning_counter(self) -> t.MutableIntMapping:
            """Captured warning counts by dotted category."""
            ...

    class EnforcementBuilder(ABC):
        """Callable contract implemented by enforcement contribution builders."""

        @abstractmethod
        def __call__(
            self,
            session: pytest.Session,
            cfg: FlextTestsEnforcementProtocolsMixin.EnforcementDispatcherConfig,
            rule: FlextTestsEnforcementProtocolsMixin.EnforcementRuleSpec,
            context: FlextTestsEnforcementProtocolsMixin.EnforcementBuildContext,
        ) -> list[pytest.Item]:
            """Build pytest items for one enforcement rule."""
            ...

    @runtime_checkable
    class NamespaceEnforcer(Protocol):
        """Runtime namespace enforcer contract consumed by test fixtures."""

        # NOTE (multi-agent, mro-wkii.17.21): Result wrapping belongs to the
        # flext-tests boundary; the external enforcer returns its report directly.
        def enforce(self, *, project_names: t.StrSequence) -> p.AttributeProbe:
            """Run namespace enforcement for the selected projects."""
            ...

    class NamespaceEnforcerFactory(Protocol):
        """Construct the external namespace enforcer boundary."""

        def __call__(
            self, *, workspace_root: Path
        ) -> FlextTestsEnforcementProtocolsMixin.NamespaceEnforcer:
            """Construct an enforcer for one workspace root."""
            ...
