"""Universal matcher Result-subject helpers."""

from __future__ import annotations

from flext_tests import c, m, p, r
from flext_tests._utilities._matchers._containment import (
    FlextTestsMatchersContainmentMixin,
)
from flext_tests._utilities._matchers._that_parts.that_part_01 import (
    FlextTestsMatchersThatMixin as FlextTestsMatchersThatMixinPart01,
)


class FlextTestsMatchersThatMixin(FlextTestsMatchersThatMixinPart01):
    """Result-aware subject helpers for universal matchers."""

    class Tests:
        class Matchers(FlextTestsMatchersThatMixinPart01.Tests.Matchers):
            @staticmethod
            def _result_subject(
                subject: p.AttributeProbe,
                params: m.Tests.ThatParams,
            ) -> p.AttributeProbe:
                """Return the value to validate after result-aware unwrapping."""
                if not isinstance(subject, r):
                    return subject
                result_obj = subject
                if params.ok is not None:
                    return FlextTestsMatchersThatMixin.Tests.Matchers._ok_value(
                        result_obj,
                        params,
                    )
                if params.has is not None:
                    err = result_obj.error or ""
                    FlextTestsMatchersContainmentMixin.check_has_lacks(
                        err,
                        params.has,
                        None,
                        params.msg,
                        as_str=True,
                    )
                    return err
                if result_obj.success:
                    return getattr(result_obj, "value", "")
                raise AssertionError(
                    params.msg or c.Tests.ERR_OK_FAILED.format(error=result_obj.error),
                )

            @staticmethod
            def _ok_value(
                result_obj: p.Result[p.AttributeProbe],
                params: m.Tests.ThatParams,
            ) -> p.AttributeProbe:
                """Validate result ok/fail expectation and return success value."""
                if params.ok and not result_obj.success:
                    raise AssertionError(
                        params.msg
                        or c.Tests.ERR_OK_FAILED.format(error=result_obj.error),
                    )
                if not params.ok and result_obj.success:
                    value_str = str(result_obj.value)
                    raise AssertionError(
                        params.msg or c.Tests.ERR_FAIL_EXPECTED.format(value=value_str),
                    )
                return getattr(result_obj, "value", "") if result_obj.success else ""


__all__: list[str] = ["FlextTestsMatchersThatMixin"]
