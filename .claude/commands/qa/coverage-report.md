---
name: coverage-report
description: "Analyze test coverage gaps and generate actionable report"
args:
  - name: scope
    description: "Scope: module | feature | full"
    required: false
    default: "full"
  - name: module
    description: "Module name if scope is module"
    required: false
---

# Generate Coverage Report

Analyze test coverage for: **$ARGUMENTS.scope** $ARGUMENTS.module

## Instructions

### Step 1: Analyze Codebase Structure

1. Find all source files:
   ```
   api/src/**/*.cs (exclude Migrations, obj, bin)
   ```

2. Categorize by type:
   - Entities: `**/Entities/*.cs`
   - AppServices: `**/*AppService.cs`
   - Domain Services: `**/Services/*.cs`
   - Validators: `**/*Validator.cs`
   - Repositories: `**/Repositories/*.cs`

### Step 2: Find Existing Tests

1. Locate test files:
   ```
   api/test/**/*Tests.cs
   api/test/**/*Test.cs
   ```

2. Map tests to source:
   - By naming convention: `PatientAppServiceTests` -> `PatientAppService`
   - By imports/usings

### Step 3: Calculate Coverage

For each source file, determine:
- Has unit tests: Yes/No
- Has integration tests: Yes/No
- Test count: Number of test methods
- Methods tested: Count vs total public methods

### Step 4: Generate Report

```markdown
# Test Coverage Report

**Generated**: [DateTime]
**Scope**: [scope]
**Module**: [module if applicable]

## Executive Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Files with tests | X/Y (Z%) | >80% | :white_check_mark:/:x: |
| AppServices tested | X/Y (Z%) | 100% | :white_check_mark:/:x: |
| Validators tested | X/Y (Z%) | 100% | :white_check_mark:/:x: |
| Domain services tested | X/Y (Z%) | >90% | :white_check_mark:/:x: |

## Coverage by Layer

### Domain Layer
| File | Has Tests | Test Count | Coverage |
|------|-----------|------------|----------|
| Patient.cs | :white_check_mark: | 5 | Good |
| Doctor.cs | :x: | 0 | **GAP** |

### Application Layer
| AppService | Has Tests | Methods | Tested | Coverage |
|------------|-----------|---------|--------|----------|
| PatientAppService | :white_check_mark: | 5 | 4 | 80% |
| DoctorAppService | :x: | 4 | 0 | **0%** |

### Validators
| Validator | Has Tests | Rules | Tested |
|-----------|-----------|-------|--------|
| CreatePatientValidator | :white_check_mark: | 5 | 5 |
| UpdatePatientValidator | :x: | 3 | 0 |

## Critical Gaps (Priority 1)

These require immediate attention:

| Type | File | Reason |
|------|------|--------|
| AppService | DoctorAppService.cs | No tests, has CRUD operations |
| Validator | UpdatePatientValidator.cs | Validation untested |

## Suggested Tests

### DoctorAppService (0% coverage)

```csharp
public class DoctorAppServiceTests : ApplicationTestBase
{
    [Fact]
    public async Task GetListAsync_ReturnsPagedResult() { }

    [Fact]
    public async Task CreateAsync_ValidInput_CreatesDoctor() { }

    [Fact]
    public async Task CreateAsync_InvalidInput_ThrowsValidation() { }

    [Fact]
    public async Task UpdateAsync_ExistingDoctor_UpdatesFields() { }

    [Fact]
    public async Task DeleteAsync_ExistingDoctor_SoftDeletes() { }
}
```

## Recommendations

1. **Immediate Actions**
   - [ ] Add tests for [specific files]
   - [ ] Cover validation rules for [validators]

2. **Short-term Improvements**
   - [ ] Increase AppService coverage to 100%
   - [ ] Add integration tests for critical paths

3. **Test Infrastructure**
   - [ ] Create test data seeders for [entities]
   - [ ] Add test utilities for common scenarios
```

### Step 5: Output Actions

1. Print report to console
2. Optionally write to `docs/quality/coverage-report-[date].md`
3. List top 5 most critical gaps with specific test suggestions

## Related Skills

- `xunit-testing-patterns` - For writing the suggested tests
- `api-integration-testing` - For integration test patterns
- `test-data-generation` - For test data setup
