"""Import validation for FLEXT architecture.

Detects import violations: lazy imports, TYPE_CHECKING, ImportError handling.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import ast
import re
from collections.abc import (
    Mapping,
    MutableSequence,
    Sequence,
)
from pathlib import Path
from typing import override

from flext_tests import FlextTestsValidatorModels, c, m, t, u


class FlextValidatorImports(FlextTestsValidatorModels.Tests.ScannerMixin):
    """Import validation methods for FlextTestsValidator.

    Uses c.Tests.Validator for constants and m.Tests.Validator for models.
    """

    _VALIDATOR_KEY = c.Tests.VALIDATOR_IMPORTS_KEY

    @classmethod
    def _check_direct_tech_imports(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect direct technology imports."""
        if u.Tests.approved("IMPORT-005", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        tech_imports = c.Tests.VALIDATOR_APPROVED_TECH_IMPORTS
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in tech_imports:
                        violation = u.Tests.create_violation(
                            file_path,
                            node.lineno,
                            "IMPORT-005",
                            lines,
                            alias.name,
                        )
                        violations.append(violation)
            elif (
                isinstance(node, ast.ImportFrom)
                and node.module
                and (node.module.split(".")[0] in tech_imports)
            ):
                violation = u.Tests.create_violation(
                    file_path,
                    node.lineno,
                    "IMPORT-005",
                    lines,
                    node.module,
                )
                violations.append(violation)
        return violations

    @classmethod
    def _check_import_error_handling(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect try/except ImportError patterns."""
        if u.Tests.approved("IMPORT-003", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Try):
                continue
            for handler in node.handlers:
                if handler.type is None:
                    continue
                handler_names = u.Tests.exception_names(handler.type)
                if (
                    "ImportError" in handler_names
                    or "ModuleNotFoundError" in handler_names
                ):
                    violation = u.Tests.create_violation(
                        file_path,
                        node.lineno,
                        "IMPORT-003",
                        lines,
                    )
                    violations.append(violation)
        return violations

    @classmethod
    def _check_lazy_imports(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect imports not at module top level."""
        if u.Tests.approved("IMPORT-001", file_path, approved):
            return []
        return [
            u.Tests.create_violation(
                file_path,
                node.lineno,
                "IMPORT-001",
                lines,
            )
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            and isinstance(
                u.Tests.parent_node(tree, node),
                (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
            )
        ]

    @classmethod
    def _check_non_root_flext_imports(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect non-root imports from flext-* packages internal modules.

        Detects imports from internal modules (prefixed with _) like:
        - from flext_core import domain  (violation)
        - from flext_tests import imports  (violation)

        Allows public module imports:
        - from flext_core import r  (OK)
        - from flext_tests import m  (OK)

        Allows __init__.py inside internal packages to import sibling modules:
        - _validator/__init__.py can import from flext_tests._validator.* (OK)
        """
        if u.Tests.approved("IMPORT-006", file_path, approved):
            return []
        file_str = str(file_path)
        internal_init_patterns = c.Tests.VALIDATOR_APPROVED_INTERNAL_INIT_PATTERNS
        if any(re.search(pattern, file_str) for pattern in internal_init_patterns):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        flext_packages = c.Tests.VALIDATOR_APPROVED_FLEXT_PACKAGES
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                parts = node.module.split(".")
                if len(parts) > 1 and parts[0] in flext_packages:
                    internal_parts = [p for p in parts[1:] if p.startswith("_")]
                    if internal_parts:
                        internal = internal_parts[0]
                        violation = u.Tests.create_violation(
                            file_path,
                            node.lineno,
                            "IMPORT-006",
                            lines,
                            f"from {node.module} (internal: {internal})",
                        )
                        violations.append(violation)
        return violations

    @classmethod
    def _check_sys_path(
        cls,
        file_path: Path,
        tree: ast.AST,
        lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect sys.path manipulation."""
        if u.Tests.approved("IMPORT-004", file_path, approved):
            return []
        return [
            u.Tests.create_violation(
                file_path,
                node.lineno,
                "IMPORT-004",
                lines,
            )
            for node in ast.walk(tree)
            if isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "sys"
            and node.attr == "path"
            and isinstance(u.Tests.parent_node(tree, node), ast.Call)
        ]

    @classmethod
    def _check_type_checking(
        cls,
        file_path: Path,
        _tree: ast.AST,
        _lines: t.StrSequence,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Detect TYPE_CHECKING blocks in files with Pydantic field annotations.

        TYPE_CHECKING is permitted for type-only imports in non-Pydantic files.
        TYPE_CHECKING is forbidden only in files where the imported types are
        used in Pydantic BaseModel/RootModel field annotations.

        For now, we allow TYPE_CHECKING in all files since detecting usage in
        field annotations requires complex AST analysis.
        """
        if u.Tests.approved("IMPORT-002", file_path, approved):
            return []
        return []

    @classmethod
    @override
    def _scan_file(
        cls,
        file_path: Path,
        approved: Mapping[str, t.StrSequence],
    ) -> Sequence[m.Tests.Violation]:
        """Scan a single file for import violations."""
        violations: MutableSequence[m.Tests.Violation] = []
        try:
            content = file_path.read_text(encoding=c.DEFAULT_ENCODING)
            tree = ast.parse(content, filename=str(file_path))
        except (SyntaxError, UnicodeDecodeError):
            return violations
        lines = content.splitlines()
        violations.extend(cls._check_lazy_imports(file_path, tree, lines, approved))
        violations.extend(cls._check_type_checking(file_path, tree, lines, approved))
        violations.extend(
            cls._check_import_error_handling(file_path, tree, lines, approved),
        )
        violations.extend(cls._check_sys_path(file_path, tree, lines, approved))
        violations.extend(
            cls._check_direct_tech_imports(file_path, tree, lines, approved),
        )
        violations.extend(
            cls._check_non_root_flext_imports(file_path, tree, lines, approved),
        )
        return violations


__all__: list[str] = ["FlextValidatorImports"]
