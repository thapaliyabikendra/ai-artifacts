# Guidelines Index

> **Navigation Hub**: Find the right guideline document for your need. This index prevents duplication by serving as the single source of truth for "where to find what."

## Quick Lookup

| I need to... | Read |
|--------------|------|
| Understand core principles | [GUIDELINES.md](../GUIDELINES.md) |
| Choose artifact type | [reference/decision-matrices.md](reference/decision-matrices.md) |
| Optimize context usage | [patterns/context-efficiency.md](patterns/context-efficiency.md) |
| Understand progressive disclosure | [patterns/progressive-disclosure.md](patterns/progressive-disclosure.md) |
| Learn agent separation of concerns | [patterns/agent-separation.md](patterns/agent-separation.md) |
| Create portable artifacts | [patterns/portability-patterns.md](patterns/portability-patterns.md) |
| Use tools efficiently | [patterns/tool-usage-patterns.md](patterns/tool-usage-patterns.md) |
| Write effective skills | [patterns/skill-optimization.md](patterns/skill-optimization.md) |
| See good agent examples | [examples/agent-examples.md](examples/agent-examples.md) |
| See good skill examples | [examples/skill-examples.md](examples/skill-examples.md) |
| See antipatterns to avoid | [examples/antipatterns.md](examples/antipatterns.md) |
| Follow agentic best practices | [workflows/agentic-coding-practices.md](workflows/agentic-coding-practices.md) |
| Create a new artifact | [workflows/creating-artifacts.md](workflows/creating-artifacts.md) |
| Migrate/refactor artifacts | [workflows/migration-guide.md](workflows/migration-guide.md) |
| Look up tool permissions | [reference/tool-permissions.md](reference/tool-permissions.md) |
| Choose a model | [reference/model-selection.md](reference/model-selection.md) |
| Check naming conventions | [standards/naming-conventions.md](standards/naming-conventions.md) |
| Verify file formats | [standards/file-formats.md](standards/file-formats.md) |

---

## By Document Type

### Core (Always Read First)
| Document | Purpose |
|----------|---------|
| [GUIDELINES.md](../GUIDELINES.md) | Main entry point, core principles, artifact overviews |

### Patterns (Design Principles)
| Document | Purpose |
|----------|---------|
| [progressive-disclosure.md](patterns/progressive-disclosure.md) | Three-level loading for context efficiency |
| [tool-usage-patterns.md](patterns/tool-usage-patterns.md) | Grep/Glob/Read/Edit efficiency |
| [agent-separation.md](patterns/agent-separation.md) | Thin coordinators vs embedded knowledge |
| [skill-optimization.md](patterns/skill-optimization.md) | Writing concise, effective skills |
| [context-efficiency.md](patterns/context-efficiency.md) | Token optimization strategies |
| [portability-patterns.md](patterns/portability-patterns.md) | Generic, reusable artifacts |

### Standards (Rules & Conventions)
| Document | Purpose |
|----------|---------|
| [naming-conventions.md](standards/naming-conventions.md) | Naming rules for all artifact types |
| [file-formats.md](standards/file-formats.md) | Frontmatter and structure requirements |

### Examples (Learning)
| Document | Purpose |
|----------|---------|
| [agent-examples.md](examples/agent-examples.md) | Good and bad agent structures |
| [skill-examples.md](examples/skill-examples.md) | Good and bad skill structures |
| [antipatterns.md](examples/antipatterns.md) | Common mistakes to avoid |

### Workflows (How-To Guides)
| Document | Purpose |
|----------|---------|
| [agentic-coding-practices.md](workflows/agentic-coding-practices.md) | Anthropic's best practices |
| [creating-artifacts.md](workflows/creating-artifacts.md) | Step-by-step artifact creation |
| [migration-guide.md](workflows/migration-guide.md) | Refactoring bloated artifacts |

### Reference (Lookup Tables)
| Document | Purpose |
|----------|---------|
| [decision-matrices.md](reference/decision-matrices.md) | All decision flowcharts consolidated |
| [tool-permissions.md](reference/tool-permissions.md) | Tool access patterns by agent type |
| [model-selection.md](reference/model-selection.md) | Haiku vs Sonnet vs Opus guidance |

---

## Cross-Reference to Indexes

These indexes exist at the `.claude/` root level:

| Index | Purpose |
|-------|---------|
| [SKILL-INDEX.md](../SKILL-INDEX.md) | Find skills by task/keyword/error |
| [CONTEXT-GRAPH.md](../CONTEXT-GRAPH.md) | Skill dependencies and load order |
| [COMMAND-INDEX.md](../COMMAND-INDEX.md) | Command discovery by action |
| [AGENT-QUICK-REF.md](../AGENT-QUICK-REF.md) | Agent selection by task |

---

## Usage Patterns

### For Claude (claude-artifact-creator skill)

1. **Always read**: [GUIDELINES.md](../GUIDELINES.md) for core principles
2. **Read on-demand**: Specific pattern/example docs as needed
3. **Never duplicate**: If pattern exists here, reference it; don't embed

### For Humans

1. Start with [GUIDELINES.md](../GUIDELINES.md)
2. Use this index to find deep-dives
3. Bookmark frequently used patterns

---

## Maintenance Rules

| Rule | When |
|------|------|
| **New pattern** | Create in `patterns/`, add to this index |
| **New example** | Create in `examples/`, add to this index |
| **New workflow** | Create in `workflows/`, add to this index |
| **New standard** | Create in `standards/`, add to this index |
| **Duplicated content found** | Extract to appropriate folder, replace with link |
| **GUIDELINES.md over 1000 lines** | Extract section here, add link |

### Size Limits

| Document | Max Lines | If Exceeded |
|----------|-----------|-------------|
| GUIDELINES.md | 1,000 | Extract to guidelines/ |
| Pattern docs | 400 | Split into sub-patterns |
| Example docs | 500 | Split by category |
| This INDEX.md | 200 | Remove redundant entries |

### Quarterly Health Check

- [ ] GUIDELINES.md under 1,000 lines?
- [ ] Any section >200 lines? → Extract
- [ ] Any concept in 2+ places? → Consolidate
- [ ] All docs referenced in this INDEX?
- [ ] All cross-references valid?
