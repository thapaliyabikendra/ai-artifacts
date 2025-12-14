---
name: SOLID Principles Overview
category: solid
implementations:
  dotnet: ../../implementations/dotnet/solid.md
used_by_skills: [clean-code-dotnet, code-review-excellence, abp-code-reviewer]
---

# SOLID Principles

> "The SOLID principles are a set of design principles that help developers create more maintainable, flexible, and scalable software."

## The Principles

SOLID is an acronym for five object-oriented design principles:

| Letter | Principle | Summary |
|--------|-----------|---------|
| **S** | [Single Responsibility](srp.md) | A class should have one reason to change |
| **O** | [Open/Closed](ocp.md) | Open for extension, closed for modification |
| **L** | [Liskov Substitution](lsp.md) | Subtypes must be substitutable for base types |
| **I** | [Interface Segregation](isp.md) | Many specific interfaces over one general |
| **D** | [Dependency Inversion](dip.md) | Depend on abstractions, not concretions |

## Why It Matters

SOLID principles help achieve:

- **Maintainability** - Easier to understand and modify
- **Flexibility** - Easier to adapt to changing requirements
- **Testability** - Easier to write unit tests
- **Reusability** - Components can be used in different contexts
- **Reduced Coupling** - Changes don't ripple through the system

## When to Apply

- Designing new classes and modules
- Refactoring existing code
- Code reviews
- Architectural decisions

## The Relationship Between Principles

```
                    ┌─────────────────────┐
                    │       SRP           │
                    │  (One Reason to     │
                    │      Change)        │
                    └──────────┬──────────┘
                               │ enables
                               ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│      ISP        │────►│       OCP       │◄────│       LSP       │
│  (Small         │     │  (Extend, Don't │     │  (Substitutable │
│   Interfaces)   │     │    Modify)      │     │   Subtypes)     │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 │ achieved via
                                 ▼
                    ┌─────────────────────┐
                    │       DIP           │
                    │  (Depend on         │
                    │   Abstractions)     │
                    └─────────────────────┘
```

## How to Detect Violations

- Class has many unrelated methods (SRP violation)
- Adding features requires modifying existing code (OCP violation)
- Subclass can't replace base class without breaking (LSP violation)
- Classes implement methods they don't need (ISP violation)
- High-level modules depend on low-level details (DIP violation)

## Related Concepts

- [Clean Code Principles](../clean-code/principles.md) - Foundation
- [Code Smells](../code-smells/taxonomy.md) - Indicators of violations
- [Package Design](../package-design/cohesion.md) - Module-level principles

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [SOLID in C#](../../implementations/dotnet/solid.md) |

## Sources

- Agile Software Development: Principles, Patterns, and Practices by Robert C. Martin
- Clean Code Cheatsheet V2.4 by Urs Enzler
