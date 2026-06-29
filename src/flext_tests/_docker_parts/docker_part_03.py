"""Docker SDK and compose operations for flext-tests."""

from __future__ import annotations

import socket
import time
from pathlib import Path

from docker.errors import DockerException, NotFound
from python_on_whales.exceptions import DockerException as WhalesDockerException

from flext_tests import c, m, p, r, t
from flext_tests._docker_parts.docker_part_02 import (
    FlextTestsDocker as FlextTestsDockerPart02,
)


class FlextTestsDocker(FlextTestsDockerPart02):
    """Run low-level Docker SDK and compose operations."""

    def compose_down(self, compose_file: str) -> p.Result[str]:
        """Stop services using docker-compose via python_on_whales."""
        try:
            compose_path = Path(compose_file)
            if not compose_path.is_absolute():
                compose_path = self.workspace_root / compose_file
            original_files = self.docker.client_config.compose_files
            try:
                self.docker.client_config.compose_files = [str(compose_path)]
                self.docker.compose.down(volumes=True, remove_orphans=True)
            finally:
                self.docker.client_config.compose_files = original_files
            return r[str].ok("Compose down successful")
        except (
            AttributeError,
            OSError,
            RuntimeError,
            TypeError,
            ValueError,
            WhalesDockerException,
        ) as exc:
            self.logger.warning("Compose down failed", error=str(exc))
            return r[str].fail_op("Compose down", exc)

    def compose_up(
        self,
        compose_file: str,
        service: str | None = None,
        *,
        force_recreate: bool = False,
    ) -> p.Result[str]:
        """Start services using docker-compose via python_on_whales."""
        try:
            compose_path = Path(compose_file)
            if not compose_path.is_absolute():
                compose_path = self.workspace_root / compose_file
            original_files = self.docker.client_config.compose_files
            try:
                self.docker.client_config.compose_files = [str(compose_path)]
                if force_recreate:
                    down_result = self._compose_down_current_file()
                    if down_result.failure:
                        return down_result
                services = [service] if service else []
                self.docker.compose.up(
                    services=services,
                    detach=True,
                    remove_orphans=True,
                )
            finally:
                self.docker.client_config.compose_files = original_files
            return r[str].ok("Compose up successful")
        except (
            AttributeError,
            OSError,
            RuntimeError,
            TypeError,
            ValueError,
            WhalesDockerException,
        ) as exc:
            self.logger.exception("Compose up failed")
            return r[str].fail_op("Compose up", exc)

    def _compose_down_current_file(self) -> p.Result[str]:
        """Run compose down for the currently configured compose file."""
        try:
            self.docker.compose.down(remove_orphans=True, volumes=True)
        except (
            AttributeError,
            OSError,
            RuntimeError,
            TypeError,
            ValueError,
            WhalesDockerException,
        ) as exc:
            self.logger.warning("Compose recreate cleanup failed", error=str(exc))
            return r[str].fail_op("Compose recreate cleanup", exc)
        return r[str].ok("Compose recreate cleanup successful")

    def fetch_container_info(
        self, container_name: str
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Fetch container information."""
        try:
            client = self.client
            if client is None:
                error = self.client_error or "Docker daemon unavailable"
                return r[m.Tests.ContainerInfo].fail(error)
            container = client.containers.get(container_name)
            ports_raw: t.MappingKV[str, t.Tests.TestobjectSerializable] = (
                t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER.validate_python(
                    container.ports
                )
            )
            ports: t.MutableStrMapping = {}
            for container_port, host_bindings in ports_raw.items():
                normalized_bindings = self._normalize_bindings(host_bindings)
                host_port = self._extract_host_port(normalized_bindings)
                if host_port:
                    ports[container_port] = host_port
            image_obj = container.image
            image_tags_raw = image_obj.tags if image_obj is not None else ()
            image_tags = list(image_tags_raw)
            return r[m.Tests.ContainerInfo].ok(
                m.Tests.ContainerInfo(
                    name=container_name,
                    status=c.Tests.ContainerStatus(container.status),
                    ports=ports,
                    image=image_tags[0] if image_tags else "",
                    container_id=str(container.id),
                ),
            )
        except NotFound:
            return r[m.Tests.ContainerInfo].fail(
                f"Container {container_name} not found",
            )
        except c.EXC_BROAD_RUNTIME as exc:
            return r[m.Tests.ContainerInfo].fail(str(exc))

    def fetch_container_status(
        self, container_name: str
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Fetch container status."""
        return self.fetch_container_info(container_name)

    def start_existing_container(self, container_name: str) -> p.Result[bool]:
        """Start an existing stopped container by name."""
        try:
            client = self.client
            if client is None:
                error = self.client_error or "Docker daemon unavailable"
                return r[bool].fail(error)
            container = client.containers.get(container_name)
            if container.status == "running":
                return r[bool].ok(value=True)
            container.start()
            return r[bool].ok(value=True)
        except NotFound:
            return r[bool].fail(f"Container {container_name} not found")
        except (DockerException, OSError, RuntimeError, AttributeError) as exc:
            return r[bool].fail(f"Failed to start container {container_name}: {exc}")

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


__all__: list[str] = ["FlextTestsDocker"]
