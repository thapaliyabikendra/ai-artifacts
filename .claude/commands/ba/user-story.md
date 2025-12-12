---
name: user-story
description: "Generate user story with acceptance criteria from feature description"
args:
  - name: feature
    description: "Feature name or brief description"
    required: true
  - name: role
    description: "Primary user role (default: user)"
    required: false
    default: "user"
  - name: output
    description: "Output path for user story"
    required: false
---

# Generate User Story

Feature: **$ARGUMENTS.feature**
Primary role: **$ARGUMENTS.role**

## Instructions

### Step 1: Gather Context

1. If feature exists in `docs/features/`, read existing requirements
2. Check `docs/domain/entities/` for related entities
3. Review `docs/domain/permissions.md` for applicable permissions
4. Identify related user stories if any exist

### Step 2: Generate User Story

Use INVEST criteria:
- **I**ndependent: Can be developed separately
- **N**egotiable: Details can be discussed
- **V**aluable: Delivers user value
- **E**stimable: Can be sized
- **S**mall: Fits in a sprint
- **T**estable: Has clear acceptance criteria

```markdown
# US-[XXX]: [Feature Title]

## Story

**As a** [role],
**I want to** [action/capability],
**So that** [benefit/value].

## Context

[Brief background on why this feature is needed and how it fits into the system]

## Acceptance Criteria

### AC-1: [Happy Path Scenario]
```gherkin
Given [initial context]
  And [additional context if needed]
When [action is performed]
Then [expected outcome]
  And [additional outcomes]
```

### AC-2: [Validation Scenario]
```gherkin
Given [context with invalid input]
When [action is attempted]
Then [validation error is shown]
  And [operation is not completed]
```

### AC-3: [Authorization Scenario]
```gherkin
Given a user without [required permission]
When they attempt to [action]
Then access is denied with 403 Forbidden
```

### AC-4: [Edge Case Scenario]
```gherkin
Given [edge condition]
When [action is performed]
Then [graceful handling occurs]
```

## Business Rules

| ID | Rule | Condition | Action |
|----|------|-----------|--------|
| BR-001 | [Rule name] | [When condition] | [Then action] |
| BR-002 | [Rule name] | [When condition] | [Then action] |

## Data Requirements

| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| [field] | [type] | Yes/No | [rules] | [notes] |

## UI/UX Notes

- [Key interaction patterns]
- [Form layout considerations]
- [Error message display]

## Dependencies

- **Requires**: [List prerequisite stories]
- **Blocks**: [List stories that depend on this]
- **Related**: [Associated stories]

## Technical Notes

- [API endpoint suggestions]
- [Database considerations]
- [Integration points]

## Priority & Sizing

- **Priority**: Must Have | Should Have | Could Have
- **Effort**: S (1-2d) | M (3-5d) | L (1-2w) | XL (2+w)
- **Risk**: Low | Medium | High

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]
```

### Step 3: Validate Quality

Checklist:
- [ ] Story follows "As a... I want... So that..." format
- [ ] At least 3 acceptance criteria defined
- [ ] Each AC uses Given/When/Then format
- [ ] Happy path, validation, and auth scenarios covered
- [ ] Business rules are numbered
- [ ] Data requirements specified
- [ ] Priority and effort assigned
- [ ] Dependencies identified

### Step 4: Output

1. Write to `$ARGUMENTS.output` if provided
2. Otherwise write to `docs/features/[feature]/US-[XXX].md`
3. Update feature index if exists

## Related Skills

- `requirements-engineering` - Full requirements patterns
- `domain-modeling` - Entity and rule analysis
