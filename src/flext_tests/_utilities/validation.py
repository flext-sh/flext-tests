"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Callable,
    Sequence,
)

from flext_tests import (
    r,
)


class FlextTestsValidationUtilitiesMixin:
    """Validation helpers for tests - extends FlextCliUtilities.Validation."""

    @staticmethod
    def validate_pipeline(
        value: str,
        validators: Sequence[Callable[[str], r[bool]]],
    ) -> r[bool]:
        """Execute validation pipeline with multiple validators.

        Runs validators sequentially. If any validator fails, returns that failure.
        If all validators succeed, returns success.

        Args:
            value: Value to validate
            validators: List of validator functions, each returns r[bool]

        Returns:
            r[bool]: Success if all validators pass, failure from first failure

        """
        for validator in validators:
            try:
                result = validator(value)
                if result.is_failure:
                    return result
                if result.value is False:
                    return r[bool].fail("Validator must return r[bool].ok(True)")
            except TypeError as e:
                return r[bool].fail(f"Validator failed: {e}")
            except (ValueError, AttributeError, RuntimeError) as e:
                return r[bool].fail(str(e))
        return r[bool].ok(value=True)
