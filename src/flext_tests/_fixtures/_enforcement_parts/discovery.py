"""Project discovery helpers for enforcement dispatch."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path

import pytest

from flext_tests import c, p, t


def _load_infra_report(
    workspace_root: Path,
    *,
    project_names: t.StrSequence,
) -> p.AttributeProbe | None:
    """Return a workspace enforcement report when available."""
    if not project_names:
        return None
    try:
        refactor = import_module("flext_infra.refactor.namespace_enforcer")
    except ImportError:
        return None
    enforcer_cls = getattr(refactor, "FlextInfraNamespaceEnforcer", None)
    if enforcer_cls is None:
        return None
    try:
        enforcer = enforcer_cls(workspace_root=workspace_root)
        report = enforcer.enforce(project_names=project_names)
    except c.EXC_BROAD_RUNTIME:
        return None
    return report


def _item_path(item: pytest.Item) -> Path | None:
    """Return the filesystem path represented by one collected pytest item."""
    path_value = getattr(item, "path", None)
    if isinstance(path_value, Path):
        return path_value.resolve()
    fspath = getattr(item, "fspath", None)
    if fspath is None:
        return None
    return Path(str(fspath)).resolve()


def _project_name_for_path(
    *,
    path: Path,
    workspace_root: Path,
) -> str | None:
    """Return the owning FLEXT project name for one workspace path."""
    try:
        relative_path = path.relative_to(workspace_root)
    except ValueError:
        return None
    if not relative_path.parts:
        return None
    project_name = relative_path.parts[0]
    project_root = workspace_root / project_name
    if not (
        project_name.startswith("flext-")
        and project_root.is_dir()
        and (project_root / "pyproject.toml").is_file()
    ):
        return None
    return project_name


def _project_name_for_item(
    *,
    item: pytest.Item,
    workspace_root: Path,
) -> str | None:
    """Return the owning FLEXT project name for one collected item."""
    item_path = _item_path(item)
    if item_path is None:
        return None
    return _project_name_for_path(path=item_path, workspace_root=workspace_root)


def _collected_project_names(
    *,
    items: t.SequenceOf[pytest.Item],
    workspace_root: Path,
) -> t.StrSequence:
    """Return sorted FLEXT project names represented by collected pytest items."""
    project_names = {
        project_name
        for item in items
        if (
            project_name := _project_name_for_item(
                item=item,
                workspace_root=workspace_root,
            )
        )
        is not None
    }
    return tuple(sorted(project_names))


def _validator_target_for_item(
    *,
    item: pytest.Item,
    workspace_root: Path,
) -> Path | None:
    """Return the validation target represented by one collected item."""
    item_path = _item_path(item)
    if item_path is None:
        return None
    project_name = _project_name_for_path(path=item_path, workspace_root=workspace_root)
    if project_name is not None:
        return workspace_root / project_name
    return item_path


def _collected_validator_targets(
    *,
    items: t.SequenceOf[pytest.Item],
    workspace_root: Path,
) -> t.SequenceOf[Path]:
    """Return sorted validation targets represented by collected pytest items."""
    targets = {
        target
        for item in items
        if (
            target := _validator_target_for_item(
                item=item,
                workspace_root=workspace_root,
            )
        )
        is not None
    }
    return tuple(sorted(targets))


__all__: list[str] = [
    "_collected_project_names",
    "_collected_validator_targets",
    "_load_infra_report",
    "_project_name_for_path",
]
