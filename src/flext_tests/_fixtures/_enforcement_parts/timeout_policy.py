"""Fail-closed pytest timeout policy for the enforcement plugin."""

from __future__ import annotations

import math
import os
import shlex
from typing import ClassVar, Never

import pytest


class PytestTimeoutPolicy:
    """Validate that pytest-timeout cannot be weakened by a test run."""

    _ceiling_key: ClassVar[pytest.StashKey[float]] = pytest.StashKey()
    _marker_positional_limit: ClassVar[int] = 2
    _timeout_option: ClassVar[str] = "--timeout"

    @classmethod
    def configure(cls, config: pytest.Config) -> None:
        """Resolve and validate the configured per-item timeout ceiling."""
        overrides = tuple(str(value) for value in config.getoption("override_ini"))
        if overrides:
            cls._fail("-o/--override-ini is forbidden by the timeout policy")
        configured_tokens = cls._tokens(config.getini("addopts"))
        configured_values = cls._timeout_values(
            configured_tokens, source="configured addopts"
        )
        if len(configured_values) != 1:
            cls._fail("configured addopts must define exactly one --timeout")
        ceiling = cls._positive_seconds(
            configured_values[0], source="configured addopts"
        )
        if bool(config.getini("timeout_func_only")):
            cls._fail("timeout_func_only must remain disabled")
        configured_ini = str(config.getini("timeout") or "")
        if configured_ini:
            cls._at_most(
                configured_ini, ceiling=ceiling, source="configured timeout ini"
            )
        cls._validate_tokens(
            config.invocation_params.args, ceiling=ceiling, source="pytest CLI"
        )
        cls._validate_tokens(
            cls._tokens(os.environ.get("PYTEST_ADDOPTS")),
            ceiling=ceiling,
            source="PYTEST_ADDOPTS",
        )
        env_timeout = os.environ.get("PYTEST_TIMEOUT")
        if env_timeout is not None:
            cls._at_most(env_timeout, ceiling=ceiling, source="PYTEST_TIMEOUT")
        effective = config.getoption("timeout")
        if effective is not None:
            cls._at_most(effective, ceiling=ceiling, source="effective --timeout")
        config.stash[cls._ceiling_key] = ceiling

    @classmethod
    def validate_items(cls, config: pytest.Config, items: list[pytest.Item]) -> None:
        """Reject item markers that disable or exceed the configured ceiling."""
        ceiling = config.stash.get(cls._ceiling_key, None)
        if ceiling is None:
            cls._fail("timeout policy was not configured")
        for item in items:
            for marker in item.iter_markers(name="timeout"):
                cls._validate_marker(marker, ceiling=ceiling, nodeid=item.nodeid)

    @classmethod
    def _validate_marker(
        cls, marker: pytest.Mark, *, ceiling: float, nodeid: str
    ) -> None:
        if not marker.args and not marker.kwargs:
            cls._fail(f"{nodeid}: timeout marker requires an argument")
        if len(marker.args) > cls._marker_positional_limit:
            cls._fail(f"{nodeid}: timeout marker has too many positional arguments")
        known = {"disable_debugger_detection", "func_only", "method", "timeout"}
        unknown = set(marker.kwargs).difference(known)
        if unknown:
            cls._fail(
                f"{nodeid}: timeout marker has unsupported keys {sorted(unknown)}"
            )
        if marker.args and "timeout" in marker.kwargs:
            cls._fail(f"{nodeid}: timeout marker defines timeout twice")
        if len(marker.args) > 1 and "method" in marker.kwargs:
            cls._fail(f"{nodeid}: timeout marker defines method twice")
        timeout = marker.args[0] if marker.args else marker.kwargs.get("timeout")
        if timeout is not None:
            cls._at_most(timeout, ceiling=ceiling, source=f"{nodeid} timeout marker")
        func_only = marker.kwargs.get("func_only")
        if func_only is not None and not isinstance(func_only, bool):
            cls._fail(f"{nodeid}: timeout marker func_only must be boolean")
        if func_only:
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
            if token == cls._timeout_option:
                index += 1
                if index >= len(tokens):
                    cls._fail(f"{source}: --timeout requires a value")
                values.append(tokens[index])
            elif token.startswith(f"{cls._timeout_option}="):
                values.append(token.partition("=")[2])
            index += 1
        return tuple(values)

    @staticmethod
    def _tokens(raw: object) -> tuple[str, ...]:
        if raw is None:
            return ()
        if isinstance(raw, (list, tuple)):
            return tuple(str(value) for value in raw)
        try:
            return tuple(shlex.split(str(raw)))
        except ValueError as exc:
            message = f"invalid pytest option string: {exc}"
            raise pytest.UsageError(message) from exc

    @classmethod
    def _at_most(cls, raw: object, *, ceiling: float, source: str) -> None:
        value = cls._positive_seconds(raw, source=source)
        if value > ceiling:
            cls._fail(f"{source}: timeout {value:g}s exceeds policy {ceiling:g}s")

    @classmethod
    def _positive_seconds(cls, raw: object, *, source: str) -> float:
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
