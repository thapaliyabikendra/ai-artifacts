---
name: Single Responsibility Principle
category: solid
implementations:
  dotnet: ../../implementations/dotnet/solid.md#srp
used_by_skills: [clean-code-dotnet, code-review-excellence, abp-code-reviewer]
---

# Single Responsibility Principle (SRP)

> "A class should have one, and only one, reason to change."

## The Principle

A module should be responsible to one, and only one, actor (stakeholder or user). When a class has more than one responsibility, changes to one responsibility may affect or break the other.

**Alternative formulation**: Gather together the things that change for the same reasons. Separate those things that change for different reasons.

## Why It Matters

- **Reduced coupling** - Changes in one responsibility don't affect others
- **Easier testing** - Smaller, focused classes are easier to test
- **Better organization** - Clear purpose for each class
- **Parallel development** - Different responsibilities can be worked on independently
- **Reusability** - Focused classes are more reusable

## How to Identify Responsibilities

Ask these questions:
1. Who are the actors (users/stakeholders) that might request changes?
2. What different reasons could this class need to change?
3. Can you describe what this class does without using "and"?

## How to Detect Violations

### Observable Symptoms

- Class name contains "And", "Manager", "Handler", "Processor" (vague)
- Class has many unrelated public methods
- Different methods use completely different dependencies
- Changes for one feature require touching unrelated methods
- Unit tests require mocking many unrelated dependencies

### Constructor Dependency Count

The number of constructor dependencies is a strong indicator:

| Dependencies | Status | Action |
|--------------|--------|--------|
| 1-5 | Normal | Acceptable |
| 6-8 | Warning | Review for splitting opportunities |
| 9+ | Smell | Refactor required |

### The "Describe It" Test

Can you describe what the class does in one sentence without using "and" or "or"?
- "This class manages user authentication" - OK
- "This class manages users and sends emails and logs activity" - Violation

## Refactoring Strategies

1. **Extract Service** - Move related operations to dedicated service
2. **Facade Pattern** - Group related dependencies behind a facade
3. **Domain Events** - Decouple via publish/subscribe
4. **Mediator Pattern** - Reduce direct dependencies

## Related Concepts

- [SOLID Overview](overview.md) - All five principles
- [Open/Closed Principle](ocp.md) - Extension without modification
- [High Cohesion](../clean-code/principles.md) - Related concept
- [Code Smells](../code-smells/taxonomy.md) - Violation indicators

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [SRP in C#](../../implementations/dotnet/solid.md#srp) |

## Sources

- Agile Software Development by Robert C. Martin
- Clean Code Cheatsheet V2.4 by Urs Enzler
