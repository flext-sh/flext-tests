"""Kubernetes (kind) cluster control facade for FLEXT test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Annotated, Self, override

from flext_tests import c, m, p, r, t, u
from flext_tests.docker import FlextTestsDocker


class FlextTestsKube(FlextTestsDocker):
    """Manage a kind Kubernetes cluster for FLEXT tests via docker compose.

    Specializes :class:`FlextTestsDocker` for the ``flext-kind-test`` shared
    container entry: brings its shared-asset
    ``docker/docker-compose.kubernetes.yml`` stack up, waits for the
    apiserver port, and asserts node readiness through ``kubectl``.
    """

    kubectl_service: Annotated[
        str,
        u.Field(
            min_length=1,
            description=(
                "Compose service exposing kubectl against the kind kubeconfig."
            ),
        ),
    ] = "kubectl"

    @classmethod
    def kind(
        cls,
        *,
        repository_root: Path | None = None,
        state_dir: Path | None = None,
    ) -> Self:
        """Build a DSL-configured service for the shared kind cluster.

        Returns:
            The resulting ``Self``.
        """
        return cls.shared(
            c.Tests.KIND_CONTAINER_NAME,
            repository_root=repository_root,
            state_dir=state_dir,
        )

    def cluster_up(self) -> p.Result[str]:
        """Start the kind stack and wait for the apiserver to accept TCP.

        Returns:
            The resulting ``p.Result[str]``.
        """
        target = self.target_config
        if target is None:
            return r[str].fail(
                "Kubernetes target not configured. Use FlextTestsKube.kind(...) first.",
            )
        if target.compose_file is None:
            return r[str].fail("Kubernetes target has no compose file configured.")
        up_result = self.up()
        if up_result.failure:
            return up_result.map_error(
                lambda error: f"Kind cluster start failed: {error}",
            )
        if target.port is None or not target.container_name:
            return r[str].ok("Kind cluster started (no readiness port configured)")
        port = target.port
        listening = (
            self
            .fetch_container_info(target.container_name)
            .flat_map(lambda info: u.Tests.resolve_host_port(info, port))
            .flat_map(
                lambda host_port: self.wait_for_port_ready(
                    target.host,
                    host_port,
                    max_wait=target.startup_timeout,
                ),
            )
        )
        if listening.failure:
            return r[str].from_failure(
                listening.map_error(
                    lambda error: f"Kind apiserver readiness failed: {error}",
                ),
            )
        return r[str].ok("Kind cluster started and apiserver is reachable")

    def cluster_down(self) -> p.Result[str]:
        """Tear down the kind stack via compose down.

        Returns:
            The resulting ``p.Result[str]``.
        """
        target = self.target_config
        if target is None:
            return r[str].fail(
                "Kubernetes target not configured. Use FlextTestsKube.kind(...) first.",
            )
        if target.compose_file is None:
            return r[str].fail("Kubernetes target has no compose file configured.")
        return self.down()

    def nodes_ready(self) -> p.Result[bool]:
        """Run ``kubectl get nodes`` and confirm every node reports Ready.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        target = self.target_config
        if target is None or target.compose_file is None:
            return r[bool].fail(
                "Kubernetes target not configured. Use FlextTestsKube.kind(...) first.",
            )
        enabled = self.lifecycle_enabled()
        if enabled.failure:
            return enabled
        client = self._compose_client(
            target.compose_file,
            target.project_name or u.Tests.docker_compose_project(target.compose_file),
        )
        try:
            output = client.compose.execute(
                self.kubectl_service,
                ["get", "nodes", "--no-headers"],
                tty=False,
            )
        except self._compose_exception_types() as exc:
            return r[bool].fail_op("kubectl get nodes", exc)
        lines = [line.strip() for line in (output or "").splitlines() if line.strip()]
        if not lines:
            return r[bool].fail("kubectl get nodes returned no nodes")
        not_ready = [line for line in lines if " Ready" not in f" {line}"]
        if not_ready:
            return r[bool].fail(f"Kind nodes not Ready: {not_ready}")
        return r[bool].ok(value=True)

    @override
    def execute(
        self,
        *,
        initializer: p.Tests.ContainerInitializer | None = None,
        readiness_probe: p.Tests.ReadinessProbe | None = None,
        creation_environment: t.MappingKV[str, t.SecretStr] | None = None,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Bring the kind cluster up, verify node readiness, and return info.

        The cluster is not a sealed container: ``initializer`` and
        ``creation_environment`` are rejected; ``readiness_probe`` is polled
        after the nodes report Ready.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.
        """
        target = self.target_config
        if target is None:
            return r[m.Tests.ContainerInfo].fail(
                "Kubernetes target not configured. "
                "Use FlextTestsKube.kind(...).execute().",
            )
        if initializer is not None or creation_environment:
            return r[m.Tests.ContainerInfo].fail(
                c.Tests.ERR_DOCKER_KUBE_HOOKS_UNSUPPORTED,
            )
        enabled = self.lifecycle_enabled()
        if enabled.failure:
            return r[m.Tests.ContainerInfo].from_failure(enabled)
        deadline = time.monotonic() + target.startup_timeout
        up_result = self.cluster_up()
        if up_result.failure:
            return r[m.Tests.ContainerInfo].from_failure(up_result)
        nodes_result = self.nodes_ready()
        if nodes_result.failure:
            return r[m.Tests.ContainerInfo].from_failure(nodes_result)
        return self._probe_kind_readiness(target, readiness_probe, deadline)

    def _probe_kind_readiness(
        self,
        target: m.Tests.ContainerConfig,
        readiness_probe: p.Tests.ReadinessProbe | None,
        deadline: float,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Collect the kind container info and poll the declared readiness probe.

        Returns:
            The resulting ``p.Result[m.Tests.ContainerInfo]``.
        """
        container_name = target.container_name
        info = (
            self.fetch_container_info(container_name)
            if container_name
            else r[m.Tests.ContainerInfo].ok(
                m.Tests.ContainerInfo(
                    name=target.service or c.Tests.KIND_CONTAINER_NAME,
                    status=c.Tests.ContainerStatus.RUNNING,
                    ports={},
                    image="",
                ),
            )
        )
        if info.failure or readiness_probe is None:
            return info
        probed = self._poll_readiness(
            info.value,
            readiness_probe,
            deadline,
            target.startup_timeout,
        )
        if probed.failure:
            return r[m.Tests.ContainerInfo].from_failure(probed)
        return info


__all__: list[str] = ["FlextTestsKube"]
