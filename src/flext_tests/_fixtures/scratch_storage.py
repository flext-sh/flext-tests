"""Scratch-storage class plugin for flext_tests (T6).

Storage law: caches never live inside the checkout. Hypothesis and benchmark
storage use the checkout-keyed host scratch root.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest
from hypothesis.configuration import set_hypothesis_home_dir

from flext_tests import c
from flext_tests._utilities import FlextTestsScratchStorageUtilitiesMixin


class FlextTestsScratchStoragePlugin:
    """Native hooks retaining the canonical scratch-storage configuration."""

    @staticmethod
    def _scratch_root(config: pytest.Config) -> Path:
        """Resolve storage through its pure owner, not the composed facade.

        Returns:
            Path: The resolved scratch root for this checkout.

        """
        return FlextTestsScratchStorageUtilitiesMixin.scratch_root(
            checkout_root=Path(config.rootpath),
            override=config.getini(c.Tests.SCRATCH_ROOT_INI) or None,
        )

    @staticmethod
    def pytest_configure(config: pytest.Config) -> None:
        """Relocate hypothesis/benchmark storage under the scratch root."""
        scratch = FlextTestsScratchStoragePlugin._scratch_root(config)
        hypothesis_dir = scratch / "hypothesis"
        hypothesis_dir.mkdir(parents=True, exist_ok=True)
        set_hypothesis_home_dir(hypothesis_dir)
        benchmark_dir = scratch / "benchmarks"
        benchmark_dir.mkdir(parents=True, exist_ok=True)
        config.option.benchmark_storage = str(benchmark_dir)

    @staticmethod
    def pytest_addoption(parser: pytest.Parser) -> None:
        """Declare the scratch-root override (defaults to ~/.flext/scratch)."""
        parser.addini(
            c.Tests.SCRATCH_ROOT_INI,
            default="",
            help="Override the scratch root for hypothesis/benchmark storage.",
        )


__all__: list[str] = ["FlextTestsScratchStoragePlugin"]
