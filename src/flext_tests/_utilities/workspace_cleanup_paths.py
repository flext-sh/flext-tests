"""Path validation and containment for workspace cleanup utilities.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_core import r
from flext_tests import c, p
from flext_tests._utilities.workspace_cleanup_git import (
    FlextTestsWorkspaceCleanupGitUtilitiesMixin,
)

if TYPE_CHECKING:
    from flext_core import t


class FlextTestsWorkspaceCleanupPathsUtilitiesMixin(
    FlextTestsWorkspaceCleanupGitUtilitiesMixin,
):
    """Resolve the Git root and validate normalized contained residue paths."""

    # NOTE (multi-agent): immutable hard-deny floor; these components are never
    # development residue and must never be a cleanup candidate or ancestor.
    _PROTECTED_COMPONENTS: frozenset[str] = frozenset({
        ".git",
        ".hg",
        ".svn",
        ".beads",
        ".venv",
        "venv",
        ".env",
        ".ssh",
        ".gnupg",
        "secrets",
        "credentials",
        "config",
        "settings",
    })

    @staticmethod
    def _validated_request_root(
        request: p.Tests.WorkspaceCleanupRequest,
    ) -> p.Result[Path]:
        """Resolve the request root and require an existing directory.

        Returns:
            The resulting ``p.Result[Path]``.
        """
        try:
            root = request.repository_root.resolve(strict=True)
        except OSError as exc:
            return r[Path].fail(
                f"cleanup workspace root resolution failed: {exc}",
                exception=exc,
            )
        if not root.is_dir():
            return r[Path].fail(f"cleanup workspace root is not a directory: {root}")
        return r[Path].ok(root)

    @classmethod
    def _successful_git_output(
        cls,
        root: Path,
        arguments: t.VariadicTuple[str],
        label: str,
    ) -> p.Result[p.Cli.CommandOutput]:
        """Run Git in ``root`` and require a zero exit code.

        Returns:
            The resulting ``p.Result[p.Cli.CommandOutput]``.
        """
        git_result = cls._git(root, arguments)
        if git_result.failure:
            return r[p.Cli.CommandOutput].fail(git_result.error)
        output = git_result.value
        if output.outcome.raw_return_code != c.Cli.EXIT_CODE_SUCCESS:
            return r[p.Cli.CommandOutput].fail(cls._command_error(label, output))
        return r[p.Cli.CommandOutput].ok(output)

    @classmethod
    def _resolved_git_root(cls, root: Path) -> p.Result[Path]:
        """Resolve the Git worktree root and require it to equal ``root``.

        Returns:
            The resulting ``p.Result[Path]``.
        """
        output_result = cls._successful_git_output(
            root,
            ("rev-parse", "--show-toplevel"),
            "git root discovery",
        )
        if output_result.failure:
            return r[Path].from_failure(output_result)
        raw_root = output_result.value.stdout.strip()
        if not raw_root:
            return r[Path].fail("git root discovery returned an empty path")
        try:
            git_root = Path(raw_root).resolve(strict=True)
        except OSError as exc:
            return r[Path].fail(f"git root resolution failed: {exc}", exception=exc)
        if git_root != root:
            return r[Path].fail(
                f"cleanup root must equal the Git worktree root: {root} != {git_root}",
            )
        return r[Path].ok(root)

    @classmethod
    def _repository_root(
        cls,
        request: p.Tests.WorkspaceCleanupRequest,
    ) -> p.Result[Path]:
        """Require the request root to be the exact enclosing Git worktree root.

        Returns:
            The resulting ``p.Result[Path]``.
        """
        root_result = cls._validated_request_root(request)
        if root_result.failure:
            return r[Path].from_failure(root_result)
        root = root_result.value
        git_root_result = cls._resolved_git_root(root)
        if git_root_result.failure:
            return r[Path].from_failure(git_root_result)
        return r[Path].ok(root)

    @staticmethod
    def _relative_path(path: Path) -> p.Result[Path]:
        """Validate one exact normalized workspace-relative path.

        Returns:
            The resulting ``p.Result[Path]``.
        """
        if path.is_absolute() or not path.parts:
            return r[Path].fail(f"cleanup residue must be a relative path: {path}")
        if any(part in {".", ".."} for part in path.parts):
            return r[Path].fail(f"cleanup residue is not normalized: {path}")
        normalized = Path(*path.parts)
        if normalized != path:
            return r[Path].fail(f"cleanup residue is not normalized: {path}")
        return r[Path].ok(normalized)

    @staticmethod
    def _lexical_path(root: Path, relative_path: Path) -> p.Result[Path]:
        """Resolve containment while retaining the lexical path for symlink unlinking.

        Returns:
            The resulting ``p.Result[Path]``.
        """
        lexical = root.joinpath(relative_path)
        try:
            resolved = lexical.resolve(strict=False)
            _ = resolved.relative_to(root)
        except (OSError, ValueError) as exc:
            return r[Path].fail(
                f"cleanup residue escapes the workspace: {relative_path}: {exc}",
            )
        if lexical == root:
            return r[Path].fail("cleanup residue cannot be the workspace root")
        return r[Path].ok(lexical)

    @classmethod
    def _reject_protected(cls, root: Path, relative_path: Path) -> p.Result[bool]:
        """Refuse any residue that targets a protected component or the Git dir.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        if any(part in cls._PROTECTED_COMPONENTS for part in relative_path.parts):
            return r[bool].fail(
                f"cleanup residue targets a protected path: {relative_path}",
            )
        for name in ("--git-dir", "--git-common-dir"):
            output_result = cls._successful_git_output(
                root,
                ("rev-parse", name),
                "git dir discovery",
            )
            if output_result.failure:
                return r[bool].from_failure(output_result)
            raw = output_result.value.stdout.strip()
            if not raw:
                continue
            try:
                git_dir = Path(raw if Path(raw).is_absolute() else root / raw).resolve(
                    strict=False,
                )
                candidate = root.joinpath(relative_path).resolve(strict=False)
            except (OSError, ValueError) as exc:
                return r[bool].fail(
                    f"protected path resolution failed: {relative_path}: {exc}",
                )
            if candidate == git_dir or git_dir in candidate.parents:
                return r[bool].fail(
                    f"cleanup residue targets the protected Git directory: "
                    f"{relative_path}",
                )
            if candidate in git_dir.parents:
                return r[bool].fail(
                    f"cleanup residue would remove the protected Git directory: "
                    f"{relative_path}",
                )
        return r[bool].ok(value=True)

    @staticmethod
    def _reject_symlink_ancestor(root: Path, relative_path: Path) -> p.Result[bool]:
        """Refuse a residue whose own ancestor components are symbolic links.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        current = root
        for part in relative_path.parts[:-1]:
            current /= part
            if current.is_symlink():
                return r[bool].fail(
                    f"cleanup residue has a symlink ancestor: {relative_path}",
                )
        return r[bool].ok(value=True)


__all__: t.VariadicTuple[str] = ("FlextTestsWorkspaceCleanupPathsUtilitiesMixin",)
