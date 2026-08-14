"""Immutability matcher tests: assignment rejection on frozen and enum surfaces."""

from __future__ import annotations

import enum

import pytest
from pydantic import BaseModel, ConfigDict, ValidationError

from flext_tests import tm


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True)

    host: str


class _Mutable(BaseModel):
    host: str


class _PluginType(enum.StrEnum):
    EXTRACTORS = "extractors"


class MatchersRejectsAssignmentMixin:
    """Cover ``tm.rejects_assignment`` against real frozen and enum surfaces."""

    def test_rejects_assignment_on_frozen_model(self) -> None:
        """A frozen pydantic model rejects field assignment."""
        tm.rejects_assignment(
            _Frozen(host="h"), "host", "other", expected=ValidationError
        )

    def test_rejects_assignment_matches_error_text(self) -> None:
        """The rejection reason is assertable through ``match``."""
        tm.rejects_assignment(
            _Frozen(host="h"),
            "host",
            "other",
            expected=ValidationError,
            match="frozen_instance",
        )

    def test_rejects_assignment_on_enum_member(self) -> None:
        """Enum members cannot be reassigned through the public class."""
        tm.rejects_assignment(
            _PluginType, "EXTRACTORS", "mutated", expected=(AttributeError, TypeError)
        )

    def test_rejects_assignment_reports_a_mutable_target(self) -> None:
        """A target that accepts the assignment fails the matcher."""
        with pytest.raises(AssertionError):
            tm.rejects_assignment(
                _Mutable(host="h"), "host", "other", expected=ValidationError
            )
