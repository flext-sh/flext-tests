"""Test domain facade for FLEXT ecosystem tests."""

from __future__ import annotations

from pathlib import Path

from flext_tests import t
from flext_tests._domains_parts.domains_part_03 import (
    FlextTestsDomains as FlextTestsDomainsPart03,
)


class FlextTestsDomains(FlextTestsDomainsPart03):
    """Test domain objects and fixtures."""

    class BoundFixtures:
        """Bound fixture loader for one fixture root and extension."""

        def __init__(
            self,
            fixtures_root: Path,
            *,
            file_extension: str = ".ldif",
        ) -> None:
            self._fixtures_root: Path = fixtures_root
            self._file_extension: str = file_extension

        def fixture_path(self, group: str, kind: str) -> Path:
            return FlextTestsDomains.fixture_path(
                group,
                kind,
                fixtures_root=self._fixtures_root,
                file_extension=self._file_extension,
            )

        def load_fixture(self, group: str, kind: str) -> str:
            return FlextTestsDomains.load_fixture(
                group,
                kind,
                fixtures_root=self._fixtures_root,
                file_extension=self._file_extension,
            )

        def fixture_exists(self, group: str, kind: str) -> bool:
            return FlextTestsDomains.fixture_exists(
                group,
                kind,
                fixtures_root=self._fixtures_root,
                file_extension=self._file_extension,
            )

        def available_fixture_servers(self) -> t.StrSequence:
            return FlextTestsDomains.available_fixture_servers(
                fixtures_root=self._fixtures_root,
            )

        def available_fixture_types(self, group: str) -> t.StrSequence:
            return FlextTestsDomains.available_fixture_types(
                group,
                fixtures_root=self._fixtures_root,
                file_extension=self._file_extension,
            )

        def load_server_fixtures(self, group: str) -> t.MappingKV[str, str]:
            return FlextTestsDomains.load_server_fixtures(
                group,
                fixtures_root=self._fixtures_root,
                file_extension=self._file_extension,
            )

        def load_fixture_kind(self, kind: str) -> t.MappingKV[str, str]:
            return {
                group: self.load_fixture(group, kind)
                for group in self.available_fixture_servers()
                if self.fixture_exists(group, kind)
            }

        def load_all(self) -> t.MappingKV[str, t.MappingKV[str, str]]:
            return {
                group: self.load_server_fixtures(group)
                for group in self.available_fixture_servers()
            }

        def pytest_params_for_group(self, group: str) -> t.StrPairSequence:
            return [
                (fixture_type, self.load_fixture(group, fixture_type))
                for fixture_type in self.available_fixture_types(group)
            ]

        def all_pytest_params(self) -> t.SequenceOf[tuple[str, str, str]]:
            return [
                (group, fixture_type, self.load_fixture(group, fixture_type))
                for group in self.available_fixture_servers()
                for fixture_type in self.available_fixture_types(group)
            ]

    @classmethod
    def bind(
        cls,
        fixtures_root: Path,
        *,
        file_extension: str = ".ldif",
    ) -> BoundFixtures:
        return cls.BoundFixtures(fixtures_root, file_extension=file_extension)


td = FlextTestsDomains

__all__: list[str] = ["FlextTestsDomains", "td"]
