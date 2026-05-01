"""FLEXT Architecture Validator.

Provides FlextTestsValidator (tv) for detecting architecture violations in pytest tests.

Usage:
from flext_tests import tv, t

    # Validate imports
    result = tv.imports(Path("src"))
    assert result.success and result.value.passed

    # Validate types
    result = tv.types(Path("src"))

    # Validate pyproject.toml
    result = tv.validate_config(Path("pyproject.toml"))

    # Validate all
    result = tv.all(Path("src"), pyproject=Path("pyproject.toml"))

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import fnmatch
from collections.abc import (
    MutableSequence,
)
from pathlib import Path
from types import MappingProxyType
from typing import Annotated, ClassVar, override

from flext_tests import (
    FlextValidatorBypass,
    FlextValidatorImports,
    FlextValidatorLayer,
    FlextValidatorMarkdown,
    FlextValidatorSettings,
    FlextValidatorTests,
    FlextValidatorTypes,
    c,
    m,
    p,
    r,
    t,
    u,
)
from flext_tests.base import s


class FlextTestsValidator(s[m.Tests.ScanResult]):
    """FLEXT Architecture Validator - detects code violations.

        Provides methods to validate:
        - imports: lazy imports, TYPE_CHECKING, ImportError handling
    - types: type suppression, wildcard types, unapproved
        - tests: monkeypatch, mocks, @patch
        - settings: pyproject.toml deviations
        - bypass: noqa, pragma, exception swallowing
        - layer: cross-layer import violations
        - markdown: Python code blocks in .md files

        Uses c.Validator for all rules, messages, and defaults.

        Usage:
            from flext_tests import tv

            result = tv.imports(Path("src"))
            result = tv.types(Path("src"))
            result = tv.validate_config(Path("pyproject.toml"))
            result = tv.all(Path("src"))
    """

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
        """Discover Python files to scan.

        Args:
            path: Directory or file to scan
            exclude_patterns: Glob patterns to exclude

        Returns:
            List of Python file paths

        """
        excludes = exclude_patterns or list(c.Tests.VALIDATOR_EXCLUDE_PATTERNS)
        if path.is_file():
            return [path] if path.suffix == ".py" else []
        files: t.SequenceOf[Path] = [
            py_file
            for py_file in path.rglob("*.py")
            if not any(fnmatch.fnmatch(str(py_file), pattern) for pattern in excludes)
        ]
        return files

    @classmethod
    def all(
        cls,
        path: Path,
        options: AllValidationOptions | None = None,
        **kwargs: t.JsonValue,
    ) -> p.Result[m.Tests.ScanResult]:
        """Run all validations and combine results.

        Args:
            path: Directory or file to scan
            pyproject_path: Path to pyproject.toml (optional)
            exclude_patterns: Glob patterns to exclude
            approved_exceptions: Dict mapping rule IDs to approved file patterns
            include_tests_validation: Whether to include test pattern validation

        Returns:
            r[ScanResult] with combined violations from all validators

        """
        payload: t.MutableJsonMapping = (
            options.model_dump(mode="python") if options is not None else {}
        )
        payload.update(kwargs)
        all_options = cls.AllValidationOptions.model_validate(payload)
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
        """Validate bypass patterns in Python files.

        Detects:
        - BYPASS-001: noqa comments
        - BYPASS-002: pragma: no cover (unapproved)
        - BYPASS-003: Exception swallowing

        Args:
            path: Directory or file to scan
            exclude_patterns: Glob patterns to exclude
            approved_exceptions: Dict mapping rule IDs to approved file patterns

        Returns:
            r[ScanResult] with violations found

        """
        files = cls._discover_files(path, exclude_patterns)
        return FlextValidatorBypass.scan(files, approved_exceptions)

    @classmethod
    def imports(
        cls,
        path: Path,
        exclude_patterns: t.StrSequence | None = None,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate imports in Python files.

        Detects:
        - IMPORT-001: Lazy imports (not at module top)
        - IMPORT-002: TYPE_CHECKING blocks
        - IMPORT-003: try/except ImportError
        - IMPORT-004: sys.path manipulation
        - IMPORT-005: Direct technology imports
        - IMPORT-006: Non-root flext-* imports

        Args:
            path: Directory or file to scan
            exclude_patterns: Glob patterns to exclude (defaults to common excludes)
            approved_exceptions: Dict mapping rule IDs to approved file patterns

        Returns:
            r[ScanResult] with violations found

        """
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
        """Validate layer dependencies in Python files.

        Detects:
        - LAYER-001: Lower layer importing upper layer

        Args:
            path: Directory or file to scan
            exclude_patterns: Glob patterns to exclude
            approved_exceptions: Dict mapping rule IDs to approved file patterns
            layer_hierarchy: Custom layer hierarchy (module_name -> layer_number)

        Returns:
            r[ScanResult] with violations found

        """
        files = cls._discover_files(path, exclude_patterns)
        return FlextValidatorLayer.scan(files, approved_exceptions, layer_hierarchy)

    @classmethod
    def tests(
        cls,
        path: Path,
        exclude_patterns: t.StrSequence | None = None,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate test patterns in Python files.

        Detects:
        - TEST-001: monkeypatch usage
        - TEST-002: Mock/MagicMock usage
        - TEST-003: @patch decorator usage

        Args:
            path: Directory or file to scan
            exclude_patterns: Glob patterns to exclude
            approved_exceptions: Dict mapping rule IDs to approved file patterns

        Returns:
            r[ScanResult] with violations found

        """
        files = cls._discover_files(path, exclude_patterns)
        return FlextValidatorTests.scan(files, approved_exceptions)

    @classmethod
    def types(
        cls,
        path: Path,
        exclude_patterns: t.StrSequence | None = None,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate type annotations in Python files.

        Detects:
        - TYPE-001:
        - TYPE-002 type annotations
        - TYPE-003: Unapproved  usage

        Args:
            path: Directory or file to scan
            exclude_patterns: Glob patterns to exclude
            approved_exceptions: Dict mapping rule IDs to approved file patterns

        Returns:
            r[ScanResult] with violations found

        """
        files = cls._discover_files(path, exclude_patterns)
        return FlextValidatorTypes.scan(files, approved_exceptions)

    @classmethod
    def validate_config(
        cls,
        pyproject_path: Path,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate pyproject.toml configuration.

        Detects:
        - CONFIG-001: mypy ignore_errors = true
        - CONFIG-002: Custom ruff ignores beyond approved
        - CONFIG-003: disallow_incomplete_defs = false
        - CONFIG-004: warn_return_any = false
        - CONFIG-005: reportPrivateUsage = false

        Args:
            pyproject_path: Path to pyproject.toml
            approved_exceptions: Dict mapping rule IDs to approved file patterns

        Returns:
            r[ScanResult] with violations found

        """
        return FlextValidatorSettings.validate(pyproject_path, approved_exceptions)

    @classmethod
    def markdown(
        cls,
        project_root: Path,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate Python code blocks in markdown files.

        Detects:
        - MD-001: Python syntax errors
        - MD-002: Forbidden typing imports (Any, Optional, Union)
        - MD-003: Missing future annotations
        - MD-004: Forbidden annotations (object as type)

        Args:
            project_root: Root directory to scan for .md files
            approved_exceptions: Dict mapping rule IDs to approved file patterns

        Returns:
            r[ScanResult] with violations found

        """
        md_files = FlextValidatorMarkdown.collect_markdown_files(project_root)
        return FlextValidatorMarkdown.markdown(
            md_files,
            approved_exceptions=approved_exceptions,
        )


tv = FlextTestsValidator
__all__: list[str] = ["FlextTestsValidator", "tv"]
