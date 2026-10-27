"""Enforcement discovery utilities mixin for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest
from flext_core import u
from flext_infra import m as infra_m, u as infra_u
from flext_infra.codemod import FlextInfraModGateEngine

from flext_tests import c, m, p, r, t


class FlextTestsEnforcementUtilitiesMixin:
    """Catalog filtering, engine findings and collected-project discovery."""

    @staticmethod
    def active_rules(
        cfg: m.Tests.EnforcementDispatcherConfig,
    ) -> tuple[m.EnforcementRuleSpec, ...]:
        """Return catalog rules after applying the include/exclude filters."""
        return tuple(
            rule
            for rule in u.build_canonical_catalog().rules
            if (not cfg.include or rule.id in cfg.include)
            and rule.id not in cfg.exclude
        )

    @staticmethod
    def infra_rule_findings(
        repository_root: Path,
        *,
        project_names: frozenset[str],
        required_rule_ids: frozenset[str],
    ) -> p.Result[infra_m.Infra.ModScanReport]:
        """Scan each collected member with its own native snapshot and rule plan.

        Every id in ``required_rule_ids`` must be declared by the engine's rule
        plan for each member; a missing rule is a failure, never an empty scan.

        Returns:
            The combined native findings, or the first member planning/scan failure.

        """
        if not project_names:
            return r[infra_m.Infra.ModScanReport].fail(
                "enforcement requires at least one collected project to scan",
            )
        reports: list[infra_m.Infra.ModScanReport] = []
        for project_name in sorted(project_names):
            project_root = repository_root / project_name
            with infra_u.Infra.codemod_workspace_snapshot(project_root) as snapshot:
                planned = infra_u.Infra.codemod_rule_plan(snapshot)
            if planned.failure:
                return r[infra_m.Infra.ModScanReport].from_failure(planned)
            missing = sorted(
                required_rule_ids - {rule.id for rule in planned.value.rules},
            )
            if missing:
                return r[infra_m.Infra.ModScanReport].fail(
                    "enforcement names flext-infra rules that config/rules does not "
                    f"declare for {project_name}: {', '.join(missing)}",
                )
            scanned = FlextInfraModGateEngine.scan(
                project_root,
                fix=False,
                selection=planned.value,
            )
            if scanned.failure:
                return r[infra_m.Infra.ModScanReport].from_failure(scanned)
            reports.append(scanned.value)
        return r[infra_m.Infra.ModScanReport].ok(
            FlextInfraModGateEngine.recounted(
                tuple(entry for report in reports for entry in report.entries),
                native_artifacts=tuple(
                    {
                        artifact.path: artifact
                        for report in reports
                        for artifact in report.native_artifacts
                    }.values()
                ),
            ),
        )

    @staticmethod
    def project_name_for_path(*, path: Path, repository_root: Path) -> str | None:
        """Return the owning FLEXT project name for one workspace path."""
        if not path.is_relative_to(repository_root):
            return None
        parts = path.relative_to(repository_root).parts
        if not parts:
            return None
        project_root = repository_root / parts[0]
        if (
            parts[0].startswith(c.Tests.ENFORCEMENT_PROJECT_PREFIX)
            and project_root.is_dir()
            and (project_root / c.PYPROJECT_FILENAME).is_file()
        ):
            return parts[0]
        return None

    @classmethod
    def collected_project_names(
        cls,
        *,
        items: t.SequenceOf[pytest.Item],
        repository_root: Path,
    ) -> frozenset[str]:
        """Return the FLEXT project names represented by collected items."""
        return frozenset(
            name
            for item in items
            if (
                name := cls.project_name_for_path(
                    path=item.path.resolve(),
                    repository_root=repository_root,
                )
            )
            is not None
        )


__all__: list[str] = ["FlextTestsEnforcementUtilitiesMixin"]
