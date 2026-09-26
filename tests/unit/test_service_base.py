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
from pydantic import ValidationError

from flext_core import FlextSettings
from flext_tests import FlextTestsServiceBase, m, tm
from tests import u


class TestsFlextTestsServiceBase:
    """Behavioral contract for the ``FlextTestsServiceBase`` typed test hooks."""

    class Tests:
        """flext-tests service-base test namespace."""

    # ---- isolated_test_runtime(build=...) for port-bearing services --------

    def test_isolated_test_runtime_builds_port_service_with_real_adapter(self) -> None:
        """A port-bearing service is constructed explicitly with a real adapter."""
        with u.Tests.EchoService.isolated_test_runtime(
            build=lambda: u.Tests.EchoService(port=u.Tests.MemoryEcho())
        ) as service:
            result = service.run()
            tm.that(result.success, eq=True)
            tm.that(result.unwrap(), eq="HI")

    def test_isolated_test_runtime_without_build_still_needs_fetch_global(self) -> None:
        """Omitting ``build`` for a port-bearing service still fails validated."""
        with (
            pytest.raises(ValidationError, match="port"),
            u.Tests.EchoService.isolated_test_runtime(),
        ):
            pytest.fail("unreachable: fetch_global() must raise ValidationError")

    def test_isolated_test_runtime_without_build_resolves_a_port_free_service(
        self,
    ) -> None:
        """A port-free service keeps resolving through ``fetch_global()``."""
        with FlextTestsServiceBase.isolated_test_runtime() as service:
            tm.that(service is FlextTestsServiceBase.fetch_global(), eq=True)

    # ---- test_settings_type: raise, never fall back -------------------------

    def test_settings_type_raises_type_error_naming_the_class(self) -> None:
        """A settings type outside the ``FlextTestsSettings`` tree fails loudly."""

        class _WrongSettingsService(FlextTestsServiceBase[str]):
            @classmethod
            @override
            def runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
                return m.RuntimeBootstrapOptions(settings_type=FlextSettings)

        with pytest.raises(TypeError, match="_WrongSettingsService"):
            _WrongSettingsService.test_settings_type()

    # ---- runtime-alias binding hook: typed 's', no getattr substitution ----

    def test_runtime_alias_hook_rejects_a_package_without_a_valid_service_type(
        self, pytester: pytest.Pytester
    ) -> None:
        """The real ``pytest_runtest_setup`` hook fails loudly for a bad package.

        A package whose ``s`` is not a ``FlextTestsServiceBase`` subclass
        (settings.py:46-48) raises; it never silently substitutes the base.
        """
        package_dir = pytester.path / "badpkg"
        package_dir.mkdir()
        (package_dir / "__init__.py").write_text("s = object\n", encoding="utf-8")
        (package_dir / "test_probe.py").write_text(
            "def test_probe() -> None:\n    pass\n", encoding="utf-8"
        )
        result = pytester.runpytest_subprocess(str(package_dir / "test_probe.py"))
        result.assert_outcomes(errors=1)
        result.stdout.fnmatch_lines(["*TypeError*badpkg*"])
