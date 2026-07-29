"""Enforcement protocols for flext_tests."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_infra import p

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

    from flext_tests import m, t


class FlextTestsEnforcementProtocolsMixin:
    """Protocols for enforcement dispatch boundaries."""

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
            rule: m.EnforcementRuleSpec,
            context: m.Tests.EnforcementBuildContext,
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
