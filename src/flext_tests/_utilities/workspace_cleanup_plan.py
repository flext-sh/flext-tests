"""Deterministic cleanup planning and guarded apply for workspace residues.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from flext_cli import u

from flext_core import r
from flext_tests import m, p
from flext_tests._utilities.workspace_cleanup_inspect import (
    FlextTestsWorkspaceCleanupInspectUtilitiesMixin,
)

if TYPE_CHECKING:
    from flext_core import t


class FlextTestsWorkspaceCleanupPlanUtilitiesMixin(
    FlextTestsWorkspaceCleanupInspectUtilitiesMixin,
):
    """Build and apply exact ignored-residue plans with stale-drift protection."""

    @staticmethod
    def _candidate_sort_key(candidate: m.Tests.WorkspaceCleanupCandidate) -> str:
        """Return the deterministic path key for cleanup plan ordering."""
        return candidate.relative_path.as_posix()

    @classmethod
    def _candidate(
        cls,
        root: Path,
        relative_path: Path,
    ) -> p.Result[m.Tests.WorkspaceCleanupCandidate]:
        """Validate and describe one existing cleanup candidate.

        Returns:
            The resulting ``p.Result[m.Tests.WorkspaceCleanupCandidate]``.
        """
        lexical_result = cls._lexical_path(root, relative_path)
        if lexical_result.failure:
            return r[m.Tests.WorkspaceCleanupCandidate].fail(lexical_result.error)
        path = lexical_result.value
        validators: t.VariadicTuple[Callable[[], p.Result[bool]]] = (
            lambda: cls._reject_protected(root, relative_path),
            lambda: cls._reject_symlink_ancestor(root, relative_path),
            lambda: cls._reject_unsafe_node(path, relative_path),
            lambda: cls._ignored(root, relative_path),
            lambda: cls._untracked_and_clean(root, relative_path),
        )
        for validate in validators:
            validator_result = validate()
            if validator_result.failure:
                return r[m.Tests.WorkspaceCleanupCandidate].fail(
                    validator_result.error,
                )
        fingerprint_result = cls._path_fingerprint(path)
        if fingerprint_result.failure:
            return r[m.Tests.WorkspaceCleanupCandidate].fail(fingerprint_result.error)
        kind: Literal["file", "directory", "symlink"] = (
            "symlink" if path.is_symlink() else "directory" if path.is_dir() else "file"
        )
        candidate = m.Tests.WorkspaceCleanupCandidate(
            relative_path=relative_path,
            path=path,
            kind=kind,
            fingerprint=fingerprint_result.value,
        )
        return r[m.Tests.WorkspaceCleanupCandidate].ok(candidate)

    @staticmethod
    def _reject_nested(
        candidates: tuple[m.Tests.WorkspaceCleanupCandidate, ...],
    ) -> p.Result[bool]:
        """Reject overlapping parent and child cleanup targets.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        for index, parent in enumerate(candidates):
            for child in candidates[index + 1 :]:
                if (
                    parent.path in child.path.parents
                    or child.path in parent.path.parents
                ):
                    return r[bool].fail(
                        "cleanup residues overlap: "
                        f"{parent.relative_path} and {child.relative_path}",
                    )
        return r[bool].ok(value=True)

    @classmethod
    def _unique_relative_path(cls, declared: Path, seen: set[Path]) -> p.Result[Path]:
        """Validate one declared residue and require its uniqueness.

        Returns:
            The resulting ``p.Result[Path]``.
        """
        relative_result = cls._relative_path(declared)
        if relative_result.failure:
            return r[Path].fail(relative_result.error)
        relative_path = relative_result.value
        if relative_path in seen:
            return r[Path].fail(
                f"cleanup residue is declared more than once: {relative_path}",
            )
        return r[Path].ok(relative_path)

    @classmethod
    def _lexical_existing(
        cls,
        candidates: list[m.Tests.WorkspaceCleanupCandidate],
        root: Path,
        relative_path: Path,
    ) -> p.Result[bool]:
        """Plan one residue candidate when it exists; absent residue is skipped.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        lexical_result = cls._lexical_path(root, relative_path)
        if lexical_result.failure:
            return r[bool].fail(lexical_result.error)
        lexical = lexical_result.value
        if not lexical.exists() and not lexical.is_symlink():
            return r[bool].ok(value=True)
        candidate_result = cls._candidate(root, relative_path)
        if candidate_result.failure:
            return r[bool].fail(candidate_result.error)
        candidates.append(candidate_result.value)
        return r[bool].ok(value=True)

    @classmethod
    def workspace_cleanup_plan(
        cls,
        request: p.Tests.WorkspaceCleanupRequest,
    ) -> p.Result[p.Tests.WorkspaceCleanupPlan]:
        """Build a deterministic read-only plan for exact ignored residues.

        Returns:
            The resulting ``p.Result[p.Tests.WorkspaceCleanupPlan]``.
        """
        if not isinstance(request, m.Tests.WorkspaceCleanupRequest):
            return r[p.Tests.WorkspaceCleanupPlan].fail(
                "cleanup request must be the canonical WorkspaceCleanupRequest model",
            )
        root_result = cls._repository_root(request)
        if root_result.failure:
            return r[p.Tests.WorkspaceCleanupPlan].fail(root_result.error)
        root = root_result.value
        relative_paths: set[Path] = set()
        candidates: list[m.Tests.WorkspaceCleanupCandidate] = []
        for declared in request.policy.residues:
            unique_result = cls._unique_relative_path(declared, relative_paths)
            if unique_result.failure:
                return r[p.Tests.WorkspaceCleanupPlan].fail(unique_result.error)
            relative_path = unique_result.value
            relative_paths.add(relative_path)
            planned_result = cls._lexical_existing(candidates, root, relative_path)
            if planned_result.failure:
                return r[p.Tests.WorkspaceCleanupPlan].fail(planned_result.error)
        ordered = tuple(sorted(candidates, key=cls._candidate_sort_key))
        nested_result = cls._reject_nested(ordered)
        if nested_result.failure:
            return r[p.Tests.WorkspaceCleanupPlan].fail(nested_result.error)
        plan = m.Tests.WorkspaceCleanupPlan(request=request, candidates=ordered)
        return r[p.Tests.WorkspaceCleanupPlan].ok(plan)

    @classmethod
    def _apply_candidate(
        cls,
        root: Path,
        candidate: m.Tests.WorkspaceCleanupCandidate,
        removed: list[Path],
    ) -> p.Result[bool]:
        """Re-validate one planned candidate, delete it, and record the removal.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        fresh_result = cls._candidate(root, candidate.relative_path)
        if fresh_result.failure:
            return r[bool].fail(f"cleanup plan is stale: {fresh_result.error}")
        if fresh_result.value != candidate:
            return r[bool].fail(
                f"cleanup plan is stale for {candidate.relative_path}: "
                "filesystem state changed since dry-run",
            )
        delete_result = u.Cli.files_delete(candidate.path)
        if delete_result.failure:
            completed = ", ".join(path.as_posix() for path in removed)
            return r[bool].fail(
                f"cleanup deletion failed for {candidate.relative_path}: "
                f"{delete_result.error}; already removed=[{completed}]",
            )
        if candidate.path.exists() or candidate.path.is_symlink():
            return r[bool].fail(
                f"cleanup deletion reported success but path remains: "
                f"{candidate.relative_path}",
            )
        removed.append(candidate.path)
        return r[bool].ok(value=True)

    @classmethod
    def workspace_cleanup_apply(
        cls,
        plan: p.Tests.WorkspaceCleanupPlan,
    ) -> p.Result[p.Tests.WorkspaceCleanupReport]:
        """Apply exactly one fresh canonical dry-run plan and fail loudly.

        Returns:
            The resulting ``p.Result[p.Tests.WorkspaceCleanupReport]``.
        """
        if not isinstance(plan, m.Tests.WorkspaceCleanupPlan):
            return r[p.Tests.WorkspaceCleanupReport].fail(
                "cleanup plan must be the canonical WorkspaceCleanupPlan model",
            )
        replanned_result = cls.workspace_cleanup_plan(plan.request)
        if replanned_result.failure:
            return r[p.Tests.WorkspaceCleanupReport].fail(
                f"cleanup plan is stale: {replanned_result.error}",
            )
        replanned = replanned_result.value
        if replanned.candidates != plan.candidates:
            return r[p.Tests.WorkspaceCleanupReport].fail(
                "cleanup plan is stale: candidates changed since dry-run",
            )
        root_result = cls._repository_root(plan.request)
        if root_result.failure:
            return r[p.Tests.WorkspaceCleanupReport].fail(
                f"cleanup plan is stale: {root_result.error}",
            )
        root = root_result.value
        removed: list[Path] = []
        for candidate in plan.candidates:
            applied_result = cls._apply_candidate(root, candidate, removed)
            if applied_result.failure:
                return r[p.Tests.WorkspaceCleanupReport].fail(applied_result.error)
        report = m.Tests.WorkspaceCleanupReport(plan=plan, removed=tuple(removed))
        return r[p.Tests.WorkspaceCleanupReport].ok(report)


__all__: t.VariadicTuple[str] = ("FlextTestsWorkspaceCleanupPlanUtilitiesMixin",)
