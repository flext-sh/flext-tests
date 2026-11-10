"""Public consumer runs prove connectivity applicability and failure visibility.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/unit/test_capability_collection
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import socket
from collections.abc import Generator

from flext_infra import config

from tests import c, p, t, tm, u

pytest_plugins = ["pytester"]


class TestsFlextTestsCapabilityCollection:
    """Exercise the installed plugin, without replacing any service or probe."""

    @u.Tests.fixture
    @staticmethod
    def consumer(pytester: t.Tests.Pytester) -> Generator[t.Tests.Pytester]:
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
            "@pytest.hookimpl(trylast=True)\n"
            "def pytest_collection_modifyitems(items):\n"
            "    items.sort(key=lambda item: item.name)\n"
            "@pytest.fixture\n"
            "def service():\n"
            "    pytest.fail('service fixture executed')\n",
        )
        ci = config.Infra.codegen.make.ci
        with u.Tests.env_vars_context(
            {ci.variable: f"{ci.value}-other"},
        ):
            yield pytester

    @staticmethod
    def _run(consumer: t.Tests.Pytester, *paths: str) -> t.Tests.RunResult:
        return u.Tests.pytest_subprocess(
            consumer,
            "-p",
            "no:flext_tests_enforcement",
            "-p",
            "no:cacheprovider",
            "-rs",
            *paths,
        )

    @staticmethod
    @c.Tests.MARK.slow
    def test_undeclared_connectivity_skips_and_remote_gate_runs(
        consumer: t.Tests.Pytester,
        fixture_tree: p.Tests.FixtureTree,
    ) -> None:
        """An endpoint is required; file presence is unrelated to selection."""
        tree = fixture_tree(
            "capability_markers", destination=consumer.path / "capability_markers"
        )
        result = TestsFlextTestsCapabilityCollection._run(
            consumer, "-v", str(tree / "test_remote.py")
        )
        result.assert_outcomes(passed=2, skipped=1)
        result.stdout.fnmatch_lines([
            "*test_remote_gate PASSED*",
            "*External test endpoint is not declared*",
        ])
        tm.that(result.ret, eq=0)

    @staticmethod
    @c.Tests.MARK.slow
    @c.Tests.MARK.parametrize("in_ci", [False, True])
    def test_docker_markers_skip_only_when_docker_unreachable(
        consumer: t.Tests.Pytester,
        fixture_tree: p.Tests.FixtureTree,
        *,
        in_ci: bool,
    ) -> None:
        """Docker-provisioned markers never ask for .env; an absent daemon skips."""
        tree = fixture_tree(
            "capability_markers", destination=consumer.path / "capability_markers"
        )
        with socket.socket() as closed_endpoint:
            closed_endpoint.bind(("127.0.0.1", 0))
            port = closed_endpoint.getsockname()[1]
            with u.Tests.env_vars_context(
                {
                    c.Tests.DOCKER_HOST_VARIABLE: f"tcp://127.0.0.1:{port}",
                    config.Infra.codegen.make.ci.variable: (
                        config.Infra.codegen.make.ci.value if in_ci else "local"
                    ),
                },
                vars_to_clear=("DOCKER_TLS_VERIFY", "DOCKER_CERT_PATH"),
            ):
                result = TestsFlextTestsCapabilityCollection._run(
                    consumer, str(tree / "test_docker_markers.py")
                )
        result.assert_outcomes(skipped=len(c.Tests.CONNECTIVITY_MARKERS))
        result.stdout.fnmatch_lines(["*Docker test environment is unreachable*"])
        result.stdout.no_fnmatch_line("*untracked .env*")
        tm.that(result.ret, eq=0)

    @staticmethod
    @c.Tests.MARK.slow
    @c.Tests.MARK.docker
    def test_docker_marker_runs_with_isolated_environment(
        consumer: t.Tests.Pytester,
        fixture_tree: p.Tests.FixtureTree,
    ) -> None:
        """With Docker up, the test runs on a generated, isolated .env."""
        tree = fixture_tree(
            "capability_docker_isolated_env",
            destination=consumer.path / "capability_docker_isolated_env",
        )
        result = TestsFlextTestsCapabilityCollection._run(consumer, str(tree))
        result.assert_outcomes(passed=1)
        tm.that(result.ret, eq=0)

    @staticmethod
    @c.Tests.MARK.slow
    def test_process_inputs_reach_fixtures_without_an_environment_file(
        consumer: t.Tests.Pytester,
    ) -> None:
        """Selected inputs reach service fixtures without any local file."""
        consumer.makeconftest(
            "import os\nimport pytest\n"
            "@pytest.fixture\n"
            "def service():\n    return os.environ['TEST_LABEL']\n",
        )
        consumer.makepyfile(
            "import pytest\n"
            "@pytest.mark.connectivity(required_vars=('TEST_LABEL',), "
            "url_var='TEST_ENDPOINT')\n"
            "def test_external(service):\n"
            "    assert service == 'selected-process-input'\n",
        )
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(32)
            port = listener.getsockname()[1]
            with u.Tests.env_vars_context({
                "TEST_LABEL": "selected-process-input",
                "TEST_ENDPOINT": f"http://127.0.0.1:{port}",
            }):
                result = TestsFlextTestsCapabilityCollection._run(consumer)
        result.assert_outcomes(passed=1)
        tm.that(result.ret, eq=0)
        tm.that((consumer.path / ".env").exists(), eq=False)

    @staticmethod
    @c.Tests.MARK.slow
    def test_changed_process_inputs_are_revalidated(
        consumer: t.Tests.Pytester,
    ) -> None:
        """Changed inputs retain readiness and declaration failures per case."""
        mutations = {
            "missing": "os.environ.pop('TEST_REQUIRED_MISSING')",
            "closed": "os.environ['TEST_ENDPOINT_CLOSED'] = {closed!r}",
            "invalid": "os.environ['TEST_ENDPOINT_INVALID'] = 'not-a-url'",
        }
        with socket.socket() as listener, socket.socket() as closed:
            listener.bind(("127.0.0.1", 0))
            listener.listen(32)
            closed.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
            closed_url = f"http://127.0.0.1:{closed.getsockname()[1]}"
            environment = {}
            for mutation, body in mutations.items():
                suffix = mutation.upper()
                environment[f"TEST_ENDPOINT_{suffix}"] = f"http://127.0.0.1:{port}"
                environment[f"TEST_REQUIRED_{suffix}"] = "selected"
                consumer.makepyfile(**{
                    f"test_{mutation}": (
                        "import os\nimport pytest\n"
                        f"pytestmark = pytest.mark.connectivity(required_vars="
                        f"('TEST_REQUIRED_{suffix}',), "
                        f"url_var='TEST_ENDPOINT_{suffix}')\n"
                        "def test_1_change_inputs():\n"
                        f"    {body.format(closed=closed_url)}\n"
                        "def test_2_recheck(service):\n    pass\n"
                    ),
                })
            with u.Tests.env_vars_context(environment):
                result = TestsFlextTestsCapabilityCollection._run(consumer)
        result.assert_outcomes(passed=len(mutations), skipped=2, errors=1)
        tm.that(result.ret, eq=1)

    @staticmethod
    @c.Tests.MARK.slow
    def test_host_executables_gate_without_endpoint(
        consumer: t.Tests.Pytester,
    ) -> None:
        """A present executable runs; an absent one is a recorded prerequisite skip."""
        absent = consumer.path.name + "-absent-executable"
        consumer.makepyfile(
            "import pytest\n"
            "@pytest.mark.connectivity(executables=('git',))\n"
            "def test_present():\n    pass\n"
            f"@pytest.mark.connectivity(executables=('git', {absent!r}))\n"
            "def test_absent():\n    pytest.fail('ran without its executable')\n",
        )
        result = TestsFlextTestsCapabilityCollection._run(consumer)
        result.assert_outcomes(passed=1, skipped=1)
        result.stdout.fnmatch_lines([f"*Host executable is unavailable: {absent}*"])
        tm.that(result.ret, eq=0)

    @staticmethod
    @c.Tests.MARK.slow
    def test_invalid_declarations_error_without_environment(
        consumer: t.Tests.Pytester,
    ) -> None:
        """Every malformed declaration errors before CI or environment skips."""
        declarations = (
            ("required_vars='INVALID'", "Connectivity required_vars must be names"),
            ("required_vars=(1,)", "Connectivity required_vars must be names"),
            ("url_var=1", "Connectivity url_var must be a name"),
            (
                "host=1, port=1",
                "Connectivity host and port must be a string and an integer",
            ),
            (
                "host='localhost', port='invalid'",
                "Connectivity host and port must be a string and an integer",
            ),
            (
                "host='localhost', port=True",
                "Connectivity host and port must be a string and an integer",
            ),
            (
                "host='localhost'",
                "Connectivity host and port must be a string and an integer",
            ),
            (
                "host='', port=1",
                "Connectivity host and port must be a string and an integer",
            ),
            (
                f"host='localhost', port={c.MIN_PORT - 1}",
                "Connectivity host and port must be a string and an integer",
            ),
            (
                f"host='localhost', port={c.MAX_PORT + 1}",
                "Connectivity host and port must be a string and an integer",
            ),
            ("required_vars=('',)", "Connectivity required_vars must be names"),
            ("url_var=''", "Connectivity url_var must be a name"),
            ("executables='git'", "Connectivity executables must be names"),
            ("executables=(1,)", "Connectivity executables must be names"),
            ("executables=('',)", "Connectivity executables must be names"),
            (
                "url_vaar='TEST_ENDPOINT'",
                "Connectivity declarations require supported keyword arguments",
            ),
            (
                "'unexpected'",
                "Connectivity declarations require supported keyword arguments",
            ),
        )
        other_markers = ("remote", "docker")
        ci = config.Infra.codegen.make.ci
        consumer.makepyfile(
            "import pytest\n"
            + "".join(
                f"@pytest.mark.connectivity({declaration})\n"
                f"@pytest.mark.{other_marker}\n"
                f"def test_invalid_{index}_{other_marker}(service):\n    pass\n"
                for index, (declaration, _) in enumerate(declarations)
                for other_marker in other_markers
            ),
        )
        with u.Tests.env_vars_context({ci.variable: ci.value}):
            result = TestsFlextTestsCapabilityCollection._run(consumer)
        result.assert_outcomes(errors=len(declarations) * len(other_markers))
        result.stdout.fnmatch_lines_random([
            f"*UsageError: {message}*" for _, message in declarations
        ])
        tm.that(result.ret, eq=1)

    @staticmethod
    @c.Tests.MARK.slow
    @c.Tests.MARK.parametrize("in_ci", [False, True])
    def test_explicit_service_endpoints_are_not_docker_dependent(
        consumer: t.Tests.Pytester,
        *,
        in_ci: bool,
    ) -> None:
        """Explicit remote transports run locally and in CI without Docker probes."""
        ci = config.Infra.codegen.make.ci
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(32)
            port = listener.getsockname()[1]

            declarations = (
                f"host='127.0.0.1', port={port}",
                "url_var='TEST_HTTP_ENDPOINT'",
                "url_var='TEST_LDAP_ENDPOINT'",
            )
            consumer.makepyfile(
                "import pytest\n"
                "def test_pure():\n    pass\n"
                "def test_visible_failure():\n    pytest.fail('visible failure')\n"
                + "".join(
                    f"@pytest.mark.{service_marker}({declaration})\n"
                    f"def test_remote_{service_marker}_{index}():\n    pass\n"
                    f"@pytest.mark.{service_marker}({declaration})\n"
                    f"def test_application_failure_{service_marker}_{index}():\n"
                    "    pytest.fail('remote application failed')\n"
                    for service_marker in c.Tests.CONNECTIVITY_MARKER_CONTAINERS
                    for index, declaration in enumerate(declarations)
                ),
            )
            case_count = len(c.Tests.CONNECTIVITY_MARKER_CONTAINERS) * len(declarations)
            ci_value = ci.value if in_ci else f"{ci.value}-other"
            with u.Tests.env_vars_context({
                ci.variable: ci_value,
                "TEST_HTTP_ENDPOINT": f"http://127.0.0.1:{port}",
                "TEST_LDAP_ENDPOINT": f"ldap://127.0.0.1:{port}",
            }):
                result = TestsFlextTestsCapabilityCollection._run(consumer)
            result.assert_outcomes(passed=case_count + 1, failed=case_count + 1)
            tm.that(result.ret, eq=1)

    @staticmethod
    @c.Tests.MARK.slow
    def test_unreachable_env_skips(
        consumer: t.Tests.Pytester,
    ) -> None:
        """Test unreachable env skips."""
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
            # A bound socket that does not listen gives a real refused connection.

            consumer.makepyfile(
                "import pytest\n@pytest.mark.connectivity(url_var='TEST_ENDPOINT')\n"
                "def test_external(service):\n    pass\n",
            )
            with u.Tests.env_vars_context({
                "TEST_ENDPOINT": f"http://127.0.0.1:{port}",
            }):
                result = TestsFlextTestsCapabilityCollection._run(consumer)
        result.assert_outcomes(skipped=1)

    @staticmethod
    @c.Tests.MARK.parametrize(
        "endpoint",
        [
            "http://user:secret@[invalid",
            "http://user:secret@localhost:invalid",
            f"http://user:secret@localhost:{c.MAX_PORT + 1}",
            f"http://user:secret@localhost:{c.MIN_PORT - 1}",
            "http://user:secret@",
            "//user:secret@localhost:80",
            "unknown://user:secret@localhost",
        ],
    )
    def test_invalid_endpoint_values_fail_without_exposing_credentials(
        endpoint: str,
    ) -> None:
        """Malformed configured URLs fail before transport and hide credentials."""
        with (
            u.Tests.env_vars_context({"TEST_ENDPOINT": endpoint}),
            u.Tests.raises(c.Tests.UsageError) as error,
        ):
            u.Tests.external_environment_reason(url_var="TEST_ENDPOINT")
        tm.that(
            str(error.value),
            eq="External test endpoint is invalid or lacks a transport port",
        )
        tm.that(str(error.value), lacks="secret")

    @staticmethod
    @c.Tests.MARK.parametrize("scheme", ["http", "https", "ldap", "ldaps", "custom"])
    def test_explicit_endpoint_ports_use_the_real_transport(
        scheme: str,
    ) -> None:
        """An explicit transport port needs no scheme-specific default."""
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen()
            port = listener.getsockname()[1]
            with u.Tests.env_vars_context({
                "TEST_ENDPOINT": f"{scheme}://127.0.0.1:{port}",
            }):
                tm.that(
                    u.Tests.external_environment_reason(url_var="TEST_ENDPOINT"),
                    eq=None,
                )

    @staticmethod
    @c.Tests.MARK.slow
    def test_ready_endpoint_executes_and_real_failures_stay_failures(
        consumer: t.Tests.Pytester,
    ) -> None:
        """Test ready endpoint executes and real failures stay failures."""
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen()
            port = listener.getsockname()[1]

            consumer.makepyfile(
                "import pytest\n"
                "pytestmark = pytest.mark.connectivity(url_var='TEST_ENDPOINT')\n"
                "def test_success():\n    pass\n"
                "def test_application_failure():\n    pytest.fail('application "
                "failed')\n"
                "def test_fixture_failure(service):\n    pass\n",
            )
            with u.Tests.env_vars_context({
                "TEST_ENDPOINT": f"http://127.0.0.1:{port}",
            }):
                result = TestsFlextTestsCapabilityCollection._run(consumer)
            result.assert_outcomes(passed=1, failed=1, errors=1)
            tm.that(result.ret, eq=1)
