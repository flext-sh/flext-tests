"""Docker base model and small helpers for flext-tests."""

from __future__ import annotations

from collections.abc import MutableSet, Sequence
from pathlib import Path
from typing import Annotated, ClassVar

from docker import DockerClient as DockerSDKClient
from python_on_whales import DockerClient as WhalesDockerClient

from flext_tests import c, m, p, s, t, u


class FlextTestsDocker(s[m.Tests.ContainerInfo]):
    """Docker model fields and pure helper methods."""

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
        u.Field(exclude=True, description="Persistent dirty container state file."),
    ] = None
    target_config: Annotated[
        m.Tests.ContainerConfig | None,
        u.Field(description="Configured Docker target used by the public DSL."),
    ] = None

    @staticmethod
    def _resolve_shared_target_config(
        container_name: str,
        workspace_root: Path,
    ) -> m.Tests.ContainerConfig:
        """Resolve one shared-container entry into the canonical target config."""
        settings = c.Tests.SHARED_CONTAINERS.get(container_name)
        if settings is None:
            msg = f"Unknown shared container: {container_name}"
            raise ValueError(msg)
        compose_file_raw = settings.get("compose_file")
        if not compose_file_raw:
            msg = f"Shared container '{container_name}' missing compose_file"
            raise ValueError(msg)
        target = m.Tests.ContainerConfig.model_validate({
            **settings,
            "compose_file": Path(str(compose_file_raw)),
        })
        compose_path = target.compose_file
        if not compose_path.is_absolute():
            compose_path = workspace_root / compose_path
        return target.model_copy(
            update={"container_name": container_name, "compose_file": compose_path},
        )

    @staticmethod
    def _resolve_readiness_port(
        target: m.Tests.ContainerConfig,
        info: m.Tests.ContainerInfo,
    ) -> int | None:
        """Resolve the host port used by a target readiness check."""
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
        """Extract the first Docker HostPort value from normalized bindings."""
        if not isinstance(bindings, Sequence) or isinstance(bindings, str | bytes):
            return ""
        if not bindings:
            return ""
        host_port = bindings[0].get("HostPort", "")
        return host_port if isinstance(host_port, str) else str(host_port)

    @staticmethod
    def _normalize_bindings(
        bindings: t.Tests.TestobjectSerializable | None,
    ) -> p.Result[t.SequenceOf[t.StrMapping]]:
        """Validate Docker SDK port bindings into a typed sequence."""
        return u.try_(
            lambda: t.Tests.STR_MAPPING_SEQUENCE_ADAPTER.validate_python(bindings),
            catch=c.ValidationError,
            op_name="normalize Docker port bindings",
        )


__all__: list[str] = ["FlextTestsDocker"]
