---
name: Liskov Substitution Principle
category: solid
implementations:
  dotnet: ../../implementations/dotnet/solid.md#lsp
used_by_skills: [clean-code-dotnet, code-review-excellence]
---

# Liskov Substitution Principle (LSP)

> "Derived classes must be substitutable for their base classes."

## The Principle

Objects of a superclass should be replaceable with objects of its subclasses without breaking the application. If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering any of the desirable properties of the program.

## Why It Matters

- **Correctness** - Subclasses won't break existing code
- **Predictability** - Code behaves as expected with any subtype
- **Polymorphism** - Safe to use base type references
- **Testing** - Tests for base class apply to subclasses

## LSP Rules

### Preconditions

A subclass must not strengthen preconditions. If the base class accepts a parameter, the subclass must also accept it.

### Postconditions

A subclass must not weaken postconditions. If the base class guarantees a result, the subclass must also guarantee it.

### Invariants

A subclass must preserve all invariants of the base class.

### History Constraint

A subclass should not modify state in a way that the base class doesn't allow.

## How to Detect Violations

- Subclass throws exceptions not thrown by base class
- Subclass returns different/incompatible types
- Type checking in code that uses base type
- Overridden methods that do nothing or throw `NotImplementedException`
- "Square extends Rectangle" type problems
- Client code needs to know about specific subtypes

## The Classic Example: Rectangle/Square

A Square cannot properly extend Rectangle if Rectangle has independent `SetWidth()` and `SetHeight()` methods, because Square must keep width and height equal. This violates the expectation that setting width doesn't change height.

**Solution**: Use a common abstraction (like `Shape`) with `GetArea()` instead of forcing inheritance.

## Related Concepts

- [SOLID Overview](overview.md) - All five principles
- [Interface Segregation](isp.md) - Related principle
- [Design by Contract](../clean-code/principles.md) - Pre/postconditions

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [LSP in C#](../../implementations/dotnet/solid.md#lsp) |

## Sources

- A Behavioral Notion of Subtyping by Barbara Liskov
- Clean Code Cheatsheet V2.4 by Urs Enzler
