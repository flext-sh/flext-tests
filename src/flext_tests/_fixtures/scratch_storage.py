"""Scratch-storage plugin for flext_tests (T6).

Storage law: caches never live inside the checkout. This plugin relocates
the Hypothesis database and the pytest-benchmark storage under the host
scratch root (``~/.flext/scratch/<checkout-identity>/``), keyed by the
checkout identity so two checkouts never share a database.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import c


def _scratch_root(config: pytest.Config) -> Path:
    """Transport hook: resolve the scratch root through its pure owner.

    The owner mixin is reached directly, not through the composed ``u``
    facade: configuring an ungoverned session must not load the model facade
    that the other utility mixins import.

    Returns:
        The resulting ``Path``.
    """
    from flext_tests._utilities import FlextTestsScratchStorageUtilitiesMixin

    return FlextTestsScratchStorageUtilitiesMixin.scratch_root(
        checkout_root=Path(config.rootpath),
        override=config.getini(c.Tests.SCRATCH_ROOT_INI) or None,
    )


def pytest_configure(config: pytest.Config) -> None:
    """Relocate hypothesis/benchmark storage under the scratch root."""
    from importlib.util import find_spec

    scratch = _scratch_root(config)
    hypothesis_dir = scratch / "hypothesis"
    hypothesis_dir.mkdir(parents=True, exist_ok=True)
    if find_spec("hypothesis") is not None:
        from hypothesis.configuration import set_hypothesis_home_dir

        set_hypothesis_home_dir(hypothesis_dir)
    benchmark_dir = scratch / "benchmarks"
    benchmark_dir.mkdir(parents=True, exist_ok=True)
    config.option.benchmark_storage = str(benchmark_dir)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Declare the scratch-root override (defaults to ~/.flext/scratch)."""
    parser.addini(
        c.Tests.SCRATCH_ROOT_INI,
        default="",
        help="Override the scratch root for hypothesis/benchmark storage.",
    )


__all__: list[str] = ["pytest_addoption", "pytest_configure"]
