# Progressive Disclosure Pattern

> Extracted from GUIDELINES.md for modularity. Core pattern for context-efficient skill loading.

## Concept

Progressive disclosure loads information in stages, minimizing initial context usage while providing depth on-demand.

## Three-Level Loading

| Level | What Loads | Token Cost | When |
|-------|------------|------------|------|
| **1. Discovery** | `name` + `description` only | ~100 tokens | Startup (all skills) |
| **2. Instructions** | Full `SKILL.md` body | <5,000 tokens | When triggered |
| **3. Resources** | Scripts, references, templates | As needed | On-demand |

## Implementation Patterns

### Pattern 1: High-Level Guide with References

```markdown
# PDF Processing

## Quick Start
[Immediate actionable code - 20-30 lines]

## Core Operations
[Essential patterns - 50-100 lines]

## Advanced Features
**Form filling**: See [FORMS.md](references/forms.md)
**API reference**: See [REFERENCE.md](references/reference.md)
**Examples**: See [EXAMPLES.md](references/examples.md)
```

**Key**: Core SKILL.md stays under 500 lines; depth is in references.

### Pattern 2: Domain-Specific Organization

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    └── product.md (API usage, features)
```

**Key**: Split by domain, not by technical category.

### Pattern 3: Conditional Details

```markdown
## Creating Documents
Use docx-js for new documents. See [DOCX-JS.md](references/docx-js.md).

## Editing Documents
For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](references/redlining.md)
```

**Key**: Link to advanced content only when needed.

## Skill Structure Template

```
skills/
└── {skill-name}/
    ├── SKILL.md              # Required - entry point (<500 lines)
    ├── references/           # On-demand documentation
    │   ├── advanced.md
    │   └── examples.md
    ├── assets/               # Templates, boilerplate
    └── scripts/              # Executable helpers
```

## File Size Guidelines

| File | Max Lines | If Exceeded |
|------|-----------|-------------|
| SKILL.md | 500 | Extract to references/ |
| Reference file | 400 | Split into sub-files |
| Total skill folder | 2,000 | Consider splitting skill |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Everything in SKILL.md | High token cost every trigger | Extract to references/ |
| Nested reference folders | Hard to navigate | Keep references one level deep |
| Duplicated content in references | Maintenance burden | Single source, link elsewhere |
| No table of contents | Hard to scan | Add TOC for files >100 lines |

## When to Use Each Level

```
START: What does Claude need?
│
├─ Just skill existence? → Level 1 (Discovery)
│
├─ How to perform task? → Level 2 (Instructions)
│
└─ Specific implementation details? → Level 3 (Resources)
```

## Related

- [Context Efficiency](context-efficiency.md) - Token optimization strategies
- [Skill Optimization](skill-optimization.md) - Writing effective skills
- [GUIDELINES.md](../../GUIDELINES.md#skills-skills) - Skill overview
