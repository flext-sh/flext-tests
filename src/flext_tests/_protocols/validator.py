# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_tests/_protocols/validator
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableMapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flext_cli import p, t


class FlextTestsProtocolsValidator:
    """Own the structural model contracts declared by this module."""

    @runtime_checkable
    class EnforcementInfraRuleSource(Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def kind(self) -> Literal["flext_infra_rule"]: ...
        @property
        def rule_ids(self) -> Sequence[str]: ...

    @runtime_checkable
    class EnforcementRuntimeWarningSource(Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def kind(self) -> Literal["runtime_warning"]: ...
        @property
        def category(self) -> t.NonEmptyStr: ...

    @runtime_checkable
    class EnforcementRuleSpec(Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def id(self) -> t.NonEmptyStr: ...
        @property
        def description(self) -> str: ...
        @property
        def source(
            self,
        ) -> (
            FlextTestsProtocolsValidator.EnforcementInfraRuleSource
            | FlextTestsProtocolsValidator.EnforcementRuntimeWarningSource
        ): ...

    @runtime_checkable
    class EnforcementCatalog(Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def rules(
            self,
        ) -> tuple[FlextTestsProtocolsValidator.EnforcementRuleSpec, ...]: ...

    @runtime_checkable
    class EnforcementBuildContext(Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def infra_findings(self) -> t.Port[p.Model] | None: ...
        @property
        def project_names(self) -> frozenset[str]: ...

    @runtime_checkable
    class EnforcementDispatcherConfig(Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def strict(self) -> bool: ...
        @property
        def include(self) -> frozenset[str]: ...
        @property
        def exclude(self) -> frozenset[str]: ...
        @property
        def repository_root(self) -> Path | None: ...
        @property
        def warning_counter(self) -> MutableMapping[str, int]: ...

    @runtime_checkable
    class EnforcementViolation(Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def rule_id(self) -> str: ...
        @property
        def severity(self) -> str: ...
        @property
        def description(self) -> str: ...
        @property
        def project(self) -> str: ...
        @property
        def violations(self) -> tuple[str, ...]: ...


__all__: list[str] = [
    "FlextTestsProtocolsValidator",
]
