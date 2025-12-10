# Workflow Patterns

Patterns for structuring multi-step processes, agent coordination, and phased execution.

## Sequential Workflows

Break operations into clear, sequential steps with an overview at the beginning:

```markdown
PDF form filling involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

Guide through decision points with branching logic:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## Phased Workflows

Organize complex processes into distinct phases:

```markdown
## Phase 1: Assessment and Inventory

### 1.1 Analyze Current State
Examine the codebase to understand:
- Current implementation patterns
- Components needing attention
- Specific issues identified

**Actions:**
- Search for patterns: [specific searches]
- Review [specific directories]
- Check [specific files]

### 1.2 Create Inventory
Classify findings:

**Category A:**
- Item 1, Item 2, Item 3

**Category B:**
- Item 1, Item 2, Item 3

---

## Phase 2: Implementation

### 2.1 [First Implementation Step]
[Detailed instructions with before/after examples]

### 2.2 [Second Implementation Step]
[Detailed instructions]

---

## Phase 3: Validation and Completion

### 3.1 Verify Results
Test that:
- [Verification criterion 1]
- [Verification criterion 2]
- [Verification criterion 3]

### 3.2 Generate Documentation
Include:
- Summary of changes
- Usage instructions
- Migration guide if applicable
```

## User Input Gathering

Gather information upfront to prevent wasted effort:

```markdown
## User Input Required

Ask the user for:
1. **Scope**: Which components/folders to analyze?
2. **Approach**: What strategy to use?
   - Option A (lightweight)
   - Option B (recommended)
   - Option C (comprehensive)
3. **Priority**: Focus on specific areas first?
```

## Iterative Refinement

For tasks requiring multiple passes:

```markdown
## Iteration Workflow

1. Execute initial implementation
2. Run validation checks
3. If issues found:
   - Document specific problems
   - Apply targeted fixes
   - Re-validate
4. Repeat until all checks pass
```

---

## Agent Integration Patterns

Skills are often referenced by agents and commands. Design skills to work well in multi-agent workflows.

### Context Passing Pattern

When skills produce outputs consumed by subsequent workflow phases:

```markdown
## Output Format

This skill produces structured output for downstream processing:

### For Downstream Agents
```json
{
  "status": "success|partial|failed",
  "findings": [...],
  "recommendations": [...],
  "artifacts": ["path/to/file1", "path/to/file2"]
}
```

### For Human Review
[Markdown-formatted summary]
```

### Handoff Points

Define clear handoff points between workflow phases:

```markdown
## Phase Completion Criteria

### Phase 1 Complete When:
- [ ] All files analyzed
- [ ] Inventory document created
- [ ] Priority ranking assigned

**Handoff to Phase 2:**
- Pass: inventory.md
- Pass: priority-list.json
- Context: [summary of Phase 1 findings]

### Phase 2 Complete When:
- [ ] All high-priority items addressed
- [ ] Changes verified
- [ ] No regressions

**Handoff to Phase 3:**
- Pass: changes-summary.md
- Context: [list of modified files]
```

### Skill-to-Agent Interface

Design skills to be easily referenced by agents:

```markdown
## Agent Usage

When referenced by an agent, this skill provides:

**Input Required:**
- Entity name (string)
- Entity properties (list)
- Options (object)

**Output Provided:**
- Generated file paths
- Validation results
- Post-generation checklist

**Example Agent Prompt:**
"Use the crud-service skill to generate a CRUD service for the
'Product' entity with properties: Name (string), Price (decimal),
CategoryId (Guid). Include import/export functionality."
```

### Multi-Agent Coordination

For skills supporting multi-agent workflows:

```markdown
## Multi-Agent Support

This skill supports parallel execution by multiple agents:

### Parallelizable Tasks
- File analysis (can run concurrently on different files)
- Validation checks (independent of each other)

### Sequential Dependencies
- Schema generation must complete before service generation
- Tests must wait for implementation

### Conflict Prevention
- Lock files during modification
- Use unique output directories per agent
- Merge results using [merge strategy]
```

---

## Workflow Templates by Role

### Backend Developer Workflow

```markdown
## CRUD Implementation Workflow

### Input Gathering
1. Entity name and properties
2. Related entities for joins
3. Include import/export?

### Generation Phase
1. Generate AppService → [template]
2. Generate Interface → [template]
3. Generate DTOs → [template]
4. Generate Validator → [template]

### Integration Phase
1. Register in DI container
2. Configure AutoMapper
3. Add to module

### Verification Phase
1. Build solution
2. Run unit tests
3. Test endpoints manually
```

### Frontend Developer Workflow

```markdown
## Component Implementation Workflow

### Input Gathering
1. Component name and type
2. State management approach
3. Include tests and stories?

### Generation Phase
1. Generate component file
2. Generate styles
3. Generate tests
4. Generate Storybook story

### Integration Phase
1. Export from index
2. Add to parent component
3. Connect to state/API

### Verification Phase
1. Run component tests
2. Check Storybook rendering
3. Verify responsive behavior
```

### QA Engineer Workflow

```markdown
## Test Coverage Workflow

### Analysis Phase
1. Identify code under test
2. Map existing coverage
3. Identify gaps

### Planning Phase
1. Prioritize by risk
2. Group related scenarios
3. Estimate effort

### Implementation Phase
1. Write unit tests
2. Write integration tests
3. Write E2E tests

### Verification Phase
1. Run full test suite
2. Generate coverage report
3. Verify thresholds met
```

### Security Engineer Workflow

```markdown
## Security Audit Workflow

### Scope Phase
1. Define audit boundaries
2. Identify critical assets
3. Review threat model

### Analysis Phase
1. Static analysis scan
2. Dependency audit
3. Configuration review
4. Manual code review

### Classification Phase
1. Categorize findings (P0-P3)
2. Assess impact
3. Determine remediation effort

### Reporting Phase
1. Generate executive summary
2. Detail findings with evidence
3. Provide remediation guidance
```

---

## Validation and Verification Patterns

### Pre-Execution Validation

```markdown
## Prerequisites Check

Before starting:
- [ ] Required files exist: [list]
- [ ] Dependencies installed: [list]
- [ ] Permissions available: [list]
- [ ] Environment configured: [list]

If any prerequisite fails, stop and report.
```

### Post-Execution Verification

```markdown
## Verification Checklist

After completion:
- [ ] No syntax/compilation errors
- [ ] All tests pass
- [ ] No regression in existing functionality
- [ ] Performance within acceptable bounds
- [ ] Documentation updated
- [ ] Code review requested
```

### Rollback Strategy

```markdown
## Rollback Procedure

If verification fails:

1. **Identify failure scope**
   - Which files affected?
   - Which tests failing?

2. **Revert changes**
   - `git checkout -- [files]` for local changes
   - `git revert [commit]` for committed changes

3. **Analyze root cause**
   - Review error messages
   - Check logs
   - Compare with working state

4. **Re-attempt with fixes**
   - Address root cause
   - Re-run from appropriate phase
```

---

## Error Recovery Patterns

### Graceful Degradation

```markdown
## Error Handling

If a step fails:

1. **Non-critical failure**: Log warning, continue to next step
2. **Critical failure**: Stop execution, report error, provide recovery options
3. **Partial success**: Complete what's possible, report incomplete items

### Recovery Options

| Error Type | Recovery Action |
|------------|-----------------|
| File not found | Skip or create default |
| Permission denied | Request elevated access |
| Network timeout | Retry with backoff |
| Validation failed | Report issues, allow manual fix |
```

### Checkpoint Pattern

```markdown
## Checkpoints

Save progress at key points:

### Checkpoint 1: After Analysis
Save: analysis-results.json
Resume: Skip to Phase 2 with saved analysis

### Checkpoint 2: After Generation
Save: generated-files.json
Resume: Skip to Integration phase

### Checkpoint 3: After Integration
Save: integration-status.json
Resume: Skip to Verification phase
```
