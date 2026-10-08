"""Capability-gated collection: typed NOT EXECUTED, never skip.

Operator law (2026-09-29, OUD program decision 5): capability gating is
declarative and automatic. A test declares the capability it needs through a
marker; at collection time the marker maps to a capability probe:

- CI=Y (the exact Make token) or an absent host capability (no Docker
  daemon, service endpoint unreachable) → the test is DESELECTED with a
  typed reason recorded for the runner receipts — it is NOT EXECUTED and
  is never reported as passed, and it is never a runtime ``pytest.skip``.
- A capable host executes the test: a real service failure is RED.

The gate is marker-driven and data-owned: ``CONNECTIVITY_MARKER_CONTAINERS``
maps a pytest marker to the shared container whose declared host/port is
probed. Each endpoint is probed at most once per session, and only when a
collected test actually carries the marker, so suites that need nothing
external pay nothing. This replaces the historical skip-based behaviour and
its stale "AGENTS.md skip rule" citation.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import socket
from importlib import import_module
from typing import TYPE_CHECKING

import pytest
from flext_infra import config as infra_config

from flext_tests import c

# The Docker manager and the ``u`` facade load the model tree, so they resolve
# through the deferred ``import_module`` form inside the probes that need them:
# a session without capability-marked tests never loads ``flext_tests.models``.

if TYPE_CHECKING:
    from collections.abc import Iterable

    from flext_tests import t

_DESELECTED_CAPABILITY_RECEIPT: pytest.StashKey[dict[str, str]] = pytest.StashKey()
"""Typed config-stash key carrying the NOT EXECUTED receipt for the runner."""


class FlextTestsCapabilityPlugin:
    """Deselect capability-bound tests with typed NOT EXECUTED reasons."""

    def __init__(self) -> None:
        """Per-session probe cache: one probe per marker per pytest process."""
        self._probe_cache: t.MutableMappingKV[str, str | None] = {}

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
        root = import_module("flext_tests")
        published = (
            root
            .FlextTestsDocker()
            .fetch_container_info(container_name)
            .flat_map(
                lambda info: root.u.Tests.resolve_host_port(info, container_port),
            )
        )
        return published.value if published.success else None

    def _unreachable_reason(self, marker: str) -> str | None:
        """Return a deselect reason when the marker's service is unavailable."""
        if marker in self._probe_cache:
            return self._probe_cache[marker]
        if marker == c.Tests.DOCKER_CONNECTIVITY_MARKER:
            manager = import_module("flext_tests").FlextTestsDocker()
            client = manager.client
            docker_reason: str | None
            if client is None:
                docker_reason = c.Tests.DOCKER_UNREACHABLE_DESELECT_REASON
            else:
                client.close()
                docker_reason = None
            self._probe_cache[marker] = docker_reason
            return docker_reason
        reason: str | None = None
        container = c.Tests.CONNECTIVITY_MARKER_CONTAINERS.get(marker)
        endpoint = None if container is None else self._endpoint(container)
        if container is not None and endpoint is not None:
            host, port = endpoint
            unreachable = c.Tests.UNREACHABLE_DESELECT_REASON.format(
                marker=marker,
                host=host,
                port=port,
            )
            host_port = self._published_port(container, port)
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
        self._probe_cache[marker] = reason
        return reason

    def deselect_reasons(
        self,
        config: pytest.Config,
        items: Iterable[pytest.Item],
    ) -> t.MutableMappingKV[str, str]:
        """Compute {nodeid: reason} for capability tests this host cannot run.

        Returns:
            The resulting ``t.MutableMappingKV[str, str]``.
        """
        reasons: dict[str, str] = {}
        ci_disabled: bool | None = None
        for item in items:
            for marker in c.Tests.CONNECTIVITY_MARKERS:
                if item.get_closest_marker(marker) is None:
                    continue
                if marker == c.Tests.DOCKER_CONNECTIVITY_MARKER and ci_disabled is None:
                    ci_disabled = self._ci_disables_docker()
                if marker == c.Tests.DOCKER_CONNECTIVITY_MARKER and ci_disabled:
                    ci = infra_config.Infra.codegen.make.ci
                    reasons[item.nodeid] = c.Tests.ERR_DOCKER_DISABLED_BY_CI.format(
                        variable=ci.variable,
                        value=ci.value,
                    )
                else:
                    unreachable = self._unreachable_reason(marker)
                    if unreachable is not None:
                        reasons[item.nodeid] = unreachable
                break
        del config
        return reasons

    @staticmethod
    def _ci_disables_docker() -> bool:
        """True when the Make CI token (config SSOT) is active.

        Returns:
            The resulting ``bool``.
        """
        ci_disables: bool = import_module(
            "flext_tests",
        ).FlextTestsDocker.ci_disables_docker()
        return ci_disables

    def pytest_collection_modifyitems(
        self,
        config: pytest.Config,
        items: list[pytest.Item],
    ) -> None:
        """Deselect capability tests this host cannot run; record the reasons."""
        reasons = self.deselect_reasons(config, items)
        if not reasons:
            return
        items[:] = [item for item in items if item.nodeid not in reasons]
        recorded_raw = config.stash.get(_DESELECTED_CAPABILITY_RECEIPT, None)
        recorded: dict[str, str] = (
            dict(recorded_raw) if recorded_raw is not None else {}
        )
        recorded.update(reasons)
        config.stash[_DESELECTED_CAPABILITY_RECEIPT] = recorded

    @staticmethod
    def pytest_terminal_summary(
        terminalreporter: pytest.TerminalReporter,
    ) -> None:
        """Report the typed NOT EXECUTED accounting for the runner receipts."""
        empty_receipt: dict[str, str] = {}
        recorded = terminalreporter.config.stash.get(
            _DESELECTED_CAPABILITY_RECEIPT,
            empty_receipt,
        )
        if not recorded:
            return
        terminalreporter.section(
            f"NOT EXECUTED (capability deselected): {len(recorded)}",
            sep="=",
        )
        for nodeid, reason in sorted(recorded.items()):
            terminalreporter.write_line(f"  {nodeid}: {reason}")


__all__: list[str] = ["FlextTestsCapabilityPlugin"]
