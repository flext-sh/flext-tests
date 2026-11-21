"""Behavioral coverage for the enforcement dispatcher public contract.

The end-to-end pytest11 pipeline (entry-point load ->
``pytest_warning_recorded`` -> ``pytest_terminal_summary``)
is driven inside a ``pytester`` subprocess sandbox and asserted on observable
outcomes plus the terminal summary the plugin promises to print. Subprocess
runs keep the real workspace untouched. Discovery contracts retain installed
plugin autoloading; dispatcher-only consumers load their declared owner alone.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from importlib import import_module
from importlib.metadata import EntryPoint, distribution
from inspect import getattr_static
from pathlib import Path

import pytest
from flext_infra import config

from tests import c, e, m, t, tm, u


class TestsFlextTestsEnforcementPlugin:
    """Public contract of the enforcement dispatcher facade."""

    FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "enforcement"

    # Subprocess cases are reserved for contracts whose behavior is entry-point
    # discovery itself; ordinary dispatcher behavior stays in-process or loads
    # only its explicit owner plugins.

    @classmethod
    def _render(
        cls,
        destination: Path,
        template: str,
        values: Mapping[str, str] | None = None,
    ) -> Path:
        """Render one scenario template from the fleet fixture root.

        Returns:
            The written destination path.

        """
        rendered = u.Cli.template_render(
            cls.FIXTURES / template,
            m.Tests.TemplateContext(values=dict(values or {})),
        ).unwrap()
        destination.write_text(rendered, encoding="utf-8")
        return destination

    @classmethod
    def _write_pytest_ini(cls, pytester: t.Tests.Pytester, addopts: str = "") -> None:
        """Render the sandbox pytest configuration, with optional addopts."""
        cls._render(
            pytester.path / "pytest.ini",
            "pytest_ini.j2",
            {"addopts": addopts},
        )

    @staticmethod
    def _declared_pytest_entries() -> tuple[EntryPoint, ...]:
        """Round-trip CUSTOM declarations through their installed distribution.

        Returns:
            tuple[EntryPoint, ...]: The installed pytest11 entry points.

        """
        root = Path(__file__).resolve().parents[2]
        metadata = u.build_project_metadata(root, u.read_project_document_cached(root))
        document = tm.ok(u.Cli.toml_read_json(root / c.PYPROJECT_FILENAME))
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
        tm.ok(bool(entries))
        return entries

    @staticmethod
    def test_flext_pytest11_entrypoints_have_one_package_owner() -> None:
        """Installed plugin identities and targets match their CUSTOM owner."""
        TestsFlextTestsEnforcementPlugin._declared_pytest_entries()

    @staticmethod
    def test_flext_pytest11_entrypoint_load_defers_fixture_imports(
        pytester: t.Tests.Pytester,
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
        pytestconfig: t.Tests.Config,
    ) -> None:
        """Installed metadata registers static hooks, not a module or factory."""
        for entry in TestsFlextTestsEnforcementPlugin._declared_pytest_entries():
            plugin = entry.load()
            tm.ok(isinstance(plugin, type))
            tm.ok(callable(plugin))
            tm.that(f"{plugin.__module__}:{plugin.__qualname__}", eq=entry.value)
            hook_name = "pytest_collection_modifyitems"
            tm.that(
                isinstance(getattr_static(plugin, hook_name), staticmethod),
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
                for hook in getattr(pytestconfig.hook, hook_name).get_hookimpls()
                if hook.plugin is plugin
            ]
            tm.that(
                [hook.function for hook in implementations],
                eq=[plugin.pytest_collection_modifyitems],
            )
        for module in c.Tests.FIXTURE_PLUGIN_MODULES:
            registered = pytestconfig.pluginmanager.get_plugin(module)
            tm.ok(registered is not None)
            tm.that(type(registered).__module__, eq=module)
        tm.that(
            pytestconfig.pluginmanager.hasplugin(c.Tests.CAPABILITY_PLUGIN_MODULE),
            eq=True,
        )

    @staticmethod
    @c.Tests.MARK.slow
    @c.Tests.MARK.parametrize("autoload", [False, True])
    def test_fixture_entrypoint_supports_explicit_loading_and_autoload(
        pytester: t.Tests.Pytester,
        *,
        autoload: bool,
    ) -> None:
        """Named loading preserves pre-parse options, fixtures and registry identity."""
        entries = TestsFlextTestsEnforcementPlugin._declared_pytest_entries()
        selected = tuple((entry.name, entry.value) for entry in entries)
        TestsFlextTestsEnforcementPlugin._write_pytest_ini(pytester)
        TestsFlextTestsEnforcementPlugin._render(
            pytester.path / "test_plugin.py",
            "plugin_consumer.py.j2",
            {"selected": repr(selected)},
        )
        with u.Tests.env_vars_context(
            {}
            if autoload
            else {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": c.ParserBooleanToken.ONE},
            vars_to_clear=("PYTEST_ADDOPTS", "PYTEST_DISABLE_PLUGIN_AUTOLOAD"),
        ):
            result = u.Tests.pytest_subprocess(
                pytester,
                *(argument for entry in entries for argument in ("-p", entry.name)),
                "--no-flext-enforce",
                "--flext-enforce-strict",
                "--flext-enforce-rules=probe",
            )
        result.assert_outcomes(passed=1)
        tm.that(result.ret, eq=c.Tests.ExitCode.OK)

    @staticmethod
    @c.Tests.MARK.slow
    @c.Tests.MARK.parametrize("autoload", [False, True])
    def test_class_fixture_plugins_preserve_shared_lifecycle(
        pytester: t.Tests.Pytester,
        *,
        autoload: bool,
    ) -> None:
        """Cold consumers share sessions, reset every item and close on failure.

        Settings roots keep one published identity and reload their sources in
        place per item; the DI container is rebuilt per item.
        """
        entries = TestsFlextTestsEnforcementPlugin._declared_pytest_entries()
        TestsFlextTestsEnforcementPlugin._write_pytest_ini(pytester)
        TestsFlextTestsEnforcementPlugin._render(
            pytester.path / "test_lifecycle.py",
            "lifecycle_consumer.py.j2",
        )
        with u.Tests.env_vars_context(
            {}
            if autoload
            else {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": c.ParserBooleanToken.ONE},
            vars_to_clear=("PYTEST_ADDOPTS", "PYTEST_DISABLE_PLUGIN_AUTOLOAD"),
        ):
            result = u.Tests.pytest_subprocess(
                pytester,
                *(argument for entry in entries for argument in ("-p", entry.name)),
                "-p",
                "no:randomly",
                "--no-flext-enforce",
            )
        result.assert_outcomes(passed=3, failed=1)
        tm.that(result.ret, eq=c.Tests.ExitCode.TESTS_FAILED)
        records = sorted(pytester.path.glob("runtime-*"))
        tm.that(len(records), eq=4)
        directories = {record.read_text() for record in records}
        tm.that(len(directories), eq=1)
        for directory in directories:
            tm.fail(Path(directory).exists())

    @staticmethod
    @c.Tests.MARK.slow
    def test_inactive_session_collects_only_consumer_tests(
        pytester: t.Tests.Pytester,
    ) -> None:
        """Shared fixtures register without activating enforcement in a sandbox."""
        TestsFlextTestsEnforcementPlugin._write_pytest_ini(pytester)
        TestsFlextTestsEnforcementPlugin._render(
            pytester.path / "test_probe.py",
            "probe_collection.py.j2",
        )
        result = u.Tests.pytest_subprocess(pytester, "--collect-only")
        tm.that(result.ret, eq=c.Tests.ExitCode.OK)
        result.stdout.fnmatch_lines(["*collected 1 item*", "*test_probe*"])
        result.stdout.no_fnmatch_line("*flext-enforce*")

    @staticmethod
    @c.Tests.MARK.slow
    def test_inactive_enforcement_session_never_imports_flext_infra(
        pytester: t.Tests.Pytester,
    ) -> None:
        """The enforcement plugin alone keeps an ungoverned session off flext-infra.

        Mirrors the nested run of flext-infra's collection-manifest contract
        with only the flext-tests enforcement plugin loaded: flext-infra is
        reached through its CLI and its own pytest plugin, so an ungoverned
        enforcement session imports no ``flext_infra`` module at all.
        """
        TestsFlextTestsEnforcementPlugin._write_pytest_ini(pytester)
        TestsFlextTestsEnforcementPlugin._render(
            pytester.path / "conftest.py",
            "probe_imports_conftest.py.j2",
        )
        pytester.makepyfile(test_probe="def test_probe() -> None:\n    assert True\n")
        entries = TestsFlextTestsEnforcementPlugin._declared_pytest_entries()
        enforcement = next(
            entry
            for entry in entries
            if entry.name == config.Infra.tooling.tools.pytest.enforcement_plugin
        )
        with u.Tests.env_vars_context(
            {"PYTEST_DISABLE_PLUGIN_AUTOLOAD": c.ParserBooleanToken.ONE},
            vars_to_clear=("PYTEST_ADDOPTS",),
        ):
            result = u.Tests.pytest_subprocess(
                pytester,
                "-p",
                enforcement.name,
                "--collect-only",
                "-q",
            )
        tm.that(result.ret, eq=c.Tests.ExitCode.OK)
        result.stdout.fnmatch_lines(["*test_probe*"])

    # ---- end-to-end pytest11 pipeline via pytester subprocess ----------------

    @classmethod
    def _write_violation_module(cls, pytester: t.Tests.Pytester) -> None:
        """Write a warning consumer with only its installed dispatcher selected."""
        cls._write_pytest_ini(
            pytester,
            "--disable-plugin-autoload -p "
            f"{config.Infra.tooling.tools.pytest.enforcement_plugin}",
        )
        cls._render(
            pytester.path / "test_violation.py",
            "warning_consumer.py.j2",
            {"category": e.MroViolationError.__name__},
        )

    @c.Tests.MARK.slow
    def test_dispatcher_inactive_outside_workspace(
        self,
        pytester: t.Tests.Pytester,
    ) -> None:
        """Without workspace markers the dispatcher stays silent and passive."""
        self._write_violation_module(pytester)
        result = u.Tests.pytest_subprocess(pytester)
        result.assert_outcomes(passed=1, warnings=1)
        result.stdout.no_fnmatch_line("*flext-enforce*")
        result.stdout.no_fnmatch_line("runtime warnings captured:*")

    @staticmethod
    @c.Tests.MARK.slow
    def test_infra_rule_engine_boundary_returns_results(tmp_path: Path) -> None:
        """Engine findings come through the public Result boundary.

        A rule the engine does not declare is a failure, never an empty scan.
        """
        project = tmp_path / "flext-contract-probe"
        package = project / "src" / "flext_contract_probe"
        package.mkdir(parents=True)
        (package / "__init__.py").write_text(
            '"""Probe."""\n\nfrom __future__ import annotations\n',
            encoding="utf-8",
        )
        (project / "pyproject.toml").write_text(
            '[project]\nname = "flext-contract-probe"\nversion = "0.1.0"\n'
            "dependencies = []\n",
            encoding="utf-8",
        )
        u.Cli.run_checked([*c.Cli.GIT_INIT_COMMAND, str(project)]).unwrap()
        (project / ".venv").symlink_to(Path(sys.prefix), target_is_directory=True)
        missing = u.Tests.infra_rule_findings(
            project, required_rule_ids=frozenset({"no-such-rule"})
        )
        tm.fail(missing, has="no-such-rule")
        tm.ok(u.Tests.infra_rule_findings(project, required_rule_ids=frozenset()))
