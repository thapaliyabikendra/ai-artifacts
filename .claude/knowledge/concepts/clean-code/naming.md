---
name: Naming Conventions
category: clean-code
implementations:
  dotnet: ../../implementations/dotnet/clean-code.md#naming
  react: ../../implementations/react/clean-code.md#naming
used_by_skills: [clean-code-dotnet, code-review-excellence]
---

# Naming Conventions

> "Names have to reflect what a variable, field, property stands for. Names have to be precise."

## The Principle

Names are the most important documentation in code. They should be:
- **Descriptive** - Reflect what the element represents
- **Unambiguous** - Only one possible interpretation
- **Pronounceable** - Can be discussed verbally
- **Searchable** - Can be found in codebase

## Why It Matters

- Names communicate intent to future readers (including yourself)
- Good names reduce need for comments
- Searchable names make refactoring easier
- Consistent naming reduces cognitive load

## Naming Rules

### Choose Descriptive/Unambiguous Names

Names must reflect what a variable, field, or property stands for. Names must be precise.

### Choose Names at Appropriate Level of Abstraction

Choose names that reflect the level of abstraction of the class or method you are working in.

### Name Interfaces After Functionality They Abstract

The name of an interface should be derived from its usage by the client.

### Name Classes After How They Implement Interfaces

The name of a class should reflect how it fulfills the functionality provided by its interface(s).

### Name Methods After What They Do

The name of a method should describe what is done, not how it is done.

### Use Long Names for Long Scopes

| Scope | Name Length |
|-------|-------------|
| Fields | Long |
| Parameters | Medium |
| Locals | Short-Medium |
| Loop variables | Short |

### Names Describe Side Effects

Names must reflect the entire functionality, including side effects.

### Standard Nomenclature Where Possible

Don't invent your own language when there is a standard.

## How to Detect Violations

- Single-letter variable names outside loop counters
- Abbreviated names that require mental translation
- Names with encodings (Hungarian notation, type prefixes)
- Generic names (data, info, item, temp, manager, handler)
- Names that don't match the abstraction level
- Inconsistent naming for same concepts

## Anti-Patterns

### Encodings in Names

Avoid prefixes, type information, or scope information in names:
- `strName` (Hungarian notation)
- `m_count` (member prefix)
- `IService` (acceptable for interfaces in some languages)

### Magic Strings/Numbers

Replace magic values with named constants to give them meaningful names when meaning cannot be derived from the value itself.

## Related Concepts

- [Clean Code Principles](principles.md) - Core principles
- [Functions](functions.md) - Method naming
- [Code Smells - Opacity](../code-smells/taxonomy.md) - Hard to understand code

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [Naming in C#](../../implementations/dotnet/clean-code.md#naming) |
| React/TS | [Naming in React](../../implementations/react/clean-code.md#naming) |

## Sources

- Clean Code by Robert C. Martin
- Clean Code Cheatsheet V2.4 by Urs Enzler
