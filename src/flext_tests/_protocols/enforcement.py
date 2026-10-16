"""Enforcement protocols for flext_tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol, Self, runtime_checkable

from flext_cli import p

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    import pytest

    from flext_tests import m, t


class FlextTestsEnforcementProtocolsMixin:
    """Protocols for enforcement dispatch boundaries."""

    class EnforcementItemFactory[T](Protocol):
        """Bound pytest ``from_parent`` contract for violation items."""

        def __call__(
            self,
            *,
            parent: pytest.Collector,
            name: str,
            violation: m.Tests.EnforcementViolation,
        ) -> T:
            """Construct an item through pytest's public node factory."""
            ...

    class EnforcementCollectorFactory[T](Protocol):
        """Bound pytest ``from_parent`` contract for session collectors."""

        def __call__(self, *, parent: pytest.Session, name: str) -> T:
            """Construct a collector through pytest's public node factory."""
            ...

    class EnforcementBuilder(ABC):
        """Callable contract implemented by enforcement contribution builders."""

        @abstractmethod
        def __call__(
            self,
            session: pytest.Session,
            cfg: m.Tests.EnforcementDispatcherConfig,
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

    @runtime_checkable
    class NamespaceEnforcerFactory(Protocol):
        """Construct the external namespace enforcer boundary."""

        def __call__(
            self,
            *,
            repository_root: Path,
        ) -> FlextTestsEnforcementProtocolsMixin.NamespaceEnforcer:
            """Construct an enforcer for one workspace root."""
            ...

    @runtime_checkable
    class EnforcementScanFinding(Protocol):
        """One rule-engine finding, as the enforcement dispatcher reads it."""

        @property
        def rule_id(self) -> str:
            """Rule that produced the finding."""
            ...

        @property
        def repository(self) -> str:
            """Project whose tree holds the finding."""
            ...

        @property
        def file(self) -> Path:
            """Workspace-relative finding path."""
            ...

        @property
        def text(self) -> str:
            """Exact matched source text."""
            ...

        @property
        def severity(self) -> str:
            """Severity supplied by the native rule result."""
            ...

        @property
        def message(self) -> str | None:
            """Native finding message, when supplied by the producer."""
            ...

    @runtime_checkable
    class EnforcementScanReport(Protocol):
        """Rule-engine findings consumed by the enforcement dispatcher.

        The engine's report satisfies it structurally, so the shared test
        models never import the engine's model family to type this field.
        """

        @property
        def entries(
            self,
        ) -> Sequence[FlextTestsEnforcementProtocolsMixin.EnforcementScanFinding]:
            """Every finding in stable order."""
            ...


class FlextTestsEnforcementItemNodeMixin:
    """Typed node boundary mixin for violation items.

    ``pytest.Item.from_parent`` is unannotated upstream (its ``**kw`` forward
    is ``Unknown``), so enforcement items inherit this mixin to record the
    typed public factory contract; at runtime the attribute still resolves to
    pytest's own ``from_parent`` through the MRO.
    """

    if TYPE_CHECKING:
        from_parent: FlextTestsEnforcementProtocolsMixin.EnforcementItemFactory[Self]


class FlextTestsEnforcementCollectorNodeMixin:
    """Typed node boundary mixin for session collectors.

    ``pytest.Collector.from_parent`` is unannotated upstream, so enforcement
    collectors inherit this mixin to record the typed public factory
    contract; at runtime the attribute still resolves to pytest's own
    ``from_parent`` through the MRO.
    """

    if TYPE_CHECKING:
        from_parent: FlextTestsEnforcementProtocolsMixin.EnforcementCollectorFactory[
            Self
        ]
