"""Registry for enforcement plugin contributions across FLEXT packages.

The ``flext_tests`` pytest plugin acts as the central dispatcher for cross-layer
enforcement rules. Other FLEXT packages (``flext-core``, ``flext-infra``) can
contribute their own source kinds and warning categories by registering them here
from their own ``pytest11`` entry-point modules.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from pathlib import Path

    import pytest

    from flext_tests import m, p


class EnforcementBuildContext:
    """Shared context passed to contribution builders."""

    def __init__(
        self,
        *,
        infra_report: p.AttributeProbe | None = None,
        validator_targets: Sequence[Path] = (),
        workspace_root: Path | None = None,
    ) -> None:
        self.infra_report = infra_report
        self.validator_targets = tuple(validator_targets)
        self.workspace_root = workspace_root


class EnforcementContribution:
    """One contribution from an external enforcement pytest plugin."""

    def __init__(
        self,
        *,
        source_kind: str,
        builder: Callable[..., list[pytest.Item]] | None = None,
        configure: Callable[[pytest.Config, m.Tests.EnforcementDispatcherConfig], None]
        | None = None,
        warning_categories: Sequence[type[Warning]] = (),
    ) -> None:
        self.source_kind = source_kind
        self.builder = builder
        self.configure = configure
        self.warning_categories = tuple(warning_categories)


_REGISTRY: dict[str, EnforcementContribution] = {}


def register(name: str, contribution: EnforcementContribution) -> None:
    """Register an enforcement contribution from another FLEXT package."""
    _REGISTRY[name] = contribution


def get(name: str) -> EnforcementContribution | None:
    """Return the contribution registered under ``name`` if any."""
    return _REGISTRY.get(name)


def builders() -> dict[str, EnforcementContribution]:
    """Return all registered contributions keyed by name."""
    return dict(_REGISTRY)


def warning_categories() -> frozenset[type[Warning]]:
    """Return the union of warning categories registered by all contributors."""
    categories: set[type[Warning]] = set()
    for contribution in _REGISTRY.values():
        categories.update(contribution.warning_categories)
    return frozenset(categories)


def builder_for(
    source_kind: str,
) -> EnforcementContribution | None:
    """Return the first contribution matching ``source_kind`` that has a builder."""
    for contribution in _REGISTRY.values():
        if contribution.source_kind == source_kind and contribution.builder is not None:
            return contribution
    return None


def clear() -> None:
    """Clear the registry. Intended for tests only."""
    _REGISTRY.clear()


__all__: list[str] = [
    "EnforcementBuildContext",
    "EnforcementContribution",
    "builder_for",
    "builders",
    "clear",
    "get",
    "register",
    "warning_categories",
]
