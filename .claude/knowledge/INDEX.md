# Shared Knowledge Base

Extracted common concepts and implementations referenced by multiple skills. Follows a **three-layer architecture** separating concepts from implementations.

## Three-Layer Architecture

```
                    ┌─────────────────────────────────────┐
                    │            CONCEPTS                 │
                    │   Framework-independent principles  │
                    │          (NO CODE)                  │
                    └──────────────┬──────────────────────┘
                                   │ implements
                    ┌──────────────▼──────────────────────┐
                    │         IMPLEMENTATIONS             │
                    │   Language-specific examples        │
                    │        (WITH CODE)                  │
                    └──────────────┬──────────────────────┘
                                   │ references
                    ┌──────────────▼──────────────────────┐
                    │             SKILLS                  │
                    │   Context-aware orchestration       │
                    └─────────────────────────────────────┘
```

### Why This Structure?

| Layer | Purpose | Example |
|-------|---------|---------|
| **Concepts** | Universal principles that apply to ANY language | "Single Responsibility Principle" - one reason to change |
| **Implementations** | How to apply concepts in specific technologies | SRP in C#/ABP with code examples |
| **Skills** | When and how to apply during specific tasks | Use SRP when creating AppServices |

## Directory Structure

```
knowledge/
├── INDEX.md                      # This file
├── concepts/                     # Framework-independent principles
│   ├── INDEX.md                  # Concept registry
│   ├── clean-code/               # Clean Code principles
│   │   ├── principles.md
│   │   ├── naming.md
│   │   └── functions.md
│   ├── solid/                    # SOLID principles
│   │   ├── overview.md
│   │   ├── srp.md
│   │   ├── ocp.md
│   │   ├── lsp.md
│   │   ├── isp.md
│   │   └── dip.md
│   ├── clean-architecture/       # Architecture principles
│   │   ├── layers.md
│   │   ├── dependency-rule.md
│   │   ├── types.md
│   │   └── smells.md
│   ├── code-smells/              # Code smell taxonomy
│   │   └── taxonomy.md
│   └── testing/                  # Testing principles
│       ├── tdd-principles.md
│       ├── first.md
│       └── test-smells.md
├── implementations/              # Language-specific patterns
│   ├── INDEX.md                  # Implementation registry
│   └── dotnet/                   # .NET/C# implementations
│       ├── clean-code.md
│       ├── solid.md
│       ├── code-smells.md
│       └── xunit-tdd.md
├── entities/                     # ABP entity knowledge (legacy)
├── patterns/                     # Design patterns (legacy)
├── conventions/                  # Project conventions (legacy)
└── examples/                     # Complete examples (legacy)
```

## Quick Navigation

### By Topic

| Topic | Concept | .NET Implementation |
|-------|---------|---------------------|
| Clean Code | [concepts/clean-code/](concepts/INDEX.md#clean-code) | [implementations/dotnet/clean-code.md](implementations/dotnet/clean-code.md) |
| SOLID | [concepts/solid/](concepts/INDEX.md#solid) | [implementations/dotnet/solid.md](implementations/dotnet/solid.md) |
| Code Smells | [concepts/code-smells/](concepts/INDEX.md#code-smells) | [implementations/dotnet/code-smells.md](implementations/dotnet/code-smells.md) |
| TDD/Testing | [concepts/testing/](concepts/INDEX.md#testing) | [implementations/dotnet/xunit-tdd.md](implementations/dotnet/xunit-tdd.md) |
| Architecture | [concepts/clean-architecture/](concepts/INDEX.md#clean-architecture) | (in skills) |

### By Skill

| Skill | Concepts | Implementations |
|-------|----------|-----------------|
| clean-code-dotnet | clean-code/*, solid/* | dotnet/clean-code.md, dotnet/solid.md |
| abp-code-reviewer | code-smells/*, clean-architecture/* | dotnet/code-smells.md |
| xunit-testing-patterns | testing/* | dotnet/xunit-tdd.md |
| qa-engineer | testing/tdd-principles, testing/first | dotnet/xunit-tdd.md |
| debugging-patterns | code-smells/taxonomy | dotnet/code-smells.md |

## Usage

### From Skills

Skills reference concepts and implementations:

```markdown
## Entity Creation

For SRP application, see:
- **Concept**: [knowledge/concepts/solid/srp.md](../knowledge/concepts/solid/srp.md)
- **C# Examples**: [knowledge/implementations/dotnet/solid.md#srp](../knowledge/implementations/dotnet/solid.md#srp)
```

### From Agents

Agents compose knowledge from multiple sources:

```markdown
To review this code, apply:
1. Code smell detection from concepts/code-smells/taxonomy.md
2. C# specific patterns from implementations/dotnet/code-smells.md
```

## Legacy Structure (Migrate on Touch)

These directories contain older knowledge that will be migrated to the new structure when touched:

| Legacy Path | Migrate To |
|-------------|------------|
| entities/ | concepts/abp/entities.md + implementations/dotnet/abp-entities.md |
| patterns/ | concepts/design-patterns/ + implementations/dotnet/ |
| conventions/ | Project-specific, keep in conventions/ |
| examples/ | Move to implementations/{lang}/ |

## Cross-References

- [Concepts Index](concepts/INDEX.md) - All concepts
- [Implementations Index](implementations/INDEX.md) - All implementations
- [SKILL-INDEX.md](../SKILL-INDEX.md) - Find skills by task
- [CONTEXT-GRAPH.md](../CONTEXT-GRAPH.md) - Skill relationships
- [GUIDELINES.md](../GUIDELINES.md) - Governance rules

## Sources

- Clean Code by Robert C. Martin
- Clean Architecture by Robert C. Martin
- Clean Code Cheatsheet V2.4 by Urs Enzler
- Clean Architecture Cheatsheet V1.0 by Urs Enzler
- Clean ATDD/TDD Cheatsheet by Urs Enzler
