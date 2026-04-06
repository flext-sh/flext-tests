"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Generator,
)
from contextlib import contextmanager

from flext_tests import (
    t,
)


class FlextTestsTestContextUtilitiesMixin:
    """Context managers for tests."""

    @staticmethod
    @contextmanager
    def temporary_attribute(
        target: t.Tests.Testobject,
        attribute: str,
        value: t.Tests.Testobject,
    ) -> Generator[None]:
        """Temporarily set attribute on target t.NormalizedValue.

        Args:
            target: Object to modify
            attribute: Attribute name
            value: Temporary value

        Yields:
            None

        """
        attribute_existed = hasattr(target, attribute)
        original_value: t.Tests.Testobject | None = None
        if attribute_existed:
            original_value = target.__getattribute__(attribute)
        object.__setattr__(target, attribute, value)
        try:
            yield
        finally:
            if attribute_existed:
                object.__setattr__(target, attribute, original_value)
            else:
                object.__delattr__(target, attribute)
