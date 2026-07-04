"""Settings validation scanning for flext-tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_cli import u as cli_u
from flext_tests import c, m, p, r, t, u
from flext_tests._validator._settings_parts.settings_part_01 import (
    FlextValidatorSettings as FlextValidatorSettingsPart01,
)

if TYPE_CHECKING:
    from collections.abc import MutableSequence
    from pathlib import Path


class FlextValidatorSettings(FlextValidatorSettingsPart01):
    """Config validation methods for FlextTestsValidator."""

    @classmethod
    def _check_pyright_settings(
        cls,
        file_path: Path,
        data: t.Tests.TomlDict,
        lines: t.StrSequence,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Check pyright configuration for violations."""
        tool_data: t.Tests.TomlValue = data.get("tool", {})
        if not isinstance(tool_data, dict):
            return []
        pyright_config: t.Tests.TomlValue = tool_data.get("pyright", {})
        if not isinstance(pyright_config, dict):
            return []
        if (
            not u.Tests.approved("CONFIG-005", file_path, approved)
            and pyright_config.get("reportPrivateUsage") is False
        ):
            line_num = u.Tests.find_line_number(lines, "reportPrivateUsage")
            return [
                cls._create_config_violation(
                    file_path,
                    line_num,
                    "CONFIG-005",
                    "reportPrivateUsage = false",
                ),
            ]
        return []

    @classmethod
    def _scan_file(
        cls,
        file_path: Path,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Scan a single pyproject.toml for settings violations."""
        violations: MutableSequence[m.Tests.Violation] = []
        read = u.Cli.files_read_text(file_path)
        if read.failure:
            return [
                u.Tests.create_violation(
                    file_path,
                    0,
                    "CONFIG-UNREADABLE",
                    (),
                    read.error or "could not read file",
                ),
            ]
        content = read.value
        mapping = cli_u.Cli.toml_mapping_from_text(content)
        if mapping is None:
            return [
                u.Tests.create_violation(
                    file_path,
                    0,
                    "CONFIG-INVALID-TOML",
                    (),
                    "invalid TOML - could not parse pyproject",
                ),
            ]
        data = cls.to_toml_dict(mapping)
        lines = content.splitlines()
        violations.extend(cls._check_mypy_settings(file_path, data, lines, approved))
        violations.extend(cls._check_pyright_settings(file_path, data, lines, approved))
        return violations

    @classmethod
    def scan(
        cls,
        files: t.SequenceOf[Path],
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Scan pyproject.toml files for settings violations."""
        violations: MutableSequence[m.Tests.Violation] = []
        approved = approved_exceptions or {}
        for file_path in files:
            if file_path.name != "pyproject.toml":
                continue
            file_violations = cls._scan_file(file_path, approved)
            violations.extend(file_violations)
        return r[m.Tests.ScanResult].ok(
            m.Tests.ScanResult.create(
                validator_name=c.Tests.VALIDATOR_CONFIG_KEY,
                files_scanned=len(files),
                violations=violations,
            ),
        )

    @classmethod
    def validate(
        cls,
        pyproject_path: Path,
        approved_exceptions: t.MappingKV[str, t.StrSequence] | None = None,
    ) -> p.Result[m.Tests.ScanResult]:
        """Validate a single pyproject.toml file."""
        return cls.scan([pyproject_path], approved_exceptions)


__all__: list[str] = ["FlextValidatorSettings"]
