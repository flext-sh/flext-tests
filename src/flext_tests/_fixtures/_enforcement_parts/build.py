"""Enforcement item construction for the pytest plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import m
from flext_tests.utilities import u

from ._collector import FlextTestsEnforcementCollector
from .namespace import NamespaceDetectorBuilder
from .validators import FlextTestsEnforcementValidators

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

    from flext_tests import p, t


class FlextTestsEnforcementBuilder:
    """Build synthetic enforcement items for active collection-time rules."""

    @classmethod
    def build_items(
        cls,
        session: pytest.Session,
        cfg: m.Tests.EnforcementDispatcherConfig,
        *,
        collected_items: t.SequenceOf[pytest.Item],
    ) -> list[pytest.Item]:
        """Return one enforcement item per rule and offending project."""
        repository_root = cfg.repository_root
        if repository_root is None:
            return []
        rules = u.Tests.active_rules(cfg)
        collector = FlextTestsEnforcementCollector.from_parent(
            parent=session, name="flext-enforcement"
        )
        context = m.Tests.EnforcementBuildContext(
            infra_report=cls.infra_report_if_needed(
                rules, repository_root, collected_items
            ),
            validator_targets=u.Tests.collected_validator_targets(
                items=collected_items, repository_root=repository_root
            ),
            repository_root=repository_root,
        )
        namespace_builder = NamespaceDetectorBuilder()
        items: list[pytest.Item] = []
        for rule in rules:
            if rule.source.kind == m.EnforcementSourceKind.FLEXT_INFRA_DETECTOR.value:
                items.extend(namespace_builder(session, cfg, rule, context))
            elif rule.source.kind == "flext_tests_validator":
                items.extend(
                    FlextTestsEnforcementValidators.build_tests_validator_items(
                        collector, rule, context
                    )
                )
        return items

    @staticmethod
    def infra_report_if_needed(
        rules: tuple[m.EnforcementRuleSpec, ...],
        repository_root: Path,
        collected_items: t.SequenceOf[pytest.Item],
    ) -> p.AttributeProbe | None:
        """Load the workspace infra report only when a rule needs it."""
        if not any(
            rule.source.kind == m.EnforcementSourceKind.FLEXT_INFRA_DETECTOR.value
            for rule in rules
        ):
            return None
        project_names = u.Tests.collected_project_names(
            items=collected_items, repository_root=repository_root
        )
        if not project_names:
            return None
        # Detector failures must stop collection; replacing them with None
        # would silently disable the active enforcement rule.
        return u.Tests.load_infra_report(
            repository_root, project_names=project_names
        ).unwrap()


__all__: list[str] = ["FlextTestsEnforcementBuilder"]
