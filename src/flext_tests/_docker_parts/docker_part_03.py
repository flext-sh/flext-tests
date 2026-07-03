"""Docker compose operations for flext-tests."""

from __future__ import annotations

from pathlib import Path

from python_on_whales.exceptions import DockerException as WhalesDockerException

from flext_tests import p, r
from flext_tests._docker_parts.docker_part_02 import (
    FlextTestsDocker as FlextTestsDockerPart02,
)


class FlextTestsDocker(FlextTestsDockerPart02):
    """Run low-level Docker compose operations."""

    def compose_down(self, compose_file: str) -> p.Result[str]:
        """Stop services using docker-compose via python_on_whales."""
        compose_path = self._compose_path(compose_file)
        try:
            self._run_compose_down(compose_path)
        except self._compose_exception_types() as exc:
            self.logger.warning("Compose down failed", error=str(exc))
            return r[str].fail_op("Compose down", exc)
        return r[str].ok("Compose down successful")

    def compose_up(
        self,
        compose_file: str,
        service: str | None = None,
        *,
        force_recreate: bool = False,
    ) -> p.Result[str]:
        """Start services using docker-compose via python_on_whales."""
        compose_path = self._compose_path(compose_file)
        try:
            cleanup_result = self._run_compose_up(
                compose_path,
                service,
                force_recreate=force_recreate,
            )
        except self._compose_exception_types() as exc:
            self.logger.exception("Compose up failed")
            return r[str].fail_op("Compose up", exc)
        if cleanup_result.failure:
            return cleanup_result
        return r[str].ok("Compose up successful")

    def _compose_path(self, compose_file: str) -> Path:
        """Resolve a compose path against the configured workspace root."""
        compose_path = Path(compose_file)
        return (
            compose_path
            if compose_path.is_absolute()
            else self.workspace_root / compose_file
        )

    @staticmethod
    def _compose_exception_types() -> tuple[type[Exception], ...]:
        """Return compose exception types handled by this adapter."""
        return (
            AttributeError,
            OSError,
            RuntimeError,
            TypeError,
            ValueError,
            WhalesDockerException,
        )

    def _run_compose_down(self, compose_path: Path) -> None:
        """Run compose down with temporary compose-file binding."""
        original_files = self.docker.client_config.compose_files
        try:
            self.docker.client_config.compose_files = [str(compose_path)]
            self.docker.compose.down(volumes=True, remove_orphans=True)
        finally:
            self.docker.client_config.compose_files = original_files

    def _run_compose_up(
        self,
        compose_path: Path,
        service: str | None,
        *,
        force_recreate: bool,
    ) -> p.Result[str]:
        """Run compose up with temporary compose-file binding."""
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

    def _compose_down_current_file(self) -> p.Result[str]:
        """Run compose down for the currently configured compose file."""
        try:
            self.docker.compose.down(remove_orphans=True, volumes=True)
        except self._compose_exception_types() as exc:
            self.logger.warning("Compose recreate cleanup failed", error=str(exc))
            return r[str].fail_op("Compose recreate cleanup", exc)
        return r[str].ok("Compose recreate cleanup successful")


__all__: list[str] = ["FlextTestsDocker"]
