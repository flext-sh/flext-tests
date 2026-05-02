"""Rule normalization and path extraction — Group C.

Static methods used internally by ``FlextTestsMatchersUtilities``.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from flext_core.utilities import u
from flext_tests._utilities.payload import FlextTestsPayloadUtilities
from flext_tests.constants import c
from flext_tests.models import m
from flext_tests.protocols import p
from flext_tests.typings import t


class FlextTestsMatchersRulesDispatchMixin:
    """Normalize declarative match rules and extract dotted paths."""

    @staticmethod
    def _matcher_rule_keys() -> frozenset[str]:
        """Return the accepted matcher-rule keys from the canonical param models."""

        def iter_aliases() -> Iterable[str]:
            for model in (m.Tests.ThatParams, m.Tests.OkParams, m.Tests.FailParams):
                for field_name, field_info in model.model_fields.items():
                    yield field_name
                    alias_choices = getattr(field_info.validation_alias, "choices", ())
                    for alias in alias_choices:
                        if isinstance(alias, str):
                            yield alias

        return frozenset(iter_aliases())

    @staticmethod
    def _rule_to_kwargs(
        rule: t.Tests.MatchRuleSpec,
        *,
        inherited_msg: str | None = None,
    ) -> dict[str, t.Tests.MatcherKwargValue]:
        """Normalize one declarative matcher rule into tm.that()-compatible kwargs."""
        kwargs_t = dict[str, t.Tests.MatcherKwargValue]
        result: kwargs_t
        if isinstance(rule, Mapping):
            raw_mapping = dict(rule)
            if raw_mapping and set(raw_mapping).issubset(
                FlextTestsMatchersRulesDispatchMixin._matcher_rule_keys(),
            ):
                result = dict(raw_mapping)
            else:
                result = {"eq": FlextTestsPayloadUtilities.to_payload(rule)}
        elif isinstance(rule, type) or (
            isinstance(rule, tuple) and all(isinstance(item, type) for item in rule)
        ):
            result = {"is_": rule}
        elif callable(rule):
            result = {"where": rule}
        else:
            result = {"eq": rule}
        if inherited_msg is not None and "msg" not in result:
            result["msg"] = inherited_msg
        return result

    @staticmethod
    def _extract_mapping_path(
        value: t.Tests.TestobjectSerializable
        | m.BaseModel
        | t.MappingKV[str, t.Tests.TestobjectSerializable],
        path: str,
    ) -> t.Tests.TestobjectSerializable:
        """Extract one dotted path from a model or mapping using flext-core extract helpers."""
        extract_source: m.ConfigMap
        if isinstance(value, m.BaseModel):
            extract_source = m.ConfigMap.model_validate({
                key: FlextTestsPayloadUtilities.to_config_map_value(
                    FlextTestsPayloadUtilities.to_payload(item),
                )
                for key, item in value.model_dump(mode="python").items()
            })
        elif isinstance(value, Mapping):
            extract_source = m.ConfigMap.model_validate({
                key: FlextTestsPayloadUtilities.to_config_map_value(
                    FlextTestsPayloadUtilities.to_payload(item),
                )
                for key, item in value.items()
            })
        else:
            raise AssertionError(
                f"Path assertions require dict or model, got {type(value).__name__}",
            )
        extracted = u.extract(extract_source, path)
        if extracted.failure:
            raise AssertionError(
                c.Tests.ERR_SCOPE_PATH_NOT_FOUND.format(
                    path=path,
                    error=extracted.error,
                ),
            )
        return FlextTestsPayloadUtilities.to_payload(extracted.value)

    @staticmethod
    def _extract_attribute_path(
        value: p.AttributeProbe, attr_path: str
    ) -> t.Tests.TestobjectSerializable:
        """Extract one dotted attribute path from a runtime object."""
        current: object | t.Tests.TestobjectSerializable = value
        for segment in attr_path.split("."):
            if isinstance(current, Mapping) and segment in current:
                current = current[segment]
                continue
            if not hasattr(current, segment):
                raise AssertionError(f"Object missing attribute path: {attr_path}")
            current = getattr(current, segment)
        return FlextTestsPayloadUtilities.to_payload(current)


__all__: list[str] = ["FlextTestsMatchersRulesDispatchMixin"]
