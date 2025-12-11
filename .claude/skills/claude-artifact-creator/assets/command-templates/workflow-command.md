---
description: Execute [WORKFLOW_NAME] with phased approach
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <target> [--phase <n>]
---

# {Command Title}

Multi-phase workflow with checkpoints and validation.

## Usage

```
/{command-name} <target> [options]
```

**Arguments:**
- `target`: What to apply the workflow to

**Options:**
- `--phase <n>`: Start from specific phase (1-4)
- `--dry-run`: Preview without making changes

## Context

**Target**: $ARGUMENTS
**Current status**: !`git status --short`

## Workflow Phases

### Phase 1: Assessment

**Objective**: Understand current state

**Actions:**
1. Analyze target scope
2. Identify affected areas
3. Create inventory of items

**Checkpoint:**
- [ ] Scope clearly defined
- [ ] All items inventoried
- [ ] Risks identified

---

### Phase 2: Planning

**Objective**: Design the approach

**Actions:**
1. Prioritize items
2. Determine order of operations
3. Identify dependencies

**Checkpoint:**
- [ ] Plan reviewed
- [ ] Dependencies mapped
- [ ] Rollback strategy defined

---

### Phase 3: Execution

**Objective**: Apply changes incrementally

**Actions:**
1. Apply changes in priority order
2. Verify each change
3. Document what changed

**Checkpoint:**
- [ ] All planned changes applied
- [ ] No regressions introduced
- [ ] Changes documented

---

### Phase 4: Validation

**Objective**: Verify results and document

**Actions:**
1. Run tests
2. Verify build
3. Document outcomes

**Checkpoint:**
- [ ] All tests passing
- [ ] Build successful
- [ ] Documentation updated

## Output Format

```markdown
## Workflow Summary: [Target]

### Phase Completion
- Phase 1 (Assessment): [Complete/Partial/Skipped]
- Phase 2 (Planning): [Complete/Partial/Skipped]
- Phase 3 (Execution): [Complete/Partial/Skipped]
- Phase 4 (Validation): [Complete/Partial/Skipped]

### Changes Applied
- [Change 1]
- [Change 2]

### Results
- Tests: [Pass/Fail]
- Build: [Pass/Fail]

### Follow-up Items
- [Item requiring attention]
```
