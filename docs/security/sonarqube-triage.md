# Triagem SonarCloud — flext-sh/flext-tests

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead: `mro-2wjm.23`

## Resumo

**106 issues** — BLOCKER 15, CRITICAL 18, MAJOR 44, MINOR 29
Tipos: VULNERABILITY 48, BUG 0, CODE_SMELL 58 · **Debt total: 1433min**

| regra | issues |
|---|---|
| `docker:S6506` | 20 |
| `docker:S8482` | 15 |
| `python:S3776` | 11 |
| `python:S7498` | 10 |
| `python:S3358` | 9 |
| `python:S108` | 9 |
| `docker:S6470` | 5 |
| `docker:S6471` | 5 |
| `docker:S7031` | 5 |
| `python:S2772` | 3 |

## Como usar

Cada issue traz a **mensagem do SonarQube** (descreve o problema e o impacto), o **código real** (linha `>>>`), o tipo e o effort estimado.
**Decisão**: `corrigir` / `falso-positivo` (marcar na plataforma com justificativa) / `risco-aceito`. Ordem: BLOCKER → CRITICAL → VULNERABILITY → MAJOR. CODE_SMELL em volume pede correção de padrão.

## Issues

### 1 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:20` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       16  # === SECTION: managed tool bootstrap (managed) ===
       17  # Source: config:python_version, template (installer URLs)
       18  # mise installs the supported Python 3.13 family.
       19  # uv is supplied by the managed environment without a project patch pin.
>>>    20  RUN curl -fsSL https://mise.run | sh
       21  # uv is intentionally supplied by the caller environment; install it explicitly
       22  # in clean-machine images so the project bootstrap can resolve dependencies.
       23  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       24  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
```

**Decisão**: 

### 2 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:23` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       19  # uv is supplied by the managed environment without a project patch pin.
       20  RUN curl -fsSL https://mise.run | sh
       21  # uv is intentionally supplied by the caller environment; install it explicitly
       22  # in clean-machine images so the project bootstrap can resolve dependencies.
>>>    23  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       24  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       25  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       26  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       27  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
```

**Decisão**: 

### 3 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:25` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       21  # uv is intentionally supplied by the caller environment; install it explicitly
       22  # in clean-machine images so the project bootstrap can resolve dependencies.
       23  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       24  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
>>>    25  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       26  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       27  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       28      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       29  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
```

**Decisão**: 

### 4 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/arch.Dockerfile:22` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       18  # === SECTION: managed tool bootstrap (managed) ===
       19  # Source: config:python_version, template (installer URLs)
       20  # mise installs the supported Python 3.13 family.
       21  # uv is supplied by the managed environment without a project patch pin.
>>>    22  RUN curl -fsSL https://mise.run | sh
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
       25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
```

**Decisão**: 

### 5 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/arch.Dockerfile:25` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       21  # uv is supplied by the managed environment without a project patch pin.
       22  RUN curl -fsSL https://mise.run | sh
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
>>>    25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       27  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       28  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       29  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
```

**Decisão**: 

### 6 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/arch.Dockerfile:27` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
       25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
>>>    27  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       28  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       29  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       30      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       31  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
```

**Decisão**: 

### 7 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:23` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       19  # === SECTION: managed tool bootstrap (managed) ===
       20  # Source: config:python_version, template (installer URLs)
       21  # mise installs the supported Python 3.13 family.
       22  # uv is supplied by the managed environment without a project patch pin.
>>>    23  RUN curl -fsSL https://mise.run | sh
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
       26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
```

**Decisão**: 

### 8 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:26` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       22  # uv is supplied by the managed environment without a project patch pin.
       23  RUN curl -fsSL https://mise.run | sh
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
>>>    26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       28  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       29  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       30  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
```

**Decisão**: 

### 9 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:28` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
       26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
>>>    28  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       29  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       30  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       31      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       32  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
```

**Decisão**: 

### 10 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/fedora.Dockerfile:22` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       18  # === SECTION: managed tool bootstrap (managed) ===
       19  # Source: config:python_version, template (installer URLs)
       20  # mise installs the supported Python 3.13 family.
       21  # uv is supplied by the managed environment without a project patch pin.
>>>    22  RUN curl -fsSL https://mise.run | sh
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
       25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
```

**Decisão**: 

### 11 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/fedora.Dockerfile:25` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       21  # uv is supplied by the managed environment without a project patch pin.
       22  RUN curl -fsSL https://mise.run | sh
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
>>>    25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       27  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       28  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       29  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
```

**Decisão**: 

### 12 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/fedora.Dockerfile:27` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
       25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
>>>    27  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       28  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       29  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       30      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       31  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
```

**Decisão**: 

### 13 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:23` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       19  # === SECTION: managed tool bootstrap (managed) ===
       20  # Source: config:python_version, template (installer URLs)
       21  # mise installs the supported Python 3.13 family.
       22  # uv is supplied by the managed environment without a project patch pin.
>>>    23  RUN curl -fsSL https://mise.run | sh
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
       26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
```

**Decisão**: 

### 14 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:26` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       22  # uv is supplied by the managed environment without a project patch pin.
       23  RUN curl -fsSL https://mise.run | sh
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
>>>    26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       28  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       29  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       30  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
```

**Decisão**: 

### 15 · 🔴 BLOCKER · VULNERABILITY · `docker:S8482`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:28` · **Effort**: 15min

> Avoid executing downloaded artifacts directly without verification.

```Dockerfile
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
       26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
>>>    28  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       29  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       30  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       31      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       32  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
```

**Decisão**: 

### 16 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_utilities/_files/_batch.py:16` · **Effort**: 13min

> Refactor this function to reduce its Cognitive Complexity from 23 to the 15 allowed.

```python
       12  
       13  class FlextTestsFilesBatchMixin(FlextTestsFilesContextsMixin):
       14      """Batch create/read/delete file operations."""
       15  
>>>    16      def batch_files[TModel: m.BaseModel](
       17          self,
       18          items: t.Tests.BatchFiles,
       19          *,
       20          directory: Path | None = None,
```

**Decisão**: 

### 17 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_utilities/_files/_info.py:109` · **Effort**: 7min

> Refactor this function to reduce its Cognitive Complexity from 17 to the 15 allowed.

```python
      105              return (text, lines, is_empty, first_line, c.Tests.DEFAULT_ENCODING)
      106          except UnicodeDecodeError:
      107              return ("", 0, size == 0, "", c.Tests.DEFAULT_BINARY_ENCODING)
      108  
>>>   109      def _parse_content_metadata(
      110          self, text: str, fmt: str, validate_model: type[m.BaseModel] | None = None
      111      ) -> m.Tests.ContentMeta:
      112          """Parse file content and extract metadata.
      113  
```

**Decisão**: 

### 18 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_utilities/_files/_reading.py:63` · **Effort**: 13min

> Refactor this function to reduce its Cognitive Complexity from 23 to the 15 allowed.

```python
       59          delim: str = c.Tests.DEFAULT_CSV_DELIMITER,
       60          has_headers: bool = True,
       61      ) -> p.Result[TModelRead]: ...
       62  
>>>    63      def read[TModelRead: m.BaseModel](
       64          self,
       65          path: Path,
       66          *,
       67          model_cls: type[TModelRead] | None = None,
```

**Decisão**: 

### 19 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_utilities/_matchers/_containment.py:21` · **Effort**: 54min

> Refactor this function to reduce its Cognitive Complexity from 64 to the 15 allowed.

```python
       17  class FlextTestsMatchersContainmentMixin:
       18      """Shared ``has``/``lacks`` containment checks."""
       19  
       20      @staticmethod
>>>    21      def check_has_lacks(
       22          value: p.AttributeProbe,
       23          has: p.AttributeProbe | None,
       24          lacks: p.AttributeProbe | None,
       25          msg: str | None,
```

**Decisão**: 

### 20 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:532` · **Effort**: 8min

> Refactor this function to reduce its Cognitive Complexity from 18 to the 15 allowed.

```python
      528                  except c.ValidationError:
      529                      return dict[str, t.Tests.TestobjectSerializable]()
      530  
      531              @classmethod
>>>   532              def _validate_mapping(
      533                  cls,
      534                  subject_payload: t.Tests.TestobjectSerializable,
      535                  params: m.Tests.ThatParams,
      536              ) -> None:
```

**Decisão**: 

### 21 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:607` · **Effort**: 10min

> Refactor this function to reduce its Cognitive Complexity from 20 to the 15 allowed.

```python
      603                              )
      604                          )
      605  
      606              @classmethod
>>>   607              def _validate_attrs(
      608                  cls, subject: p.AttributeProbe, params: m.Tests.ThatParams
      609              ) -> None:
      610                  """Validate attrs/methods/attr_eq predicates."""
      611                  if params.attrs is not None:
```

**Decisão**: 

### 22 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_utilities/make_contract.py:53` · **Effort**: 16min

> Refactor this function to reduce its Cognitive Complexity from 26 to the 15 allowed.

```python
       49                  )
       50          return r[bool].ok(True)
       51  
       52      @staticmethod
>>>    53      def make_validate_command_contract(command: m.Tests.MakeCommand) -> p.Result[bool]:
       54          """Validate one command against the generic dispatcher contract."""
       55          param_by_name = {param.name: param for param in command.params}
       56          if command.mutates:
       57              for name in c.Tests.MAKE_MUTATION_REQUIRED_PARAMS:
```

**Decisão**: 

### 23 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_utilities/make_registry.py:132` · **Effort**: 10min

> Refactor this function to reduce its Cognitive Complexity from 20 to the 15 allowed.

```python
      128              )
      129          return r[m.Tests.MakeCommand].ok(command)
      130  
      131      @classmethod
>>>   132      def make_discover(cls, scripts_dir: Path) -> p.Result[m.Tests.MakeRegistry]:
      133          """Discover and validate promoted commands under ``scripts/cmd``."""
      134          if not scripts_dir.exists():
      135              return r[m.Tests.MakeRegistry].fail("diretorio scripts/cmd missing")
      136  
```

**Decisão**: 

### 24 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_utilities/make_rendering.py:155` · **Effort**: 7min

> Refactor this function to reduce its Cognitive Complexity from 17 to the 15 allowed.

```python
      151              lines.extend(f"  {example}" for example in examples)
      152          return r[str].ok("\n".join(lines))
      153  
      154      @staticmethod
>>>   155      def make_render_command_help(
      156          registry: m.Tests.MakeRegistry, requested_verb: str, what: str
      157      ) -> p.Result[str]:
      158          """Render help for one promoted command."""
      159          command_result = FlextTestsMakeRegistryUtilitiesMixin.make_registry_command(
```

**Decisão**: 

### 25 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_utilities/workspace_cleanup_paths.py:94` · **Effort**: 7min

> Refactor this function to reduce its Cognitive Complexity from 17 to the 15 allowed.

```python
       90              return r[Path].fail("cleanup residue cannot be the workspace root")
       91          return r[Path].ok(lexical)
       92  
       93      @classmethod
>>>    94      def _reject_protected(cls, root: Path, relative_path: Path) -> p.Result[bool]:
       95          """Refuse any residue that targets a protected component or the Git dir."""
       96          if any(part in cls._PROTECTED_COMPONENTS for part in relative_path.parts):
       97              return r[bool].fail(
       98                  f"cleanup residue targets a protected path: {relative_path}"
```

**Decisão**: 

### 26 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_tests/_validator/tests.py:60` · **Effort**: 9min

> Refactor this function to reduce its Cognitive Complexity from 19 to the 15 allowed.

```python
       56              index += 1
       57          return tuple(signatures)
       58  
       59      @classmethod
>>>    60      def _check_mock_usage(
       61          cls,
       62          file_path: Path,
       63          lines: t.StrSequence,
       64          approved: t.MappingKV[str, t.StrSequence],
```

**Decisão**: 

### 27 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_tests/domains.py:15` · **Effort**: 18min

> Define a constant instead of duplicating this literal ".ldif" 9 times.

```python
       11  class FlextTestsDomains:
       12      """Test domain objects and fixtures."""
       13  
       14      @staticmethod
>>>    15      def fixture_filename(group: str, kind: str, file_extension: str = ".ldif") -> str:
       16          """Build the canonical fixture filename for a group and kind."""
       17          return f"{group}_{kind}_fixtures{file_extension}"
       18  
       19      @classmethod
```

**Decisão**: 

### 28 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_tests/kube.py:56` · **Effort**: 6min

> Define a constant instead of duplicating this literal "Kubernetes target not configured. Use tkube.kind(...) first." 3 times.

```python
       52          """Start the kind stack and wait for the apiserver to accept TCP."""
       53          target = self.target_config
       54          if target is None:
       55              return r[str].fail(
>>>    56                  "Kubernetes target not configured. Use tkube.kind(...) first."
       57              )
       58          if target.compose_file is None:
       59              return r[str].fail("Kubernetes target has no compose file configured.")
       60          up_result = self.compose_up(
```

**Decisão**: 

### 29 · 🟠 CRITICAL · VULNERABILITY · `docker:S6470`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:33` · **Effort**: 20min

> Copying recursively might inadvertently add sensitive data to the container. Make sure it is safe here.

```Dockerfile
       29  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
       30  # End SECTION: managed tool bootstrap
       31  
       32  WORKDIR /workspace
>>>    33  COPY . .
       34  
       35  # === SECTION: mise install (managed) ===
       36  # Source: computed (reads .mise.toml from copied workspace)
       37  RUN mise trust .mise.toml && mise install --yes
```

**Decisão**: 

### 30 · 🟠 CRITICAL · VULNERABILITY · `docker:S6470`
**Local**: `tests/fixtures/ci/docker/arch.Dockerfile:35` · **Effort**: 20min

> Copying recursively might inadvertently add sensitive data to the container. Make sure it is safe here.

```Dockerfile
       31  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
       32  # End SECTION: managed tool bootstrap
       33  
       34  WORKDIR /workspace
>>>    35  COPY . .
       36  
       37  # === SECTION: mise install (managed) ===
       38  # Source: computed (reads .mise.toml from copied workspace)
       39  RUN mise trust .mise.toml && mise install --yes
```

**Decisão**: 

### 31 · 🟠 CRITICAL · VULNERABILITY · `docker:S6470`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:36` · **Effort**: 20min

> Copying recursively might inadvertently add sensitive data to the container. Make sure it is safe here.

```Dockerfile
       32  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
       33  # End SECTION: managed tool bootstrap
       34  
       35  WORKDIR /workspace
>>>    36  COPY . .
       37  
       38  # === SECTION: mise install (managed) ===
       39  # Source: computed (reads .mise.toml from copied workspace)
       40  RUN mise trust .mise.toml && mise install --yes
```

**Decisão**: 

### 32 · 🟠 CRITICAL · VULNERABILITY · `docker:S6470`
**Local**: `tests/fixtures/ci/docker/fedora.Dockerfile:35` · **Effort**: 20min

> Copying recursively might inadvertently add sensitive data to the container. Make sure it is safe here.

```Dockerfile
       31  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
       32  # End SECTION: managed tool bootstrap
       33  
       34  WORKDIR /workspace
>>>    35  COPY . .
       36  
       37  # === SECTION: mise install (managed) ===
       38  # Source: computed (reads .mise.toml from copied workspace)
       39  RUN mise trust .mise.toml && mise install --yes
```

**Decisão**: 

### 33 · 🟠 CRITICAL · VULNERABILITY · `docker:S6470`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:36` · **Effort**: 20min

> Copying recursively might inadvertently add sensitive data to the container. Make sure it is safe here.

```Dockerfile
       32  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
       33  # End SECTION: managed tool bootstrap
       34  
       35  WORKDIR /workspace
>>>    36  COPY . .
       37  
       38  # === SECTION: mise install (managed) ===
       39  # Source: computed (reads .mise.toml from copied workspace)
       40  RUN mise trust .mise.toml && mise install --yes
```

**Decisão**: 

### 34 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8264`
**Local**: `.github/workflows/docs.yml:18` · **Effort**: 5min

> Move this read permission from workflow level to job level.

```yaml
       14        - ".github/workflows/docs.yml"
       15    workflow_dispatch:
       16  
       17  permissions:
>>>    18    contents: read
       19    pages: write
       20    id-token: write
       21  
       22  concurrency:
```

**Decisão**: 

### 35 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:19` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       15    workflow_dispatch:
       16  
       17  permissions:
       18    contents: read
>>>    19    pages: write
       20    id-token: write
       21  
       22  concurrency:
       23    group: pages
```

**Decisão**: 

### 36 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:20` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       16  
       17  permissions:
       18    contents: read
       19    pages: write
>>>    20    id-token: write
       21  
       22  concurrency:
       23    group: pages
       24    cancel-in-progress: false
```

**Decisão**: 

### 37 · 🟡 MAJOR · CODE_SMELL · `python:S8786`
**Local**: `src/flext_tests/_constants/validator.py:205` · **Effort**: 20min

> Simplify this regular expression to reduce its runtime, as it has super-linear performance due to backtracking.

```python
      201      VALIDATOR_INDENTED_IMPORT_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
      202          r"^[ \t]+(?:from\s+\S+\s+import\b|import\s+\S+)"
      203      )
      204      VALIDATOR_IMPORT_ERROR_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
>>>   205          r"^[ \t]*except\b.*\b(?:ImportError|ModuleNotFoundError)\b.*:\s*(?:#.*)?$"
      206      )
      207      VALIDATOR_BARE_EXCEPT_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
      208          r"^[ \t]*except\s*:\s*(?:#.*)?$"
      209      )
```

**Decisão**: 

### 38 · 🟡 MAJOR · CODE_SMELL · `python:S8786`
**Local**: `src/flext_tests/_constants/validator.py:211` · **Effort**: 20min

> Simplify this regular expression to reduce its runtime, as it has super-linear performance due to backtracking.

```python
      207      VALIDATOR_BARE_EXCEPT_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
      208          r"^[ \t]*except\s*:\s*(?:#.*)?$"
      209      )
      210      VALIDATOR_EXCEPT_HEADER_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
>>>   211          r"^(?P<indent>[ \t]*)except\b.*:\s*(?:#.*)?$"
      212      )
      213      VALIDATOR_PASS_OR_ELLIPSIS_RE: ClassVar[t.Infra.RegexPattern] = re.compile(
      214          r"^(?:pass|\.\.\.)\s*(?:#.*)?$"
      215      )
```

**Decisão**: 

### 39 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_tests/_utilities/_files/_comparison.py:36` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
       32          """Try to parse both contents as dicts in given format."""
       33          parse = (
       34              u.Cli.json_parse
       35              if fmt == "json"
>>>    36              else u.Cli.yaml_parse
       37              if fmt == "yaml"
       38              else None
       39          )
       40          if parse is None:
```

**Decisão**: 

### 40 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_tests/_utilities/_files/_comparison_parts/comparison_part_01.py:35` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
       31          """Try to parse both contents as dicts in given format."""
       32          parse = (
       33              u.Cli.json_parse
       34              if fmt == "json"
>>>    35              else u.Cli.yaml_parse
       36              if fmt == "yaml"
       37              else None
       38          )
       39          if parse is None:
```

**Decisão**: 

### 41 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_tests/_utilities/_files/_creation.py:171` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
      167              | None
      168          ) = (
      169              actual_content.root
      170              if isinstance(actual_content, (m.ConfigMap, m.Dict))
>>>   171              else actual_content
      172              if isinstance(actual_content, Mapping)
      173              else None
      174          )
      175          fallback_value = FlextTestsPayloadUtilities.to_normalized_value(
```

**Decisão**: 

### 42 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_tests/_utilities/_files/_creation.py:186` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
      182                  )
      183                  for k, v in mapping_content.items()
      184              }
      185              if mapping_content is not None
>>>   186              else {"value": fallback_value}
      187              if actual_content
      188              else {}
      189          )
      190          return t.json_value_adapter().validate_python(raw_payload)
```

**Decisão**: 

### 43 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_tests/_utilities/_files/_info.py:143` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      139                          key_count = len(parsed_dict)
      140                      case list() as parsed_list:
      141                          item_count = len(parsed_list)
      142                      case _:
>>>   143                          pass
      144              case "csv":
      145                  csv_outcome = u.Cli.csv_loads(text)
      146                  rows: list[list[str]] = csv_outcome.value if csv_outcome.success else []
      147                  if rows:
```

**Decisão**: 

### 44 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_tests/_utilities/_files/_info.py:151` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      147                  if rows:
      148                      row_count = len(rows)
      149                      column_count = len(rows[0]) if rows[0] else 0
      150              case _:
>>>   151                  pass
      152          if validate_model is not None:
      153              if parsed_mapping is not None:
      154                  # mro-j47u: consume the composed reading capability through self.
      155                  model_valid = self._validate_model_content(
```

**Decisão**: 

### 45 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_tests/_utilities/_matchers/_containment.py:64` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
       60                          )
       61                      contains_item = (
       62                          isinstance(check_val, str) and check_val in target_raw
       63                          if isinstance(target_raw, Mapping)
>>>    64                          else str(check_val) in target_raw
       65                          if isinstance(target_raw, str)
       66                          else any(candidate == check_val for candidate in target_raw)
       67                      )
       68                      if not contains_item:
```

**Decisão**: 

### 46 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_tests/_utilities/_matchers/_containment.py:110` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
      106                          )
      107                      contains_item = (
      108                          isinstance(check_val, str) and check_val in target_raw_2
      109                          if isinstance(target_raw_2, Mapping)
>>>   110                          else str(check_val) in target_raw_2
      111                          if isinstance(target_raw_2, str)
      112                          else any(candidate == check_val for candidate in target_raw_2)
      113                      )
      114                      if contains_item:
```

**Decisão**: 

### 47 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_tests/_utilities/_matchers/_result.py:166` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      162                  )
      163                  # mro-j47u: matcher type failures remain assertion failures.
      164                  match result_value:
      165                      case m.BaseModel() | Mapping():
>>>   166                          pass
      167                      case _:
      168                          failure = (
      169                              "Path extraction requires dict or model, got "
      170                              f"{type(result_value).__name__}"
```

**Decisão**: 

### 48 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_tests/_utilities/_matchers/_result.py:439` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      435                  if deep_spec is None:
      436                      return result_value
      437                  match result_value:
      438                      case m.BaseModel() | Mapping():
>>>   439                          pass
      440                      case _:
      441                          failure = (
      442                              "Deep matching requires dict or model, got "
      443                              f"{type(result_value).__name__}"
```

**Decisão**: 

### 49 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:586` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      582                          kv_items = ()
      583                  for key, expected_val in kv_items:
      584                      match key:
      585                          case str():
>>>   586                              pass
      587                          case _:
      588                              raise AssertionError(
      589                                  params.msg
      590                                  or f"Mapping key must be str, got {type(key).__name__}"
```

**Decisão**: 

### 50 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:635` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      631                                  params.msg or f"Object missing method: {method}"
      632                              )
      633                          match getattr(subject, method):
      634                              case method_value if callable(method_value):
>>>   635                                  pass
      636                              case _:
      637                                  raise AssertionError(
      638                                      params.msg
      639                                      or f"Object attribute {method} is not callable"
```

**Decisão**: 

### 51 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:660` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      656                          attr_items = ()
      657                  for attr, expected_val in attr_items:
      658                      match attr:
      659                          case str():
>>>   660                              pass
      661                          case _:
      662                              raise AssertionError(
      663                                  params.msg
      664                                  or (
```

**Decisão**: 

### 52 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:711` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
      707                  cls._validate_scalar(subject_payload, params, raw_eq, raw_ne, kwargs)
      708                  effective_has = (
      709                      raw_has
      710                      if raw_has is not None
>>>   711                      else raw_contains
      712                      if raw_contains is not None
      713                      else params.has
      714                  )
      715                  cls._validate_common(
```

**Decisão**: 

### 53 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:841` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      837          path: str,
      838      ) -> t.Tests.TestobjectSerializable:
      839          match subject:
      840              case m.BaseModel() | Mapping():
>>>   841                  pass
      842              case _:
      843                  message = (
      844                      "Path assertions require dict or model, got "
      845                      f"{type(subject).__name__}"
```

**Decisão**: 

### 54 · 🟡 MAJOR · CODE_SMELL · `python:S108`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:907` · **Effort**: 5min

> Either remove or fill this block of code.

```python
      903                          sequence_value[index], rule, inherited_msg=inherited_msg
      904                      )
      905                  return
      906              case Mapping():
>>>   907                  pass
      908              case _:
      909                  raise AssertionError(
      910                      inherited_msg
      911                      or "Item assertions must be a sequence or selector mapping"
```

**Decisão**: 

### 55 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:921` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
      917                  continue
      918              target_index = (
      919                  0
      920                  if selector == "first"
>>>   921                  else -1
      922                  if selector == "last"
      923                  else int(selector)
      924              )
      925              cls._apply_rule(
```

**Decisão**: 

### 56 · 🟡 MAJOR · CODE_SMELL · `python:S3358`
**Local**: `src/flext_tests/_utilities/workspace_cleanup_plan.py:57` · **Effort**: 5min

> Extract this nested conditional expression into an independent statement.

```python
       53          fingerprint_result = cls._path_fingerprint(path)
       54          if fingerprint_result.failure:
       55              return r[p.Tests.WorkspaceCleanupCandidate].fail(fingerprint_result.error)
       56          kind: Literal["file", "directory", "symlink"] = (
>>>    57              "symlink" if path.is_symlink() else "directory" if path.is_dir() else "file"
       58          )
       59          candidate = m.Tests.WorkspaceCleanupCandidate(
       60              relative_path=relative_path,
       61              path=path,
```

**Decisão**: 

### 57 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:20` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       16  # === SECTION: managed tool bootstrap (managed) ===
       17  # Source: config:python_version, template (installer URLs)
       18  # mise installs the supported Python 3.13 family.
       19  # uv is supplied by the managed environment without a project patch pin.
>>>    20  RUN curl -fsSL https://mise.run | sh
       21  # uv is intentionally supplied by the caller environment; install it explicitly
       22  # in clean-machine images so the project bootstrap can resolve dependencies.
       23  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       24  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
```

**Decisão**: 

### 58 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:23` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       19  # uv is supplied by the managed environment without a project patch pin.
       20  RUN curl -fsSL https://mise.run | sh
       21  # uv is intentionally supplied by the caller environment; install it explicitly
       22  # in clean-machine images so the project bootstrap can resolve dependencies.
>>>    23  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       24  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       25  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       26  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       27  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
```

**Decisão**: 

### 59 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:25` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       21  # uv is intentionally supplied by the caller environment; install it explicitly
       22  # in clean-machine images so the project bootstrap can resolve dependencies.
       23  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       24  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
>>>    25  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       26  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       27  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       28      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       29  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
```

**Decisão**: 

### 60 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:27` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       23  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       24  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       25  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       26  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
>>>    27  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       28      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       29  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
       30  # End SECTION: managed tool bootstrap
       31  
```

**Decisão**: 

### 61 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/arch.Dockerfile:22` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       18  # === SECTION: managed tool bootstrap (managed) ===
       19  # Source: config:python_version, template (installer URLs)
       20  # mise installs the supported Python 3.13 family.
       21  # uv is supplied by the managed environment without a project patch pin.
>>>    22  RUN curl -fsSL https://mise.run | sh
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
       25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
```

**Decisão**: 

### 62 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/arch.Dockerfile:25` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       21  # uv is supplied by the managed environment without a project patch pin.
       22  RUN curl -fsSL https://mise.run | sh
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
>>>    25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       27  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       28  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       29  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
```

**Decisão**: 

### 63 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/arch.Dockerfile:27` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
       25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
>>>    27  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       28  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       29  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       30      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       31  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
```

**Decisão**: 

### 64 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/arch.Dockerfile:29` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       27  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       28  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
>>>    29  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       30      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       31  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
       32  # End SECTION: managed tool bootstrap
       33  
```

**Decisão**: 

### 65 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:23` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       19  # === SECTION: managed tool bootstrap (managed) ===
       20  # Source: config:python_version, template (installer URLs)
       21  # mise installs the supported Python 3.13 family.
       22  # uv is supplied by the managed environment without a project patch pin.
>>>    23  RUN curl -fsSL https://mise.run | sh
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
       26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
```

**Decisão**: 

### 66 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:26` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       22  # uv is supplied by the managed environment without a project patch pin.
       23  RUN curl -fsSL https://mise.run | sh
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
>>>    26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       28  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       29  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       30  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
```

**Decisão**: 

### 67 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:28` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
       26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
>>>    28  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       29  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       30  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       31      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       32  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
```

**Decisão**: 

### 68 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:30` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       28  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       29  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
>>>    30  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       31      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       32  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
       33  # End SECTION: managed tool bootstrap
       34  
```

**Decisão**: 

### 69 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/fedora.Dockerfile:22` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       18  # === SECTION: managed tool bootstrap (managed) ===
       19  # Source: config:python_version, template (installer URLs)
       20  # mise installs the supported Python 3.13 family.
       21  # uv is supplied by the managed environment without a project patch pin.
>>>    22  RUN curl -fsSL https://mise.run | sh
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
       25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
```

**Decisão**: 

### 70 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/fedora.Dockerfile:25` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       21  # uv is supplied by the managed environment without a project patch pin.
       22  RUN curl -fsSL https://mise.run | sh
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
>>>    25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       27  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       28  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       29  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
```

**Decisão**: 

### 71 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/fedora.Dockerfile:27` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       23  # uv is intentionally supplied by the caller environment; install it explicitly
       24  # in clean-machine images so the project bootstrap can resolve dependencies.
       25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
>>>    27  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       28  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       29  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       30      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       31  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
```

**Decisão**: 

### 72 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/fedora.Dockerfile:29` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       25  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       26  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       27  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       28  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
>>>    29  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       30      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       31  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
       32  # End SECTION: managed tool bootstrap
       33  
```

**Decisão**: 

### 73 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:23` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       19  # === SECTION: managed tool bootstrap (managed) ===
       20  # Source: config:python_version, template (installer URLs)
       21  # mise installs the supported Python 3.13 family.
       22  # uv is supplied by the managed environment without a project patch pin.
>>>    23  RUN curl -fsSL https://mise.run | sh
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
       26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
```

**Decisão**: 

### 74 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:26` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       22  # uv is supplied by the managed environment without a project patch pin.
       23  RUN curl -fsSL https://mise.run | sh
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
>>>    26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       28  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       29  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       30  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
```

**Decisão**: 

### 75 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:28` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       24  # uv is intentionally supplied by the caller environment; install it explicitly
       25  # in clean-machine images so the project bootstrap can resolve dependencies.
       26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
>>>    28  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       29  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
       30  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       31      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       32  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
```

**Decisão**: 

### 76 · 🟡 MAJOR · VULNERABILITY · `docker:S6506`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:30` · **Effort**: 30min

> Not enforcing HTTPS here might allow for redirections to insecure websites. Make sure it is safe here.

```Dockerfile
       26  RUN curl -fsSL https://astral.sh/uv/install.sh | sh
       27  # tokei (and any future cargo-backed mise tool) needs a Rust toolchain.
       28  RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
       29  # go is required for mise-managed beads (go:github.com/steveyegge/beads/cmd/bd).
>>>    30  RUN curl -fsSL https://go.dev/dl/go1.23.4.linux-amd64.tar.gz | tar -C /usr/local -xzf - \
       31      && ln -sf /usr/local/go/bin/go /usr/local/bin/go
       32  ENV PATH="/usr/local/go/bin:/root/.local/bin:/root/.cargo/bin:/root/.local/share/mise/shims:${PATH}"
       33  # End SECTION: managed tool bootstrap
       34  
```

**Decisão**: 

### 77 · 🟡 MAJOR · CODE_SMELL · `python:S5778`
**Local**: `tests/unit/test_utilities.py:131` · **Effort**: 5min

> Refactor this exception test to have only one invocation possibly throwing an exception.

```python
      127          )
      128  
      129      def test_assert_result_chain_treats_zero_alias_count_as_explicit(self) -> None:
      130          """Explicit expected_success_count=0 is honored, not treated as unset."""
>>>   131          with pytest.raises(AssertionError, match="Expected 0 successes, got 1"):
      132              u.Tests.assert_result_chain(
      133                  [r[str].ok("success")], expected_success_count=0
      134              )
      135  
```

**Decisão**: 

### 78 · ⚪ MINOR · CODE_SMELL · `python:S7504`
**Local**: `conftest.py:20` · **Effort**: 5min

> Remove this unnecessary `list()` call on an already iterable object.

```python
       16      if (
       17          existing_package is None
       18          or Path(getattr(existing_package, "__file__", "")).resolve() != init_file
       19      ):
>>>    20          for module_name in list(sys.modules):
       21              if module_name == package_name or module_name.startswith(
       22                  f"{package_name}."
       23              ):
       24                  sys.modules.pop(module_name, None)
```

**Decisão**: 

### 79 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_tests/_models/batch.py:76` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
       72              t.MappingKV[str, p.Result[t.Tests.TestResultValue]],
       73              u.Field(description="Mapping of file names to operation results"),
       74          ] = u.Field(
       75              default_factory=lambda: MappingProxyType(
>>>    76                  dict[str, p.Result[t.Tests.TestResultValue]]()
       77              )
       78          )
       79          errors: Annotated[
       80              t.StrMapping, u.Field(description="Mapping of file names to error messages")
```

**Decisão**: 

### 80 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_tests/_models/batch.py:81` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
       77              )
       78          )
       79          errors: Annotated[
       80              t.StrMapping, u.Field(description="Mapping of file names to error messages")
>>>    81          ] = u.Field(default_factory=lambda: MappingProxyType(dict[str, str]()))
       82  
       83          @u.computed_field
       84          @property
       85          def failure_count(self) -> int:
```

**Decisão**: 

### 81 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_tests/_models/make.py:95` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
       91          ]
       92          aliases_by_name: Annotated[
       93              t.MappingKV[str, str],
       94              u.Field(description="Verb aliases keyed by alias name."),
>>>    95          ] = u.Field(default_factory=lambda: MappingProxyType(dict[str, str]()))
       96  
       97      class MakeSurfaceProbe(m.Value):
       98          """One in-process dispatcher probe for surface validation."""
       99  
```

**Decisão**: 

### 82 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_tests/_models/make.py:105` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
      101          argv: Annotated[t.StrSequence, u.Field(description="Dispatcher argv.")]
      102          env: Annotated[
      103              t.MappingKV[str, str],
      104              u.Field(description="Environment values for this probe."),
>>>   105          ] = u.Field(default_factory=lambda: MappingProxyType(dict[str, str]()))
      106          expected_output: Annotated[
      107              t.StrSequence,
      108              u.Field(description="Output fragments expected from the probe."),
      109          ] = ()
```

**Decisão**: 

### 83 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_tests/_models/matchers.py:391` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
      387              t.MappingKV[str, t.Tests.TestobjectSerializable],
      388              u.Field(description="Configuration dictionary."),
      389          ] = u.Field(
      390              default_factory=lambda: MappingProxyType(
>>>   391                  dict[str, t.Tests.TestobjectSerializable]()
      392              )
      393          )
      394          container: Annotated[
      395              t.MappingKV[str, t.Tests.TestobjectSerializable],
```

**Decisão**: 

### 84 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_tests/_models/matchers.py:399` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
      395              t.MappingKV[str, t.Tests.TestobjectSerializable],
      396              u.Field(description="Container/service mappings."),
      397          ] = u.Field(
      398              default_factory=lambda: MappingProxyType(
>>>   399                  dict[str, t.Tests.TestobjectSerializable]()
      400              )
      401          )
      402          context: Annotated[
      403              t.MappingKV[str, t.Tests.TestobjectSerializable],
```

**Decisão**: 

### 85 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_tests/_models/matchers.py:407` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
      403              t.MappingKV[str, t.Tests.TestobjectSerializable],
      404              u.Field(description="Context values."),
      405          ] = u.Field(
      406              default_factory=lambda: MappingProxyType(
>>>   407                  dict[str, t.Tests.TestobjectSerializable]()
      408              )
      409          )
      410  
      411  
```

**Decisão**: 

### 86 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:521` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
      517                  subject_payload: t.Tests.TestobjectSerializable,
      518              ) -> t.MappingKV[str, t.Tests.TestobjectSerializable]:
      519                  """Validate and normalize a mapping payload."""
      520                  if not isinstance(subject_payload, Mapping):
>>>   521                      return dict[str, t.Tests.TestobjectSerializable]()
      522                  try:
      523                      return (
      524                          t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER.validate_python(
      525                              subject_payload
```

**Decisão**: 

### 87 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_tests/_utilities/_matchers/_that.py:529` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
      525                              subject_payload
      526                          )
      527                      )
      528                  except c.ValidationError:
>>>   529                      return dict[str, t.Tests.TestobjectSerializable]()
      530  
      531              @classmethod
      532              def _validate_mapping(
      533                  cls,
```

**Decisão**: 

### 88 · ⚪ MINOR · CODE_SMELL · `python:S2772`
**Local**: `src/flext_tests/_validator/_types_parts/types_part_01.py:12` · **Effort**: 2min

> Remove this unneeded "pass".

```python
        8  
        9  from flext_tests import c, t, u
       10  
       11  if TYPE_CHECKING:
>>>    12      pass
       13      from flext_tests import m
       14  
       15  
       16  class FlextValidatorTypes(u.Tests.ValidatorScannerMixin):
```

**Decisão**: 

### 89 · ⚪ MINOR · CODE_SMELL · `python:S2772`
**Local**: `src/flext_tests/_validator/_types_parts/types_part_02.py:15` · **Effort**: 2min

> Remove this unneeded "pass".

```python
       11      FlextValidatorTypes as FlextValidatorTypesPart01,
       12  )
       13  
       14  if TYPE_CHECKING:
>>>    15      pass
       16      from flext_tests import m
       17  
       18  
       19  class FlextValidatorTypes(FlextValidatorTypesPart01):
```

**Decisão**: 

### 90 · ⚪ MINOR · CODE_SMELL · `python:S2772`
**Local**: `src/flext_tests/_validator/tests.py:18` · **Effort**: 2min

> Remove this unneeded "pass".

```python
       14  
       15  from flext_tests import c, t, u
       16  
       17  if TYPE_CHECKING:
>>>    18      pass
       19      from flext_tests import m
       20  
       21  
       22  class FlextValidatorTests(u.Tests.ValidatorScannerMixin):
```

**Decisão**: 

### 91 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_tests/validator.py:24` · **Effort**: 2min

> Rename this field "Violation" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       20  
       21  class FlextTestsValidator:
       22      """FLEXT architecture validator orchestrating all scanners."""
       23  
>>>    24      Violation: ClassVar[type[m.Tests.Violation]] = m.Tests.Violation
       25  
       26      ScanResult: ClassVar[type[m.Tests.ScanResult]] = m.Tests.ScanResult
       27  
       28      class AllValidationOptions(m.Value):
```

**Decisão**: 

### 92 · ⚪ MINOR · CODE_SMELL · `python:S116`
**Local**: `src/flext_tests/validator.py:26` · **Effort**: 2min

> Rename this field "ScanResult" to match the regular expression ^[_a-z][_a-z0-9]*$.

```python
       22      """FLEXT architecture validator orchestrating all scanners."""
       23  
       24      Violation: ClassVar[type[m.Tests.Violation]] = m.Tests.Violation
       25  
>>>    26      ScanResult: ClassVar[type[m.Tests.ScanResult]] = m.Tests.ScanResult
       27  
       28      class AllValidationOptions(m.Value):
       29          """Options envelope for aggregate validation runs."""
       30  
```

**Decisão**: 

### 93 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_tests/validator.py:45` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
       41          approved_exceptions: Annotated[
       42              t.MappingKV[str, t.StrSequence],
       43              u.Field(description="Rule-to-path allowlist for approved exceptions."),
       44          ] = u.Field(
>>>    45              default_factory=lambda: MappingProxyType(dict[str, t.StrSequence]())
       46          )
       47          include_tests_validation: Annotated[
       48              bool,
       49              u.Field(
```

**Decisão**: 

### 94 · ⚪ MINOR · VULNERABILITY · `docker:S6471`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:8` · **Effort**: 15min

> The "alpine" image runs with "root" as the default user. Make sure it is safe here.

```Dockerfile
        4  # Free: no
        5  # End SECTION: header
        6  # Clean-machine proof: project bootstrap + canonical make verbs on Alpine
        7  # (musl, POSIX /bin/sh at runtime; bash installed for the project scripts).
>>>     8  FROM alpine:3.21
        9  
       10  # === SECTION: base packages (managed) ===
       11  # Source: template (distro-specific package list)
       12  RUN apk add --no-cache \
```

**Decisão**: 

### 95 · ⚪ MINOR · CODE_SMELL · `docker:S7031`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:12` · **Effort**: 5min

> Merge this RUN instruction with the consecutive ones.

```Dockerfile
        8  FROM alpine:3.21
        9  
       10  # === SECTION: base packages (managed) ===
       11  # Source: template (distro-specific package list)
>>>    12  RUN apk add --no-cache \
       13        bash ca-certificates curl git make build-base icu-dev icu-libs
       14  # End SECTION: base packages
       15  
       16  # === SECTION: managed tool bootstrap (managed) ===
```

**Decisão**: 

### 96 · ⚪ MINOR · CODE_SMELL · `docker:S7018`
**Local**: `tests/fixtures/ci/docker/alpine.Dockerfile:12` · **Effort**: 5min

> Sort these package names alphanumerically.

```Dockerfile
        8  FROM alpine:3.21
        9  
       10  # === SECTION: base packages (managed) ===
       11  # Source: template (distro-specific package list)
>>>    12  RUN apk add --no-cache \
       13        bash ca-certificates curl git make build-base icu-dev icu-libs
       14  # End SECTION: base packages
       15  
       16  # === SECTION: managed tool bootstrap (managed) ===
```

**Decisão**: 

### 97 · ⚪ MINOR · VULNERABILITY · `docker:S6471`
**Local**: `tests/fixtures/ci/docker/arch.Dockerfile:7` · **Effort**: 15min

> The "archlinux" image runs with "root" as the default user. Make sure it is safe here.

```Dockerfile
        3  # Source: template (base/tests/fixtures/ci/docker/arch.Dockerfile.j2)
        4  # Free: no
        5  # End SECTION: header
        6  # Clean-machine proof: project bootstrap + canonical make verbs on Arch Linux.
>>>     7  FROM archlinux:base
        8  
        9  SHELL ["/bin/bash", "-o", "pipefail", "-c"]
       10  
       11  # === SECTION: base packages (managed) ===
```

**Decisão**: 

### 98 · ⚪ MINOR · CODE_SMELL · `docker:S7031`
**Local**: `tests/fixtures/ci/docker/arch.Dockerfile:13` · **Effort**: 5min

> Merge this RUN instruction with the consecutive ones.

```Dockerfile
        9  SHELL ["/bin/bash", "-o", "pipefail", "-c"]
       10  
       11  # === SECTION: base packages (managed) ===
       12  # Source: template (distro-specific package list)
>>>    13  RUN pacman -Syu --noconfirm --needed \
       14        bash ca-certificates curl git make base-devel icu \
       15      && pacman -Scc --noconfirm
       16  # End SECTION: base packages
       17  
```

**Decisão**: 

### 99 · ⚪ MINOR · VULNERABILITY · `docker:S6471`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:7` · **Effort**: 15min

> The "debian" image runs with "root" as the default user. Make sure it is safe here.

```Dockerfile
        3  # Source: template (base/tests/fixtures/ci/docker/debian.Dockerfile.j2)
        4  # Free: no
        5  # End SECTION: header
        6  # Clean-machine proof: project bootstrap + canonical make verbs on Debian.
>>>     7  FROM debian:bookworm-slim
        8  
        9  SHELL ["/bin/bash", "-o", "pipefail", "-c"]
       10  
       11  # === SECTION: base packages (managed) ===
```

**Decisão**: 

### 100 · ⚪ MINOR · CODE_SMELL · `docker:S7031`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:13` · **Effort**: 5min

> Merge this RUN instruction with the consecutive ones.

```Dockerfile
        9  SHELL ["/bin/bash", "-o", "pipefail", "-c"]
       10  
       11  # === SECTION: base packages (managed) ===
       12  # Source: template (distro-specific package list)
>>>    13  RUN apt-get update \
       14      && apt-get install -y --no-install-recommends \
       15         bash ca-certificates curl git make build-essential libicu-dev \
       16      && rm -rf /var/lib/apt/lists/*
       17  # End SECTION: base packages
```

**Decisão**: 

### 101 · ⚪ MINOR · CODE_SMELL · `docker:S7018`
**Local**: `tests/fixtures/ci/docker/debian.Dockerfile:14` · **Effort**: 5min

> Sort these package names alphanumerically.

```Dockerfile
       10  
       11  # === SECTION: base packages (managed) ===
       12  # Source: template (distro-specific package list)
       13  RUN apt-get update \
>>>    14      && apt-get install -y --no-install-recommends \
       15         bash ca-certificates curl git make build-essential libicu-dev \
       16      && rm -rf /var/lib/apt/lists/*
       17  # End SECTION: base packages
       18  
```

**Decisão**: 

### 102 · ⚪ MINOR · VULNERABILITY · `docker:S6471`
**Local**: `tests/fixtures/ci/docker/fedora.Dockerfile:7` · **Effort**: 15min

> The "fedora" image runs with "root" as the default user. Make sure it is safe here.

```Dockerfile
        3  # Source: template (base/tests/fixtures/ci/docker/fedora.Dockerfile.j2)
        4  # Free: no
        5  # End SECTION: header
        6  # Clean-machine proof: project bootstrap + canonical make verbs on Fedora.
>>>     7  FROM fedora:41
        8  
        9  SHELL ["/bin/bash", "-o", "pipefail", "-c"]
       10  
       11  # === SECTION: base packages (managed) ===
```

**Decisão**: 

### 103 · ⚪ MINOR · CODE_SMELL · `docker:S7031`
**Local**: `tests/fixtures/ci/docker/fedora.Dockerfile:13` · **Effort**: 5min

> Merge this RUN instruction with the consecutive ones.

```Dockerfile
        9  SHELL ["/bin/bash", "-o", "pipefail", "-c"]
       10  
       11  # === SECTION: base packages (managed) ===
       12  # Source: template (distro-specific package list)
>>>    13  RUN dnf install -y \
       14        bash ca-certificates curl git make gcc gcc-c++ libatomic libicu-devel \
       15      && dnf clean all
       16  # End SECTION: base packages
       17  
```

**Decisão**: 

### 104 · ⚪ MINOR · VULNERABILITY · `docker:S6471`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:7` · **Effort**: 15min

> The "ubuntu" image runs with "root" as the default user. Make sure it is safe here.

```Dockerfile
        3  # Source: template (base/tests/fixtures/ci/docker/ubuntu.Dockerfile.j2)
        4  # Free: no
        5  # End SECTION: header
        6  # Clean-machine proof: project bootstrap + canonical make verbs on Ubuntu.
>>>     7  FROM ubuntu:24.04
        8  
        9  SHELL ["/bin/bash", "-o", "pipefail", "-c"]
       10  
       11  # === SECTION: base packages (managed) ===
```

**Decisão**: 

### 105 · ⚪ MINOR · CODE_SMELL · `docker:S7031`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:13` · **Effort**: 5min

> Merge this RUN instruction with the consecutive ones.

```Dockerfile
        9  SHELL ["/bin/bash", "-o", "pipefail", "-c"]
       10  
       11  # === SECTION: base packages (managed) ===
       12  # Source: template (distro-specific package list)
>>>    13  RUN apt-get update \
       14      && apt-get install -y --no-install-recommends \
       15         bash ca-certificates curl git make build-essential libicu-dev \
       16      && rm -rf /var/lib/apt/lists/*
       17  # End SECTION: base packages
```

**Decisão**: 

### 106 · ⚪ MINOR · CODE_SMELL · `docker:S7018`
**Local**: `tests/fixtures/ci/docker/ubuntu.Dockerfile:14` · **Effort**: 5min

> Sort these package names alphanumerically.

```Dockerfile
       10  
       11  # === SECTION: base packages (managed) ===
       12  # Source: template (distro-specific package list)
       13  RUN apt-get update \
>>>    14      && apt-get install -y --no-install-recommends \
       15         bash ca-certificates curl git make build-essential libicu-dev \
       16      && rm -rf /var/lib/apt/lists/*
       17  # End SECTION: base packages
       18  
```

**Decisão**: 

