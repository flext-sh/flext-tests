"""Local test-environment prerequisites, never application health checks.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import socket
from collections.abc import Mapping, Sequence
from pathlib import Path
from urllib.parse import urlsplit

import pytest
from dotenv import dotenv_values
from flext_cli import u

from flext_tests import c, t


class FlextTestsUtilitiesEnvironment:
    """Resolve selected process inputs without logging their values."""

    @staticmethod
    def external_environment_reason(
        required_vars: Sequence[str] = (),
        *,
        endpoint: tuple[str, int] | None = None,
        url_var: str | None = None,
    ) -> str | None:
        """Return an unmet prerequisite; transport readiness is not authentication.

        Capability markers select the service. Declared inputs come from the
        process environment, independently of local files or Git state.

        Returns:
            The unmet prerequisite reason, or ``None`` when the environment is ready.

        """
        values = u.Cli.process_env()
        reason = FlextTestsUtilitiesEnvironment._values_reason(values, required_vars)
        if reason is not None:
            return reason
        return FlextTestsUtilitiesEnvironment._endpoint_reason(
            values, url_var, endpoint
        )

    @staticmethod
    def _values_reason(
        values: t.OptionalStrMapping,
        required_vars: Sequence[str],
    ) -> str | None:
        if any(not values.get(name) for name in required_vars):
            return "External test environment is not configured"
        return None

    @staticmethod
    def endpoint_reason(endpoint: tuple[str, int]) -> str | None:
        """Probe one transport endpoint that needs no local environment file.

        Returns:
            The unreachable reason, or ``None`` when the endpoint accepts.

        """
        return FlextTestsUtilitiesEnvironment._endpoint_reason({}, None, endpoint)

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
            # Configured endpoints may contain credentials; never echo them.
            msg = "External test endpoint is invalid or lacks a transport port"
            try:
                url = urlsplit(value)
                host = url.hostname
                port = url.port
            except ValueError:
                raise pytest.UsageError(msg) from None
            if not url.scheme or not host:
                raise pytest.UsageError(msg)
            if port is None:
                port = {
                    "http": c.HTTP_PORT,
                    "https": c.HTTPS_PORT,
                    "ldap": c.LDAP_PORT,
                    "ldaps": c.LDAPS_PORT,
                }.get(url.scheme)
            if port is None or not c.MIN_PORT <= port <= c.MAX_PORT:
                raise pytest.UsageError(msg)
            endpoint = (host, port)
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
    def external_environment_values(env_file: Path) -> Mapping[str, str]:
        """Decode the environment artifact of an explicitly selected fixture.

        Returns:
            Only values explicitly assigned in the selected artifact.

        """
        return {
            name: value
            for name, value in dotenv_values(env_file, interpolate=False).items()
            if value is not None
        }


__all__ = ["FlextTestsUtilitiesEnvironment"]
