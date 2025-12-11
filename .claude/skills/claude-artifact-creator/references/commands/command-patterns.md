# Command Patterns

Commands are user-invoked workflows organized by action (what user wants to DO).

## Category Overview

| Category | Purpose | Examples |
|----------|---------|----------|
| `review/` | Analyze existing code | code-review, pr-enhance |
| `generate/` | Create new code/docs | scaffold, doc-generate |
| `debug/` | Diagnose and fix issues | error-trace, smart-debug |
| `refactor/` | Improve existing code | cleanup, tech-debt |
| `tdd/` | Test-driven development | tdd-cycle, tdd-red |
| `feature/` | End-to-end feature work | feature-development |
| `git/` | Version control workflows | git-workflow, pr-create |
| `explain/` | Code explanation | explain-function |
| `optimize/` | Performance improvements | optimize-query |
| `team/` | Team collaboration | standup, retro |

## Command File Format

```yaml
---
description: Brief description      # Required for SlashCommand tool
allowed-tools: Bash(git:*), Read    # Optional: restrict tools
argument-hint: [file] [options]     # Optional: shown in autocomplete
model: sonnet                       # Optional: override model
---

[Command instructions using $ARGUMENTS]

## Context
- Current status: !`git status`     # Bash execution with ! prefix

## Steps
1. [Step 1]
2. [Step 2]
```

## Key Features

### Arguments

Commands receive user input via `$ARGUMENTS`:

```markdown
**Target**: $ARGUMENTS (defaults to current directory if not specified)
```

### Bash Execution

Use `!` prefix for inline bash:

```markdown
**Current branch**: !`git branch --show-current`
**Status**: !`git status --short`
```

### Tool Restrictions

Limit what tools a command can use:

```yaml
# Only git commands and reading
allowed-tools: Bash(git:*), Read

# Full access
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
```

## Common Patterns

### Review Pattern

For code analysis commands:

```markdown
## Review Process

### Step 1: Understand Scope
- Identify files to review
- Check recent changes

### Step 2: Analyze Code
- [Checklist items]

### Step 3: Report Findings
[Output format]
```

### Generate Pattern

For scaffolding commands:

```markdown
## Generation Process

### Step 1: Gather Information
- Extract from $ARGUMENTS

### Step 2: Check Existing Patterns
- Review existing code

### Step 3: Generate Files
- [File list]

### Step 4: Post-Generation
- [Integration steps]
```

### Debug Pattern

For troubleshooting commands:

```markdown
## Debugging Process

### Step 1: Reproduce & Understand
- Identify error type
- Gather context

### Step 2: Analyze
- Locate source
- Investigate root cause

### Step 3: Diagnose
- [Analysis checklist]

### Step 4: Fix & Verify
- Apply fix
- Run tests
```

### Workflow Pattern

For multi-phase commands:

```markdown
## Workflow Phases

### Phase 1: Assessment
**Objective**: [Goal]
**Actions**: [Steps]
**Checkpoint**: [Verification]

---

### Phase 2: Planning
...

### Phase 3: Execution
...

### Phase 4: Validation
...
```

### Git Pattern

For version control commands:

```markdown
## Git Workflow

### Step 1: Pre-flight Checks
- [ ] Working directory clean
- [ ] On correct branch
- [ ] Remote up to date

### Step 2: Execute Operation
[Git commands]

### Step 3: Verify
- [ ] Operation successful
- [ ] History looks correct
```

## Output Format Conventions

### Summary Output

```markdown
## [Action] Summary: [Target]

### Changes Applied
- [Change 1]
- [Change 2]

### Results
- Tests: [Pass/Fail]
- Build: [Pass/Fail]

### Next Steps
- [Recommendation]
```

### Findings Output

```markdown
## [Analysis Type]: [Target]

### Summary
[1-2 sentence overview]

### Findings

#### Critical (Must Fix)
- [file:line] - [issue]

#### Suggestions
- [file:line] - [improvement]

### Verdict
[Approve / Request Changes / Comment only]
```

## Template Reference

| Template | Category | Purpose |
|----------|----------|---------|
| `review` | review | Code review and analysis |
| `generate` | generate | Scaffolding and generation |
| `debug` | debug | Error diagnosis |
| `workflow` | feature | Multi-phase processes |
| `git` | git | Git automation |
| `refactor` | refactor | Code improvement |

## Best Practices

### Clear Description

```yaml
# Good - explains what and when
description: Review code for quality, security, and best practices

# Bad - too vague
description: Reviews code
```

### Argument Hints

```yaml
# Good - shows expected format
argument-hint: <file-or-directory> [--focus <area>]

# Bad - no guidance
argument-hint: args
```

### Structured Output

Always define output format in the command so results are consistent.

### Verification Steps

Include checkpoints to verify success:

```markdown
### Verification
- [ ] Changes applied
- [ ] Tests passing
- [ ] Build successful
```

### Safety for Destructive Operations

```markdown
## Safety Rules

1. **Never force push** without explicit confirmation
2. **Always verify** before destructive operations
3. **Create backup** before risky operations
```
