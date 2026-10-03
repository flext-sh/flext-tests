"""Behavioral unit tests for the ``flext_tests.domains`` (``FlextTestsDomains``) facade.

These tests exercise only the public contract of ``FlextTestsDomains``: the values it
returns, the ``r[T]`` outcomes it builds, the fixtures it discovers/loads on
disk, and the exceptions it raises on missing inputs. No private attribute,
internal collaborator, or implementation detail is touched.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import FlextTestsDomains, t, tm


class TestsFlextTestsDomains:
    """Public-contract tests for the ``FlextTestsDomains`` test-domain facade."""

    # --- fixtures ---------------------------------------------------------

    @staticmethod
    @pytest.fixture
    def fixtures_root(tmp_path: Path) -> Path:
        """Build a two-server fixture tree exercised by the discovery API.

        Layout::

            <root>/oid/oid_schema_fixtures.ldif
            <root>/oid/oid_entries_fixtures.ldif
            <root>/oud/oud_schema_fixtures.ldif

        Returns:
            The resulting ``Path``.
        """
        payloads: t.MappingKV[tuple[str, str], str] = {
            ("oid", "schema"): "dn: cn=schema,dc=oid\n",
            ("oid", "entries"): "dn: cn=alice,dc=oid\n",
            ("oud", "schema"): "dn: cn=schema,dc=oud\n",
        }
        for (group, kind), text in payloads.items():
            group_dir = tmp_path / group
            group_dir.mkdir(parents=True, exist_ok=True)
            (group_dir / f"{group}_{kind}_fixtures.ldif").write_text(
                text,
                encoding="utf-8",
            )
        return tmp_path

    # --- case-table data helpers -----------------------------------------

    @staticmethod
    def test_valid_email_cases_pairs_input_with_expected_validity() -> None:
        """Each email case is a ``(value, is_valid)`` pair with stable verdicts."""
        cases = dict(FlextTestsDomains.valid_email_cases())

        tm.that(cases["test@example.com"], eq=True)
        tm.that(cases["user.name@domain.co.uk"], eq=True)
        tm.that(cases["invalid-email"], eq=False)
        tm.that(cases[""], eq=False)

    @staticmethod
    def test_valid_email_cases_verdicts_are_deterministic() -> None:
        """Repeated calls return equal case tables (pure data helper)."""
        tm.that(
            list(FlextTestsDomains.valid_email_cases()),
            eq=list(FlextTestsDomains.valid_email_cases()),
        )

    @staticmethod
    def test_default_handler_case_specs_expose_expected_handler_ids() -> None:
        """The shared handler specs cover the documented success/fail ids."""
        specs = FlextTestsDomains.default_handler_case_specs()

        handler_ids = [spec.handler_id for spec in specs]
        tm.that(
            handler_ids,
            eq=[
                "success_command",
                "success_query",
                "success_event",
                "fail_command",
                "fail_query",
            ],
        )

    @staticmethod
    @pytest.mark.parametrize(
        ("handler_id", "should_fail"),
        [
            ("success_command", False),
            ("success_query", False),
            ("success_event", False),
            ("fail_command", True),
            ("fail_query", True),
        ],
    )
    def test_default_handler_case_specs_flag_failures_consistently(
        handler_id: str,
        *,
        should_fail: bool,
    ) -> None:
        """Only the ``fail_*`` handler specs carry the ``should_fail`` marker."""
        spec = next(
            entry
            for entry in FlextTestsDomains.default_handler_case_specs()
            if entry.handler_id == handler_id
        )

        tm.that(spec.should_fail, eq=should_fail)

    # --- fixture path + loading ------------------------------------------

    @staticmethod
    def test_fixture_filename_follows_group_kind_extension_convention() -> None:
        """The filename contract is ``<group>_<kind>_fixtures<ext>``."""
        tm.that(
            FlextTestsDomains.fixture_filename("oid", "schema"),
            eq="oid_schema_fixtures.ldif",
        )
        tm.that(
            FlextTestsDomains.fixture_filename("oud", "acl", file_extension=".txt"),
            eq="oud_acl_fixtures.txt",
        )

    @staticmethod
    def test_load_fixture_returns_file_contents(fixtures_root: Path) -> None:
        """Loading an existing fixture returns its exact text."""
        loaded = FlextTestsDomains.load_fixture(
            "oid",
            "schema",
            fixtures_root=fixtures_root,
        )

        tm.that(loaded, eq="dn: cn=schema,dc=oid\n")

    @staticmethod
    def test_fixture_path_points_at_existing_file(fixtures_root: Path) -> None:
        """``fixture_path`` resolves to an existing file inside the group dir."""
        resolved = FlextTestsDomains.fixture_path(
            "oid",
            "schema",
            fixtures_root=fixtures_root,
        )

        tm.that(resolved.exists(), eq=True)
        tm.that(resolved.parent.name, eq="oid")
        tm.that(resolved.name, eq="oid_schema_fixtures.ldif")

    @staticmethod
    def test_fixture_path_raises_file_not_found_when_absent(
        fixtures_root: Path,
    ) -> None:
        """A missing fixture is a hard error, not a silent empty result."""
        with pytest.raises(FileNotFoundError, match="Fixture file not found"):
            FlextTestsDomains.fixture_path(
                "oid",
                "missing",
                fixtures_root=fixtures_root,
            )

    @staticmethod
    def test_load_fixture_raises_when_fixture_absent(fixtures_root: Path) -> None:
        """Loading an absent fixture surfaces the missing-file failure."""
        with pytest.raises(FileNotFoundError):
            FlextTestsDomains.load_fixture(
                "oid",
                "missing",
                fixtures_root=fixtures_root,
            )

    @staticmethod
    @pytest.mark.parametrize(
        ("group", "kind", "expected"),
        [
            ("oid", "schema", True),
            ("oid", "entries", True),
            ("oud", "schema", True),
            ("oid", "absent", False),
            ("ghost", "schema", False),
        ],
    )
    def test_fixture_exists_reports_presence(
        fixtures_root: Path,
        group: str,
        kind: str,
        *,
        expected: bool,
    ) -> None:
        """``fixture_exists`` mirrors on-disk presence without raising."""
        tm.that(
            FlextTestsDomains.fixture_exists(group, kind, fixtures_root=fixtures_root),
            eq=expected,
        )

    # --- fixture discovery ------------------------------------------------

    @staticmethod
    def test_available_fixture_servers_lists_group_dirs_sorted(
        fixtures_root: Path,
    ) -> None:
        """Discovery returns each server directory name, sorted."""
        tm.that(
            FlextTestsDomains.available_fixture_servers(fixtures_root=fixtures_root),
            eq=("oid", "oud"),
        )

    @staticmethod
    def test_available_fixture_servers_empty_for_missing_root(
        tmp_path: Path,
    ) -> None:
        """A non-existent root yields an empty tuple, never an error."""
        tm.that(
            FlextTestsDomains.available_fixture_servers(
                fixtures_root=tmp_path / "nope",
            ),
            eq=(),
        )

    @staticmethod
    def test_available_fixture_types_lists_kinds_for_group(
        fixtures_root: Path,
    ) -> None:
        """Discovery extracts the ``kind`` segment of each fixture file."""
        tm.that(
            FlextTestsDomains.available_fixture_types(
                "oid",
                fixtures_root=fixtures_root,
            ),
            eq=("entries", "schema"),
        )

    @staticmethod
    def test_available_fixture_types_empty_for_unknown_group(
        fixtures_root: Path,
    ) -> None:
        """An unknown group has no fixture types."""
        tm.that(
            FlextTestsDomains.available_fixture_types(
                "ghost",
                fixtures_root=fixtures_root,
            ),
            eq=(),
        )

    @staticmethod
    def test_load_server_fixtures_maps_every_kind_to_its_contents(
        fixtures_root: Path,
    ) -> None:
        """All of a group's fixtures load into a kind -> text mapping."""
        loaded = FlextTestsDomains.load_server_fixtures(
            "oid",
            fixtures_root=fixtures_root,
        )

        tm.that(
            loaded,
            eq={"entries": "dn: cn=alice,dc=oid\n", "schema": "dn: cn=schema,dc=oid\n"},
        )

    # --- bound loader (public ``bind`` API) -------------------------------

    @staticmethod
    def test_bind_loads_same_content_as_unbound_facade(
        fixtures_root: Path,
    ) -> None:
        """A bound loader is equivalent to passing the root each call."""
        bound = FlextTestsDomains.bind(fixtures_root)

        tm.that(
            bound.load_fixture("oid", "schema"),
            eq=FlextTestsDomains.load_fixture(
                "oid",
                "schema",
                fixtures_root=fixtures_root,
            ),
        )
        tm.that(bound.available_fixture_servers(), eq=("oid", "oud"))
        tm.that(bound.fixture_exists("oud", "schema"), eq=True)

    @staticmethod
    def test_bind_load_all_aggregates_every_server_and_kind(
        fixtures_root: Path,
    ) -> None:
        """``load_all`` returns the full server -> kind -> text structure."""
        bound = FlextTestsDomains.bind(fixtures_root)

        tm.that(
            bound.load_all(),
            eq={
                "oid": {
                    "entries": "dn: cn=alice,dc=oid\n",
                    "schema": "dn: cn=schema,dc=oid\n",
                },
                "oud": {"schema": "dn: cn=schema,dc=oud\n"},
            },
        )

    @staticmethod
    def test_bind_load_fixture_kind_collects_one_kind_across_servers(
        fixtures_root: Path,
    ) -> None:
        """``load_fixture_kind`` gathers a single kind from every server."""
        bound = FlextTestsDomains.bind(fixtures_root)

        tm.that(
            bound.load_fixture_kind("schema"),
            eq={"oid": "dn: cn=schema,dc=oid\n", "oud": "dn: cn=schema,dc=oud\n"},
        )

    @staticmethod
    def test_bind_pytest_params_for_group_pairs_kind_and_content(
        fixtures_root: Path,
    ) -> None:
        """Per-group params expose ``(kind, content)`` tuples."""
        bound = FlextTestsDomains.bind(fixtures_root)

        tm.that(
            bound.pytest_params_for_group("oid"),
            eq=[
                ("entries", "dn: cn=alice,dc=oid\n"),
                ("schema", "dn: cn=schema,dc=oid\n"),
            ],
        )

    @staticmethod
    def test_bind_all_pytest_params_yields_group_kind_content_triples(
        fixtures_root: Path,
    ) -> None:
        """The flattened params expose ``(group, kind, content)`` triples."""
        bound = FlextTestsDomains.bind(fixtures_root)

        tm.that(
            bound.all_pytest_params(),
            eq=[
                ("oid", "entries", "dn: cn=alice,dc=oid\n"),
                ("oid", "schema", "dn: cn=schema,dc=oid\n"),
                ("oud", "schema", "dn: cn=schema,dc=oud\n"),
            ],
        )

    @staticmethod
    def test_bind_honors_custom_file_extension(tmp_path: Path) -> None:
        """A bound loader created with a custom extension only sees those files."""
        group_dir = tmp_path / "oid"
        group_dir.mkdir(parents=True, exist_ok=True)
        (group_dir / "oid_schema_fixtures.json").write_text("{}", encoding="utf-8")

        bound = FlextTestsDomains.bind(tmp_path, file_extension=".json")

        tm.that(bound.available_fixture_types("oid"), eq=("schema",))
        tm.that(bound.load_fixture("oid", "schema"), eq="{}")
