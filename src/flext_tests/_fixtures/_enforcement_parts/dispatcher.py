"""Enforcement dispatcher behind the ``flext_tests_enforcement`` pytest plugin.

Activation resolves from the pytest options, the rootdir and the workspace
markers alone. The enforcement catalog, its models and the builder load only
once a session is proven active, so every pytest process that enforcement does
not govern (a nested runner project, a sandbox, a worker outside the workspace)
starts without importing the full facade tree.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

import pytest

from flext_tests import c
from flext_tests.enforcement_plugin import SLOW_TIMEOUT_INI_OPTION

if TYPE_CHECKING:
    from flext_tests import m, p, t


class FlextTestsEnforcementDispatcher:
    """Resolve the session activation and run every enforcement hook body."""

    stash_root: ClassVar[pytest.StashKey[Path | None]] = pytest.StashKey()
    stash_config: ClassVar[pytest.StashKey[m.Tests.EnforcementDispatcherConfig]] = (
        pytest.StashKey()
    )
    session_config: ClassVar[pytest.Config | None] = None

    @staticmethod
    def discover_repository_root(start: Path) -> Path | None:
        """Walk upward from ``start`` to find the FLEXT workspace root."""
        for candidate in (start, *start.parents):
            if all(
                (candidate / marker).exists()
                for marker in c.Tests.ENFORCEMENT_WORKSPACE_MARKERS
            ):
                return candidate
        return None

    @staticmethod
    def split_csv(raw: str | None) -> frozenset[str]:
        """Split a comma-separated option value into a normalized frozen set."""
        if not raw:
            return frozenset()
        return frozenset(part.strip() for part in raw.split(",") if part.strip())

    @classmethod
    def active_root(cls, config: pytest.Config) -> Path | None:
        """Return the governed workspace root, or None when enforcement is off."""
        if cls.stash_root in config.stash:
            return config.stash[cls.stash_root]
        override_root = str(config.getoption("--flext-enforce-workspace-root") or "")
        rootpath = Path(config.rootpath).resolve()
        repository_root: Path | None
        if config.getoption("--no-flext-enforce"):
            repository_root = None
        elif override_root:
            repository_root = Path(override_root).resolve()
        elif config.getoption("--flext-enforce"):
            repository_root = cls.discover_repository_root(rootpath)
        else:
            discovered = cls.discover_repository_root(rootpath)
            repository_root = discovered if discovered == rootpath else None
        config.stash[cls.stash_root] = repository_root
        return repository_root

    @classmethod
    def resolve_config(
        cls, config: pytest.Config, repository_root: Path
    ) -> m.Tests.EnforcementDispatcherConfig:
        """Build and cache the configuration of an active enforcement session."""
        stashed = config.stash.get(cls.stash_config, None)
        if stashed is not None:
            return stashed
        from flext_tests import m

        resolved = m.Tests.EnforcementDispatcherConfig(
            strict=bool(config.getoption("--flext-enforce-strict")),
            include=cls.split_csv(str(config.getoption("--flext-enforce-rules") or "")),
            exclude=cls.split_csv(
                str(config.getoption("--flext-enforce-exclude-rules") or "")
            ),
            repository_root=repository_root,
        )
        config.stash[cls.stash_config] = resolved
        return resolved

    @classmethod
    def configure(cls, config: pytest.Config) -> None:
        """Register filterwarnings for every active runtime-warning rule."""
        repository_root = cls.active_root(config)
        if repository_root is None:
            return
        from flext_tests.utilities import u

        cfg = cls.resolve_config(config, repository_root)
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
        repository_root = cls.active_root(config)
        if repository_root is None or hasattr(config, "workerinput"):
            return
        from .build import FlextTestsEnforcementBuilder

        items.extend(
            FlextTestsEnforcementBuilder.build_items(
                session,
                cls.resolve_config(config, repository_root),
                collected_items=items,
            )
        )

    @classmethod
    def record_warning(cls, warning_message: p.AttributeProbe) -> None:
        """Count one captured runtime warning by its dotted category."""
        if cls.session_config is None:
            return
        repository_root = cls.active_root(cls.session_config)
        category = getattr(warning_message, "category", None)
        if repository_root is None or category is None:
            return
        cfg = cls.resolve_config(cls.session_config, repository_root)
        dotted = f"{category.__module__}.{category.__qualname__}"
        cfg.warning_counter[dotted] = cfg.warning_counter.get(dotted, 0) + 1

    @classmethod
    def terminal_summary(
        cls, terminalreporter: pytest.TerminalReporter, config: pytest.Config
    ) -> None:
        """Print the per-kind breakdown at the end of the session."""
        repository_root = cls.active_root(config)
        if repository_root is None:
            return
        from flext_tests.utilities import u

        cfg = cls.resolve_config(config, repository_root)
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
