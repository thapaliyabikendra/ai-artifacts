# Agent Optimization Patterns

> **Purpose**: Techniques for optimizing agent definitions, derived from real-world refactoring case studies.
> **Referenced By**: `GUIDELINES.md`, `claude-artifact-creator` skill

## Overview

These patterns transform **prescriptive, self-contained agents** into **lean workflow orchestrators** that delegate domain knowledge to skills. The result is typically:
- 60-70% size reduction
- Improved maintainability
- Expanded capabilities through skill composition
- Better reusability across projects

---

## Core Optimization Principles

### 1. Composition Over Embedding

**Anti-pattern**: Embed all patterns, checklists, and examples directly in the agent.

**Pattern**: Reference skills for domain knowledge; agent defines workflow only.

```yaml
# ❌ Before (embedded)
skills: skill1, skill2, skill3  # Flat list, no organization

# ✅ After (composed with semantic categories)
skills:
  # METHODOLOGY - How to do the work
  - process-skill

  # DOMAIN KNOWLEDGE - What to know
  - pattern-skill-1
  - pattern-skill-2

  # OUTPUT FORMAT - How to report
  - format-skill
```

**Benefit**: Update skills once, all consuming agents benefit.

---

### 2. Semantic Skill Categorization

Organize skills in the agent frontmatter by **purpose**, not alphabetically:

| Category | Purpose | Examples |
|----------|---------|----------|
| **METHODOLOGY** | How to perform the task | `code-review-excellence`, `tdd-patterns` |
| **DOMAIN KNOWLEDGE** | Patterns to validate/apply | `abp-framework-patterns`, `efcore-patterns` |
| **SECURITY LENS** | Vulnerability detection | `security-patterns`, `owasp-checks` |
| **PERFORMANCE LENS** | Efficiency checks | `linq-optimization-patterns`, `async-patterns` |
| **OUTPUT FORMAT** | Report structure | `actionable-review-format-standards` |

**Template**:
```yaml
skills:
  # METHODOLOGY - How to [verb] effectively
  - methodology-skill

  # DOMAIN KNOWLEDGE - [Domain] patterns to validate
  - domain-skill-1
  - domain-skill-2

  # [LENS] - [Purpose] checks
  - lens-skill

  # OUTPUT FORMAT - Standardized reports
  - output-skill
```

---

### 3. Explicit Workflow Pipeline

**Anti-pattern**: Implicit, prose-based process description.

**Pattern**: Declarative pipeline in frontmatter + phase-to-skill mapping.

```yaml
# Frontmatter
workflow: GATHER → ANALYZE → VALIDATE → REPORT
```

```markdown
## Workflow

| Phase | Action | Apply Skill |
|-------|--------|-------------|
| 1. Gather | Read inputs, context docs | — |
| 2. Analyze | [Domain-specific analysis] | `domain-skill` |
| 3. Validate | [Validation checks] | `validation-skill` |
| 4. Report | Structured output | `output-format-skill` |
```

**Benefit**: Self-documenting, repeatable process.

---

### 4. Skill Invocation Guidance

**Problem**: Agent lists skills but doesn't specify when to invoke them.

**Solution**: Add explicit phase-to-skill mapping with fallback.

```markdown
## Skill Invocation

**Before each phase**, invoke the corresponding skill:

```
Phase 2 → Skill: analysis-skill
Phase 3 → Skill: validation-skill-1, validation-skill-2
Phase 4 → Skill: output-format-skill
```

**Fallback**: If skill invocation fails, apply these minimum checks:

| Category | Minimum Checks |
|----------|----------------|
| Security | [3-5 critical checks] |
| Performance | [3-5 critical checks] |
| Patterns | [3-5 critical checks] |
| Output | [Required output elements] |
```

---

### 5. Project-Agnostic Design

**Anti-pattern**: Hardcode project names, paths, tech stack in agent.

**Pattern**: Load project context from documentation at runtime.

```markdown
# ❌ Before (hardcoded)
## Project: Clinic Management System
| Component | Technology |
|-----------|------------|
| Runtime | .NET 10 |
...

## File Types
- `api/src/ClinicManagementSystem.Domain/`

# ✅ After (dynamic)
## Project Context

Before starting, read:
1. `docs/architecture/README.md` for project structure
2. `docs/architecture/patterns.md` for coding conventions

**Include**: `.cs`, `.razor`, `.xaml`, `.fs`, `.csproj`...
**Exclude**: `bin/`, `obj/`, `.vs/`...
```

**Benefit**: Agent is portable across projects.

---

### 6. Externalize Output Templates

**Anti-pattern**: Embed 30+ line output templates in agent.

**Pattern**: Create dedicated output format skill.

```yaml
# ❌ Before (embedded)
## Output Template
### Summary
### Critical Issues
### Major Issues
[... 30 lines of template ...]

# ✅ After (externalized)
skills:
  - actionable-review-format-standards  # Comprehensive output patterns
```

**Output format skill provides**:
- Severity classification with decision tree
- Location format standards (`file:line`)
- Issue template (Problem/Fix/Why)
- Full report template
- Feedback language guide

---

### 7. Categorized Quality Self-Check

**Anti-pattern**: Flat checklist of verification items.

**Pattern**: Organize checklist by workflow phase/concern.

```markdown
# ❌ Before (flat)
- [ ] Read all files
- [ ] Checked authorization
- [ ] Validated patterns
- [ ] Checked performance
- [ ] Provided references

# ✅ After (categorized)
## Quality Self-Check

- [ ] Read all changed files
- [ ] **Security**: Checked authorization on all mutations
- [ ] **Security**: Verified no PII logging, no hardcoded secrets
- [ ] **Performance**: Scanned for N+1 patterns and blocking async
- [ ] **Patterns**: Validated entity encapsulation
- [ ] **Output**: Provided file:line references
- [ ] **Output**: Included code examples for fixes
```

**Benefit**: Traceability between workflow phases and verification.

---

### 8. Priority Re-evaluation

Review and update priority rankings based on impact:

```markdown
# Before (legacy priorities)
| Priority | Category |
|----------|----------|
| 1 | Security |
| 2 | DDD |
| 3 | Patterns |
| 4 | Performance |  ← Often causes most user-facing issues

# After (impact-based)
| Priority | Category |
|----------|----------|
| 1 | Security |
| 2 | Performance |  ← Elevated (user-facing impact)
| 3 | DDD |
| 4 | Patterns |
```

---

### 9. Skill Specialization

**Anti-pattern**: One broad skill covering multiple concerns.

**Pattern**: Multiple focused skills for better precision.

```yaml
# ❌ Before (broad)
skills:
  - csharp-advanced-patterns  # Covers async, LINQ, patterns

# ✅ After (specialized)
skills:
  - dotnet-async-patterns       # Async/await, cancellation, deadlocks
  - linq-optimization-patterns  # N+1, projections, eager loading
```

**Benefit**: More targeted knowledge injection, better skill reuse.

---

### 10. Shift-Left Concerns

Move concerns earlier in the workflow when they should be caught earlier:

| Concern | Old Approach | New Approach |
|---------|--------------|--------------|
| Security | Delegated to separate audit | Part of every review |
| Performance | Check at end | Check early (priority #2) |
| Testing | After implementation | TDD from start |

**Implementation**:
- Add relevant skills to agent
- Include in workflow phases
- Add to quality self-check

---

## Optimization Checklist

Use this when refactoring an agent:

```
Agent Optimization Review:
- [ ] Skills organized by semantic category (METHODOLOGY, DOMAIN, LENS, OUTPUT)
- [ ] Workflow defined as explicit pipeline in frontmatter
- [ ] Phase-to-skill mapping documented
- [ ] Fallback checks provided for skill invocation failure
- [ ] No hardcoded project names/paths
- [ ] Output template externalized to skill
- [ ] Quality self-check categorized by concern
- [ ] Priority rankings reflect impact
- [ ] Broad skills replaced with specialized alternatives
- [ ] Security/performance concerns shifted left
- [ ] Agent size <150 lines
- [ ] All embedded checklists extracted to skills
```

---

## Before/After Metrics

Track these when optimizing:

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Total lines | Count | Count | <150 |
| Skills count | N | N+M | More specialized |
| Embedded checklists | Count | 0 | 0 (delegated) |
| Code examples | Count | 0 | 0 (in skills) |
| Project-specific refs | Count | 0 | 0 (dynamic) |
| Output template lines | N | 0 | 0 (externalized) |

---

## Case Study: Code Reviewer Agent

**Before** (330 lines):
- 6 skills (flat list)
- 9 embedded checklists
- 3 inline code examples
- 30-line output template
- Hardcoded project paths
- Security delegated to other agent

**After** (115 lines):
- 8 skills (categorized: METHODOLOGY, DOMAIN, SECURITY LENS, PERFORMANCE LENS, OUTPUT)
- 0 embedded checklists (delegated to skills)
- 0 code examples (in skills)
- Output template externalized to `actionable-review-format-standards` skill
- Project-agnostic design
- Security first-class (OWASP, PII logging)
- Explicit workflow: `GATHER → SECURITY → PERFORMANCE → PATTERNS → REPORT`
- Skill invocation guidance with fallback

**Result**: 65% size reduction, expanded capabilities, improved maintainability.

---

## Related Patterns

- **Agent Separation of Concerns** - See `GUIDELINES.md § Agent Separation of Concerns`
- **Artifact Portability Rules** - See `GUIDELINES.md § Artifact Portability Rules`
- **Progressive Disclosure** - See `GUIDELINES.md § Skills`
- **Agent Refactoring Guide** - See `references/agent-refactoring-guide.md`
