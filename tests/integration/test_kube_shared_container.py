"""TDD Wave-0 RED contract for the FlextTestsKube Kubernetes facade.

flext-tests ships a Docker facade (``tk`` / ``FlextTestsDocker``) over a
shared-container registry, but has no Kubernetes/kind equivalent yet. These
tests pin the public contract that a later wave must satisfy:

* a ``flext_tests.kube`` module exposing ``FlextTestsKube``, mirroring the
  Docker facade;
* a ``flext-kind-test`` entry in ``c.Tests.SHARED_CONTAINERS`` alongside the
  existing Docker entries.

They MUST fail until that facade and registry entry exist. Imports happen
inside the test bodies so the failures are clean assertion/ModuleNotFound
failures, never collection errors.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib

import pytest

from tests import c, tm


class TestsFlextTestsKubeSharedContainer:
    """Public facade + registry contract for Kubernetes/kind test containers."""

    @pytest.mark.integration
    def test_flext_tests_kube_importable(self) -> None:
        """``flext_tests.kube`` exists and exposes ``FlextTestsKube``.

        RED until the facade module is implemented; fails with
        ``ModuleNotFoundError`` (no ``flext_tests.kube``) or ``AssertionError``
        (module present but class missing).
        """
        mod = importlib.import_module("flext_tests.kube")

        tm.that(hasattr(mod, "FlextTestsKube"), eq=True)

    @pytest.mark.integration
    def test_kind_registered_in_shared_containers(self) -> None:
        """``flext-kind-test`` is registered in the shared-container catalog."""
        tm.that("flext-kind-test" in c.Tests.SHARED_CONTAINERS, eq=True)
