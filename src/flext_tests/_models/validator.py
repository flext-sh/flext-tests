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


# NOTE (import discipline): nested param models annotate through their
# enclosing mixin and through sibling mixins (TYPE_CHECKING-only imports)
# that are not yet bound while the class body executes — pydantic defers
# those models and its lazy rebuild resolves against the CALLING module's
# imports, which breaks consumers whose test modules import neither.
# Rebuild every nested model deterministically against the merged namespace
# of this module and every already-imported _models sibling.
import sys as _sys

_rebuild_ns = {
    k: v
    for _mod_name, _mod in tuple(_sys.modules.items())
    if _mod is not None
    and _mod_name in ("flext_tests",) or _mod_name.startswith("flext_tests._models.")
    for k, v in vars(_mod).items()
    if k.endswith("ModelsMixin") or k in ("t", "p", "m", "u", "c", "r", "s", "x")
}
_rebuild_ns.update(
    {
        k: v
        for k, v in vars(_sys.modules[__name__]).items()
        if k.endswith("ModelsMixin") or k in ("t", "p", "m", "u", "c", "r")
    },
)
for _mixin_name, _mixin in tuple(vars(_sys.modules[__name__]).items()):
    if not isinstance(_mixin, type) or not _mixin_name.endswith("ModelsMixin"):
        continue
    _rebuild_ns[_mixin_name] = _mixin
    for _member in tuple(vars(_mixin).values()):
        if isinstance(_member, type) and hasattr(_member, "model_rebuild"):
            _member.model_rebuild(_types_namespace=_rebuild_ns)
