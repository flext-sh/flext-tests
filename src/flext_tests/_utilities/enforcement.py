"""Enforcement discovery utilities mixin for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest
from flext_infra import FlextInfraModGateEngine, u as _infra_u

from flext_core import r, u as _core_u
from flext_tests import c, m, p, t


class FlextTestsEnforcementUtilitiesMixin:
    """Catalog filtering, engine findings and collected-project discovery."""

    @staticmethod
    def active_rules(
        cfg: m.Tests.EnforcementDispatcherConfig,
    ) -> tuple[m.EnforcementRuleSpec, ...]:
        """Return catalog rules after applying the include/exclude filters."""
        return tuple(
            rule
            for rule in _core_u.build_canonical_catalog().rules
            if (not cfg.include or rule.id in cfg.include)
            and rule.id not in cfg.exclude
        )

    @staticmethod
    def infra_rule_findings(
        repository_root: Path,
        *,
        required_rule_ids: frozenset[str],
    ) -> p.Result[m.Infra.ModScanReport]:
        """Return the flext-infra rule-engine findings for the workspace.

        Every id in ``required_rule_ids`` must be declared by the engine's rule
        plan; a missing rule is a failure, never an empty scan.
        """
        planned = _infra_u.Infra.codemod_rule_plan(repository_root)
        if planned.failure:
            return r[m.Infra.ModScanReport].from_failure(planned)
        missing = sorted(required_rule_ids - {rule.id for rule in planned.value.rules})
        if missing:
            return r[m.Infra.ModScanReport].fail(
                "enforcement names flext-infra rules that config/rules does not "
                f"declare: {', '.join(missing)}",
            )
        return FlextInfraModGateEngine.scan(repository_root, fix=False)

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
