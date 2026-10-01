"""Private docker Make-CI-token gate test mixins."""

from __future__ import annotations

from pathlib import Path

import pytest
from flext_infra import config as infra_config

from flext_tests import FlextTestsDocker, FlextTestsKube, m, tm
from tests import c, t, u


class TestsFlextTestsDockerCiMixin:
    """The Make CI token disables every Docker effect with a typed failure."""

    @pytest.mark.parametrize(
        ("value_template", "disabled"),
        [
            pytest.param(None, False, id="unset"),
            pytest.param("{token}", True, id="make-token"),
            pytest.param(" {token} ", True, id="make-token-padded"),
            pytest.param("{token}-other", False, id="other-value"),
        ],
    )
    def test_ci_token_gates_the_lifecycle(
        self, *, value_template: str | None, disabled: bool
    ) -> None:
        """Only the configured Make CI value disables Docker, and it is typed."""
        ci = infra_config.Infra.codegen.make.ci
        env: t.StrMapping = (
            {}
            if value_template is None
            else {ci.variable: value_template.format(token=ci.value)}
        )
        with u.Tests.env_vars_context(env, vars_to_clear=(ci.variable,)):
            tm.that(FlextTestsDocker.ci_disables_docker(), eq=disabled)
            gate = FlextTestsDocker.lifecycle_enabled()
        if disabled:
            tm.fail(gate, code=c.Tests.DockerErrorCode.DISABLED_BY_CI)
        else:
            tm.that(tm.ok(gate), eq=True)

    def test_lifecycle_effects_fail_disabled_by_ci(self, tmp_path: Path) -> None:
        """Under the CI token no effect reaches Docker; each one fails typed."""
        ci = infra_config.Infra.codegen.make.ci
        disabled = c.Tests.DockerErrorCode.DISABLED_BY_CI
        compose_file = tmp_path / "never-created.yml"
        docker = FlextTestsDocker.compose(
            compose_file,
            target=m.Tests.ContainerConfig(
                container_name="flext-tests-ci-gate", service="gate"
            ),
            repository_root=tmp_path,
            state_dir=tmp_path / "state",
        )
        with u.Tests.env_vars_context({ci.variable: ci.value}):
            tm.fail(docker.execute(), code=disabled)
            tm.fail(docker.verify(), code=disabled)
            tm.fail(docker.up(), code=disabled)
            tm.fail(docker.down(), code=disabled)
            tm.fail(docker.compose_up(str(compose_file)), code=disabled)
            tm.fail(docker.compose_down(str(compose_file)), code=disabled)
            tm.fail(docker.start_compose_stack(str(compose_file)), code=disabled)
            tm.fail(
                docker.start_existing_container("flext-tests-ci-gate"), code=disabled
            )
            tm.fail(docker.cleanup_dirty_containers(), code=disabled)

    def test_kube_effects_fail_disabled_by_ci(self, tmp_path: Path) -> None:
        """The kind specialization inherits the same typed CI gate."""
        ci = infra_config.Infra.codegen.make.ci
        disabled = c.Tests.DockerErrorCode.DISABLED_BY_CI
        kube = FlextTestsKube.kind(repository_root=tmp_path, state_dir=tmp_path)
        with u.Tests.env_vars_context({ci.variable: ci.value}):
            tm.fail(kube.execute(), code=disabled)
            tm.fail(kube.cluster_up(), code=disabled)
            tm.fail(kube.cluster_down(), code=disabled)
            tm.fail(kube.nodes_ready(), code=disabled)

    def test_ci_token_leaves_host_records_writable(self, tmp_path: Path) -> None:
        """Dirty marking is host bookkeeping, not a Docker effect."""
        ci = infra_config.Infra.codegen.make.ci
        docker = FlextTestsDocker(state_dir=tmp_path)
        with u.Tests.env_vars_context({ci.variable: ci.value}):
            _ = u.Tests.assert_success(docker.mark_container_dirty("flext-tests-ci"))
        tm.that(docker.container_dirty("flext-tests-ci"), eq=True)
