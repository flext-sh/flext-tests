"""Exception for enforcement violations."""

from __future__ import annotations


class FlextTestsEnforcementViolationError(Exception):
    """Raised by ``FlextTestsEnforcementItem.runtest`` when violations are present."""
