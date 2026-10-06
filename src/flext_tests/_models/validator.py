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

    class EnforcementViolation(m.Value):
        """One grouped ``(rule_id, project)`` enforcement violation payload."""

        rule_id: Annotated[
            str,
            u.Field(description="Enforcement rule ID the findings belong to."),
        ]
        severity: Annotated[
            str,
            u.Field(description="Severity declared by the finding payload."),
        ]
        description: Annotated[
            str,
            u.Field(description="Human-readable finding message of the first hit."),
        ]
        project: Annotated[
            str,
            u.Field(description="FLEXT project the findings belong to."),
        ]
        violations: Annotated[
            tuple[str, ...],
            u.Field(description="Formatted per-finding lines for the failure body."),
        ] = ()


# NOTE (import discipline): nested models annotate through sibling modules and
# TYPE_CHECKING-only imports whose names are invisible to a nested class body;
# complete them here against the merged namespace (own globals + base module +
# package aliases), tolerating the rare still-unresolvable annotation (it
# stays deferred exactly as before instead of crashing the import).
import sys as _sys

_rebuild_ns: dict = dict(globals())
try:
    _rebuild_ns.update(vars(_sys.modules["flext_tests._models.base"]))
except KeyError:
    pass
for _alias in ("t", "p", "m", "u", "c", "r", "s", "x"):
    try:
        _rebuild_ns.setdefault(_alias, getattr(_sys.modules["flext_tests"], _alias))
    except AttributeError:
        pass

for _mixin_name in tuple(globals()):
    _mixin = globals().get(_mixin_name)
    if isinstance(_mixin, type) and _mixin_name.endswith("ModelsMixin"):
        for _member in tuple(vars(_mixin).values()):
            if isinstance(_member, type) and hasattr(_member, "model_rebuild"):
                _member.model_rebuild(_types_namespace=_rebuild_ns, raise_errors=False)
