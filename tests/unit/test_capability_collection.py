"""Public consumer runs prove connectivity applicability and failure visibility.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/unit/test_capability_collection
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import socket
import subprocess
from collections.abc import Generator

import pytest
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
        subprocess.run(["git", "init", "--quiet", str(pytester.path)], check=True)
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
        with u.Tests.env_vars_context(
            {ci.variable: ci.value},
            vars_to_clear=("FLEXT_TEST_ENV_EFFECT",),
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
