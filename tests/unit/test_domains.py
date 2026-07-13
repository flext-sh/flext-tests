"""Behavioral unit tests for the ``flext_tests.domains`` (``td``) facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

These tests exercise only the public contract of ``td``: the values it
returns, the ``r[T]`` outcomes it builds, the fixtures it discovers/loads on
disk, and the exceptions it raises on missing inputs. No private attribute,
internal collaborator, or implementation detail is touched.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import td, tm


class TestsFlextTestsDomains:
    """Public-contract tests for the ``td`` test-domain facade."""

    # --- fixtures ---------------------------------------------------------

    @staticmethod
    @pytest.fixture
    def fixtures_root(tmp_path: Path) -> Path:
        """Build a two-server fixture tree exercised by the discovery API.

        Layout::

            <root>/oid/oid_schema_fixtures.ldif
            <root>/oid/oid_entries_fixtures.ldif
            <root>/oud/oud_schema_fixtures.ldif
        """
        payloads: dict[tuple[str, str], str] = {
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

    # --- result builders --------------------------------------------------

    def test_create_result_ok_yields_success_carrying_value(self) -> None:
        """A generic OK result reports success and unwraps to the input value."""
        payload: dict[str, str] = {"foo": "bar"}

        result = td.create_result_ok(payload)

        assert tm.ok(result) == payload

    def test_create_result_ok_is_chainable_as_result_monad(self) -> None:
        """The OK builder returns a real ``r[T]`` that supports ``.map``."""
        result = td.create_result_ok("payload")

        assert result.map(lambda value: f"[{value}]").unwrap() == "[payload]"

    def test_create_result_failure_carries_error_message_code_and_data(self) -> None:
        """A generic failure exposes message, code and structured data."""
        result = td.create_result_failure(
            "failed",
            error_code="GENERIC_ERROR",
            error_data={"detail": "reason"},
        )

        error_text = tm.fail(
            result,
            has="failed",
            code="GENERIC_ERROR",
            data={"detail": "reason"},
        )
        assert error_text == "failed"

    def test_create_result_failure_defaults_to_test_error_code(self) -> None:
        """Omitting ``error_code`` yields the documented default code."""
        result = td.create_result_failure("boom")

        tm.fail(result, has="boom", code="TEST_ERROR")

    def test_failure_result_does_not_expose_a_value(self) -> None:
        """A failed result is observably not a success."""
        result = td.create_result_failure("nope")

        assert result.failure
        assert not result.success

    # --- case-table data helpers -----------------------------------------

    def test_valid_email_cases_pairs_input_with_expected_validity(self) -> None:
        """Each email case is a ``(value, is_valid)`` pair with stable verdicts."""
        cases = dict(td.valid_email_cases())

        assert cases["test@example.com"] is True
        assert cases["user.name@domain.co.uk"] is True
        assert cases["invalid-email"] is False
        assert cases[""] is False

    def test_valid_email_cases_verdicts_are_deterministic(self) -> None:
        """Repeated calls return equal case tables (pure data helper)."""
        assert list(td.valid_email_cases()) == list(td.valid_email_cases())

    def test_default_handler_case_specs_expose_expected_handler_ids(self) -> None:
        """The shared handler specs cover the documented success/fail ids."""
        specs = td.default_handler_case_specs()

        handler_ids = {spec["handler_id"] for spec in specs}
        assert handler_ids == {
            "success_command",
            "success_query",
            "success_event",
            "fail_command",
            "fail_query",
        }

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
        self,
        handler_id: str,
        should_fail: bool,
    ) -> None:
        """Only the ``fail_*`` handler specs carry the ``should_fail`` marker."""
        spec = next(
            entry
            for entry in td.default_handler_case_specs()
            if entry["handler_id"] == handler_id
        )

        assert bool(spec.get("should_fail", False)) is should_fail

    # --- fixture path + loading ------------------------------------------

    def test_fixture_filename_follows_group_kind_extension_convention(self) -> None:
        """The filename contract is ``<group>_<kind>_fixtures<ext>``."""
        assert td.fixture_filename("oid", "schema") == "oid_schema_fixtures.ldif"
        assert (
            td.fixture_filename("oud", "acl", file_extension=".txt")
            == "oud_acl_fixtures.txt"
        )

    def test_load_fixture_returns_file_contents(self, fixtures_root: Path) -> None:
        """Loading an existing fixture returns its exact text."""
        loaded = td.load_fixture("oid", "schema", fixtures_root=fixtures_root)

        assert loaded == "dn: cn=schema,dc=oid\n"

    def test_fixture_path_points_at_existing_file(
        self,
        fixtures_root: Path,
    ) -> None:
        """``fixture_path`` resolves to an existing file inside the group dir."""
        resolved = td.fixture_path("oid", "schema", fixtures_root=fixtures_root)

        assert resolved.exists()
        assert resolved.parent.name == "oid"
        assert resolved.name == "oid_schema_fixtures.ldif"

    def test_fixture_path_raises_file_not_found_when_absent(
        self,
        fixtures_root: Path,
    ) -> None:
        """A missing fixture is a hard error, not a silent empty result."""
        with pytest.raises(FileNotFoundError, match="Fixture file not found"):
            td.fixture_path("oid", "missing", fixtures_root=fixtures_root)

    def test_load_fixture_raises_when_fixture_absent(
        self,
        fixtures_root: Path,
    ) -> None:
        """Loading an absent fixture surfaces the missing-file failure."""
        with pytest.raises(FileNotFoundError):
            td.load_fixture("oid", "missing", fixtures_root=fixtures_root)

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
        self,
        fixtures_root: Path,
        group: str,
        kind: str,
        expected: bool,
    ) -> None:
        """``fixture_exists`` mirrors on-disk presence without raising."""
        assert td.fixture_exists(group, kind, fixtures_root=fixtures_root) is expected

    # --- fixture discovery ------------------------------------------------

    def test_available_fixture_servers_lists_group_dirs_sorted(
        self,
        fixtures_root: Path,
    ) -> None:
        """Discovery returns each server directory name, sorted."""
        assert td.available_fixture_servers(
            fixtures_root=fixtures_root,
        ) == ("oid", "oud")

    def test_available_fixture_servers_empty_for_missing_root(
        self,
        tmp_path: Path,
    ) -> None:
        """A non-existent root yields an empty tuple, never an error."""
        assert (
            td.available_fixture_servers(
                fixtures_root=tmp_path / "nope",
            )
            == ()
        )

    def test_available_fixture_types_lists_kinds_for_group(
        self,
        fixtures_root: Path,
    ) -> None:
        """Discovery extracts the ``kind`` segment of each fixture file."""
        assert td.available_fixture_types(
            "oid",
            fixtures_root=fixtures_root,
        ) == ("entries", "schema")

    def test_available_fixture_types_empty_for_unknown_group(
        self,
        fixtures_root: Path,
    ) -> None:
        """An unknown group has no fixture types."""
        assert (
            td.available_fixture_types(
                "ghost",
                fixtures_root=fixtures_root,
            )
            == ()
        )

    def test_load_server_fixtures_maps_every_kind_to_its_contents(
        self,
        fixtures_root: Path,
    ) -> None:
        """All of a group's fixtures load into a kind -> text mapping."""
        loaded = td.load_server_fixtures("oid", fixtures_root=fixtures_root)

        assert loaded == {
            "entries": "dn: cn=alice,dc=oid\n",
            "schema": "dn: cn=schema,dc=oid\n",
        }

    # --- bound loader (public ``bind`` API) -------------------------------

    def test_bind_loads_same_content_as_unbound_facade(
        self,
        fixtures_root: Path,
    ) -> None:
        """A bound loader is equivalent to passing the root each call."""
        bound = td.bind(fixtures_root)

        assert bound.load_fixture("oid", "schema") == td.load_fixture(
            "oid",
            "schema",
            fixtures_root=fixtures_root,
        )
        assert bound.available_fixture_servers() == ("oid", "oud")
        assert bound.fixture_exists("oud", "schema") is True

    def test_bind_load_all_aggregates_every_server_and_kind(
        self,
        fixtures_root: Path,
    ) -> None:
        """``load_all`` returns the full server -> kind -> text structure."""
        bound = td.bind(fixtures_root)

        assert bound.load_all() == {
            "oid": {
                "entries": "dn: cn=alice,dc=oid\n",
                "schema": "dn: cn=schema,dc=oid\n",
            },
            "oud": {"schema": "dn: cn=schema,dc=oud\n"},
        }

    def test_bind_load_fixture_kind_collects_one_kind_across_servers(
        self,
        fixtures_root: Path,
    ) -> None:
        """``load_fixture_kind`` gathers a single kind from every server."""
        bound = td.bind(fixtures_root)

        assert bound.load_fixture_kind("schema") == {
            "oid": "dn: cn=schema,dc=oid\n",
            "oud": "dn: cn=schema,dc=oud\n",
        }

    def test_bind_pytest_params_for_group_pairs_kind_and_content(
        self,
        fixtures_root: Path,
    ) -> None:
        """Per-group params expose ``(kind, content)`` tuples."""
        bound = td.bind(fixtures_root)

        assert bound.pytest_params_for_group("oid") == [
            ("entries", "dn: cn=alice,dc=oid\n"),
            ("schema", "dn: cn=schema,dc=oid\n"),
        ]

    def test_bind_all_pytest_params_yields_group_kind_content_triples(
        self,
        fixtures_root: Path,
    ) -> None:
        """The flattened params expose ``(group, kind, content)`` triples."""
        bound = td.bind(fixtures_root)

        assert bound.all_pytest_params() == [
            ("oid", "entries", "dn: cn=alice,dc=oid\n"),
            ("oid", "schema", "dn: cn=schema,dc=oid\n"),
            ("oud", "schema", "dn: cn=schema,dc=oud\n"),
        ]

    def test_bind_honors_custom_file_extension(self, tmp_path: Path) -> None:
        """A bound loader created with a custom extension only sees those files."""
        group_dir = tmp_path / "oid"
        group_dir.mkdir(parents=True, exist_ok=True)
        (group_dir / "oid_schema_fixtures.json").write_text("{}", encoding="utf-8")

        bound = td.bind(tmp_path, file_extension=".json")

        assert bound.available_fixture_types("oid") == ("schema",)
        assert bound.load_fixture("oid", "schema") == "{}"
