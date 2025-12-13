# Skill Optimization Patterns

> Extracted from GUIDELINES.md for modularity. Best practices for writing effective skills.

## Core Principle

**Concise is key.** Challenge each piece of information for its token cost.

## Skill Structure

```
skills/
└── {skill-name}/
    ├── SKILL.md              # Required - entry point (<500 lines)
    ├── references/           # On-demand documentation
    │   ├── advanced.md
    │   └── api.md
    ├── assets/               # Templates, boilerplate
    └── scripts/              # Executable helpers
```

## SKILL.md Template

```yaml
---
name: skill-name                    # max 64 chars, lowercase/numbers/hyphens
description: |                      # max 1024 chars, no XML tags
  What it does. Use when: (1) scenario, (2) scenario, (3) scenario.
tech_stack: [dotnet, csharp, abp]   # Languages/frameworks used
allowed-tools: Read, Grep, Glob     # Optional: restrict tools
---

# Skill Name

## Quick Start
[Immediate, actionable content - 20-30 lines]

## Core Patterns
[Essential patterns with code examples - 100-200 lines]

## Advanced Topics
**Topic A**: See [TOPIC_A.md](references/topic_a.md)
**Topic B**: See [TOPIC_B.md](references/topic_b.md)
```

## Writing Effective Descriptions

**Always write in third person** - descriptions are injected into system prompts.

| Good | Avoid |
|------|-------|
| "Processes Excel files and generates reports" | "I can help you process Excel files" |
| "Extracts text from PDF documents" | "You can use this to extract text" |

**Be specific and include triggers (3+ scenarios):**

```yaml
# Good: Specific with triggers
description: |
  Extract text and tables from PDF files, fill forms, merge documents.
  Use when: (1) working with PDF files, (2) user mentions PDFs/forms,
  (3) document extraction needed.

# Bad: Vague
description: Helps with documents
```

## Naming Conventions

Use **gerund form** (verb + -ing) or topic-based:

| Good (Gerund) | Good (Topic) | Avoid |
|---------------|--------------|-------|
| `processing-pdfs` | `pdf-processing` | `helper` |
| `analyzing-spreadsheets` | `spreadsheet-analysis` | `utils` |
| `managing-databases` | `database-management` | `tools` |

## Tech Stack Enforcement

The `tech_stack` field declares allowed languages/frameworks:

| Category | Values |
|----------|--------|
| **Backend** | `dotnet`, `csharp`, `abp`, `efcore`, `grpc` |
| **Frontend** | `typescript`, `react`, `javascript` |
| **Testing** | `xunit`, `playwright`, `jest`, `vitest` |
| **Infrastructure** | `docker`, `postgresql`, `redis`, `git`, `bash` |
| **Design** | `agnostic`, `markdown`, `mermaid`, `yaml` |

## Size Guidelines

| Component | Max | If Exceeded |
|-----------|-----|-------------|
| SKILL.md | 500 lines | Extract to references/ |
| Reference file | 400 lines | Split into sub-files |
| Code example | 50 lines | Simplify or split |
| Description | 1024 chars | Condense |

## Best Practices

1. **Keep references one level deep** - All reference files link directly from SKILL.md
2. **Include TOC for long files** - For reference files >100 lines
3. **Test with all models** - What works for Opus might need more detail for Haiku
4. **Avoid time-sensitive information** - Use "old patterns" sections instead of dates
5. **Use consistent terminology** - Choose one term and use it throughout

## Workflow Checklist Pattern

For complex operations, provide a checklist:

```markdown
## Document Processing Workflow

Copy this checklist and track progress:

```
Task Progress:
- [ ] Step 1: Analyze input
- [ ] Step 2: Create mapping
- [ ] Step 3: Validate
- [ ] Step 4: Execute
- [ ] Step 5: Verify output
```
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Everything in SKILL.md | Too large, always loaded | Extract to references/ |
| Verbose explanations | Wastes tokens | Claude knows most concepts |
| Duplicated content | Maintenance burden | Single source, reference |
| Nested reference folders | Hard to navigate | Keep flat |
| No specific triggers | Won't auto-activate | Add 3+ trigger scenarios |

## Quality Checklist

Before sharing a skill:

- [ ] Description is specific and includes key terms
- [ ] Description includes 3+ "Use when:" scenarios
- [ ] SKILL.md body under 500 lines
- [ ] Additional details in separate reference files
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep
- [ ] Tested with Haiku, Sonnet, and Opus

## Related

- [Progressive Disclosure](progressive-disclosure.md) - Three-level loading
- [Context Efficiency](context-efficiency.md) - Token optimization
- [GUIDELINES.md](../../GUIDELINES.md#skills-skills) - Skill overview
