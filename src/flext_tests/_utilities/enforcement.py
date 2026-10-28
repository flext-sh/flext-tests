"""Enforcement discovery utilities mixin for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar

import pytest
from flext_infra import m as infra_m, u as infra_u
from flext_infra.codemod import FlextInfraModGateEngine

from flext_tests import c, m, p, r


class FlextTestsUtilitiesEnforcement:
    """Catalog filtering, engine findings and collected-project discovery."""

    _plan_cache: ClassVar[dict[str, infra_m.Infra.CodemodRulePlan]] = {}
    _catalog_cache: ClassVar[dict[str, m.Tests.EnforcementCatalog]] = {}

    @classmethod
    def build_canonical_catalog(
        cls,
        repository_root: Path,
    ) -> m.Tests.EnforcementCatalog:
        """Compose the catalog from the declarative flext-infra rule plan.

        The declarative rule catalog in flext-infra owns enforcement law; the
        dispatcher only maps its elected engine rules into catalog entries.

        Returns:
            The composed catalog for the governed root.

        """
        cache_key = str(repository_root.resolve())
        if cache_key in cls._catalog_cache:
            return cls._catalog_cache[cache_key]
        with infra_u.Infra.codemod_workspace_snapshot(repository_root) as snapshot:
            planned = infra_u.Infra.codemod_rule_plan(snapshot)
        plan = planned.unwrap()
        catalog = m.Tests.EnforcementCatalog(
            rules=tuple(
                m.Tests.EnforcementRuleSpec(
                    id=engine_rule.id,
                    description=engine_rule.message,
                    source=m.Tests.EnforcementInfraRuleSource(
                        rule_ids=(engine_rule.id,),
                    ),
                )
                for engine_rule in plan.rules
            ),
        )
        cls._catalog_cache[cache_key] = catalog
        return catalog

    @classmethod
    def active_rules(
        cls,
        cfg: m.Tests.EnforcementDispatcherConfig,
    ) -> tuple[m.Tests.EnforcementRuleSpec, ...]:
        """Return catalog rules after applying the include/exclude filters."""
        if cfg.repository_root is None:
            return ()
        catalog = cls.build_canonical_catalog(cfg.repository_root)
        return tuple(
            rule
            for rule in catalog.rules
            if (not cfg.include or rule.id in cfg.include)
            and rule.id not in cfg.exclude
        )

    @classmethod
    def infra_rule_findings(
        cls,
        repository_root: Path,
        *,
        project_names: frozenset[str] | None = None,
        required_rule_ids: frozenset[str],
    ) -> p.Result[infra_m.Infra.ModScanReport]:
        """Scan each collected member with its own native snapshot and rule plan.

        Every id in ``required_rule_ids`` must be declared by the engine's rule
        plan for each member; a missing rule is a failure, never an empty scan.

        Returns:
            The combined native findings, or the first member planning/scan failure.

        """
        if project_names is None:
            if (repository_root / "pyproject.toml").exists():
                project_names = frozenset({""})
            else:
                return r[infra_m.Infra.ModScanReport].fail(
                    "enforcement requires at least one collected project to scan",
                )
        elif not project_names:
            return r[infra_m.Infra.ModScanReport].fail(
                "enforcement requires at least one collected project to scan",
            )
        reports: list[infra_m.Infra.ModScanReport] = []
        for project_name in sorted(project_names):
            project_root = (
                repository_root / project_name if project_name else repository_root
            )
            cache_key = str(project_root.resolve())
            if cache_key in cls._plan_cache:
                plan = cls._plan_cache[cache_key]
            else:
                with infra_u.Infra.codemod_workspace_snapshot(project_root) as snapshot:
                    planned = infra_u.Infra.codemod_rule_plan(snapshot)
                if planned.failure:
                    return r[infra_m.Infra.ModScanReport].from_failure(planned)
                plan = planned.value
                cls._plan_cache[cache_key] = plan
            missing = sorted(
                required_rule_ids - {rule.id for rule in plan.rules},
            )
            if missing:
                display_name = project_name or project_root.name
                return r[infra_m.Infra.ModScanReport].fail(
                    "enforcement names flext-infra rules that config/rules does not "
                    f"declare for {display_name}: {', '.join(missing)}",
                )
            scanned = FlextInfraModGateEngine.scan(
                project_root,
                fix=False,
                selection=plan,
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
        items: Sequence[pytest.Item],
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


__all__: list[str] = ["FlextTestsUtilitiesEnforcement"]
