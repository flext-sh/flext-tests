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

from flext_tests import c, t
from flext_tests._utilities import FlextTestsUtilitiesScratchStorage


class FlextTestsScratchStoragePlugin:
    """Native hooks retaining the canonical scratch-storage configuration."""

    @staticmethod
    def _scratch_root(config: t.Tests.Config) -> Path:
        """Resolve storage once, before any session isolates its environment.

        The xdist controller resolves through the pure owner; each worker
        adopts the controller's root, so every worker and every run of the
        checkout share one persistent storage area.

        Returns:
            Path: The resolved scratch root for this checkout.

        """
        worker_input = getattr(config, "workerinput", None)
        if worker_input is not None:
            return Path(worker_input[c.Tests.SCRATCH_ROOT_WORKERINPUT_KEY])
        return FlextTestsUtilitiesScratchStorage.scratch_root(
            checkout_root=Path(config.rootpath),
            override=config.getini(c.Tests.SCRATCH_ROOT_INI) or None,
        )

    @staticmethod
    @pytest.hookimpl(optionalhook=True)
    def pytest_configure_node(node: t.Tests.WorkerController) -> None:
        """Hand the controller's pre-isolation scratch root to one xdist worker."""
        node.workerinput[c.Tests.SCRATCH_ROOT_WORKERINPUT_KEY] = str(
            FlextTestsScratchStoragePlugin._scratch_root(node.config),
        )

    @pytest.fixture(scope="session")
    @staticmethod
    def scratch_root(request: t.Tests.FixtureRequest) -> Path:
        """Provide the persistent scratch root shared by every worker and run.

        Returns:
            Path: The scratch root the controller resolved before isolation.

        """
        return FlextTestsScratchStoragePlugin._scratch_root(request.config)

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
