"""Enforcement item construction for the pytest plugin.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import u
from flext_tests import m
from flext_tests._fixtures._enforcement_parts._collector import (
    FlextTestsEnforcementCollector,
)
from flext_tests._fixtures._enforcement_parts.validators import (
    FlextTestsEnforcementValidators,
)

if TYPE_CHECKING:
    import pytest

    from flext_tests import t


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
        project_names = u.Tests.collected_project_names(
            items=collected_items,
            repository_root=repository_root,
        )
        # Catalog rows naming engine rules, plus included ids the catalog does
        # not own (engine rule ids), must all be declared by the engine.
        required_rule_ids = frozenset({
            *(
                rule_id
                for rule in rules
                if isinstance(rule.source, m.EnforcementInfraRuleSource)
                for rule_id in rule.source.rule_ids
            ),
            *(cfg.include - {rule.id for rule in rules}),
        })
        engine_selected = not cfg.include or bool(required_rule_ids)
        context = m.Tests.EnforcementBuildContext(
            infra_findings=u.Tests.infra_rule_findings(
                repository_root,
                required_rule_ids=required_rule_ids,
            ).unwrap()
            if project_names and engine_selected
            else None,
            project_names=project_names,
        )
        collector = FlextTestsEnforcementCollector.from_parent(
            parent=session,
            name="flext-enforcement",
        )
        return [
            *FlextTestsEnforcementValidators.build_infra_rule_items(
                collector,
                cfg,
                context,
            ),
        ]


__all__: list[str] = ["FlextTestsEnforcementBuilder"]
