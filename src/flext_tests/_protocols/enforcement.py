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

    class EnforcementBuildContext(Protocol):
        """Shared context contract passed to enforcement contribution builders.

        Members are read-only (covariant) so a concrete context exposing
        ``validator_targets: tuple[Path, ...]`` satisfies ``Sequence[Path]``.
        """

        @property
        def infra_report(self) -> p.AttributeProbe | None:
            """Optional infra namespace report shared with builders."""
            ...

        @property
        def validator_targets(self) -> t.SequenceOf[Path]:
            """Validator target paths collected for the current session."""
            ...

        @property
        def workspace_root(self) -> Path | None:
            """Resolved workspace root when discovery succeeded."""
            ...

    class EnforcementBuilder(ABC):
        """Callable contract implemented by enforcement contribution builders."""

        @abstractmethod
        def __call__(
            self,
            session: pytest.Session,
            cfg: m.Tests.EnforcementDispatcherConfig,
            rule: m.EnforcementRuleSpec,
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
