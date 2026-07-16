"""Git process boundary for workspace cleanup utilities."""

from __future__ import annotations

from pathlib import Path

from flext_cli import u
from flext_tests import c, p, r


class FlextTestsWorkspaceCleanupGitUtilitiesMixin:
    """Execute Git commands and describe failures without hiding output."""

    @staticmethod
    def _git(
        workspace_root: Path,
        arguments: tuple[str, ...],
        *,
        input_data: bytes | None = None,
    ) -> p.Result[p.Cli.CommandOutput]:
        """Execute Git through the canonical flext-cli process boundary."""
        result = u.Cli.run_raw(
            (c.Infra.GIT, *arguments), cwd=workspace_root, input_data=input_data
        )
        if result.failure and result.error is None:
            return r[p.Cli.CommandOutput].fail(
                "git execution failed without an error message"
            )
        return result

    @staticmethod
    def _command_error(operation: str, output: p.Cli.CommandOutput) -> str:
        """Describe one non-zero Git command without hiding its real output."""
        detail = output.stderr.strip()
        if not detail:
            detail = output.stdout.strip()
        if not detail:
            detail = f"exit code {output.exit_code}"
        return f"{operation} failed: {detail}"


__all__: tuple[str, ...] = ("FlextTestsWorkspaceCleanupGitUtilitiesMixin",)
