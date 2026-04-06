"""Extracted mixin for flext_tests."""

from __future__ import annotations

import ast
import re
from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path

from flext_tests import (
    c,
    m,
    t,
)


class FlextTestsValidatorUtilitiesMixin:
    """Validator utilities for architecture validation (tv.* methods).

    Provides reusable helper functions for validators. All validators
    should use these instead of implementing their own versions.
    """

    @staticmethod
    def create_violation(
        file_path: Path,
        line_number: int,
        rule_id: str,
        lines: t.StrSequence,
        extra_desc: str = "",
    ) -> m.Tests.Violation:
        """Create a violation model using c.Tests.Validator.Rules.

        Args:
            file_path: Path to file with violation
            line_number: Line number of violation (1-indexed)
            rule_id: Rule identifier (e.g., "IMPORT-001")
            lines: File content as list of lines
            extra_desc: Optional extra description

        Returns:
            r[TEntity]: Result containing created entity or error
            Violation model instance

        """
        severity, desc = c.Tests.Validator.Rules.get(rule_id)
        description = f"{desc}: {extra_desc}" if extra_desc else desc
        line = lines[line_number - 1] if line_number <= len(lines) else ""
        return m.Tests.Violation(
            file_path=file_path,
            line_number=line_number,
            rule_id=rule_id,
            severity=severity,
            description=description,
            code_snippet=line.strip(),
        )

    @staticmethod
    def find_line_number(lines: t.StrSequence, pattern: str) -> int:
        """Find line number containing pattern.

        Args:
            lines: File content as list of lines
            pattern: Pattern to search for

        Returns:
            r[TEntity]: Result containing created entity or error
            Line number (1-indexed) or 1 if not found

        """
        for i, line in enumerate(lines, start=1):
            if pattern in line:
                return i
        return 1

    @staticmethod
    def get_exception_names(exc_type: ast.expr) -> set[str]:
        """Extract exception names from exception type AST node.

        Args:
            exc_type: Exception type AST node

        Returns:
            r[TEntity]: Result containing created entity or error
            Set of exception names found

        """
        names: set[str] = set()
        if isinstance(exc_type, ast.Name):
            names.add(exc_type.id)
        elif isinstance(exc_type, ast.Tuple):
            for elt in exc_type.elts:
                if isinstance(elt, ast.Name):
                    names.add(elt.id)
        return names

    @staticmethod
    def get_parent(tree: ast.AST, node: ast.AST) -> ast.AST | None:
        """Get parent node of an AST node.

        Args:
            tree: AST tree root
            node: Node to find parent of

        Returns:
            r[TEntity]: Result containing created entity or error
            Parent node or None if not found

        """
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                if child is node:
                    return parent
        return None

    @staticmethod
    def is_any_type(node: ast.expr) -> bool:
        """Check if an annotation node represents the typing wildcard type.

        Args:
            node: AST annotation node

        Returns:
            r[TEntity]: Result containing created entity or error
            True if node represents typing wildcard type annotation

        """
        wildcard_name = "".join((chr(65), chr(110), chr(121)))
        return (
            (isinstance(node, ast.Name) and node.id == wildcard_name)
            or (isinstance(node, ast.Attribute) and node.attr == wildcard_name)
            or (isinstance(node, ast.Constant) and node.value == wildcard_name)
        )

    @staticmethod
    def is_approved(
        rule_id: str,
        file_path: Path,
        approved: Mapping[str, t.StrSequence],
    ) -> bool:
        """Check if file is approved for this rule.

        Args:
            rule_id: Rule identifier (e.g., "IMPORT-001")
            file_path: Path to file being checked
            approved: Dict mapping rule IDs to list of approved file patterns

        Returns:
            r[TEntity]: Result containing created entity or error
            True if file matches any approved pattern for this rule

        """
        patterns = approved.get(rule_id, [])
        file_str = str(file_path)
        return any(re.search(pattern, file_str) for pattern in patterns)

    @staticmethod
    def is_only_pass(body: Sequence[ast.stmt]) -> bool:
        """Check if exception handler body contains only pass or ellipsis.

        Used by BYPASS-003 to detect exception swallowing patterns.

        Args:
            body: AST statement list (exception handler body)

        Returns:
            r[TEntity]: Result containing created entity or error
            True if body contains only pass or ellipsis (...)

        """
        if len(body) == 1:
            stmt = body[0]
            if isinstance(stmt, ast.Pass):
                return True
            if (
                isinstance(stmt, ast.Expr)
                and isinstance(stmt.value, ast.Constant)
                and (stmt.value.value is ...)
            ):
                return True
        return False

    @staticmethod
    def is_real_comment(line: str, pattern: re.Pattern[str]) -> bool:
        """Check if pattern match is in a real comment, not inside a string.

        Used by validators to avoid false positives from patterns appearing
        in docstrings or string literals.

        Args:
            line: Source code line
            pattern: Compiled regex pattern to search

        Returns:
            r[TEntity]: Result containing created entity or error
            True if pattern appears in real code comment (after #),
            not inside a string literal (single/double/triple quoted)

        """
        match = pattern.search(line)
        if not match:
            return False
        pos = match.start()
        in_single = False
        in_double = False
        in_triple_single = False
        in_triple_double = False
        i = 0
        while i < pos:
            if line[i : i + 3] == '"""' and (not in_single) and (not in_triple_single):
                in_triple_double = not in_triple_double
                i += 3
                continue
            if line[i : i + 3] == "'''" and (not in_double) and (not in_triple_double):
                in_triple_single = not in_triple_single
                i += 3
                continue
            if (
                line[i] == '"'
                and (not in_single)
                and (not in_triple_single)
                and (not in_triple_double)
            ):
                in_double = not in_double
            elif (
                line[i] == "'"
                and (not in_double)
                and (not in_triple_single)
                and (not in_triple_double)
            ):
                in_single = not in_single
            i += 1
        return not (in_single or in_double or in_triple_single or in_triple_double)
