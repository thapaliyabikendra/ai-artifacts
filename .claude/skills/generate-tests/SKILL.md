---
name: generating-tests
description: "Generates xUnit tests for C#/.NET ABP Framework code using NSubstitute and Shouldly. Use when the user asks to generate tests, create test coverage, write unit tests, write integration tests, fill coverage gaps, or test a class or file. Supports AppServices, Validators, and HTTP API Controllers."
---

# Generating Tests

Generate xUnit tests for C#/.NET ABP Framework projects.

## Quick Start

```python
# Analyze source and generate tests
python scripts/generate_tests.py src/MyAppService.cs --type unit
```

## Workflow

Copy this checklist and track progress:

```
Test Generation Progress:
- [ ] Step 1: Locate source file
- [ ] Step 2: Analyze public methods and dependencies
- [ ] Step 3: Select template based on source type
- [ ] Step 4: Generate test file
- [ ] Step 5: Validate generated tests compile
```

**Step 1: Locate source**

| Input | Action |
|-------|--------|
| File path | Read directly |
| Class name | `find api/src -name "*ClassName*.cs" -type f` |
| `gaps` | Run `scripts/find_coverage_gaps.py` |

**Step 2: Analyze source**

Extract from each public method:
- Method signature (name, parameters, return type)
- Constructor dependencies → mock with `Substitute.For<T>()`
- `[Authorize]` attributes → add 401/403 test cases
- FluentValidation rules → add validation error tests

**Step 3: Select template**

| Source Pattern | Reference |
|----------------|-----------|
| `*AppService.cs` | See [reference/appservice-tests.md](reference/appservice-tests.md) |
| `*Validator.cs` | See [reference/validator-tests.md](reference/validator-tests.md) |
| `*Controller.cs` | See [reference/integration-tests.md](reference/integration-tests.md) |

**Step 4: Generate and write**

Output locations:
- **Unit tests**: `api/test/[Module].Application.Tests/[Class]Tests.cs`
- **Integration tests**: `api/test/[Module].HttpApi.Tests/[Class]IntegrationTests.cs`

**Step 5: Validate**

```bash
dotnet build api/test/[Module].Application.Tests/
```

If build fails, fix compilation errors and rebuild.

## Test Naming

Use pattern: `[Method]_[Scenario]_[Expected]`

| Example | Meaning |
|---------|---------|
| `Create_ValidInput_ReturnsDto` | Happy path |
| `Create_MissingName_ThrowsValidation` | Validation failure |
| `Get_NotFound_ThrowsException` | Entity not found |
| `Delete_Unauthorized_Returns403` | Permission denied |
