"""Enforcement dispatcher behind the ``flext_tests_enforcement`` pytest plugin."""

from __future__ import annotations

import math
from pathlib import Path
from typing import ClassVar

import pytest

from flext_tests import m, p, t
from flext_tests.enforcement_plugin import SLOW_TIMEOUT_INI_OPTION
from flext_tests.utilities import u

from .build import FlextTestsEnforcementBuilder


class FlextTestsEnforcementDispatcher:
    """Resolve the session configuration and run every enforcement hook body."""

    stash_config: ClassVar[pytest.StashKey[m.Tests.EnforcementDispatcherConfig]] = (
        pytest.StashKey()
    )
    session_config: ClassVar[pytest.Config | None] = None

    @classmethod
    def resolve_config(
        cls, config: pytest.Config
    ) -> m.Tests.EnforcementDispatcherConfig:
        """Build and cache the dispatcher's resolved configuration."""
        stashed = config.stash.get(cls.stash_config, None)
        if stashed is not None:
            return stashed
        forced = bool(config.getoption("--flext-enforce"))
        override_root = str(config.getoption("--flext-enforce-workspace-root") or "")
        rootpath = Path(config.rootpath).resolve()
        if override_root:
            repository_root = Path(override_root).resolve()
        elif forced:
            repository_root = u.Tests.discover_repository_root(rootpath)
        else:
            discovered = u.Tests.discover_repository_root(rootpath)
            repository_root = discovered if discovered == rootpath else None
        resolved = m.Tests.EnforcementDispatcherConfig(
            active=not bool(config.getoption("--no-flext-enforce"))
            and repository_root is not None,
            strict=bool(config.getoption("--flext-enforce-strict")),
            include=u.Tests.split_csv(
                str(config.getoption("--flext-enforce-rules") or "")
            ),
            exclude=u.Tests.split_csv(
                str(config.getoption("--flext-enforce-exclude-rules") or "")
            ),
            repository_root=repository_root,
        )
        config.stash[cls.stash_config] = resolved
        return resolved

    @classmethod
    def configure(cls, config: pytest.Config) -> None:
        """Register filterwarnings for every active runtime-warning rule."""
        cfg = cls.resolve_config(config)
        if not cfg.active:
            return
        for rule in u.Tests.active_rules(cfg):
            category = getattr(rule.source, "category", None)
            if rule.source.kind != "runtime_warning" or not category:
                continue
            strict = cfg.strict and rule.promote_to_error_when_strict
            action = "error" if strict else "default"
            config.addinivalue_line("filterwarnings", f"{action}::{category}")

    @staticmethod
    def slow_budget_seconds(config: pytest.Config) -> float | None:
        """Return the config-owned slow item budget, or None when unconfigured."""
        raw_timeout = str(config.getini(SLOW_TIMEOUT_INI_OPTION)).strip()
        if not raw_timeout:
            return None
        msg = (
            "FLEXT slow timeout policy: "
            f"{SLOW_TIMEOUT_INI_OPTION} must be a positive finite number"
        )
        try:
            slow_timeout = float(raw_timeout)
        except ValueError as err:
            raise pytest.UsageError(msg) from err
        if not math.isfinite(slow_timeout) or slow_timeout <= 0:
            raise pytest.UsageError(msg)
        if not any(
            config.pluginmanager.hasplugin(plugin_name)
            for plugin_name in ("timeout", "pytest_timeout")
        ):
            msg = "FLEXT slow timeout policy requires the pytest-timeout plugin"
            raise pytest.UsageError(msg)
        return slow_timeout

    @classmethod
    def collection_modifyitems(
        cls, session: pytest.Session, config: pytest.Config, items: list[pytest.Item]
    ) -> None:
        """Apply the slow budget, then append dispatcher items when active."""
        slow_timeout = cls.slow_budget_seconds(config)
        for item in items if slow_timeout is not None else ():
            if item.get_closest_marker("timeout") is not None:
                msg = (
                    "FLEXT slow timeout policy: explicit pytest.mark.timeout is "
                    f"forbidden; {item.nodeid} must use the config-owned item budget"
                )
                raise pytest.UsageError(msg)
            if item.get_closest_marker("slow") is not None:
                item.add_marker(pytest.mark.timeout(slow_timeout), append=False)
        cfg = cls.resolve_config(config)
        if not cfg.active or hasattr(config, "workerinput"):
            return
        items.extend(
            FlextTestsEnforcementBuilder.build_items(
                session, cfg, collected_items=items
            )
        )

    @classmethod
    def record_warning(cls, warning_message: p.AttributeProbe) -> None:
        """Count one captured runtime warning by its dotted category."""
        if cls.session_config is None:
            return
        cfg = cls.resolve_config(cls.session_config)
        category = getattr(warning_message, "category", None)
        if not cfg.active or category is None:
            return
        dotted = f"{category.__module__}.{category.__qualname__}"
        cfg.warning_counter[dotted] = cfg.warning_counter.get(dotted, 0) + 1

    @classmethod
    def terminal_summary(
        cls, terminalreporter: pytest.TerminalReporter, config: pytest.Config
    ) -> None:
        """Print the per-kind breakdown at the end of the session."""
        cfg = cls.resolve_config(config)
        if not cfg.active:
            return
        active = u.Tests.active_rules(cfg)
        kinds: t.MutableMappingKV[str, int] = {}
        for rule in active:
            kinds[rule.source.kind] = kinds.get(rule.source.kind, 0) + 1
        terminalreporter.write_sep("-", "flext-enforce", yellow=True)
        terminalreporter.write_line(
            f"catalog active: {len(active)} rules across {len(kinds)} source kinds"
        )
        for kind in sorted(kinds):
            terminalreporter.write_line(f"  {kind}: {kinds[kind]}")
        terminalreporter.write_line(
            f"runtime warnings captured: {sum(cfg.warning_counter.values())}"
        )


__all__: list[str] = ["FlextTestsEnforcementDispatcher"]
