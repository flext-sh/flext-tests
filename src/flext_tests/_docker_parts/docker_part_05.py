"""Docker execution helper for flext-tests."""

from __future__ import annotations

from typing import override

from flext_tests import c, m, p, r, t
from flext_tests._docker_parts.docker_part_04 import (
    FlextTestsDocker as FlextTestsDockerPart04,
)


class FlextTestsDocker(FlextTestsDockerPart04):
    """Execute configured Docker targets."""

    @override
    def execute(self) -> p.Result[m.Tests.ContainerInfo]:
        """Ensure the configured container is available with a single DSL call."""
        target = self.target_config
        if target is None:
            return r[m.Tests.ContainerInfo].fail(
                "Docker target not configured. Use tk.shared(...).execute() or tk.compose(...).execute().",
            )
        if not target.container_name:
            return r[m.Tests.ContainerInfo].fail(
                "Docker target has no inspection container configured. Use up()/down()/ready() for stack-only lifecycles.",
            )

        error_msg = self._ensure_target_started(target)
        if error_msg is not None:
            return r[m.Tests.ContainerInfo].fail(error_msg)
        return self._ensure_target_ready(target)

    def _ensure_target_started(
        self,
        target: m.Tests.ContainerConfig,
    ) -> str | None:
        """Start or recreate the configured target when required."""
        if target.force_recreate or self.container_dirty(target.container_name):
            compose_result = self.compose_up(
                str(target.compose_file),
                service=target.service or None,
                force_recreate=True,
            )
            if compose_result.failure:
                return compose_result.error or "Failed to recreate Docker target"
            _ = self.mark_container_clean(target.container_name)
            return None

        status_result = self.fetch_container_status(target.container_name)
        container_running = status_result.success and (
            status_result.value.status == c.Tests.ContainerStatus.RUNNING
        )
        if container_running:
            return None
        start_result = self.start_existing_container(target.container_name)
        if start_result.success:
            return None
        compose_result = self.compose_up(str(target.compose_file), service=target.service or None)
        if compose_result.failure:
            return compose_result.error or "Failed to start Docker target"
        return None

    def _ensure_target_ready(
        self,
        target: m.Tests.ContainerConfig,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Fetch target info and run configured readiness checks."""
        container_info_result = self.fetch_container_info(target.container_name)
        if container_info_result.failure:
            return container_info_result
        if target.port is None:
            return container_info_result

        ready_port = self._resolve_readiness_port(target, container_info_result.value)
        if ready_port is None:
            return r[m.Tests.ContainerInfo].fail(
                f"Docker target {target.container_name} has no resolved host port for readiness check",
            )
        ready_result = self.wait_for_port_ready(
            target.host,
            ready_port,
            max_wait=target.startup_timeout,
        )
        if ready_result.failure:
            return r[m.Tests.ContainerInfo].fail(
                ready_result.error or "Docker target readiness check failed",
            )
        if not ready_result.value:
            return r[m.Tests.ContainerInfo].fail(
                f"Container {target.container_name} did not become ready on {target.host}:{ready_port}",
            )
        return container_info_result


__all__: list[str] = ["FlextTestsDocker"]
