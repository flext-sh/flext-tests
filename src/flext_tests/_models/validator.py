"""Enforcement dispatch models for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableMapping
from pathlib import Path
from typing import Annotated, ClassVar

from flext_cli import m, p, u


class FlextTestsValidatorModelsMixin:
    class EnforcementBuildContext(m.ArbitraryTypesModel):
        """Validated immutable inputs shared by enforcement item builders."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(frozen=True)

        infra_findings: Annotated[
            p.Model | None,
            u.Field(
                description="flext-infra rule-engine findings keyed by rule id, "
                "absent when no engine rule is selected.",
            ),
        ] = None
        project_names: Annotated[
            frozenset[str],
            u.Field(description="FLEXT projects represented by collected items."),
        ] = frozenset()

    class EnforcementDispatcherConfig(m.Value):
        """Resolved runtime configuration for the pytest enforcement dispatcher."""

        strict: Annotated[
            bool,
            u.Field(description="Promote runtime warnings to failures when true."),
        ]
        include: Annotated[
            frozenset[str],
            u.Field(description="Optional allow-list of enforcement rule IDs."),
        ] = frozenset()
        exclude: Annotated[
            frozenset[str],
            u.Field(description="Optional block-list of enforcement rule IDs."),
        ] = frozenset()
        repository_root: Annotated[
            Path | None,
            u.Field(description="Resolved FLEXT workspace root for the session."),
        ] = None
        warning_counter: Annotated[
            MutableMapping[str, int],
            u.Field(
                description="Captured runtime warning counts keyed by dotted category.",
            ),
        ] = u.Field(default_factory=dict)
