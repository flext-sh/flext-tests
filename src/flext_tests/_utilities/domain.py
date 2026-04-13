"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, RootModel

from flext_cli.utilities import FlextCliUtilities
from flext_core import p, r
from flext_tests import (
    FlextTestsPayloadUtilities,
    FlextTestsProtocols,
    t,
)


class FlextTestsDomainHelpersUtilitiesMixin:
    """Helpers for domain model testing."""

    @staticmethod
    def create_test_entities_batch[TEntity](
        names: t.StrSequence,
        values: Sequence[t.Tests.TestobjectSerializable],
        entity_class: FlextTestsProtocols.Tests.EntityFactory[TEntity],
        remove_ids: Sequence[bool] | None = None,
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
        dh = FlextTestsDomainHelpersUtilitiesMixin
        for name, value, remove_id in zip(
            names,
            values,
            ids_removal,
            strict=True,
        ):
            try:
                entity = dh.create_test_entity_instance(
                    name=name,
                    value=value,
                    entity_class=entity_class,
                    remove_id=remove_id,
                )
                entities.append(entity)
            except (TypeError, ValueError, AttributeError, RuntimeError) as e:
                return r[Sequence[TEntity]].fail(
                    f"Failed to create entity {name}: {e}",
                )
        return r[Sequence[TEntity]].ok(entities)

    @staticmethod
    def create_test_entity_instance[TEntity](
        name: str,
        value: t.Tests.TestobjectSerializable,
        entity_class: FlextTestsProtocols.Tests.EntityFactory[TEntity],
        *,
        remove_id: bool = False,
    ) -> TEntity:
        """Create a test entity instance.

        Args:
            name: Entity name
            value: Entity value
            entity_class: Entity class or factory callable
            remove_id: If True, remove unique_id attribute

        Returns:
            TEntity: Created entity instance

        """
        entity = entity_class(name=name, value=value)
        if remove_id and hasattr(entity, "unique_id"):
            attr_name = "unique_id"
            delattr(entity, attr_name)
        return entity

    @staticmethod
    def create_test_value_object_instance[TValue](
        data: str,
        count: int,
        value_class: FlextTestsProtocols.Tests.ValueFactory[TValue],
    ) -> TValue:
        """Create a test value t.RecursiveContainer instance.

        Args:
            data: Data field value
            count: Count field value
            value_class: Value t.RecursiveContainer class or factory callable

        Returns:
            TValue: Created value t.RecursiveContainer instance

        """
        return value_class(data=data, count=count)

    @staticmethod
    def create_test_value_objects_batch[TValue](
        data_list: t.StrSequence,
        count_list: Sequence[int],
        value_class: FlextTestsProtocols.Tests.ValueFactory[TValue],
    ) -> Sequence[TValue]:
        """Create batch of test value objects.

        Args:
            data_list: List of data values
            count_list: List of count values
            value_class: Value t.RecursiveContainer class to instantiate

        Returns:
            r[TEntity]: Result containing created entity or error
            List of created value objects

        """
        return [
            FlextTestsDomainHelpersUtilitiesMixin.create_test_value_object_instance(
                data=data,
                count=count,
                value_class=value_class,
            )
            for data, count in zip(data_list, count_list, strict=True)
        ]

    @staticmethod
    def execute_domain_operation(
        operation: str,
        input_data: Mapping[str, t.Tests.TestobjectSerializable],
        **kwargs: t.Tests.TestobjectSerializable,
    ) -> t.Tests.TestobjectSerializable:
        """Execute a domain utility operation.

        Args:
            operation: Operation name from FlextCliUtilities
            input_data: Input data dictionary
            **kwargs: Additional arguments

        Returns:
            r[TEntity]: Result containing created entity or error
            Operation result (type depends on operation)

        """
        if not hasattr(FlextCliUtilities, operation):
            msg = f"Unknown operation: {operation}"
            raise ValueError(msg)
        op_method = getattr(FlextCliUtilities, operation)
        if not callable(op_method):
            msg = f"Unknown operation: {operation}"
            raise ValueError(msg)
        all_args = {**input_data, **kwargs}
        result = op_method(**all_args)
        if isinstance(result, RootModel):
            empty_map: MutableMapping[str, t.Tests.TestobjectSerializable] = {}
            return empty_map
        if isinstance(result, (BaseModel, Path)):
            return FlextTestsPayloadUtilities.to_payload(result)
        if isinstance(result, (str, int, float, bool, bytes, datetime)):
            payload_scalar: t.Tests.TestobjectSerializable = result
            return FlextTestsPayloadUtilities.to_payload(payload_scalar)
        if isinstance(result, type):
            return FlextTestsPayloadUtilities.to_payload(result)
        if result is None:
            return FlextTestsPayloadUtilities.to_payload(result)
        return FlextTestsPayloadUtilities.to_payload(str(result))
