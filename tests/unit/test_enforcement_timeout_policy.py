"""Behavioral contracts for the canonical pytest timeout policy."""

from __future__ import annotations

from typing import ClassVar

import pytest

from flext_tests import FlextTestsConfig, c, config, tm, u


class TestsFlextTestsEnforcementTimeoutPolicy:
    """Exercise timeout enforcement through the installed pytest11 plugin."""

    policy_seconds: ClassVar[float] = 2.5

    def test_project_config_import_roundtrips_typed_policy(self) -> None:
        """Loaded YAML survives a typed model round-trip without local expectations."""
        roundtripped = FlextTestsConfig.model_validate(config.model_dump())
        policy = roundtripped.Tests.enforcement.pytest_timeout
        tm.that(roundtripped, eq=config)
        tm.that(
            all(
                isinstance(key, c.Tests.PytestTimeoutIniKey)
                for key in policy.timeout_owned_ini_keys
            ),
            eq=True,
        )

    def test_typed_owner_rejects_func_only_weakening(self) -> None:
        """Schema-invalid policy cannot enable fixture-only timeout coverage."""
        payload = config.model_dump()
        payload["Tests"]["enforcement"]["pytest_timeout"]["allow_timeout_func_only"] = (
            True
        )
        with pytest.raises(ValueError, match="allow_timeout_func_only"):
            FlextTestsConfig.model_validate(payload)

    def test_typed_owner_rejects_unprotected_timeout_ini(self) -> None:
        """Schema-invalid policy cannot leave a timeout-owned INI replaceable."""
        payload = config.model_dump()
        policy = payload["Tests"]["enforcement"]["pytest_timeout"]
        protected = set(policy["timeout_owned_ini_keys"])
        protected.remove(c.Tests.PytestTimeoutIniKey.ADDOPTS)
        policy["timeout_owned_ini_keys"] = protected
        with pytest.raises(ValueError, match="timeout_owned_ini_keys"):
            FlextTestsConfig.model_validate(payload)

    @pytest.mark.parametrize("ratio", [None, 1.0, 0.5])
    def test_accepts_no_cli_override_exact_or_below_policy(
        self,
        pytester: pytest.Pytester,
        monkeypatch: pytest.MonkeyPatch,
        ratio: float | None,
    ) -> None:
        """No override and non-weakening CLI values preserve the configured ceiling."""
        u.Tests.pytester_make_timeout_ini(pytester, policy_seconds=self.policy_seconds)
        u.Tests.pytester_make_timeout_test(pytester)
        args = (
            ()
            if ratio is None
            else (f"{c.Tests.PYTEST_TIMEOUT_OPTION}={self.policy_seconds * ratio}",)
        )
        u.Tests.pytester_run_enforcement(pytester, monkeypatch, *args).assert_outcomes(
            passed=1
        )

    @pytest.mark.parametrize("ratio", [0.0, 2.0])
    def test_rejects_cli_timeout_that_disables_or_exceeds_policy(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, ratio: float
    ) -> None:
        """CLI cannot disable the timer or increase its configured ceiling."""
        u.Tests.pytester_make_timeout_ini(pytester, policy_seconds=self.policy_seconds)
        u.Tests.pytester_make_timeout_test(pytester)
        u.Tests.pytester_assert_usage_error(
            u.Tests.pytester_run_enforcement(
                pytester,
                monkeypatch,
                f"{c.Tests.PYTEST_TIMEOUT_OPTION}={self.policy_seconds * ratio}",
            )
        )

    @pytest.mark.parametrize("ratio", [1.0, 0.5])
    def test_accepts_marker_at_or_below_policy(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, ratio: float
    ) -> None:
        """A marker may only retain or tighten the configured item ceiling."""
        u.Tests.pytester_make_timeout_ini(pytester, policy_seconds=self.policy_seconds)
        u.Tests.pytester_make_timeout_test(
            pytester, marker=str(self.policy_seconds * ratio)
        )
        u.Tests.pytester_run_enforcement(pytester, monkeypatch).assert_outcomes(
            passed=1
        )

    @pytest.mark.parametrize("ratio", [1.0, 0.5])
    def test_accepts_timeout_ini_at_or_below_addopts_cap(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, ratio: float
    ) -> None:
        """Optional timeout ini may retain or tighten the addopts-owned cap."""
        u.Tests.pytester_make_timeout_ini(
            pytester,
            policy_seconds=self.policy_seconds,
            timeout_ini=self.policy_seconds * ratio,
        )
        u.Tests.pytester_make_timeout_test(pytester)
        u.Tests.pytester_run_enforcement(pytester, monkeypatch).assert_outcomes(
            passed=1
        )

    @pytest.mark.parametrize(
        "marker",
        [
            "0",
            f"{policy_seconds * 2}",
            f"1.0, {c.Tests.PYTEST_TIMEOUT_MARKER}=1.0",
            f"1.0, 'signal', {c.Tests.PYTEST_TIMEOUT_MARKER_METHOD_KEY}='thread'",
            "1.0, 'signal', False",
            f"1.0, {c.Tests.PYTEST_TIMEOUT_MARKER_FUNC_ONLY_KEY}=True",
            "1.0, unsupported=True",
        ],
    )
    def test_rejects_weakening_or_conflicting_timeout_marker(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, marker: str
    ) -> None:
        """Marker zero, excess, duplicate values, and func-only are forbidden."""
        u.Tests.pytester_make_timeout_ini(pytester, policy_seconds=self.policy_seconds)
        u.Tests.pytester_make_timeout_test(pytester, marker=marker)
        u.Tests.pytester_assert_usage_error(
            u.Tests.pytester_run_enforcement(pytester, monkeypatch)
        )

    def test_rejects_duplicate_addopts_timeout(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Configured addopts must contain one and only one canonical timeout."""
        u.Tests.pytester_make_timeout_ini(
            pytester, policy_seconds=self.policy_seconds, duplicate_addopts=True
        )
        u.Tests.pytester_make_timeout_test(pytester)
        u.Tests.pytester_assert_usage_error(
            u.Tests.pytester_run_enforcement(pytester, monkeypatch)
        )

    def test_rejects_missing_addopts_timeout(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Timeout ini cannot replace the missing canonical addopts owner."""
        u.Tests.pytester_make_timeout_ini(
            pytester,
            policy_seconds=self.policy_seconds,
            include_addopts=False,
            timeout_ini=self.policy_seconds,
        )
        u.Tests.pytester_make_timeout_test(pytester)
        u.Tests.pytester_assert_usage_error(
            u.Tests.pytester_run_enforcement(pytester, monkeypatch)
        )

    def test_rejects_timeout_ini_above_addopts_cap(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Timeout ini cannot exceed the canonical addopts-owned cap."""
        u.Tests.pytester_make_timeout_ini(
            pytester,
            policy_seconds=self.policy_seconds,
            timeout_ini=self.policy_seconds * 2,
        )
        u.Tests.pytester_make_timeout_test(pytester)
        u.Tests.pytester_assert_usage_error(
            u.Tests.pytester_run_enforcement(pytester, monkeypatch)
        )

    def test_rejects_configured_func_only(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Configuration cannot exclude fixture setup and teardown from the timer."""
        u.Tests.pytester_make_timeout_ini(
            pytester, policy_seconds=self.policy_seconds, func_only=True
        )
        u.Tests.pytester_make_timeout_test(pytester)
        u.Tests.pytester_assert_usage_error(
            u.Tests.pytester_run_enforcement(pytester, monkeypatch)
        )

    @pytest.mark.parametrize(
        "override",
        [
            (c.Tests.PYTEST_OVERRIDE_INI_SHORT_OPTION, f"{key.value}=invalid")
            for key in sorted(
                config.Tests.enforcement.pytest_timeout.timeout_owned_ini_keys,
                key=lambda item: item.value,
            )
        ]
        + [
            (f"{c.Tests.PYTEST_OVERRIDE_INI_LONG_OPTION}={key.value}=invalid",)
            for key in sorted(
                config.Tests.enforcement.pytest_timeout.timeout_owned_ini_keys,
                key=lambda item: item.value,
            )
        ],
    )
    def test_rejects_override_ini_forms(
        self,
        pytester: pytest.Pytester,
        monkeypatch: pytest.MonkeyPatch,
        override: tuple[str, ...],
    ) -> None:
        """Both pytest override-ini spellings are rejected fail-closed."""
        u.Tests.pytester_make_timeout_ini(pytester, policy_seconds=self.policy_seconds)
        u.Tests.pytester_make_timeout_test(pytester)
        u.Tests.pytester_assert_usage_error(
            u.Tests.pytester_run_enforcement(pytester, monkeypatch, *override)
        )

    def test_accepts_unrelated_override_ini(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Unrelated pytest ini overrides remain valid configuration."""
        u.Tests.pytester_make_timeout_ini(pytester, policy_seconds=self.policy_seconds)
        u.Tests.pytester_make_timeout_test(pytester)
        u.Tests.pytester_run_enforcement(
            pytester,
            monkeypatch,
            c.Tests.PYTEST_OVERRIDE_INI_SHORT_OPTION,
            "console_output_style=classic",
        ).assert_outcomes(passed=1)

    @pytest.mark.parametrize(
        "variable", [c.Tests.PYTEST_TIMEOUT_ENV, c.Tests.PYTEST_ADDOPTS_ENV]
    )
    def test_rejects_environment_timeout_above_policy(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch, variable: str
    ) -> None:
        """Environment-controlled timeout precedence cannot weaken the ceiling."""
        u.Tests.pytester_make_timeout_ini(pytester, policy_seconds=self.policy_seconds)
        u.Tests.pytester_make_timeout_test(pytester)
        value = str(self.policy_seconds * 2)
        monkeypatch.setenv(
            variable,
            value
            if variable == c.Tests.PYTEST_TIMEOUT_ENV
            else f"{c.Tests.PYTEST_TIMEOUT_OPTION}={value}",
        )
        u.Tests.pytester_assert_usage_error(
            u.Tests.pytester_run_enforcement(pytester, monkeypatch)
        )

    def test_rejects_timeout_marker_added_by_late_collection_plugin(
        self, pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Trylast validation sees markers added by other collection plugins."""
        u.Tests.pytester_make_timeout_ini(pytester, policy_seconds=self.policy_seconds)
        u.Tests.pytester_make_timeout_test(pytester)
        pytester.makeconftest(
            "import pytest\n"
            "\n"
            "\n"
            "@pytest.hookimpl(tryfirst=True)\n"
            "def pytest_collection_modifyitems(items):\n"
            "    for item in items:\n"
            f"        item.add_marker(pytest.mark.{c.Tests.PYTEST_TIMEOUT_MARKER}(0))\n"
        )
        u.Tests.pytester_assert_usage_error(
            u.Tests.pytester_run_enforcement(pytester, monkeypatch)
        )
