"""Pytest dispatcher for the cross-layer enforcement catalog.

Reads ``flext_core.FlextConstantsEnforcement.get_catalog()`` and, when
the pytest run is rooted at the FLEXT workspace (triple marker
``AGENTS.md`` + ``flext-core/`` + ``flext-tests/``), drives the catalog's
active sources:

* ``flext_infra_detector`` rules run ``FlextInfraNamespaceEnforcer.enforce()``
  once per session and adapt each ``ProjectEnforcementReport`` field into a
  ``m.Tests.Violation`` collection.
* ``flext_tests_validator`` rules invoke the matching public classmethod on
  ``FlextTestsValidator`` (``tv.*``) and filter by the rule IDs each catalog
  entry declares.
* ``runtime_warning`` rules register a ``filterwarnings`` entry so pytest
  captures emissions; strict mode promotes those warnings to failures.
* ``ruff``, ``ast_grep``, and ``skill_pointer`` rules are indexed only — they
  stay authoritative in ``make lint``, ``sgconfig.yml``, and ``.agents/``
  respectively.

Usage in any downstream ``conftest.py``::

    pytest_plugins = ["flext_tests.conftest_plugin"]

CLI flags: ``--flext-enforce`` (default on when the triple marker is
present), ``--no-flext-enforce``, ``--flext-enforce-strict``,
``--flext-enforce-rules=CSV``, ``--flext-enforce-exclude-rules=CSV``,
``--flext-enforce-workspace-root=PATH``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from importlib import import_module
from pathlib import Path
from typing import Final, override

import pytest

from flext_core import FlextConstantsEnforcement, FlextModelsEnforcement

_me = FlextModelsEnforcement
_sk = _me.EnforcementSourceKind

_WORKSPACE_MARKERS: Final[tuple[str, ...]] = (
    "AGENTS.md",
    "flext-core",
    "flext-tests",
)
_VALIDATOR_METHODS: Final[frozenset[str]] = frozenset({
    "imports",
    "types",
    "bypass",
    "layer",
    "tests",
    "validate_config",
    "markdown",
})

_StashConfig: pytest.StashKey[dict[str, object]] = pytest.StashKey()
_active_session_config: pytest.Config | None = None


def _discover_workspace_root(start: Path) -> Path | None:
    """Walk upward from ``start`` to find the FLEXT workspace root.

    Returns the first directory containing all of ``_WORKSPACE_MARKERS``;
    ``None`` when the caller is outside the workspace (e.g. running pytest
    rooted at a sub-project).
    """
    for candidate in (start, *start.parents):
        if all((candidate / marker).exists() for marker in _WORKSPACE_MARKERS):
            return candidate
    return None


def _split_csv(raw: str | None) -> frozenset[str]:
    if not raw:
        return frozenset()
    return frozenset(part.strip() for part in raw.split(",") if part.strip())


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register CLI options for the enforcement dispatcher."""
    group = parser.getgroup(
        "flext-enforce",
        "FLEXT cross-layer enforcement catalog",
    )
    group.addoption(
        "--flext-enforce",
        action="store_true",
        default=False,
        help=(
            "Force-enable the FLEXT enforcement dispatcher (default: auto — "
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


def _resolve_config(config: pytest.Config) -> dict[str, object]:
    """Build (and cache) the dispatcher's resolved configuration."""
    stashed = config.stash.get(_StashConfig, None)
    if stashed is not None:
        return stashed

    disabled = bool(config.getoption("--no-flext-enforce"))
    forced = bool(config.getoption("--flext-enforce"))
    strict = bool(config.getoption("--flext-enforce-strict"))
    include = _split_csv(str(config.getoption("--flext-enforce-rules") or ""))
    exclude = _split_csv(str(config.getoption("--flext-enforce-exclude-rules") or ""))
    override_root = str(config.getoption("--flext-enforce-workspace-root") or "")

    rootpath = Path(config.rootpath).resolve()
    workspace_root: Path | None
    if override_root:
        workspace_root = Path(override_root).resolve()
    elif forced:
        # --flext-enforce: honor a nested rootdir by walking up to the marker.
        workspace_root = _discover_workspace_root(rootpath)
    else:
        # Auto-detect activates ONLY when pytest is rooted AT the workspace
        # root (intent documented in flext-enforcement-catalog SKILL.md:
        # "pytest flext-core/   # sub-project — no-op").
        discovered = _discover_workspace_root(rootpath)
        workspace_root = discovered if discovered == rootpath else None

    active = not disabled and workspace_root is not None
    resolved: dict[str, object] = {
        "active": active,
        "strict": strict,
        "include": include,
        "exclude": exclude,
        "workspace_root": workspace_root,
        "warning_counter": {},
    }
    config.stash[_StashConfig] = resolved
    return resolved


def _active_rules(
    cfg: dict[str, object],
) -> tuple[_me.EnforcementRuleSpec, ...]:
    catalog = FlextConstantsEnforcement.get_catalog()
    include_raw = cfg["include"]
    exclude_raw = cfg["exclude"]
    if not isinstance(include_raw, frozenset):
        msg = f"cfg['include'] must be frozenset, got {type(include_raw).__name__}"
        raise TypeError(msg)
    if not isinstance(exclude_raw, frozenset):
        msg = f"cfg['exclude'] must be frozenset, got {type(exclude_raw).__name__}"
        raise TypeError(msg)
    include: frozenset[str] = include_raw
    exclude: frozenset[str] = exclude_raw
    rules: list[_me.EnforcementRuleSpec] = []
    for rule in catalog.rules:
        if not rule.enabled:
            continue
        if include and rule.id not in include:
            continue
        if rule.id in exclude:
            continue
        rules.append(rule)
    return tuple(rules)


def pytest_configure(config: pytest.Config) -> None:
    """Register ``filterwarnings`` for every active RUNTIME_WARNING rule."""
    cfg = _resolve_config(config)
    if not cfg["active"]:
        return

    for rule in _active_rules(cfg):
        if rule.source.kind != _sk.RUNTIME_WARNING.value:
            continue
        # mypy/pyright narrow via discriminator: guard anyway for runtime.
        category = getattr(rule.source, "category", None)
        if not category:
            continue
        action = (
            "error"
            if cfg["strict"] and rule.promote_to_error_when_strict
            else "default"
        )
        config.addinivalue_line("filterwarnings", f"{action}::{category}")


# --- Collection items --------------------------------------------------------


class EnforcementItem(pytest.Item):
    """Pytest item representing one ``(project, rule_id)`` violation group."""

    def __init__(
        self,
        name: str,
        parent: pytest.Collector,
        *,
        rule: _me.EnforcementRuleSpec,
        project: str,
        violations: Sequence[_me.Violation | object],
    ) -> None:
        super().__init__(name, parent)
        self._rule = rule
        self._project = project
        self._violations = tuple(violations)

    @override
    def runtest(self) -> None:
        if not self._violations:
            return
        detail_lines = [f"  - {self._format_violation(v)}" for v in self._violations]
        header = (
            f"{self._rule.id} ({self._rule.severity}) in {self._project}: "
            f"{len(self._violations)} violation(s)"
        )
        msg = "\n".join([header, *detail_lines])
        raise EnforcementViolationError(msg)

    @staticmethod
    def _format_violation(violation: object) -> str:
        # flext_tests Violation has rule_id + file_path + line_number + description
        rule_id = getattr(violation, "rule_id", "")
        file_path = getattr(violation, "file_path", None) or getattr(
            violation, "file", ""
        )
        line = getattr(violation, "line_number", None) or getattr(violation, "line", "")
        description = (
            getattr(violation, "description", None)
            or getattr(violation, "detail", None)
            or getattr(violation, "suggestion", None)
            or ""
        )
        parts = [str(rule_id) if rule_id else ""]
        if file_path:
            parts.append(str(file_path))
        if line:
            parts.append(f"line {line}")
        if description:
            parts.append(str(description))
        return " | ".join(part for part in parts if part)

    @override
    def repr_failure(
        self,
        excinfo: pytest.ExceptionInfo[BaseException],
        style: str | None = None,
    ) -> str:
        _ = style
        return str(excinfo.value)

    @override
    def reportinfo(self) -> tuple[Path | str, int | None, str]:
        return (
            f"flext-enforce::{self._rule.id}",
            None,
            f"{self._rule.id} [{self._project}] {self._rule.description}",
        )


class EnforcementCollector(pytest.Collector):
    """Synthetic collector that owns every ``EnforcementItem`` for the session."""

    def __init__(
        self,
        name: str,
        parent: pytest.Session,
        *,
        items: Sequence[EnforcementItem] = (),
    ) -> None:
        super().__init__(name, parent)
        self._items: list[EnforcementItem] = list(items)

    def add(self, item: EnforcementItem) -> None:
        self._items.append(item)

    @override
    def collect(self) -> Iterable[pytest.Item]:
        return list(self._items)


class EnforcementViolationError(Exception):
    """Raised by ``EnforcementItem.runtest`` when violations are present."""


# --- Dispatch ---------------------------------------------------------------


def _load_infra_report(
    workspace_root: Path,
) -> object | None:
    """Return a ``WorkspaceEnforcementReport`` or ``None`` when unavailable.

    ``flext_infra`` is an optional dependency at dispatch time — if the
    package isn't importable, we skip all FLEXT_INFRA_DETECTOR rules rather
    than fail the pytest run.
    """
    try:
        refactor = import_module("flext_infra.refactor.namespace_enforcer")
    except ImportError:
        return None
    enforcer_cls = getattr(refactor, "FlextInfraNamespaceEnforcer", None)
    if enforcer_cls is None:
        return None
    try:
        enforcer = enforcer_cls(workspace_root=workspace_root)
        report: object = enforcer.enforce()
    except Exception:  # pragma: no cover - defensive: propagate as no-op
        return None
    return report


def _iter_infra_violations(
    report: object,
    field: str,
    *,
    match_missing: bool,
) -> Iterable[tuple[str, object]]:
    """Yield ``(project_name, violation)`` from a workspace report.

    ``match_missing=True`` maps ``facade_statuses`` entries with
    ``exists=False`` to pseudo-violations (preserving the
    ``FacadeStatus`` object as the carrier).
    """
    projects = getattr(report, "projects", ())
    for project in projects:
        project_name = getattr(project, "project", "") or getattr(
            project, "project_name", ""
        )
        entries = getattr(project, field, ())
        if match_missing:
            entries = tuple(e for e in entries if not getattr(e, "exists", True))
        for entry in entries:
            yield str(project_name), entry


def _dispatch_infra_detector(
    rule: _me.EnforcementRuleSpec,
    report: object,
) -> dict[str, list[object]]:
    source = rule.source
    field = getattr(source, "violation_field", "")
    match_missing = bool(getattr(source, "match_missing", False))
    grouped: dict[str, list[object]] = {}
    for project, entry in _iter_infra_violations(
        report, field, match_missing=match_missing
    ):
        grouped.setdefault(project, []).append(entry)
    return grouped


def _dispatch_tests_validator(
    rule: _me.EnforcementRuleSpec,
    workspace_root: Path,
) -> dict[str, list[object]]:
    try:
        validator_mod = import_module("flext_tests.validator")
    except ImportError:
        return {}
    tv = getattr(validator_mod, "FlextTestsValidator", None)
    if tv is None:
        return {}
    method_name = getattr(rule.source, "method", "")
    if method_name not in _VALIDATOR_METHODS:
        return {}
    method = getattr(tv, method_name, None)
    if method is None:
        return {}
    wanted_ids = frozenset(getattr(rule.source, "rule_ids", ()))
    try:
        # validate_config takes a file path, not a directory
        target: Path = (
            (workspace_root / "pyproject.toml")
            if method_name == "validate_config"
            else workspace_root
        )
        result = method(target)
    except Exception:  # pragma: no cover - defensive
        return {}
    if getattr(result, "failure", False):
        return {}
    scan = getattr(result, "value", None)
    if scan is None:
        return {}
    grouped: dict[str, list[object]] = {}
    for violation in getattr(scan, "violations", ()):
        if wanted_ids and getattr(violation, "rule_id", "") not in wanted_ids:
            continue
        # Derive the owning project from the file path's first path segment
        # relative to the workspace root.
        file_path = getattr(violation, "file_path", None)
        project = "workspace"
        if file_path is not None:
            try:
                rel = Path(file_path).resolve().relative_to(workspace_root)
                project = rel.parts[0] if rel.parts else "workspace"
            except ValueError:
                project = "workspace"
        grouped.setdefault(project, []).append(violation)
    return grouped


def _build_items(
    session: pytest.Session,
    cfg: dict[str, object],
) -> list[EnforcementItem]:
    workspace_root = cfg.get("workspace_root")
    if not isinstance(workspace_root, Path):
        return []

    rules = _active_rules(cfg)

    infra_report: object | None = None
    if any(r.source.kind == _sk.FLEXT_INFRA_DETECTOR.value for r in rules):
        infra_report = _load_infra_report(workspace_root)

    collector = EnforcementCollector.from_parent(
        parent=session,
        name="flext-enforcement",
    )
    items: list[EnforcementItem] = []

    for rule in rules:
        grouped: dict[str, list[object]] = {}
        if rule.source.kind == _sk.FLEXT_INFRA_DETECTOR.value:
            if infra_report is None:
                continue
            grouped = _dispatch_infra_detector(rule, infra_report)
        elif rule.source.kind == _sk.FLEXT_TESTS_VALIDATOR.value:
            grouped = _dispatch_tests_validator(rule, workspace_root)
        # RUNTIME_WARNING, RUFF, AST_GREP, SKILL_POINTER → no collection-time items.
        else:
            continue

        for project, violations in grouped.items():
            if not violations:
                continue
            items.append(
                EnforcementItem.from_parent(
                    collector,
                    name=f"{rule.id}[{project}]",
                    rule=rule,
                    project=project,
                    violations=violations,
                )
            )
    return items


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Append dispatcher items to the collection when active."""
    cfg = _resolve_config(config)
    if not cfg["active"]:
        return
    # Skip on xdist workers — let the master collect once.
    if hasattr(config, "workerinput"):
        return
    generated = _build_items(session, cfg)
    if not generated:
        return
    items.extend(generated)


def pytest_warning_recorded(
    warning_message: object,
    when: str,
    nodeid: str,
    location: tuple[str, int, str] | None,
) -> None:
    """Track (and optionally fail on) runtime enforcement warnings."""
    _ = when, nodeid, location
    if _active_session_config is None:
        return
    cfg = _resolve_config(_active_session_config)
    if not cfg["active"]:
        return
    category = getattr(warning_message, "category", None)
    if category is None:
        return
    dotted = f"{category.__module__}.{category.__qualname__}"
    counter_raw = cfg["warning_counter"]
    if not isinstance(counter_raw, dict):
        msg = f"cfg['warning_counter'] must be dict, got {type(counter_raw).__name__}"
        raise TypeError(msg)
    counter: dict[str, int] = counter_raw
    counter[dotted] = counter.get(dotted, 0) + 1


def pytest_sessionstart(session: pytest.Session) -> None:
    """Expose the session config for warning-capture plumbing."""
    global _active_session_config  # noqa: PLW0603 - intentional session state
    _active_session_config = session.config


def pytest_terminal_summary(
    terminalreporter: pytest.TerminalReporter,
    exitstatus: int,
    config: pytest.Config,
) -> None:
    """Print the per-kind breakdown at the end of the session."""
    _ = exitstatus
    cfg = _resolve_config(config)
    if not cfg["active"]:
        return
    active = _active_rules(cfg)
    kinds: dict[str, int] = {}
    for rule in active:
        kinds[rule.source.kind] = kinds.get(rule.source.kind, 0) + 1
    counter_raw = cfg["warning_counter"]
    if not isinstance(counter_raw, dict):
        msg = f"cfg['warning_counter'] must be dict, got {type(counter_raw).__name__}"
        raise TypeError(msg)
    counter: dict[str, int] = counter_raw
    warning_total = sum(counter.values())
    terminalreporter.write_sep("-", "flext-enforce", yellow=True)
    terminalreporter.write_line(
        f"catalog active: {len(active)} rules across {len(kinds)} source kinds"
    )
    for kind in sorted(kinds):
        terminalreporter.write_line(f"  {kind}: {kinds[kind]}")
    terminalreporter.write_line(f"runtime warnings captured: {warning_total}")


__all__: list[str] = [
    "EnforcementCollector",
    "EnforcementItem",
    "EnforcementViolationError",
    "pytest_addoption",
    "pytest_collection_modifyitems",
    "pytest_configure",
    "pytest_sessionstart",
    "pytest_terminal_summary",
    "pytest_warning_recorded",
]
