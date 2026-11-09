# Docker test lifecycle

A Docker marker selects the daemon capability. A service marker such as `ldap`
selects its packaged service through `tk.shared(name)`. Collection does not create
services. Before a selected service test enters its fixtures, the capability owner
invokes that service's preparation explicitly. Offline tests never provision a service.
CI uses the same selection contract.

`execute()` holds the named service lease, inspects the live container, and creates
only an absent selected service. Creation uses native Compose `up --no-recreate
--no-deps`, its declared service, generated creation secrets and bounded readiness.
It never runs Compose down, removes volumes, or removes sibling services. A stopped
matching service is started without replacement. Existing unhealthy services and
native declaration drift fail; neither condition authorizes a reset.

Native Compose resolves the declaration. Its image, explicit environment values,
container name and published ports are checked against live inspection. Host JSON
records, dirty flags and file fingerprints have no authority over runtime data.

`verify()` performs declaration and readiness checks without changing the service.
`lease()` protects a session using the shared service. The private host directory
stores leases and temporary creation artifacts, with no lifecycle cache.

Docker fixtures read credentials from the service's own creation environment through
`fetch_container_environment`, whose values are `SecretStr`. A missing required key
fails by key name without printing its value. Generated secrets reach Compose through
a temporary mode-0600 artifact and a matching process scope; inherited credentials do
not override the selected provider. External service markers use their explicitly
declared process inputs instead. No `.env` file or Git tracking state selects tests.

Container ports belong to Compose; readiness and fixture connections resolve the
published host port from live inspection. Tests own their isolated data namespaces.
Connecting never authorizes application data initialization or cleanup.

Explicit `down()` and `compose_down()` are destructive lifecycle operations for the
caller-owned project. Test connection fixtures do not invoke them. Lifecycle integration
tests use unique projects and clean up only those projects.
