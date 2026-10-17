"""Behavioral coverage for the enforcement dispatcher public contract.

The end-to-end pytest11 pipeline (entry-point load -> ``pytest_configure``
filterwarnings -> ``pytest_warning_recorded`` -> ``pytest_terminal_summary``)
is driven inside a ``pytester`` subprocess sandbox and asserted on observable
outcomes plus the terminal summary the plugin promises to print. Subprocess
runs keep the real workspace untouched and prove entry-point loading without
any manual ``-p`` wiring.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib import import_module
from importlib.metadata import EntryPoint, distribution
from inspect import getattr_static
from pathlib import Path

import pytest
from flext_infra import config

from tests import c, tm, u


class TestsFlextTestsEnforcementPlugin:
    """Public contract of the enforcement dispatcher facade."""

    # Subprocess cases are reserved for contracts whose behavior is entry-point
    # discovery itself; ordinary dispatcher behavior stays in-process or loads
    # only its explicit owner plugins.

    @staticmethod
    def _declared_pytest_entries() -> tuple[EntryPoint, ...]:
        """Round-trip CUSTOM declarations through their installed distribution."""
        root = Path(__file__).resolve().parents[2]
        metadata = u.build_project_metadata(root, u.read_project_document_cached(root))
        document = tm.ok(u.Cli.toml_read_json(root / "pyproject.toml"))
        declared = u.Cli.toml_mapping_path(
            document,
            ("project", "entry-points", "pytest11"),
        )
        if declared is None:
            pytest.fail("The project must declare its pytest11 plugin objects")
        entries = tuple(
            entry
            for entry in distribution(metadata.project.name).entry_points
            if entry.group == "pytest11"
        )
        tm.that({entry.name: entry.value for entry in entries}, eq=declared)
        tm.that(bool(entries), eq=True)
        return entries

    @staticmethod
    def test_flext_pytest11_entrypoints_have_one_package_owner() -> None:
        """Installed plugin identities and targets match their CUSTOM owner."""
        TestsFlextTestsEnforcementPlugin._declared_pytest_entries()

    @staticmethod
    def test_flext_pytest11_entrypoint_load_defers_fixture_imports(
        pytester: pytest.Pytester,
    ) -> None:
        """Cold entry-point discovery does not pre-import measured product code."""
        entries = TestsFlextTestsEnforcementPlugin._declared_pytest_entries()
        selected = tuple((entry.name, entry.value) for entry in entries)
        probe = (
            "from importlib.metadata import entry_points\n"
            "import sys\n"
            "import pytest\n"
            "entries = {entry.name: entry for entry "
            "in entry_points(group='pytest11')}\n"
            "manager = pytest.PytestPluginManager()\n"
            f"for name, target in {selected!r}:\n"
            "    if entries[name].value != target:\n"
            "        raise RuntimeError(f'entry target drift: {name}')\n"
            "    manager.register(entries[name].load(), name=name)\n"
            "eager = sorted(\n"
            "    name for name in sys.modules\n"
            "    if name.startswith('flext_tests._fixtures')\n"
            ")\n"
            "if eager:\n"
            "    raise RuntimeError(f'eager fixture imports: {eager}')\n"
        )
        completed = pytester.runpython_c(probe)
        tm.that(completed.ret, eq=0)
        tm.that(completed.errlines, eq=[])

    @staticmethod
    def test_fixture_entrypoint_registers_the_class_object(
        pytestconfig: pytest.Config,
    ) -> None:
        """Installed metadata registers static hooks, not a module or factory."""
        for entry in TestsFlextTestsEnforcementPlugin._declared_pytest_entries():
            plugin = entry.load()
            tm.that(isinstance(plugin, type), eq=True)
            tm.that(callable(plugin), eq=True)
            tm.that(f"{plugin.__module__}:{plugin.__qualname__}", eq=entry.value)
            tm.that(
                isinstance(getattr_static(plugin, "pytest_configure"), staticmethod),
                eq=True,
            )
            tm.that(
                [
                    name
                    for name, value in vars(import_module(entry.module)).items()
                    if name.startswith("pytest_") and callable(value)
                ],
                eq=[],
            )
            tm.that(
                pytestconfig.pluginmanager.get_plugin(entry.name) is plugin, eq=True
            )
            implementations = [
                hook
                for hook in pytestconfig.hook.pytest_configure.get_hookimpls()
                if hook.plugin is plugin
            ]
            tm.that(
                [hook.function for hook in implementations],
                eq=[plugin.pytest_configure],
            )
        for module in c.Tests.FIXTURE_PLUGIN_MODULES:
            registered = pytestconfig.pluginmanager.get_plugin(module)
            tm.that(isinstance(registered, type), eq=True)
            tm.that(registered.__module__, eq=module)
        tm.that(
            pytestconfig.pluginmanager.hasplugin(c.Tests.CAPABILITY_PLUGIN_MODULE),
            eq=True,
        )

    @staticmethod
    @pytest.mark.slow
    @pytest.mark.parametrize("autoload", [False, True])
    def test_fixture_entrypoint_supports_explicit_loading_and_autoload(
        pytester: pytest.Pytester,
        *,
        autoload: bool,
    ) -> None:
        """Named loading preserves pre-parse options, fixtures and registry identity."""
        entries = TestsFlextTestsEnforcementPlugin._declared_pytest_entries()
        selected = tuple((entry.name, entry.value) for entry in entries)
        pytester.makeini("[pytest]\n")
        pytester.makepyfile(
            test_plugin=(
                "import pytest\n"
                "from importlib.metadata import entry_points\n"
                "from flext_tests import c, m, tm\n"
                "\n"
                "class TestsPluginConsumer:\n"
                "    @staticmethod\n"
                "    def test_registered(pytestconfig: pytest.Config,\n"
                "                        run_namespace: m.Tests.TestNamespace) -> None:\n"
                "        manager = pytestconfig.pluginmanager\n"
                "        before = manager.list_name_plugin()\n"
                f"        for name, target in {selected!r}:\n"
                "            entry = next(iter(entry_points(group='pytest11', name=name)))\n"
                "            tm.that(entry.value, eq=target)\n"
                "            plugin = manager.get_plugin(name)\n"
                "            tm.that(plugin is entry.load(), eq=True)\n"
                "            plugin.pytest_configure(pytestconfig)\n"
                "        tm.that(manager.list_name_plugin(), eq=before)\n"
                "        for module in c.Tests.FIXTURE_PLUGIN_MODULES:\n"
                "            owner = manager.get_plugin(module)\n"
                "            tm.that(isinstance(owner, type), eq=True)\n"
                "            tm.that(owner.__module__, eq=module)\n"
                "        tm.that(manager.hasplugin(\n"
                "            c.Tests.CAPABILITY_PLUGIN_MODULE), eq=True)\n"
                "        tm.that(bool(run_namespace.token), eq=True)\n"
                "        tm.that(pytestconfig.getoption('no_flext_enforce'), eq=True)\n"
                "        tm.that(pytestconfig.getoption('flext_enforce_strict'), eq=True)\n"
                "        tm.that(pytestconfig.getoption('flext_enforce_rules'), eq='probe')\n"
            ),
        )
        with u.Tests.env_vars_context(
            {} if autoload else {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
            vars_to_clear=("PYTEST_ADDOPTS", "PYTEST_DISABLE_PLUGIN_AUTOLOAD"),
        ):
            result = pytester.runpytest_subprocess(
                *(argument for entry in entries for argument in ("-p", entry.name)),
                "--no-flext-enforce",
                "--flext-enforce-strict",
                "--flext-enforce-rules=probe",
            )
        result.assert_outcomes(passed=1)
        tm.that(result.ret, eq=pytest.ExitCode.OK)

    @staticmethod
    @pytest.mark.slow
    @pytest.mark.parametrize("autoload", [False, True])
    def test_class_fixture_plugins_preserve_shared_lifecycle(
        pytester: pytest.Pytester,
        *,
        autoload: bool,
    ) -> None:
        """Cold consumers share sessions, reset every item and close on failure."""
        entries = TestsFlextTestsEnforcementPlugin._declared_pytest_entries()
        pytester.makeini("[pytest]\n")
        pytester.makepyfile(
            test_lifecycle="""
            from pathlib import Path
            import pytest
            from flext_core import FlextContainer, FlextSettings
            from flext_tests import FlextTestsSettings, m, p, tm

            class TestsFirstConsumer:
                previous = None
                runtime = None
                namespace = None

                @staticmethod
                @pytest.mark.parametrize('case', range(2))
                def test_shared(case: int, session_runtime: p.Tests.SessionRuntime,
                                run_namespace: m.Tests.TestNamespace,
                                test_namespace: m.Tests.TestNamespace,
                                temp_dir: Path, temp_file: Path) -> None:
                    current = (FlextSettings.fetch_global(),
                               FlextTestsSettings.fetch_global(), FlextContainer())
                    if TestsFirstConsumer.previous is not None:
                        for before, after in zip(TestsFirstConsumer.previous, current, strict=True):
                            tm.that(before is after, eq=False)
                        tm.that(session_runtime is TestsFirstConsumer.runtime, eq=True)
                        tm.that(run_namespace is TestsFirstConsumer.namespace, eq=True)
                    TestsFirstConsumer.previous = current
                    TestsFirstConsumer.runtime = session_runtime
                    TestsFirstConsumer.namespace = run_namespace
                    tm.that(temp_file.parent, eq=temp_dir)
                    tm.that(bool(test_namespace.token), eq=True)
                    tm.that(session_runtime.directory.is_dir(), eq=True)
                    Path(f'runtime-{case}').write_text(str(session_runtime.directory))

            class TestsSecondConsumer:
                @staticmethod
                def test_shared(session_runtime: p.Tests.SessionRuntime,
                                run_namespace: m.Tests.TestNamespace, reset_settings: None,
                                clean_container: p.Container, settings: FlextTestsSettings,
                                settings_factory) -> None:
                    tm.that(session_runtime is TestsFirstConsumer.runtime, eq=True)
                    tm.that(run_namespace is TestsFirstConsumer.namespace, eq=True)
                    tm.that(clean_container is not None, eq=True)
                    tm.that(isinstance(settings, FlextTestsSettings), eq=True)
                    created = settings_factory(FlextTestsSettings)
                    tm.that(created is FlextTestsSettings.fetch_global(), eq=True)
                    Path('runtime-second').write_text(str(session_runtime.directory))

                @staticmethod
                def test_failure_still_closes(session_runtime: p.Tests.SessionRuntime) -> None:
                    Path('runtime-failure').write_text(str(session_runtime.directory))
                    raise RuntimeError('intentional consumer failure')
            """,
        )
        with u.Tests.env_vars_context(
            {} if autoload else {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
            vars_to_clear=("PYTEST_ADDOPTS", "PYTEST_DISABLE_PLUGIN_AUTOLOAD"),
        ):
            result = pytester.runpytest_subprocess(
                *(argument for entry in entries for argument in ("-p", entry.name)),
                "-p",
                "no:randomly",
                "--no-flext-enforce",
            )
        result.assert_outcomes(passed=3, failed=1)
        tm.that(result.ret, eq=pytest.ExitCode.TESTS_FAILED)
        records = sorted(pytester.path.glob("runtime-*"))
        tm.that(len(records), eq=4)
        directories = {record.read_text() for record in records}
        tm.that(len(directories), eq=1)
        for directory in directories:
            tm.that(Path(directory).exists(), eq=False)

    @staticmethod
    @pytest.mark.slow
    def test_inactive_session_collects_only_consumer_tests(
        pytester: pytest.Pytester,
    ) -> None:
        """Shared fixtures register without activating enforcement in a sandbox."""
        pytester.makeini("[pytest]\n")
        pytester.makepyfile(
            test_probe=(
                "def test_probe() -> None:\n"
                "    raise RuntimeError('collection must not execute tests')\n"
            ),
        )
        result = pytester.runpytest_subprocess("--collect-only")
        tm.that(result.ret, eq=pytest.ExitCode.OK)
        result.stdout.fnmatch_lines(["*collected 1 item*", "*test_probe*"])
        result.stdout.no_fnmatch_line("*flext-enforce*")

    @staticmethod
    @pytest.mark.slow
    def test_inactive_enforcement_session_never_imports_flext_infra(
        pytester: pytest.Pytester,
    ) -> None:
        """The enforcement plugin alone keeps an ungoverned session off flext-infra.

        Mirrors the nested run of flext-infra's collection-manifest contract
        with only the flext-tests enforcement plugin loaded: flext-infra is
        reached through its CLI and its own pytest plugin, so an ungoverned
        enforcement session imports no ``flext_infra`` module at all.
        """
        pytester.makeini("[pytest]\n")
        pytester.makeconftest(
            "import sys\n"
            "\n"
            "\n"
            "def pytest_sessionfinish(session):\n"
            "    loaded = sorted(\n"
            "        name for name in sys.modules\n"
            "        if name.split('.')[0] == 'flext_infra'\n"
            "    )\n"
            "    if loaded:\n"
            "        raise RuntimeError(f'flext_infra imported: {loaded}')\n",
        )
        pytester.makepyfile(test_probe="def test_probe() -> None:\n    assert True\n")
        entries = TestsFlextTestsEnforcementPlugin._declared_pytest_entries()
        enforcement = next(
            entry
            for entry in entries
            if entry.name == config.Infra.tooling.tools.pytest.enforcement_plugin
        )
        with u.Tests.env_vars_context(
            {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
            vars_to_clear=("PYTEST_ADDOPTS",),
        ):
            result = pytester.runpytest_subprocess(
                "-p",
                enforcement.name,
                "--collect-only",
                "-q",
            )
        tm.that(result.ret, eq=pytest.ExitCode.OK)
        result.stdout.fnmatch_lines(["*test_probe*"])

    # ---- end-to-end pytest11 pipeline via pytester subprocess ----------------

    @staticmethod
    def _write_violation_module(pytester: pytest.Pytester) -> None:
        """Write a sandbox test that emits one runtime enforcement warning."""
        pytester.makepyfile(
            test_violation=(
                "import warnings\n"
                "\n"
                "from flext_core import e\n"
                "\n"
                "\n"
                "def test_emits_runtime_enforcement_warning() -> None:\n"
                "    warnings.warn(\n"
                '        "synthetic MRO violation",\n'
                "        e.MroViolation,\n"
                "        stacklevel=2,\n"
                "    )\n"
            ),
        )

    @classmethod
    def _make_workspace_sandbox(cls, pytester: pytest.Pytester) -> None:
        """Shape the sandbox as a FLEXT workspace root so auto-activation fires."""
        pytester.makeini("[pytest]\n")
        (pytester.path / "AGENTS.md").write_text("# sandbox workspace stub")
        (pytester.path / "flext-core").mkdir()
        (pytester.path / "flext-tests").mkdir()
        cls._write_violation_module(pytester)

    @pytest.mark.slow
    def test_dispatcher_records_warning_and_prints_summary(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Non-strict run captures the warning and reports it in the summary."""
        self._make_workspace_sandbox(pytester)
        result = pytester.runpytest_subprocess("--flext-enforce-rules=ENFORCE-022")
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.fnmatch_lines([
            "*flext-enforce*",
            "catalog active: 1 rules across 1 source kinds",
            "  runtime_warning: 1",
            "runtime warnings captured: 1",
        ])

    @pytest.mark.slow
    def test_strict_mode_promotes_warning_to_failure(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """--flext-enforce-strict promotes the configured warning to a failure."""
        self._make_workspace_sandbox(pytester)
        result = pytester.runpytest_subprocess(
            "--flext-enforce-rules=ENFORCE-022",
            "--flext-enforce-strict",
        )
        result.assert_outcomes(failed=1)
        result.stdout.fnmatch_lines([
            "*FlextMroViolation: synthetic MRO violation*",
            "runtime warnings captured: 0",
        ])

    @pytest.mark.slow
    def test_dispatcher_inactive_outside_workspace(
        self,
        pytester: pytest.Pytester,
    ) -> None:
        """Without workspace markers the dispatcher stays silent and passive."""
        pytester.makeini("[pytest]\n")
        self._write_violation_module(pytester)
        result = pytester.runpytest_subprocess()
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.no_fnmatch_line("*flext-enforce*")
        result.stdout.no_fnmatch_line("runtime warnings captured:*")

    @staticmethod
    @pytest.mark.slow
    def test_infra_rule_engine_boundary_runs_in_subprocess(
        pytester: pytest.Pytester,
    ) -> None:
        """Engine findings come through the public Result boundary.

        A rule the engine does not declare is a failure, never an empty scan.
        """
        pytester.makeini("[pytest]\n")
        pytester.makepyfile(
            test_public_boundary=(
                "from pathlib import Path\n"
                "\n"
                "from flext_tests import u\n"
                "\n"
                "\n"
                "class TestsPublicInfraRuleBoundary:\n"
                "    def test_engine_boundary(self, tmp_path: Path) -> None:\n"
                "        project = tmp_path / 'flext-contract-probe'\n"
                "        package = project / 'src' / 'flext_contract_probe'\n"
                "        package.mkdir(parents=True)\n"
                "        (package / '__init__.py').write_text(\n"
                '            \'"""Probe."""\\n\\n'
                "from __future__ import annotations\\n',\n"
                "            encoding='utf-8',\n"
                "        )\n"
                "        (project / 'pyproject.toml').write_text(\n"
                "            '[project]\\n'\n"
                "            'name = \\\"flext-contract-probe\\\"\\n'\n"
                "            'version = \\\"0.1.0\\\"\\n'\n"
                "            'dependencies = []\\n',\n"
                "            encoding='utf-8',\n"
                "        )\n"
                "        missing = u.Tests.infra_rule_findings(\n"
                "            project, required_rule_ids=frozenset({'no-such-rule'})\n"
                "        )\n"
                "        assert missing.failure\n"
                "        assert 'no-such-rule' in str(missing.error)\n"
                "        scanned = u.Tests.infra_rule_findings(\n"
                "            project, required_rule_ids=frozenset()\n"
                "        )\n"
                "        assert scanned.success\n"
            ),
        )
        result = pytester.runpytest_subprocess()
        result.assert_outcomes(passed=1)
