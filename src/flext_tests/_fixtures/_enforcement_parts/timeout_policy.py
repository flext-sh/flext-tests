"""Fail-closed pytest timeout policy for the enforcement plugin."""

from __future__ import annotations

import math
import os
import shlex
from typing import TYPE_CHECKING, ClassVar, Never

import pytest

from flext_tests import c, t

if TYPE_CHECKING:
    from flext_tests import p


class PytestTimeoutPolicy:
    """Validate that pytest-timeout cannot be weakened by a test run."""

    _ceiling_key: ClassVar[pytest.StashKey[float]] = pytest.StashKey()
    _policy_key: ClassVar[pytest.StashKey[p.Tests.PytestTimeoutPolicy]] = (
        pytest.StashKey()
    )

    @classmethod
    def configure(
        cls, config: pytest.Config, policy: p.Tests.PytestTimeoutPolicy
    ) -> None:
        """Resolve and validate the configured per-item timeout ceiling."""
        overrides = tuple(
            str(value) for value in config.getoption(c.Tests.PYTEST_OVERRIDE_INI_DEST)
        )
        for override in overrides:
            raw_key = override.partition("=")[0].strip()
            try:
                override_key = c.Tests.PytestTimeoutIniKey(raw_key)
            except ValueError:
                continue
            if override_key in policy.timeout_owned_ini_keys:
                cls._fail(
                    f"-o/--override-ini cannot replace timeout-owned key {override!r}"
                )
        configured_tokens = cls._tokens(config.getini(c.Tests.PYTEST_ADDOPTS_INI))
        configured_values = cls._timeout_values(
            configured_tokens, source="configured addopts"
        )
        if len(configured_values) != policy.required_configured_cap_count:
            cls._fail(
                "configured addopts must define "
                f"{policy.required_configured_cap_count} timeout cap(s)"
            )
        ceiling = cls._positive_seconds(
            configured_values[0], source="configured addopts"
        )
        if not policy.allow_timeout_func_only and bool(
            config.getini(c.Tests.PYTEST_TIMEOUT_FUNC_ONLY_INI)
        ):
            cls._fail("timeout_func_only must remain disabled")
        configured_ini = str(config.getini(c.Tests.PYTEST_TIMEOUT_INI) or "")
        if configured_ini:
            cls._at_most(
                configured_ini, ceiling=ceiling, source="configured timeout ini"
            )
        cls._validate_tokens(
            config.invocation_params.args, ceiling=ceiling, source="pytest CLI"
        )
        cls._validate_tokens(
            cls._tokens(os.environ.get(c.Tests.PYTEST_ADDOPTS_ENV)),
            ceiling=ceiling,
            source="PYTEST_ADDOPTS",
        )
        env_timeout = os.environ.get(c.Tests.PYTEST_TIMEOUT_ENV)
        if env_timeout is not None:
            cls._at_most(env_timeout, ceiling=ceiling, source="PYTEST_TIMEOUT")
        effective = config.getoption(c.Tests.PYTEST_TIMEOUT_INI)
        if effective is not None:
            cls._at_most(effective, ceiling=ceiling, source="effective --timeout")
        config.stash[cls._ceiling_key] = ceiling
        config.stash[cls._policy_key] = policy

    @classmethod
    def validate_items(cls, config: pytest.Config, items: list[pytest.Item]) -> None:
        """Reject item markers that disable or exceed the configured ceiling."""
        ceiling = config.stash.get(cls._ceiling_key, None)
        if ceiling is None:
            cls._fail("timeout policy was not configured")
        policy = config.stash.get(cls._policy_key, None)
        if policy is None:
            cls._fail("typed timeout policy was not configured")
        for item in items:
            for marker in item.iter_markers(name=c.Tests.PYTEST_TIMEOUT_MARKER):
                cls._validate_marker(
                    marker, ceiling=ceiling, nodeid=item.nodeid, policy=policy
                )

    @classmethod
    def _validate_marker(
        cls,
        marker: pytest.Mark,
        *,
        ceiling: float,
        nodeid: str,
        policy: p.Tests.PytestTimeoutPolicy,
    ) -> None:
        if not marker.args and not marker.kwargs:
            cls._fail(f"{nodeid}: timeout marker requires an argument")
        if len(marker.args) > c.Tests.PYTEST_TIMEOUT_MARKER_POSITIONAL_LIMIT:
            cls._fail(f"{nodeid}: timeout marker has too many positional arguments")
        unknown = set(marker.kwargs).difference(
            c.Tests.PYTEST_TIMEOUT_MARKER_ALLOWED_KEYS
        )
        if unknown:
            cls._fail(
                f"{nodeid}: timeout marker has unsupported keys {sorted(unknown)}"
            )
        if marker.args and c.Tests.PYTEST_TIMEOUT_MARKER in marker.kwargs:
            cls._fail(f"{nodeid}: timeout marker defines timeout twice")
        if (
            len(marker.args) > 1
            and c.Tests.PYTEST_TIMEOUT_MARKER_METHOD_KEY in marker.kwargs
        ):
            cls._fail(f"{nodeid}: timeout marker defines method twice")
        timeout = (
            marker.args[0]
            if marker.args
            else marker.kwargs.get(c.Tests.PYTEST_TIMEOUT_MARKER)
        )
        if timeout is not None:
            if isinstance(timeout, bool) or not isinstance(timeout, (str, int, float)):
                cls._fail(f"{nodeid}: timeout marker must be a positive finite number")
            cls._at_most(timeout, ceiling=ceiling, source=f"{nodeid} timeout marker")
        func_only = marker.kwargs.get(c.Tests.PYTEST_TIMEOUT_MARKER_FUNC_ONLY_KEY)
        if func_only is not None and not isinstance(func_only, bool):
            cls._fail(f"{nodeid}: timeout marker func_only must be boolean")
        if func_only and not policy.allow_timeout_func_only:
            cls._fail(f"{nodeid}: timeout marker func_only=True is forbidden")

    @classmethod
    def _validate_tokens(
        cls, tokens: tuple[str, ...], *, ceiling: float, source: str
    ) -> None:
        for value in cls._timeout_values(tokens, source=source):
            cls._at_most(value, ceiling=ceiling, source=source)

    @classmethod
    def _timeout_values(
        cls, tokens: tuple[str, ...], *, source: str
    ) -> tuple[str, ...]:
        values: list[str] = []
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token == c.Tests.PYTEST_TIMEOUT_OPTION:
                index += 1
                if index >= len(tokens):
                    cls._fail(f"{source}: --timeout requires a value")
                values.append(tokens[index])
            elif token.startswith(f"{c.Tests.PYTEST_TIMEOUT_OPTION}="):
                values.append(token.partition("=")[2])
            index += 1
        return tuple(values)

    @staticmethod
    def _tokens(raw: t.Tests.PytestOptionSource) -> tuple[str, ...]:
        if raw is None:
            return ()
        if not isinstance(raw, str):
            return tuple(raw)
        try:
            return tuple(shlex.split(raw))
        except ValueError as exc:
            message = f"invalid pytest option string: {exc}"
            raise pytest.UsageError(message) from exc

    @classmethod
    def _at_most(
        cls, raw: t.Tests.PytestTimeoutValue, *, ceiling: float, source: str
    ) -> None:
        value = cls._positive_seconds(raw, source=source)
        if value > ceiling:
            cls._fail(f"{source}: timeout {value:g}s exceeds policy {ceiling:g}s")

    @classmethod
    def _positive_seconds(
        cls, raw: t.Tests.PytestTimeoutValue, *, source: str
    ) -> float:
        if isinstance(raw, bool):
            cls._fail(f"{source}: timeout must be a positive finite number")
        try:
            value = float(str(raw))
        except ValueError:
            cls._fail(f"{source}: invalid timeout {raw!r}")
        if not math.isfinite(value) or value <= 0:
            cls._fail(f"{source}: timeout must be a positive finite number")
        return value

    @staticmethod
    def _fail(message: str) -> Never:
        detail = f"FLEXT timeout policy: {message}"
        raise pytest.UsageError(detail)


__all__: list[str] = ["PytestTimeoutPolicy"]
