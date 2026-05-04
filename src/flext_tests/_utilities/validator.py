"""Extracted mixin for flext_tests."""

from __future__ import annotations

from pathlib import Path

from flext_infra import t as it
from flext_tests.constants import FlextTestsConstants as c
from flext_tests.models import FlextTestsModels as m
from flext_tests.typings import FlextTestsTypes as t


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
        """Create a violation model using c.Tests.

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
        severity, desc = c.Tests.validator_rule(rule_id)
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
    def split_import_targets(value: str) -> tuple[str, ...]:
        """Normalize one import target list into canonical imported names."""
        cleaned = value.split("#", maxsplit=1)[0].replace("(", " ").replace(")", " ")
        targets: list[str] = []
        for raw_target in cleaned.split(","):
            target = raw_target.split(" as ", maxsplit=1)[0].strip()
            if target:
                targets.append(target)
        return tuple(targets)

    @staticmethod
    def approved(
        rule_id: str,
        file_path: Path,
        approved: t.MappingKV[str, t.StrSequence],
        extra_patterns: t.StrSequence = (),
    ) -> bool:
        """Check if file is approved for this rule.

        Args:
            rule_id: Rule identifier (e.g., "IMPORT-001")
            file_path: Path to file being checked
            approved: Dict mapping rule IDs to list of approved file patterns
            extra_patterns: Additional canonical patterns to honor for this scan

        Returns:
            r[TEntity]: Result containing created entity or error
            True if file matches any approved pattern for this rule

        """
        patterns = tuple(approved.get(rule_id, ())) + tuple(extra_patterns)
        file_str = str(file_path)
        return any(
            c.Tests.path_pattern_matches(file_str, pattern) for pattern in patterns
        )

    @staticmethod
    def code_match(line: str, pattern: it.Infra.RegexPattern) -> bool:
        """Check if one pattern match appears outside quoted string literals.

        Args:
            line: Source code line
            pattern: Compiled regex pattern to search

        Returns:
            r[TEntity]: Result containing created entity or error
            True if the first match is not inside a quoted string literal

        """
        match = pattern.search(line)
        if match is None:
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

    @staticmethod
    def real_comment(line: str, pattern: it.Infra.RegexPattern) -> bool:
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
        return FlextTestsValidatorUtilitiesMixin.code_match(line, pattern)

    @staticmethod
    def except_block_only_pass(lines: t.StrSequence, line_number: int) -> bool:
        """Check whether one ``except`` block body contains only pass or ellipsis."""
        header_index = line_number - 1
        if header_index < 0 or header_index >= len(lines):
            return False
        header_line = lines[header_index]
        header_match = c.Tests.VALIDATOR_EXCEPT_HEADER_RE.match(header_line)
        if header_match is None:
            return False
        trailing = header_line.rsplit(":", maxsplit=1)[-1].strip()
        if (
            trailing
            and c.Tests.VALIDATOR_PASS_OR_ELLIPSIS_RE.match(trailing) is not None
        ):
            return True
        header_indent = len(header_match.group("indent").expandtabs())
        body_lines: list[str] = []
        for line in lines[header_index + 1 :]:
            stripped = line.strip()
            if not stripped:
                continue
            current_indent = len(line.expandtabs()) - len(line.lstrip().expandtabs())
            if current_indent <= header_indent:
                break
            if stripped.startswith("#"):
                continue
            body_lines.append(stripped)
        return (
            len(body_lines) == 1
            and c.Tests.VALIDATOR_PASS_OR_ELLIPSIS_RE.match(body_lines[0]) is not None
        )
