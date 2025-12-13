# Stage Prompt Templates

Detailed prompt templates for each stage of feature development.

## Stage 1: Requirements Analysis

**Agent**: `product-architect`

### Prompt Template

```
Create a requirements document for the {feature-name} feature.

## Input
- Feature Name: {feature-name}
- Raw Requirements: {requirements-text}

## Context Files (Read First)
1. docs/project-context.md - Project conventions
2. docs/entity-glossary.md - Existing entities and roles
3. docs/business-requirements.md - Existing patterns

## Apply Skills
- `requirements-engineering` skill for user story format and acceptance criteria

## Output
Create: docs/features/{feature-name}/requirements.md

Include:
- Feature Overview (business context, success metrics)
- User Stories (US-XXX format with priority)
- Acceptance Criteria (Given/When/Then)
- Data Model (fields, types, constraints)
- Business Rules (BR-XXX format)
- Permission Requirements
- Open Questions
```

### Validation Criteria

- [ ] At least 3 user stories
- [ ] Each story has acceptance criteria
- [ ] Data model includes field types and constraints
- [ ] Permissions align with existing roles in entity-glossary.md

---

## Stage 2: Technical Design

**Agent**: `backend-architect`

### Prompt Template

```
Create a technical design for the {feature-name} feature.

## Input
- docs/features/{feature-name}/requirements.md

## Context Files (Read First)
1. docs/project-context.md - Paths, naming conventions, code patterns
2. docs/technical-specification.md - Existing architecture patterns

## Apply Skills
- `api-design-principles` skill for REST endpoint design
- `postgresql` skill for schema design

## Output
Create: docs/features/{feature-name}/technical-design.md

Include:
- Entity Design (C# class with base class from project-context.md)
- DTOs (following naming conventions)
- AppService Interface
- Permissions (following naming convention)
- API Endpoints table
- Database Schema (columns, types, indexes)
- File Locations (using path templates)
```

### Validation Criteria

- [ ] Entity inherits correct base class
- [ ] DTOs follow naming convention
- [ ] API endpoints cover all CRUD operations
- [ ] Permissions follow project naming pattern
- [ ] File paths match project-context.md templates

---

## Stage 3: Implementation

**Agent**: `abp-developer`

### Prompt Template

```
Implement the {feature-name} feature.

## Input
- docs/features/{feature-name}/technical-design.md

## Context Files (Read First)
1. docs/project-context.md - Paths, build commands
2. Existing similar features in codebase (for patterns)

## Apply Skills
- `abp-framework-patterns` skill for entity, service patterns, and CRUD templates
  - See `references/crud-templates.md` for code generation templates

## Requirements
- Follow entity base class from project-context.md
- Follow naming conventions from project-context.md
- All list endpoints support pagination
- All mutations have authorization attributes
- All input DTOs have validators

## Output
1. Create all files specified in technical-design.md
2. Provide list of created/modified files
3. Provide migration command
4. Verify build succeeds
```

### Validation Criteria

- [ ] Entity file created in Domain layer
- [ ] DTOs created in Application.Contracts
- [ ] AppService created in Application layer
- [ ] Validator created for input DTOs
- [ ] DbContext updated with DbSet
- [ ] Build succeeds

---

## Stage 4: Testing

**Agent**: `qa-engineer`

### Prompt Template

```
Create tests for the {feature-name} feature.

## Input
- docs/features/{feature-name}/requirements.md
- docs/features/{feature-name}/technical-design.md

## Context Files (Read First)
1. docs/project-context.md - Test paths, testing libraries
2. Existing test files (for patterns)

## Apply Skills
- `xunit-testing-patterns` skill for test structure

## Part 1: Test Documentation
Create: docs/features/{feature-name}/test-cases.md

Test categories:
- Happy Path (CRUD operations)
- Validation (required fields, formats, lengths)
- Authorization (permissions, roles)
- Edge Cases (not found, empty list, soft delete)

## Part 2: Test Implementation
Create test files using paths from project-context.md:
- {Entity}TestData.cs - Test constants
- {Entity}TestDataSeedContributor.cs - Test data seeder
- {Entity}AppService_Tests.cs - xUnit tests
```

### Validation Criteria

- [ ] At least 10 test cases documented
- [ ] Test cases cover all 4 categories
- [ ] Test files created in correct paths
- [ ] Tests compile successfully

---

## Prompt Variables

| Variable | Source | Example |
|----------|--------|---------|
| `{feature-name}` | Command argument | `patient-management` |
| `{requirements-text}` | Command argument | `"CRUD for patients..."` |
| `{Entity}` | Derived from feature-name | `Patient` |
| `{entity}` | Derived from feature-name | `patient` |

---

## Stage 5: Code Review (Optional)

**Agent**: `abp-code-reviewer`

### Prompt Template

```
Review the implemented code for the {feature-name} feature.

## Input
- docs/features/{feature-name}/technical-design.md
- All source code files created in Stage 3

## Context Files (Read First)
1. docs/project-context.md - Coding standards, patterns
2. Existing similar features (for consistency)

## Apply Skills
- `code-review-excellence` skill for review patterns
- `abp-framework-patterns` skill for ABP-specific checks

## Review Checklist
- [ ] Entities inherit correct ABP base classes
- [ ] AppServices follow naming conventions
- [ ] DTOs have FluentValidation validators
- [ ] Authorization attributes on all endpoints
- [ ] Async/await used correctly
- [ ] Logging for important operations
- [ ] No hardcoded values

## Output
Create: docs/features/{feature-name}/review-report.md

Include:
- Summary (1-2 sentences)
- Critical Issues (must fix)
- Major Issues (should fix)
- Minor Issues/Suggestions
- What's Good (positive feedback)
- Verdict: Approve | Approve with comments | Request changes
```

### Validation Criteria

- [ ] No critical issues
- [ ] All ABP patterns followed
- [ ] Code is consistent with existing codebase
- [ ] Recommendations are actionable

---

## Stage 6: Security Audit (Optional)

**Agent**: `security-engineer`

### Prompt Template

```
Perform security audit for the {feature-name} feature.

## Input
- docs/features/{feature-name}/requirements.md
- docs/features/{feature-name}/technical-design.md
- All source code files

## Context Files (Read First)
1. docs/project-context.md - Security requirements
2. docs/entity-glossary.md - Sensitive data identification

## Apply Skills
- `security-patterns` skill for STRIDE and OWASP checks

## Security Checklist
- [ ] All endpoints have [Authorize] attributes
- [ ] Permissions defined for all operations
- [ ] Input validation on all DTOs
- [ ] No PII in logs
- [ ] Error messages don't expose internals
- [ ] SQL uses parameterized queries (EF Core)

## Output
Create: docs/features/{feature-name}/security-audit.md

Include:
- Threat Model (STRIDE analysis)
- Vulnerability Findings (if any)
- OWASP Top 10 Compliance
- Recommendations
- Risk Level: Critical | High | Medium | Low
```

### Validation Criteria

- [ ] No critical/high vulnerabilities
- [ ] All authorization in place
- [ ] Input validation complete
- [ ] Threat model documented

---

## Skills Referenced

| Skill | Used In Stages |
|-------|----------------|
| `requirements-engineering` | Stage 1 |
| `api-design-principles` | Stage 2 |
| `postgresql` | Stage 2 |
| `abp-framework-patterns` | Stage 3 (includes CRUD templates) |
| `xunit-testing-patterns` | Stage 4 |
| `code-review-excellence` | Stage 5 |
| `security-patterns` | Stage 6 |
