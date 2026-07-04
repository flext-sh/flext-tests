"""Universal matcher final dispatcher."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests._utilities._matchers._that_parts.that_part_05 import (
    FlextTestsMatchersThatMixin as FlextTestsMatchersThatMixinPart05,
)
from flext_tests._utilities.payload import FlextTestsPayloadUtilities
from flext_tests.constants import c
from flext_tests.models import m
from flext_tests.typings import t

if TYPE_CHECKING:
    from flext_tests.protocols import p


class FlextTestsMatchersThatMixin(FlextTestsMatchersThatMixinPart05):
    """Final universal matcher dispatcher."""

    class Tests:
        """Container for test utility storages and aliases."""

        class Matchers(FlextTestsMatchersThatMixinPart05.Tests.Matchers):
            """Public universal matcher method."""

            @staticmethod
            def that(
                value: p.AttributeProbe,
                **kwargs: t.Tests.MatcherKwargValue,
            ) -> None:
                """Assert a value against universal matcher constraints."""
                params, raw_eq, raw_ne, raw_has, raw_contains = (
                    FlextTestsMatchersThatMixin.Tests.Matchers._that_params(kwargs)
                )
                FlextTestsMatchersThatMixin.Tests.Matchers._validate_declared_types(
                    value,
                    params,
                )
                if FlextTestsMatchersThatMixin.Tests.Matchers._is_type_only(
                    params,
                    raw_eq,
                    raw_ne,
                ):
                    return
                subject = FlextTestsMatchersThatMixin.Tests.Matchers._result_subject(
                    value,
                    params,
                )
                subject_payload = FlextTestsPayloadUtilities.to_payload(subject)
                FlextTestsMatchersThatMixin.Tests.Matchers._validate_scalar(
                    subject_payload,
                    params,
                    raw_eq,
                    raw_ne,
                    kwargs,
                )
                effective_has = (
                    raw_has
                    if raw_has is not None
                    else raw_contains
                    if raw_contains is not None
                    else params.has
                )
                FlextTestsMatchersThatMixin.Tests.Matchers._validate_common(
                    subject_payload,
                    params,
                    effective_has=effective_has,
                )
                FlextTestsMatchersThatMixin.Tests.Matchers._validate_sequence(
                    subject_payload,
                    params,
                )
                FlextTestsMatchersThatMixin.Tests.Matchers._validate_mapping(
                    subject_payload,
                    params,
                )
                FlextTestsMatchersThatMixin.Tests.Matchers._validate_attrs(
                    subject,
                    params,
                )
                FlextTestsMatchersThatMixin.Tests.Matchers._validate_deep(
                    subject_payload,
                    params,
                )
                FlextTestsMatchersThatMixin.Tests.Matchers._validate_rule_sets(
                    subject,
                    subject_payload,
                    params,
                )

            @staticmethod
            def _validate_deep(
                subject_payload: t.Tests.TestobjectSerializable,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate deep structural constraints."""
                if params.deep is None:
                    return
                if not isinstance(subject_payload, (m.BaseModel, dict)):
                    raise AssertionError(
                        params.msg
                        or f"Deep matching requires dict or model, got {type(subject_payload).__name__}",
                    )
                deep_value = (
                    subject_payload
                    if isinstance(subject_payload, m.BaseModel)
                    else t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER.validate_python(
                        subject_payload,
                    )
                )
                match_result = FlextTestsPayloadUtilities.deep_match(
                    deep_value,
                    params.deep,
                )
                if not match_result.matched:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_DEEP_PATH_FAILED.format(
                            path=match_result.path,
                            reason=match_result.reason,
                        ),
                    )

            @staticmethod
            def _validate_rule_sets(
                subject: p.AttributeProbe,
                subject_payload: t.Tests.TestobjectSerializable,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate path, item, attribute, and predicate rule sets."""
                if params.paths is not None:
                    FlextTestsMatchersThatMixin.apply_path_rules(
                        subject_payload,
                        params.paths,
                        inherited_msg=params.msg,
                    )
                if params.items is not None:
                    FlextTestsMatchersThatMixin.apply_item_rules(
                        subject_payload,
                        params.items,
                        inherited_msg=params.msg,
                    )
                if params.attrs_match is not None:
                    FlextTestsMatchersThatMixin.apply_attribute_rules(
                        subject,
                        params.attrs_match,
                        inherited_msg=params.msg,
                    )
                if params.where is not None and not params.where(subject_payload):
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_PREDICATE_FAILED.format(value=subject_payload),
                    )


__all__: list[str] = ["FlextTestsMatchersThatMixin"]
