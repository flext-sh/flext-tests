"""Aggregate validation orchestration for flext-tests."""

from __future__ import annotations

import fnmatch
from collections.abc import MutableSequence
from pathlib import Path
from types import MappingProxyType
from typing import Annotated, ClassVar, override

from flext_tests import c, m, p, r, s, t, u


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

    @override
    def execute(self) -> p.Result[m.Tests.ScanResult]:
        """Execute validator service with default current-path scope."""
        return self.all(Path.cwd())

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

    @classmethod
    def all(
        cls,
        path: Path,
        options: AllValidationOptions | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Run all validations and combine results."""
        all_options = options or cls.AllValidationOptions()
        all_violations: MutableSequence[m.Tests.Violation] = []
        total_files = 0
        validators: MutableSequence[tuple[str, p.Result[m.Tests.ScanResult]]] = [
            (
                "imports",
                cls.imports(
                    path,
                    all_options.exclude_patterns,
                    all_options.approved_exceptions,
                ),
            ),
            (
                "types",
                cls.types(
                    path,
                    all_options.exclude_patterns,
                    all_options.approved_exceptions,
                ),
            ),
            (
                "bypass",
                cls.bypass(
                    path,
                    all_options.exclude_patterns,
                    all_options.approved_exceptions,
                ),
            ),
            (
                "layer",
                cls.layer(
                    path,
                    all_options.exclude_patterns,
                    all_options.approved_exceptions,
                ),
            ),
        ]
        if all_options.include_tests_validation:
            validators.append((
                "tests",
                cls.tests(
                    path,
                    all_options.exclude_patterns,
                    all_options.approved_exceptions,
                ),
            ))
        if (
            all_options.pyproject_path is not None
            and all_options.pyproject_path.exists()
        ):
            validators.append((
                "settings",
                cls.validate_config(
                    all_options.pyproject_path,
                    all_options.approved_exceptions,
                ),
            ))
        for name, result in validators:
            if result.failure:
                return r[m.Tests.ScanResult].fail(
                    f"Validator '{name}' failed: {result.error}",
                )
            scan_result = result.value
            all_violations.extend(scan_result.violations)
            total_files = max(total_files, scan_result.files_scanned)
        return r[m.Tests.ScanResult].ok(
            m.Tests.ScanResult.create(
                validator_name="all",
                files_scanned=total_files,
                violations=all_violations,
            ),
        )


__all__: list[str] = ["FlextTestsValidator"]
