"""Unit tests for the pytest enforcement dispatcher.

Exercises the module-level helpers that don't require a live pytest session:
workspace discovery, CSV parsing, and rule filtering against the catalog.
End-to-end dispatch tests belong in a future ``test_enforcement_plugin.py``
using ``pytester`` fixtures.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests._fixtures import enforcement as dispatcher


class TestWorkspaceDiscovery:
    """``_discover_workspace_root`` walks up until the triple marker matches."""

    def test_detects_workspace_from_nested_path(self, tmp_path: Path) -> None:
        workspace = tmp_path / "ws"
        workspace.mkdir()
        (workspace / "AGENTS.md").write_text("# stub")
        (workspace / "flext-core").mkdir()
        (workspace / "flext-tests").mkdir()

        nested = workspace / "flext-core" / "src" / "pkg"
        nested.mkdir(parents=True)

        found = dispatcher._discover_workspace_root(nested)
        assert found == workspace

    def test_returns_none_outside_workspace(self, tmp_path: Path) -> None:
        sub = tmp_path / "unrelated" / "nested"
        sub.mkdir(parents=True)
        assert dispatcher._discover_workspace_root(sub) is None

    def test_missing_one_marker_fails(self, tmp_path: Path) -> None:
        fake = tmp_path / "fake"
        fake.mkdir()
        (fake / "AGENTS.md").write_text("# stub")
        (fake / "flext-core").mkdir()
        # no flext-tests/ directory
        assert dispatcher._discover_workspace_root(fake) is None


class TestCsvSplit:
    """``_split_csv`` normalizes user CLI input."""

    def test_empty_string_returns_empty_set(self) -> None:
        assert dispatcher._split_csv("") == frozenset()

    def test_none_returns_empty_set(self) -> None:
        assert dispatcher._split_csv(None) == frozenset()

    def test_splits_and_strips(self) -> None:
        got = dispatcher._split_csv("ENFORCE-001, ENFORCE-002 ,,ENFORCE-003")
        assert got == frozenset({"ENFORCE-001", "ENFORCE-002", "ENFORCE-003"})


class TestActiveRules:
    """``_active_rules`` respects enabled/include/exclude filters."""

    def _cfg(
        self,
        *,
        include: frozenset[str] = frozenset(),
        exclude: frozenset[str] = frozenset(),
    ) -> dict[str, object]:
        return {
            "active": True,
            "strict": False,
            "include": include,
            "exclude": exclude,
            "workspace_root": None,
            "warning_counter": {},
        }

    def test_include_narrows_to_listed_ids(self) -> None:
        active = dispatcher._active_rules(self._cfg(include=frozenset({"ENFORCE-001"})))
        assert {r.id for r in active} == {"ENFORCE-001"}

    def test_exclude_drops_listed_ids(self) -> None:
        active = dispatcher._active_rules(self._cfg(exclude=frozenset({"ENFORCE-001"})))
        assert "ENFORCE-001" not in {r.id for r in active}

    def test_disabled_rules_always_skipped(self) -> None:
        # ENFORCE-034..038 are skill-pointer rules with enabled=False by default.
        active = dispatcher._active_rules(self._cfg())
        assert "ENFORCE-034" not in {r.id for r in active}
        assert "ENFORCE-038" not in {r.id for r in active}


class TestAutoActivation:
    """Auto-activation requires the pytest rootdir to BE the workspace root.

    Running pytest inside a sub-project must be a no-op even though
    ``_discover_workspace_root`` can walk up to find the workspace —
    otherwise every sub-project test run would trigger the Rope-based
    ``FlextInfraNamespaceEnforcer.enforce()`` scan.
    """

    @staticmethod
    def _make_workspace(tmp_path: Path) -> Path:
        workspace = tmp_path / "ws"
        workspace.mkdir()
        (workspace / "AGENTS.md").write_text("# stub")
        (workspace / "flext-core").mkdir()
        (workspace / "flext-tests").mkdir()
        return workspace

    def test_nested_rootpath_is_not_workspace(self, tmp_path: Path) -> None:
        workspace = self._make_workspace(tmp_path)
        sub = workspace / "flext-core"
        discovered = dispatcher._discover_workspace_root(sub)
        assert discovered == workspace
        # Auto-activation guard: sub-project rootpath must not match.
        assert discovered != sub

    def test_exact_rootpath_is_workspace(self, tmp_path: Path) -> None:
        workspace = self._make_workspace(tmp_path)
        discovered = dispatcher._discover_workspace_root(workspace)
        assert discovered == workspace


class TestPublicHookSurface:
    """The module exposes the pytest plugin protocol expected by pytest11."""

    @pytest.mark.parametrize(
        "hook_name",
        [
            "pytest_addoption",
            "pytest_configure",
            "pytest_collection_modifyitems",
            "pytest_sessionstart",
            "pytest_terminal_summary",
            "pytest_warning_recorded",
        ],
    )
    def test_hook_present(self, hook_name: str) -> None:
        assert callable(getattr(dispatcher, hook_name, None)), (
            f"missing pytest hook: {hook_name}"
        )

    @pytest.mark.parametrize(
        "cls_name",
        ["EnforcementCollector", "EnforcementItem", "EnforcementViolationError"],
    )
    def test_class_exported(self, cls_name: str) -> None:
        assert hasattr(dispatcher, cls_name)
