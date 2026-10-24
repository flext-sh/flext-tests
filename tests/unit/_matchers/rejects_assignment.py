"""Immutability matcher tests: assignment rejection on frozen and enum surfaces.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import enum
import re

import pytest

from tests import m, tm


class TestsFlextTestsFrozen(m.BaseModel):
    model_config = m.ConfigDict(frozen=True)

    host: str


class TestsFlextTestsMutable(m.BaseModel):
    host: str


class TestsFlextTestsPluginType(enum.StrEnum):
    EXTRACTORS = "extractors"


class TestsFlextTestsRejectedAssignment:
    """Write-only descriptor target with an identifiable rejection cause."""

    def __init__(self, rejection: ValueError) -> None:
        self.rejection = rejection

    def reject(self, _value: str) -> None:
        """Refuse a write while preserving the supplied rejection instance."""
        raise self.rejection

    host = property(fset=reject)


class TestsFlextTestsMatchersRejectsAssignmentMixin:
    """Cover ``tm.rejects_assignment`` against real frozen and enum surfaces."""

    @staticmethod
    def test_rejects_assignment_on_frozen_model() -> None:
        """A frozen pydantic model rejects field assignment."""
        tm.rejects_assignment(
            TestsFlextTestsFrozen(host="h"),
            "host",
            "other",
            expected=m.ValidationError,
        )

    @staticmethod
    def test_rejects_assignment_matches_error_text() -> None:
        """The rejection reason is assertable through ``match``."""
        tm.rejects_assignment(
            TestsFlextTestsFrozen(host="h"),
            "host",
            "other",
            expected=m.ValidationError,
            match="frozen_instance",
        )

    @staticmethod
    def test_rejects_assignment_on_enum_member() -> None:
        """Enum members cannot be reassigned through the public class."""
        tm.rejects_assignment(
            TestsFlextTestsPluginType,
            "EXTRACTORS",
            "mutated",
            expected=(AttributeError, TypeError),
        )

    @staticmethod
    def test_rejects_assignment_reports_a_mutable_target() -> None:
        """A target that accepts the assignment fails the test (pytest outcome)."""
        with pytest.raises(pytest.fail.Exception):
            tm.rejects_assignment(
                TestsFlextTestsMutable(host="h"),
                "host",
                "other",
                expected=m.ValidationError,
            )

    @staticmethod
    def test_rejects_assignment_propagates_unexpected_exception_identity() -> None:
        """An unexpected descriptor error escapes without normalization."""
        rejection = ValueError("assignment rejected")

        with pytest.raises(ValueError, match=re.escape(str(rejection))) as caught:
            tm.rejects_assignment(
                TestsFlextTestsRejectedAssignment(rejection),
                "host",
                "other",
                expected=TypeError,
            )

        tm.ok(caught.value is rejection)

    @staticmethod
    def test_rejects_assignment_keeps_original_on_regex_mismatch() -> None:
        """A mismatched rejection message keeps the original as its context."""
        rejection = ValueError("assignment rejected")

        with pytest.raises(AssertionError) as caught:
            tm.rejects_assignment(
                TestsFlextTestsRejectedAssignment(rejection),
                "host",
                "other",
                expected=ValueError,
                match="^a different rejection$",
            )

        tm.ok(caught.value.__context__ is rejection)
