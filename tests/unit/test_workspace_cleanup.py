"""Real Git/filesystem behavior tests for public workspace cleanup utilities."""

from __future__ import annotations

from pathlib import Path

from flext_tests import c, m, p, tm, u


class TestsFlextTestsWorkspaceCleanup:
    """Exercise deterministic planning and guarded apply without test doubles."""

    @staticmethod
    def _git(repository: Path, *arguments: str) -> p.Cli.CommandOutput:
        result = u.Cli.run_raw((c.Infra.GIT, *arguments), cwd=repository)
        output = u.Tests.assert_success(result)
        tm.that(output.exit_code, eq=c.Cli.EXIT_CODE_SUCCESS)
        return output

    @classmethod
    def _repository(cls, root: Path, gitignore: str) -> Path:
        cls._git(root, "init", "--quiet")
        _ = u.Tests.assert_success(
            u.Cli.files_write_text(root / ".gitignore", gitignore)
        )
        return root

    @staticmethod
    def _write(path: Path, content: str = "residue") -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = u.Tests.assert_success(u.Cli.files_write_text(path, content))
        return path

    @staticmethod
    def _request(root: Path, *residues: str) -> p.Tests.WorkspaceCleanupRequest:
        policy = m.Tests.WorkspaceCleanupPolicy(
            residues=tuple(Path(residue) for residue in residues)
        )
        return m.Tests.WorkspaceCleanupRequest(workspace_root=root, policy=policy)

    def test_plan_is_deterministic_and_retains_source_request(
        self, tmp_path: Path
    ) -> None:
        """Return sorted declared residues while preserving request identity."""
        root = self._repository(tmp_path, ".cache/\n*.tmp\n")
        _ = self._write(root / ".cache" / "nested.bin")
        _ = self._write(root / "artifact.tmp")
        _ = self._write(root / "unlisted.tmp")
        request = self._request(root, "artifact.tmp", "missing", ".cache")

        plan = u.Tests.assert_success(u.Tests.workspace_cleanup_plan(request))

        tm.that(plan.request is request, eq=True)
        tm.that(
            tuple(candidate.relative_path.as_posix() for candidate in plan.candidates),
            eq=(".cache", "artifact.tmp"),
        )
        tm.that((root / "unlisted.tmp").exists(), eq=True)

    def test_apply_removes_only_the_exact_dry_run_plan(self, tmp_path: Path) -> None:
        """Delete planned residues without touching other ignored content."""
        root = self._repository(tmp_path, ".cache/\n*.tmp\n")
        _ = self._write(root / ".cache" / "nested.bin")
        _ = self._write(root / "artifact.tmp")
        _ = self._write(root / "unlisted.tmp")
        plan = u.Tests.assert_success(
            u.Tests.workspace_cleanup_plan(
                self._request(root, "artifact.tmp", ".cache")
            )
        )

        report = u.Tests.assert_success(u.Tests.workspace_cleanup_apply(plan))

        tm.that(report.plan is plan, eq=True)
        tm.that((root / ".cache").exists(), eq=False)
        tm.that((root / "artifact.tmp").exists(), eq=False)
        tm.that((root / "unlisted.tmp").exists(), eq=True)

    def test_apply_rejects_content_changed_after_dry_run(self, tmp_path: Path) -> None:
        """Preserve ignored WIP whose content changed after dry-run."""
        root = self._repository(tmp_path, "*.tmp\n")
        target = self._write(root / "artifact.tmp", "before")
        plan = u.Tests.assert_success(
            u.Tests.workspace_cleanup_plan(self._request(root, "artifact.tmp"))
        )
        # NOTE (multi-agent): prove the dry-run captured real filesystem state.
        tm.that(bool(plan.candidates[0].fingerprint), eq=True)
        _ = self._write(target, "important WIP after dry-run")

        result = u.Tests.workspace_cleanup_apply(plan)

        _ = u.Tests.assert_failure(result, "cleanup plan is stale")
        content = u.Tests.assert_success(u.Cli.files_read_text(target))
        tm.that(content, eq="important WIP after dry-run")

    def test_plan_rejects_non_ignored_candidate(self, tmp_path: Path) -> None:
        """Refuse a declared path that Git does not ignore."""
        root = self._repository(tmp_path, ".cache/\n")
        _ = self._write(root / "source.txt")

        result = u.Tests.workspace_cleanup_plan(self._request(root, "source.txt"))

        _ = u.Tests.assert_failure(result, "not ignored by Git")

    def test_plan_rejects_workspace_escape(self, tmp_path: Path) -> None:
        """Refuse parent traversal before inspecting the filesystem."""
        root = self._repository(tmp_path, "*.tmp\n")

        result = u.Tests.workspace_cleanup_plan(self._request(root, "../escape.tmp"))

        _ = u.Tests.assert_failure(result, "not normalized")

    def test_plan_rejects_symlink_escape(self, tmp_path: Path) -> None:
        """Refuse an ignored symlink whose resolved target is external."""
        root = self._repository(tmp_path, "escape\n")
        outside = tmp_path.parent / f"{tmp_path.name}-outside"
        outside.mkdir()
        (root / "escape").symlink_to(outside, target_is_directory=True)

        result = u.Tests.workspace_cleanup_plan(self._request(root, "escape"))

        _ = u.Tests.assert_failure(result, "escapes the workspace")

    def test_plan_rejects_tracked_ignored_content(self, tmp_path: Path) -> None:
        """Refuse clean tracked content even when an ignore rule matches."""
        root = self._repository(tmp_path, ".cache/\n")
        _ = self._write(root / ".cache" / "tracked.bin")
        self._git(root, "add", "-f", "--", ".cache/tracked.bin")
        self._git(
            root,
            "-c",
            "user.name=FLEXT Tests",
            "-c",
            "user.email=tests@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "tracked cleanup fixture",
            "--",
            ".cache/tracked.bin",
        )

        result = u.Tests.workspace_cleanup_plan(self._request(root, ".cache"))

        _ = u.Tests.assert_failure(result, "Git-tracked content")

    def test_plan_rejects_dirty_tracked_wip(self, tmp_path: Path) -> None:
        """Refuse dirty tracked work before evaluating tracked ownership."""
        root = self._repository(tmp_path, ".cache/\n")
        tracked = self._write(root / ".cache" / "tracked.bin")
        self._git(root, "add", "-f", "--", ".cache/tracked.bin")
        self._git(
            root,
            "-c",
            "user.name=FLEXT Tests",
            "-c",
            "user.email=tests@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "dirty cleanup fixture",
            "--",
            ".cache/tracked.bin",
        )
        _ = self._write(tracked, "important WIP")

        result = u.Tests.workspace_cleanup_plan(self._request(root, ".cache"))

        _ = u.Tests.assert_failure(result, "dirty or untracked WIP")

    def test_apply_rejects_plan_changed_after_dry_run(self, tmp_path: Path) -> None:
        """Refuse apply when Git state changed after the dry-run plan."""
        root = self._repository(tmp_path, ".cache/\n")
        _ = self._write(root / ".cache" / "artifact.bin")
        plan = u.Tests.assert_success(
            u.Tests.workspace_cleanup_plan(self._request(root, ".cache"))
        )
        self._git(root, "add", "-f", "--", ".cache/artifact.bin")

        result = u.Tests.workspace_cleanup_apply(plan)

        _ = u.Tests.assert_failure(result, "cleanup plan is stale")
        tm.that((root / ".cache" / "artifact.bin").exists(), eq=True)

    def test_plan_rejects_nested_targets(self, tmp_path: Path) -> None:
        """Refuse parent and child declarations that overlap."""
        root = self._repository(tmp_path, ".cache/\n")
        _ = self._write(root / ".cache" / "nested" / "artifact.bin")

        result = u.Tests.workspace_cleanup_plan(
            self._request(root, ".cache", ".cache/nested")
        )

        _ = u.Tests.assert_failure(result, "cleanup residues overlap")

    def test_apply_propagates_real_filesystem_deletion_failure(
        self, tmp_path: Path
    ) -> None:
        """Return the real deletion failure without swallowing it."""
        root = self._repository(tmp_path, "blocked/\n")
        blocked = root / "blocked"
        _ = self._write(blocked / "nested" / "artifact.bin")
        blocked.chmod(0o500)
        try:
            plan = u.Tests.assert_success(
                u.Tests.workspace_cleanup_plan(self._request(root, "blocked"))
            )
            result = u.Tests.workspace_cleanup_apply(plan)
        finally:
            blocked.chmod(0o700)

        _ = u.Tests.assert_failure(result, "cleanup deletion failed")
        tm.that(blocked.exists(), eq=True)
