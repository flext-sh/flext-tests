"""Enforcement protocols for flext_tests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_infra import p

if TYPE_CHECKING:
    from flext_tests import t


class FlextTestsEnforcementProtocolsMixin:
    """Protocols for enforcement dispatch boundaries."""

    @runtime_checkable
    class NamespaceEnforcer(Protocol):
        """Runtime namespace enforcer contract consumed by test fixtures."""

        def enforce(
            self,
            *,
            project_names: t.StrSequence,
        ) -> p.Result[p.AttributeProbe]:
            """Run namespace enforcement for the selected projects."""
            ...
