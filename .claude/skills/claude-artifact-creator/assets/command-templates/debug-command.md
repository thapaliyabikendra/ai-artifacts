---
description: Debug and diagnose [ISSUE_TYPE] with systematic analysis
allowed-tools: Read, Glob, Grep, Bash
argument-hint: <error-message-or-file>
---

# {Command Title}

Systematically diagnose and fix errors with root cause analysis.

## Context

**Error/Issue**: $ARGUMENTS

**Current status**:
- Git status: !`git status --short`
- Recent changes: !`git log --oneline -3`

## Debugging Process

### Step 1: Reproduce & Understand

1. **Identify the error type:**
   - Compilation/build error
   - Runtime error
   - Test failure
   - Unexpected behavior

2. **Gather context:**
   - When does it occur?
   - Is it reproducible?
   - Recent changes that might be related

### Step 2: Analyze

1. **Locate the source:**
   - Stack trace analysis
   - Error message parsing
   - Related file identification

2. **Investigate root cause:**
   - Check recent changes in related files
   - Review dependencies
   - Look for similar issues in codebase

### Step 3: Diagnose

**Analysis checklist:**
- [ ] Error message understood
- [ ] Root cause identified
- [ ] Impact scope assessed
- [ ] Fix approach determined

### Step 4: Fix & Verify

1. **Apply fix:**
   - Make minimal necessary changes
   - Don't introduce new issues

2. **Verify:**
   - Run relevant tests
   - Build the project
   - Manual verification if needed

## Output Format

```markdown
## Debug Report: [Error Description]

### Error Analysis
- **Type**: [error type]
- **Location**: [file:line]
- **Message**: [error message]

### Root Cause
[Explanation of why the error occurred]

### Fix Applied
- **File**: [file path]
- **Change**: [description of change]

### Verification
- [ ] Tests passing
- [ ] Build successful
- [ ] Error no longer occurs

### Prevention
[How to prevent this in the future]
```

## Common Error Patterns

| Error Type | Common Causes | Investigation |
|------------|---------------|---------------|
| Null reference | Missing null checks | Check data flow |
| Type error | Mismatched types | Check interfaces |
| Import error | Missing dependency | Check package.json/csproj |
| Test failure | Logic error or stale test | Compare expected vs actual |
