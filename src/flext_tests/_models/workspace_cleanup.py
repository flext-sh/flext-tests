"""Typed workspace cleanup contracts for flext-tests consumers.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Literal

from flext_cli import m, u

if TYPE_CHECKING:
    from flext_core import t


class FlextTestsWorkspaceCleanupModelsMixin:
    """Immutable cleanup policy, plan, and execution report models."""

    class WorkspaceCleanupPolicy(m.Value):
        """Config-owned exact residue paths eligible for cleanup."""

        residues: Annotated[
            t.VariadicTuple[Path],
            u.Field(
                strict=False,
                description="Exact workspace-relative development residue paths.",
            ),
        ]

    class WorkspaceCleanupRequest(m.Value):
        """Runtime root composed with the original cleanup policy object."""

        repository_root: Annotated[
            Path,
            u.Field(strict=False, description="Exact Git workspace root."),
        ]
        policy: Annotated[
            FlextTestsWorkspaceCleanupModelsMixin.WorkspaceCleanupPolicy,
            u.Field(description="Original config-owned cleanup policy."),
        ]

    class WorkspaceCleanupCandidate(m.Value):
        """One validated ignored residue in a cleanup plan."""

        relative_path: Annotated[
            Path,
            u.Field(strict=False, description="Workspace-relative residue path."),
        ]
        path: Annotated[
            Path,
            u.Field(strict=False, description="Absolute lexical residue path."),
        ]
        kind: Annotated[
            Literal["file", "directory", "symlink"],
            u.Field(description="Observed filesystem kind during planning."),
        ]
        # NOTE (multi-agent): bind apply to the exact dry-run filesystem state.
        fingerprint: Annotated[
            str,
            u.Field(description="SHA-256 fingerprint of the planned residue tree."),
        ]

    class WorkspaceCleanupPlan(m.Value):
        """Deterministic dry-run plan retaining its source request."""

        request: Annotated[
            FlextTestsWorkspaceCleanupModelsMixin.WorkspaceCleanupRequest,
            u.Field(description="Original cleanup request."),
        ]
        candidates: Annotated[
            tuple[FlextTestsWorkspaceCleanupModelsMixin.WorkspaceCleanupCandidate, ...],
            u.Field(description="Sorted validated cleanup candidates."),
        ]

    class WorkspaceCleanupReport(m.Value):
        """Applied cleanup report retaining the exact validated plan."""

        plan: Annotated[
            FlextTestsWorkspaceCleanupModelsMixin.WorkspaceCleanupPlan,
            u.Field(description="Exact dry-run plan applied by the operation."),
        ]
        removed: Annotated[
            t.VariadicTuple[Path],
            u.Field(strict=False, description="Sorted paths removed successfully."),
        ]


__all__: t.VariadicTuple[str] = ("FlextTestsWorkspaceCleanupModelsMixin",)


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
