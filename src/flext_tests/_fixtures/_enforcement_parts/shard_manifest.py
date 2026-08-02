"""Deterministic pytest shard assignment and manifest persistence."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Literal

type ShardOutcome = Literal[
    "passed", "failed", "skipped", "xfailed", "xpassed", "error"
]
type JsonValue = (
    bool | int | float | str | list[JsonValue] | dict[str, JsonValue] | None
)
type ShardSpec = tuple[int, int, int, Literal["sha256-mod-v1"], Path]
type WorkerRecord = tuple[
    tuple[str, ...], tuple[str, ...], dict[str, ShardOutcome], tuple[str, ...]
]

ASSIGNMENT: Literal["sha256-mod-v1"] = "sha256-mod-v1"
SCHEMA_VERSION = 1
_OUTCOMES: dict[str, ShardOutcome] = {
    "error": "error",
    "failed": "failed",
    "passed": "passed",
    "skipped": "skipped",
    "xfailed": "xfailed",
    "xpassed": "xpassed",
}
_WORKER_KEYS: frozenset[str] = frozenset({
    "full_collection",
    "selected_nodeids",
    "outcomes",
    "validation_errors",
})


def shard_index(nodeid: str, shard_count: int) -> int:
    """Return the stable external shard for one canonical pytest nodeid."""
    digest = hashlib.sha256(nodeid.encode("utf-8")).hexdigest()
    return int(digest, 16) % shard_count


def parse_worker_payload(
    value: JsonValue,
) -> tuple[WorkerRecord | None, tuple[str, ...]]:
    """Parse one untrusted xdist payload once into the canonical worker record."""
    if not isinstance(value, dict):
        return None, ("worker payload is not a JSON mapping",)
    if frozenset(value) != _WORKER_KEYS:
        return None, ("worker payload fields differ from schema v1",)
    raw_full = value["full_collection"]
    raw_selected = value["selected_nodeids"]
    raw_outcomes = value["outcomes"]
    raw_errors = value["validation_errors"]
    if not isinstance(raw_full, list) or not all(
        isinstance(nodeid, str) and nodeid for nodeid in raw_full
    ):
        return None, ("worker full collection is not a non-empty-string list",)
    if not isinstance(raw_selected, list) or not all(
        isinstance(nodeid, str) and nodeid for nodeid in raw_selected
    ):
        return None, ("worker selection is not a non-empty-string list",)
    full_collection = tuple(nodeid for nodeid in raw_full if isinstance(nodeid, str))
    selected_nodeids = tuple(
        nodeid for nodeid in raw_selected if isinstance(nodeid, str)
    )
    if full_collection != tuple(sorted(full_collection)):
        return None, ("worker full collection is not canonically sorted",)
    if selected_nodeids != tuple(sorted(selected_nodeids)):
        return None, ("worker selection is not canonically sorted",)
    if len(full_collection) != len(frozenset(full_collection)):
        return None, ("worker full collection contains duplicate nodeids",)
    if len(selected_nodeids) != len(frozenset(selected_nodeids)):
        return None, ("worker selection contains duplicate nodeids",)
    if not isinstance(raw_outcomes, dict) or not all(
        isinstance(nodeid, str)
        and nodeid
        and isinstance(outcome, str)
        and outcome in _OUTCOMES
        for nodeid, outcome in raw_outcomes.items()
    ):
        return None, ("worker outcomes contain an invalid nodeid or outcome",)
    if not isinstance(raw_errors, list) or not all(
        isinstance(error, str) and error for error in raw_errors
    ):
        return None, ("worker validation errors are not a non-empty-string list",)
    outcomes = {
        nodeid: _OUTCOMES[outcome]
        for nodeid, outcome in raw_outcomes.items()
        if isinstance(outcome, str) and outcome in _OUTCOMES
    }
    errors = tuple(error for error in raw_errors if isinstance(error, str))
    return ((full_collection, selected_nodeids, outcomes, errors), ())


def aggregate_workers(
    records: dict[str, WorkerRecord],
    *,
    shard_index_value: int,
    shard_count: int,
    observed_workers: int,
    expected_workers: int,
    inherited_errors: tuple[str, ...],
) -> tuple[tuple[str, ...], tuple[str, ...], dict[str, ShardOutcome], tuple[str, ...]]:
    """Validate worker collections and aggregate their disjoint outcomes."""
    errors = list(inherited_errors)
    if observed_workers != expected_workers:
        errors.append(
            f"observed {observed_workers} xdist workers, expected {expected_workers}"
        )
    ordered_records = tuple(records[key] for key in sorted(records))
    if len(ordered_records) != observed_workers:
        errors.append("one or more xdist workers omitted shard evidence")
    full_collection = ordered_records[0][0] if ordered_records else ()
    selected_nodeids = ordered_records[0][1] if ordered_records else ()
    if not full_collection:
        errors.append("complete pytest collection is empty")
    if full_collection != tuple(sorted(full_collection)):
        errors.append("complete pytest collection is not canonically sorted")
    if len(full_collection) != len(frozenset(full_collection)):
        errors.append("complete pytest collection contains duplicate nodeids")
    expected_selected = tuple(
        nodeid
        for nodeid in full_collection
        if shard_index(nodeid, shard_count) == shard_index_value
    )
    if selected_nodeids != expected_selected:
        errors.append("selected nodeids differ from sha256-mod-v1 assignment")
    outcomes: dict[str, ShardOutcome] = {}
    for full, selected, worker_outcomes, worker_errors in ordered_records:
        errors.extend(worker_errors)
        if full != full_collection:
            errors.append("xdist workers collected different nodeid sets")
        if selected != selected_nodeids:
            errors.append("xdist workers selected different nodeid sets")
        if frozenset(worker_outcomes).difference(selected):
            errors.append("worker outcomes contain nodeids outside its selection")
        for nodeid, outcome in worker_outcomes.items():
            if nodeid in outcomes:
                errors.append(f"nodeid executed more than once: {nodeid}")
            else:
                outcomes[nodeid] = outcome
    completed_nodeids = tuple(sorted(outcomes))
    if completed_nodeids != selected_nodeids:
        errors.append("completed nodeids differ from selected nodeids")
    return (
        full_collection,
        selected_nodeids,
        {nodeid: outcomes[nodeid] for nodeid in completed_nodeids},
        tuple(sorted(frozenset(errors))),
    )


def write_manifest(
    spec: ShardSpec,
    *,
    worker_count: int,
    full_collection: tuple[str, ...],
    selected_nodeids: tuple[str, ...],
    outcomes: dict[str, ShardOutcome],
    validation_errors: tuple[str, ...],
) -> None:
    """Atomically replace one schema-v1 shard manifest."""
    shard_count, shard_index_value, max_workers, assignment, manifest = spec
    manifest.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "assignment": assignment,
        "completed_nodeids": list(outcomes),
        "full_collection": list(full_collection),
        "max_workers": max_workers,
        "outcomes": outcomes,
        "schema_version": SCHEMA_VERSION,
        "selected_nodeids": list(selected_nodeids),
        "shard_count": shard_count,
        "shard_index": shard_index_value,
        "validation_errors": list(validation_errors),
        "worker_count": worker_count,
    }
    temporary_name = ""
    try:
        with NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=manifest.parent,
            prefix=f".{manifest.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_name = temporary.name
        Path(temporary_name).replace(manifest)
    finally:
        temporary_path = Path(temporary_name)
        if temporary_name and temporary_path.exists():
            temporary_path.unlink()


__all__: list[str] = [
    "ASSIGNMENT",
    "JsonValue",
    "ShardOutcome",
    "ShardSpec",
    "WorkerRecord",
    "aggregate_workers",
    "parse_worker_payload",
    "shard_index",
    "write_manifest",
]
