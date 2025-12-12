---
name: adr
description: "Generate Architecture Decision Record for significant technical decisions"
args:
  - name: title
    description: "Short title for the decision"
    required: true
  - name: number
    description: "ADR number (auto-increment if not specified)"
    required: false
---

# Generate Architecture Decision Record

Title: **$ARGUMENTS.title**
Number: **$ARGUMENTS.number**

## Instructions

### Step 1: Determine ADR Number

If number not provided:
1. Search `docs/architecture/decisions/` for existing ADRs
2. Find highest number: `ADR-NNNN-*.md`
3. Increment by 1

### Step 2: Gather Context

Before writing, consider:
1. What problem are we solving?
2. What options were considered?
3. What constraints exist?
4. Who are the stakeholders?
5. What are the trade-offs?

### Step 3: Generate ADR

```markdown
# ADR-[NNNN]: [Title]

**Date**: [YYYY-MM-DD]
**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
**Deciders**: [List of people involved]
**Technical Story**: [Link to issue/story if applicable]

## Context

[Describe the context and problem statement. What is the issue that we're seeing that is motivating this decision?]

### Current State

[Describe how things work today, if applicable]

### Problem Statement

[Clear statement of the problem to be solved]

### Constraints

- [Constraint 1: e.g., Must work with existing database]
- [Constraint 2: e.g., Budget limitation]
- [Constraint 3: e.g., Timeline pressure]

## Decision Drivers

- [Driver 1: e.g., Performance requirements]
- [Driver 2: e.g., Maintainability]
- [Driver 3: e.g., Team expertise]
- [Driver 4: e.g., Cost]

## Considered Options

### Option 1: [Name]

[Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Effort**: Low | Medium | High
**Risk**: Low | Medium | High

### Option 2: [Name]

[Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Effort**: Low | Medium | High
**Risk**: Low | Medium | High

### Option 3: [Name]

[Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Effort**: Low | Medium | High
**Risk**: Low | Medium | High

## Decision

**Chosen Option**: [Option N] - [Name]

[Justify why this option was selected over others]

### Rationale

[Detailed explanation of why this decision was made, referencing the decision drivers]

## Consequences

### Positive

- [Positive consequence 1]
- [Positive consequence 2]

### Negative

- [Negative consequence 1 and how we'll mitigate it]
- [Negative consequence 2 and how we'll mitigate it]

### Neutral

- [Neutral observation]

## Implementation

### Action Items

- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

### Timeline

| Phase | Task | Target Date |
|-------|------|-------------|
| 1 | [Task] | [Date] |
| 2 | [Task] | [Date] |

### Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| [Metric 1] | [Value] | [Value] |
| [Metric 2] | [Value] | [Value] |

## Related Decisions

- [ADR-XXXX](./ADR-XXXX-title.md): [Relationship]
- [ADR-YYYY](./ADR-YYYY-title.md): [Relationship]

## References

- [Link to relevant documentation]
- [Link to research/analysis]
- [Link to similar decisions elsewhere]

---

## Review History

| Date | Reviewer | Decision |
|------|----------|----------|
| [Date] | [Name] | Proposed |
| [Date] | [Name] | Accepted |
```

### Step 4: Output

1. Write to `docs/architecture/decisions/ADR-[NNNN]-[slug].md`
2. Update ADR index if exists at `docs/architecture/decisions/README.md`
3. Summarize the decision to console

## ADR Lifecycle

```
Proposed → Accepted → [Deprecated | Superseded]
    ↓
  Rejected
```

### Status Definitions

| Status | Meaning |
|--------|---------|
| **Proposed** | Under discussion, not yet decided |
| **Accepted** | Decision made, in effect |
| **Deprecated** | No longer relevant, kept for history |
| **Superseded** | Replaced by newer ADR |
| **Rejected** | Considered but not accepted |

## Common ADR Topics

- Technology selection (database, framework, library)
- Architecture patterns (microservices, monolith, CQRS)
- API design decisions (REST, GraphQL, gRPC)
- Security approaches (auth, encryption)
- Data management (storage, caching, replication)
- Infrastructure choices (cloud, containers, serverless)

## Related Skills

- `technical-design-patterns` - Technical specifications
- `system-design-patterns` - Architecture patterns
