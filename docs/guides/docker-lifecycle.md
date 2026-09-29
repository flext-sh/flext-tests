# Docker test lifecycle

<!-- TOC START -->

- [Host-scoped state](#host-scoped-state)
- [Host file lock](#host-file-lock)
- [Ensure: decide, converge, serve](#ensure-decide-converge-serve)
- [Verify and lease](#verify-and-lease)
- [Ports, environment and fingerprint](#ports-environment-and-fingerprint)
- [The Make CI token](#the-make-ci-token)
- [Removed surfaces](#removed-surfaces)

<!-- TOC END -->

`tk` (`FlextTestsDocker`) manages the containers that FLEXT test suites share. One
container of a given name serves every checkout and every pytest worker of the machine;
nothing about it is scoped to a worker or to a repository.

## Host-scoped state

Each container name has one JSON record under `state_dir`, by default
`~/.flext/docker/<name>.json` (`u.Tests.docker_state_dir()`). The record
(`m.Tests.ContainerState`) holds the container id and fingerprint the lifecycle sealed,
the `dirty` flag and the `sealed` flag. A name without a record is unprovisioned: no id,
no fingerprint, clean and unsealed.

A record is rewritten atomically while `<name>.state.lock` is held
(`u.Tests.update_container_state`), so a reader always sees one complete record. An
unreadable or invalid record fails every reader and writer with its cause; it is never
replaced by the unprovisioned default. A container name outside Docker's own grammar is
rejected before it becomes a path.

`mark_container_dirty(name)`, `mark_container_clean(name)`, `container_dirty(name)` and
`dirty_containers` read and write these host records. Marking a container dirty is
bookkeeping, not a Docker effect, so it also works under the CI token.
`cleanup_dirty_containers()` recreates the dirty containers declared in
`c.Tests.SHARED_CONTAINERS` and leaves the records of every other container to the
lifecycle that declares it; the first recreation failure is returned.

Every builder (`tk.shared`, `tk.compose`, `tk.stack`, `FlextTestsKube.kind`) and the
constructor accept `state_dir`. Tests pass a directory under `tmp_path`; nothing a test
does reaches the host records.

## Host file lock

`u.Tests.FileLock(lock_file, *, shared=False, timeout_seconds=None)` is the single host
lock primitive. It is exclusive by default; `shared=True` takes a shared lock that
coexists with other shared holders and excludes an exclusive one. With
`timeout_seconds=None` it blocks until granted; with a number it polls a non-blocking
attempt until that deadline and raises `TimeoutError` naming the file and the mode. The
lock file is never removed, so all holders coordinate through one inode. Shared and
bounded modes need POSIX `fcntl`; on Windows only the blocking exclusive mode exists.

The session lease of a container uses `<name>.lease.lock`, separate from
`<name>.state.lock`, so marking a container dirty never waits on the sessions that use
it.

## Ensure: decide, converge, serve

`tk.execute(*, initializer=None, readiness_probe=None, creation_environment=None)`
ensures the configured container. `u.Tests.docker_action(info, state, fingerprint=...)`
is the pure decision table it applies:

| Container and record                                               | Action     |
| ------------------------------------------------------------------ | ---------- |
| no container                                                       | `CREATE`   |
| record dirty, unsealed, sealed for other inputs or for another id  | `RECREATE` |
| healthcheck `unhealthy`                                            | `RECREATE` |
| sealed, matching, `running` (healthy, starting or without a check) | `REUSE`    |
| sealed, matching, `exited` or `created`                            | `START`    |
| any other status                                                   | `RECREATE` |

The decision is taken under a shared lease, where a matching container is reused. Any
other action takes the exclusive lease, waiting at most the target's
`lock_timeout_seconds` for the other sessions to release theirs (`LOCK_TIMEOUT`
otherwise), and decides again: another session may already have converged. Creation
unseals the record, runs `compose up --wait --wait-timeout <startup_timeout>` in the
target's compose project, runs `initializer` once, and only then seals the record with
the new container id and fingerprint. An interrupted or failed creation leaves the
record unsealed, so the next ensure recreates it.

Every successful ensure then serves the container within `startup_timeout`: it waits for
a starting healthcheck to settle, waits for the published host port of `port` to accept
TCP, and polls `readiness_probe` until it reports `True` (`READINESS_TIMEOUT`
otherwise). Waits are bounded condition polling; no operation is retried.

## Verify and lease

`tk.verify(*, readiness_probe=None, required_environment=())` changes nothing. It fails
with one typed code: `NOT_PROVISIONED`, `DIRTY`, `UNSEALED`, `FINGERPRINT_MISMATCH`,
`UNHEALTHY`, `LOCK_TIMEOUT` (a recreation holds the lease), `ENVIRONMENT_MISSING`,
`PORT_NOT_PUBLISHED` or `READINESS_TIMEOUT`. `u.Tests.docker_verify` is its pure part.

`with tk.lease():` holds the shared lease of the configured container, so no other
session recreates it meanwhile. A session ensures first and leases second: an ensure
that must mutate cannot run inside its own session's lease.

## Ports, environment and fingerprint

`ContainerConfig.port` is the port the service listens on inside the container.
`u.Tests.resolve_host_port(info, port)` reads the host port Docker published for it,
which also works for ephemeral bindings such as `127.0.0.1::389`; an unpublished port
fails `PORT_NOT_PUBLISHED`. The `flext-openldap-test` shared entry therefore declares
389 and resolves the published 3390.

`creation_environment` values reach compose only while it creates the container, through
a 0600 env file next to the host records that is removed when compose returns; a
leftover file from an interrupted run fails the creation. Values are written literally,
so a single quote or a line break is rejected before any effect.
`tk.fetch_container_environment(name, keys)` reads them back from the container as
`SecretStr`; a missing key fails `ENVIRONMENT_MISSING`, naming the key only.

`tk.fingerprint(target)` (`u.Tests.docker_fingerprint`) is a SHA-256 over the compose
project, the service and the bytes of the compose file and of `fingerprint_inputs`. The
process environment is never an input. `project_name` overrides the project derived from
the compose file stem (`u.Tests.docker_compose_project`).

## The Make CI token

The CI token is owned by flext-infra (`config.Infra.codegen.make.ci`, variable `CI`).
`tk.ci_disables_docker()` is true only for that exact value; GitHub's `CI=true` is not
the token. Under the token every Docker effect of `tk` and `FlextTestsKube` (`execute`,
`up`, `down`, `compose_up`, `compose_down`, `start_compose_stack`,
`start_existing_container`, `cleanup_dirty_containers`, `verify`, `cluster_up`,
`cluster_down`, `nodes_ready`) returns a failure whose `error_code` is
`c.Tests.DockerErrorCode.DISABLED_BY_CI`, before touching Docker.
`tk.lifecycle_enabled()` exposes the same gate. Nothing skips: a suite that runs a
Docker test under the token fails, typed. Docker tests carry the `docker` marker, which
the runner excludes from `make test` and CI; `make test-full` on a Docker host runs
them. Caller errors, such as an unconfigured target, are reported first because they do
not depend on the environment.

## Removed surfaces

- `worker_id` (field, builder and `FlextTestsKube.kind` parameter): state is per host.
- `dirty_container_names`, `state_file_path` and the `docker_state_<worker>.json` files:
  replaced by the host records. Old files under `~/.flext/` are no longer read.
- `skip_if_ci_disables_docker()` and `c.Tests.DOCKER_CI_SKIP_REASON`: the CI token is a
  typed failure, never a skip.
- `c.Tests.ENV_CI` and `c.Tests.CI_MAKE_VALUE`: duplicates of the flext-infra CI token.
- `FlextTestsDocker.compose_project_name` and the shared `docker` client class variable:
  every compose call binds its own file, project and env files
  (`u.Tests.docker_compose_project`).
- The readiness fallback that treated `port` as a host port when no binding matched.
