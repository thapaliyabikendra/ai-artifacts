---
name: Clean Code Principles
category: clean-code
implementations:
  dotnet: ../../implementations/dotnet/clean-code.md
  react: ../../implementations/react/clean-code.md
used_by_skills: [clean-code-dotnet, code-review-excellence]
---

# Clean Code Principles

> "Code is clean if it can be understood easily - by everyone on the team."

## The Principle

Clean code is code that can be understood easily by everyone on the team. With understandability comes readability, changeability, extensibility, and maintainability - all things needed to keep a project going over a long time without accumulating a large amount of technical debt.

## Why It Matters

### The Cost of Change

Writing clean code from the start is an investment in keeping the **cost of change** as constant as possible throughout the lifecycle of a software product.

- **Initial cost** is slightly higher than quick-and-dirty code
- **Payback** comes quickly as maintenance begins
- **Unclean code** results in technical debt that increases over time
- **Responsiveness to change** decreases as debt accumulates

### In Clean Code, Bugs Cannot Hide

Most software defects are introduced when changing existing code. The reason: the developer changing the code cannot fully grasp the effects of the changes made. Clean code minimizes this risk by making code as easy to understand as possible.

## Core Principles

### 1. Loose Coupling

Two classes, components, or modules are coupled when at least one of them uses the other. The less these items know about each other, the looser they are coupled.

A component that is only loosely coupled to its environment can be more easily changed or replaced than a strongly coupled component.

### 2. High Cohesion

Cohesion is the degree to which elements of a whole belong together. Methods and fields in a single class, and classes of a component, should have high cohesion.

High cohesion results in simpler, more easily understandable code structure and design.

### 3. Change is Local

When a software system has to be maintained, extended, and changed for a long time, keeping change local reduces involved costs and risks.

Keeping change local means there are boundaries in the design which changes do not cross.

### 4. It is Easy to Remove

We normally build software by adding, extending, or changing features. However, removing elements is important so that the overall design can be kept as simple as possible.

When a block gets too complicated, it has to be removed and replaced with one or more simpler blocks.

### 5. Mind-sized Components

Break your system down into components that are of a size you can grasp within your mind so that you can predict consequences of changes easily (dependencies, control flow, etc.).

## How to Detect Violations

- Code requires extensive explanation to understand
- New team members take excessive time to become productive
- Fear of changing code due to unknown side effects
- Bug fixes introduce new bugs
- Simple changes require modifications in many places
- Duplicated logic across the codebase

## Related Concepts

- [Naming](naming.md) - Meaningful names
- [Functions](functions.md) - Single-purpose functions
- [SOLID Principles](../solid/overview.md) - Object-oriented design
- [Code Smells](../code-smells/taxonomy.md) - Design problem indicators

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [Clean Code in C#](../../implementations/dotnet/clean-code.md) |
| React/TS | [Clean Code in React](../../implementations/react/clean-code.md) |

## Sources

- Clean Code: A Handbook of Agile Software Craftsmanship by Robert C. Martin
- Clean Code Cheatsheet V2.4 by Urs Enzler (bbv Software Services)
