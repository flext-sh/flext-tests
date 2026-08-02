"""Reusable black-box launcher for the flext-tests pytest shard plugin."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING, cast

import pytest

if TYPE_CHECKING:
    from contextlib import AbstractContextManager

type ManifestValue = int | str | list[str] | dict[str, str]
type Manifest = dict[str, ManifestValue]


class _EnvironmentScope:
    """Restore the inherited plugin-autoload setting after a nested run."""

    previous: str | None = None

    def __enter__(self) -> None:
        self.previous = os.environ.get("PYTEST_DISABLE_PLUGIN_AUTOLOAD")
        os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        _ = exception_type, exception, traceback
        if self.previous is None:
            os.environ.pop("PYTEST_DISABLE_PLUGIN_AUTOLOAD", None)
        else:
            os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = self.previous


class PytestShardRunner:
    """Run the installed pytest11 plugin in one isolated pytester sandbox."""

    @staticmethod
    def autoload_disabled() -> AbstractContextManager[None]:
        """Keep unrelated installed entry points out of a nested pytest process."""
        return _EnvironmentScope()

    @classmethod
    def run(
        cls,
        pytester: pytest.Pytester,
        *,
        shard_count: int,
        shard_index: int,
        max_workers: int,
        manifest: Path,
    ) -> pytest.RunResult:
        """Execute one fixed-worker shard under the public plugin entry module."""
        arguments = (
            "-p",
            "xdist.plugin",
            "-p",
            "flext_tests.conftest_plugin",
            "-n",
            str(max_workers),
            "--dist=worksteal",
            f"--flext-shard-count={shard_count}",
            f"--flext-shard-index={shard_index}",
            f"--flext-shard-max-workers={max_workers}",
            "--flext-shard-assignment=sha256-mod-v1",
            f"--flext-shard-manifest={manifest}",
            "-q",
        )
        with cls.autoload_disabled():
            return pytester.runpytest_subprocess(*arguments, timeout=8)

    @staticmethod
    def manifest(path: Path) -> Manifest:
        """Read one plugin-produced JSON manifest for behavioral assertions."""
        return cast("Manifest", json.loads(path.read_text(encoding="utf-8")))

    @staticmethod
    def index(nodeid: str, shard_count: int) -> int:
        """Independently apply the immutable sha256-mod-v1 protocol."""
        digest = hashlib.sha256(nodeid.encode("utf-8")).hexdigest()
        return int(digest, 16) % shard_count

    @staticmethod
    def nodeids() -> tuple[str, ...]:
        """Return the canonical nodeids written by ``write_cases``."""
        return (
            "test_cases.py::test_alpha",
            "test_cases.py::test_beta",
            "test_cases.py::test_delta",
            "test_cases.py::test_gamma",
        )

    @staticmethod
    def write_cases(pytester: pytest.Pytester) -> None:
        """Write an intentionally non-sorted collection for canonicalization."""
        pytester.makepyfile(
            test_cases=(
                "def test_gamma() -> None:\n    pass\n\n"
                "def test_alpha() -> None:\n    pass\n\n"
                "def test_delta() -> None:\n    pass\n\n"
                "def test_beta() -> None:\n    pass\n"
            )
        )


__all__: list[str] = ["Manifest", "PytestShardRunner"]
