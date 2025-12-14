# Skill Template (QMD Format)

Use this template when creating new skills. Copy and customize.

---

```markdown
---
name: {skill-name}
description: "{One-line description under 100 chars. Start with verb.}"
layer: {1|2|3|4}
tech_stack: [{tech1}, {tech2}]
topics: [{topic1}, {topic2}]
depends_on: [{prerequisite-skills}]
complements: [{related-skills}]
keywords: [{grep-target1}, {grep-target2}]
used_by: [{agent1}, {agent2}]
---

# {Skill Title}

## Summary

2-3 sentences explaining what this skill does and when to use it.
Key capabilities: X, Y, Z.

---

## Quick Reference

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Pattern1 | Condition | `code` |
| Pattern2 | Condition | `code` |

---

## Patterns

### Pattern 1: Name

Description...

\`\`\`{lang}
// Code example
\`\`\`

### Pattern 2: Name

Description...

\`\`\`{lang}
// Code example
\`\`\`

---

## Examples

### Example 1: Scenario

\`\`\`{lang}
// Full working example
\`\`\`

---

## Checklist

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

---

## Related

- [skill-name](../skill-name/SKILL.md) - Description
- [skill-name](../skill-name/SKILL.md) - Description
```

---

## Layer Guide

| Layer | Purpose | Examples |
|-------|---------|----------|
| 1 | Foundations (no deps) | csharp-advanced, dotnet-async |
| 2 | Framework patterns | abp-framework, efcore-patterns |
| 3 | Feature-specific | xunit-testing, security-patterns |
| 4 | Workflows/orchestration | feature-development-workflow |

---

## Structure Rules

1. **Frontmatter**: Max 20 lines, `description` < 100 chars
2. **## Summary**: Required, 2-3 sentences
3. **## Quick Reference**: Required, lookup tables
4. **---**: Horizontal rule separates major sections
5. **### Subsections**: Use level-3 for subsections

---

## Section Detection

Sections are detected by headings and separators:
- `## Heading` starts a section
- `---` or next `## ` ends a section
- No custom markers needed
