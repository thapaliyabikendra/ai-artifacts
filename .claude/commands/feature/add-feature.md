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

## Mode Selection

Parse arguments to determine execution mode:

| Flag | Mode | Stages | Model | Speed |
|------|------|--------|-------|-------|
| `--minimal` | Fast CRUD | 3 only (implement) | sonnet | ~2 min |
| `--parallel` | Parallel docs | 1+2 parallel, then 3+4 | haiku/sonnet | ~5 min |
| (default) | Sequential | 1→2→3→4 | haiku/sonnet | ~8 min |
| `--full-review` | Complete | 1→2→3→4→5→6 | haiku/sonnet/sonnet | ~12 min |

## Workflow

```
--minimal:     Stage 3 only (direct implementation)
--parallel:    [Stage 1 + Stage 2] → [Stage 3 + Stage 4]
default:       Stage 1 → Stage 2 → Stage 3 → Stage 4
--full-review: Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6
```

---

## Execution: --minimal Mode

For simple CRUD features, skip documentation and use direct scaffolding.

Use Task tool with `subagent_type="abp-developer"` and `model="sonnet"`:

```
Implement CRUD feature for {feature-name}.

Requirements: {requirements-text}
Context: Read docs/architecture/README.md, docs/architecture/patterns.md
Skills: Apply abp-framework-patterns, efcore-patterns, fluentvalidation-patterns

Generate ALL files in a single pass:
1. Entity in Domain layer
2. DTOs in Application.Contracts
3. AppService interface + implementation
4. FluentValidation validator
5. EF Core configuration
6. Permissions

Build and verify: dotnet build api/*.slnx
```

**Output**: List created files. Done.

---

## Execution: --parallel Mode

Run documentation stages in parallel, then implementation stages in parallel.

### Phase 1: Parallel Documentation (haiku)

Launch BOTH agents simultaneously using multiple Task tool calls in ONE message:

**Agent 1** - Task with `subagent_type="business-analyst"`, `model="haiku"`:
```
Analyze requirements for {feature-name}. Be CONCISE.

Input: {requirements-text}
Output: docs/features/{feature-name}/requirements.md (max 100 lines)

Include ONLY:
- 3-5 user stories with acceptance criteria
- Entity properties list
- Business rules (BR-XXX format)
- Required permissions
```

**Agent 2** - Task with `subagent_type="backend-architect"`, `model="haiku"`:
```
Create technical design for {feature-name}. Be CONCISE.

Input: {requirements-text}
Context: Read docs/architecture/patterns.md
Output: docs/features/{feature-name}/technical-design.md (max 150 lines)

Include ONLY:
- Entity class skeleton
- DTO definitions (properties only)
- AppService interface
- API endpoints table
- Database columns table
```

### Phase 2: Parallel Implementation (sonnet)

After Phase 1 completes, launch BOTH agents simultaneously:

**Agent 3** - Task with `subagent_type="abp-developer"`, `model="sonnet"`:
```
Implement {feature-name} feature.

Input: docs/features/{feature-name}/technical-design.md
Skills: Apply abp-framework-patterns
Output: Source code files

Build and verify: dotnet build api/*.slnx
```

**Agent 4** - Task with `subagent_type="qa-engineer"`, `model="haiku"`:
```
Create test cases for {feature-name}. Be CONCISE.

Input: docs/features/{feature-name}/requirements.md
Output: docs/features/{feature-name}/test-cases.md (max 80 lines)

Include ONLY:
- Test case table (ID, Description, Expected Result)
- 8-10 test cases covering happy path, validation, authorization
```

---

## Execution: Default Mode (Sequential)

### Stage 1: Analysis & Requirements

Use Task tool with `subagent_type="business-analyst"`, `model="haiku"`:

```
Analyze requirements for {feature-name}. Be CONCISE.

Input: {requirements-text}
Context: Read docs/domain/*, docs/architecture/README.md

Output (max 150 lines total):
1. docs/domain/entities/{entity}.md - Entity definition
2. docs/features/{feature-name}/requirements.md - User stories
3. Update docs/domain/business-rules.md - Add BR-XXX rules
4. Update docs/domain/permissions.md - Add permissions

Skills: Apply requirements-engineering, domain-modeling patterns
```

**Checkpoint**: Requirements doc exists.

---

### Stage 2: Technical Design

Use Task tool with `subagent_type="backend-architect"`, `model="haiku"`:

```
Create technical design for {feature-name}. Be CONCISE.

Input: docs/features/{feature-name}/requirements.md
Context: Read docs/architecture/patterns.md
Output: docs/features/{feature-name}/technical-design.md (max 200 lines)

Include:
- Entity class with properties
- DTOs (output, input, list input)
- AppService interface
- API endpoints table
- Database schema (columns only)

Skills: Apply api-design-principles, efcore-patterns
```

**Checkpoint**: Technical design exists.

---

### Stage 3: Implementation

Use Task tool with `subagent_type="abp-developer"`, `model="sonnet"`:

```
Implement {feature-name} feature.

Input: docs/features/{feature-name}/technical-design.md
Context: Read docs/architecture/README.md
Skills: Apply abp-framework-patterns

Requirements:
- Follow project naming conventions
- All mutations have authorization
- All inputs have validators

Build: dotnet build api/*.slnx
```

**Checkpoint**: Build succeeds.

---

### Stage 4: Testing

Use Task tool with `subagent_type="qa-engineer"`, `model="haiku"`:

```
Create tests for {feature-name}. Be CONCISE.

Input: docs/features/{feature-name}/requirements.md, technical-design.md
Output:
1. docs/features/{feature-name}/test-cases.md (max 80 lines)
2. Test class file

Include 8-10 test cases: Happy path, Validation, Authorization.
Skills: Apply xunit-testing-patterns
```

**Checkpoint**: Test cases documented.

---

### Stage 5: Code Review (Optional)

Use Task tool with `subagent_type="code-reviewer"`, `model="haiku"`:

```
Review {feature-name} implementation. Be CONCISE.

Input: Source code files from Stage 3
Output: docs/features/{feature-name}/review-report.md (max 50 lines)

Checklist: ABP patterns, async usage, validation, authorization.
```

---

### Stage 6: Security Audit (Optional)

Use Task tool with `subagent_type="security-engineer"`, `model="haiku"`:

```
Security audit for {feature-name}. Be CONCISE.

Input: All source code
Output: docs/features/{feature-name}/security-audit.md (max 50 lines)

Checklist: Authorization, input validation, error handling.
```

---

## Output Summary

```
## Feature: {feature-name}

### Mode: {minimal|parallel|default|full-review}

### Files Created
[List files]

### Next Steps
1. Generate migration: /generate:migration Add{Entity}
2. Apply migration: Run DbMigrator
3. Run tests: dotnet test api/
```

## Options

| Option | Effect |
|--------|--------|
| `--minimal` | Implementation only, skip docs (~2 min) |
| `--parallel` | Parallel doc + impl stages (~5 min) |
| `--stage analyze` | Stage 1 only |
| `--stage design` | Stage 2 only |
| `--stage implement` | Stage 3 only |
| `--stage test` | Stage 4 only |
| `--stage review` | Stage 5 only |
| `--stage security` | Stage 6 only |
| `--review` | Stages 1-5 |
| `--security` | Stages 1-4 + 6 |
| `--full-review` | All stages 1-6 |
| `--dry-run` | Preview without files |

## Error Handling

On failure: Preserve completed outputs, report failed stage, suggest `--stage` to resume.
