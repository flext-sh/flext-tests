"""Enforcement protocols for flext_tests."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import MutableMapping
    from pathlib import Path

    import pytest

    from flext_infra import p
    from flext_tests import t


class FlextTestsEnforcementProtocolsMixin:
    """Protocols for enforcement dispatch boundaries."""

    @runtime_checkable
    class EnforcementBuildContext(Protocol):
        """Immutable inputs shared by enforcement contribution builders."""

        @property
        def infra_report(self) -> p.AttributeProbe | None: ...

        @property
        def validator_targets(self) -> tuple[Path, ...]: ...

        @property
        def workspace_root(self) -> Path | None: ...

    @runtime_checkable
    class EnforcementDispatcherConfig(Protocol):
        """Resolved runtime configuration for enforcement dispatch."""

        @property
        def active(self) -> bool: ...

        @property
        def strict(self) -> bool: ...

        @property
        def include(self) -> frozenset[str]: ...

        @property
        def exclude(self) -> frozenset[str]: ...

        @property
        def workspace_root(self) -> Path | None: ...

        @property
        def warning_counter(self) -> MutableMapping[str, int]: ...

    class EnforcementBuilder(ABC):
        """Callable contract implemented by enforcement contribution builders."""

        @abstractmethod
        def __call__(
            self,
            session: pytest.Session,
            cfg: FlextTestsEnforcementProtocolsMixin.EnforcementDispatcherConfig,
            rule: p.EnforcementRuleSpec,
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
