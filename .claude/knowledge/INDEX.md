# Shared Knowledge Base

Extracted common concepts referenced by multiple skills. Like Context7's documentation chunks.

## Purpose

This directory contains **shared knowledge** that:
- Reduces duplication across skills
- Provides single source of truth
- Enables progressive disclosure
- Improves consistency

## Directory Structure

```
knowledge/
├── INDEX.md                 # This file
├── entities/                # Entity-related knowledge
│   ├── base-classes.md      # ABP entity base classes
│   ├── audit-properties.md  # Audit trail properties
│   └── soft-delete.md       # Soft delete pattern
├── patterns/                # Design patterns
│   ├── repository.md        # Repository pattern
│   ├── unit-of-work.md      # Unit of Work pattern
│   └── specification.md     # Specification pattern
├── conventions/             # Project conventions
│   ├── naming.md            # Naming conventions
│   ├── folder-structure.md  # Project structure
│   └── permissions.md       # Permission naming
└── examples/                # Complete examples
    ├── crud-entity.md       # Full CRUD example
    └── validation-chain.md  # Validation pipeline
```

## Quick Reference

### By Topic

| Topic | File | Used By Skills |
|-------|------|----------------|
| Entity inheritance | entities/base-classes.md | abp-framework-patterns, efcore-patterns |
| Audit properties | entities/audit-properties.md | abp-framework-patterns, efcore-patterns |
| Soft delete | entities/soft-delete.md | abp-framework-patterns, efcore-patterns |
| Repository pattern | patterns/repository.md | abp-framework-patterns |
| Unit of Work | patterns/unit-of-work.md | abp-framework-patterns, efcore-patterns |
| Specification | patterns/specification.md | abp-framework-patterns, linq-optimization |
| Naming rules | conventions/naming.md | All backend skills |
| Project structure | conventions/folder-structure.md | All skills |
| Permission format | conventions/permissions.md | openiddict-authorization, abp-framework |

### By Skill

| Skill | References |
|-------|------------|
| abp-framework-patterns | entities/*, patterns/*, conventions/* |
| efcore-patterns | entities/base-classes.md, patterns/unit-of-work.md |
| fluentvalidation-patterns | conventions/naming.md |
| openiddict-authorization | conventions/permissions.md |
| xunit-testing-patterns | examples/crud-entity.md |

## Usage Pattern

Skills reference shared knowledge like this:

```markdown
## Entity Creation

For base class selection, see [knowledge/entities/base-classes.md](../../knowledge/entities/base-classes.md).

[Rest of skill-specific content...]
```

## Cross-References

- [SKILL-INDEX.md](../SKILL-INDEX.md) - Find skills by task
- [CONTEXT-GRAPH.md](../CONTEXT-GRAPH.md) - Skill relationships
- [flows/INDEX.md](../flows/INDEX.md) - Multi-skill workflows
