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
    MutableSequence,
    MutableSet,
    Sequence,
)
from pathlib import Path
from typing import Annotated, ClassVar, Self, override

from docker import DockerClient as DockerSDKClient, from_env as docker_from_env
from docker.errors import DockerException, NotFound
from python_on_whales import DockerClient as WhalesDockerClient
from python_on_whales.exceptions import DockerException as WhalesDockerException

from flext_tests import c, m, p, r, t, u
from flext_tests._typings.base import FlextTestsBaseTypesMixin
from flext_tests.base import s


class FlextTestsDocker(s[m.Tests.ContainerInfo]):
    """Simplified Docker container management for FLEXT tests.

    Essential functionality only:
    - Container creation via docker-compose (python_on_whales)
    - Container status/start/stop (docker SDK)
    - Dirty state tracking for container recreation
    - Port readiness checking
    """

    docker: ClassVar[WhalesDockerClient] = WhalesDockerClient(client_type="docker")
    workspace_root: Annotated[
        Path,
        u.Field(description="Workspace root used to resolve compose files."),
    ] = u.Field(default_factory=Path.cwd)
    worker_id: Annotated[
        str,
        u.Field(description="Worker identifier used to isolate persisted state."),
    ] = "master"
    docker_client: Annotated[
        DockerSDKClient | None,
        u.Field(exclude=True, description="Cached Docker SDK client instance."),
    ] = None
    client_error: Annotated[
        str | None,
        u.Field(exclude=True, description="Last Docker client initialization error."),
    ] = None
    dirty_container_names: Annotated[
        MutableSet[str],
        u.Field(exclude=True, description="Tracked dirty containers for the worker."),
    ] = u.Field(default_factory=set)
    state_file_path: Annotated[
        Path | None,
        u.Field(
            exclude=True, description="Persistent state file for dirty containers."
        ),
    ] = None
    target_config: Annotated[
        m.Tests.ContainerConfig | None,
        u.Field(description="Configured Docker target used by the public DSL."),
    ] = None

    @classmethod
    def shared(
        cls,
        container_name: str,
        *,
        workspace_root: Path | None = None,
        worker_id: str | None = None,
    ) -> Self:
        """Build a DSL-configured service from a shared container constant."""
        resolved_root = workspace_root or Path.cwd()
        settings = c.Tests.SHARED_CONTAINERS.get(container_name)
        if settings is None:
            msg = f"Unknown shared container: {container_name}"
            raise ValueError(msg)
        compose_path = Path(str(settings.get("compose_file", "")))
        if not compose_path.is_absolute():
            compose_path = resolved_root / compose_path
        port_value = settings.get("port")
        port = (
            port_value
            if isinstance(port_value, int)
            else int(str(port_value))
            if str(port_value).isdigit()
            else None
        )
        return cls(
            workspace_root=resolved_root,
            worker_id=worker_id or "master",
            target_config=m.Tests.ContainerConfig(
                container_name=container_name,
                compose_file=compose_path,
                service=str(settings.get("service", "")),
                host=str(settings.get("host", c.LOCALHOST)),
                port=port,
            ),
        )

    @classmethod
    def compose(
        cls,
        compose_file: str | Path,
        *,
        container_name: str | None = None,
        service: str = "",
        host: str = c.LOCALHOST,
        port: int | None = None,
        startup_timeout: int = 30,
        force_recreate: bool = False,
        workspace_root: Path | None = None,
        worker_id: str | None = None,
    ) -> Self:
        """Build a DSL-configured service for an explicit compose target."""
        resolved_root = workspace_root or Path.cwd()
        compose_path = Path(compose_file)
        if not compose_path.is_absolute():
            compose_path = resolved_root / compose_path
        return cls(
            workspace_root=resolved_root,
            worker_id=worker_id or "master",
            target_config=m.Tests.ContainerConfig(
                container_name=container_name,
                compose_file=compose_path,
                service=service,
                host=host,
                port=port,
                startup_timeout=startup_timeout,
                force_recreate=force_recreate,
            ),
        )

    @classmethod
    def stack(
        cls,
        compose_file: str | Path,
        *,
        container_name: str | None = None,
        service: str = "",
        host: str = c.LOCALHOST,
        port: int | None = None,
        startup_timeout: int = 30,
        force_recreate: bool = False,
        workspace_root: Path | None = None,
        worker_id: str | None = None,
    ) -> Self:
        """Build a DSL-configured service for a compose stack target."""
        return cls.compose(
            compose_file,
            container_name=container_name,
            service=service,
            host=host,
            port=port,
            startup_timeout=startup_timeout,
            force_recreate=force_recreate,
            workspace_root=workspace_root,
            worker_id=worker_id,
        )

    @override
    def model_post_init(self, __context: t.JsonValue | None, /) -> None:
        """Initialize private runtime state after model validation."""
        super().model_post_init(__context)
        self.state_file_path = (
            Path.home() / ".flext" / f"docker_state_{self.worker_id}.json"
        )
        self._load_dirty_state()
        _ = self.client

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
        if target.force_recreate or self.container_dirty(target.container_name):
            compose_result = self.compose_up(
                str(target.compose_file),
                service=target.service or None,
                force_recreate=True,
            )
            if compose_result.failure:
                return r[m.Tests.ContainerInfo].fail(
                    compose_result.error or "Failed to recreate Docker target",
                )
            _ = self.mark_container_clean(target.container_name)
        else:
            status_result = self.fetch_container_status(target.container_name)
            container_running = status_result.success and (
                status_result.value.status == c.Tests.ContainerStatus.RUNNING
            )
            if not container_running:
                start_result = self.start_existing_container(target.container_name)
                if start_result.failure:
                    compose_result = self.compose_up(
                        str(target.compose_file),
                        service=target.service or None,
                    )
                    if compose_result.failure:
                        return r[m.Tests.ContainerInfo].fail(
                            compose_result.error or "Failed to start Docker target",
                        )
        container_info_result = self.fetch_container_info(target.container_name)
        if container_info_result.failure:
            return container_info_result
        if target.port is not None:
            ready_port = self._resolve_readiness_port(
                target, container_info_result.value
            )
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

    def up(self) -> p.Result[str]:
        """Start the configured compose target using the DSL state."""
        target = self.target_config
        if target is None:
            return r[str].fail(
                "Docker target not configured. Use tk.shared(...), tk.compose(...), or tk.stack(...).",
            )
        return self.compose_up(
            str(target.compose_file),
            service=target.service or None,
            force_recreate=target.force_recreate,
        )

    def down(self) -> p.Result[str]:
        """Stop the configured compose target using the DSL state."""
        target = self.target_config
        if target is None:
            return r[str].fail(
                "Docker target not configured. Use tk.shared(...), tk.compose(...), or tk.stack(...).",
            )
        return self.compose_down(str(target.compose_file))

    def ready(
        self, *, port: int | None = None, max_wait: int | None = None
    ) -> p.Result[bool]:
        """Run a readiness check against the configured target."""
        target = self.target_config
        if target is None:
            return r[bool].fail(
                "Docker target not configured. Use tk.shared(...), tk.compose(...), or tk.stack(...).",
            )
        resolved_port = target.port if port is None else port
        if resolved_port is None:
            return r[bool].fail(
                f"Docker target {target.container_name} has no configured readiness port.",
            )
        return self.wait_for_port_ready(
            target.host,
            resolved_port,
            max_wait=target.startup_timeout if max_wait is None else max_wait,
        )

    @staticmethod
    def _resolve_readiness_port(
        target: m.Tests.ContainerConfig,
        info: m.Tests.ContainerInfo,
    ) -> int | None:
        if target.port is None:
            return None
        target_port_str = str(target.port)
        for container_port, host_port in info.ports.items():
            if container_port.startswith(f"{target_port_str}/"):
                return int(host_port)
            if host_port == target_port_str:
                return int(host_port)
        return int(target_port_str) if target_port_str.isdigit() else None

    @staticmethod
    def _extract_host_port(bindings: t.SequenceOf[t.StrMapping] | None) -> str:
        if not isinstance(bindings, Sequence) or isinstance(bindings, str | bytes):
            return ""
        if not bindings:
            return ""
        first_binding = bindings[0]
        host_port = first_binding.get("HostPort", "")
        return host_port if isinstance(host_port, str) else str(host_port)

    @staticmethod
    def _normalize_bindings(
        bindings: FlextTestsBaseTypesMixin.TestobjectSerializable | None,
    ) -> t.SequenceOf[t.StrMapping]:
        try:
            validated: t.SequenceOf[t.StrMapping] = (
                FlextTestsBaseTypesMixin.STR_MAPPING_SEQUENCE_ADAPTER.validate_python(
                    bindings
                )
            )
        except c.ValidationError:
            return []
        return validated

    def cleanup_dirty_containers(self) -> p.Result[t.StrSequence]:
        """Clean up all dirty containers by recreating them with fresh volumes."""
        cleaned: MutableSequence[str] = []
        for container_name in list(self.dirty_container_names):
            settings = c.Tests.SHARED_CONTAINERS.get(container_name)
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
            original_files = self.docker.client_config.compose_files
            try:
                self.docker.client_config.compose_files = [str(compose_path)]
                if force_recreate:
                    with contextlib.suppress(Exception):
                        self.docker.compose.down(remove_orphans=True, volumes=True)
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
            return r[str].fail(f"Compose up failed: {exc}")

    @property
    def client(self) -> DockerSDKClient | None:
        """Docker client with lazy initialization.

        Returns a real Docker client when the daemon is reachable.
        Returns None when the daemon is unavailable.
        """
        if self.docker_client is None:
            try:
                self.docker_client = docker_from_env()
                self.client_error = None
            except (DockerException, OSError, TypeError, ValueError) as error:
                self.logger.exception(
                    "Failed to initialize Docker client",
                    error=str(error),
                )
                self.client_error = str(error)
        return self.docker_client

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
            ports_raw: t.MappingKV[
                str, FlextTestsBaseTypesMixin.TestobjectSerializable
            ] = FlextTestsBaseTypesMixin.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER.validate_python(
                container.ports
            )
            ports: t.MutableStrMapping = {}
            for container_port, host_bindings in ports_raw.items():
                normalized_bindings = self._normalize_bindings(host_bindings)
                host_port = self._extract_host_port(normalized_bindings)
                if host_port:
                    ports[container_port] = host_port
            status_val = container.status
            image_obj = container.image
            image_tags_raw = image_obj.tags if image_obj is not None else ()
            image_tags = list(image_tags_raw)
            container_id = str(container.id)
            return r[m.Tests.ContainerInfo].ok(
                m.Tests.ContainerInfo(
                    name=container_name,
                    status=c.Tests.ContainerStatus(status_val),
                    ports=ports,
                    image=image_tags[0] if image_tags else "",
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
        return list(self.dirty_container_names)

    def container_dirty(self, container_name: str) -> bool:
        """Whether a container is marked as dirty."""
        return container_name in self.dirty_container_names

    def mark_container_clean(self, container_name: str) -> p.Result[bool]:
        """Mark a container as clean after successful recreation."""
        try:
            self.dirty_container_names.discard(container_name)
            self._save_dirty_state()
            self.logger.info("Container marked clean", container=container_name)
            return r[bool].ok(value=True)
        except (OSError, TypeError) as exc:
            return r[bool].fail(f"Failed to mark clean: {exc}")

    def mark_container_dirty(self, container_name: str) -> p.Result[bool]:
        """Mark a container as dirty for recreation on next use."""
        try:
            self.dirty_container_names.add(container_name)
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
            if client is None:
                error = self.client_error or "Docker daemon unavailable"
                return r[bool].fail(error)
            container = client.containers.get(container_name)
            status = container.status
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
            state_file = self.state_file_path
            if state_file is not None and state_file.exists():
                state_text = state_file.read_text(encoding=c.Tests.DEFAULT_ENCODING)
                state_raw: t.MappingKV[str, t.StrSequence] = (
                    FlextTestsBaseTypesMixin.STR_SEQUENCE_MAPPING_ADAPTER.validate_json(
                        state_text
                    )
                )
                dirty_raw = state_raw.get("dirty_containers", ())
                self.dirty_container_names = set(dirty_raw)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            self.logger.warning("Failed to load dirty state", error=str(exc))
            self.dirty_container_names = set[str]()

    def _save_dirty_state(self) -> None:
        """Save dirty container state to persistent storage."""
        try:
            state_file = self.state_file_path
            if state_file is None:
                return
            state_file.parent.mkdir(parents=True, exist_ok=True)
            data: t.MappingKV[str, t.StrSequence] = {
                "dirty_containers": list(self.dirty_container_names),
            }
            json_bytes = (
                FlextTestsBaseTypesMixin.STR_SEQUENCE_MAPPING_ADAPTER.dump_json(data)
            )
            state_file.write_bytes(json_bytes)
        except (OSError, TypeError) as exc:
            self.logger.warning("Failed to save dirty state", error=str(exc))


tk = FlextTestsDocker

__all__: list[str] = ["FlextTestsDocker", "tk"]
