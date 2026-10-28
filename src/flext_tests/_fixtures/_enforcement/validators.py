"""Enforcement items from the flext-infra rule engine findings.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import TYPE_CHECKING

from flext_tests import m, p
from flext_tests._fixtures._enforcement import FlextTestsEnforcementItem

if TYPE_CHECKING:
    import pytest


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

        Raises:
            TypeError: If engine findings lack the scan-report contract.

        """
        report = context.infra_findings
        if report is None:
            return []
        if not isinstance(report, p.Tests.EnforcementScanReport):
            msg = f"engine findings lack the scan-report contract: {type(report)!r}"
            raise TypeError(msg)
        grouped: MutableMapping[
            tuple[str, str],
            list[p.Tests.EnforcementScanFinding],
        ] = {}
        for finding in report.entries:
            if finding.repository not in context.project_names:
                continue
            if cfg.include and finding.rule_id not in cfg.include:
                continue
            if finding.rule_id in cfg.exclude:
                continue
            grouped.setdefault((finding.rule_id, finding.repository), []).append(
                finding,
            )
        return [
            FlextTestsEnforcementItem.from_parent(
                collector,
                name=f"{rule_id}[{project}]",
                violation=m.Tests.EnforcementViolation(
                    rule_id=rule_id,
                    severity=findings[0].severity,
                    description=str(findings[0].message),
                    project=project,
                    violations=tuple(
                        f"{finding.file.as_posix()} | {finding.text.splitlines()[0]}"
                        for finding in findings
                    ),
                ),
            )
            for (rule_id, project), findings in sorted(grouped.items())
        ]


__all__: list[str] = ["FlextTestsEnforcementValidators"]
