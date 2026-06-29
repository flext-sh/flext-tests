"""Public config validator facade for flext-tests."""

from __future__ import annotations

from flext_tests._validator._settings_parts.settings_part_02 import (
    FlextValidatorSettings as FlextValidatorSettingsPart02,
)


class FlextValidatorSettings(FlextValidatorSettingsPart02):
    """Config validation facade for FlextTestsValidator."""


__all__: list[str] = ["FlextValidatorSettings"]
