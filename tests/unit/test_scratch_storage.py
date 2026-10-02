"""Scratch-storage relocation tests (T6, bead flext-ht1t9.8).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import c


class TestsFlextTestsScratchStorage:
    """Public contract of the scratch-storage relocation plugin."""

    def test_no_hypothesis_directory_inside_the_checkout(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """A hypothesis test leaves .hypothesis/ out of the checkout."""
        pytester.makepyfile(
            test_hyp="""
            import hypothesis
            from hypothesis import given, strategies

            @given(strategies.integers())
            def test_ok(value):
                assert isinstance(value, int)
            """,
        )
        result = pytester.runpytest_subprocess(
            "-p",
            "no:cacheprovider",
            "-p",
            "no:flext_tests_enforcement",
        )
        result.assert_outcomes(passed=1)
        assert not (pytester.path / ".hypothesis").exists()

    def test_benchmark_storage_outside_the_checkout(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """A benchmark run stores under the scratch root, not the checkout."""
        pytester.makepyfile(
            test_bench="""
            def test_perf(benchmark):
                benchmark(lambda: sum(range(100)))
            """,
        )
        result = pytester.runpytest_subprocess(
            "--benchmark-only",
            "-p",
            "no:cacheprovider",
            "-p",
            "no:flext_tests_enforcement",
            "-p",
            "no:randomly",
        )
        result.assert_outcomes(passed=1)
        benchmarks = list(pytester.path.rglob(".benchmarks"))
        assert benchmarks == []

    def test_scratch_root_ini_override(
        self,
        pytester: pytest.Pytester,
        tmp_path: Path,
    ) -> None:
        """The flext_scratch_root ini redirects the storage base."""
        override = tmp_path / "custom-scratch"
        pytester.makepyfile(test_plain="def test_plain():\n    assert True\n")
        result = pytester.runpytest_subprocess(
            "-p",
            "no:cacheprovider",
            "-p",
            "no:flext_tests_enforcement",
            "-o",
            f"{c.Tests.SCRATCH_ROOT_INI}={override}",
        )
        result.assert_outcomes(passed=1)
        assert override.exists()

    def test_scratch_root_utility_keys_by_checkout(
        self,
        tmp_path: Path,
        tmp_path_factory: pytest.TempPathFactory,
    ) -> None:
        """u.Tests.scratch_root keys per checkout and honors the override."""
        from flext_tests import u

        checkout_a = tmp_path_factory.mktemp("checkout-a")
        checkout_b = tmp_path_factory.mktemp("checkout-b")
        override = tmp_path / "custom"
        root_a = u.Tests.scratch_root(checkout_root=checkout_a)
        root_b = u.Tests.scratch_root(checkout_root=checkout_b)
        root_override = u.Tests.scratch_root(
            checkout_root=checkout_a,
            override=str(override),
        )
        assert root_a != root_b
        assert root_override == override / root_a.name
