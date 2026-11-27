# Workspace Check Report

Generated: 2026-11-09 03:16:51 UTC
Check phase: complete
Execution: INCOMPLETE
Projects reached: 1/1

## Summary

| Project | Status | Findings |
| --- |---:|---:|
| flext-tests | INCOMPLETE | 2 |

## Details

### flext-tests
Root: `/home/marlonsc/flext/flext-tests`
- lint: PASS (0 issues)
  - Native output receipt: [lint.raw.log](file:///home/marlonsc/flext/flext-tests/.reports/check/a666de4e-1cb8-4f67-8f28-e03f20c8fc1a/flext-tests/lint.raw.log)
- pyrefly: FAIL (2 issues)
  - src/flext_tests/_utilities/_files/info.py:113:26 [bad-argument-type] Argument `flext_tests._protocols.filesystem.FlextTestsProtocolsFilesystem.ContentMeta | None` is not assignable to parameter `content_meta` with type `flext_tests._models.filesystem.FlextTestsModelsFilesystem.ContentMeta | None` in function `flext_tests._models.filesystem.FileInfo.__init__`
  - tests/unit/test_service_base.py:42:13 [bad-argument-type] Argument `flext_infra._models.deps_tool_config.FlextInfraModelsDepsToolConfig.ToolConfigDocument` is not assignable to parameter `document` with type `flext_infra._protocols.deps_tool_config.FlextInfraProtocolsDepsToolConfig.ToolConfigDocument` in function `flext_infra._utilities.native_tooling.FlextInfraUtilitiesNativeTooling.native_tool_setting`
  `FlextInfraModelsDepsToolConfig.ToolConfigDocument.tools` has type `FlextInfraModelsDepsToolConfig.ToolConfigTools`, which is not assignable to `() -> FlextInfraProtocolsDepsToolConfig.ToolConfigTools`, the property getter for `ToolConfigDocument.tools`
  - Native output receipt: [pyrefly.raw.log](file:///home/marlonsc/flext/flext-tests/.reports/check/a666de4e-1cb8-4f67-8f28-e03f20c8fc1a/flext-tests/pyrefly.raw.log)
