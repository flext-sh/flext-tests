"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    MutableSequence,
    Sequence,
)

from flext_core import r
from flext_tests import c, p, t


class FlextTestsDomainHelpersUtilitiesMixin:
    """Helpers for domain model testing."""

    @staticmethod
    def create_test_entities_batch[TEntity](
        names: t.StrSequence,
        values: t.SequenceOf[t.Tests.TestobjectSerializable],
        entity_class: p.Tests.EntityFactory[TEntity],
        remove_ids: t.SequenceOf[bool] | None = None,
    ) -> p.Result[Sequence[TEntity]]:
        """Create batch of test entities.

        Args:
            names: List of entity names
            values: List of entity values
            entity_class: Entity class to instantiate
            remove_ids: List of booleans for ID removal

        Returns:
            r[Sequence[TEntity]]: Result containing list of entities or error

        """
        ids_removal = remove_ids or [False] * len(names)
        entities: MutableSequence[TEntity] = []
        for name, value, remove_id in zip(
            names,
            values,
            ids_removal,
            strict=True,
        ):
            try:
                entity: TEntity = entity_class(name=name, value=value)
                if remove_id and hasattr(entity, "unique_id"):
                    attr_name = "unique_id"
                    delattr(entity, attr_name)
                entities.append(entity)
            except c.EXC_ATTR_RUNTIME_TYPE as e:
                return r[Sequence[TEntity]].fail(
                    f"Failed to create entity {name}: {e}",
                )
        return r[Sequence[TEntity]].ok(entities)

    @staticmethod
    def create_test_value_objects_batch[TValue](
        data_list: t.StrSequence,
        count_list: t.SequenceOf[int],
        value_class: p.Tests.ValueFactory[TValue],
    ) -> t.SequenceOf[TValue]:
        """Create batch of test value objects.

        Args:
            data_list: List of data values
            count_list: List of count values
            value_class: Value object class to instantiate

        Returns:
            r[TEntity]: Result containing created entity or error
            List of created value objects

        """
        return [
            value_class(data=data, count=count)
            for data, count in zip(data_list, count_list, strict=True)
        ]
