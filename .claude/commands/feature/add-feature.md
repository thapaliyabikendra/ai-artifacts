---
description: Add a new backend feature with full SDLC automation (requirements → design → implementation → tests)
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <feature-name> "<requirements>" [--fast] [--minimal] [--full-review] [--stage <stage>]
---

# Add Feature Command

Orchestrate end-to-end feature development using specialized agents with optimized progressive handoff.

**Arguments**: $ARGUMENTS

## Pre-flight

**Project**: !`basename $(pwd)`
**Date**: !`date +%Y-%m-%d`

Required files:
- !`test -d docs/domain && echo "✓ docs/domain/" || echo "✗ MISSING: docs/domain/"`
- !`test -d docs/architecture && echo "✓ docs/architecture/" || echo "✗ MISSING: docs/architecture/"`

## Mode Selection

| Flag | Mode | Flow | Time |
|------|------|------|------|
| `--minimal` | Direct implementation | Stage 3 only | ~2 min |
| `--fast` | Skip BA, Arch parses requirements | Arch → [Dev + QA] | ~3 min |
| (default) | Progressive handoff | BA(entity) → Arch ∥ BA(reqs) → [Dev + QA] | ~4 min |
| `--full-review` | Complete with reviews | All stages with parallelism | ~6 min |

## Workflow Diagram

```
--minimal:     [abp-developer only]

--fast:        backend-architect ──→ [abp-developer + qa-engineer]
               (parses requirements directly)

default:       BA(entity+perms) ─┬──→ [backend-architect + qa-data] ──→ [abp-developer + qa-tests]
               🟢 ENTITY_READY   │    🟢 CONTRACTS_READY                 (parallel impl)
                                 │
               BA(reqs+rules) ───┘    (continues in background, non-blocking)

--full-review: [default] ──→ [abp-code-reviewer + security-engineer]
```

**Parallelism Gains**:
- Phase 1b: Architect + QA-Data run in parallel (previously sequential)
- QA-Data starts ~45s earlier (on entity, not contracts)
- BA secondary outputs are non-blocking

**Key**: Progressive handoff means Arch starts as soon as entity definition exists, doesn't wait for full BA completion.

## Signal Protocol

Agents communicate completion through explicit signals. The orchestrator monitors these to start dependent agents immediately.

| Signal | Emitted By | Triggers |
|--------|------------|----------|
| `🟢 ENTITY_READY` | BA | Architect can start contracts |
| `🟢 CONTRACTS_READY` | Architect | Developer + QA-Tests can start |
| `🟢 ENTITY_READY` | BA | QA-Data can start (parallel with Architect) |

**Agent Instructions**: After completing a critical output, emit the signal:
```
🟢 ENTITY_READY: docs/domain/entities/{entity}.md created
```

**Orchestrator Behavior**:
- On `ENTITY_READY`: Launch Architect AND QA-Data in parallel
- On `CONTRACTS_READY`: Launch Developer + QA-Tests in parallel
- Don't wait for BA secondary outputs (requirements.md, business-rules.md)

---

## Execution: --minimal Mode

For simple CRUD features, skip documentation and use direct scaffolding.

Use Task tool with `subagent_type="abp-developer"` and `model="sonnet"`:

```
Implement CRUD feature for {feature-name}.

Requirements: {requirements-text}
Context: Read CLAUDE.md, docs/architecture/README.md
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

## Execution: --fast Mode

Skip business-analyst when requirements are detailed. Backend-architect parses requirements directly.

### Step 1: Design + Contracts

Use Task tool with `subagent_type="backend-architect"`, `model="haiku"`:

```
Create technical design AND generate contracts for {feature-name}.

Requirements (parse directly): {requirements-text}
Context: Read CLAUDE.md, docs/architecture/README.md, docs/domain/permissions.md
Skills: Apply technical-design-patterns, abp-contract-scaffolding

Output:
1. docs/features/{feature-name}/technical-design.md (max 150 lines)
2. docs/domain/entities/{entity}.md (entity definition)
3. Application.Contracts/{Feature}/I{Entity}AppService.cs
4. Application.Contracts/{Feature}/{Entity}Dto.cs
5. Application.Contracts/{Feature}/Create{Entity}Dto.cs
6. Application.Contracts/{Feature}/Update{Entity}Dto.cs
7. Application.Contracts/{Feature}/Get{Entity}sInput.cs
8. Application.Contracts/Permissions/{Entity}Permissions.cs
9. Update docs/domain/permissions.md
```

**Checkpoint**: Contracts exist.

### Step 2: Parallel Implementation + Testing

Launch BOTH agents simultaneously using multiple Task tool calls in ONE message:

**Agent A** - Task with `subagent_type="abp-developer"`, `model="sonnet"`:
```
Implement {feature-name} using generated contracts.

Input: Application.Contracts/{Feature}/ (interface + DTOs exist)
Skills: Apply abp-framework-patterns, efcore-patterns, fluentvalidation-patterns

Generate:
1. Domain/{Feature}/{Entity}.cs
2. Domain.Shared/{Feature}/{Entity}Consts.cs
3. Application/{Feature}/{Entity}AppService.cs
4. Application/{Feature}/{Entity}ApplicationMappers.cs
5. Application/{Feature}/*Validator.cs
6. EntityFrameworkCore/EntityTypeConfigurations/{Entity}Configuration.cs
7. Update DbContext, PermissionDefinitionProvider

DO NOT recreate contracts - they exist.
Build: dotnet build api/*.slnx
```

**Agent B** - Task with `subagent_type="qa-engineer"`, `model="sonnet"`:
```
Create tests for {feature-name} using generated contracts.

Input: Application.Contracts/{Feature}/ (interface + DTOs exist)
Skills: Apply xunit-testing-patterns

Output:
1. test/TestBase/{Feature}/{Entity}TestData.cs
2. test/TestBase/{Feature}/{Entity}TestDataSeedContributor.cs
3. test/Application.Tests/{Feature}/{Entity}AppService_Tests.cs

Write tests against INTERFACE - implementation is parallel.
```

**Checkpoint**: Both complete. Build succeeds.

---

## Execution: Default Mode (Progressive Handoff)

### Phase 1a: Entity Definition (Priority Output)

Use Task tool with `subagent_type="business-analyst"`, `model="haiku"`:

```
Analyze {feature-name} and produce PRIORITY outputs first.

Requirements: {requirements-text}
Context: Read docs/domain/*, docs/architecture/README.md

PRIORITY OUTPUT (produce these FIRST, max 60 lines total):
1. docs/domain/entities/{entity}.md - Entity definition with:
   - Properties table (Type, Required, Constraints)
   - API Access table (Permission names)
2. Update docs/domain/permissions.md - Add permission entries

After writing entity.md, IMMEDIATELY emit signal:
🟢 ENTITY_READY: docs/domain/entities/{entity}.md

Then continue with secondary outputs (don't block on these):

SECONDARY OUTPUT:
3. docs/features/{feature-name}/requirements.md - User stories (max 80 lines)
4. Update docs/domain/business-rules.md - Add BR-XXX rules

DO NOT generate:
- ANALYSIS.md (redundant summary)
- impact-analysis.md (use --impact flag if needed)

Skills: Apply requirements-engineering, domain-modeling
```

### Phase 1b: Contracts + QA-Data (Parallel on ENTITY_READY)

On `🟢 ENTITY_READY` signal, launch BOTH agents in parallel:

**Agent A** - Task with `subagent_type="backend-architect"`, `model="haiku"`:
```
Generate technical design AND contracts for {feature-name}.

Input: docs/domain/entities/{entity}.md (just created)
Context: docs/architecture/README.md, docs/domain/permissions.md
Skills: Apply technical-design-patterns, abp-contract-scaffolding

Output:
1. docs/features/{feature-name}/technical-design.md (max 150 lines)
2. Application.Contracts/{Feature}/I{Entity}AppService.cs
3. Application.Contracts/{Feature}/{Entity}Dto.cs
4. Application.Contracts/{Feature}/Create{Entity}Dto.cs
5. Application.Contracts/{Feature}/Update{Entity}Dto.cs
6. Application.Contracts/{Feature}/Get{Entity}sInput.cs
7. Application.Contracts/Permissions/{Entity}Permissions.cs

After writing contracts, emit signal:
🟢 CONTRACTS_READY: Application.Contracts/{Feature}/
```

**Agent B** - Task with `subagent_type="qa-engineer"`, `model="haiku"`:
```
Create test data scaffolding for {feature-name}.

Input: docs/domain/entities/{entity}.md (entity properties)
Skills: Apply xunit-testing-patterns, test-data-generation

Output (test data only - tests come later):
1. test/TestBase/{Feature}/{Entity}TestData.cs - Test constants
2. test/TestBase/{Feature}/{Entity}TestDataSeedContributor.cs - Data seeder

Use entity properties from entity.md. Does NOT need contracts.
```

**Checkpoint**: Contracts exist AND test data scaffolding ready. BA may still be completing (that's OK).

### Phase 2: Implementation + Tests (Parallel on CONTRACTS_READY)

On `🟢 CONTRACTS_READY` signal, launch BOTH agents in parallel:

**Agent A** - Task with `subagent_type="abp-developer"`, `model="sonnet"`:
```
Implement {feature-name} using generated contracts.

Input:
- docs/features/{feature-name}/technical-design.md
- Application.Contracts/{Feature}/ (contracts exist)

Skills: Apply abp-framework-patterns, efcore-patterns, fluentvalidation-patterns

Generate implementation files:
1. Domain/{Feature}/{Entity}.cs
2. Domain.Shared/{Feature}/{Entity}Consts.cs
3. Application/{Feature}/{Entity}AppService.cs
4. Application/{Feature}/{Entity}ApplicationMappers.cs
5. Application/{Feature}/Create{Entity}DtoValidator.cs
6. Application/{Feature}/Update{Entity}DtoValidator.cs
7. EntityFrameworkCore/EntityTypeConfigurations/{Entity}Configuration.cs
8. Update DbContext with DbSet<{Entity}>
9. Update PermissionDefinitionProvider

DO NOT recreate contracts - they exist.
Build: dotnet build api/*.slnx
```

**Agent B** - Task with `subagent_type="qa-engineer"`, `model="sonnet"`:
```
Create tests for {feature-name}.

Input:
- docs/features/{feature-name}/requirements.md (if exists)
- docs/features/{feature-name}/technical-design.md
- Application.Contracts/{Feature}/ (contracts exist)
- test/TestBase/{Feature}/ (TestData + Seeder already exist from Phase 1b)

Skills: Apply xunit-testing-patterns

Output:
1. docs/features/{feature-name}/test-cases.md (max 80 lines)
2. test/Application.Tests/{Feature}/{Entity}AppService_Tests.cs

TestData and Seeder already exist - DO NOT recreate them.
Write tests against INTERFACE.
Include: Happy path (5), Validation errors (3), Auth checks (2), Edge cases (3).
```

**Checkpoint**: Both complete. Build succeeds.

---

## Execution: --full-review Mode

Run default mode, then add review phase.

### Phase 3: Parallel Review + Security

Launch BOTH agents simultaneously:

**Agent A** - Task with `subagent_type="abp-code-reviewer"`, `model="haiku"`:
```
Review {feature-name} backend implementation. Be CONCISE.

Input: All source code from Phase 2
Output: docs/features/{feature-name}/review-report.md (max 50 lines)

Checklist: ABP patterns, async usage, validation, authorization, naming.
```

**Agent B** - Task with `subagent_type="security-engineer"`, `model="haiku"`:
```
Security audit for {feature-name}. Be CONCISE.

Input: All source code from Phase 2
Output: docs/features/{feature-name}/security-audit.md (max 50 lines)

Checklist: Authorization, input validation, OWASP top 10, error handling.
```

---

## Output Summary

```
## Feature: {feature-name}

### Mode: {minimal|fast|default|full-review}
### Execution Time: {time}

### Files Created

**Documentation:**
- docs/domain/entities/{entity}.md
- docs/features/{feature-name}/requirements.md (default/full only)
- docs/features/{feature-name}/technical-design.md
- docs/features/{feature-name}/test-cases.md

**Contracts:**
- Application.Contracts/{Feature}/I{Entity}AppService.cs
- Application.Contracts/{Feature}/{Entity}Dto.cs
- Application.Contracts/{Feature}/Create{Entity}Dto.cs
- Application.Contracts/{Feature}/Update{Entity}Dto.cs
- Application.Contracts/{Feature}/Get{Entity}sInput.cs

**Implementation:**
- Domain/{Feature}/{Entity}.cs
- Domain.Shared/{Feature}/{Entity}Consts.cs
- Application/{Feature}/{Entity}AppService.cs
- Application/{Feature}/{Entity}ApplicationMappers.cs
- Application/{Feature}/*Validator.cs
- EntityFrameworkCore/EntityTypeConfigurations/{Entity}Configuration.cs

**Tests:**
- test/TestBase/{Feature}/{Entity}TestData.cs
- test/TestBase/{Feature}/{Entity}TestDataSeedContributor.cs
- test/Application.Tests/{Feature}/{Entity}AppService_Tests.cs

### Build Status: {PASSED|FAILED}

### Next Steps
1. Generate migration: /generate:migration Add{Entity}
2. Apply migration: dotnet run --project api/src/*.DbMigrator
3. Run tests: dotnet test api/
```

## Options Reference

| Option | Effect |
|--------|--------|
| `--minimal` | Implementation only, skip all docs (~2 min) |
| `--fast` | Skip BA, Arch parses requirements (~3 min) |
| `--stage analyze` | BA only |
| `--stage design` | Arch only (needs entity definition) |
| `--stage implement` | Dev only (needs contracts) |
| `--stage test` | QA only (needs contracts) |
| `--review` | Default + code review |
| `--security` | Default + security audit |
| `--full-review` | All stages with reviews (~6 min) |
| `--impact` | Generate impact-analysis.md (skipped by default) |
| `--dry-run` | Preview without creating files |

## Error Handling

On failure:
1. Preserve completed outputs
2. Report failed stage and agent
3. Suggest `--stage {next}` to resume
4. If progressive handoff failed, suggest `--fast` mode

## Performance Summary

| Mode | Stages | Parallelism | Time |
|------|--------|-------------|------|
| --minimal | 1 | None | ~2 min |
| --fast | 2 | Phase 2 parallel | ~2.5 min |
| default | 3 | Phase 1b + Phase 2 parallel | ~3 min |
| --full-review | 4 | All phases optimized | ~4.5 min |

**Optimization Gains** (vs previous):
- `--fast`: ~20% faster (2.5 min vs 3 min)
- `default`: ~25% faster (3 min vs 4 min) - QA-Data starts 45s earlier
- `--full-review`: ~25% faster (4.5 min vs 6 min)
