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

    from flext_cli import t


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
    DOCKER_CI_SKIP_REASON: ClassVar[str] = (
        "Docker lifecycle disabled under the Make CI token: "
        "container tests are not executed in CI"
    )
    DOCKER_UNREACHABLE_DESELECT_REASON: ClassVar[str] = (
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
    # Scratch root for relocated caches (hypothesis, benchmarks): never
    # inside the checkout; keyed per checkout identity under this root.
    SCRATCH_DIR_PARTS: ClassVar[t.VariadicTuple[str]] = (".flext", "scratch")
    SCRATCH_ROOT_INI: ClassVar[str] = "flext_scratch_root"
    # Docker's own container-name grammar; the name is also the state file stem.
    DOCKER_CONTAINER_NAME_PATTERN: ClassVar[str] = r"^[a-zA-Z0-9][a-zA-Z0-9_.-]+$"
    ERR_DOCKER_STATE_NAME_MISMATCH: ClassVar[str] = (
        "Container state {path} records {recorded!r}, expected {expected!r}"
    )

    # A mutation waits at most this long for other sessions' leases, then fails
    # LOCK_TIMEOUT; a target may declare its own bound.
    DOCKER_LEASE_TIMEOUT_SECONDS: ClassVar[float] = 120.0
    # Bounded condition polling of container health and readiness.
    DOCKER_HEALTH_POLL_SECONDS: ClassVar[float] = 0.5
    # Creation-only secrets reach compose through a 0600 env file in the state
    # directory that exists only for the duration of ``compose up``.
    DOCKER_ENV_FILE_SUFFIX: ClassVar[str] = ".creation.env"
    DOCKER_ENV_FILE_MODE: ClassVar[int] = 0o600
    DOCKER_TCP_PORT_SUFFIX: ClassVar[str] = "/tcp"
    DOCKER_TCP_CONNECT_TIMEOUT_SECONDS: ClassVar[float] = 1.0
    DOCKER_ENV_SEPARATOR: ClassVar[str] = "="
    # Values are written single-quoted, which compose reads literally; a quote
    # or a line break cannot be represented.
    DOCKER_ENV_FORBIDDEN_MARKS: ClassVar[t.VariadicTuple[str]] = ("'", "\n", "\r")
    DOCKER_FINGERPRINT_SEPARATOR: ClassVar[bytes] = b"\0"
    DOCKER_FINGERPRINT_SIZE_BYTES: ClassVar[int] = 8
    ERR_DOCKER_NOT_PROVISIONED: ClassVar[str] = "Container {name} does not exist"
    ERR_DOCKER_UNHEALTHY: ClassVar[str] = (
        "Container {name} is {status} with health {health}"
    )
    ERR_DOCKER_DIRTY: ClassVar[str] = (
        "Container {name} is marked dirty; the next ensure recreates it"
    )
    ERR_DOCKER_UNSEALED: ClassVar[str] = (
        "Container {name} ({container_id}) is not the one the lifecycle sealed"
    )
    ERR_DOCKER_FINGERPRINT_MISMATCH: ClassVar[str] = (
        "Container {name} was sealed for {sealed}; the declared inputs give {current}"
    )
    ERR_DOCKER_PORT_NOT_PUBLISHED: ClassVar[str] = (
        "Container {name} publishes no host port for {port}/tcp"
    )
    ERR_DOCKER_READINESS_TIMEOUT: ClassVar[str] = (
        "Container {name} not ready within {timeout}s: {detail}"
    )
    ERR_DOCKER_ENVIRONMENT_MISSING: ClassVar[str] = (
        "Container {name} environment lacks {keys}"
    )
    ERR_DOCKER_ENV_VALUE: ClassVar[str] = (
        "Creation value of {key} cannot be written to a compose env file: "
        "it contains a single quote or a line break"
    )
    ERR_DOCKER_TARGET_MISSING: ClassVar[str] = (
        "Docker target not configured. Use FlextTestsDocker.shared(...), "
        "FlextTestsDocker.compose(...), or FlextTestsDocker.stack(...)."
    )
    ERR_DOCKER_TARGET_NOT_INSPECTABLE: ClassVar[str] = (
        "Docker target has no inspection container or compose file configured. "
        "Use up()/down()/ready() for stack-only lifecycles."
    )
    ERR_DOCKER_KUBE_HOOKS_UNSUPPORTED: ClassVar[str] = (
        "The kind cluster lifecycle creates no sealed container: "
        "initializer and creation_environment do not apply"
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
    UNREACHABLE_DESELECT_REASON: ClassVar[str] = (
        "{marker} service unreachable at {host}:{port}; start it to run these tests"
    )
    CONNECTIVITY_PROBE_TIMEOUT_SECONDS: ClassVar[float] = 1.5

    # Shared-container compose files ship inside the flext_tests package under
    # this directory, so workspace and standalone checkouts resolve the same file.
    DOCKER_SHARED_ASSETS_DIR: ClassVar[str] = "assets"

    # ``compose_file`` is relative to DOCKER_SHARED_ASSETS_DIR. ``port`` is the
    # container port a service listens on; the host port it is published on is
    # read from the running container (u.Tests.resolve_host_port).
    SHARED_CONTAINERS: ClassVar[Mapping[str, t.HeaderMapping]] = MappingProxyType({
        "flext-openldap-test": MappingProxyType({
            "compose_file": "docker/docker-compose.openldap.yml",
            "service": "openldap",
            "port": 389,
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
        NOT_PROVISIONED = "NOT_PROVISIONED"
        UNHEALTHY = "UNHEALTHY"
        DIRTY = "DIRTY"
        UNSEALED = "UNSEALED"
        FINGERPRINT_MISMATCH = "FINGERPRINT_MISMATCH"
        PORT_NOT_PUBLISHED = "PORT_NOT_PUBLISHED"
        READINESS_TIMEOUT = "READINESS_TIMEOUT"
        ENVIRONMENT_MISSING = "ENVIRONMENT_MISSING"

    @unique
    class ContainerHealth(StrEnum):
        """Docker healthcheck state; UNKNOWN is Docker's ``none`` (no check)."""

        HEALTHY = "healthy"
        UNHEALTHY = "unhealthy"
        STARTING = "starting"
        UNKNOWN = "none"

    @unique
    class ContainerAction(StrEnum):
        """What an ensure does with a container and its host record."""

        CREATE = "create"
        START = "start"
        RECREATE = "recreate"
        REUSE = "reuse"

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
