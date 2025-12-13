# Output Patterns

Patterns for producing consistent, high-quality skill outputs across different roles and deliverable types.

## Template Pattern

Provide templates for output format. Match strictness to requirements.

### Strict Templates (APIs, Data Formats)

```markdown
## Report Structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive Summary
[One-paragraph overview of key findings]

## Key Findings
- Finding 1 with supporting data
- Finding 2 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

### Flexible Templates (Adaptable Guidance)

```markdown
## Report Structure

Sensible default format (adapt as needed):

# [Analysis Title]

## Executive Summary
[Overview]

## Key Findings
[Adapt sections based on discoveries]

## Recommendations
[Tailor to specific context]

Adjust sections based on analysis type.
```

---

## Examples Pattern

For quality-dependent outputs, provide input/output pairs:

```markdown
## Commit Message Format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation

Follow this style: type(scope): brief description, then detailed explanation.
```

---

## Before/After Transformation Pattern

Show concrete transformations:

```markdown
## Transformation Examples

**Before (problem):**
[Show problematic code/content]

**After (solution):**
[Show improved code/content]

**Why**: [Brief explanation of the improvement]
```

---

## Deliverables Checklist Pattern

Define explicit outputs for skills producing multiple artifacts:

```markdown
## Output Deliverables

After execution, provide:

1. **Assessment Report:**
   - Current patterns found
   - Items needing attention
   - Priority ranking

2. **Action Plan:**
   - Step-by-step changes
   - Component-by-component breakdown

3. **Implementation:**
   - Actual code changes
   - Configuration updates

4. **Verification Checklist:**
   - [ ] Tests pass
   - [ ] No regressions
   - [ ] Documentation updated
```

---

## Classification/Inventory Pattern

Provide frameworks for organizing findings:

```markdown
## Classification Framework

**Critical (P0):** [Criteria for critical items]
**High (P1):** [Criteria for high priority]
**Medium (P2):** [Criteria for medium priority]
**Low (P3):** [Criteria for low priority]
```

---

## Context-Specific Notes Pattern

End skills with environment-specific constraints:

```markdown
## Important Notes

- Technology stack: [versions, frameworks]
- Existing patterns to follow: [conventions]
- Known limitations: [edge cases]
- Testing requirements: [what to verify]
```

---

## Generic Deliverables Template

Use this parameterized template for any role. Replace `{Role}` and `{deliverable_type}` with specifics.

### Deliverable Definition

```markdown
## {Role} Deliverables

| Deliverable | Format | Description |
|-------------|--------|-------------|
| {deliverable_1} | {format} | {purpose} |
| {deliverable_2} | {format} | {purpose} |
| {deliverable_3} | {format} | {purpose} |
```

### Document Template

```markdown
# {Document Title}

## Status
[Draft | In Review | Approved | Superseded]

## Context
[Why this document exists, what problem it solves]

## Content
[Main content organized by logical sections]

## Decision/Outcome
[If applicable: what was decided and why]

## Consequences
- Positive: [benefits]
- Negative: [tradeoffs]

## References
- [Related documents]
```

### Code Artifact Template

```markdown
## {Artifact} Structure

**File**: `{path}/{Name}.{ext}`

**Purpose**: [What this artifact does]

**Dependencies**: [What it requires]

**Template**:
[Language-appropriate code template with {placeholders}]
```

### Report Template

```markdown
# {Report Type}: {Subject}

**Date**: YYYY-MM-DD
**Author**: {role}

## Executive Summary
[High-level findings in 2-3 sentences]

## Findings Summary
| Severity | Count |
|----------|-------|
| Critical | [N] |
| High | [N] |
| Medium | [N] |
| Low | [N] |

## Detailed Findings
[Individual findings with location, description, impact, recommendation]

## Recommendations
[Prioritized action items]
```

---

## Role-to-Deliverable Mapping

| Role | Primary Deliverables | Common Formats |
|------|---------------------|----------------|
| Architect | Design docs, ADRs, API specs, schemas | Markdown, YAML, diagrams |
| Developer | Code, tests, migrations | Source files, test files |
| Reviewer | Review reports, findings | Markdown with tables |
| QA Engineer | Test plans, test cases, bug reports | Markdown, Gherkin |
| Security Engineer | Audit reports, threat models | Markdown, STRIDE tables |
| DevOps Engineer | Pipelines, Dockerfiles, runbooks | YAML, Dockerfile, Markdown |
| Product/Manager | Requirements, user stories, release notes | Markdown |

---

## Output Quality Guidelines

### Consistency Markers

Use consistent markers across outputs:

```markdown
Status indicators:
- ✅ Complete/Pass
- ❌ Failed/Issue
- ⚠️ Warning/Attention
- 🔄 In Progress

Priority levels:
- 🔴 Critical (P0)
- 🟠 High (P1)
- 🟡 Medium (P2)
- 🟢 Low (P3)
```

### Structured Outputs for Automation

When outputs may be parsed programmatically:

```json
{
  "status": "success|partial|failed",
  "summary": { "total": 0, "passed": 0, "failed": 0 },
  "details": [{ "id": "item-1", "status": "passed", "message": "..." }]
}
```

### Human-Readable Summaries

Always include executive summaries:

```markdown
## Executive Summary

**Overall Status**: ✅ Successful | ⚠️ Needs Attention | ❌ Failed

**Key Findings:**
1. [Most important finding]
2. [Second finding]

**Recommended Actions:**
1. [Immediate action needed]
2. [Follow-up action]
```
