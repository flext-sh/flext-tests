"""Rule dispatch helpers for enforcement plugin validators."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

from flext_tests import m, p, t

from .items import FlextTestsEnforcementItem

if TYPE_CHECKING:
    from collections.abc import Callable

    import pytest


class FlextTestsEnforcementValidators:
    """Group detector and flext-tests validator violations into items."""

    @staticmethod
    def dispatch_infra_detector(
        rule: m.EnforcementRuleSpec, report: p.AttributeProbe
    ) -> t.MappingKV[str, list[p.AttributeProbe]]:
        """Group namespace-detector violations by owning project."""
        field = getattr(rule.source, "violation_field", "")
        match_missing = bool(getattr(rule.source, "match_missing", False))
        grouped: t.MutableMappingKV[str, list[p.AttributeProbe]] = {}
        for project in getattr(report, "projects", ()):
            project_name = getattr(project, "project", "") or getattr(
                project, "project_name", ""
            )
            for entry in getattr(project, field, ()):
                if match_missing and getattr(entry, "exists", True):
                    continue
                grouped.setdefault(str(project_name), []).append(entry)
        return grouped

    @classmethod
    def build_tests_validator_items(
        cls,
        collector: pytest.Collector,
        rule: m.EnforcementRuleSpec,
        context: m.Tests.EnforcementBuildContext,
    ) -> list[FlextTestsEnforcementItem]:
        """Build enforcement items from flext-tests validator methods."""
        repository_root = context.repository_root
        if repository_root is None:
            return []
        grouped = cls.collect_tests_validator_violations(
            rule, repository_root, context.validator_targets
        )
        return [
            FlextTestsEnforcementItem.from_parent(
                collector,
                name=f"{rule.id}[{project}]",
                rule=rule,
                project=project,
                violations=violations,
            )
            for project, violations in grouped.items()
            if violations
        ]

    @classmethod
    def collect_tests_validator_violations(
        cls,
        rule: m.EnforcementRuleSpec,
        repository_root: Path,
        targets: t.SequenceOf[Path],
    ) -> t.MappingKV[str, list[p.AttributeProbe]]:
        """Run one flext-tests validator method over every collected target."""
        result: t.MutableMappingKV[str, list[p.AttributeProbe]] = {}
        method_name = getattr(rule.source, "method", "")
        if not method_name or method_name.startswith("_"):
            return result
        # Late import: flext_tests.validator transitively imports this package
        # facet; a missing module or validator symbol is a defect and raises.
        method = getattr(
            import_module("flext_tests.validator").FlextTestsValidator, method_name
        )
        wanted_ids = frozenset(getattr(rule.source, "rule_ids", ()))
        for target in targets:
            dispatch_target = cls.validator_dispatch_target(
                method_name=method_name, target=target
            )
            if dispatch_target is not None:
                cls.merge_tests_validator_result(
                    method=method,
                    result=result,
                    rule_ids=wanted_ids,
                    target=dispatch_target,
                    repository_root=repository_root,
                )
        return result

    @staticmethod
    def validator_dispatch_target(*, method_name: str, target: Path) -> Path | None:
        """Return the concrete path to pass to one validator method."""
        if method_name != "validate_config":
            return target
        pyproject_path = target / "pyproject.toml" if target.is_dir() else target
        return pyproject_path if pyproject_path.name == "pyproject.toml" else None

    @staticmethod
    def merge_tests_validator_result(
        *,
        method: Callable[[Path], p.AttributeProbe],
        result: t.MutableMappingKV[str, list[p.AttributeProbe]],
        rule_ids: frozenset[str],
        target: Path,
        repository_root: Path,
    ) -> None:
        """Execute one validator and merge matching violations into ``result``."""
        call_result = method(target)
        if getattr(call_result, "failure", False):
            # A validator that cannot scan its target is a red gate, never an
            # empty scan: skipping it would silently disable the rule.
            msg = f"validator failed on {target}: {getattr(call_result, 'error', '')}"
            raise RuntimeError(msg)
        scan = getattr(call_result, "value", None)
        for violation in getattr(scan, "violations", ()):
            if rule_ids and getattr(violation, "rule_id", "") not in rule_ids:
                continue
            file_path = getattr(violation, "file_path", None)
            parts = (
                Path(file_path).resolve().relative_to(repository_root).parts
                if file_path is not None
                else ()
            )
            result.setdefault(parts[0] if parts else "workspace", []).append(
                violation
            )


__all__: list[str] = ["FlextTestsEnforcementValidators"]
