"""Auto-skip tests whose external service is unreachable.

A suite that needs a live service must not FAIL on a machine where that service
is simply not running: it must SKIP. Failing conflates "the code is wrong" with
"the database is down", and it blocks every push from a developer machine that
does not host the whole fleet.

The gate is marker-driven and data-owned: ``CONNECTIVITY_MARKER_CONTAINERS`` maps
a pytest marker to the shared container whose declared host/port is probed. Each
endpoint is probed at most once per session, and only when a collected test
actually carries the marker, so suites that need nothing external pay nothing.

A reachable service is never skipped — a service that answers and then
misbehaves still fails, which is the whole point of the suite.
"""

from __future__ import annotations

import socket
from typing import TYPE_CHECKING, ClassVar

import pytest

from flext_tests import c, u

if TYPE_CHECKING:
    from collections.abc import Iterable

    from flext_tests import t


class FlextTestsConnectivityPlugin:
    """Pytest plugin skipping connectivity-bound tests with a down service."""

    _probe_cache: ClassVar[t.MutableMappingKV[str, str | None]] = {}

    @staticmethod
    def _endpoint(container_name: str) -> tuple[str, int] | None:
        """Return the declared host and container port of one shared container."""
        settings = c.Tests.SHARED_CONTAINERS.get(container_name)
        if settings is None:
            return None
        host = settings.get("host")
        port = settings.get("port")
        if host is None or port is None:
            return None
        return str(host), int(port)

    @staticmethod
    def _published_port(container_name: str, container_port: int) -> int | None:
        """Return the host port a running container publishes, if any."""
        from flext_tests.docker import FlextTestsDocker

        published = (
            FlextTestsDocker()
            .fetch_container_info(container_name)
            .flat_map(lambda info: u.Tests.resolve_host_port(info, container_port))
        )
        return published.value if published.success else None

    @classmethod
    def _unreachable_reason(cls, marker: str) -> str | None:
        """Return a skip reason when the marker's service cannot be reached."""
        if marker in cls._probe_cache:
            return cls._probe_cache[marker]
        if marker == c.Tests.DOCKER_CONNECTIVITY_MARKER:
            from flext_tests.docker import FlextTestsDocker

            manager = FlextTestsDocker()
            client = manager.client
            docker_reason: str | None
            if client is None:
                docker_reason = c.Tests.DOCKER_UNREACHABLE_SKIP_REASON
            else:
                client.close()
                docker_reason = None
            cls._probe_cache[marker] = docker_reason
            return docker_reason
        reason: str | None = None
        container = c.Tests.CONNECTIVITY_MARKER_CONTAINERS.get(marker)
        endpoint = None if container is None else cls._endpoint(container)
        if container is not None and endpoint is not None:
            host, port = endpoint
            unreachable = c.Tests.UNREACHABLE_SKIP_REASON.format(
                marker=marker, host=host, port=port
            )
            host_port = cls._published_port(container, port)
            reason = unreachable
            if host_port is not None:
                try:
                    with socket.create_connection(
                        (host, host_port),
                        timeout=c.Tests.CONNECTIVITY_PROBE_TIMEOUT_SECONDS,
                    ):
                        reason = None
                except OSError:
                    reason = unreachable
        cls._probe_cache[marker] = reason
        return reason

    @staticmethod
    def pytest_collection_modifyitems(
        config: pytest.Config, items: Iterable[pytest.Item]
    ) -> None:
        """Mark connectivity-bound tests as skipped when their service is down."""
        del config
        for item in items:
            for marker in c.Tests.CONNECTIVITY_MARKERS:
                if item.get_closest_marker(marker) is None:
                    continue
                reason = FlextTestsConnectivityPlugin._unreachable_reason(marker)
                if reason is not None:
                    item.add_marker(pytest.mark.skip(reason=reason))
                break


__all__: list[str] = ["FlextTestsConnectivityPlugin"]
