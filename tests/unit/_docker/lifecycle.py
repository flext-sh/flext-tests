"""Private docker lifecycle rule test mixins (no Docker daemon involved).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import stat
from collections.abc import Mapping, MutableMapping, Sequence
from pathlib import Path

from flext_tests import FlextTestsDocker
from tests import c, m, p, t, tm, u


class TestsFlextTestsDockerLifecycle:
    """Pure lifecycle rules: decision table, verification, projections."""

    @staticmethod
    def _info(
        status: c.Tests.ContainerStatus,
        health: c.Tests.ContainerHealth,
        container_id: str = "sealed-id",
    ) -> p.Tests.ContainerInfo:
        return m.Tests.ContainerInfo(
            name="lifecycle-rule",
            status=status,
            ports={},
            image="fixture:latest",
            container_id=container_id,
            health=health,
        )

    @staticmethod
    def test_generated_secrets_cover_declared_keys_and_are_writable() -> None:
        """Each declared key gets its own fresh value an env file can carry."""
        for name in c.Tests.SHARED_CONTAINERS:
            keys = FlextTestsDocker.shared_target_config(name).secret_keys
            first = u.Tests.generate_creation_secrets(keys)
            second = u.Tests.generate_creation_secrets(keys)
            tm.that(tuple(first), eq=keys)
            tm.ok(u.Tests.validate_creation_environment(first))
            values = {secret.get_secret_value() for secret in first.values()}
            tm.that(len(values), eq=len(keys))
            tm.that(
                values.isdisjoint(
                    secret.get_secret_value() for secret in second.values()
                ),
                truth=True,
            )

    @staticmethod
    def test_caller_cannot_supply_a_generated_secret() -> None:
        """An owned secret key from the caller fails before any effect."""
        for name in c.Tests.SHARED_CONTAINERS:
            keys = FlextTestsDocker.shared_target_config(name).secret_keys
            if not keys:
                continue
            supplied = {keys[0]: t.SecretStr("caller-value")}
            result = FlextTestsDocker.shared(name).execute(
                creation_environment=supplied,
            )
            tm.fail(result, has=keys[0])

    def test_host_port_is_read_from_published_bindings(self) -> None:
        """A published TCP port resolves; an unpublished one fails typed."""
        info = self._info(
            c.Tests.ContainerStatus.RUNNING,
            c.Tests.ContainerHealth.HEALTHY,
        ).model_copy(update={"ports": {"80/tcp": "49153"}})
        tm.that(tm.ok(u.Tests.resolve_host_port(info, 80)), eq=49153)
        tm.fail(
            u.Tests.resolve_host_port(info, 443),
            code=c.Tests.DockerErrorCode.PORT_NOT_PUBLISHED,
        )

    @staticmethod
    def _inspect(
        health: Mapping[str, str] | None,
        env: Sequence[str] | None,
    ) -> p.Tests.ContainerInspect:
        state: MutableMapping[str, str | Mapping[str, str]] = {"Status": "running"}
        if health is not None:
            state["Health"] = health
        return m.Tests.ContainerInspect.model_validate({
            "Id": "0123456789ab",
            "Image": "sha256:feedface",
            "Name": "/lifecycle-rule",
            "State": state,
            "Config": {"Image": "nginx:alpine", "Env": env, "Labels": {}},
            "NetworkSettings": {
                "Ports": {
                    "80/tcp": [{"HostIp": "127.0.0.1", "HostPort": "49153"}],
                    "443/tcp": None,
                },
            },
        })

    def test_inspect_projects_onto_container_info(self) -> None:
        """Inspect data becomes the typed view: ids, image, published ports."""
        info = u.Tests.container_info(
            "lifecycle-rule",
            self._inspect({"Status": "healthy"}, None),
        )
        tm.that(info.container_id, eq="0123456789ab")
        tm.that(info.image, eq="nginx:alpine")
        tm.that(info.image_id, eq="sha256:feedface")
        tm.that(info.status, eq=c.Tests.ContainerStatus.RUNNING)
        tm.that(info.health, eq=c.Tests.ContainerHealth.HEALTHY)
        tm.that(dict(info.ports), eq={"80/tcp": "49153"})

    def test_inspect_without_healthcheck_is_unknown_health(self) -> None:
        """No Health block, or Docker's 'none', both read as UNKNOWN."""
        for health in (None, {"Status": "none"}):
            info = u.Tests.container_info("lifecycle-rule", self._inspect(health, None))
            tm.that(info.health, eq=c.Tests.ContainerHealth.UNKNOWN)

    def test_container_environment_returns_secrets_and_names_missing_keys(self) -> None:
        """Values come back as secrets; a missing key is named, never a value."""
        inspect = self._inspect(None, ["PLAIN=1", "WITH_EQ=a=b", "BARE"])
        environment = tm.ok(
            u.Tests.container_environment(
                "lifecycle-rule",
                inspect,
                ["PLAIN", "WITH_EQ"],
            ),
        )
        tm.that(environment["PLAIN"].get_secret_value(), eq=c.ParserBooleanToken.ONE)
        tm.that(environment["WITH_EQ"].get_secret_value(), eq="a=b")
        tm.that(str(environment["PLAIN"]), lacks=c.ParserBooleanToken.ONE)
        missing = u.Tests.container_environment(
            "lifecycle-rule",
            inspect,
            ["PLAIN", "ABSENT", "BARE"],
        )
        tm.fail(
            missing,
            code=c.Tests.DockerErrorCode.ENVIRONMENT_MISSING,
            has=["ABSENT", "BARE"],
            lacks="PLAIN",
        )

    @staticmethod
    def test_creation_env_file_is_private_and_removed(tmp_path: Path) -> None:
        """Creation values live in a 0600 file only inside the block."""
        environment = {"FLEXT_TESTS_SECRET": t.SecretStr("s3cr=t value")}
        with u.Tests.creation_env_file(tmp_path, "env-owner", environment) as env_files:
            (env_file,) = env_files
            tm.that(stat.S_IMODE(env_file.stat().st_mode), eq=0o600)
            tm.that(
                env_file.read_text(encoding="utf-8"),
                eq="FLEXT_TESTS_SECRET='s3cr=t value'\n",
            )
        tm.fail(env_file.exists())
        with u.Tests.creation_env_file(tmp_path, "env-owner", {}) as no_files:
            tm.that(no_files, eq=())

    @staticmethod
    def test_creation_env_file_never_overwrites_a_leftover(
        tmp_path: Path,
    ) -> None:
        """A file left by an interrupted run fails instead of being replaced."""
        leftover = tmp_path / f"env-owner{c.Tests.DOCKER_ENV_FILE_SUFFIX}"
        _ = leftover.write_text("LEFT=over\n", encoding="utf-8")
        environment = {"FLEXT_TESTS_SECRET": t.SecretStr("value")}
        with (
            u.Tests.raises(FileExistsError),
            u.Tests.creation_env_file(tmp_path, "env-owner", environment),
        ):
            tm.ok(leftover.exists())
        tm.that(leftover.read_text(encoding="utf-8"), eq="LEFT=over\n")

    @staticmethod
    def test_unrepresentable_creation_value_is_rejected() -> None:
        """A quote or line break cannot be written literally and is refused."""
        for value in ("it's", "two\nlines"):
            tm.fail(
                u.Tests.validate_creation_environment({"KEY": t.SecretStr(value)}),
                has="KEY",
            )
        tm.ok(u.Tests.validate_creation_environment({"KEY": t.SecretStr("fine")}))
