"""Black-box contract for deterministic pytest11 shard execution."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_tests import tm
from flext_tests.sharding import ShardSessionState
from tests.fixtures.pytest_shard import PytestShardRunner

if TYPE_CHECKING:
    from pathlib import Path


class TestsFlextTestsShardPlugin:
    """The installed flext-tests pytest11 plugin owns shard production."""

    def test_installed_plugin_writes_exact_schema_v1_manifest(
        self, pytester: pytest.Pytester
    ) -> None:
        """Real xdist execution records one exact deterministic bucket."""
        PytestShardRunner.write_cases(pytester)
        manifest = pytester.path / "shard-1.json"
        result = PytestShardRunner.run(
            pytester, shard_count=3, shard_index=1, max_workers=2, manifest=manifest
        )

        tm.that(result.ret, eq=pytest.ExitCode.OK)
        payload = PytestShardRunner.manifest(manifest)
        full_collection = PytestShardRunner.nodeids()
        selected = tuple(
            nodeid
            for nodeid in full_collection
            if PytestShardRunner.index(nodeid, 3) == 1
        )
        tm.that(payload["schema_version"], eq=1)
        tm.that(payload["assignment"], eq="sha256-mod-v1")
        tm.that(payload["worker_count"], eq=2)
        tm.that(payload["full_collection"], eq=list(full_collection))
        tm.that(payload["selected_nodeids"], eq=list(selected))
        tm.that(payload["completed_nodeids"], eq=list(selected))
        tm.that(payload["outcomes"], eq=dict.fromkeys(selected, "passed"))
        tm.that(payload["validation_errors"], eq=[])
        tm.that(tuple(manifest.parent.glob(f".{manifest.name}.*.tmp")), eq=())

    def test_arbitrary_count_accepts_a_valid_empty_bucket(
        self, pytester: pytest.Pytester
    ) -> None:
        """An empty external bucket still starts every worker and exits green."""
        pytester.makepyfile(test_only="def test_only() -> None:\n    pass\n")
        nodeid = "test_only.py::test_only"
        shard_count = 17
        occupied_index = PytestShardRunner.index(nodeid, shard_count)
        empty_index = next(
            index for index in range(shard_count) if index != occupied_index
        )
        manifest = pytester.path / f"shard-{empty_index}.json"
        result = PytestShardRunner.run(
            pytester,
            shard_count=shard_count,
            shard_index=empty_index,
            max_workers=2,
            manifest=manifest,
        )

        tm.that(result.ret, eq=pytest.ExitCode.OK)
        payload = PytestShardRunner.manifest(manifest)
        tm.that(payload["worker_count"], eq=2)
        tm.that(payload["full_collection"], eq=[nodeid])
        tm.that(payload["selected_nodeids"], eq=[])
        tm.that(payload["completed_nodeids"], eq=[])
        tm.that(payload["outcomes"], eq={})
        tm.that(payload["validation_errors"], eq=[])

    def test_fixed_worker_contract_fails_before_execution(
        self, pytester: pytest.Pytester
    ) -> None:
        """The declared worker ceiling must equal xdist's concrete count."""
        pytester.makepyfile(test_only="def test_only() -> None:\n    pass\n")
        manifest = pytester.path / "shard-0.json"
        arguments = (
            "-p",
            "xdist.plugin",
            "-p",
            "flext_tests.conftest_plugin",
            "-n",
            "1",
            "--dist=worksteal",
            "--flext-shard-count=2",
            "--flext-shard-index=0",
            "--flext-shard-max-workers=2",
            "--flext-shard-assignment=sha256-mod-v1",
            f"--flext-shard-manifest={manifest}",
        )
        with PytestShardRunner.autoload_disabled():
            result = pytester.runpytest_subprocess(*arguments, timeout=8)

        tm.that(result.ret, eq=pytest.ExitCode.USAGE_ERROR)
        tm.that(not manifest.exists(), where=bool)
        result.stderr.fnmatch_lines(["*xdist worker count must be the fixed value 2*"])

    def test_teardown_error_overwrites_a_passing_call(
        self, pytester: pytest.Pytester
    ) -> None:
        """Final manifest outcome reflects a teardown failure, not an earlier pass."""
        pytester.makepyfile(
            test_teardown=(
                "import pytest\n\n"
                "@pytest.fixture\n"
                "def resource():\n"
                "    yield\n"
                "    raise RuntimeError('teardown failed')\n\n"
                "def test_case(resource) -> None:\n"
                "    pass\n"
            )
        )
        nodeid = "test_teardown.py::test_case"
        shard_count = 2
        index = PytestShardRunner.index(nodeid, shard_count)
        manifest = pytester.path / f"shard-{index}.json"
        result = PytestShardRunner.run(
            pytester,
            shard_count=shard_count,
            shard_index=index,
            max_workers=2,
            manifest=manifest,
        )

        tm.that(result.ret, eq=pytest.ExitCode.TESTS_FAILED)
        payload = PytestShardRunner.manifest(manifest)
        tm.that(payload["completed_nodeids"], eq=[nodeid])
        tm.that(payload["outcomes"], eq={nodeid: "error"})
        tm.that(payload["validation_errors"], eq=[])

    def test_nested_inprocess_session_restores_outer_config(
        self, pytester: pytest.Pytester, tmp_path: Path
    ) -> None:
        """Nested pytest cannot clobber the parent session's report-hook config."""
        _ = tmp_path
        outer_config = ShardSessionState.config
        pytester.makepyfile(test_nested="def test_nested() -> None:\n    pass\n")
        with PytestShardRunner.autoload_disabled():
            result = pytester.runpytest_inprocess(
                "-p", "flext_tests.conftest_plugin", "-q"
            )

        tm.that(result.ret, eq=pytest.ExitCode.OK)
        tm.that(ShardSessionState.config is outer_config, where=bool)


__all__: list[str] = []
