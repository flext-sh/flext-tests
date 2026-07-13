"""Docker container operations for flext-tests."""

from __future__ import annotations

import socket
import time
from typing import TYPE_CHECKING

from docker.errors import DockerException, NotFound

from flext_tests import c, m, p, r, t
from flext_tests._docker_parts.docker_part_03 import (
    FlextTestsDocker as FlextTestsDockerPart03,
)

if TYPE_CHECKING:
    # NOTE (multi-agent, mro-f8vk / kimi): in docker SDK 7.x Container lives
    # in docker.models.containers; docker.containers does not exist (checked
    # installed package + docker-stubs).
    from docker.models.containers import Container


class FlextTestsDocker(FlextTestsDockerPart03):
    """Run Docker SDK container operations."""

    def fetch_container_info(
        self,
        container_name: str,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Fetch container information."""
        client = self.client
        if client is None:
            error = self.client_error or "Docker daemon unavailable"
            return r[m.Tests.ContainerInfo].fail(error)
        try:
            container = client.containers.get(container_name)
        except NotFound:
            return r[m.Tests.ContainerInfo].fail(
                f"Container {container_name} not found",
            )
        except c.EXC_BROAD_RUNTIME as exc:
            return r[m.Tests.ContainerInfo].fail(str(exc))
        return r[m.Tests.ContainerInfo].ok(
            self._container_info_from_sdk(container_name, container),
        )

    def fetch_container_status(
        self,
        container_name: str,
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Fetch container status."""
        return self.fetch_container_info(container_name)

    def start_existing_container(self, container_name: str) -> p.Result[bool]:
        """Start an existing stopped container by name."""
        client = self.client
        if client is None:
            error = self.client_error or "Docker daemon unavailable"
            return r[bool].fail(error)
        try:
            container = client.containers.get(container_name)
        except NotFound:
            return r[bool].fail(f"Container {container_name} not found")
        except (DockerException, OSError, RuntimeError, AttributeError) as exc:
            return r[bool].fail(f"Failed to inspect container {container_name}: {exc}")
        return self._start_sdk_container(container_name, container)

    def start_compose_stack(
        self,
        compose_file: str,
        network_name: str | None = None,
    ) -> p.Result[str]:
        """Start a Docker Compose stack."""
        _ = network_name
        result = self.compose_up(compose_file)
        if result.failure:
            return r[str].fail_op("Stack start", result.error)
        return r[str].ok("Stack started successfully")

    def wait_for_port_ready(
        self,
        host: str,
        port: int,
        max_wait: int = 30,
    ) -> p.Result[bool]:
        """Wait until a TCP port is accepting connections."""
        waited = 0.0
        while waited < max_wait:
            try:
                with socket.create_connection((host, port), timeout=1):
                    return r[bool].ok(value=True)
            except (ConnectionRefusedError, TimeoutError, OSError):
                time.sleep(0.5)
                waited += 0.5
        return r[bool].ok(value=False)

    def _container_info_from_sdk(
        self,
        container_name: str,
        container: Container,
    ) -> m.Tests.ContainerInfo:
        """Build canonical container info from a Docker SDK container."""
        ports_raw: t.MappingKV[str, t.Tests.TestobjectSerializable] = (
            t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER.validate_python(
                container.ports,
            )
        )
        ports: t.MutableStrMapping = {}
        empty_bindings: t.SequenceOf[t.StrMapping] = []
        for container_port, host_bindings in ports_raw.items():
            normalized_bindings = self._normalize_bindings(host_bindings).unwrap_or(
                empty_bindings,
            )
            host_port = self._extract_host_port(normalized_bindings)
            if host_port:
                ports[container_port] = host_port
        image_obj = container.image
        image_tags_raw = image_obj.tags if image_obj is not None else ()
        image_tags = list(image_tags_raw)
        return m.Tests.ContainerInfo(
            name=container_name,
            status=c.Tests.ContainerStatus(container.status),
            ports=ports,
            image=image_tags[0] if image_tags else "",
            container_id=str(container.id),
        )

    @staticmethod
    def _start_sdk_container(
        container_name: str,
        container: Container,
    ) -> p.Result[bool]:
        """Start a Docker SDK container when it is not already running."""
        try:
            if container.status == "running":
                return r[bool].ok(value=True)
            container.start()
        except (DockerException, OSError, RuntimeError, AttributeError) as exc:
            return r[bool].fail(f"Failed to start container {container_name}: {exc}")
        return r[bool].ok(value=True)


__all__: list[str] = ["FlextTestsDocker"]
