# Agent Template (QMD Format)

Use this template when creating new agents. Copy and customize.

---

```markdown
---
name: {agent-name}
description: "{One-line description. Start with verb. When to use.}"
tools: {Tool1}, {Tool2}, {Tool3}
model: {sonnet|opus|haiku}
permissionMode: {default|acceptEdits|bypassPermissions}
layer: {1|2|3|4}
keywords: [{grep-target1}, {grep-target2}]
skills: {skill1}, {skill2}, {skill3}
understands:
  - {concept/topic}
  - {concept/topic}
applies:
  - {implementation/pattern}
---

# {Agent Title}

## Summary

You are a {role} specializing in {domain}.
Primary responsibilities: X, Y, Z.

---

## Scope

**Does**:
- Task 1
- Task 2
- Task 3

**Does NOT**:
- Task A (→ `other-agent`)
- Task B (→ `other-agent`)

---

## Quick Reference

### Key Info
| Item | Value |
|------|-------|
| Model | sonnet |
| Category | engineer |

### Skills Auto-Loaded
| Skill | Purpose |
|-------|---------|
| skill-name | What it does |

---

## Project Context

Before starting:
1. Read `CLAUDE.md` for project overview
2. Read `docs/architecture/README.md` for structure
3. Read feature-specific docs if applicable

---

## Workflow

### Step 1: Name
Description...

### Step 2: Name
Description...

---

## Constraints

- Constraint 1
- Constraint 2
- Constraint 3

---

## Inter-Agent Communication

| Direction | Agent | Data |
|-----------|-------|------|
| **From** | agent-name | Input description |
| **To** | agent-name | Output description |

---

## Related

- [AGENT-INDEX.md](../../AGENT-INDEX.md) - Agent lookup
- [SKILL-INDEX.md](../../SKILL-INDEX.md) - Skill lookup
```

---

## Agent Categories

| Category | Purpose | Writes Code |
|----------|---------|-------------|
| architect | Design, specs | No |
| engineer | Implementation | Yes |
| reviewer | Code review | No |
| specialist | Specific tasks | Varies |

---

## Structure Rules

1. **Frontmatter**: Max 20 lines, `description` < 100 chars
2. **## Summary**: Required, role and responsibilities
3. **## Scope**: Required, Does/Does NOT
4. **## Quick Reference**: Lookup tables
5. **---**: Horizontal rule separates major sections

---

## Section Detection

Sections are detected by headings and separators:
- `## Heading` starts a section
- `---` or next `## ` ends a section
- No custom markers needed
