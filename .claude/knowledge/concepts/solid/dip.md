---
name: Dependency Inversion Principle
category: solid
implementations:
  dotnet: ../../implementations/dotnet/solid.md#dip
used_by_skills: [clean-code-dotnet, code-review-excellence]
---

# Dependency Inversion Principle (DIP)

> "Depend on abstractions, not on concretions."

## The Principle

1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
2. Abstractions should not depend on details. Details should depend on abstractions.

## Why It Matters

- **Flexibility** - Easy to swap implementations
- **Testability** - Mock dependencies for unit testing
- **Decoupling** - Modules don't know concrete implementations
- **Maintainability** - Changes are isolated

## The Inversion

Traditional dependency flow:
```
High-level → Low-level
```

After applying DIP:
```
High-level → Abstraction ← Low-level
                ↑
        Both depend on this
```

## Key Mechanisms

### Dependency Injection

Pass dependencies into the constructor rather than creating them:
- Constructor injection (preferred)
- Property injection
- Method injection

### Inversion of Control (IoC)

Framework controls object creation and lifecycle, not your code.

### Service Locator (Anti-pattern)

While it inverts control, it hides dependencies. Prefer explicit DI.

## How to Detect Violations

- `new` keyword for services/dependencies in business logic
- Direct references to concrete classes in high-level modules
- Static method calls for operations that could change
- Configuration loaded directly instead of injected
- Tight coupling to specific implementations

## Singletons and Service Locator

Both are anti-patterns when misused:
- **Singletons** hide dependencies and global state
- **Service Locator** hides what a class needs

**Prefer**: Explicit constructor injection that makes dependencies visible.

## Related Concepts

- [SOLID Overview](overview.md) - All five principles
- [Open/Closed Principle](ocp.md) - DIP enables OCP
- [Clean Architecture](../clean-architecture/layers.md) - Uses DIP for layer isolation

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [DIP in C#](../../implementations/dotnet/solid.md#dip) |

## Sources

- Agile Software Development by Robert C. Martin
- Clean Code Cheatsheet V2.4 by Urs Enzler
