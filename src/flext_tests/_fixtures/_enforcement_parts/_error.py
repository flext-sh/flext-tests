"""Private exception for enforcement violations."""

from __future__ import annotations


class _EnforcementViolationError(Exception):
    """Raised by ``FlextTestsEnforcementItem.runtest`` when violations are present."""