"""Layer validation for FLEXT architecture.

Detects layer violations: lower layer importing upper layer.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableSequence
from pathlib import Path

from flext_tests import c, m, p, t, u


class FlextValidatorLayer:
    """Layer validation methods for FlextTestsValidator.

    Uses c.Tests.Validator, m.Tests.Validator, u.Tests.Validator.
    """

    @classmethod
    def _extract_module_name(cls, module_path: str) -> str:
        """Extract the final module name from an import path.

        Examples:
            'flext_core' -> 'result'
            'flext_core' -> 'domain'
            'result' -> 'result'

        """
        parts = module_path.split(".")
        return parts[-1]

    @classmethod
    def _imported_modules(cls, line: str) -> t.StrSequence:
        """Return imported module stems referenced by one import line."""
        from_match = c.Tests.VALIDATOR_FROM_IMPORT_LINE_RE.match(line)
        if from_match is not None and u.Tests.code_match(
            line, c.Tests.VALIDATOR_FROM_IMPORT_LINE_RE
        ):
            module = from_match.group("module").lstrip(".")
            return (cls._extract_module_name(module),) if module else ()

        import_match = c.Tests.VALIDATOR_IMPORT_LINE_RE.match(line)
        if import_match is None or not u.Tests.code_match(
            line, c.Tests.VALIDATOR_IMPORT_LINE_RE
        ):
            return ()

        modules: list[str] = []
        for target in u.Tests.split_import_targets(import_match.group("modules")):
            module = target.lstrip(".")
            if module:
                modules.append(cls._extract_module_name(module))
        return tuple(modules)

    @classmethod
    def _scan_file(
        cls,
        file_path: Path,
        approved: t.MappingKV[str, t.StrSequence],
        hierarchy: t.IntMapping,
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Scan a single file for layer violations."""
        if u.Tests.approved("LAYER-001", file_path, approved):
            return []
        violations: MutableSequence[m.Tests.Violation] = []
        current_module = file_path.stem
        current_layer = hierarchy.get(current_module)
        if current_layer is None:
            return violations
        content, unreadable = u.Tests.read_scan_file(file_path, "LAYER-UNREADABLE")
        if content is None:
            return unreadable
        lines = content.splitlines()
        for line_number, line in enumerate(lines, start=1):
            for imported_module in cls._imported_modules(line):
                imported_layer = hierarchy.get(imported_module)
                if imported_layer is not None and imported_layer > current_layer:
                    violation = u.Tests.create_violation(
                        file_path,
                        line_number,
                        "LAYER-001",
                        lines,
                        c.Tests.VALIDATOR_MSG_LAYER_VIOLATION.format(
                            current=current_module,
                            current_level=current_layer,
                            imported=imported_module,
                            imported_level=imported_layer,
                        ),
                    )
                    violations.append(violation)
        return violations

    @classmethod
    def scan(
        cls,
        files: t.SequenceOf[Path],
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
        layer_hierarchy: t.IntMapping | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Scan files for layer violations.

        Args:
            files: List of Python files to scan
            approved_exceptions: Dict mapping rule IDs to list of approved file patterns
            layer_hierarchy: Custom layer hierarchy (module_name -> layer_number)

        Returns:
            r with ScanResult containing all violations found

        """
        hierarchy = layer_hierarchy or u.Tests.layer_dict()
        return u.Tests.validator_run_scan(
            files=files,
            approved_exceptions=approved_exceptions,
            validator_name=c.Tests.VALIDATOR_LAYER_KEY,
            scan_file=lambda fp, ap: cls._scan_file(fp, ap, hierarchy),
        )


__all__: list[str] = ["FlextValidatorLayer"]
