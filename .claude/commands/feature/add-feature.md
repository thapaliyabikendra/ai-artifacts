---
description: Add a new backend feature with full SDLC automation (requirements → design → implementation → tests)
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <feature-name> "<requirements>" [--stage <stage>] [--dry-run]
---

# Add Feature Command

Orchestrate end-to-end feature development using specialized agents with optimized parallel execution.

**Arguments**: $ARGUMENTS

## Pre-flight

**Project**: !`basename $(pwd)`
**Date**: !`date +%Y-%m-%d`

Required files:
- !`test -d docs/domain && echo "✓ docs/domain/" || echo "✗ MISSING: docs/domain/"`
- !`test -d docs/architecture && echo "✓ docs/architecture/" || echo "✗ MISSING: docs/architecture/"`

## Mode Selection

Parse arguments to determine execution mode:

| Flag | Mode | Stages | Parallelism | Speed |
|------|------|--------|-------------|-------|
| `--minimal` | Fast CRUD | 3 only | None | ~2 min |
| (default) | Optimized | 1+2 → 3+4 | Phase 1+2 parallel | ~5 min |
| `--sequential` | Sequential | 1→2→3→4 | None | ~8 min |
| `--full-review` | Complete | 1+2 → 3+4 → 5+6 | All phases parallel | ~8 min |

## Workflow Diagram

```
--minimal:     Stage 3 only (direct implementation)

default:       Phase 1: [Stage 1 + Stage 2*] ──→ Phase 2: [Stage 3 + Stage 4]
               (* Stage 2 generates interface contracts enabling parallel Phase 2)

--sequential:  Stage 1 → Stage 2 → Stage 3 → Stage 4

--full-review: Phase 1: [Stage 1 + Stage 2] → Phase 2: [Stage 3 + Stage 4] → Phase 3: [Stage 5 + Stage 6]
```

**Key Optimization**: Backend-architect (Stage 2) generates interface contracts + DTOs, enabling abp-developer and qa-engineer to run in TRUE parallel.

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

## Execution: Default Mode (Optimized Parallel)

### Phase 1: Parallel Analysis + Contract Generation

Launch BOTH agents simultaneously using multiple Task tool calls in ONE message:

**Agent 1** - Task with `subagent_type="business-analyst"`, `model="haiku"`:
```
Analyze requirements for {feature-name}. Be CONCISE.

Input: {requirements-text}
Context: Read docs/domain/*, docs/architecture/README.md

Output (max 150 lines total):
1. docs/domain/entities/{entity}.md - Entity definition
2. docs/features/{feature-name}/requirements.md - User stories with acceptance criteria
3. Update docs/domain/business-rules.md - Add BR-XXX rules
4. Update docs/domain/permissions.md - Add permissions

Skills: Apply requirements-engineering, domain-modeling
```

**Agent 2** - Task with `subagent_type="backend-architect"`, `model="haiku"`:
```
Create technical design AND generate contract scaffolding for {feature-name}.

Input: {requirements-text}
Context: Read docs/architecture/README.md, docs/architecture/patterns.md
Skills: Apply technical-design-patterns, abp-contract-scaffolding

Output Part 1 - Documentation:
- docs/features/{feature-name}/technical-design.md (max 200 lines)

Output Part 2 - Contract Scaffolding (REQUIRED):
Generate these files in the codebase:
1. api/src/{Project}.Application.Contracts/{Feature}/I{Entity}AppService.cs
2. api/src/{Project}.Application.Contracts/{Feature}/{Entity}Dto.cs
3. api/src/{Project}.Application.Contracts/{Feature}/Create{Entity}Dto.cs
4. api/src/{Project}.Application.Contracts/{Feature}/Update{Entity}Dto.cs
5. api/src/{Project}.Application.Contracts/{Feature}/Get{Entity}sInput.cs
6. api/src/{Project}.Application.Contracts/Permissions/{Entity}Permissions.cs (constants only)

The contract scaffolding enables parallel implementation and testing in Phase 2.
```

**Checkpoint**: Wait for BOTH agents to complete. Verify:
- requirements.md exists
- technical-design.md exists
- I{Entity}AppService.cs exists (contract scaffolding)

---

### Phase 2: Parallel Implementation + Testing

After Phase 1 completes, launch BOTH agents simultaneously:

**Agent 3** - Task with `subagent_type="abp-developer"`, `model="sonnet"`:
```
Implement {feature-name} feature using the generated contracts.

Input:
- docs/features/{feature-name}/technical-design.md
- api/src/{Project}.Application.Contracts/{Feature}/ (interface + DTOs already exist)

Skills: Apply abp-framework-patterns, efcore-patterns, fluentvalidation-patterns

Generate implementation files:
1. api/src/{Project}.Domain/{Feature}/{Entity}.cs - Entity
2. api/src/{Project}.Domain.Shared/{Feature}/{Entity}Consts.cs - Constants
3. api/src/{Project}.Application/{Feature}/{Entity}AppService.cs - Implementation
4. api/src/{Project}.Application/{Feature}/{Entity}ApplicationMappers.cs - Mapperly mapper
5. api/src/{Project}.Application/{Feature}/Create{Entity}DtoValidator.cs - Validator
6. api/src/{Project}.Application/{Feature}/Update{Entity}DtoValidator.cs - Validator
7. api/src/{Project}.EntityFrameworkCore/EntityTypeConfigurations/{Entity}Configuration.cs
8. Update DbContext with DbSet<{Entity}>
9. Update PermissionDefinitionProvider

DO NOT recreate interface or DTOs - they already exist from Phase 1.

Build and verify: dotnet build api/*.slnx
```

**Agent 4** - Task with `subagent_type="qa-engineer"`, `model="sonnet"`:
```
Create tests for {feature-name} using the generated contracts.

Input:
- docs/features/{feature-name}/requirements.md
- docs/features/{feature-name}/technical-design.md
- api/src/{Project}.Application.Contracts/{Feature}/ (interface + DTOs already exist)

Skills: Apply xunit-testing-patterns

Output:
1. docs/features/{feature-name}/test-cases.md (max 100 lines)
2. api/test/{Project}.TestBase/{Feature}/{Entity}TestData.cs
3. api/test/{Project}.TestBase/{Feature}/{Entity}TestDataSeedContributor.cs
4. api/test/{Project}.Application.Tests/{Feature}/{Entity}AppService_Tests.cs

Write tests against the INTERFACE (I{Entity}AppService) - implementation is being created in parallel.

Include 10-15 test cases:
- Happy path CRUD (5)
- Validation errors (3)
- Authorization checks (2)
- Edge cases (3-5)
```

**Checkpoint**: Wait for BOTH agents. Verify build succeeds.

---

## Execution: --sequential Mode

For cases where parallel execution causes issues.

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

### Stage 2: Technical Design + Contracts

Use Task tool with `subagent_type="backend-architect"`, `model="haiku"`:

```
Create technical design AND contract scaffolding for {feature-name}.

Input: docs/features/{feature-name}/requirements.md
Context: Read docs/architecture/patterns.md
Skills: Apply technical-design-patterns, abp-contract-scaffolding

Output:
1. docs/features/{feature-name}/technical-design.md (max 200 lines)
2. Contract scaffolding files (interface, DTOs, permissions)
```

**Checkpoint**: Technical design + contracts exist.

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
- Use existing contracts from Stage 2

Build: dotnet build api/*.slnx
```

**Checkpoint**: Build succeeds.

---

### Stage 4: Testing

Use Task tool with `subagent_type="qa-engineer"`, `model="sonnet"`:

```
Create tests for {feature-name}.

Input: docs/features/{feature-name}/requirements.md, technical-design.md
Output:
1. docs/features/{feature-name}/test-cases.md
2. Test data and seeder files
3. AppService test class

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

Checklist: ABP patterns, async usage, validation, authorization, code quality.
```

---

### Stage 6: Security Audit (Optional)

Use Task tool with `subagent_type="security-engineer"`, `model="haiku"`:

```
Security audit for {feature-name}. Be CONCISE.

Input: All source code
Output: docs/features/{feature-name}/security-audit.md (max 50 lines)

Checklist: Authorization, input validation, error handling, OWASP top 10.
```

---

## Execution: --full-review Mode

Run all 6 stages with maximum parallelism:

### Phase 1: Analysis + Design (parallel)
- Agent 1: business-analyst
- Agent 2: backend-architect (with contract generation)

### Phase 2: Implementation + Testing (parallel)
- Agent 3: abp-developer
- Agent 4: qa-engineer

### Phase 3: Review + Security (parallel)
- Agent 5: code-reviewer
- Agent 6: security-engineer

---

## Output Summary

```
## Feature: {feature-name}

### Mode: {minimal|default|sequential|full-review}
### Execution Time: {time}

### Files Created

**Documentation:**
- docs/features/{feature-name}/requirements.md
- docs/features/{feature-name}/technical-design.md
- docs/features/{feature-name}/test-cases.md

**Contracts (Phase 1):**
- api/src/.../Application.Contracts/{Feature}/I{Entity}AppService.cs
- api/src/.../Application.Contracts/{Feature}/{Entity}Dto.cs
- api/src/.../Application.Contracts/{Feature}/Create{Entity}Dto.cs
- api/src/.../Application.Contracts/{Feature}/Update{Entity}Dto.cs
- api/src/.../Application.Contracts/{Feature}/Get{Entity}sInput.cs

**Implementation (Phase 2):**
- api/src/.../Domain/{Feature}/{Entity}.cs
- api/src/.../Application/{Feature}/{Entity}AppService.cs
- api/src/.../Application/{Feature}/{Entity}ApplicationMappers.cs
- api/src/.../Application/{Feature}/*Validator.cs
- api/src/.../EntityFrameworkCore/.../{Entity}Configuration.cs

**Tests (Phase 2):**
- api/test/.../TestBase/{Feature}/{Entity}TestData.cs
- api/test/.../TestBase/{Feature}/{Entity}TestDataSeedContributor.cs
- api/test/.../Application.Tests/{Feature}/{Entity}AppService_Tests.cs

### Build Status: {PASSED|FAILED}

### Next Steps
1. Generate migration: /generate:migration Add{Entity}
2. Apply migration: dotnet run --project api/src/*.DbMigrator
3. Run tests: dotnet test api/
```

## Options

| Option | Effect |
|--------|--------|
| `--minimal` | Implementation only, skip docs (~2 min) |
| `--sequential` | Non-parallel execution (~8 min) |
| `--stage analyze` | Stage 1 only |
| `--stage design` | Stage 2 only (includes contract generation) |
| `--stage implement` | Stage 3 only |
| `--stage test` | Stage 4 only |
| `--stage review` | Stage 5 only |
| `--stage security` | Stage 6 only |
| `--review` | Default + Stage 5 |
| `--security` | Default + Stage 6 |
| `--full-review` | All stages with max parallelism |
| `--dry-run` | Preview without creating files |

## Error Handling

On failure:
1. Preserve completed outputs
2. Report failed stage and agent
3. Suggest `--stage {next}` to resume
4. If contract generation failed, use `--sequential` mode

## Performance Comparison

| Mode | Stages | Parallelism | Time |
|------|--------|-------------|------|
| --minimal | 1 | None | ~2 min |
| default (optimized) | 4 | Phase 1 + Phase 2 | ~5 min |
| --sequential | 4 | None | ~8 min |
| --full-review | 6 | All 3 phases | ~8 min |
