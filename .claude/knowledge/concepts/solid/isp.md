---
name: Interface Segregation Principle
category: solid
implementations:
  dotnet: ../../implementations/dotnet/solid.md#isp
used_by_skills: [clean-code-dotnet, code-review-excellence]
---

# Interface Segregation Principle (ISP)

> "Make fine-grained interfaces that are client-specific."

## The Principle

Clients should not be forced to depend upon interfaces they do not use. Instead of one large interface, many small interfaces are preferred based on groups of methods, each serving one submodule.

## Why It Matters

- **Reduced coupling** - Clients only know about methods they use
- **Easier implementation** - Classes don't implement unused methods
- **Better evolution** - Changes affect fewer clients
- **Clearer contracts** - Purpose of each interface is obvious

## How to Apply

1. **Identify client groups** - Who uses which methods?
2. **Separate by usage** - Group methods by client needs
3. **Create role interfaces** - Small, focused contracts
4. **Allow multiple interfaces** - Classes can implement several

## How to Detect Violations

- Interfaces with many methods (>5-7 is a smell)
- Classes implementing methods with `throw new NotImplementedException()`
- Classes implementing methods that do nothing
- Different clients using different subsets of an interface
- Interface name too generic (e.g., `IManager`, `IService`)
- Changes to interface affect unrelated clients

## Interface Segregation Patterns

### Role Interface

Create interfaces based on roles that clients play:
- `IReadable` - for readers
- `IWritable` - for writers
- `IRepository<T>` combines both for full access

### Client-Specific Interface

Name interfaces after what clients need:
- `IOrderProcessor` - for order handling
- `IOrderViewer` - for order display

## Related Concepts

- [SOLID Overview](overview.md) - All five principles
- [Single Responsibility](srp.md) - Applied to interfaces
- [Dependency Inversion](dip.md) - Uses segregated interfaces

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [ISP in C#](../../implementations/dotnet/solid.md#isp) |

## Sources

- Agile Software Development by Robert C. Martin
- Clean Code Cheatsheet V2.4 by Urs Enzler
