"""Unit tests for flext_tests.domains module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

from flext_tests import td, tm


class TestsFlextTestsDomains:
    """Test suite for td class."""

    def test_create_result_ok(self) -> None:
        """Test generic success result builder."""
        result = td.create_result_ok({"foo": "bar"})
        tm.that(result.success, eq=True)
        tm.that(result.value, eq={"foo": "bar"})

    def test_create_result_failure(self) -> None:
        """Test generic failure result builder."""
        result = td.create_result_failure(
            "failed",
            error_code="GENERIC_ERROR",
            error_data={"detail": "reason"},
        )
        tm.that(result.success, eq=False)
        tm.that(result.error, eq="failed")
        tm.that(result.error_code, eq="GENERIC_ERROR")
        tm.that(result.error_data, eq={"detail": "reason"})

    def test_generic_fixture_helpers(self, tmp_path: Path) -> None:
        """Test generic fixture helper path & loader behavior."""
        server_dir = tmp_path / "oid"
        server_dir.mkdir(parents=True, exist_ok=True)
        fixture_path = server_dir / "oid_schema_fixtures.ldif"
        fixture_path.write_text("dn: cn=test,dc=example,dc=com\n", encoding="utf-8")

        loaded = td.load_fixture(
            "oid",
            "schema",
            fixtures_root=tmp_path,
        )
        tm.that(loaded, eq="dn: cn=test,dc=example,dc=com\n")
        tm.that(
            td.fixture_exists(
                "oid",
                "schema",
                fixtures_root=tmp_path,
            ),
            eq=True,
        )
        tm.that(
            td.available_fixture_servers(fixtures_root=tmp_path),
            eq=("oid",),
        )
        tm.that(
            td.available_fixture_types(
                "oid",
                fixtures_root=tmp_path,
            ),
            eq=("schema",),
        )
