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

## Workflow Overview

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

## Signal Protocol

Agents communicate completion through explicit signals:

| Signal | Emitted By | Triggers |
|--------|------------|----------|
| `🟢 ENTITY_READY` | BA | Architect + QA-Data can start |
| `🟢 CONTRACTS_READY` | Architect | Developer + QA-Tests can start |

## Execution

**See**: [references/add-feature-modes.md](references/add-feature-modes.md) for detailed mode scripts.

Parse mode from arguments, then follow the appropriate execution flow.

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
| `--minimal` | Implementation only, skip all docs |
| `--fast` | Skip BA, Arch parses requirements |
| `--stage analyze` | BA only |
| `--stage design` | Arch only (needs entity definition) |
| `--stage implement` | Dev only (needs contracts) |
| `--stage test` | QA only (needs contracts) |
| `--review` | Default + code review |
| `--security` | Default + security audit |
| `--full-review` | All stages with reviews |
| `--impact` | Generate impact-analysis.md |
| `--dry-run` | Preview without creating files |

## Error Handling

On failure:
1. Preserve completed outputs
2. Report failed stage and agent
3. Suggest `--stage {next}` to resume
4. If progressive handoff failed, suggest `--fast` mode

## Performance

| Mode | Stages | Time |
|------|--------|------|
| --minimal | 1 | ~2 min |
| --fast | 2 | ~2.5 min |
| default | 3 | ~3 min |
| --full-review | 4 | ~4.5 min |
