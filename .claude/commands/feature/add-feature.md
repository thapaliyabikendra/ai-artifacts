---
description: Add a new backend feature with full SDLC automation (requirements → design → implementation → tests)
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <feature-name> "<requirements>" [--stage <stage>] [--dry-run]
---

# Add Feature Command

Orchestrate end-to-end feature development using specialized agents.

**Arguments**: $ARGUMENTS

## Pre-flight

**Project**: !`basename $(pwd)`
**Date**: !`date +%Y-%m-%d`

Required files:
- !`test -d docs/domain && echo "✓ docs/domain/" || echo "✗ MISSING: docs/domain/"`
- !`test -d docs/architecture && echo "✓ docs/architecture/" || echo "✗ MISSING: docs/architecture/"`

## Workflow

Apply `feature-development-workflow` skill for stage details.

```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6
Analyze   Design   Implement  Test      Review    Security
& Require                               (optional) (optional)
```

## Execution

### Stage 1: Analysis & Requirements (business-analyst)

Use Task tool with `subagent_type="business-analyst"`:

```
Analyze requirements and update domain for {feature-name}.

Input: {requirements-text}
Context: Read docs/domain/*, docs/architecture/README.md

Phase 1 - Domain Analysis:
- Identify affected entities (new, modified)
- Check business rule conflicts
- List required permissions

Phase 2 - Domain Updates:
- Create/update docs/domain/entities/{entity}.md
- Add business rules to docs/domain/business-rules.md (BR-XXX format)
- Add permissions to docs/domain/permissions.md
- Update role mappings in docs/domain/roles.md

Phase 3 - Requirements:
- Create docs/features/{feature-name}/requirements.md
- Include user stories with Given/When/Then acceptance criteria

Phase 4 - Impact Report:
- Create docs/features/{feature-name}/impact-analysis.md
- Document all changes, risks, affected components

Skills: Apply requirements-engineering, domain-modeling patterns
```

**Checkpoint**:
- Domain files updated (if needed)
- 3+ user stories with acceptance criteria
- Impact analysis complete

---

### Stage 2: Technical Design (backend-architect)

Use Task tool with `subagent_type="backend-architect"`:

```
Create technical design for {feature-name}.

Input:
- docs/features/{feature-name}/requirements.md
- docs/features/{feature-name}/impact-analysis.md
- docs/domain/entities/

Context: Read docs/architecture/README.md, docs/architecture/patterns.md
Skills: Apply api-design-principles, postgresql patterns
Output: docs/features/{feature-name}/technical-design.md

Include: Entity design, DTOs, AppService interface, permissions, API endpoints, schema.
```

**Checkpoint**: Verify entity, DTOs, and API endpoints defined.

---

### Stage 3: Implementation (abp-developer)

Use Task tool with `subagent_type="abp-developer"`:

```
Implement {feature-name} feature.

Input: docs/features/{feature-name}/technical-design.md
Context: Read docs/architecture/README.md, examine existing features
Skills: Apply abp-framework-patterns
Output: Source code files per technical design

Requirements:
- Follow project naming conventions
- All endpoints support pagination
- All mutations have authorization
- All inputs have validators
```

**Checkpoint**: Entity, AppService, DTOs created. Build succeeds.

---

### Stage 4: Testing (qa-engineer)

Use Task tool with `subagent_type="qa-engineer"`:

```
Create tests for {feature-name} feature.

Input:
- docs/features/{feature-name}/requirements.md
- docs/features/{feature-name}/technical-design.md

Context: Read docs/architecture/README.md, examine existing tests
Skills: Apply xunit-testing-patterns
Output:
- docs/features/{feature-name}/test-cases.md
- Test code files

Categories: Happy path, Validation, Authorization, Edge cases.
```

**Checkpoint**: 10+ test cases. Tests compile.

---

### Stage 5: Code Review (Optional)

Use Task tool with `subagent_type="code-reviewer"`:

```
Review implemented code for {feature-name} feature.

Input: All source code files from Stage 3
Context: Read docs/architecture/patterns.md, technical-design.md
Skills: Apply code-review-excellence patterns
Output: docs/features/{feature-name}/review-report.md

Checklist: ABP patterns, async usage, validation, authorization, logging.
```

**Checkpoint**: No critical issues. Recommendations documented.

---

### Stage 6: Security Audit (Optional)

Use Task tool with `subagent_type="security-engineer"`:

```
Perform security audit for {feature-name} feature.

Input: All artifacts and source code
Context: Read docs/domain/permissions.md, docs/domain/entities/
Skills: Apply security-patterns (STRIDE, OWASP Top 10)
Output: docs/features/{feature-name}/security-audit.md

Checklist: Authorization, input validation, PII protection, error handling.
```

**Checkpoint**: No critical/high vulnerabilities. Security controls verified.

---

## Output Summary

```
## Feature: {feature-name}

### Domain Changes
- Entities: [new/modified count]
- Business Rules: [new/modified count]
- Permissions: [new count]

### Documents
- docs/features/{feature-name}/requirements.md
- docs/features/{feature-name}/impact-analysis.md
- docs/features/{feature-name}/technical-design.md
- docs/features/{feature-name}/test-cases.md
- docs/features/{feature-name}/review-report.md (if --review)
- docs/features/{feature-name}/security-audit.md (if --security)

### Code
[List created files]

### Next Steps
1. Review impact-analysis.md for stakeholder sign-offs
2. Run migration (see docs/architecture/README.md)
3. Build solution
4. Run tests
```

## Options

| Option | Effect |
|--------|--------|
| `--stage analyze` | Stage 1 only (analysis + requirements) |
| `--stage design` | Stage 2 only |
| `--stage implement` | Stage 3 only |
| `--stage test` | Stage 4 only |
| `--stage review` | Stage 5 only |
| `--stage security` | Stage 6 only |
| `--review` | Stages 1-5 (includes code review) |
| `--security` | Stages 1-4 + 6 (includes security audit) |
| `--full-review` | Stages 1-6 (all stages) |
| `--dry-run` | Preview without files |

## Error Handling

On failure: Preserve completed outputs, report failed stage, suggest `--stage` to resume.
