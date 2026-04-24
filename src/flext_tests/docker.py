"""Simplified Docker container control for FLEXT test infrastructure.

Essential container management using Python libraries only:
- docker SDK for container operations
- python_on_whales for docker-compose operations
- NO shell commands ever

Core functionality:
- Create/start containers via docker-compose
- Dirty state tracking for container recreation
- Port readiness checking

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import contextlib
import socket
import time
from collections.abc import (
    Mapping,
    MutableSequence,
    Sequence,
)
from pathlib import Path
from typing import ClassVar

from docker import DockerClient as DockerSDKClient, from_env as docker_from_env
from docker.errors import DockerException, NotFound
from docker.models.containers import Container
from python_on_whales import DockerClient as WhalesDockerClient
from python_on_whales.exceptions import DockerException as WhalesDockerException

from flext_tests import c, m, p, r, t, u

docker: WhalesDockerClient = WhalesDockerClient(client_type="docker")
logger: p.Logger = u.fetch_logger(__name__)


class FlextTestsDocker:
    """Simplified Docker container management for FLEXT tests.

    Essential functionality only:
    - Container creation via docker-compose (python_on_whales)
    - Container status/start/stop (docker SDK)
    - Dirty state tracking for container recreation
    - Port readiness checking
    """

    ContainerStatus: ClassVar[type[c.Tests.ContainerStatus]] = c.Tests.ContainerStatus

    class ContainerInfo(m.Tests.ContainerInfo):
        """Container information model for tests - real inheritance from m."""

    SHARED_CONTAINERS: ClassVar[Mapping[str, t.HeaderMapping]] = (
        c.Tests.SHARED_CONTAINERS
    )

    class _OfflineContainers:
        """Minimal container manager that always reports not found.

        Does NOT inherit from ContainerCollection (which is untyped in docker SDK).
        Instead, implements the same interface via composition and protocol.
        """

        def get(self, container_id: str) -> Container:
            """Raise NotFound for any container lookup.

            Business Rule: Always raises NotFound.
            This is intentional for offline mode - containers are not available.
            """
            msg = f"Container {container_id} not found (offline client)"
            raise NotFound(msg)

    class _OfflineDockerClient:
        """Offline Docker client used when the daemon is unavailable.

        Does NOT inherit from DockerClient (which is untyped in docker SDK).
        Instead, wraps the containers interface via composition.
        """

        def __init__(self) -> None:
            """Initialize offline Docker client without contacting daemon."""
            super().__init__()
            self._offline_containers: FlextTestsDocker._OfflineContainers = (
                FlextTestsDocker._OfflineContainers()
            )

        @property
        def containers(self) -> FlextTestsDocker._OfflineContainers:
            """Return offline container manager."""
            return self._offline_containers

    def __init__(
        self,
        workspace_root: Path | None = None,
        worker_id: str | None = None,
    ) -> None:
        """Initialize Docker client with dirty state tracking."""
        super().__init__()
        self._client: DockerSDKClient | FlextTestsDocker._OfflineDockerClient | None = (
            None
        )
        self.logger: p.Logger = u.fetch_logger(__name__)
        self.workspace_root: Path = workspace_root or Path.cwd()
        self.worker_id: str = worker_id or "master"
        self._dirty_containers: set[str] = set()
        self._state_file: Path = (
            Path.home() / ".flext" / f"docker_state_{self.worker_id}.json"
        )
        self._load_dirty_state()
        _ = self.client

    @property
    def shared_containers(self) -> Mapping[str, t.HeaderMapping]:
        """Get shared container configurations."""
        result: Mapping[str, t.HeaderMapping] = c.Tests.SHARED_CONTAINERS
        return result

    @staticmethod
    def _extract_host_port(bindings: Sequence[t.StrMapping] | None) -> str:
        if not isinstance(bindings, Sequence) or isinstance(bindings, str | bytes):
            return ""
        if not bindings:
            return ""
        first_binding = bindings[0]
        host_port = first_binding.get("HostPort", "")
        return str(host_port)

    @staticmethod
    def _normalize_bindings(
        bindings: t.Tests.TestobjectSerializable | None,
    ) -> Sequence[t.StrMapping]:
        try:
            validated: Sequence[t.StrMapping] = (
                t.Tests.STR_MAPPING_SEQUENCE_ADAPTER.validate_python(bindings)
            )
        except c.ValidationError:
            return []
        return validated

    def cleanup_dirty_containers(self) -> p.Result[t.StrSequence]:
        """Clean up all dirty containers by recreating them with fresh volumes."""
        cleaned: MutableSequence[str] = []
        for container_name in list(self._dirty_containers):
            settings = self.shared_containers.get(container_name)
            if not settings:
                continue
            compose_file = str(settings.get("compose_file", ""))
            if not compose_file:
                continue
            if not Path(compose_file).is_absolute():
                compose_file = str(self.workspace_root / compose_file)
            service = str(settings.get("service", ""))
            self.logger.info("Recreating dirty container", container=container_name)
            _ = self.compose_down(compose_file)
            result = self.compose_up(compose_file, service, force_recreate=True)
            if result.success:
                _ = self.mark_container_clean(container_name)
                cleaned.append(container_name)
        return r[t.StrSequence].ok(cleaned)

    def compose_down(self, compose_file: str) -> p.Result[str]:
        """Stop services using docker-compose via python_on_whales."""
        try:
            compose_path = Path(compose_file)
            if not compose_path.is_absolute():
                compose_path = self.workspace_root / compose_file
            original_files = docker.client_config.compose_files
            try:
                docker.client_config.compose_files = [str(compose_path)]
                docker.compose.down(volumes=True, remove_orphans=True)
            finally:
                docker.client_config.compose_files = original_files
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
            return r[str].fail(f"Compose down failed: {exc}")

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
            original_files = docker.client_config.compose_files
            try:
                docker.client_config.compose_files = [str(compose_path)]
                if force_recreate:
                    with contextlib.suppress(Exception):
                        docker.compose.down(remove_orphans=True, volumes=True)
                services = [service] if service else []
                docker.compose.up(services=services, detach=True, remove_orphans=True)
            finally:
                docker.client_config.compose_files = original_files
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
            return r[str].fail(f"Compose up failed: {exc}")

    @property
    def client(self) -> DockerSDKClient | FlextTestsDocker._OfflineDockerClient:
        """Docker client with lazy initialization.

        Returns either a real DockerClient connected to daemon, or an offline stub
        if the daemon is unavailable.
        """
        if self._client is None:
            try:
                self._client = docker_from_env()
            except (DockerException, OSError, TypeError, ValueError) as error:
                self.logger.exception(
                    "Failed to initialize Docker client",
                    error=str(error),
                )
                self._client = self._OfflineDockerClient()
        return self._client

    def fetch_container_info(
        self, container_name: str
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Fetch container information."""
        try:
            client = self.client
            container = client.containers.get(container_name)
            ports_raw: Mapping[str, t.Tests.TestobjectSerializable] = (
                t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER.validate_python(
                    container.ports
                )
            )
            ports: t.MutableStrMapping = {}
            for container_port, host_bindings in ports_raw.items():
                normalized_bindings = self._normalize_bindings(host_bindings)
                host_port = self._extract_host_port(normalized_bindings)
                if host_port:
                    ports[str(container_port)] = host_port
            status_val = str(container.status)
            image_obj = container.image
            image_tags_raw = image_obj.tags if image_obj is not None else ()
            image_tags = [str(tag) for tag in image_tags_raw]
            container_id = str(container.id)
            return r[m.Tests.ContainerInfo].ok(
                m.Tests.ContainerInfo(
                    name=container_name,
                    status=self.ContainerStatus(status_val),
                    ports=ports,
                    image=str(image_tags[0]) if image_tags else "",
                    container_id=container_id,
                ),
            )
        except NotFound:
            return r[m.Tests.ContainerInfo].fail(
                f"Container {container_name} not found",
            )
        except (AttributeError, KeyError, TypeError, ValueError, RuntimeError) as exc:
            return r[m.Tests.ContainerInfo].fail(str(exc))

    def fetch_container_status(
        self, container_name: str
    ) -> p.Result[m.Tests.ContainerInfo]:
        """Fetch container status."""
        return self.fetch_container_info(container_name)

    @property
    def dirty_containers(self) -> t.StrSequence:
        """Dirty container names."""
        return list(self._dirty_containers)

    def container_dirty(self, container_name: str) -> bool:
        """Whether a container is marked as dirty."""
        return container_name in self._dirty_containers

    def mark_container_clean(self, container_name: str) -> p.Result[bool]:
        """Mark a container as clean after successful recreation."""
        try:
            self._dirty_containers.discard(container_name)
            self._save_dirty_state()
            self.logger.info("Container marked clean", container=container_name)
            return r[bool].ok(value=True)
        except (OSError, TypeError) as exc:
            return r[bool].fail(f"Failed to mark clean: {exc}")

    def mark_container_dirty(self, container_name: str) -> p.Result[bool]:
        """Mark a container as dirty for recreation on next use."""
        try:
            self._dirty_containers.add(container_name)
            self._save_dirty_state()
            self.logger.info("Container marked dirty", container=container_name)
            return r[bool].ok(value=True)
        except (OSError, TypeError) as exc:
            return r[bool].fail(f"Failed to mark dirty: {exc}")

    def start_existing_container(self, container_name: str) -> p.Result[bool]:
        """Start an existing stopped container by name.

        Uses docker SDK to find and start the container. If already running,
        returns success. If not found, returns failure.
        """
        try:
            client = self.client
            container = client.containers.get(container_name)
            status = str(container.status)
            if status == "running":
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
            return r[str].fail(f"Stack start failed: {result.error}")
        return r[str].ok("Stack started successfully")

    def wait_for_port_ready(
        self,
        host: str,
        port: int,
        max_wait: int = 30,
    ) -> p.Result[bool]:
        """Wait until a TCP port is accepting connections.

        Returns ok(True) if the port becomes ready within the timeout,
        ok(False) if the timeout expires without the port becoming ready.
        Only returns failure for unexpected errors.
        """
        waited = 0.0
        while waited < max_wait:
            try:
                with socket.create_connection((host, port), timeout=1):
                    return r[bool].ok(value=True)
            except (ConnectionRefusedError, TimeoutError, OSError):
                time.sleep(0.5)
                waited += 0.5
        return r[bool].ok(value=False)

    def _load_dirty_state(self) -> None:
        """Load dirty container state from persistent storage."""
        try:
            if self._state_file.exists():
                state_text = self._state_file.read_text(encoding="utf-8")
                state_raw: Mapping[str, t.StrSequence] = (
                    t.Tests.STR_SEQUENCE_MAPPING_ADAPTER.validate_json(state_text)
                )
                dirty_raw = state_raw.get("dirty_containers", ())
                self._dirty_containers = {
                    str(container_name) for container_name in dirty_raw
                }
        except (OSError, ValueError, KeyError, TypeError) as exc:
            self.logger.warning("Failed to load dirty state", error=str(exc))
            self._dirty_containers = set[str]()

    def _save_dirty_state(self) -> None:
        """Save dirty container state to persistent storage."""
        try:
            self._state_file.parent.mkdir(parents=True, exist_ok=True)
            data: Mapping[str, t.StrSequence] = {
                "dirty_containers": list(self._dirty_containers),
            }
            json_bytes = t.Tests.STR_SEQUENCE_MAPPING_ADAPTER.dump_json(data)
            self._state_file.write_bytes(json_bytes)
        except (OSError, TypeError) as exc:
            self.logger.warning("Failed to save dirty state", error=str(exc))


tk = FlextTestsDocker

__all__: list[str] = ["FlextTestsDocker", "tk"]
