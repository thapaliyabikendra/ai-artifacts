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

## Workflow Overview

```
┌─────────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
│ 1.Analyze & │ → │ 2.Design  │ → │ 3.Implement│ → │ 4.Test    │ → │ 5.Review  │ → │ 6.Security│
│   Require   │   │ (backend- │   │ (abp-     │   │ (qa-      │   │ (code-    │   │ (security-│
│ (business-  │   │ architect)│   │ developer)│   │ engineer) │   │ reviewer) │   │ engineer) │
│  analyst)   │   │           │   │           │   │           │   │           │   │           │
└─────────────┘   └───────────┘   └───────────┘   └───────────┘   └───────────┘   └───────────┘
      ↓                 ↓               ↓               ↓               ↓               ↓
 • domain/* updates  technical-    Source code    test-cases.md   review-        security-
 • requirements.md   design.md     files          + Test code     report.md      audit.md
 • impact-analysis.md
```

**Note**: Stages 5-6 are optional (use `--review`, `--security`, or `--full-review` flags).

## Stage Summary

| Stage | Agent | Input | Output | Skills Used | Optional |
|-------|-------|-------|--------|-------------|----------|
| 1. Analyze & Require | `business-analyst` | Raw requirements | `requirements.md`, `impact-analysis.md`, domain updates | `requirements-engineering`, `domain-modeling` | No |
| 2. Design | `backend-architect` | requirements.md, impact-analysis.md | `technical-design.md` | `api-design-principles`, `postgresql` | No |
| 3. Implementation | `abp-developer` | technical-design.md | Source code | `abp-framework-patterns` | No |
| 4. Testing | `qa-engineer` | requirements + design | test-cases.md + tests | `xunit-testing-patterns` | No |
| 5. Code Review | `code-reviewer` | Source code | `review-report.md` | `code-review-excellence` | Yes |
| 6. Security | `security-engineer` | All artifacts | `security-audit.md` | `security-patterns` | Yes |

## Stage Details

### Stage 1: Analysis & Requirements (business-analyst)

**Purpose**: Analyze requirements, update domain knowledge, and create specifications.

**Agent**: `business-analyst` (merged from domain-manager + product-architect)

**Phases**:
1. **Domain Analysis**: Review existing entities, rules, permissions
2. **Domain Updates**: Create/update domain files as needed
3. **Requirements**: Write user stories with acceptance criteria
4. **Impact Report**: Document all changes and risks

**Outputs**:
- `docs/domain/entities/{entity}.md` (if new entities)
- `docs/domain/business-rules.md` (new BR-XXX rules appended)
- `docs/domain/permissions.md` (new permissions appended)
- `docs/features/{feature}/requirements.md`
- `docs/features/{feature}/impact-analysis.md`

**Checkpoint**: Domain updated, 3+ user stories, impact analysis complete.

### Stage 2: Technical Design (backend-architect)

**Purpose**: Create implementation blueprint from requirements.

**Agent Prompt Essentials**:
- Read requirements.md and impact-analysis.md from Stage 1
- Reference domain entity definitions
- Apply `api-design-principles` and `postgresql` skills
- Output entity design, DTOs, API contracts

**Checkpoint**: Entity, DTOs, and API endpoints defined.

### Stage 3: Implementation (abp-developer)

**Purpose**: Generate production code following technical design.

**Agent Prompt Essentials**:
- Read technical-design.md from Stage 2
- Apply `abp-framework-patterns` skill
- Follow existing code patterns in project

**Checkpoint**: Entity, AppService, DTOs, Validator created. Build succeeds.

### Stage 4: Testing (qa-engineer)

**Purpose**: Create test documentation and implement automated tests.

**Agent Prompt Essentials**:
- Read requirements.md, technical-design.md, and impact-analysis.md
- Apply `xunit-testing-patterns` skill
- Create both documentation and test code

**Checkpoint**: 10+ test cases, test files compile.

### Stage 5: Code Review (Optional)

**Purpose**: Review implemented code for quality and patterns.

**Agent Prompt Essentials**:
- Read all generated source code
- Apply `code-review-excellence` skill
- Check ABP patterns, async usage, validation

**Checkpoint**: No critical issues. Recommendations documented.

### Stage 6: Security Audit (Optional)

**Purpose**: Verify security controls and identify vulnerabilities.

**Agent Prompt Essentials**:
- Read all artifacts and source code
- Apply `security-patterns` skill
- Check OWASP Top 10, authorization, input validation

**Checkpoint**: No critical/high vulnerabilities. Security controls verified.

## Output Locations

All outputs go to `docs/features/{feature-name}/`:

| File | Stage | Content |
|------|-------|---------|
| `requirements.md` | 1 | User stories, acceptance criteria, data model |
| `impact-analysis.md` | 1 | Domain changes, risks, affected components |
| `technical-design.md` | 2 | Entity, DTOs, API contracts, schema |
| `test-cases.md` | 4 | Test case table with priorities |
| `review-report.md` | 5 | Code review findings (optional) |
| `security-audit.md` | 6 | Security findings (optional) |

Code outputs follow `docs/architecture/README.md` path templates.

## Stage Options

| Flag | Stages Executed |
|------|-----------------|
| (default) | 1, 2, 3, 4 |
| `--stage analyze` | 1 only |
| `--stage design` | 2 only |
| `--stage implement` | 3 only |
| `--stage test` | 4 only |
| `--stage review` | 5 only |
| `--stage security` | 6 only |
| `--review` | 1, 2, 3, 4, 5 |
| `--security` | 1, 2, 3, 4, 6 |
| `--full-review` | 1, 2, 3, 4, 5, 6 |

## Impact Analysis Benefits

Stage 1 now produces `impact-analysis.md` which:

- **Audit trail**: Documents what changed and why
- **Risk visibility**: Flags concerns before implementation
- **Stakeholder alignment**: Identifies who needs to approve
- **Test guidance**: Helps QA understand what to test
- **Security context**: Gives security engineer scope of changes

## Error Recovery

If a stage fails:
1. Preserve completed stage outputs
2. Report which stage failed and why
3. Allow re-running from failed stage with `--stage` flag

## Alternative Workflows

Beyond new feature development, use these patterns for other scenarios:

### Bug Fix Workflow

Use `/smart-debug` command which orchestrates:

```
┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
│ 1.Diagnose│ → │ 2.Fix     │ → │ 3.Verify  │ → │ 4.Review  │
│ (debugger)│   │ (abp-     │   │ (qa-      │   │ (code-    │
│           │   │ developer)│   │ engineer) │   │ reviewer) │
└───────────┘   └───────────┘   └───────────┘   └───────────┘
      ↓               ↓               ↓               ↓
  Root cause      Code fix      Test verification  Review report
  analysis
```

**Invocation**: `/smart-debug "<error-message-or-description>"`

### Standalone Security Audit

Run security audit on existing feature code:

```bash
/add-feature <existing-feature> --stage security
```

Uses `security-engineer` agent with `security-patterns` skill to audit existing implementation.

### Domain-Only Update

Update domain knowledge without full feature workflow:

```bash
/add-feature <feature-name> --stage analyze
```

Uses `business-analyst` agent to:
- Analyze requirements against existing domain
- Update `docs/domain/` files
- Create impact analysis
- No implementation triggered

### Code Review Only

Review existing implementation:

```bash
/add-feature <feature-name> --stage review
```

Uses `code-reviewer` agent with `code-review-excellence` skill.

## Unified Entry Points

| Scenario | Command |
|----------|---------|
| New Feature | `/add-feature <name> "<requirements>"` |
| Bug Fix | `/smart-debug "<error>"` |
| Security Audit | `/add-feature <name> --stage security` |
| Domain Update | `/add-feature <name> --stage analyze` |
| Code Review | `/add-feature <name> --stage review` |
| Full Pipeline | `/add-feature <name> "<req>" --full-review` |

## References

- [references/stage-templates.md](references/stage-templates.md) - Full prompt templates for each stage
- [references/checkpoint-validation.md](references/checkpoint-validation.md) - Validation criteria
