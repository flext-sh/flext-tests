"""Runtime settings namespace for FLEXT test services."""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextSettings
from flext_tests import m


class FlextTestsSettings(FlextSettings):
    """FLEXT settings extended with the test runtime namespace."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_TESTS_",
        extra="ignore",
    )

    class TestsSettings(m.SettingsValue):
        """Namespaced test runtime settings branch."""

    Tests: TestsSettings = m.Field(
        default_factory=TestsSettings,
        description="Namespaced FLEXT tests settings branch.",
    )


__all__: list[str] = ["FlextTestsSettings"]
