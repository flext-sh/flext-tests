"""Fail-closed worker-evidence validation for pytest shard manifests."""

from __future__ import annotations

from flext_tests import tm
from flext_tests.sharding import (
    JsonValue,
    WorkerRecord,
    aggregate_workers,
    parse_worker_payload,
    shard_index,
)


class TestsFlextTestsShardManifest:
    """Controller validation never trusts serialized xdist worker payloads."""

    def test_controller_accepts_uneven_disjoint_worker_subsets(self) -> None:
        """Only the controller requires the exact completed external-shard union."""
        full_collection = tuple(
            sorted(f"suite.py::test_case_{index}" for index in range(12))
        )
        shard_count = 3
        external_index = max(
            range(shard_count),
            key=lambda index: sum(
                shard_index(nodeid, shard_count) == index for nodeid in full_collection
            ),
        )
        selected = tuple(
            nodeid
            for nodeid in full_collection
            if shard_index(nodeid, shard_count) == external_index
        )
        records: dict[str, WorkerRecord] = {
            "gw0": (
                full_collection,
                selected,
                dict.fromkeys(selected[:1], "passed"),
                (),
            ),
            "gw1": (
                full_collection,
                selected,
                dict.fromkeys(selected[1:], "passed"),
                (),
            ),
        }

        full, actual_selected, outcomes, errors = aggregate_workers(
            records,
            shard_index_value=external_index,
            shard_count=shard_count,
            observed_workers=2,
            expected_workers=2,
            inherited_errors=(),
        )

        tm.that(full, eq=full_collection)
        tm.that(actual_selected, eq=selected)
        tm.that(tuple(outcomes), eq=selected)
        tm.that(errors, eq=())

    def test_untrusted_payload_rejects_duplicates_and_invalid_outcomes(self) -> None:
        """Malformed worker values cannot become a canonical record."""
        duplicate_payload: JsonValue = {
            "full_collection": ["a", "a"],
            "outcomes": {},
            "selected_nodeids": [],
            "validation_errors": [],
        }
        record, duplicate_errors = parse_worker_payload(duplicate_payload)
        tm.that(record, none=True)
        tm.that(
            any("duplicate nodeids" in error for error in duplicate_errors), eq=True
        )

        invalid_outcome: JsonValue = {
            "full_collection": ["a"],
            "outcomes": {"a": "unknown"},
            "selected_nodeids": ["a"],
            "validation_errors": [],
        }
        record, outcome_errors = parse_worker_payload(invalid_outcome)
        tm.that(record, none=True)
        tm.that(
            any("invalid nodeid or outcome" in error for error in outcome_errors),
            eq=True,
        )

    def test_worker_crash_and_omitted_payload_fail_closed(self) -> None:
        """Observed workers without evidence remain explicit validation failures."""
        full = ("suite.py::test_case",)
        external_index = shard_index(full[0], 2)
        _, _, _, errors = aggregate_workers(
            {"gw0": (full, full, {"suite.py::test_case": "passed"}, ())},
            shard_index_value=external_index,
            shard_count=2,
            observed_workers=2,
            expected_workers=2,
            inherited_errors=("xdist worker gw1 failed: crash",),
        )

        tm.that(any("omitted shard evidence" in error for error in errors), eq=True)
        tm.that("xdist worker gw1 failed: crash" in errors, eq=True)


__all__: list[str] = []
