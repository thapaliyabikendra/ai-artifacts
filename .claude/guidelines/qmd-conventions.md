# QMD Conventions (Queryable Markdown)

Token-efficient documentation format using native markdown features for section-based retrieval.

---

## Summary

QMD uses **standard markdown** with consistent conventions to enable:
- Section extraction via `---` boundaries
- Grep-based lookups via heading patterns
- Link references via `file.md#section-name`

**No custom syntax. Pure markdown.**

---

## Core Principles

### 1. Sections are Bounded

Every major section ends with `---`:

```markdown
## Section Name
Content here...

---

## Next Section
```

### 2. Headings Define Structure

| Level | Purpose | Example |
|-------|---------|---------|
| `#` | Document title | `# LINQ Optimization Patterns` |
| `##` | Major sections | `## Anti-Patterns` |
| `###` | Items within sections | `### N+1 Query` |
| `####` | Sub-parts of items | `#### Bad:` |

### 3. Bold Keys for Metadata

Use `**Key**:` for structured data within items:

```markdown
### N+1 Query

**Severity**: HIGH
**Detect**: `foreach.*await.*Repository`

**Bad**:
```csharp
// code
```

**Fix**:
```csharp
// code
```
```

### 4. Anchors Work Naturally

Every heading auto-generates an anchor:

| Heading | Anchor |
|---------|--------|
| `## Anti-Patterns` | `#anti-patterns` |
| `### N+1 Query` | `#n1-query` |
| `### Count After Pagination` | `#count-after-pagination` |

**Reference**: `linq-optimization.md#anti-patterns`

---

## Standard Sections

### For Skills

```markdown
---
name: skill-name
description: "Brief description"
keywords: [grep, targets]
---

# Skill Title

## Summary
2-3 sentences. When to use.

---

## Quick Reference
| Item | Usage | Notes |
|------|-------|-------|

---

## Patterns
### Pattern Name
**When**: Use case
```code```

---

## Anti-Patterns
### Anti-Pattern Name
**Severity**: HIGH | MEDIUM | LOW
**Detect**: `grep pattern`

**Bad**:
```code```

**Why**: Explanation

**Fix**:
```code```

---

## Rules
### Rule Name
Plain English rule statement.

---

## Checklist
- [ ] Check item

---
```

### For Agents

```markdown
---
name: agent-name
description: "Brief description"
tools: [Tool1, Tool2]
skills: [skill-a, skill-b]
---

# Agent Name

## Summary
What this agent does.

---

## Scope
**Does**: List of responsibilities
**Does NOT**: Explicit exclusions

---

## Workflow
1. Step one
2. Step two

---

## Handoffs
| From | To | When |
|------|-----|------|

---
```

---

## Section Extraction

### Algorithm

```
1. Grep("^## Section Name$", file)     → line N
2. Grep("^---$", file, offset: N+1)    → line M
3. Read(file, offset: N, limit: M-N)   → exact section
```

### Examples

```bash
# Get Anti-Patterns section
Grep("^## Anti-Patterns$", skill.md)    → line 73
Grep("^---$", skill.md, offset: 74)     → line 210
Read(skill.md, offset: 73, limit: 137)  → section content

# Get specific anti-pattern
Grep("^### N\+1 Query$", skill.md)      → line 75
Grep("^---$", skill.md, offset: 76)     → line 105
Read(skill.md, offset: 75, limit: 30)   → item content
```

---

## Grep Patterns

### Section Headers

| Target | Pattern |
|--------|---------|
| All major sections | `^## ` |
| All items | `^### ` |
| Specific section | `^## Anti-Patterns$` |
| Specific item | `^### N\+1 Query$` |

### Metadata Fields

| Target | Pattern |
|--------|---------|
| All severities | `\*\*Severity\*\*:` |
| Critical items | `\*\*Severity\*\*: CRITICAL` |
| Detection patterns | `\*\*Detect\*\*:` |
| Bad code blocks | `\*\*Bad\*\*:` |
| Fix code blocks | `\*\*Fix\*\*:` |

### Cross-File Searches

```bash
# Find all HIGH severity anti-patterns across skills
Grep("\*\*Severity\*\*: HIGH", .claude/skills/)

# Find all detection patterns
Grep("\*\*Detect\*\*:", .claude/skills/)

# Find all checklists
Grep("^## Checklist$", .claude/skills/)
```

---

## Linking

### Within Same File

```markdown
See [Anti-Patterns](#anti-patterns) for common mistakes.
The [N+1 Query](#n1-query) anti-pattern is most common.
```

### Cross-File

```markdown
See [security-patterns.md#authorization](../security-patterns/SKILL.md#authorization)
Refer to [content-retrieval](../content-retrieval/SKILL.md) for extraction protocol.
```

### From CLAUDE.md or Other Docs

```markdown
For LINQ optimization, see [.claude/skills/linq-optimization-patterns/SKILL.md#anti-patterns]
```

---

## Anti-Pattern Format

Each anti-pattern should have:

```markdown
### Anti-Pattern Name

**Severity**: CRITICAL | HIGH | MEDIUM | LOW
**Detect**: `regex pattern for grep`

**Bad**:
```language
// Problematic code
```

**Why**: Explanation of the problem and impact.

**Fix**:
```language
// Corrected code
```
```

### Severity Guidelines

| Level | Criteria |
|-------|----------|
| CRITICAL | Security vulnerability, data loss |
| HIGH | Performance blocker, incorrect behavior |
| MEDIUM | Inefficiency, code smell |
| LOW | Style, minor improvement |

---

## Quick Reference Format

Include a Quick Reference table near the top for fast lookups:

```markdown
## Quick Reference

| Problem | Solution | Severity | Detect |
|---------|----------|----------|--------|
| N+1 queries | Use Include | HIGH | `foreach.*await` |
| Count after page | Count first | HIGH | `Count.*ToList` |
```

**Benefits**:
- Single grep for overview
- Detection patterns in one place
- Severity visible without reading details

---

## Checklist Format

End skills with a checklist for review use:

```markdown
## Checklist

- [ ] No queries inside loops
- [ ] Count before pagination
- [ ] Projections for DTOs
- [ ] Authorization on mutations
```

---

## File Authoring Checklist

When creating QMD-compliant files:

- [ ] Frontmatter under 15 lines
- [ ] `## Summary` section (2-3 sentences)
- [ ] `---` after every `##` section
- [ ] `## Quick Reference` with lookup table
- [ ] Anti-patterns have **Severity**, **Detect**, **Bad**, **Why**, **Fix**
- [ ] `## Checklist` at end
- [ ] Headings use consistent hierarchy
- [ ] Anchors tested (no special characters that break)

---

## Migration Guide

To convert existing skills to QMD:

1. **Add `---` boundaries** after each `##` section
2. **Consolidate anti-patterns** into single `## Anti-Patterns` section
3. **Add Quick Reference table** at top with Detect patterns
4. **Add metadata fields** to each anti-pattern (Severity, Detect)
5. **Add Checklist section** at end
6. **Test extraction**: Grep section header, verify `---` boundary works

---

## Related

- [content-retrieval](../skills/content-retrieval/SKILL.md) - Depth levels and extraction protocol
- [GUIDELINES.md](../GUIDELINES.md) - Overall artifact standards
- [SKILL-INDEX.md](../SKILL-INDEX.md) - Skill discovery

---
