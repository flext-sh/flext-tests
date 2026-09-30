"""Unit tests for fail-loud approval-pattern registration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_tests import c
from tests import u

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextTestsValidatorApprovedRegistration:
    """Approved patterns outside the registry must fail loud, never no-op."""

    def test_registered_pattern_matches(self, tmp_path: Path) -> None:
        path = tmp_path / "pkg" / "__init__.py"
        assert u.Tests.approved(
            "IMPORT-001",
            path,
            {"IMPORT-001": (c.Tests.VALIDATOR_APPROVED_PRAGMA_PATTERN,)},
        )

    def test_registered_pattern_non_match_returns_false(self, tmp_path: Path) -> None:
        path = tmp_path / "pkg" / "module.py"
        assert not u.Tests.approved(
            "IMPORT-001",
            path,
            {"IMPORT-001": (c.Tests.VALIDATOR_APPROVED_PRAGMA_PATTERN,)},
        )

    def test_unregistered_pattern_raises_naming_the_key(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="unregistered approved pattern"):
            u.Tests.approved(
                "IMPORT-001",
                tmp_path / "module.py",
                {"IMPORT-001": ("api\\.py$",)},
            )

    def test_mixed_patterns_raise_naming_only_the_unknown(
        self, tmp_path: Path
    ) -> None:
        registered = c.Tests.VALIDATOR_APPROVED_PRAGMA_PATTERN
        with pytest.raises(ValueError, match="api") as excinfo:
            u.Tests.approved(
                "IMPORT-001",
                tmp_path / "module.py",
                {"IMPORT-001": (registered, "api\\.py$")},
            )
        assert registered not in str(excinfo.value)

    def test_extra_patterns_are_validated_too(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="unregistered approved pattern"):
            u.Tests.approved(
                "IMPORT-001",
                tmp_path / "module.py",
                {},
                ("_pptx_builder/_base\\.py$",),
            )

    def test_empty_patterns_approve_nothing(self, tmp_path: Path) -> None:
        assert not u.Tests.approved("IMPORT-001", tmp_path / "module.py", {})
