# Output Patterns

Patterns for producing consistent, high-quality skill outputs across different roles and deliverable types.

## Template Pattern

Provide templates for output format. Match strictness to requirements.

### Strict Templates (APIs, Data Formats)

```markdown
## Report Structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive Summary
[One-paragraph overview of key findings]

## Key Findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

### Flexible Templates (Adaptable Guidance)

```markdown
## Report Structure

Sensible default format (adapt as needed):

# [Analysis Title]

## Executive Summary
[Overview]

## Key Findings
[Adapt sections based on discoveries]

## Recommendations
[Tailor to specific context]

Adjust sections based on analysis type.
```

---

## Examples Pattern

For quality-dependent outputs, provide input/output pairs:

```markdown
## Commit Message Format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
```

---

## Before/After Transformation Pattern

Show concrete transformations:

```markdown
## Transformation Examples

**Before (problem):**
```css
.red-button-large {
  width: 200px;
  padding: 12px 24px;
  background: #FF0000;
  color: white;
}
```

**After (solution):**
```css
/* Structure */
.button {
  padding: 12px 24px;
}

.button--large {
  width: 200px;
}

/* Skin */
.button--primary {
  background: var(--color-primary);
  color: var(--color-primary-contrast);
}
```
```

---

## Deliverables Checklist Pattern

Define explicit outputs for skills producing multiple artifacts:

```markdown
## Output Deliverables

After execution, provide:

1. **Assessment Report:**
   - Current patterns found
   - Items needing attention
   - Priority ranking

2. **Action Plan:**
   - Step-by-step changes
   - Component-by-component breakdown
   - New file structure if needed

3. **Implementation:**
   - Actual code changes
   - Configuration updates
   - New files created

4. **Verification Checklist:**
   - [ ] Tests pass
   - [ ] No regressions
   - [ ] Documentation updated
```

---

## Classification/Inventory Pattern

Provide frameworks for organizing findings:

```markdown
## Classification Framework

Classify findings into groups:

**Category A (High Priority):**
- Characteristic 1
- Characteristic 2
- Examples: X, Y, Z

**Category B (Medium Priority):**
- Characteristic 1
- Characteristic 2
- Examples: A, B, C

**Category C (Low Priority):**
- Characteristic 1
- Characteristic 2
- Examples: D, E, F
```

---

## Context-Specific Notes Pattern

End skills with environment-specific constraints:

```markdown
## Important Notes for This Project

- Technology stack: [versions, frameworks]
- Existing patterns to follow: [conventions]
- Known limitations: [edge cases, compatibility]
- Testing requirements: [what to verify]
- Backwards compatibility: [migration concerns]
```

---

## Role-Specific Deliverables

### Backend Architect Deliverables

| Deliverable | Format | Template |
|-------------|--------|----------|
| Architecture Decision Record | Markdown | See below |
| API Specification | OpenAPI 3.x | YAML/JSON |
| Data Model | ERD + SQL | Diagram + DDL |
| System Diagram | Mermaid/PlantUML | Code |
| Technical Specification | Markdown | Structured doc |

**ADR Template:**
```markdown
# ADR-{NUMBER}: {TITLE}

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
[What is the issue that we're seeing that is motivating this decision?]

## Decision
[What is the change that we're proposing and/or doing?]

## Consequences
[What becomes easier or harder as a result of this decision?]

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

### Neutral
- [Side effect 1]
```

**API Specification Template:**
```yaml
openapi: 3.0.3
info:
  title: {API_NAME}
  version: {VERSION}
paths:
  /{resource}:
    get:
      summary: List {resources}
      responses:
        '200':
          description: Successful response
    post:
      summary: Create {resource}
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/{Resource}Create'
```

### Backend Developer Deliverables

| Deliverable | Format | Template |
|-------------|--------|----------|
| Service Class | C#/TypeScript | Class file |
| Controller | C#/TypeScript | API endpoints |
| DTOs | C#/TypeScript | Data contracts |
| Unit Tests | xUnit/Jest | Test files |
| Migration | SQL/EF | Migration file |

**Service Class Template (.NET):**
```csharp
public class {EntityName}AppService : ApplicationService, I{EntityName}AppService
{
    private readonly IRepository<{EntityName}, Guid> _repository;
    private readonly ILogger<{EntityName}AppService> _logger;

    public {EntityName}AppService(
        IRepository<{EntityName}, Guid> repository,
        ILogger<{EntityName}AppService> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public async Task<{EntityName}Dto> GetAsync(Guid id)
    {
        var entity = await _repository.GetAsync(id);
        return ObjectMapper.Map<{EntityName}, {EntityName}Dto>(entity);
    }

    // Additional CRUD methods...
}
```

### Frontend Developer Deliverables

| Deliverable | Format | Template |
|-------------|--------|----------|
| Component | TSX/JSX | React component |
| Styles | CSS/SCSS/Styled | Style file |
| Tests | Jest/RTL | Test file |
| Story | Storybook | Story file |
| Hook | TypeScript | Custom hook |

**React Component Template:**
```tsx
import React from 'react';
import styles from './{ComponentName}.module.css';

interface {ComponentName}Props {
  // Props definition
}

export const {ComponentName}: React.FC<{ComponentName}Props> = ({
  // Destructured props
}) => {
  return (
    <div className={styles.container}>
      {/* Component content */}
    </div>
  );
};

{ComponentName}.displayName = '{ComponentName}';
```

**Test Template:**
```tsx
import { render, screen } from '@testing-library/react';
import { {ComponentName} } from './{ComponentName}';

describe('{ComponentName}', () => {
  it('renders correctly', () => {
    render(<{ComponentName} />);
    expect(screen.getByRole('...')).toBeInTheDocument();
  });

  it('handles user interaction', () => {
    // Test user interactions
  });
});
```

### QA Engineer Deliverables

| Deliverable | Format | Template |
|-------------|--------|----------|
| Test Plan | Markdown | Structured doc |
| Test Cases | Gherkin/Markdown | Scenarios |
| Coverage Report | HTML/JSON | Report |
| Bug Report | Markdown | Issue template |
| E2E Script | Playwright/Cypress | Test file |

**Test Plan Template:**
```markdown
# Test Plan: {Feature Name}

## Scope
- In scope: [list]
- Out of scope: [list]

## Test Strategy
- Unit tests: {coverage target}%
- Integration tests: {scenarios}
- E2E tests: {critical paths}

## Test Cases

### TC-001: {Test Case Name}
**Priority:** High | Medium | Low
**Preconditions:** [setup required]
**Steps:**
1. [Action 1]
2. [Action 2]
**Expected Result:** [outcome]

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Action] |
```

**E2E Test Template (Playwright):**
```typescript
import { test, expect } from '@playwright/test';

test.describe('{Feature}', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should {expected behavior}', async ({ page }) => {
    // Arrange
    await page.fill('[data-testid="input"]', 'value');

    // Act
    await page.click('[data-testid="submit"]');

    // Assert
    await expect(page.locator('[data-testid="result"]'))
      .toBeVisible();
  });
});
```

### Security Engineer Deliverables

| Deliverable | Format | Template |
|-------------|--------|----------|
| Security Audit | Markdown | Report |
| Vulnerability Report | Markdown | Finding doc |
| Threat Model | Diagram + doc | STRIDE analysis |
| Remediation Plan | Markdown | Action items |
| Compliance Checklist | Markdown | Checklist |

**Security Finding Template:**
```markdown
# {Finding Title}

## Severity
Critical | High | Medium | Low | Informational

## CVSS Score
{score} ({vector string})

## Description
[What was found]

## Location
- File: `{path/to/file}`
- Line: {line numbers}
- Endpoint: `{API endpoint if applicable}`

## Proof of Concept
```
[Steps to reproduce or exploit code]
```

## Impact
[What could an attacker do with this vulnerability]

## Remediation
[Specific steps to fix]

**Before:**
```{language}
[Vulnerable code]
```

**After:**
```{language}
[Fixed code]
```

## References
- [CWE-XXX](link)
- [OWASP reference](link)
```

### DevOps Engineer Deliverables

| Deliverable | Format | Template |
|-------------|--------|----------|
| Dockerfile | Dockerfile | Container config |
| CI/CD Pipeline | YAML | Workflow file |
| IaC Template | Terraform/Pulumi | Infrastructure |
| Monitoring Config | YAML | Alerts/dashboards |
| Runbook | Markdown | Operations doc |

**Dockerfile Template:**
```dockerfile
# syntax=docker/dockerfile:1-labs
FROM mcr.microsoft.com/dotnet/aspnet:{VERSION}-alpine AS base
USER app
WORKDIR /app
EXPOSE 8080

FROM mcr.microsoft.com/dotnet/sdk:{VERSION} AS publish
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY --parents **/*.csproj /src/
RUN dotnet restore
COPY . .
RUN dotnet publish -c $BUILD_CONFIGURATION -o /app/publish

FROM base AS final
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "{Assembly}.dll"]
```

**GitHub Actions Template:**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '{VERSION}'
      - name: Restore
        run: dotnet restore
      - name: Build
        run: dotnet build --no-restore
      - name: Test
        run: dotnet test --no-build
```

### Product Manager Deliverables

| Deliverable | Format | Template |
|-------------|--------|----------|
| PRD | Markdown | Requirements doc |
| User Story | Markdown | Story format |
| Acceptance Criteria | Gherkin | BDD format |
| Release Notes | Markdown | Changelog |
| Roadmap | Markdown/Diagram | Timeline |

**User Story Template:**
```markdown
# {Story Title}

## User Story
As a {user type}
I want to {action}
So that {benefit}

## Acceptance Criteria

### Scenario 1: {Happy Path}
Given {context}
When {action}
Then {expected result}

### Scenario 2: {Edge Case}
Given {context}
When {action}
Then {expected result}

## Technical Notes
- [Implementation considerations]
- [Dependencies]

## Out of Scope
- [What this story does NOT include]
```

---

## Output Quality Guidelines

### Consistency Markers

Use consistent markers across outputs:

```markdown
Status indicators:
- ✅ Complete/Pass
- ❌ Failed/Issue
- ⚠️ Warning/Attention
- 🔄 In Progress
- ⏸️ Blocked/Paused

Priority levels:
- 🔴 Critical (P0)
- 🟠 High (P1)
- 🟡 Medium (P2)
- 🟢 Low (P3)
```

### Structured Outputs for Automation

When outputs may be parsed programmatically:

```markdown
## Machine-Readable Output

```json
{
  "status": "success",
  "summary": {
    "total": 10,
    "passed": 8,
    "failed": 2
  },
  "details": [
    {
      "id": "item-1",
      "status": "passed",
      "message": "Validation successful"
    }
  ]
}
```
```

### Human-Readable Summaries

Always include executive summaries for human consumption:

```markdown
## Executive Summary

**Overall Status:** ✅ Successful with minor issues

**Key Findings:**
1. [Most important finding]
2. [Second finding]
3. [Third finding]

**Recommended Actions:**
1. [Immediate action needed]
2. [Follow-up action]

**Next Steps:**
- [What happens next]
```
