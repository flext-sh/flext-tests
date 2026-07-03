"""Settings validation primitives for flext-tests."""

from __future__ import annotations

from collections.abc import MutableSequence
from pathlib import Path

from flext_tests import c, m, t, u


class FlextValidatorSettings:
    """Config validation primitives for FlextTestsValidator."""

    @staticmethod
    def to_toml_value(value: t.JsonValue) -> t.Tests.TomlValue:
        """Project a JsonValue into a TOML-compatible value."""
        if value is None:
            return ""
        if isinstance(value, dict):
            return {
                key: FlextValidatorSettings.to_toml_value(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [FlextValidatorSettings.to_toml_value(item) for item in value]
        return value

    @staticmethod
    def to_toml_dict(mapping: t.JsonMapping) -> t.Tests.TomlDict:
        """Recursively convert a JsonMapping to a TOML-compatible dictionary."""
        return {
            key: FlextValidatorSettings.to_toml_value(value)
            for key, value in mapping.items()
        }

    @classmethod
    def _create_config_violation(
        cls,
        file_path: Path,
        line_number: int,
        rule_id: str,
        code_snippet: str,
        extra_desc: str = "",
    ) -> m.Tests.Violation:
        """Create a settings violation."""
        severity, desc = c.Tests.validator_rule(rule_id)
        description = f"{desc}: {extra_desc}" if extra_desc else desc
        return m.Tests.Violation(
            file_path=file_path,
            line_number=line_number,
            rule_id=rule_id,
            severity=severity,
            description=description,
            code_snippet=code_snippet,
        )

    @classmethod
    def _check_mypy_settings(
        cls,
        file_path: Path,
        data: t.Tests.TomlDict,
        lines: t.StrSequence,
        approved: t.MappingKV[str, t.StrSequence],
    ) -> t.SequenceOf[m.Tests.Violation]:
        """Check mypy configuration for violations."""
        violations: MutableSequence[m.Tests.Violation] = []
        tool_data: t.Tests.TomlValue = data.get("tool", {})
        if not isinstance(tool_data, dict):
            return violations
        mypy_config: t.Tests.TomlValue = tool_data.get("mypy", {})
        if not isinstance(mypy_config, dict):
            return violations
        if (
            not u.Tests.approved("CONFIG-001", file_path, approved)
            and mypy_config.get("ignore_errors") is True
        ):
            line_num = u.Tests.find_line_number(lines, "ignore_errors")
            violations.append(
                cls._create_config_violation(
                    file_path,
                    line_num,
                    "CONFIG-001",
                    "ignore_errors = true",
                    "(global)",
                ),
            )
        overrides_raw: t.Tests.TomlValue = mypy_config.get("overrides", [])
        if not isinstance(overrides_raw, list):
            return violations
        for override in overrides_raw:
            if not isinstance(override, dict):
                continue
            module = str(override.get("module", "unknown"))
            approved_rule = u.Tests.approved("CONFIG-001", file_path, approved)
            ignore_errors_raw: t.Tests.TomlValue = override.get("ignore_errors", False)
            if ignore_errors_raw is True and (not approved_rule):
                line_num = u.Tests.find_line_number(lines, f'module = "{module}"')
                violations.append(
                    cls._create_config_violation(
                        file_path,
                        line_num,
                        "CONFIG-001",
                        f"ignore_errors = true (module: {module})",
                        c.Tests.VALIDATOR_MSG_CONFIG_IGNORE.format(module=module),
                    ),
                )
        for code, key in (
            ("CONFIG-003", "disallow_incomplete_defs"),
            ("CONFIG-004", "warn_return_any"),
        ):
            if (
                not u.Tests.approved(code, file_path, approved)
                and mypy_config.get(key) is False
            ):
                line_num = u.Tests.find_line_number(lines, key)
                violations.append(
                    cls._create_config_violation(
                        file_path,
                        line_num,
                        code,
                        f"{key} = false",
                    ),
                )
        return violations


__all__: list[str] = ["FlextValidatorSettings"]
