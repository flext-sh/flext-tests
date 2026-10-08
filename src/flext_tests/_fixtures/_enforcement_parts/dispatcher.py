"""Enforcement dispatcher behind the ``flext_tests_enforcement`` pytest plugin.

Activation resolves from the pytest options, the rootdir and the workspace
markers alone. The module itself stays import-light: the enforcement catalog,
its models and the builder load through the deferred ``import_module`` form
only once a governed session reaches them, so every pytest process that
enforcement does not govern (a nested runner project, a sandbox, a worker
outside the workspace) starts without importing the full facade tree.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import math
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, cast

import pytest

from flext_tests import c

if TYPE_CHECKING:
    import warnings

    from flext_tests import m, t


class FlextTestsEnforcementDispatcher:
    """Resolve the session activation and run every enforcement hook body."""

    stash_root: ClassVar[pytest.StashKey[Path | None]] = pytest.StashKey()
    stash_config: ClassVar[pytest.StashKey[m.Tests.EnforcementDispatcherConfig]] = (
        pytest.StashKey()
    )
    session_config: ClassVar[pytest.Config | None] = None

    @staticmethod
    def discover_repository_root(start: Path) -> Path | None:
        """Walk upward from ``start`` to find the FLEXT workspace root.

        Returns:
            The resulting ``Path | None``.
        """
        for candidate in (start, *start.parents):
            if all(
                (candidate / marker).exists()
                for marker in c.Tests.ENFORCEMENT_WORKSPACE_MARKERS
            ):
                return candidate
        return None

    @staticmethod
    def split_csv(raw: str | None) -> frozenset[str]:
        """Split a comma-separated option value into a normalized frozen set.

        Returns:
            The resulting ``frozenset[str]``.
        """
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
        cls,
        config: pytest.Config,
        repository_root: Path,
    ) -> m.Tests.EnforcementDispatcherConfig:
        """Build and cache the configuration of an active enforcement session.

        Returns:
            The resulting ``m.Tests.EnforcementDispatcherConfig``.
        """
        stashed = config.stash.get(cls.stash_config, None)
        if stashed is not None:
            return stashed
        models = import_module("flext_tests").m
        resolved = models.Tests.EnforcementDispatcherConfig(
            strict=bool(config.getoption("--flext-enforce-strict")),
            include=cls.split_csv(str(config.getoption("--flext-enforce-rules") or "")),
            exclude=cls.split_csv(
                str(config.getoption("--flext-enforce-exclude-rules") or ""),
            ),
            repository_root=repository_root,
        )
        config.stash[cls.stash_config] = resolved
        return cast("m.Tests.EnforcementDispatcherConfig", resolved)

    @classmethod
    def configure(cls, config: pytest.Config) -> None:
        """Register filterwarnings for every active runtime-warning rule."""
        repository_root = cls.active_root(config)
        if repository_root is None:
            return
        cfg = cls.resolve_config(config, repository_root)
        action = "error" if cfg.strict else "default"
        root = import_module("flext_tests")
        for rule in root.u.Tests.active_rules(cfg):
            if isinstance(rule.source, root.m.EnforcementRuntimeWarningSource):
                config.addinivalue_line(
                    "filterwarnings",
                    f"{action}::{rule.source.category}",
                )

    @staticmethod
    def slow_budget_seconds(config: pytest.Config) -> float | None:
        """Return the config-owned slow item budget, or None when unconfigured.

        Raises:
            UsageError: If FLEXT slow timeout policy; or if FLEXT slow timeout policy
                requires the pytest-timeout plugin.
        """
        raw_timeout = str(
            config.getini(c.Tests.ENFORCEMENT_SLOW_TIMEOUT_INI_OPTION)
        ).strip()
        if not raw_timeout:
            return None
        msg = (
            "FLEXT slow timeout policy: "
            f"{c.Tests.ENFORCEMENT_SLOW_TIMEOUT_INI_OPTION} must be a positive "
            "finite number"
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
        cls,
        session: pytest.Session,
        config: pytest.Config,
        items: list[pytest.Item],
    ) -> None:
        """Apply the slow budget, then append dispatcher items when active.

        Raises:
            UsageError: If FLEXT slow timeout policy.
        """
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
        builder = import_module(
            "flext_tests._fixtures._enforcement_parts.build",
        ).FlextTestsEnforcementBuilder
        items.extend(
            builder.build_items(
                session,
                cls.resolve_config(config, repository_root),
                collected_items=items,
            ),
        )

    @classmethod
    def record_warning(cls, warning_message: warnings.WarningMessage) -> None:
        """Count one captured runtime warning by its dotted category."""
        if cls.session_config is None:
            return
        repository_root = cls.active_root(cls.session_config)
        if repository_root is None:
            return
        category = warning_message.category
        cfg = cls.resolve_config(cls.session_config, repository_root)
        dotted = f"{category.__module__}.{category.__qualname__}"
        cfg.warning_counter[dotted] = cfg.warning_counter.get(dotted, 0) + 1

    @classmethod
    def terminal_summary(
        cls,
        terminalreporter: pytest.TerminalReporter,
        config: pytest.Config,
    ) -> None:
        """Print the per-kind breakdown at the end of the session."""
        repository_root = cls.active_root(config)
        if repository_root is None:
            return
        cfg = cls.resolve_config(config, repository_root)
        active = import_module("flext_tests").u.Tests.active_rules(cfg)
        kinds: t.MutableMappingKV[str, int] = {}
        for rule in active:
            kinds[rule.source.kind] = kinds.get(rule.source.kind, 0) + 1
        terminalreporter.write_sep("-", "flext-enforce", yellow=True)
        terminalreporter.write_line(
            f"catalog active: {len(active)} rules across {len(kinds)} source kinds",
        )
        for kind in sorted(kinds):
            terminalreporter.write_line(f"  {kind}: {kinds[kind]}")
        terminalreporter.write_line(
            f"runtime warnings captured: {sum(cfg.warning_counter.values())}",
        )


__all__: list[str] = ["FlextTestsEnforcementDispatcher"]
