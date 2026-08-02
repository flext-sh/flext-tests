"""Pytest hooks for deterministic external shard execution."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from flext_tests._fixtures._enforcement_parts.shard_config import (
    ERRORS_KEY,
    FULL_KEY,
    OUTCOMES_KEY,
    PREVIOUS_CONFIG_KEY,
    SEEN_WORKERS_KEY,
    SELECTED_KEY,
    SPEC_KEY,
    WORKERS_KEY,
    WORKER_PAYLOAD_KEY,
    ShardSessionState,
    pytest_addoption,
    pytest_configure,
)
from flext_tests._fixtures._enforcement_parts.shard_manifest import (
    JsonValue,
    aggregate_workers,
    parse_worker_payload,
    shard_index,
    write_manifest,
)

if TYPE_CHECKING:
    from xdist.workermanage import WorkerController


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Sort the full collection and select this external shard exactly."""
    spec = config.stash[SPEC_KEY]
    if spec is None or not hasattr(config, "workerinput"):
        return
    shard_count, index, _, _, _ = spec
    full_collection = tuple(sorted(item.nodeid for item in items))
    config.stash[FULL_KEY] = full_collection
    if len(full_collection) != len(frozenset(full_collection)):
        config.stash[ERRORS_KEY].append("collection contains duplicate nodeids")
        return
    by_nodeid = {item.nodeid: item for item in items}
    selected = tuple(
        nodeid
        for nodeid in full_collection
        if shard_index(nodeid, shard_count) == index
    )
    config.stash[SELECTED_KEY] = selected
    items[:] = [by_nodeid[nodeid] for nodeid in selected]


def pytest_collectreport(report: pytest.CollectReport) -> None:
    """Record collection errors in the worker's fail-closed evidence."""
    config = ShardSessionState.config
    if config is None or not hasattr(config, "workerinput"):
        return
    spec = config.stash.get(SPEC_KEY, None)
    if spec is not None and report.failed:
        config.stash[ERRORS_KEY].append(f"collection error: {report.nodeid}")


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """Record the final semantic outcome for each executed nodeid."""
    config = ShardSessionState.config
    if config is None or not hasattr(config, "workerinput"):
        return
    if config.stash.get(SPEC_KEY, None) is None:
        return
    outcomes = config.stash[OUTCOMES_KEY]
    was_xfail = bool(getattr(report, "wasxfail", False))
    if report.when in {"setup", "teardown"} and report.failed:
        outcomes[report.nodeid] = "error"
    elif report.when == "setup" and report.skipped:
        outcomes[report.nodeid] = "xfailed" if was_xfail else "skipped"
    elif report.when == "call":
        if report.passed:
            outcomes[report.nodeid] = "xpassed" if was_xfail else "passed"
        elif report.skipped:
            outcomes[report.nodeid] = "xfailed" if was_xfail else "skipped"
        else:
            outcomes[report.nodeid] = "failed"


@pytest.hookimpl(optionalhook=True)
def pytest_testnodedown(node: WorkerController, error: str | None) -> None:
    """Collect one worker's serialized shard evidence on the controller."""
    config = node.config
    if config.stash.get(SPEC_KEY, None) is None:
        return
    worker_id = node.workerinput["workerid"]
    config.stash[SEEN_WORKERS_KEY].add(worker_id)
    if error is not None:
        config.stash[ERRORS_KEY].append(f"xdist worker {worker_id} failed: {error}")
    raw_workeroutput: JsonValue = getattr(node, "workeroutput", None)
    raw: JsonValue = (
        raw_workeroutput.get(WORKER_PAYLOAD_KEY)
        if isinstance(raw_workeroutput, dict)
        else None
    )
    record, payload_errors = parse_worker_payload(raw)
    if record is None:
        config.stash[ERRORS_KEY].extend(
            f"xdist worker {worker_id}: {message}" for message in payload_errors
        )
        return
    config.stash[WORKERS_KEY][worker_id] = record


def pytest_sessionstart(session: pytest.Session) -> None:
    """Expose the active process-local config to report-only pytest hooks."""
    session.config.stash[PREVIOUS_CONFIG_KEY] = ShardSessionState.config
    ShardSessionState.config = session.config


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: pytest.ExitCode) -> None:
    """Emit worker evidence or atomically finalize the controller manifest."""
    config = session.config
    spec = config.stash.get(SPEC_KEY, None)
    if spec is None:
        if ShardSessionState.config is config:
            ShardSessionState.config = config.stash.get(PREVIOUS_CONFIG_KEY, None)
        return
    if hasattr(config, "workerinput"):
        selected = config.stash[SELECTED_KEY]
        outcomes = config.stash[OUTCOMES_KEY]
        errors = config.stash[ERRORS_KEY]
        if frozenset(outcomes).difference(selected):
            errors.append("worker outcomes contain nodeids outside its selection")
        full_payload: list[JsonValue] = list(config.stash[FULL_KEY])
        selected_payload: list[JsonValue] = list(selected)
        errors_payload: list[JsonValue] = list(errors)
        outcomes_payload: dict[str, JsonValue] = {
            nodeid: outcomes[nodeid] for nodeid in sorted(outcomes)
        }
        payload: dict[str, JsonValue] = {
            "full_collection": full_payload,
            "outcomes": outcomes_payload,
            "selected_nodeids": selected_payload,
            "validation_errors": errors_payload,
        }
        raw_workeroutput: JsonValue = getattr(config, "workeroutput", None)
        if not isinstance(raw_workeroutput, dict):
            errors.append("xdist worker output is not a JSON mapping")
            session.exitstatus = pytest.ExitCode.TESTS_FAILED
        else:
            raw_workeroutput[WORKER_PAYLOAD_KEY] = payload
        if (
            isinstance(raw_workeroutput, dict)
            and not selected
            and exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED
        ):
            session.exitstatus = pytest.ExitCode.OK
            raw_workeroutput["exitstatus"] = int(pytest.ExitCode.OK)
        if ShardSessionState.config is config:
            ShardSessionState.config = config.stash.get(PREVIOUS_CONFIG_KEY, None)
        return
    count, index, max_workers, _, _ = spec
    observed_workers = len(config.stash[SEEN_WORKERS_KEY])
    full, selected, outcomes, errors = aggregate_workers(
        config.stash[WORKERS_KEY],
        shard_index_value=index,
        shard_count=count,
        observed_workers=observed_workers,
        expected_workers=max_workers,
        inherited_errors=tuple(config.stash[ERRORS_KEY]),
    )
    write_manifest(
        spec,
        worker_count=observed_workers,
        full_collection=full,
        selected_nodeids=selected,
        outcomes=outcomes,
        validation_errors=errors,
    )
    if errors:
        session.exitstatus = pytest.ExitCode.TESTS_FAILED
    elif not selected and exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED:
        session.exitstatus = pytest.ExitCode.OK
    if ShardSessionState.config is config:
        ShardSessionState.config = config.stash.get(PREVIOUS_CONFIG_KEY, None)


__all__: list[str] = [
    "pytest_addoption",
    "pytest_collection_modifyitems",
    "pytest_collectreport",
    "pytest_configure",
    "pytest_runtest_logreport",
    "pytest_sessionfinish",
    "pytest_sessionstart",
    "pytest_testnodedown",
]
