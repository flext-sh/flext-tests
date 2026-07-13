"""Universal matcher declarative rule helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_core import u
from flext_tests import c, m, p, t
from flext_tests._utilities._matchers._that_parts.that_part_04 import (
    FlextTestsMatchersThatMixin as FlextTestsMatchersThatMixinPart04,
)
from flext_tests._utilities.payload import FlextTestsPayloadUtilities


class FlextTestsMatchersThatMixin(FlextTestsMatchersThatMixinPart04):
    """Declarative rule helpers for the universal matcher."""

    @staticmethod
    def _rule_kwargs(
        rule: t.Tests.MatchRuleSpec,
    ) -> dict[str, t.Tests.MatcherKwargValue]:
        if isinstance(rule, Mapping):
            raw_mapping = dict(rule)
            matcher_rule_keys = frozenset(
                alias
                for model in (m.Tests.ThatParams, m.Tests.OkParams, m.Tests.FailParams)
                for field_name, field_info in model.model_fields.items()
                for alias in (
                    field_name,
                    *(
                        candidate
                        for candidate in getattr(
                            field_info.validation_alias,
                            "choices",
                            (),
                        )
                        if isinstance(candidate, str)
                    ),
                )
            )
            if raw_mapping and set(raw_mapping).issubset(matcher_rule_keys):
                return dict(raw_mapping)
            return {"eq": FlextTestsPayloadUtilities.to_payload(rule)}
        if isinstance(rule, type) or (
            isinstance(rule, tuple) and all(isinstance(item, type) for item in rule)
        ):
            return {"is_": rule}
        if callable(rule):
            return {"where": rule}
        return {"eq": rule}

    @classmethod
    def _apply_rule(
        cls,
        subject: t.Tests.TestobjectSerializable | m.BaseModel | p.AttributeProbe,
        rule: t.Tests.MatchRuleSpec,
        *,
        inherited_msg: str | None = None,
    ) -> None:
        kwargs = cls._rule_kwargs(rule)
        if inherited_msg is not None and "msg" not in kwargs:
            kwargs["msg"] = inherited_msg
        if not hasattr(cls.Tests.Matchers, "that"):
            message = "Matcher rule runner missing"
            raise AssertionError(message)
        cls.Tests.Matchers.that(subject, **kwargs)

    @staticmethod
    def _extract_path_value(
        subject: t.Tests.TestobjectSerializable
        | m.BaseModel
        | t.MappingKV[str, t.Tests.TestobjectSerializable],
        path: str,
    ) -> t.Tests.TestobjectSerializable:
        if not isinstance(subject, (m.BaseModel, Mapping)):
            raise AssertionError(
                f"Path assertions require dict or model, got {type(subject).__name__}",
            )
        extracted = u.extract(FlextTestsPayloadUtilities.to_config_map(subject), path)
        if extracted.failure:
            raise AssertionError(
                c.Tests.ERR_SCOPE_PATH_NOT_FOUND.format(
                    path=path,
                    error=extracted.error,
                ),
            )
        return FlextTestsPayloadUtilities.to_payload(extracted.value)

    @classmethod
    def apply_path_rules(
        cls,
        subject: t.Tests.TestobjectSerializable
        | m.BaseModel
        | t.MappingKV[str, t.Tests.TestobjectSerializable],
        rules: t.Tests.PathMatchSpec,
        *,
        inherited_msg: str | None = None,
    ) -> None:
        for path, rule in rules.items():
            try:
                cls._apply_rule(
                    cls._extract_path_value(subject, path),
                    rule,
                    inherited_msg=inherited_msg,
                )
            except AssertionError as exc:
                raise AssertionError(
                    inherited_msg or f"Path rule '{path}' failed: {exc}",
                ) from exc

    @classmethod
    def apply_item_rules(
        cls,
        subject: t.Tests.TestobjectSerializable
        | t.SequenceOf[t.Tests.TestobjectSerializable],
        rules: t.Tests.ItemMatchSpec,
        *,
        inherited_msg: str | None = None,
    ) -> None:
        if not isinstance(subject, Sequence) or isinstance(subject, t.STR_BINARY_TYPES):
            raise AssertionError(
                inherited_msg
                or f"Item assertions require a sequence, got {type(subject).__name__}",
            )
        sequence_value = list(subject)
        if isinstance(rules, Sequence) and not isinstance(rules, t.STR_BINARY_TYPES):
            for index, rule in enumerate(rules):
                cls._apply_rule(
                    sequence_value[index],
                    rule,
                    inherited_msg=inherited_msg,
                )
            return
        if not isinstance(rules, Mapping):
            raise AssertionError(
                inherited_msg
                or "Item assertions must be a sequence or selector mapping",
            )
        for selector, rule in rules.items():
            if selector in {"*", "all"}:
                for item in sequence_value:
                    cls._apply_rule(item, rule, inherited_msg=inherited_msg)
                continue
            target_index = (
                0
                if selector == "first"
                else -1
                if selector == "last"
                else int(selector)
            )
            cls._apply_rule(
                sequence_value[target_index],
                rule,
                inherited_msg=inherited_msg,
            )

    @staticmethod
    def _resolve_attribute_path(
        subject: p.AttributeProbe,
        attr_path: str,
    ) -> p.AttributeProbe:
        current: p.AttributeProbe = subject
        for segment in attr_path.split("."):
            if isinstance(current, Mapping) and segment in current:
                current = current[segment]
                continue
            if not hasattr(current, segment):
                raise AssertionError(f"Object missing attribute path: {attr_path}")
            current = getattr(current, segment)
        return current

    @classmethod
    def apply_attribute_rules(
        cls,
        subject: p.AttributeProbe,
        rules: t.Tests.AttributeMatchSpec,
        *,
        inherited_msg: str | None = None,
    ) -> None:
        for attr_path, rule in rules.items():
            try:
                cls._apply_rule(
                    FlextTestsPayloadUtilities.to_payload(
                        cls._resolve_attribute_path(subject, attr_path),
                    ),
                    rule,
                    inherited_msg=inherited_msg,
                )
            except AssertionError as exc:
                raise AssertionError(
                    inherited_msg or f"Attribute rule '{attr_path}' failed: {exc}",
                ) from exc


__all__: list[str] = ["FlextTestsMatchersThatMixin"]
