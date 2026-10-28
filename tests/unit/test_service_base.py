"""Behavioral coverage for the typed service base (S6, flext-4jtcb.5).

Every test exercises the PUBLIC contract of ``s`` (``FlextTestsServiceBase``) and
the pytest plugin's explicit runtime lifecycle: observable return values,
raised exceptions, and their messages. No mocks, no patches, no private-module
imports or private-attribute assertions. The port-bearing service and its
adapter are real (``tests.u.Tests.EchoService`` / ``tests.u.Tests.MemoryEcho``),
never a stand-in.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

import pytest
from flext_core import FlextSettings
from flext_infra import FlextInfraConstants, config, u as infra_u

from flext_tests import FlextTestsServiceBase
from tests import c, m, s, tm, u


class TestsFlextTestsServiceBase:
    """Behavioral contract for the ``FlextTestsServiceBase`` typed test hooks."""

    @staticmethod
    def _consumer_options() -> tuple[str, ...]:
        """Inner-run options a consumer receives from the canonical runner.

        The flext-infra runner passes the config-owned asyncio loop scope to
        every pytest it starts; a synthetic consumer package gets the same
        value from the same owner, never a copied literal.

        Returns:
            The resulting ``tuple[str, ...]``.

        """
        loop_scope = infra_u.Infra.native_tool_setting(
            config.Infra.tooling,
            "pytest.ini_options",
            FlextInfraConstants.Infra.ASYNCIO_DEFAULT_FIXTURE_LOOP_SCOPE,
            str,
        )
        return (
            "-o",
            f"{FlextInfraConstants.Infra.ASYNCIO_DEFAULT_FIXTURE_LOOP_SCOPE}={loop_scope}",
        )

    class Tests:
        """flext-tests service-base test namespace."""

    @staticmethod
    def test_public_service_alias_preserves_generic_test_runtime() -> None:
        """The public short alias remains a generic class with test settings."""

        class _TestService(s[str]):
            """A consumer subclass of the public generic service alias."""

        tm.ok(s is FlextTestsServiceBase)
        with _TestService.isolated_test_runtime() as service:
            tm.that(
                isinstance(service.settings, _TestService.test_settings_type()),
                eq=True,
            )
            tm.ok(service is _TestService.fetch_global())

    # ---- isolated_test_runtime(build=...) for port-bearing services --------

    @staticmethod
    def test_isolated_test_runtime_builds_port_service_with_real_adapter() -> None:
        """A port-bearing service is constructed explicitly with a real adapter."""
        with u.Tests.EchoService.isolated_test_runtime(
            build=lambda: u.Tests.EchoService(port=u.Tests.MemoryEcho()),
        ) as service:
            result = service.run()
            tm.ok(result.success)
            tm.that(result.unwrap(), eq="HI")
            tm.that("port" in service.model_dump(), truth=False)

    @staticmethod
    def test_isolated_test_runtime_without_build_still_needs_fetch_global() -> None:
        """Omitting ``build`` for a port-bearing service still fails validated."""
        with (
            pytest.raises(m.ValidationError, match="port"),
            u.Tests.EchoService.isolated_test_runtime(),
        ):
            pytest.fail("unreachable: fetch_global() must raise ValidationError")

    @staticmethod
    def test_isolated_test_runtime_without_build_resolves_a_port_free_service() -> None:
        """A port-free service keeps resolving through ``fetch_global()``."""
        with FlextTestsServiceBase.isolated_test_runtime() as service:
            tm.ok(service is FlextTestsServiceBase.fetch_global())

    # ---- test_settings_type: raise, never fall back -------------------------

    @staticmethod
    def test_settings_type_without_declaration_raises_with_service_name() -> None:
        """An absent settings class cannot silently select the test base settings."""

        class _MissingSettingsService(FlextTestsServiceBase[str]):
            @classmethod
            @override
            def runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
                return m.RuntimeBootstrapOptions(settings_type=None)

        with pytest.raises(TypeError, match="_MissingSettingsService"):
            _MissingSettingsService.test_settings_type()

    @staticmethod
    def test_settings_type_raises_type_error_naming_the_class() -> None:
        """A settings type outside the ``FlextTestsSettings`` tree fails loudly."""

        class _WrongSettingsService(FlextTestsServiceBase[str]):
            @classmethod
            @override
            def runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
                return m.RuntimeBootstrapOptions(settings_type=FlextSettings)

        with pytest.raises(TypeError, match="_WrongSettingsService"):
            _WrongSettingsService.test_settings_type()

    @classmethod
    def _run_consumer(
        cls,
        pytester: pytest.Pytester,
        source: str,
        *,
        exports: str = "",
        conftest: str | None = None,
    ) -> pytest.RunResult:
        """Exercise the public plugin in an isolated, real consumer process.

        Returns:
            The consumer's observable pytest outcome.

        """
        package_dir = pytester.path / "consumer_probe"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text(exports, encoding=c.DEFAULT_ENCODING)
        (package_dir / "test_probe.py").write_text(source, encoding=c.DEFAULT_ENCODING)
        if conftest is not None:
            (package_dir / "conftest.py").write_text(
                conftest, encoding=c.DEFAULT_ENCODING
            )
        return u.Tests.pytest_subprocess(
            pytester,
            *cls._consumer_options(),
            str(package_dir / "test_probe.py"),
        )

    @pytest.mark.slow
    def test_runtime_does_not_interpret_an_unrelated_service_export(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """A consumer's unrelated ``s`` is not treated as a dependency provider."""
        result = self._run_consumer(
            pytester,
            "from flext_tests import FlextTestsCase\n"
            "from . import s\n\n"
            "class TestProbe(FlextTestsCase):\n"
            "    def test_probe(self) -> None:\n"
            "        assert s is object\n",
            exports="s = object\n",
        )
        result.assert_outcomes(passed=1)

    @pytest.mark.slow
    def test_runtime_does_not_require_a_package_service_export(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """The public lifecycle fixture does not infer a consumer service."""
        result = self._run_consumer(
            pytester,
            "from flext_tests import FlextTestsCase\n\n"
            "class TestProbe(FlextTestsCase):\n"
            "    def test_probe(self, test_runtime: None) -> None:\n"
            "        assert test_runtime is None\n",
        )
        result.assert_outcomes(passed=1)

    @pytest.mark.slow
    def test_runtime_uses_an_explicit_service_without_unrelated_facade_exports(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Only the declared service participates in its explicit lifecycle."""
        result = self._run_consumer(
            pytester,
            "from flext_tests import FlextTestsCase\n"
            "from . import s\n\n"
            "class TestProbe(FlextTestsCase):\n"
            "    def test_probe(self) -> None:\n"
            "        with s[bool].isolated_test_runtime() as service:\n"
            "            assert service is s[bool].fetch_global()\n"
            "            assert service.settings is s[bool].fetch_settings()\n",
            exports="from flext_tests import s\n",
        )
        result.assert_outcomes(passed=1)

    @pytest.mark.slow
    def test_runtime_preserves_explicit_dependencies_and_resets_after_failure(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Real hooks clean state before and after both passing and failing items."""
        state_key = "runtime-isolation-probe"
        result = self._run_consumer(
            pytester,
            "from flext_tests import "
            "FlextTestsCase, FlextTestsUtilities, p, s, tm, u\n\n"
            "class TestProbe(FlextTestsCase):\n"
            "    def test_success(self, checked_container: p.Container) -> None:\n"
            "        assert u is FlextTestsUtilities\n"
            "        with s[bool].isolated_test_runtime() as service:\n"
            "            assert service.settings is s[bool].fetch_settings()\n"
            f"        checked_container.bind({state_key!r}, True)\n"
            "    def test_failure(self, checked_container: p.Container) -> None:\n"
            f"        checked_container.bind({state_key!r}, True)\n"
            "        tm.reject('intentional runtime failure')\n",
            conftest=(
                "from collections.abc import Iterator\n"
                "import pytest\n"
                "from flext_core import FlextContainer\n"
                "from flext_tests import p\n\n"
                "def pytest_collection_finish(session: pytest.Session) -> None:\n"
                f"    FlextContainer().bind({state_key!r}, True)\n\n"
                "@pytest.fixture\n"
                "def checked_container() -> Iterator[p.Container]:\n"
                "    container = FlextContainer()\n"
                f"    assert container.resolve({state_key!r}).failure\n"
                "    yield container\n\n"
                "def pytest_runtest_logreport(report: pytest.TestReport) -> None:\n"
                "    if report.when == 'teardown':\n"
                f"        assert FlextContainer().resolve({state_key!r}).failure\n"
            ),
        )
        expected = {"passed": 1, "failed": 1}
        tm.that(
            result.parseoutcomes() == expected,
            truth=True,
            assertion_message=f"{result.stdout.str()}\n{result.stderr.str()}",
        )
        result.assert_outcomes(**expected)
        result.stdout.fnmatch_lines(["*intentional runtime failure*"])
