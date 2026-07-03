"""Docker client and dirty-state helpers for flext-tests."""

from __future__ import annotations

from pathlib import Path
from typing import override

from docker import DockerClient as DockerSDKClient, from_env as docker_from_env
from docker.errors import DockerException

from flext_tests import c, p, r, t, u
from flext_tests._docker_parts.docker_part_01 import (
    FlextTestsDocker as FlextTestsDockerPart01,
)


class FlextTestsDocker(FlextTestsDockerPart01):
    """Manage Docker client initialization and persisted dirty state."""

    @override
    def model_post_init(self, __context: t.JsonValue | None, /) -> None:
        """Initialize private runtime state after model validation."""
        super().model_post_init(__context)
        self.state_file_path = (
            Path.home() / ".flext" / f"docker_state_{self.worker_id}.json"
        )
        self._load_dirty_state()
        _ = self.client

    @property
    def client(self) -> DockerSDKClient | None:
        """Docker client with lazy initialization."""
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

    @property
    def dirty_containers(self) -> t.StrSequence:
        """Dirty container names."""
        return tuple(self.dirty_container_names)

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
        except c.EXC_OS_TYPE as exc:
            return r[bool].fail(f"Failed to mark clean: {exc}")

    def mark_container_dirty(self, container_name: str) -> p.Result[bool]:
        """Mark a container as dirty for recreation on next use."""
        try:
            self.dirty_container_names.add(container_name)
            self._save_dirty_state()
            self.logger.info("Container marked dirty", container=container_name)
            return r[bool].ok(value=True)
        except c.EXC_OS_TYPE as exc:
            return r[bool].fail(f"Failed to mark dirty: {exc}")

    def _load_dirty_state(self) -> None:
        """Load dirty container state from persistent storage."""
        state_file = self.state_file_path
        if state_file is None or not state_file.exists():
            return
        read = u.Cli.files_read_text(state_file)
        if read.failure:
            self.logger.warning("Failed to load dirty state", error=read.error)
            self.dirty_container_names = set[str]()
            return
        try:
            state_raw: t.MappingKV[str, t.StrSequence] = (
                t.Tests.STR_SEQUENCE_MAPPING_ADAPTER.validate_json(read.value)
            )
            self.dirty_container_names = set(state_raw.get("dirty_containers", ()))
        except c.EXC_KEY_OS_TYPE_VALUE as exc:
            self.logger.warning("Failed to load dirty state", error=str(exc))
            self.dirty_container_names = set[str]()

    def _save_dirty_state(self) -> None:
        """Save dirty container state to persistent storage."""
        state_file = self.state_file_path
        if state_file is None:
            return
        data: t.MappingKV[str, t.StrSequence] = {
            "dirty_containers": tuple(self.dirty_container_names),
        }
        write = u.Cli.json_write(state_file, data)
        if write.failure:
            self.logger.warning("Failed to save dirty state", error=write.error)


__all__: list[str] = ["FlextTestsDocker"]
