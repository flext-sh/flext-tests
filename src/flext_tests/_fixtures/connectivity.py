"""Skip unavailable connectivity prerequisites before consumer fixtures run.

An integration marker alone never selects this policy. Authentication, protocol,
and application failures after transport readiness remain ordinary failures.
Only the owner's setup skip exception can emit prerequisite accounting evidence;
consumer-supplied reserved JUnit properties are discarded in every report phase.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import ExitStack
from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker, c, m, t, u


class FlextTestsCapabilityPlugin:
    """Shared marker-driven applicability owner for every consumer conftest."""

    def __init__(self) -> None:
        self._environment_stack_key = pytest.StashKey[ExitStack]()
        self._prerequisite_skip_key = pytest.StashKey[
            tuple[BaseException, pytest.Mark, str]
        ]()
        self._prerequisite_report_key = pytest.StashKey[bool]()

    @staticmethod
    def pytest_configure(config: pytest.Config) -> None:
        config.addinivalue_line(
            "markers",
            "connectivity(required_vars=(), url_var=None, host=None, port=None): "
            "external test environment",
        )

    @staticmethod
    def _declaration(marker: pytest.Mark) -> tuple[tuple[str, ...], str | None]:
        if marker.args or marker.kwargs.keys() - {
            "required_vars",
            "url_var",
            "host",
            "port",
        }:
            msg = "Connectivity declarations require supported keyword arguments"
            raise pytest.UsageError(msg)
        required = marker.kwargs.get("required_vars", ())
        url_var = marker.kwargs.get("url_var")
        try:
            names = u.type_adapter(
                tuple[t.NonEmptyStr, ...] | list[t.NonEmptyStr]
            ).validate_python(required, strict=True)
        except m.ValidationError as exc:
            msg = "Connectivity required_vars must be names"
            raise pytest.UsageError(msg) from exc
        if any(not name.strip() for name in names):
            msg = "Connectivity required_vars must be names"
            raise pytest.UsageError(msg)
        if url_var is not None and (
            not isinstance(url_var, str) or not url_var.strip()
        ):
            msg = "Connectivity url_var must be a name"
            raise pytest.UsageError(msg)
        host = marker.kwargs.get("host")
        port = marker.kwargs.get("port")
        if host is not None or port is not None:
            try:
                u.type_adapter(tuple[t.NonEmptyStr, t.PortNumber]).validate_python(
                    (host, port), strict=True
                )
            except m.ValidationError as exc:
                msg = "Connectivity host and port must be a string and an integer"
                raise pytest.UsageError(msg) from exc
            if isinstance(host, str) and not host.strip():
                msg = "Connectivity host and port must be a string and an integer"
                raise pytest.UsageError(msg)
        return tuple(names), url_var

    def _reason(self, item: pytest.Item, marker: pytest.Mark) -> str | None:
        """Resolve the unmet prerequisite for one connectivity marker.

        Returns:
            The skip reason, or ``None`` when the environment is ready.

        """
        required, url_var = self._declaration(marker)
        # Resolve each member's own .env even during workspace-wide collection.
        root = self._environment_file(item).parent
        return self._resolve_marker_reason(marker, required, url_var, root)

    @staticmethod
    def _requires_docker(marker: pytest.Mark) -> bool:
        return marker.name == "docker" or (
            marker.name in c.Tests.CONNECTIVITY_MARKER_CONTAINERS
            and marker.kwargs.get("url_var") is None
            and not (
                isinstance(marker.kwargs.get("host"), str)
                and isinstance(marker.kwargs.get("port"), int)
            )
        )

    @staticmethod
    def _resolve_marker_reason(
        marker: pytest.Mark,
        required: tuple[str, ...],
        url_var: str | None,
        root: Path,
    ) -> str | None:
        reason = u.Tests.external_environment_reason(env_file=root / ".env")
        if reason is None and marker.name == "docker":
            return FlextTestsCapabilityPlugin._docker_reason()
        if reason is not None:
            return reason
        return FlextTestsCapabilityPlugin._container_reason(
            marker, required, url_var, root
        )

    @staticmethod
    def _docker_reason() -> str | None:
        client = FlextTestsDocker().client
        if client is None:
            return "Docker test environment is unreachable"
        client.close()
        return None

    @staticmethod
    def _container_reason(
        marker: pytest.Mark,
        required: tuple[str, ...],
        url_var: str | None,
        root: Path,
    ) -> str | None:
        container = c.Tests.CONNECTIVITY_MARKER_CONTAINERS.get(marker.name)
        endpoint: tuple[str, int] | None = None
        host = marker.kwargs.get("host")
        port_number = marker.kwargs.get("port")
        if isinstance(host, str) and isinstance(port_number, int):
            endpoint = (host, port_number)
        if container is not None and endpoint is None and url_var is None:
            declared = c.Tests.SHARED_CONTAINERS[container]
            info = FlextTestsDocker().fetch_container_info(container)
            if info.failure:
                return "External test service is unavailable"
            port = u.Tests.resolve_host_port(info.value, int(declared["port"]))
            if port.failure:
                return "External test service port is unavailable"
            endpoint = (str(declared["host"]), port.value)
        if endpoint is None and url_var is None:
            return "External test endpoint is not declared"
        return u.Tests.external_environment_reason(
            required,
            root / ".env",
            endpoint=endpoint,
            url_var=url_var,
        )

    @staticmethod
    def _environment_file(item: pytest.Item) -> Path:
        root = item.path.parent
        while root != root.parent and not (root / "pyproject.toml").is_file():
            root = root.parent
        return root / ".env"

    @pytest.hookimpl(wrapper=True)
    def pytest_runtest_protocol(
        self,
        item: pytest.Item,
    ) -> Generator[None, None, bool | None]:
        """Scope configuration to this consumer, including its service fixtures.

        Returns:
            The wrapped protocol outcome, or ``None`` when no markers apply.

        """
        with ExitStack() as stack:
            item.stash[self._environment_stack_key] = stack
            try:
                return (yield)
            finally:
                del item.stash[self._environment_stack_key]
                if self._prerequisite_skip_key in item.stash:
                    del item.stash[self._prerequisite_skip_key]
                if self._prerequisite_report_key in item.stash:
                    del item.stash[self._prerequisite_report_key]

    def _skip_prerequisite(
        self, item: pytest.Item, marker: pytest.Mark, reason: str
    ) -> None:
        """Retain the exact owner exception, never a caller-supplied property."""
        try:
            pytest.skip(reason)
        except pytest.skip.Exception as exc:
            item.stash[self._prerequisite_skip_key] = (exc, marker, reason)
            raise

    @pytest.hookimpl(wrapper=True, tryfirst=True)
    def pytest_runtest_makereport(
        self, item: pytest.Item, call: pytest.CallInfo[None]
    ) -> Generator[None, pytest.TestReport, pytest.TestReport]:
        """Seal owner setup evidence after other report hooks, including teardown.

        JUnit finalizes properties from teardown; preserve the validated setup
        receipt there while removing reserved properties supplied by consumers.

        Returns:
            The sanitized report.
        """
        report = yield
        report.user_properties = [
            prop
            for prop in report.user_properties
            if not prop[0].startswith("flext_connectivity_prerequisite")
        ]
        receipt = item.stash.get(self._prerequisite_skip_key, None)
        if call.when == "setup":
            item.stash[self._prerequisite_report_key] = (
                receipt is not None
                and call.excinfo is not None
                and call.excinfo.value is receipt[0]
                and report.skipped
                and report.when == "setup"
                and report.nodeid == item.nodeid
                and isinstance(report.longrepr, tuple)
                and report.longrepr[2] == f"Skipped: {receipt[2]}"
                and any(marker is receipt[1] for marker in item.iter_markers())
            )
        elif call.when == "call" or report.skipped or report.failed:
            item.stash[self._prerequisite_report_key] = False
        if receipt is not None and item.stash.get(self._prerequisite_report_key, False):
            report.user_properties.extend([
                ("flext_connectivity_prerequisite", receipt[2]),
                ("flext_connectivity_prerequisite_phase", "setup"),
                ("flext_connectivity_prerequisite_capability", receipt[1].name),
                ("flext_connectivity_prerequisite_node", item.nodeid),
            ])
        return report

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item: pytest.Item) -> None:
        """Skip before fixtures, after all consumer collection hooks added markers."""
        markers = [
            marker
            for marker in item.iter_markers()
            if marker.name in {*c.Tests.CONNECTIVITY_MARKERS, "remote", "connectivity"}
        ]
        for marker in markers:
            self._declaration(marker)
        if (
            any(self._requires_docker(marker) for marker in markers)
            and FlextTestsDocker.ci_disables_docker()
        ):
            reason = "Docker-dependent connectivity tests are disabled in CI"
            marker = next(marker for marker in markers if self._requires_docker(marker))
            self._skip_prerequisite(item, marker, reason)
        for marker in markers:
            reason = self._reason(item, marker)
            if reason is not None:
                self._skip_prerequisite(item, marker, reason)
        if markers:
            item.stash[self._environment_stack_key].enter_context(
                u.Tests.env_vars_context(
                    u.Tests.external_environment_values(self._environment_file(item))
                )
            )


__all__ = ["FlextTestsCapabilityPlugin"]
