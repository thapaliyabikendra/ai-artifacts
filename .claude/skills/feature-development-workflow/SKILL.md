---
name: feature-development-workflow
description: "Orchestrate end-to-end feature development from requirements through implementation, testing, and review. Use when: (1) planning feature development stages, (2) coordinating multi-agent feature workflows, (3) understanding SDLC phases for new features."
---

# Feature Development Workflow

Orchestrate complete feature development lifecycle with specialized agents at each stage.

## When to Use

- Planning new feature implementation
- Coordinating multi-stage development workflows
- Understanding what documents/artifacts each stage produces
- Running `/add-feature` command

## Execution Modes

| Mode | Command | Time | Best For |
|------|---------|------|----------|
| **Minimal** | `--minimal` | ~2 min | Simple CRUD, no docs needed |
| **Parallel** | `--parallel` | ~5 min | Standard features, balanced speed |
| **Sequential** | (default) | ~8 min | Complex features needing doc review |
| **Full Review** | `--full-review` | ~12 min | Production releases |

### Mode Comparison

```
--minimal:     [Stage 3 only] ────────────────────────────> Done
--parallel:    [Stage 1 + 2] ─────> [Stage 3 + 4] ────────> Done
default:       Stage 1 → Stage 2 → Stage 3 → Stage 4 ────> Done
--full-review: Stage 1 → 2 → 3 → 4 → 5 → 6 ───────────────> Done
```

## Model Selection by Stage

| Stage | Model | Rationale |
|-------|-------|-----------|
| 1. Analysis | `haiku` | Doc generation, no complex reasoning |
| 2. Design | `haiku` | Template-based, structured output |
| 3. Implementation | `sonnet` | Code generation needs accuracy |
| 4. Testing | `haiku` | Test case docs, simple code |
| 5. Review | `haiku` | Checklist-based analysis |
| 6. Security | `haiku` | Pattern matching, checklist |

## Workflow Overview

```
┌─────────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
│ 1.Analyze & │ → │ 2.Design  │ → │ 3.Implement│ → │ 4.Test    │ → │ 5.Review  │ → │ 6.Security│
│   Require   │   │ (backend- │   │ (abp-     │   │ (qa-      │   │ (code-    │   │ (security-│
│ (business-  │   │ architect)│   │ developer)│   │ engineer) │   │ reviewer) │   │ engineer) │
│  analyst)   │   │  haiku    │   │  sonnet   │   │  haiku    │   │  haiku    │   │  haiku    │
└─────────────┘   └───────────┘   └───────────┘   └───────────┘   └───────────┘   └───────────┘
      ↓                 ↓               ↓               ↓               ↓               ↓
   ~100 lines       ~150 lines    Source code      ~80 lines       ~50 lines       ~50 lines
```

**Note**: Stages 5-6 are optional (use `--review`, `--security`, or `--full-review` flags).

## Stage Summary

| Stage | Agent | Model | Max Output | Skills Used |
|-------|-------|-------|------------|-------------|
| 1. Analyze | `business-analyst` | haiku | 150 lines | `requirements-engineering`, `domain-modeling` |
| 2. Design | `backend-architect` | haiku | 200 lines | `api-design-principles`, `efcore-patterns` |
| 3. Implement | `abp-developer` | sonnet | Code files | `abp-framework-patterns` |
| 4. Testing | `qa-engineer` | haiku | 80 lines | `xunit-testing-patterns` |
| 5. Review | `code-reviewer` | haiku | 50 lines | `code-review-excellence` |
| 6. Security | `security-engineer` | haiku | 50 lines | `security-patterns` |

## Concise Output Guidelines

**CRITICAL**: All documentation stages must be CONCISE. Enforce line limits:

### Stage 1: requirements.md (max 100 lines)
```markdown
# {Feature} Requirements
## User Stories (3-5 stories)
## Entity Properties (table)
## Business Rules (BR-XXX)
## Permissions (list)
```

### Stage 2: technical-design.md (max 150 lines)
```markdown
# {Feature} Technical Design
## Entity (class skeleton)
## DTOs (property lists)
## AppService Interface
## API Endpoints (table)
## Database Columns (table)
```

### Stage 4: test-cases.md (max 80 lines)
```markdown
# {Feature} Test Cases
| ID | Category | Description | Expected |
```

## Parallelization Strategy

### Parallel Mode (`--parallel`)

**Phase 1**: Launch simultaneously in ONE message with multiple Task calls:
- Agent 1: business-analyst (requirements)
- Agent 2: backend-architect (design)

**Phase 2**: After Phase 1 completes, launch simultaneously:
- Agent 3: abp-developer (implementation)
- Agent 4: qa-engineer (test cases only, no code)

### Why This Works
- Stage 1 and 2 can work from the same raw requirements
- Stage 3 and 4 have independent outputs (code vs test docs)
- Reduces total time from ~15 min to ~5 min

## Stage Options

| Flag | Stages | Time |
|------|--------|------|
| `--minimal` | 3 only | ~2 min |
| `--parallel` | 1+2, then 3+4 | ~5 min |
| (default) | 1→2→3→4 | ~8 min |
| `--stage analyze` | 1 only | ~1 min |
| `--stage design` | 2 only | ~1 min |
| `--stage implement` | 3 only | ~2 min |
| `--stage test` | 4 only | ~1 min |
| `--review` | 1→2→3→4→5 | ~10 min |
| `--security` | 1→2→3→4+6 | ~10 min |
| `--full-review` | 1→2→3→4→5→6 | ~12 min |

## Quick Commands

| Scenario | Recommended Command |
|----------|---------------------|
| Simple CRUD entity | `/generate:crud {Entity} --properties "..."` |
| Fast feature (no docs) | `/add-feature {name} "{req}" --minimal` |
| Standard feature | `/add-feature {name} "{req}" --parallel` |
| Complex feature | `/add-feature {name} "{req}"` |
| Production release | `/add-feature {name} "{req}" --full-review` |

## Error Recovery

If a stage fails:
1. Preserve completed stage outputs
2. Report which stage failed and why
3. Re-run from failed stage with `--stage` flag

## Alternative Workflows

| Scenario | Command |
|----------|---------|
| Simple CRUD | `/generate:crud {Entity}` |
| Fast Feature | `/add-feature {name} --minimal` |
| Bug Fix | `/smart-debug "{error}"` |
| Security Only | `/add-feature {name} --stage security` |
| Review Only | `/add-feature {name} --stage review` |

## References

- [references/stage-templates.md](references/stage-templates.md) - Prompt templates
- [references/checkpoint-validation.md](references/checkpoint-validation.md) - Validation criteria
