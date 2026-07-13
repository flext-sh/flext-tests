"""Configuration helpers for the enforcement pytest plugin."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import pytest

from flext_tests import c, m, u
from flext_tests._fixtures._enforcement_parts import registry


class SessionConfig:
    """Session-scoped stash slot holding the resolved enforcement configuration."""

    stash_config: ClassVar[pytest.StashKey[m.Tests.EnforcementDispatcherConfig]] = (
        pytest.StashKey()
    )
    value: ClassVar[pytest.Config | None] = None


def discover_workspace_root(start: Path) -> Path | None:
    """Walk upward from ``start`` to find the FLEXT workspace root."""
    for candidate in (start, *start.parents):
        if all(
            (candidate / marker).exists()
            for marker in c.Tests.ENFORCEMENT_WORKSPACE_MARKERS
        ):
            return candidate
    return None


def split_csv(raw: str | None) -> frozenset[str]:
    """Split a comma-separated option value into a normalized frozen set."""
    if not raw:
        return frozenset()
    return frozenset(part.strip() for part in raw.split(",") if part.strip())


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register CLI options for the enforcement dispatcher."""
    group = parser.getgroup("flext-enforce", "FLEXT cross-layer enforcement catalog")
    group.addoption(
        "--flext-enforce",
        action="store_true",
        default=False,
        help=(
            "Force-enable the FLEXT enforcement dispatcher (default: auto - "
            "enabled when the pytest rootdir is the workspace root)."
        ),
    )
    group.addoption(
        "--no-flext-enforce",
        action="store_true",
        default=False,
        help="Disable the FLEXT enforcement dispatcher.",
    )
    group.addoption(
        "--flext-enforce-strict",
        action="store_true",
        default=False,
        help="Promote runtime enforcement warnings to pytest failures.",
    )
    group.addoption(
        "--flext-enforce-rules",
        action="store",
        default="",
        help="Comma-separated ENFORCE-NNN allow list.",
    )
    group.addoption(
        "--flext-enforce-exclude-rules",
        action="store",
        default="",
        help="Comma-separated ENFORCE-NNN block list.",
    )
    group.addoption(
        "--flext-enforce-workspace-root",
        action="store",
        default="",
        help="Override workspace root auto-detection with an explicit path.",
    )


def resolve_config(config: pytest.Config) -> m.Tests.EnforcementDispatcherConfig:
    """Build and cache the dispatcher's resolved configuration."""
    stashed = config.stash.get(SessionConfig.stash_config, None)
    if stashed is not None:
        return stashed

    disabled = bool(config.getoption("--no-flext-enforce"))
    forced = bool(config.getoption("--flext-enforce"))
    strict = bool(config.getoption("--flext-enforce-strict"))
    include = split_csv(str(config.getoption("--flext-enforce-rules") or ""))
    exclude = split_csv(str(config.getoption("--flext-enforce-exclude-rules") or ""))
    override_root = str(config.getoption("--flext-enforce-workspace-root") or "")
    rootpath = Path(config.rootpath).resolve()

    if override_root:
        workspace_root = Path(override_root).resolve()
    elif forced:
        workspace_root = discover_workspace_root(rootpath)
    else:
        discovered = discover_workspace_root(rootpath)
        workspace_root = discovered if discovered == rootpath else None

    resolved = m.Tests.EnforcementDispatcherConfig(
        active=not disabled and workspace_root is not None,
        strict=strict,
        include=include,
        exclude=exclude,
        workspace_root=workspace_root,
    )
    config.stash[SessionConfig.stash_config] = resolved
    return resolved


def active_rules(
    cfg: m.Tests.EnforcementDispatcherConfig,
) -> tuple[m.EnforcementRuleSpec, ...]:
    """Return enabled catalog rules after applying include/exclude filters."""
    catalog = u.build_canonical_catalog()
    rules: list[m.EnforcementRuleSpec] = []
    for rule in catalog.rules:
        if not rule.enabled:
            continue
        if cfg.include and rule.id not in cfg.include:
            continue
        if rule.id in cfg.exclude:
            continue
        rules.append(rule)
    return tuple(rules)


def pytest_configure(config: pytest.Config) -> None:
    """Register filterwarnings for every active runtime-warning rule."""
    cfg = resolve_config(config)
    if not cfg.active:
        return
    for rule in active_rules(cfg):
        if rule.source.kind != "runtime_warning":
            continue
        category = getattr(rule.source, "category", None)
        if not category:
            continue
        action = (
            "error" if cfg.strict and rule.promote_to_error_when_strict else "default"
        )
        config.addinivalue_line("filterwarnings", f"{action}::{category}")
    for contribution in registry.builders().values():
        if contribution.configure is not None:
            contribution.configure(config, cfg)


__all__: list[str] = [
    "SessionConfig",
    "active_rules",
    "discover_workspace_root",
    "pytest_addoption",
    "pytest_configure",
    "resolve_config",
    "split_csv",
]
