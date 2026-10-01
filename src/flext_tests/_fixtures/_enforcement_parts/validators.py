"""Enforcement items from the flext-infra rule engine and flext-tests validators."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

from flext_tests import c, m

from .items import FlextTestsEnforcementItem

if TYPE_CHECKING:
    from collections.abc import Callable

    import pytest

    from flext_tests import p, t


class FlextTestsEnforcementValidators:
    """Group engine findings and validator violations into enforcement items."""

    @staticmethod
    def build_infra_rule_items(
        collector: pytest.Collector,
        cfg: m.Tests.EnforcementDispatcherConfig,
        context: m.Tests.EnforcementBuildContext,
    ) -> list[FlextTestsEnforcementItem]:
        """Build one item per engine rule id and collected project with findings."""
        if context.infra_findings is None:
            return []
        grouped: dict[tuple[str, str], list[m.Infra.ModScanFinding]] = {}
        for finding in context.infra_findings.entries:
            if finding.repository not in context.project_names:
                continue
            if cfg.include and finding.rule_id not in cfg.include:
                continue
            if finding.rule_id in cfg.exclude:
                continue
            grouped.setdefault((finding.rule_id, finding.repository), []).append(
                finding
            )
        severity_key = c.Tests.ENFORCEMENT_FINDING_SEVERITY_KEY
        message_key = c.Tests.ENFORCEMENT_FINDING_MESSAGE_KEY
        return [
            FlextTestsEnforcementItem.from_parent(
                collector,
                name=f"{rule_id}[{project}]",
                rule_id=rule_id,
                severity=str(findings[0].payload[severity_key]),
                description=str(findings[0].payload[message_key]),
                project=project,
                violations=tuple(
                    f"{finding.file.as_posix()} | {finding.text.splitlines()[0]}"
                    for finding in findings
                ),
            )
            for (rule_id, project), findings in sorted(grouped.items())
        ]

    @classmethod
    def build_tests_validator_items(
        cls,
        collector: pytest.Collector,
        rule: m.EnforcementRuleSpec,
        source: m.EnforcementTestsValidatorSource,
        context: m.Tests.EnforcementBuildContext,
    ) -> list[FlextTestsEnforcementItem]:
        """Build enforcement items from one flext-tests validator method."""
        if context.repository_root is None:
            return []
        grouped = cls.collect_tests_validator_violations(
            source, context.repository_root, context.validator_targets
        )
        return [
            FlextTestsEnforcementItem.from_parent(
                collector,
                name=f"{rule.id}[{project}]",
                rule_id=rule.id,
                severity=rule.severity,
                description=rule.description,
                project=project,
                violations=tuple(
                    f"{violation.rule_id} | {violation.file_path} | "
                    f"line {violation.line_number} | {violation.description}"
                    for violation in violations
                ),
            )
            for project, violations in grouped.items()
            if violations
        ]

    @classmethod
    def collect_tests_validator_violations(
        cls,
        source: m.EnforcementTestsValidatorSource,
        repository_root: Path,
        targets: t.SequenceOf[Path],
    ) -> t.MappingKV[str, list[m.Tests.Violation]]:
        """Run one flext-tests validator method over every collected target."""
        result: dict[str, list[m.Tests.Violation]] = {}
        # Late import: flext_tests.validator transitively imports this package
        # facet; a missing module or validator method is a defect and raises.
        method: Callable[[Path], p.Result[m.Tests.ScanResult]] = getattr(
            import_module("flext_tests.validator").FlextTestsValidator, source.method
        )
        wanted_ids = frozenset(source.rule_ids)
        for target in targets:
            dispatch_target = cls.validator_dispatch_target(
                method_name=source.method, target=target
            )
            if dispatch_target is None:
                continue
            scan = method(dispatch_target).unwrap()
            for violation in scan.violations:
                if wanted_ids and violation.rule_id not in wanted_ids:
                    continue
                parts = violation.file_path.resolve().relative_to(repository_root).parts
                result.setdefault(parts[0], []).append(violation)
        return result

    @staticmethod
    def validator_dispatch_target(*, method_name: str, target: Path) -> Path | None:
        """Return the concrete path to pass to one validator method."""
        if method_name != "validate_config":
            return target
        pyproject_path = target / c.PYPROJECT_FILENAME if target.is_dir() else target
        return pyproject_path if pyproject_path.name == c.PYPROJECT_FILENAME else None


__all__: list[str] = ["FlextTestsEnforcementValidators"]
