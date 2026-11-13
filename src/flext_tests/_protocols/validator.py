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

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_cli import p

    from flext_tests import t


class FlextTestsProtocolsValidator:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class EnforcementInfraRuleSource(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def kind(self) -> Literal["flext_infra_rule"]:
            """Closed discriminator of the declarative rule source."""
            ...

        @property
        def rule_ids(self) -> Sequence[str]:
            """Engine rule IDs this catalog entry selects."""
            ...

    @runtime_checkable
    class EnforcementRuntimeWarningSource(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def kind(self) -> Literal["runtime_warning"]:
            """Closed discriminator of the runtime warning source."""
            ...

        @property
        def category(self) -> t.NonEmptyStr:
            """Dotted warning category the dispatcher filters."""
            ...

    @runtime_checkable
    class EnforcementRuleSpec(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def id(self) -> t.NonEmptyStr:
            """Canonical catalog rule ID."""
            ...

        @property
        def description(self) -> str:
            """Human-readable catalog rule description."""
            ...

        @property
        def source(
            self,
        ) -> (
            FlextTestsProtocolsValidator.EnforcementInfraRuleSource
            | FlextTestsProtocolsValidator.EnforcementRuntimeWarningSource
        ):
            """Closed rule source behind this catalog entry."""
            ...

    @runtime_checkable
    class EnforcementCatalog(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def rules(self) -> tuple[FlextTestsProtocolsValidator.EnforcementRuleSpec, ...]:
            """Canonical catalog rules in composed order."""
            ...

    @runtime_checkable
    class EnforcementBuildContext(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def infra_findings(self) -> p.BaseModel | None:
            """Structural member projected from the owning model.

            flext-infra rule-engine findings keyed by rule id, absent when no engine
            rule is selected.
            """
            ...

        @property
        def project_names(self) -> frozenset[str]:
            """FLEXT projects represented by collected items."""
            ...

    @runtime_checkable
    class EnforcementDispatcherConfig(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def strict(self) -> bool:
            """Promote runtime warnings to failures when true."""
            ...

        @property
        def include(self) -> frozenset[str]:
            """Optional allow-list of enforcement rule IDs."""
            ...

        @property
        def exclude(self) -> frozenset[str]:
            """Optional block-list of enforcement rule IDs."""
            ...

        @property
        def repository_root(self) -> Path | None:
            """Resolved FLEXT workspace root for the session."""
            ...

        @property
        def catalog_root(self) -> Path | None:
            """Structural member projected from the owning model.

            Repository pytest collects; flext-infra plans one repository at a time,
            so the rule catalog is planned here.
            """
            ...

        @property
        def warning_counter(self) -> MutableMapping[str, int]:
            """Captured runtime warning counts keyed by dotted category."""
            ...

    @runtime_checkable
    class EnforcementViolation(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def rule_id(self) -> str:
            """Enforcement rule ID the findings belong to."""
            ...

        @property
        def severity(self) -> str:
            """Severity declared by the finding payload."""
            ...

        @property
        def description(self) -> str:
            """Human-readable finding message of the first hit."""
            ...

        @property
        def project(self) -> str:
            """FLEXT project the findings belong to."""
            ...

        @property
        def violations(self) -> tuple[str, ...]:
            """Formatted per-finding lines for the failure body."""
            ...


__all__: list[str] = [
    "FlextTestsProtocolsValidator",
]
