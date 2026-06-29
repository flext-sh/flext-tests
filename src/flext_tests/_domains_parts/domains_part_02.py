"""Fixture discovery helpers for flext-tests domains."""

from __future__ import annotations

from pathlib import Path

from flext_tests import t
from flext_tests._domains_parts.domains_part_01 import (
    FlextTestsDomains as FlextTestsDomainsPart01,
)


class FlextTestsDomains(FlextTestsDomainsPart01):
    """Fixture discovery helpers."""

    @classmethod
    def available_fixture_servers(
        cls,
        *,
        fixtures_root: Path | None = None,
    ) -> t.StrSequence:
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
    ) -> t.StrSequence:
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
    ) -> t.MappingKV[str, str]:
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


__all__: list[str] = ["FlextTestsDomains"]
