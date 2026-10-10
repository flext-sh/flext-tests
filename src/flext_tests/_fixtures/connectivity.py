"""Skip unavailable connectivity prerequisites before consumer fixtures run.

An integration marker alone never selects this policy. Authentication, protocol,
and application failures after transport readiness remain ordinary failures.
"""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker, c, u


class FlextTestsCapabilityPlugin:
    """Shared marker-driven applicability owner for every consumer conftest."""

    def __init__(self) -> None:
        self._probe_cache: dict[tuple[Path, str], str | None] = {}

    @staticmethod
    def pytest_configure(config: pytest.Config) -> None:
        config.addinivalue_line(
            "markers",
            "connectivity(required_vars=(), url_var=None): external test environment",
        )

    @staticmethod
    def _declaration(marker: pytest.Mark) -> tuple[tuple[str, ...], str | None]:
        required = marker.kwargs.get("required_vars", ())
        url_var = marker.kwargs.get("url_var")
        if not isinstance(required, (tuple, list)) or not all(
            isinstance(name, str) for name in required
        ):
            raise pytest.UsageError("Connectivity required_vars must be names")
        if url_var is not None and not isinstance(url_var, str):
            raise pytest.UsageError("Connectivity url_var must be a name")
        return tuple(required), url_var

    def _reason(self, item: pytest.Item, marker: pytest.Mark) -> str | None:
        required, url_var = self._declaration(marker)
        # Resolve each member's own .env even during workspace-wide collection.
        root = self._environment_file(item).parent
        key = (root, str(marker))
        if key in self._probe_cache:
            return self._probe_cache[key]
        if marker.name == "docker" and FlextTestsDocker.ci_disables_docker():
            reason = "Docker-dependent connectivity tests are disabled in CI"
        else:
            reason = u.Tests.external_environment_reason(env_file=root / ".env")
            if reason is None and marker.name == "docker":
                client = FlextTestsDocker().client
                if client is None:
                    reason = "Docker test environment is unreachable"
                else:
                    client.close()
            elif reason is None:
                container = c.Tests.CONNECTIVITY_MARKER_CONTAINERS.get(marker.name)
                endpoint: tuple[str, int] | None = None
                host = marker.kwargs.get("host")
                port_number = marker.kwargs.get("port")
                if isinstance(host, str) and isinstance(port_number, int):
                    endpoint = (host, port_number)
                if container is not None:
                    declared = c.Tests.SHARED_CONTAINERS[container]
                    info = FlextTestsDocker().fetch_container_info(container)
                    if info.failure:
                        reason = "External test service is unavailable"
                    else:
                        port = u.Tests.resolve_host_port(info.value, int(declared["port"]))
                        if port.failure:
                            reason = "External test service port is unavailable"
                        else:
                            endpoint = (str(declared["host"]), port.value)
                if reason is None:
                    if endpoint is None and url_var is None:
                        reason = "External test endpoint is not declared"
                    else:
                        reason = u.Tests.external_environment_reason(
                            required, root / ".env", endpoint=endpoint, url_var=url_var,
                        )
        self._probe_cache[key] = reason
        return reason

    @staticmethod
    def _environment_file(item: pytest.Item) -> Path:
        root = item.path.parent
        while root != root.parent and not (root / "pyproject.toml").is_file():
            root = root.parent
        return root / ".env"

    @pytest.hookimpl(wrapper=True)
    def pytest_runtest_protocol(
        self, item: pytest.Item,
    ) -> Generator[None, None, bool | None]:
        """Scope configuration to this consumer, including its service fixtures."""
        markers = [
            marker for marker in item.iter_markers()
            if marker.name in (*c.Tests.CONNECTIVITY_MARKERS, "remote", "connectivity")
        ]
        if markers and all(self._reason(item, marker) is None for marker in markers):
            with u.Tests.external_environment(self._environment_file(item)):
                return (yield)
        return (yield)

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item: pytest.Item) -> None:
        """Skip before fixtures, after all consumer collection hooks added markers."""
        markers = [
            marker for marker in item.iter_markers()
            if marker.name in (*c.Tests.CONNECTIVITY_MARKERS, "remote", "connectivity")
        ]
        for marker in markers:
            self._declaration(marker)
        if any(
            marker.name == "docker"
            or marker.name in c.Tests.CONNECTIVITY_MARKER_CONTAINERS
            for marker in markers
        ) and FlextTestsDocker.ci_disables_docker():
            reason = "Docker-dependent connectivity tests are disabled in CI"
            item.user_properties.append(("flext_connectivity_prerequisite", reason))
            pytest.skip(reason)
        for marker in markers:
            reason = self._reason(item, marker)
            if reason is not None:
                item.user_properties.append(("flext_connectivity_prerequisite", reason))
                pytest.skip(reason)


__all__ = ["FlextTestsCapabilityPlugin"]
