"""Enforcement items from the flext-infra rule engine findings.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import c, m
from flext_tests._fixtures._enforcement_parts.items import FlextTestsEnforcementItem

if TYPE_CHECKING:
    import pytest

    from flext_tests import p


class FlextTestsEnforcementValidators:
    """Group engine findings into enforcement items by rule id and project."""

    @staticmethod
    def build_infra_rule_items(
        collector: pytest.Collector,
        cfg: m.Tests.EnforcementDispatcherConfig,
        context: m.Tests.EnforcementBuildContext,
    ) -> list[FlextTestsEnforcementItem]:
        """Build one item per engine rule id and collected project with findings.

        Returns:
            The resulting ``list[FlextTestsEnforcementItem]``.
        """
        if context.infra_findings is None:
            return []
        grouped: dict[
            tuple[str, str],
            list[p.Tests.EnforcementScanFinding],
        ] = {}
        for finding in context.infra_findings.entries:
            if finding.repository not in context.project_names:
                continue
            if cfg.include and finding.rule_id not in cfg.include:
                continue
            if finding.rule_id in cfg.exclude:
                continue
            grouped.setdefault((finding.rule_id, finding.repository), []).append(
                finding,
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


__all__: list[str] = ["FlextTestsEnforcementValidators"]
