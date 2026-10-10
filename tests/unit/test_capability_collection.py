"""Public consumer runs prove connectivity applicability and failure visibility.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/unit/test_capability_collection
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import socket
import time
from collections.abc import Generator
from pathlib import Path

import pytest
from flext_infra import FlextInfraPytestRunner
from flext_infra import config as infra_config

from flext_tests import c, tm, u

pytest_plugins = ["pytester"]


class TestsFlextTestsCapabilityCollection:
    """Exercise the installed plugin, without replacing any service or probe."""

    @staticmethod
    @pytest.fixture
    def consumer(pytester: pytest.Pytester) -> Generator[pytest.Pytester]:
        """Provide ``consumer``.

        Yields:
            Each ``pytest.Pytester``.
        """
        pytester.makepyprojecttoml("[tool.pytest.ini_options]\n")
        u.Cli.run_checked(
            [*c.Cli.GIT_INIT_COMMAND, str(pytester.path)],
        ).unwrap()
        pytester.makeconftest(
            "import pytest\n"
            "@pytest.fixture\n"
            "def service():\n"
            "    pytest.fail('service fixture executed')\n",
        )
        ci = infra_config.Infra.codegen.make.ci
        with u.Tests.env_vars_context(
            {ci.variable: f"{ci.value}-other"},
        ):
            yield pytester

    @staticmethod
    def _run(consumer: pytest.Pytester) -> pytest.RunResult:
        return consumer.runpytest_subprocess(
            "-p",
            "no:flext_tests_enforcement",
            "-p",
            "no:cacheprovider",
            "-rs",
        )

    @staticmethod
    @pytest.mark.slow
    def test_missing_env_skips_before_fixtures(
        consumer: pytest.Pytester,
    ) -> None:
        """Test missing env skips before fixtures."""
        consumer.makepyfile(
            "import pytest\n"
            "@pytest.mark.parametrize('marker', ['docker', 'oracle', 'ldap', 'remote', "
            "'connectivity'])\n"
            "def test_external(marker, request):\n"
            "    pytest.fail('test executed')\n"
            "@pytest.mark.integration\n"
            "def test_pure_integration():\n    pass\n",
        )
        consumer.makeconftest(
            "import pytest\n"
            "def pytest_collection_modifyitems(items):\n"
            "    for item in items:\n"
            "        if 'test_external' in item.name:\n"
            "            item.add_marker(getattr(pytest.mark, "
            "item.callspec.params['marker']))\n"
            "            item.add_marker(pytest.mark.usefixtures('service'))\n"
            "@pytest.fixture\n"
            "def service():\n    pytest.fail('service fixture executed')\n",
        )
        result = TestsFlextTestsCapabilityCollection._run(consumer)
        result.assert_outcomes(passed=1, skipped=5)
        tm.that(result.ret, eq=0)

    @staticmethod
    @pytest.mark.slow
    def test_canonical_runner_accepts_only_prerequisite_skips(
        consumer: pytest.Pytester,
        tmp_path: Path,
    ) -> None:
        """The real runner preserves availability skips and rejects ordinary skips."""
        cache = infra_config.Infra.codegen.make.testmon_cache
        target = consumer.path / cache.target_directory
        target.mkdir(exist_ok=True)
        test_file = target / "test_prerequisites.py"
        test_file.write_text(
            "import pytest\n"
            "@pytest.mark.connectivity(url_var='TEST_ENDPOINT')\n"
            "def test_unconfigured(service):\n    pass\n"
            "def test_pure():\n    pass\n",
            encoding="utf-8",
        )
        runner = FlextInfraPytestRunner(
            repository_root=consumer.path,
            started_at_monotonic=time.monotonic(),
            target=cache.target_directory,
            reports=cache.reports_directory,
            testmon_db=tmp_path / cache.database_filename,
            apply_changes=True,
        )
        tm.that(tm.ok(runner.execute_full()), eq=0)
        reports = consumer.path / cache.reports_directory
        latest = (reports / "latest.txt").read_text(encoding="utf-8").strip()
        tm.that(
            (reports / latest / "summary.txt").read_text(encoding="utf-8"),
            has=["skipped=1", "connectivity_prerequisite_skips=1", "exit=0"],
        )
        test_file.write_text(
            test_file.read_text(encoding="utf-8")
            + "def test_unexpected_skip():\n    pytest.skip('ordinary skip')\n",
            encoding="utf-8",
        )
        tm.that(tm.ok(runner.execute_full()), ne=0)
        latest = (reports / "latest.txt").read_text(encoding="utf-8").strip()
        tm.that(
            (reports / latest / "summary.txt").read_text(encoding="utf-8"),
            has=["skipped=2", "connectivity_prerequisite_skips=1", "failed=0"],
        )

    @staticmethod
    @pytest.mark.slow
    def test_cached_prerequisites_reactivate_each_consumer_environment(
        consumer: pytest.Pytester,
    ) -> None:
        """A/B/A consumers see their own file and restore the inherited environment."""
        consumer.makeconftest(
            "import os\nimport pytest\n"
            "def pytest_collection_modifyitems(items):\n"
            "    items.sort(key=lambda item: item.name)\n"
            "@pytest.fixture\n"
            "def service():\n    return os.environ['TEST_LABEL']\n",
        )
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(32)
            port = listener.getsockname()[1]
            for label, indices in (("A", (1, 3)), ("B", (2,))):
                member = consumer.path / label
                member.mkdir()
                (member / "pyproject.toml").write_text(
                    "[tool.pytest.ini_options]\n", encoding="utf-8"
                )
                (member / ".env").write_text(
                    f"TEST_LABEL={label}\nTEST_ENDPOINT=http://127.0.0.1:{port}\n",
                    encoding="utf-8",
                )
                (member / f"test_consumer_{label}.py").write_text(
                    "import pytest\n"
                    "pytestmark = pytest.mark.connectivity(url_var='TEST_ENDPOINT')\n"
                    + "".join(
                        f"def test_{index}(service):\n"
                        f"    if service != '{label}':\n"
                        "        pytest.fail('wrong consumer environment')\n"
                        for index in indices
                    ),
                    encoding="utf-8",
                )
            consumer.makepyfile(
                "import os\nimport pytest\n"
                "def test_4_restored():\n"
                "    if 'TEST_LABEL' in os.environ:\n"
                "        pytest.fail('consumer environment leaked')\n",
            )
            with u.Tests.env_vars_context(vars_to_clear=("TEST_LABEL",)):
                result = TestsFlextTestsCapabilityCollection._run(consumer)
        result.assert_outcomes(passed=4)
        tm.that(result.ret, eq=0)

    @staticmethod
    @pytest.mark.slow
    @pytest.mark.parametrize("service_marker", c.Tests.CONNECTIVITY_MARKER_CONTAINERS)
    @pytest.mark.parametrize(
        "ordering", ["service-only", "service-first", "docker-first"]
    )
    def test_docker_backed_markers_skip_in_ci_before_effects(
        consumer: pytest.Pytester,
        service_marker: str,
        ordering: str,
    ) -> None:
        """Test docker backed markers skip in ci before effects."""
        ci = infra_config.Infra.codegen.make.ci
        markers = [service_marker]
        if ordering == "service-first":
            markers.append("docker")
        elif ordering == "docker-first":
            markers.insert(0, "docker")
        (consumer.path / ".env").write_text(
            "FLEXT_TEST_ENV_EFFECT=loaded\n",
            encoding="utf-8",
        )
        consumer.makepyfile(
            "import os\nimport pytest\n"
            + "".join(f"@pytest.mark.{marker}\n" for marker in markers)
            + "def test_external(service):\n    pass\n"
            "def test_environment_not_loaded():\n"
            "    if 'FLEXT_TEST_ENV_EFFECT' in os.environ:\n"
            "        pytest.fail('environment loaded before CI skip')\n",
        )
        with socket.socket() as docker_endpoint:
            docker_endpoint.bind(("127.0.0.1", 0))
            port = docker_endpoint.getsockname()[1]
            consumer.makeconftest(
                "import sys\nimport pytest\n"
                "def audit(event, args):\n"
                "    if event == 'socket.connect' "
                f"and args[1] == ('127.0.0.1', {port}):\n"
                "        raise RuntimeError('Docker probe attempted before CI skip')\n"
                "sys.addaudithook(audit)\n"
                "@pytest.fixture\n"
                "def service():\n    pytest.fail('service fixture executed')\n",
            )
            with u.Tests.env_vars_context(
                {ci.variable: ci.value, "DOCKER_HOST": f"tcp://127.0.0.1:{port}"},
                vars_to_clear=(
                    "FLEXT_TEST_ENV_EFFECT",
                    "DOCKER_TLS_VERIFY",
                    "DOCKER_CERT_PATH",
                ),
            ):
                result = TestsFlextTestsCapabilityCollection._run(consumer)
        result.assert_outcomes(passed=1, skipped=1)
        result.stdout.fnmatch_lines([
            "*Docker-dependent connectivity tests are disabled in CI*",
        ])
        tm.that(result.ret, eq=0)

    @staticmethod
    @pytest.mark.slow
    @pytest.mark.parametrize(
        ("declaration", "message"),
        [
            ("required_vars='INVALID'", "Connectivity required_vars must be names"),
            ("required_vars=(1,)", "Connectivity required_vars must be names"),
            ("url_var=1", "Connectivity url_var must be a name"),
        ],
    )
    @pytest.mark.parametrize("other_marker", ["remote", "docker"])
    def test_invalid_declaration_errors_without_environment(
        consumer: pytest.Pytester,
        declaration: str,
        message: str,
        other_marker: str,
    ) -> None:
        """Test invalid declaration errors without environment."""
        ci = infra_config.Infra.codegen.make.ci
        consumer.makepyfile(
            f"import pytest\n@pytest.mark.connectivity({declaration})\n"
            f"@pytest.mark.{other_marker}\n"
            "def test_external(service):\n    pass\n",
        )
        with u.Tests.env_vars_context({ci.variable: ci.value}):
            result = TestsFlextTestsCapabilityCollection._run(consumer)
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines([f"*UsageError: {message}*"])
        tm.that(result.ret, eq=1)

    @staticmethod
    @pytest.mark.slow
    @pytest.mark.parametrize("service_marker", c.Tests.CONNECTIVITY_MARKER_CONTAINERS)
    @pytest.mark.parametrize("endpoint_kind", ["address", "url"])
    def test_explicit_service_endpoint_is_not_docker_dependent(
        consumer: pytest.Pytester,
        service_marker: str,
        endpoint_kind: str,
    ) -> None:
        """Explicit remote transports run locally and in CI without Docker probes."""
        ci = infra_config.Infra.codegen.make.ci
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(32)
            port = listener.getsockname()[1]
            (consumer.path / ".env").write_text(
                f"TEST_ENDPOINT=http://127.0.0.1:{port}\n",
                encoding="utf-8",
            )
            declaration = (
                f"host='127.0.0.1', port={port}"
                if endpoint_kind == "address"
                else "url_var='TEST_ENDPOINT'"
            )
            consumer.makepyfile(
                "import pytest\n"
                f"@pytest.mark.{service_marker}({declaration})\n"
                "def test_remote():\n    pass\n"
                f"@pytest.mark.{service_marker}({declaration})\n"
                "def test_application_failure():\n"
                "    pytest.fail('remote application failed')\n",
            )
            for ci_value in (f"{ci.value}-other", ci.value):
                with u.Tests.env_vars_context({ci.variable: ci_value}):
                    result = TestsFlextTestsCapabilityCollection._run(consumer)
                result.assert_outcomes(passed=1, failed=1)
                tm.that(result.ret, eq=1)

    @staticmethod
    @pytest.mark.slow
    @pytest.mark.parametrize("tracked", [False, True])
    def test_tracking_check_distinguishes_tracked_file_from_git_error(
        consumer: pytest.Pytester,
        *,
        tracked: bool,
    ) -> None:
        """A tracked .env skips, but a real Git repository error remains an error."""
        (consumer.path / ".env").write_text(
            "TEST_ENVIRONMENT=declared\n", encoding="utf-8"
        )
        if tracked:
            u.Cli.run_checked(["git", "add", "--", ".env"], cwd=consumer.path).unwrap()
        else:
            (consumer.path / ".git" / "HEAD").unlink()
        consumer.makepyfile(
            "import pytest\n"
            "@pytest.mark.connectivity(host='127.0.0.1', port=1)\n"
            "def test_external(service):\n    pass\n",
        )
        result = TestsFlextTestsCapabilityCollection._run(consumer)
        if tracked:
            result.assert_outcomes(skipped=1)
            result.stdout.fnmatch_lines([
                "*External tests require a local untracked .env*"
            ])
            tm.that(result.ret, eq=0)
        else:
            result.assert_outcomes(errors=1)
            result.stdout.fnmatch_lines([
                "*RuntimeError: Git test-environment tracking check failed (exit 128)*"
            ])
            tm.that(result.ret, eq=1)

    @staticmethod
    @pytest.mark.slow
    def test_unreachable_env_skips(
        consumer: pytest.Pytester,
    ) -> None:
        """Test unreachable env skips."""
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
            # A bound socket that does not listen gives a real refused connection.
            (consumer.path / ".env").write_text(
                f"TEST_ENDPOINT=http://127.0.0.1:{port}\n",
                encoding="utf-8",
            )
            consumer.makepyfile(
                "import pytest\n@pytest.mark.connectivity(url_var='TEST_ENDPOINT')\n"
                "def test_external(service):\n    pass\n",
            )
            result = TestsFlextTestsCapabilityCollection._run(consumer)
            result.assert_outcomes(skipped=1)

    @staticmethod
    @pytest.mark.slow
    def test_ready_endpoint_executes_and_real_failures_stay_failures(
        consumer: pytest.Pytester,
    ) -> None:
        """Test ready endpoint executes and real failures stay failures."""
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen()
            port = listener.getsockname()[1]
            (consumer.path / ".env").write_text(
                f"TEST_ENDPOINT=http://127.0.0.1:{port}\n",
                encoding="utf-8",
            )
            consumer.makepyfile(
                "import pytest\n"
                "pytestmark = pytest.mark.connectivity(url_var='TEST_ENDPOINT')\n"
                "def test_success():\n    pass\n"
                "def test_application_failure():\n    pytest.fail('application "
                "failed')\n"
                "def test_fixture_failure(service):\n    pass\n",
            )
            result = TestsFlextTestsCapabilityCollection._run(consumer)
            result.assert_outcomes(passed=1, failed=1, errors=1)
            tm.that(result.ret, eq=1)
