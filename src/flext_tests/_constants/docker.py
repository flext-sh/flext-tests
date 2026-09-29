"""Docker test infrastructure constants for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, unique
from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from collections.abc import Mapping

    from flext_infra import t


class FlextTestsConstantsDocker:
    """Docker test infrastructure constants mixin."""

    # The Make CI token (variable and value) is owned by flext-infra
    # ``config.Infra.codegen.make.ci``; the lifecycle reads it from there and
    # never treats GitHub's CI=true as the token.
    ERR_DOCKER_DISABLED_BY_CI: ClassVar[str] = (
        "Docker lifecycle disabled under {variable}={value}: "
        "container tests are not executed in CI"
    )
    DOCKER_CONNECTIVITY_MARKER: ClassVar[str] = "docker"
    DOCKER_UNREACHABLE_SKIP_REASON: ClassVar[str] = (
        "Docker daemon unreachable; start it to run Docker integration tests"
    )
    # Default probe ceiling for callers that omit max_wait. Under the Make CI
    # token the lifecycle fails DISABLED_BY_CI before probing. Outside CI,
    # shared-container startup_timeout remains the SSOT for long boots.
    DOCKER_PROBE_MAX_WAIT_SECONDS: ClassVar[int] = 8

    # One state record per container name, shared by every checkout of the
    # host: ``<home>/<parts>/<name>.json``, rewritten atomically under
    # ``<name>.state.lock``. The session lease owns ``<name>.lease.lock`` so
    # marking a container dirty never waits on the sessions that use it.
    DOCKER_STATE_DIR_PARTS: ClassVar[t.VariadicTuple[str]] = (".flext", "docker")
    DOCKER_STATE_FILE_SUFFIX: ClassVar[str] = ".json"
    DOCKER_STATE_LOCK_SUFFIX: ClassVar[str] = ".state.lock"
    DOCKER_LEASE_LOCK_SUFFIX: ClassVar[str] = ".lease.lock"
    DOCKER_STATE_LOCK_TIMEOUT_SECONDS: ClassVar[float] = 30.0
    # Docker's own container-name grammar; the name is also the state file stem.
    DOCKER_CONTAINER_NAME_PATTERN: ClassVar[str] = r"^[a-zA-Z0-9][a-zA-Z0-9_.-]+$"
    ERR_DOCKER_STATE_NAME_MISMATCH: ClassVar[str] = (
        "Container state {path} records {recorded!r}, expected {expected!r}"
    )

    # Bounded condition polling of a non-blocking lock attempt.
    FILE_LOCK_POLL_SECONDS: ClassVar[float] = 0.05
    FILE_LOCK_MODE_SHARED: ClassVar[str] = "shared"
    FILE_LOCK_MODE_EXCLUSIVE: ClassVar[str] = "exclusive"
    ERR_FILE_LOCK_TIMEOUT: ClassVar[str] = (
        "{mode} lock on {path} not acquired within {timeout}s"
    )
    ERR_FILE_LOCK_POSIX_ONLY: ClassVar[str] = (
        "shared or bounded lock on {path} requires POSIX fcntl; "
        "msvcrt offers only a blocking exclusive lock"
    )

    # Connectivity markers auto-skip when their service is unreachable
    # (AGENTS.md: "tests that need external/docker services skip when
    # unreachable"). Each marker maps to the shared container whose declared
    # host/port is probed once per session. A marker absent from this map is
    # never skipped, so adding one is a deliberate data change.
    CONNECTIVITY_MARKER_CONTAINERS: ClassVar[Mapping[str, str]] = MappingProxyType({
        "oracle": "flext-oracle-db-test",
        "ldap": "flext-openldap-test",
        "kubernetes": "flext-kind-test",
    })
    CONNECTIVITY_MARKERS: ClassVar[t.VariadicTuple[str]] = (
        DOCKER_CONNECTIVITY_MARKER,
        *CONNECTIVITY_MARKER_CONTAINERS,
    )
    UNREACHABLE_SKIP_REASON: ClassVar[str] = (
        "{marker} service unreachable at {host}:{port}; start it to run these tests"
    )
    CONNECTIVITY_PROBE_TIMEOUT_SECONDS: ClassVar[float] = 1.5

    SHARED_CONTAINERS: ClassVar[Mapping[str, t.HeaderMapping]] = MappingProxyType({
        "flext-openldap-test": MappingProxyType({
            "compose_file": "docker/docker-compose.openldap.yml",
            "service": "openldap",
            "port": 3390,
            "host": "localhost",
        }),
        "flext-oracle-db-test": MappingProxyType({
            "compose_file": "docker/docker-compose.oracle-db.yml",
            "service": "oracle-db",
            "port": 1521,
            "host": "localhost",
            "startup_timeout": 900,
        }),
        "flext-kind-test": MappingProxyType({
            "compose_file": "docker/docker-compose.kubernetes.yml",
            "service": "kind",
            "port": 6443,
            "host": "localhost",
            "startup_timeout": 120,
        }),
    })

    @unique
    class DockerErrorCode(StrEnum):
        """Typed failure codes of the Docker test lifecycle."""

        DISABLED_BY_CI = "DISABLED_BY_CI"
        LOCK_TIMEOUT = "LOCK_TIMEOUT"

    @unique
    class ContainerStatus(StrEnum):
        """Container status enumeration for test infrastructure."""

        CREATED = "created"
        RUNNING = "running"
        EXITED = "exited"
        PAUSED = "paused"
        REMOVING = "removing"
        DEAD = "dead"
        STOPPED = "stopped"
        NOT_FOUND = "not_found"
        ERROR = "error"
        STARTING = "starting"
        STOPPING = "stopping"
        RESTARTING = "restarting"
