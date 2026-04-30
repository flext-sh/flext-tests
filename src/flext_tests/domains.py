"""Test domain objects and fixtures for FLEXT ecosystem tests.

Provides reusable domain objects, test data structures, and fixtures for
generic domain-specific testing scenarios. Includes bases for payloads,
API responses, validation test cases, and domain result helpers.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path

from flext_tests import p, r, t

_NO_BODY: t.Tests.TestobjectSerializable = None


class FlextTestsDomains:
    """Test domain objects and fixtures.

    Provides common test data and domain objects used across FLEXT test suites.
    """

    class BoundFixtures:
        """Bound fixture loader for one fixture root + extension."""

        def __init__(
            self,
            fixtures_root: Path,
            *,
            file_extension: str = ".ldif",
        ) -> None:
            self._fixtures_root: Path = fixtures_root
            self._file_extension: str = file_extension

        def fixture_path(
            self,
            group: str,
            kind: str,
        ) -> Path:
            return FlextTestsDomains.fixture_path(
                group,
                kind,
                fixtures_root=self._fixtures_root,
                file_extension=self._file_extension,
            )

        def load_fixture(
            self,
            group: str,
            kind: str,
        ) -> str:
            return FlextTestsDomains.load_fixture(
                group,
                kind,
                fixtures_root=self._fixtures_root,
                file_extension=self._file_extension,
            )

        def fixture_exists(
            self,
            group: str,
            kind: str,
        ) -> bool:
            return FlextTestsDomains.fixture_exists(
                group,
                kind,
                fixtures_root=self._fixtures_root,
                file_extension=self._file_extension,
            )

        def available_fixture_servers(self) -> tuple[str, ...]:
            return FlextTestsDomains.available_fixture_servers(
                fixtures_root=self._fixtures_root,
            )

        def available_fixture_types(
            self,
            group: str,
        ) -> tuple[str, ...]:
            return FlextTestsDomains.available_fixture_types(
                group,
                fixtures_root=self._fixtures_root,
                file_extension=self._file_extension,
            )

        def load_server_fixtures(
            self,
            group: str,
        ) -> Mapping[str, str]:
            return FlextTestsDomains.load_server_fixtures(
                group,
                fixtures_root=self._fixtures_root,
                file_extension=self._file_extension,
            )

        def load_fixture_kind(self, kind: str) -> Mapping[str, str]:
            return {
                group: self.load_fixture(group, kind)
                for group in self.available_fixture_servers()
                if self.fixture_exists(group, kind)
            }

        def load_all(self) -> Mapping[str, Mapping[str, str]]:
            return {
                group: self.load_server_fixtures(group)
                for group in self.available_fixture_servers()
            }

        def pytest_params_for_group(
            self,
            group: str,
        ) -> Sequence[tuple[str, str]]:
            return [
                (fixture_type, self.load_fixture(group, fixture_type))
                for fixture_type in self.available_fixture_types(group)
            ]

        def all_pytest_params(self) -> Sequence[tuple[str, str, str]]:
            return [
                (group, fixture_type, self.load_fixture(group, fixture_type))
                for group in self.available_fixture_servers()
                for fixture_type in self.available_fixture_types(group)
            ]

    @staticmethod
    def fixture_filename(
        group: str,
        kind: str,
        file_extension: str = ".ldif",
    ) -> str:
        return f"{group}_{kind}_fixtures{file_extension}"

    @classmethod
    def fixture_path(
        cls,
        group: str,
        kind: str,
        *,
        fixtures_root: Path | None = None,
        file_extension: str = ".ldif",
    ) -> Path:
        fixtures_root = fixtures_root or Path.cwd()
        file_path = (
            fixtures_root
            / group
            / cls.fixture_filename(
                group,
                kind,
                file_extension=file_extension,
            )
        )
        if not file_path.exists():
            raise FileNotFoundError(f"Fixture file not found: {file_path}")
        return file_path

    @classmethod
    def load_fixture(
        cls,
        group: str,
        kind: str,
        *,
        fixtures_root: Path | None = None,
        file_extension: str = ".ldif",
    ) -> str:
        return cls.fixture_path(
            group,
            kind,
            fixtures_root=fixtures_root,
            file_extension=file_extension,
        ).read_text(encoding="utf-8")

    @classmethod
    def fixture_exists(
        cls,
        group: str,
        kind: str,
        *,
        fixtures_root: Path | None = None,
        file_extension: str = ".ldif",
    ) -> bool:
        try:
            cls.fixture_path(
                group,
                kind,
                fixtures_root=fixtures_root,
                file_extension=file_extension,
            )
        except FileNotFoundError:
            return False
        return True

    @classmethod
    def available_fixture_servers(
        cls,
        *,
        fixtures_root: Path | None = None,
    ) -> tuple[str, ...]:
        fixtures_root = fixtures_root or Path.cwd()
        if not fixtures_root.exists():
            return ()
        return tuple(
            sorted(
                directory.name
                for directory in fixtures_root.iterdir()
                if directory.is_dir()
            ),
        )

    @classmethod
    def available_fixture_types(
        cls,
        group: str,
        *,
        fixtures_root: Path | None = None,
        file_extension: str = ".ldif",
    ) -> tuple[str, ...]:
        fixtures_root = fixtures_root or Path.cwd()
        server_dir = fixtures_root / group
        if not server_dir.exists():
            return ()
        prefix = f"{group}_"
        suffix = f"_fixtures{file_extension}"
        return tuple(
            sorted(
                name[len(prefix) : -len(suffix)]
                for name in sorted(entry.name for entry in server_dir.iterdir())
                if name.startswith(prefix) and name.endswith(suffix)
            ),
        )

    @classmethod
    def load_server_fixtures(
        cls,
        group: str,
        *,
        fixtures_root: Path | None = None,
        file_extension: str = ".ldif",
    ) -> Mapping[str, str]:
        return {
            fixture_type: cls.load_fixture(
                group,
                fixture_type,
                fixtures_root=fixtures_root,
                file_extension=file_extension,
            )
            for fixture_type in cls.available_fixture_types(
                group,
                fixtures_root=fixtures_root,
                file_extension=file_extension,
            )
        }

    @classmethod
    def bind(
        cls,
        fixtures_root: Path,
        *,
        file_extension: str = ".ldif",
    ) -> BoundFixtures:
        return cls.BoundFixtures(
            fixtures_root,
            file_extension=file_extension,
        )

    @classmethod
    def pytest_params_for(
        cls,
        group: str,
        *,
        fixtures_root: Path,
        file_extension: str = ".ldif",
    ) -> Sequence[tuple[str, str]]:
        return cls.bind(
            fixtures_root,
            file_extension=file_extension,
        ).pytest_params_for_group(group)

    @classmethod
    def all_pytest_params(
        cls,
        *,
        fixtures_root: Path,
        file_extension: str = ".ldif",
    ) -> Sequence[tuple[str, str, str]]:
        return cls.bind(
            fixtures_root,
            file_extension=file_extension,
        ).all_pytest_params()

    @staticmethod
    def default_handler_case_specs() -> Sequence[
        Mapping[str, t.Tests.TestobjectSerializable]
    ]:
        """Create shared handler test-case specs for service-base tests."""
        return [
            {
                "handler_id": "success_command",
                "handler_type": "COMMAND",
                "expected_result": "Handled: test",
                "description": "Command handler success",
            },
            {
                "handler_id": "success_query",
                "handler_type": "QUERY",
                "expected_result": "Handled: query",
                "description": "Query handler success",
            },
            {
                "handler_id": "success_event",
                "handler_type": "EVENT",
                "expected_result": "Handled: event",
                "description": "Event handler success",
            },
            {
                "handler_id": "fail_command",
                "handler_type": "COMMAND",
                "should_fail": True,
                "error_message": "Command failed",
                "description": "Command handler failure",
            },
            {
                "handler_id": "fail_query",
                "handler_type": "QUERY",
                "should_fail": True,
                "error_message": "Query failed",
                "description": "Query handler failure",
            },
        ]

    @staticmethod
    def create_result_ok(
        value: t.Tests.TestobjectSerializable,
    ) -> p.Result[t.Tests.TestobjectSerializable]:
        """Create a generic successful result for test flows."""
        return r[t.Tests.TestobjectSerializable].ok(value)

    @staticmethod
    def create_result_failure(
        message: str,
        *,
        error_code: str = "TEST_ERROR",
        error_data: t.JsonMapping | t.ConfigModelInput | None = None,
    ) -> p.Result[t.Tests.TestobjectSerializable]:
        """Create a generic failed result for test flows."""
        return r[t.Tests.TestobjectSerializable].fail(
            message,
            error_code=error_code,
            error_data=error_data,
        )

    @staticmethod
    def valid_email_cases() -> Sequence[tuple[str, bool]]:
        """Get valid email test cases.

        Returns:
            List of (email, valid) tuples

        """
        return [
            ("test@example.com", True),
            ("user.name@domain.co.uk", True),
            ("test+tag@example.com", True),
            ("invalid-email", False),
            ("@example.com", False),
            ("test@", False),
            ("", False),
        ]


td = FlextTestsDomains

__all__: list[str] = ["FlextTestsDomains", "td"]
