"""Enforcement item construction for the pytest plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests._fixtures._enforcement_parts.config import active_rules
from flext_tests._fixtures._enforcement_parts.discovery import (
    collected_project_names,
    collected_validator_targets,
    load_infra_report,
)
from flext_tests._fixtures._enforcement_parts.items import (
    EnforcementCollector,
    EnforcementItem,
)
from flext_tests._fixtures._enforcement_parts.validators import (
    dispatch_infra_detector,
    dispatch_tests_validator,
)

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

    from flext_tests import m, p, t


def build_items(
    session: pytest.Session,
    cfg: m.Tests.EnforcementDispatcherConfig,
    *,
    collected_items: t.SequenceOf[pytest.Item],
) -> list[EnforcementItem]:
    """Build synthetic enforcement items for active collection-time rules."""
    workspace_root = cfg.workspace_root
    if workspace_root is None:
        return []
    rules = active_rules(cfg)
    validator_targets = collected_validator_targets(
        items=collected_items,
        workspace_root=workspace_root,
    )
    infra_report: p.AttributeProbe | None = None
    if any(rule.source.kind == "flext_infra_detector" for rule in rules):
        infra_report = load_infra_report(
            workspace_root,
            project_names=collected_project_names(
                items=collected_items,
                workspace_root=workspace_root,
            ),
        ).unwrap_or(None)

    collector = EnforcementCollector.from_parent(
        parent=session,
        name="flext-enforcement",
    )
    items: list[EnforcementItem] = []
    for rule in rules:
        grouped = _group_rule_violations(
            rule=rule,
            infra_report=infra_report,
            validator_targets=validator_targets,
            workspace_root=workspace_root,
        )
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
                ),
            )
    return items


def _group_rule_violations(
    *,
    rule: m.EnforcementRuleSpec,
    infra_report: p.AttributeProbe | None,
    validator_targets: t.SequenceOf[Path],
    workspace_root: Path,
) -> dict[str, list[p.AttributeProbe]]:
    """Dispatch one rule to its collection-time source."""
    if rule.source.kind == "flext_infra_detector":
        if infra_report is None:
            return {}
        return dispatch_infra_detector(rule, infra_report)
    if rule.source.kind == "flext_tests_validator":
        return dispatch_tests_validator(rule, workspace_root, validator_targets)
    return {}


__all__: list[str] = ["build_items"]
