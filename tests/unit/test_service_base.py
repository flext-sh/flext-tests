"""Behavioral coverage for the typed service base (S6, flext-4jtcb.5).

Every test exercises the PUBLIC contract of ``s`` (``FlextTestsServiceBase``) and
the pytest plugin's runtime-alias binding hook: observable return values,
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
from flext_infra import FlextInfraConstants, config as infra_config

from flext_core import FlextSettings
from flext_tests import FlextTestsServiceBase, m, tm
from tests import u


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
        loop_scope = (
            infra_config.Infra.tooling.tools.pytest.asyncio_default_fixture_loop_scope
        )
        return (
            "-o",
            f"{FlextInfraConstants.Infra.ASYNCIO_DEFAULT_FIXTURE_LOOP_SCOPE}={loop_scope}",
        )

    class Tests:
        """flext-tests service-base test namespace."""

    # ---- isolated_test_runtime(build=...) for port-bearing services --------

    @staticmethod
    def test_isolated_test_runtime_builds_port_service_with_real_adapter() -> None:
        """A port-bearing service is constructed explicitly with a real adapter."""
        with u.Tests.EchoService.isolated_test_runtime(
            build=lambda: u.Tests.EchoService(port=u.Tests.MemoryEcho()),
        ) as service:
            result = service.run()
            tm.that(result.success, eq=True)
            tm.that(result.unwrap(), eq="HI")

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
            tm.that(service is FlextTestsServiceBase.fetch_global(), eq=True)

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

    # ---- runtime-alias binding hook: typed 's', no getattr substitution ----

    @pytest.mark.slow
    def test_runtime_alias_hook_rejects_a_package_without_a_valid_service_type(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """The real ``pytest_runtest_setup`` hook fails loudly for a bad package.

        A package whose ``s`` is not a ``FlextTestsServiceBase`` subclass
        (settings.py:46-48) raises; it never silently substitutes the base.
        The probe is class-style because the runtime alias contract binds the
        ``FlextTestsCase`` runtime: function-style tests never trigger it.
        """
        package_dir = pytester.path / "badpkg"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text("s = object\n", encoding="utf-8")
        (package_dir / "test_probe.py").write_text(
            "import flext_tests\n"
            "\n"
            "\n"
            "class TestProbe(flext_tests.FlextTestsCase):\n"
            "    def test_probe(self) -> None:\n"
            "        pass\n",
            encoding="utf-8",
        )
        result = pytester.runpytest_subprocess(
            *self._consumer_options(),
            str(package_dir / "test_probe.py"),
        )
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*TypeError*badpkg*"])

    def test_runtime_alias_hook_rejects_a_package_without_the_service_alias(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """A package root without ``s`` raises; it never substitutes the base.

        The probe is class-style: the alias contract binds the runtime for
        ``FlextTestsCase`` tests, so the rejection fires where the binding
        actually happens.
        """
        package_dir = pytester.path / "noservicepkg"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text("", encoding="utf-8")
        (package_dir / "test_probe.py").write_text(
            "import flext_tests\n"
            "\n"
            "\n"
            "class TestProbe(flext_tests.FlextTestsCase):\n"
            "    def test_probe(self) -> None:\n"
            "        pass\n",
            encoding="utf-8",
        )
        result = pytester.runpytest(
            *self._consumer_options(),
            str(package_dir / "test_probe.py"),
        )
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*AttributeError*noservicepkg*s*"])

    def test_runtime_alias_hook_rejects_a_package_missing_a_facade_letter(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """A package root missing a canonical facade letter fails loudly.

        The hook never substitutes a flext-tests letter for a missing
        package-local one: the package root must re-export every canonical
        letter (settings.py:65-74).
        """
        init_lines = [
            "from flext_tests import FlextTestsServiceBase, e, m, p, r, t, u",
            "class Srv(FlextTestsServiceBase):",
            "    pass",
            "s = Srv",
        ]
        package_dir = pytester.path / "noletterpkg"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text(
            "\n".join(init_lines) + "\n",
            encoding="utf-8",
        )
        (package_dir / "test_probe.py").write_text(
            "from flext_tests import FlextTestsCase\n"
            "\n"
            "class TestsProbe(FlextTestsCase):\n"
            "    def test_probe(self) -> None:\n"
            "        pass\n",
            encoding="utf-8",
        )
        result = pytester.runpytest(
            *self._consumer_options(),
            str(package_dir / "test_probe.py"),
        )
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*AttributeError*noletterpkg*'c'*"])

    def test_runtime_alias_hook_binds_the_package_local_letters(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """A well-formed package gets its own letters bound, never substitutes.

        The probe package overrides ``u`` with the core utilities module; the
        bound instance alias must be exactly that package-local value.
        """
        init_lines = [
            "import flext_core",
            "from flext_tests import FlextTestsServiceBase, c, e, m, p, r, t",
            "class Srv(FlextTestsServiceBase):",
            "    pass",
            "s = Srv",
            "u = flext_core.u",
        ]
        package_dir = pytester.path / "localpkg"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text(
            "\n".join(init_lines) + "\n",
            encoding="utf-8",
        )
        (package_dir / "test_probe.py").write_text(
            "import flext_core\n"
            "from flext_tests import FlextTestsCase\n"
            "\n"
            "class TestsProbe(FlextTestsCase):\n"
            "    def test_probe(self) -> None:\n"
            "        assert self.u is flext_core.u\n",
            encoding="utf-8",
        )
        result = pytester.runpytest(
            *self._consumer_options(),
            str(package_dir / "test_probe.py"),
        )
        result.assert_outcomes(passed=1)
