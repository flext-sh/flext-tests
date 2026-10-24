"""Enforcement dispatch models for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableMapping
from pathlib import Path
from typing import Annotated, ClassVar

from flext_cli import m, p, t


def _warning_counter_default() -> MutableMapping[str, int]:
    """Create the typed empty runtime-warning counter.

    Returns:
        The resulting ``MutableMapping[str, int]``.

    """
    return {}


class FlextTestsValidatorModelsMixin:
    class EnforcementBuildContext(m.ArbitraryTypesModel):
        """Validated immutable inputs shared by enforcement item builders."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(frozen=True)

        infra_findings: Annotated[
            t.Port[p.Model] | None,
            m.Field(
                description="flext-infra rule-engine findings keyed by rule id, "
                "absent when no engine rule is selected.",
            ),
        ] = None
        project_names: Annotated[
            frozenset[str],
            m.Field(description="FLEXT projects represented by collected items."),
        ] = frozenset()

    class EnforcementDispatcherConfig(m.Value):
        """Resolved runtime configuration for the pytest enforcement dispatcher."""

        strict: Annotated[
            bool,
            m.Field(description="Promote runtime warnings to failures when true."),
        ]
        include: Annotated[
            frozenset[str],
            m.Field(description="Optional allow-list of enforcement rule IDs."),
        ] = frozenset()
        exclude: Annotated[
            frozenset[str],
            m.Field(description="Optional block-list of enforcement rule IDs."),
        ] = frozenset()
        repository_root: Annotated[
            Path | None,
            m.Field(description="Resolved FLEXT workspace root for the session."),
        ] = None
        warning_counter: Annotated[
            MutableMapping[str, int],
            m.Field(
                description="Captured runtime warning counts keyed by dotted category.",
            ),
        ] = m.Field(default_factory=_warning_counter_default)

    class EnforcementViolation(m.Value):
        """One grouped ``(rule_id, project)`` enforcement violation payload."""

        rule_id: Annotated[
            str,
            m.Field(description="Enforcement rule ID the findings belong to."),
        ]
        severity: Annotated[
            str,
            m.Field(description="Severity declared by the finding payload."),
        ]
        description: Annotated[
            str,
            m.Field(description="Human-readable finding message of the first hit."),
        ]
        project: Annotated[
            str,
            m.Field(description="FLEXT project the findings belong to."),
        ]
        violations: Annotated[
            tuple[str, ...],
            m.Field(description="Formatted per-finding lines for the failure body."),
        ] = ()


__all__: list[str] = ["FlextTestsValidatorModelsMixin"]
