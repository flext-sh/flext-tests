"""Concrete validation verbs for flext-tests."""

from __future__ import annotations

from pathlib import Path

from flext_tests import (
    FlextValidatorBypass,
    FlextValidatorImports,
    FlextValidatorLayer,
    FlextValidatorMarkdown,
    FlextValidatorSettings,
    FlextValidatorTests,
    FlextValidatorTypes,
    m,
    p,
    t,
)
from flext_tests._validator._orchestration_parts.validator_part_01 import (
    FlextTestsValidator as FlextTestsValidatorPart01,
)


class FlextTestsValidator(FlextTestsValidatorPart01):
    """Concrete validation verbs for the public facade."""

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
