"""Rule dispatch helpers for enforcement plugin validators."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from importlib import import_module
from pathlib import Path

from flext_tests import c, m, p, t


def _iter_infra_violations(
    report: p.AttributeProbe,
    field: str,
    *,
    match_missing: bool,
) -> Iterable[tuple[str, p.AttributeProbe]]:
    """Yield ``(project_name, violation)`` from a workspace report."""
    projects = getattr(report, "projects", ())
    for project in projects:
        project_name = getattr(project, "project", "") or getattr(
            project, "project_name", ""
        )
        entries = getattr(project, field, ())
        if match_missing:
            entries = tuple(
                entry for entry in entries if not getattr(entry, "exists", True)
            )
        for entry in entries:
            yield str(project_name), entry


def _dispatch_infra_detector(
    rule: m.EnforcementRuleSpec,
    report: p.AttributeProbe,
) -> dict[str, list[p.AttributeProbe]]:
    source = rule.source
    field = getattr(source, "violation_field", "")
    match_missing = bool(getattr(source, "match_missing", False))
    grouped: dict[str, list[p.AttributeProbe]] = {}
    for project, entry in _iter_infra_violations(
        report, field, match_missing=match_missing
    ):
        grouped.setdefault(project, []).append(entry)
    return grouped


def _dispatch_tests_validator(
    rule: m.EnforcementRuleSpec,
    workspace_root: Path,
    targets: t.SequenceOf[Path],
) -> dict[str, list[p.AttributeProbe]]:
    result: dict[str, list[p.AttributeProbe]] = {}
    try:
        validator_mod = import_module("flext_tests.validator")
    except ImportError:
        return result
    tv = getattr(validator_mod, "FlextTestsValidator", None)
    if tv is None:
        return result
    method_name = getattr(rule.source, "method", "")
    if not method_name or method_name.startswith("_"):
        return result
    method = getattr(tv, method_name, None)
    if method is None or not callable(method):
        return result
    wanted_ids = frozenset(getattr(rule.source, "rule_ids", ()))
    for target in targets:
        dispatch_target = _validator_dispatch_target(
            method_name=method_name,
            target=target,
        )
        if dispatch_target is None:
            continue
        _merge_tests_validator_result(
            method=method,
            result=result,
            rule_ids=wanted_ids,
            target=dispatch_target,
            workspace_root=workspace_root,
        )
    return result


def _validator_dispatch_target(
    *,
    method_name: str,
    target: Path,
) -> Path | None:
    """Return the concrete path to pass to one validator method."""
    if method_name != "validate_config":
        return target
    pyproject_path = target / "pyproject.toml" if target.is_dir() else target
    return pyproject_path if pyproject_path.name == "pyproject.toml" else None


def _merge_tests_validator_result(
    *,
    method: Callable[[Path], p.AttributeProbe],
    result: dict[str, list[p.AttributeProbe]],
    rule_ids: frozenset[str],
    target: Path,
    workspace_root: Path,
) -> None:
    """Execute one validator and merge matching violations into ``result``."""
    try:
        call_result = method(target)
    except c.EXC_BROAD_RUNTIME:
        return
    if getattr(call_result, "failure", False):
        return
    scan = getattr(call_result, "value", None)
    if scan is None:
        return
    for violation in getattr(scan, "violations", ()):
        if rule_ids and getattr(violation, "rule_id", "") not in rule_ids:
            continue
        project = _violation_project(violation=violation, workspace_root=workspace_root)
        result.setdefault(project, []).append(violation)


def _violation_project(
    *,
    violation: p.AttributeProbe,
    workspace_root: Path,
) -> str:
    """Return the owning workspace segment for one validator violation."""
    file_path = getattr(violation, "file_path", None)
    if file_path is None:
        return "workspace"
    try:
        rel = Path(file_path).resolve().relative_to(workspace_root)
    except ValueError:
        return "workspace"
    return rel.parts[0] if rel.parts else "workspace"


__all__: list[str] = [
    "_dispatch_infra_detector",
    "_dispatch_tests_validator",
]
