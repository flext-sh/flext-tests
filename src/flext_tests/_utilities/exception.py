"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Mapping,
    MutableMapping,
)

from flext_tests import (
    t,
)


class FlextTestsExceptionHelpersUtilitiesMixin:
    """Helpers for exception testing."""

    @staticmethod
    def create_metadata_object(
        attributes: Mapping[str, t.Tests.TestobjectSerializable],
    ) -> MutableMapping[str, t.Tests.TestobjectSerializable]:
        """Create a metadata object for exceptions.

        Args:
            attributes: Metadata attributes

        Returns:
            r[TEntity]: Result containing created entity or error
            Metadata object with attributes as dict

        """
        return {"attributes": attributes, **attributes}
