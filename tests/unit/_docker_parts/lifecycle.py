"""Private docker lifecycle rule test mixins (no Docker daemon involved).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import stat
from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker, m, tm
from tests import c, t, u


class TestsFlextTestsDockerLifecycleMixin:
    """Pure lifecycle rules: decision table, verification, projections."""

    @staticmethod
    def _info(
        status: c.Tests.ContainerStatus,
        health: c.Tests.ContainerHealth,
        container_id: str = "sealed-id",
    ) -> m.Tests.ContainerInfo:
        return m.Tests.ContainerInfo(
            name="lifecycle-rule",
            status=status,
            ports={},
            image="fixture:latest",
            container_id=container_id,
            health=health,
        )

    @staticmethod
    def _sealed() -> m.Tests.ContainerState:
        return m.Tests.ContainerState(
            container_name="lifecycle-rule",
            container_id="sealed-id",
            fingerprint="sealed-fingerprint",
            sealed=True,
        )

    def test_absent_container_is_created_whatever_the_record(self) -> None:
        """No container means CREATE, for a sealed, dirty or empty record."""
        records = (
            self._sealed(),
            self._sealed().model_copy(update={"dirty": True}),
            m.Tests.ContainerState(container_name="lifecycle-rule"),
        )
        for state in records:
            tm.that(
                u.Tests.docker_action(None, state, fingerprint="sealed-fingerprint"),
                eq=c.Tests.ContainerAction.CREATE,
            )

    @pytest.mark.parametrize(
        "stale",
        [
            pytest.param({"dirty": True}, id="dirty"),
            pytest.param({"sealed": False}, id="unsealed"),
            pytest.param({"fingerprint": "other-inputs"}, id="fingerprint-mismatch"),
            pytest.param({"container_id": "other-id"}, id="container-id-drift"),
        ],
    )
    def test_stale_record_recreates_in_every_status_and_health(
        self,
        stale: t.MappingKV[str, str | bool],
    ) -> None:
        """A dirty, unsealed, re-declared or foreign record always recreates."""
        state = self._sealed().model_copy(update=stale)
        for status in c.Tests.ContainerStatus:
            for health in c.Tests.ContainerHealth:
                action = u.Tests.docker_action(
                    self._info(status, health),
                    state,
                    fingerprint="sealed-fingerprint",
                )
                tm.that(action, eq=c.Tests.ContainerAction.RECREATE)

    def test_unhealthy_container_recreates_in_every_status(self) -> None:
        """A failed healthcheck recreates even a sealed matching container."""
        for status in c.Tests.ContainerStatus:
            action = u.Tests.docker_action(
                self._info(status, c.Tests.ContainerHealth.UNHEALTHY),
                self._sealed(),
                fingerprint="sealed-fingerprint",
            )
            tm.that(action, eq=c.Tests.ContainerAction.RECREATE)

    def test_sealed_matching_container_follows_its_status(self) -> None:
        """Running reuses, stopped starts, any other status recreates."""
        expected = {
            c.Tests.ContainerStatus.RUNNING: c.Tests.ContainerAction.REUSE,
            c.Tests.ContainerStatus.EXITED: c.Tests.ContainerAction.START,
            c.Tests.ContainerStatus.CREATED: c.Tests.ContainerAction.START,
        }
        settled = (
            c.Tests.ContainerHealth.HEALTHY,
            c.Tests.ContainerHealth.STARTING,
            c.Tests.ContainerHealth.UNKNOWN,
        )
        for status in c.Tests.ContainerStatus:
            for health in settled:
                action = u.Tests.docker_action(
                    self._info(status, health),
                    self._sealed(),
                    fingerprint="sealed-fingerprint",
                )
                tm.that(
                    action,
                    eq=expected.get(status, c.Tests.ContainerAction.RECREATE),
                    msg=f"{status}/{health}",
                )

    @pytest.mark.parametrize(
        ("info_status", "health", "stale", "code"),
        [
            pytest.param(None, None, {}, "NOT_PROVISIONED", id="absent"),
            pytest.param("running", "healthy", {"dirty": True}, "DIRTY", id="dirty"),
            pytest.param(
                "running",
                "healthy",
                {"sealed": False},
                "UNSEALED",
                id="unsealed",
            ),
            pytest.param(
                "running",
                "healthy",
                {"container_id": "other-id"},
                "UNSEALED",
                id="container-id-drift",
            ),
            pytest.param(
                "running",
                "healthy",
                {"fingerprint": "other-inputs"},
                "FINGERPRINT_MISMATCH",
                id="fingerprint-mismatch",
            ),
            pytest.param("running", "unhealthy", {}, "UNHEALTHY", id="unhealthy"),
            pytest.param("running", "starting", {}, "UNHEALTHY", id="starting"),
            pytest.param("exited", "healthy", {}, "UNHEALTHY", id="exited"),
        ],
    )
    def test_verification_reports_one_typed_code(
        self,
        info_status: str | None,
        health: str | None,
        stale: t.MappingKV[str, str | bool],
        code: str,
    ) -> None:
        """Each unusable combination fails with its own error code."""
        info = (
            None
            if info_status is None or health is None
            else self._info(
                c.Tests.ContainerStatus(info_status),
                c.Tests.ContainerHealth(health),
            )
        )
        result = u.Tests.docker_verify(
            info,
            self._sealed().model_copy(update=stale),
            fingerprint="sealed-fingerprint",
        )
        tm.fail(result, code=c.Tests.DockerErrorCode(code))

    def test_verification_accepts_the_sealed_running_container(self) -> None:
        """A sealed, clean, matching, healthy or check-less container passes."""
        for health in (
            c.Tests.ContainerHealth.HEALTHY,
            c.Tests.ContainerHealth.UNKNOWN,
        ):
            info = self._info(c.Tests.ContainerStatus.RUNNING, health)
            verified = u.Tests.docker_verify(
                info,
                self._sealed(),
                fingerprint="sealed-fingerprint",
            )
            tm.that(tm.ok(verified), eq=info)

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
        health: t.MappingKV[str, str] | None,
        env: t.StrSequence | None,
    ) -> m.Tests.ContainerInspect:
        state: dict[str, str | t.MappingKV[str, str]] = {"Status": "running"}
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
        tm.that(environment["PLAIN"].get_secret_value(), eq="1")
        tm.that(environment["WITH_EQ"].get_secret_value(), eq="a=b")
        tm.that(str(environment["PLAIN"]), lacks="1")
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
    def _target(
        compose_file: Path,
        *inputs: Path,
        service: str = "probe",
    ) -> m.Tests.ContainerConfig:
        return m.Tests.ContainerConfig(
            container_name="fingerprinted",
            compose_file=compose_file,
            service=service,
            fingerprint_inputs=inputs,
        )

    def test_fingerprint_follows_declared_bytes_only(self, tmp_path: Path) -> None:
        """Project, service and file bytes change it; the environment does not."""
        compose_file = tmp_path / "stack.yml"
        schema = tmp_path / "schema.ldif"
        _ = compose_file.write_text("services: {}\n", encoding="utf-8")
        _ = schema.write_text("dn: dc=example\n", encoding="utf-8")
        base = tm.ok(u.Tests.docker_fingerprint(self._target(compose_file, schema)))
        with u.Tests.env_vars_context({"FLEXT_TESTS_FINGERPRINT_NOISE": "changed"}):
            tm.that(
                tm.ok(u.Tests.docker_fingerprint(self._target(compose_file, schema))),
                eq=base,
            )
        tm.that(
            tm.ok(
                u.Tests.docker_fingerprint(
                    self._target(compose_file, schema, service="other"),
                ),
            ),
            ne=base,
        )
        tm.that(
            tm.ok(
                u.Tests.docker_fingerprint(
                    self._target(compose_file, schema).model_copy(
                        update={"project_name": "other-project"},
                    ),
                ),
            ),
            ne=base,
        )
        _ = schema.write_text("dn: dc=changed\n", encoding="utf-8")
        tm.that(
            tm.ok(u.Tests.docker_fingerprint(self._target(compose_file, schema))),
            ne=base,
        )

    def test_fingerprint_of_a_missing_input_fails(self, tmp_path: Path) -> None:
        """An input that cannot be read fails; it is never skipped."""
        compose_file = tmp_path / "stack.yml"
        _ = compose_file.write_text("services: {}\n", encoding="utf-8")
        tm.fail(
            u.Tests.docker_fingerprint(
                self._target(compose_file, tmp_path / "absent.ldif"),
            ),
        )
        tm.fail(FlextTestsDocker(state_dir=tmp_path).fingerprint())

    def test_creation_env_file_is_private_and_removed(self, tmp_path: Path) -> None:
        """Creation values live in a 0600 file only inside the block."""
        environment = {"FLEXT_TESTS_SECRET": t.SecretStr("s3cr=t value")}
        with u.Tests.creation_env_file(tmp_path, "env-owner", environment) as env_files:
            (env_file,) = env_files
            tm.that(stat.S_IMODE(env_file.stat().st_mode), eq=0o600)
            tm.that(
                env_file.read_text(encoding="utf-8"),
                eq="FLEXT_TESTS_SECRET='s3cr=t value'\n",
            )
        tm.that(env_file.exists(), eq=False)
        with u.Tests.creation_env_file(tmp_path, "env-owner", {}) as no_files:
            tm.that(no_files, eq=())

    def test_creation_env_file_never_overwrites_a_leftover(
        self,
        tmp_path: Path,
    ) -> None:
        """A file left by an interrupted run fails instead of being replaced."""
        leftover = tmp_path / f"env-owner{c.Tests.DOCKER_ENV_FILE_SUFFIX}"
        _ = leftover.write_text("LEFT=over\n", encoding="utf-8")
        environment = {"FLEXT_TESTS_SECRET": t.SecretStr("value")}
        with (
            pytest.raises(FileExistsError),
            u.Tests.creation_env_file(tmp_path, "env-owner", environment),
        ):
            tm.that(leftover.exists(), eq=True)
        tm.that(leftover.read_text(encoding="utf-8"), eq="LEFT=over\n")

    def test_unrepresentable_creation_value_is_rejected(self) -> None:
        """A quote or line break cannot be written literally and is refused."""
        for value in ("it's", "two\nlines"):
            tm.fail(
                u.Tests.validate_creation_environment({"KEY": t.SecretStr(value)}),
                has="KEY",
            )
        tm.ok(u.Tests.validate_creation_environment({"KEY": t.SecretStr("fine")}))
