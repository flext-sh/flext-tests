"""Behavioral unit tests for the pytest enforcement dispatcher facade.

Asserts the observable public contract of
``flext_tests.enforcement``: workspace discovery, CSV parsing,
catalog rule filtering, and the collection-item / collector / error trio.

End-to-end pytest *lifecycle* hooks (``pytest_configure``,
``pytest_sessionstart``, ``pytest_terminal_summary``,
``pytest_warning_recorded``, ``pytest_collection_modifyitems``) require a live
pytest session and are exercised via ``pytester`` in the E2E suite, not here.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import c, enforcement as dispatcher, m, p, tm, u


class TestsFlextTestsEnforcementDispatcher:
    """Observable behavior of the enforcement dispatcher facade."""

    # ------------------------------------------------------------------ #
    # Fixtures                                                           #
    # ------------------------------------------------------------------ #

    @pytest.fixture
    def workspace(self, tmp_path: Path) -> Path:
        """Create a directory carrying every FLEXT workspace marker."""
        root = tmp_path / "ws"
        root.mkdir()
        for marker in c.Tests.ENFORCEMENT_WORKSPACE_MARKERS:
            (root / marker).mkdir(parents=True, exist_ok=True)
        return root

    @pytest.fixture
    def rule(self) -> p.EnforcementRuleSpec:
        """First enabled rule from the canonical catalog."""
        return next(r for r in u.build_canonical_catalog().rules if r.enabled)

    @pytest.fixture
    def violation(self, rule: p.EnforcementRuleSpec) -> p.EnforcementViolation:
        """Create one canonical enforcement violation."""
        return m.Violation(
            qualname="flext_core.x.Y",
            layer="core",
            severity=rule.severity,
            message="illegal construct",
            rule_id=rule.id,
            agents_md_anchor="§3.1",
            file_path="src/pkg/mod.py",
            line_number=42,
        )

    @staticmethod
    def _cfg(
        *, include: frozenset[str] = frozenset(), exclude: frozenset[str] = frozenset()
    ) -> p.Tests.EnforcementDispatcherConfig:
        """Create a typed dispatcher configuration."""
        return m.Tests.EnforcementDispatcherConfig(
            active=True, strict=False, include=include, exclude=exclude
        )

    # ------------------------------------------------------------------ #
    # discover_workspace_root                                            #
    # ------------------------------------------------------------------ #

    def test_discovers_root_from_nested_descendant(self, workspace: Path) -> None:
        """Discovery walks from a nested package to the workspace root."""
        nested = workspace / "flext-core" / "src" / "pkg"
        nested.mkdir(parents=True)

        tm.that(dispatcher.discover_workspace_root(nested), eq=workspace)

    def test_returns_workspace_itself_when_start_is_root(self, workspace: Path) -> None:
        """Discovery returns the starting directory when it is the root."""
        tm.that(dispatcher.discover_workspace_root(workspace), eq=workspace)

    def test_returns_none_when_no_marker_present(self, tmp_path: Path) -> None:
        """Discovery returns none outside a marked workspace."""
        stray = tmp_path / "unrelated" / "deep"
        stray.mkdir(parents=True)

        tm.that(dispatcher.discover_workspace_root(stray), none=True)

    def test_returns_none_when_a_single_marker_is_missing(self, tmp_path: Path) -> None:
        """Every canonical workspace marker is required."""
        partial = tmp_path / "partial"
        partial.mkdir()
        # All markers but the last one -> not a workspace.
        for marker in list(c.Tests.ENFORCEMENT_WORKSPACE_MARKERS)[:-1]:
            (partial / marker).mkdir(parents=True, exist_ok=True)

        tm.that(dispatcher.discover_workspace_root(partial), none=True)

    def test_sub_project_root_resolves_to_workspace_not_itself(
        self, workspace: Path
    ) -> None:
        """A member path resolves to its parent workspace."""
        # Auto-activation contract: a sub-project path discovers the workspace
        # above it, and that workspace is distinguishable from the sub-project
        # (so running pytest inside a sub-project stays a no-op).
        sub = workspace / "flext-core"
        discovered = dispatcher.discover_workspace_root(sub)

        tm.that(discovered, eq=workspace)
        tm.that(discovered, ne=sub)

    # ------------------------------------------------------------------ #
    # split_csv                                                          #
    # ------------------------------------------------------------------ #

    @pytest.mark.parametrize("raw", ["", None])
    def test_split_csv_empty_input_yields_empty_set(self, raw: str | None) -> None:
        """Empty CSV inputs yield an empty immutable set."""
        tm.that(dispatcher.split_csv(raw), eq=frozenset())

    def test_split_csv_strips_whitespace_and_drops_blank_fields(self) -> None:
        """CSV parsing normalizes whitespace and blank fields."""
        got = dispatcher.split_csv("ENFORCE-001, ENFORCE-002 ,,ENFORCE-003")

        tm.that(got, eq=frozenset({"ENFORCE-001", "ENFORCE-002", "ENFORCE-003"}))

    def test_split_csv_deduplicates_repeated_ids(self) -> None:
        """CSV parsing deduplicates repeated rule identifiers."""
        tm.that(dispatcher.split_csv("A, A ,A"), eq=frozenset({"A"}))

    # ------------------------------------------------------------------ #
    # active_rules                                                       #
    # ------------------------------------------------------------------ #

    def test_active_rules_returns_only_enabled_rules(self) -> None:
        """The active catalog contains enabled rules only."""
        active = dispatcher.active_rules(self._cfg())

        tm.that(active, empty=False)
        tm.that(all(r.enabled for r in active), eq=True)

    def test_active_rules_excludes_disabled_skill_pointer_rules(self) -> None:
        """Disabled skill-pointer rules never enter the active catalog."""
        # ENFORCE-034..038 ship disabled by default.
        ids = {r.id for r in dispatcher.active_rules(self._cfg())}

        tm.that(ids.isdisjoint({"ENFORCE-034", "ENFORCE-035", "ENFORCE-038"}), eq=True)

    def test_include_narrows_to_the_listed_ids(self) -> None:
        """The include set narrows active rules to named identifiers."""
        active = dispatcher.active_rules(self._cfg(include=frozenset({"ENFORCE-001"})))

        tm.that({r.id for r in active}, eq={"ENFORCE-001"})

    def test_include_of_unknown_id_yields_no_rules(self) -> None:
        """An unknown included identifier produces no active rules."""
        active = dispatcher.active_rules(
            self._cfg(include=frozenset({"ENFORCE-DOES-NOT-EXIST"}))
        )

        tm.that(active, eq=())

    def test_exclude_removes_the_listed_id(self) -> None:
        """The exclude set removes named rule identifiers."""
        ids = {
            r.id
            for r in dispatcher.active_rules(
                self._cfg(exclude=frozenset({"ENFORCE-001"}))
            )
        }

        tm.that(ids, lacks="ENFORCE-001")

    def test_exclude_takes_precedence_over_include(self) -> None:
        """Exclusion wins when the same rule is also included."""
        active = dispatcher.active_rules(
            self._cfg(
                include=frozenset({"ENFORCE-001"}), exclude=frozenset({"ENFORCE-001"})
            )
        )

        tm.that(active, eq=())

    def test_active_rules_is_idempotent(self) -> None:
        """Repeated active-rule selection is deterministic."""
        first = dispatcher.active_rules(self._cfg())
        second = dispatcher.active_rules(self._cfg())

        tm.that([r.id for r in first], eq=[r.id for r in second])

    # ------------------------------------------------------------------ #
    # EnforcementItem / EnforcementCollector / EnforcementViolationError #
    # ------------------------------------------------------------------ #

    def test_runtest_raises_violation_error_when_violations_present(
        self,
        request: pytest.FixtureRequest,
        rule: p.EnforcementRuleSpec,
        violation: p.EnforcementViolation,
    ) -> None:
        """An item with violations raises the public violation error."""
        collector = dispatcher.EnforcementCollector.from_parent(
            request.session, name="flext-enforce"
        )
        item = dispatcher.EnforcementItem.from_parent(
            collector,
            name=f"{rule.id}-flext-core",
            rule=rule,
            project="flext-core",
            violations=[violation],
        )

        with pytest.raises(dispatcher.EnforcementViolationError) as excinfo:
            item.runtest()

        message = str(excinfo.value)
        tm.that(message, has=rule.id)
        tm.that(message, has="flext-core")
        tm.that(message, has=str(violation.line_number))

    def test_runtest_is_a_noop_when_no_violations(
        self, request: pytest.FixtureRequest, rule: p.EnforcementRuleSpec
    ) -> None:
        """An item without violations completes without error."""
        collector = dispatcher.EnforcementCollector.from_parent(
            request.session, name="flext-enforce"
        )
        item = dispatcher.EnforcementItem.from_parent(
            collector,
            name=f"{rule.id}-clean",
            rule=rule,
            project="flext-core",
            violations=[],
        )

        tm.that(item.runtest(), none=True)

    def test_collector_collects_every_added_item(
        self,
        request: pytest.FixtureRequest,
        rule: p.EnforcementRuleSpec,
        violation: p.EnforcementViolation,
    ) -> None:
        """The collector returns every item added through its public API."""
        collector = dispatcher.EnforcementCollector.from_parent(
            request.session, name="flext-enforce"
        )
        items = [
            dispatcher.EnforcementItem.from_parent(
                collector,
                name=f"{rule.id}-{i}",
                rule=rule,
                project=f"proj-{i}",
                violations=[violation],
            )
            for i in range(3)
        ]
        for item in items:
            collector.add(item)

        tm.that(list(collector.collect()), eq=items)

    def test_collector_is_empty_before_any_item_is_added(
        self, request: pytest.FixtureRequest
    ) -> None:
        """A new collector starts empty."""
        collector = dispatcher.EnforcementCollector.from_parent(
            request.session, name="flext-enforce"
        )

        tm.that(list(collector.collect()), eq=[])

    def test_violation_error_is_an_exception(self) -> None:
        """The public violation error derives from Exception."""
        tm.that(issubclass(dispatcher.EnforcementViolationError, Exception), eq=True)
