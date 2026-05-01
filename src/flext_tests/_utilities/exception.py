"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    MutableMapping,
)

from flext_tests._typings.base import FlextTestsBaseTypesMixin
from flext_tests.typings import FlextTestsTypes as t


class FlextTestsExceptionHelpersUtilitiesMixin:
    """Helpers for exception testing."""

    @staticmethod
    def create_metadata_object(
        attributes: t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable],
    ) -> MutableMapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]:
        """Create a metadata t.JsonValue for exceptions.

        Args:
            attributes: Metadata attributes

        Returns:
            r[TEntity]: Result containing created entity or error
            Metadata t.JsonValue with attributes as dict

        """
        return {"attributes": attributes, **attributes}
