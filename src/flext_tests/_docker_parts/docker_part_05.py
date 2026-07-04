"""Docker fluent DSL helpers for flext-tests."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from flext_tests import c, m, p, r, t
from flext_tests._docker_parts.docker_part_04 import (
    FlextTestsDocker as FlextTestsDockerPart04,
)


class FlextTestsDocker(FlextTestsDockerPart04):
    """Expose fluent Docker DSL helpers."""

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
        return cls(
            workspace_root=resolved_root,
            worker_id=worker_id or "master",
            target_config=cls._resolve_shared_target_config(
                container_name,
                resolved_root,
            ),
        )

    @classmethod
    def compose(
        cls,
        compose_file: str | Path,
        *,
        target: m.Tests.ContainerConfig | None = None,
        workspace_root: Path | None = None,
    ) -> Self:
        """Build a DSL-configured service for an explicit compose target."""
        resolved_root = workspace_root or Path.cwd()
        compose_path = Path(compose_file)
        if not compose_path.is_absolute():
            compose_path = resolved_root / compose_path
        base_target = target or m.Tests.ContainerConfig()
        return cls(
            workspace_root=resolved_root,
            worker_id="master",
            target_config=base_target.model_copy(
                update={"compose_file": compose_path},
            ),
        )

    @classmethod
    def stack(
        cls,
        compose_file: str | Path,
        *,
        target: m.Tests.ContainerConfig | None = None,
        workspace_root: Path | None = None,
    ) -> Self:
        """Build a DSL-configured service for a compose stack target."""
        return cls.compose(
            compose_file,
            target=target,
            workspace_root=workspace_root,
        )

    def up(self) -> p.Result[str]:
        """Start the configured compose target using the DSL state."""
        target = self.target_config
        if target is None:
            return r[str].fail(
                "Docker target not configured. Use tk.shared(...), tk.compose(...), or tk.stack(...).",
            )
        if target.compose_file is None:
            return r[str].fail(
                "Docker target has no compose file configured.",
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
        if target.compose_file is None:
            return r[str].fail(
                "Docker target has no compose file configured.",
            )
        return self.compose_down(str(target.compose_file))

    def ready(
        self,
        *,
        port: int | None = None,
        max_wait: int | None = None,
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

    def cleanup_dirty_containers(self) -> p.Result[t.StrSequence]:
        """Clean up all dirty containers by recreating them with fresh volumes."""
        cleaned: list[str] = []
        for container_name in list(self.dirty_container_names):
            if container_name not in c.Tests.SHARED_CONTAINERS:
                self.logger.warning(
                    "Removing stale dirty container entry",
                    container=container_name,
                )
                _ = self.mark_container_clean(container_name)
                continue
            target = self._resolve_shared_target_config(
                container_name,
                self.workspace_root,
            )
            self.logger.info("Recreating dirty container", container=container_name)
            _ = self.compose_down(str(target.compose_file))
            result = self.compose_up(
                str(target.compose_file),
                target.service,
                force_recreate=True,
            )
            if result.success:
                _ = self.mark_container_clean(container_name)
                cleaned.append(container_name)
        return r[t.StrSequence].ok(tuple(cleaned))


__all__: list[str] = ["FlextTestsDocker"]
