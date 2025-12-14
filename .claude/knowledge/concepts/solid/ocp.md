---
name: Open/Closed Principle
category: solid
implementations:
  dotnet: ../../implementations/dotnet/solid.md#ocp
used_by_skills: [clean-code-dotnet, code-review-excellence]
---

# Open/Closed Principle (OCP)

> "Software entities should be open for extension, but closed for modification."

## The Principle

You should be able to extend a class's behavior without modifying it. The goal is to allow adding new functionality without changing existing, tested code.

## Why It Matters

- **Stability** - Existing code remains unchanged and stable
- **Reduced Risk** - No regression in existing functionality
- **Scalability** - Easy to add new features
- **Testing** - Existing tests don't need modification

## How to Achieve OCP

1. **Abstraction** - Use interfaces or abstract classes
2. **Polymorphism** - Let derived classes extend behavior
3. **Composition** - Inject dependencies rather than hardcode
4. **Strategy Pattern** - Encapsulate algorithms
5. **Plugin Architecture** - Load extensions dynamically

## How to Detect Violations

- Adding new functionality requires modifying existing classes
- Switch/case statements that grow with new types
- Type checking (`if (obj is TypeA)`) scattered in code
- Frequent modifications to core classes
- "Shotgun surgery" - small changes affect many files

## The Switch Statement Rule

> "ONE SWITCH": There may be no more than one switch statement for a given type of selection. The cases in that switch statement must create polymorphic objects that take the place of other such switch statements in the rest of the system.

This rule helps identify OCP violations: if you have switch statements checking types scattered throughout the code, you should refactor to use polymorphism.

## Related Concepts

- [SOLID Overview](overview.md) - All five principles
- [Single Responsibility](srp.md) - Foundation for OCP
- [Dependency Inversion](dip.md) - Enables OCP via abstractions
- [Strategy Pattern](../refactoring/patterns.md) - Common OCP implementation

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [OCP in C#](../../implementations/dotnet/solid.md#ocp) |

## Sources

- Agile Software Development by Robert C. Martin
- Clean Code Cheatsheet V2.4 by Urs Enzler
