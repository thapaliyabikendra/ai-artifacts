---
name: test-plan
description: "Generate comprehensive test plan from requirements or feature specification"
args:
  - name: feature
    description: "Feature name or path to requirements file"
    required: true
  - name: type
    description: "Test scope: unit | integration | e2e | all"
    required: false
    default: "all"
  - name: output
    description: "Output path for test plan"
    required: false
---

# Generate Test Plan

Generate a comprehensive test plan for: **$ARGUMENTS.feature**
Test scope: **$ARGUMENTS.type**

## Instructions

### Step 1: Gather Context

1. Read requirements/feature file if path provided
2. If feature name only, search for:
   - `docs/features/{feature}/requirements.md`
   - `docs/features/{feature}/design.md`
   - Related entity definitions in `docs/domain/entities/`
3. Identify all user stories and acceptance criteria

### Step 2: Identify Test Categories

For each user story, identify:

| Category | Coverage Target | Framework |
|----------|----------------|-----------|
| Unit Tests | Business logic, validators, domain services | xUnit + NSubstitute |
| Integration Tests | AppServices, repositories, EF queries | xUnit + WebApplicationFactory |
| E2E Tests | Critical user flows | Playwright |

### Step 3: Generate Test Plan

Use this template:

```markdown
# Test Plan: [Feature Name]

## Overview
- **Feature**: [Name]
- **Version**: 1.0
- **Created**: [Date]
- **Test Scope**: [unit/integration/e2e/all]

## Test Summary

| Type | Test Count | Coverage Target |
|------|------------|-----------------|
| Unit | [N] | >80% business logic |
| Integration | [N] | All AppService methods |
| E2E | [N] | Critical paths only |

## User Stories Coverage

### US-001: [Story Title]

**Acceptance Criteria:**
- [ ] AC1: [Description]
- [ ] AC2: [Description]

**Test Cases:**

| ID | Type | Scenario | Given | When | Then | Priority |
|----|------|----------|-------|------|------|----------|
| TC-001 | Unit | [name] | [setup] | [action] | [expected] | P1 |
| TC-002 | Integration | [name] | [setup] | [action] | [expected] | P1 |
| TC-003 | E2E | [name] | [setup] | [action] | [expected] | P2 |

### US-002: [Story Title]
[Repeat structure...]

## Unit Test Specifications

### [ClassName]Tests.cs
Location: `test/[Module].Application.Tests/`

```csharp
public class [ClassName]Tests : [Module]ApplicationTestBase
{
    // TC-001: [Test scenario]
    [Fact]
    public async Task [MethodName]_[Scenario]_[ExpectedResult]()
    {
        // Arrange
        // Act
        // Assert
    }
}
```

## Integration Test Specifications

### [FeatureName]IntegrationTests.cs
Location: `test/[Module].HttpApi.Tests/`

```csharp
public class [FeatureName]IntegrationTests : [Module]HttpApiTestBase
{
    // TC-002: [Test scenario]
    [Fact]
    public async Task [Endpoint]_[Scenario]_Returns[StatusCode]()
    {
        // Arrange
        // Act: var response = await Client.GetAsync("/api/...");
        // Assert
    }
}
```

## E2E Test Specifications

### [feature-name].spec.ts
Location: `e2e/tests/`

```typescript
test.describe('[Feature Name]', () => {
    // TC-003: [Test scenario]
    test('[user action] should [expected result]', async ({ page }) => {
        // Arrange: Navigate, login if needed
        // Act: User interactions
        // Assert: Verify outcomes
    });
});
```

## Test Data Requirements

| Entity | Test Data | Seeder Location |
|--------|-----------|-----------------|
| [Entity1] | [Description] | TestDataSeeder.cs |
| [Entity2] | [Description] | TestDataSeeder.cs |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [High/Medium/Low] | [Strategy] |

## Dependencies

- [ ] Test database configured
- [ ] Test data seeders implemented
- [ ] Mocks for external services ready
```

### Step 4: Output

1. Write test plan to `$ARGUMENTS.output` if provided, otherwise to `docs/features/{feature}/test-plan.md`
2. Summarize:
   - Total test cases generated
   - Coverage by type
   - Any gaps or concerns identified

## Quality Checklist

- [ ] Every acceptance criterion has at least one test
- [ ] Happy path and error cases covered
- [ ] Authorization scenarios included
- [ ] Edge cases identified
- [ ] Test data requirements documented
- [ ] Test file locations specified
