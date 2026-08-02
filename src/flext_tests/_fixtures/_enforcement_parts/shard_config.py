"""Typed pytest launcher configuration for external shard execution."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import pytest

from flext_tests._fixtures._enforcement_parts.shard_manifest import (
    ASSIGNMENT,
    ShardOutcome,
    ShardSpec,
    WorkerRecord,
)

_MIN_SHARDS = 2
_MAX_WORKERS = 16
WORKER_PAYLOAD_KEY = "flext_shard"
SPEC_KEY = pytest.StashKey[ShardSpec | None]()
FULL_KEY = pytest.StashKey[tuple[str, ...]]()
SELECTED_KEY = pytest.StashKey[tuple[str, ...]]()
OUTCOMES_KEY = pytest.StashKey[dict[str, ShardOutcome]]()
ERRORS_KEY = pytest.StashKey[list[str]]()
WORKERS_KEY = pytest.StashKey[dict[str, WorkerRecord]]()
SEEN_WORKERS_KEY = pytest.StashKey[set[str]]()
PREVIOUS_CONFIG_KEY = pytest.StashKey[pytest.Config | None]()


class ShardSessionState:
    """Process-local active config for report-only pytest hooks."""

    config: ClassVar[pytest.Config | None] = None


def resolve_spec(config: pytest.Config) -> ShardSpec | None:
    """Parse and validate one complete fixed-worker shard invocation."""
    count = int(config.getoption("--flext-shard-count"))
    index = int(config.getoption("--flext-shard-index"))
    max_workers = int(config.getoption("--flext-shard-max-workers"))
    assignment = str(config.getoption("--flext-shard-assignment"))
    manifest_raw = str(config.getoption("--flext-shard-manifest"))
    values_present = (
        count > 0,
        index >= 0,
        max_workers > 0,
        bool(assignment),
        bool(manifest_raw),
    )
    if not any(values_present):
        return None
    if not all(values_present):
        message = "all --flext-shard-* options are required together"
        raise pytest.UsageError(message)
    if count < _MIN_SHARDS:
        message = "--flext-shard-count must be at least 2"
        raise pytest.UsageError(message)
    if not 0 <= index < count:
        message = "--flext-shard-index is outside the shard range"
        raise pytest.UsageError(message)
    if not 1 <= max_workers <= _MAX_WORKERS:
        message = "--flext-shard-max-workers must be between 1 and 16"
        raise pytest.UsageError(message)
    if assignment != ASSIGNMENT:
        message = f"unsupported shard assignment: {assignment}"
        raise pytest.UsageError(message)
    numprocesses = config.getoption("numprocesses", 0)
    if not isinstance(numprocesses, int) or numprocesses != max_workers:
        message = f"xdist worker count must be the fixed value {max_workers}"
        raise pytest.UsageError(message)
    if config.getoption("dist", "no") != "worksteal":
        message = "pytest shards require --dist=worksteal"
        raise pytest.UsageError(message)
    return count, index, max_workers, ASSIGNMENT, Path(manifest_raw).resolve()


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the complete typed external-shard launcher contract."""
    group = parser.getgroup("flext-shard", "FLEXT deterministic pytest sharding")
    group.addoption("--flext-shard-count", action="store", type=int, default=0)
    group.addoption("--flext-shard-index", action="store", type=int, default=-1)
    group.addoption("--flext-shard-max-workers", action="store", type=int, default=0)
    group.addoption("--flext-shard-assignment", action="store", default="")
    group.addoption("--flext-shard-manifest", action="store", default="")


@pytest.hookimpl(trylast=True)
def pytest_configure(config: pytest.Config) -> None:
    """Validate shard arguments after xdist resolves its fixed worker count."""
    config.stash[SPEC_KEY] = resolve_spec(config)
    config.stash[FULL_KEY] = ()
    config.stash[SELECTED_KEY] = ()
    config.stash[OUTCOMES_KEY] = {}
    config.stash[ERRORS_KEY] = []
    config.stash[WORKERS_KEY] = {}
    config.stash[SEEN_WORKERS_KEY] = set()


__all__: list[str] = [
    "ERRORS_KEY",
    "FULL_KEY",
    "OUTCOMES_KEY",
    "PREVIOUS_CONFIG_KEY",
    "SEEN_WORKERS_KEY",
    "SELECTED_KEY",
    "SPEC_KEY",
    "WORKERS_KEY",
    "WORKER_PAYLOAD_KEY",
    "ShardSessionState",
    "pytest_addoption",
    "pytest_configure",
    "resolve_spec",
]
