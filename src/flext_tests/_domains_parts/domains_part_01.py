"""Fixture path and loading helpers for flext-tests domains."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_cli._utilities.files import FlextCliUtilitiesFiles

if TYPE_CHECKING:
    from flext_tests import p


class FlextTestsDomains:
    """Fixture path and file loading helpers."""

    @staticmethod
    def fixture_filename(
        group: str,
        kind: str,
        file_extension: str = ".ldif",
    ) -> str:
        return f"{group}_{kind}_fixtures{file_extension}"

    @classmethod
    def _resolve_fixture_path(
        cls,
        group: str,
        kind: str,
        *,
        fixtures_root: Path | None = None,
        file_extension: str = ".ldif",
    ) -> Path:
        """Compute the candidate fixture path without checking existence."""
        fixtures_root = fixtures_root or Path.cwd()
        return (
            fixtures_root
            / group
            / cls.fixture_filename(group, kind, file_extension=file_extension)
        )

    @classmethod
    def fixture_path(
        cls,
        group: str,
        kind: str,
        *,
        fixtures_root: Path | None = None,
        file_extension: str = ".ldif",
    ) -> Path:
        file_path = cls._resolve_fixture_path(
            group,
            kind,
            fixtures_root=fixtures_root,
            file_extension=file_extension,
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
        text_result: p.Result[str] = FlextCliUtilitiesFiles.files_read_text(
            cls.fixture_path(
                group,
                kind,
                fixtures_root=fixtures_root,
                file_extension=file_extension,
            ),
        )
        if text_result.failure:
            raise ValueError(text_result.error or "Fixture file read failed")
        text: str = text_result.value
        return text

    @classmethod
    def fixture_exists(
        cls,
        group: str,
        kind: str,
        *,
        fixtures_root: Path | None = None,
        file_extension: str = ".ldif",
    ) -> bool:
        return cls._resolve_fixture_path(
            group,
            kind,
            fixtures_root=fixtures_root,
            file_extension=file_extension,
        ).exists()


__all__: list[str] = ["FlextTestsDomains"]
