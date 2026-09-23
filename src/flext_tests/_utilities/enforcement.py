"""Enforcement discovery utilities mixin for flext-tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_core import r, u as _core_u
from flext_tests import c, m, p, t


class FlextTestsEnforcementUtilitiesMixin:
    """Workspace discovery, option parsing and catalog filtering for enforcement."""

    @staticmethod
    def discover_repository_root(start: Path) -> Path | None:
        """Walk upward from ``start`` to find the FLEXT workspace root."""
        for candidate in (start, *start.parents):
            if all(
                (candidate / marker).exists()
                for marker in c.Tests.ENFORCEMENT_WORKSPACE_MARKERS
            ):
                return candidate
        return None

    @staticmethod
    def split_csv(raw: str | None) -> frozenset[str]:
        """Split a comma-separated option value into a normalized frozen set."""
        if not raw:
            return frozenset()
        return frozenset(part.strip() for part in raw.split(",") if part.strip())

    @staticmethod
    def active_rules(
        cfg: m.Tests.EnforcementDispatcherConfig,
    ) -> tuple[m.EnforcementRuleSpec, ...]:
        """Return enabled catalog rules after applying include/exclude filters."""
        return tuple(
            rule
            for rule in _core_u.build_canonical_catalog().rules
            if rule.enabled
            and (not cfg.include or rule.id in cfg.include)
            and rule.id not in cfg.exclude
        )

    @staticmethod
    def load_infra_report(
        repository_root: Path, *, project_names: t.StrSequence
    ) -> p.Result[p.AttributeProbe]:
        """Return the workspace namespace-enforcement report for the projects."""
        if not project_names:
            return r[p.AttributeProbe].fail("no project names provided")
        # Late import: the rope-backed enforcer is loaded only when a rule
        # needs it; flext-infra is a declared runtime dependency of flext-tests.
        from flext_infra.refactor import FlextInfraNamespaceEnforcer

        return r[p.AttributeProbe].ok(
            FlextInfraNamespaceEnforcer(repository_root=repository_root).enforce(
                project_names=project_names
            )
        )

    @staticmethod
    def item_path(item: pytest.Item) -> Path | None:
        """Return the filesystem path represented by one collected pytest item."""
        path_value = getattr(item, "path", None)
        if isinstance(path_value, Path):
            return path_value.resolve()
        fspath = getattr(item, "fspath", None)
        return None if fspath is None else Path(str(fspath)).resolve()

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
        cls, *, items: t.SequenceOf[pytest.Item], repository_root: Path
    ) -> t.StrSequence:
        """Return sorted FLEXT project names represented by collected items."""
        return tuple(
            sorted({
                name
                for item in items
                if (path := cls.item_path(item)) is not None
                and (
                    name := cls.project_name_for_path(
                        path=path, repository_root=repository_root
                    )
                )
                is not None
            })
        )

    @classmethod
    def collected_validator_targets(
        cls, *, items: t.SequenceOf[pytest.Item], repository_root: Path
    ) -> t.SequenceOf[Path]:
        """Return sorted validation targets represented by collected items."""
        targets: set[Path] = set()
        for item in items:
            path = cls.item_path(item)
            if path is None:
                continue
            name = cls.project_name_for_path(path=path, repository_root=repository_root)
            targets.add(repository_root / name if name is not None else path)
        return tuple(sorted(targets))


__all__: list[str] = ["FlextTestsEnforcementUtilitiesMixin"]
