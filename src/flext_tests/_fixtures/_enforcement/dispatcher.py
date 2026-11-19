"""Enforcement dispatcher behind the ``flext_tests_enforcement`` pytest plugin.

Activation resolves from the pytest options, the rootdir, the workspace
markers and, outside a workspace, the project manifest. The module itself stays
import-light: the enforcement catalog, its models and the builder load through
the deferred ``import_module`` form
only once a governed session reaches them, so every pytest process that
enforcement does not govern (a nested runner project, a sandbox, a worker
outside the workspace) starts without importing the full facade tree.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import math
import re
import tomllib
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

import pytest

# The letter facades are imported only by the methods of a governed session:
# an ungoverned pytest process must not compose the utilities facade, which
# would load flext_infra (see the module docstring).
from flext_tests._constants.validator import FlextTestsConstantsValidator

if TYPE_CHECKING:
    import warnings

    from flext_tests import p


class FlextTestsEnforcementDispatcher:
    """Resolve the session activation and run every enforcement hook body."""

    stash_root: ClassVar[pytest.StashKey[Path | None]] = pytest.StashKey()
    # A standalone project owns no workspace member to scan, so its session
    # consumes the rule catalog only when it collects a member project.
    stash_standalone: ClassVar[pytest.StashKey[bool]] = pytest.StashKey()
    stash_config: ClassVar[pytest.StashKey[p.Tests.EnforcementDispatcherConfig]] = (
        pytest.StashKey()
    )
    stash_budgeted: ClassVar[pytest.StashKey[bool]] = pytest.StashKey()
    stash_slow_limit: ClassVar[pytest.StashKey[float | None]] = pytest.StashKey()
    stash_durations: ClassVar[pytest.StashKey[dict[str, tuple[float, bool]]]] = (
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
                for marker in FlextTestsConstantsValidator.ENFORCEMENT_WORKSPACE_MARKERS
            ):
                return candidate
        return None

    @classmethod
    def declares_internal_flext(cls, root: Path) -> bool:
        """Return whether ``root`` is a standalone internal FLEXT project.

        Activation is derived from the project manifest — the declared FLEXT
        core dependency or an explicit internal kind — never from directory
        names or a project-name prefix.

        Returns:
            ``True`` when the manifest declares the internal project contract.

        """
        constants = FlextTestsConstantsValidator
        manifest = root / constants.ENFORCEMENT_PROJECT_MANIFEST
        if not manifest.is_file():
            return False
        document = tomllib.loads(
            manifest.read_text(encoding=constants.ENFORCEMENT_MANIFEST_ENCODING)
        )
        project = document.get("project", {})
        dependencies = (
            project.get("dependencies", ()) if isinstance(project, dict) else ()
        )
        marker = constants.ENFORCEMENT_PROJECT_DEPENDENCY
        pattern = rf"{re.escape(marker)}(?![A-Za-z0-9_-])"
        if isinstance(dependencies, list) and any(
            isinstance(item, str) and re.match(pattern, item.strip())
            for item in dependencies
        ):
            return True
        tool = document.get("tool", {})
        if not isinstance(tool, dict):
            return False
        flext = tool.get("flext", {})
        if (
            isinstance(flext, dict)
            and flext.get("kind") == constants.ENFORCEMENT_PROJECT_KIND
        ):
            return True
        uv = tool.get("uv", {})
        sources = uv.get("sources", {}) if isinstance(uv, dict) else {}
        return isinstance(sources, dict) and marker in sources

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
        config.stash[cls.stash_standalone] = False
        if config.getoption("--no-flext-enforce"):
            repository_root = None
        elif override_root:
            repository_root = Path(override_root).resolve()
        elif config.getoption("--flext-enforce"):
            repository_root = cls.discover_repository_root(rootpath)
        else:
            discovered = cls.discover_repository_root(rootpath)
            if discovered is not None:
                repository_root = discovered if discovered == rootpath else None
            elif cls.declares_internal_flext(rootpath):
                repository_root = rootpath
                config.stash[cls.stash_standalone] = True
            else:
                repository_root = None
        config.stash[cls.stash_root] = repository_root
        return repository_root

    @classmethod
    def resolve_config(
        cls,
        config: pytest.Config,
        repository_root: Path,
    ) -> p.Tests.EnforcementDispatcherConfig:
        """Build and cache the configuration of an active enforcement session.

        Returns:
            The resulting ``m.Tests.EnforcementDispatcherConfig``.

        """
        models = import_module("flext_tests").m

        stashed = config.stash.get(cls.stash_config, None)
        if stashed is not None:
            return stashed
        resolved = models.Tests.EnforcementDispatcherConfig(
            strict=bool(config.getoption("--flext-enforce-strict")),
            include=cls.split_csv(str(config.getoption("--flext-enforce-rules") or "")),
            exclude=cls.split_csv(
                str(config.getoption("--flext-enforce-exclude-rules") or ""),
            ),
            repository_root=repository_root,
            catalog_root=Path(config.rootpath).resolve(),
        )
        config.stash[cls.stash_config] = resolved
        return resolved

    @staticmethod
    def slow_budget_seconds(config: pytest.Config) -> float | None:
        """Return the config-owned slow item budget, or None when unconfigured.

        Raises:
            UsageError: If FLEXT slow timeout policy; or if FLEXT slow timeout policy
                requires the pytest-timeout plugin.

        """
        raw_timeout = str(
            config.getini(
                FlextTestsConstantsValidator.ENFORCEMENT_SLOW_TIMEOUT_INI_OPTION
            )
        ).strip()
        if not raw_timeout:
            return None
        msg = (
            "FLEXT slow timeout policy: "
            f"{FlextTestsConstantsValidator.ENFORCEMENT_SLOW_TIMEOUT_INI_OPTION} must "
            f"be a positive "
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

    @staticmethod
    def budget_markers() -> tuple[str, ...]:
        """Return every marker whose items run on the config-owned slow budget.

        Returns:
            The slow marker followed by the declared heavy-tier markers.

        """
        return (
            FlextTestsConstantsValidator.ENFORCEMENT_SLOW_MARKER,
            *FlextTestsConstantsValidator.ENFORCEMENT_HEAVY_TIER_MARKERS,
        )

    @classmethod
    def apply_slow_budget(
        cls,
        config: pytest.Config,
        items: list[pytest.Item],
    ) -> None:
        """Apply the shared slow budget independently of static enforcement.

        Raises:
            UsageError: If FLEXT slow timeout policy.

        """
        config.stash[cls.stash_slow_limit] = None
        slow_timeout = cls.slow_budget_seconds(config)
        config.stash[cls.stash_slow_limit] = slow_timeout
        markers = cls.budget_markers()
        for item in items if slow_timeout is not None else ():
            if item.stash.get(cls.stash_budgeted, False):
                continue
            if not any(item.get_closest_marker(marker) for marker in markers):
                continue
            if item.get_closest_marker("timeout") is not None:
                msg = (
                    "FLEXT slow timeout policy: explicit pytest.mark.timeout is "
                    f"forbidden; {item.nodeid} must use the config-owned slow budget"
                )
                raise pytest.UsageError(msg)
            item.stash[cls.stash_budgeted] = True
            if config.getoption("timeout") != 0:
                item.add_marker(pytest.mark.timeout(slow_timeout), append=False)

    @classmethod
    def collection_modifyitems(
        cls,
        session: pytest.Session,
        config: pytest.Config,
        items: list[pytest.Item],
    ) -> None:
        """Append dispatcher items when static enforcement is active."""
        repository_root = cls.active_root(config)
        if repository_root is None or hasattr(config, "workerinput"):
            return
        builder = import_module(
            "flext_tests._fixtures._enforcement.build",
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
    def record_duration(cls, report: pytest.TestReport) -> None:
        """Keep the native call-phase duration of one passed item and its slow mark.

        A timed-out item is already a failure, so only passed calls are kept.
        """
        config = cls.session_config
        if (
            config is None
            or report.when != FlextTestsConstantsValidator.ENFORCEMENT_CALL_PHASE
            or not report.passed
        ):
            return
        config.stash.setdefault(cls.stash_durations, {})[report.nodeid] = (
            report.duration,
            any(marker in report.keywords for marker in cls.budget_markers()),
        )

    @classmethod
    def slow_report(
        cls,
        terminalreporter: pytest.TerminalReporter,
        config: pytest.Config,
    ) -> None:
        """Print every passed item near its ordinary or slow limit."""
        ratio = FlextTestsConstantsValidator.ENFORCEMENT_SLOW_NEAR_LIMIT_RATIO
        ordinary = float(
            config.getoption(
                FlextTestsConstantsValidator.ENFORCEMENT_TIMEOUT_OPTION, None
            )
            or 0
        )
        # An xdist controller never collects, so it resolves the budget here.
        slow = (
            config.stash[cls.stash_slow_limit]
            if cls.stash_slow_limit in config.stash
            else cls.slow_budget_seconds(config)
        ) or 0.0
        durations: dict[str, tuple[float, bool]] = (
            config.stash.get(cls.stash_durations, None) or {}
        )
        near: list[tuple[float, bool, str]] = []
        for nodeid, (duration, marked) in durations.items():
            limit = slow if marked else ordinary
            if limit > 0 and duration >= limit * ratio:
                kind = "slow" if marked else "ordinary"
                share = duration / limit
                line = f"  {share:.0%} of the {limit:.2f}s {kind} limit "
                near.append((share, marked, f"{line}({duration:.2f}s): {nodeid}"))
        terminalreporter.write_sep(
            "-", FlextTestsConstantsValidator.ENFORCEMENT_SLOW_REPORT_TITLE, yellow=True
        )
        if not near:
            terminalreporter.write_line("no test near the ordinary or slow limit")
            return
        slow_count = sum(marked for _, marked, _ in near)
        ordinary_count = (
            f"{len(near) - slow_count} near the ordinary limit"
            if ordinary > 0
            else "ordinary limit not set, unmarked tests skipped"
        )
        terminalreporter.write_line(
            f"{ordinary_count}; {slow_count} near the slow limit",
        )
        for _, _, line in sorted(near, reverse=True):
            terminalreporter.write_line(line)

    @classmethod
    def terminal_summary(
        cls,
        terminalreporter: pytest.TerminalReporter,
        config: pytest.Config,
    ) -> None:
        """Print the per-kind breakdown and the slow-test report."""
        cls.enforcement_summary(terminalreporter, config)
        cls.slow_report(terminalreporter, config)

    @classmethod
    def enforcement_summary(
        cls,
        terminalreporter: pytest.TerminalReporter,
        config: pytest.Config,
    ) -> None:
        """Print the per-kind breakdown when static enforcement is active."""
        repository_root = cls.active_root(config)
        if repository_root is None:
            return
        cfg = cls.resolve_config(config, repository_root)
        terminalreporter.write_sep("-", "flext-enforce", yellow=True)
        if not config.stash[cls.stash_standalone]:
            active = import_module("flext_tests").u.Tests.active_rules(cfg)
            kinds: dict[str, int] = {}
            for rule in active:
                kinds[rule.source.kind] = kinds.get(rule.source.kind, 0) + 1
            terminalreporter.write_line(
                f"catalog active: {len(active)} rules across {len(kinds)} source kinds",
            )
            for kind in sorted(kinds):
                terminalreporter.write_line(f"  {kind}: {kinds[kind]}")
        terminalreporter.write_line(
            f"runtime warnings captured: {sum(cfg.warning_counter.values())}",
        )


__all__: list[str] = ["FlextTestsEnforcementDispatcher"]
