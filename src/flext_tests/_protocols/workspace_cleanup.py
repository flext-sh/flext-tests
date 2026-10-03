"""Read-only workspace cleanup protocols for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flext_core import t


class FlextTestsWorkspaceCleanupProtocols:
    """Structural contracts for cleanup models crossing public interfaces."""

    @runtime_checkable
    class WorkspaceCleanupPolicy(Protocol):
        """Config-owned cleanup policy surface."""

        @property
        def residues(self) -> t.VariadicTuple[Path]: ...

    @runtime_checkable
    class WorkspaceCleanupRequest(Protocol):
        """Runtime cleanup request surface."""

        @property
        def repository_root(self) -> Path: ...

        @property
        def policy(
            self,
        ) -> FlextTestsWorkspaceCleanupProtocols.WorkspaceCleanupPolicy: ...

    @runtime_checkable
    class WorkspaceCleanupCandidate(Protocol):
        """Validated cleanup candidate surface."""

        @property
        def relative_path(self) -> Path: ...

        @property
        def path(self) -> Path: ...

        @property
        def kind(self) -> Literal["file", "directory", "symlink"]: ...

        # NOTE (multi-agent): expose immutable dry-run state for stale-plan checks.
        @property
        def fingerprint(self) -> str: ...

    @runtime_checkable
    class WorkspaceCleanupPlan(Protocol):
        """Deterministic dry-run plan surface."""

        @property
        def request(
            self,
        ) -> FlextTestsWorkspaceCleanupProtocols.WorkspaceCleanupRequest: ...

        @property
        def candidates(
            self,
        ) -> tuple[
            FlextTestsWorkspaceCleanupProtocols.WorkspaceCleanupCandidate,
            ...,
        ]: ...

    @runtime_checkable
    class WorkspaceCleanupReport(Protocol):
        """Applied cleanup report surface."""

        @property
        def plan(self) -> FlextTestsWorkspaceCleanupProtocols.WorkspaceCleanupPlan: ...

        @property
        def removed(self) -> t.VariadicTuple[Path]: ...


__all__: t.VariadicTuple[str] = ("FlextTestsWorkspaceCleanupProtocols",)
