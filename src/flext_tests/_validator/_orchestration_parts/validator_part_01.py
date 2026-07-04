"""Aggregate validation orchestration for flext-tests."""

from __future__ import annotations

import fnmatch
from types import MappingProxyType
from typing import TYPE_CHECKING, Annotated, ClassVar

from flext_tests import c, m, s, t, u

if TYPE_CHECKING:
    from pathlib import Path


class FlextTestsValidator(s[m.Tests.ScanResult]):
    """FLEXT architecture validator orchestration."""

    Violation: ClassVar[type[m.Tests.Violation]] = m.Tests.Violation
    ScanResult: ClassVar[type[m.Tests.ScanResult]] = m.Tests.ScanResult

    class AllValidationOptions(m.Value):
        """Options envelope for aggregate validation runs."""

        pyproject_path: Annotated[
            Path | None,
            u.Field(
                description="Optional path to pyproject.toml for settings validation.",
            ),
        ] = None
        exclude_patterns: Annotated[
            t.StrSequence,
            u.Field(
                description="Glob patterns to exclude from validation.",
            ),
        ] = u.Field(default_factory=lambda: list(c.Tests.VALIDATOR_EXCLUDE_PATTERNS))
        approved_exceptions: Annotated[
            t.MappingKV[str, t.StrSequence],
            u.Field(
                description="Rule-to-path allowlist for approved exceptions.",
            ),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))
        include_tests_validation: Annotated[
            bool,
            u.Field(
                description="Whether to include test-pattern validation in the aggregate run.",
            ),
        ] = False

    @classmethod
    def _discover_files(
        cls,
        path: Path,
        exclude_patterns: t.StrSequence | None = None,
    ) -> t.SequenceOf[Path]:
        """Discover Python files to scan."""
        excludes = exclude_patterns or list(c.Tests.VALIDATOR_EXCLUDE_PATTERNS)
        if path.is_file():
            return [path] if path.suffix == ".py" else []
        files: t.SequenceOf[Path] = [
            py_file
            for py_file in u.Infra.iter_matching_files(path, includes=["*.py"])
            if not any(fnmatch.fnmatch(str(py_file), pattern) for pattern in excludes)
        ]
        return files


__all__: list[str] = ["FlextTestsValidator"]
