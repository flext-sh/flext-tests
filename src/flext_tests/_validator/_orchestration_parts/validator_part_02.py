"""Concrete validation verbs for flext-tests."""

from __future__ import annotations

from collections.abc import MutableSequence
from pathlib import Path
from typing import override

from flext_tests import (
    m,
    p,
    r,
    t,
)
from flext_tests._validator._orchestration_parts.validator_part_01 import (
    FlextTestsValidator as FlextTestsValidatorPart01,
)
from flext_tests._validator.bypass import FlextValidatorBypass
from flext_tests._validator.imports import FlextValidatorImports
from flext_tests._validator.layer import FlextValidatorLayer
from flext_tests._validator.markdown import FlextValidatorMarkdown
from flext_tests._validator.settings import FlextValidatorSettings
from flext_tests._validator.tests import FlextValidatorTests
from flext_tests._validator.types import FlextValidatorTypes


class FlextTestsValidator(FlextTestsValidatorPart01):
    """Concrete validation verbs for the public facade."""

    @override
    def execute(self) -> p.Result[m.Tests.ScanResult]:
        """Execute validator service with default current-path scope."""
        return self.all(Path.cwd())

    @classmethod
    def all(
        cls,
        path: Path,
        options: FlextTestsValidatorPart01.AllValidationOptions | None = None,
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

    @classmethod
    def bypass(
        cls,
        path: Path,
        exclude_patterns: t.StrSequence | None = None,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate bypass patterns in Python files."""
        files = cls._discover_files(path, exclude_patterns)
        return FlextValidatorBypass.scan(files, approved_exceptions)

    @classmethod
    def imports(
        cls,
        path: Path,
        exclude_patterns: t.StrSequence | None = None,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate imports in Python files."""
        files = cls._discover_files(path, exclude_patterns)
        return FlextValidatorImports.scan(files, approved_exceptions)

    @classmethod
    def layer(
        cls,
        path: Path,
        exclude_patterns: t.StrSequence | None = None,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
        layer_hierarchy: t.IntMapping | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate layer dependencies in Python files."""
        files = cls._discover_files(path, exclude_patterns)
        return FlextValidatorLayer.scan(files, approved_exceptions, layer_hierarchy)

    @classmethod
    def tests(
        cls,
        path: Path,
        exclude_patterns: t.StrSequence | None = None,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate test patterns in Python files."""
        files = cls._discover_files(path, exclude_patterns)
        return FlextValidatorTests.scan(files, approved_exceptions)

    @classmethod
    def types(
        cls,
        path: Path,
        exclude_patterns: t.StrSequence | None = None,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate type annotations in Python files."""
        files = cls._discover_files(path, exclude_patterns)
        return FlextValidatorTypes.scan(files, approved_exceptions)

    @classmethod
    def validate_config(
        cls,
        pyproject_path: Path,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate pyproject.toml configuration."""
        return FlextValidatorSettings.validate(pyproject_path, approved_exceptions)

    @classmethod
    def markdown(
        cls,
        project_root: Path,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate Python code blocks in markdown files."""
        md_files = FlextValidatorMarkdown.collect_markdown_files(project_root)
        return FlextValidatorMarkdown.markdown(
            md_files,
            approved_exceptions=approved_exceptions,
        )


__all__: list[str] = ["FlextTestsValidator"]
