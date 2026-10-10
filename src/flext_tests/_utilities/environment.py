"""Local test-environment prerequisites, never application health checks.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import socket
from collections.abc import Sequence
from pathlib import Path
from urllib.parse import urlsplit

import pytest
from dotenv import dotenv_values
from flext_cli import u

from flext_tests import c, t


class FlextTestsEnvironmentUtilitiesMixin:
    """Resolve explicit, untracked test configuration without logging its values."""

    @staticmethod
    def external_environment_reason(
        required_vars: Sequence[str] = (),
        env_file: Path | None = None,
        *,
        endpoint: tuple[str, int] | None = None,
        url_var: str | None = None,
    ) -> str | None:
        """Return an unmet prerequisite; transport readiness is not authentication.

        Only values actually declared in the local file authorize connectivity.
        Inherited credentials cannot opt an otherwise unconfigured suite in.

        Returns:
            The unmet prerequisite reason, or ``None`` when the environment is ready.

        """
        path = Path.cwd() / ".env" if env_file is None else env_file
        reason = FlextTestsEnvironmentUtilitiesMixin._untracked_reason(path)
        if reason is not None:
            return reason
        values = dotenv_values(path, interpolate=False)
        reason = FlextTestsEnvironmentUtilitiesMixin._values_reason(
            values, required_vars
        )
        if reason is not None:
            return reason
        return FlextTestsEnvironmentUtilitiesMixin._endpoint_reason(
            values, url_var, endpoint
        )

    @staticmethod
    def _untracked_reason(path: Path) -> str | None:
        if not path.is_file() or path.is_symlink():
            return "External tests require a local untracked .env"
        tracked = u.Cli.run_raw(
            [*c.Cli.GIT_TRACKED_FILE_COMMAND, path.name],
            cwd=path.parent,
        ).unwrap()
        return_code = tracked.outcome.raw_return_code
        if return_code == c.Cli.EXIT_CODE_SUCCESS:
            return "External tests require a local untracked .env"
        if return_code != c.Cli.EXIT_CODE_FAILURE:
            msg = f"Git test-environment tracking check failed (exit {return_code})"
            raise RuntimeError(msg)
        return None

    @staticmethod
    def _values_reason(
        values: t.OptionalStrMapping,
        required_vars: Sequence[str],
    ) -> str | None:
        if not values or any(not values.get(name) for name in required_vars):
            return "External test environment is not configured"
        return None

    @staticmethod
    def _endpoint_reason(
        values: t.OptionalStrMapping,
        url_var: str | None,
        endpoint: tuple[str, int] | None,
    ) -> str | None:
        if url_var is not None:
            value = values.get(url_var)
            if not value:
                return "External test endpoint is not configured"
            url = urlsplit(value)
            if not url.hostname:
                return "External test endpoint is not configured"
            endpoint = (
                url.hostname,
                url.port or (443 if url.scheme == "https" else 80),
            )
        if endpoint is None:
            return None
        try:
            with socket.create_connection(
                endpoint,
                timeout=c.Tests.CONNECTIVITY_PROBE_TIMEOUT_SECONDS,
            ):
                pass
        except OSError:
            return "External test endpoint is unreachable"
        return None

    @staticmethod
    def external_environment_values(env_file: Path) -> t.StrMapping:
        """Read declared values for the canonical test environment scope.

        Returns:
            Only values explicitly assigned in the consumer's local file.

        """
        return {
            name: value
            for name, value in dotenv_values(env_file, interpolate=False).items()
            if value is not None
        }

    @staticmethod
    def has_external_environment(
        required_vars: Sequence[str],
        env_file: Path | None = None,
        *,
        endpoint: tuple[str, int] | None = None,
        url_var: str | None = None,
    ) -> bool:
        """Check the same prerequisites used by the shared pytest plugin.

        Returns:
            ``True`` when every declared prerequisite is satisfied.

        """
        return (
            FlextTestsEnvironmentUtilitiesMixin.external_environment_reason(
                required_vars,
                env_file,
                endpoint=endpoint,
                url_var=url_var,
            )
            is None
        )

    @staticmethod
    def skip_if_no_external_environment(
        required_vars: Sequence[str],
        env_file: Path | None = None,
        *,
        endpoint: tuple[str, int] | None = None,
        url_var: str | None = None,
    ) -> None:
        """Skip before constructing a service-dependent fixture."""
        reason = FlextTestsEnvironmentUtilitiesMixin.external_environment_reason(
            required_vars,
            env_file,
            endpoint=endpoint,
            url_var=url_var,
        )
        if reason is not None:
            pytest.skip(reason)


__all__ = ["FlextTestsEnvironmentUtilitiesMixin"]
