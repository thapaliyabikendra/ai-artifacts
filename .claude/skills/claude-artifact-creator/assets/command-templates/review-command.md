---
description: Review [TARGET] for quality, patterns, and best practices
allowed-tools: Read, Glob, Grep
argument-hint: [file-or-directory]
---

# {Command Title}

Review code for quality, correctness, and adherence to best practices.

## Context

**Target**: $ARGUMENTS (defaults to current directory if not specified)

**Current status**: !`git status --short`

## Review Process

### Step 1: Understand Scope
- Identify files to review: !`git diff --name-only` or specified files
- Check recent changes: !`git log --oneline -5`

### Step 2: Analyze Code

Review each file for:

**Functionality**
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Error handling appropriate

**Quality**
- [ ] Readable and maintainable
- [ ] Follows project conventions
- [ ] No unnecessary complexity

**Security**
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] No injection vulnerabilities

**Testing**
- [ ] Tests exist for new code
- [ ] Tests are meaningful

### Step 3: Report Findings

**Output Format:**
```markdown
## Review: [Target]

### Summary
[1-2 sentence overview]

### Findings

#### Critical (Must Fix)
- [file:line] - [issue description]

#### Suggestions
- [file:line] - [improvement suggestion]

#### Positive Observations
- [What's done well]

### Verdict
[ ] Approve
[ ] Request Changes
```

## Options

- `--focus security` - Emphasize security review
- `--focus performance` - Emphasize performance analysis
- `--quick` - Quick scan, major issues only
