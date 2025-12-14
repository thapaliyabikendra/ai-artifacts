---
name: Function Design
category: clean-code
implementations:
  dotnet: ../../implementations/dotnet/clean-code.md#functions
  react: ../../implementations/react/clean-code.md#functions
used_by_skills: [clean-code-dotnet, code-review-excellence]
---

# Function Design

> "Functions should do one thing. They should do it well. They should do it only."

## The Principle

Functions are the first line of organization in any program. Writing them well is essential for clean code.

## Why It Matters

- Small functions are easier to understand and test
- Single-purpose functions are easier to name
- Functions with few arguments are easier to call correctly
- Side-effect-free functions are easier to reason about

## Function Rules

### Functions Should Do One Thing

A function should do one thing and do it well. Signs of doing too much:
- Loops, exception handling, etc. should be in sub-methods
- The function can be meaningfully split into smaller functions
- Different abstraction levels in one function

### Functions Should Descend One Level of Abstraction

The statements within a method should all be written at the same level of abstraction, which should be one level below the operation described by the name of the function.

### Limit Function Arguments

Prefer fewer arguments:
- Zero (niladic) - best
- One (monadic) - good
- Two (dyadic) - acceptable
- Three (triadic) - avoid if possible
- More than three - requires strong justification

If many arguments are needed, consider grouping them into an object.

### Avoid Side Effects

Functions should not:
- Modify global state
- Modify input parameters (unexpected)
- Depend on hidden state

Pure functions (same input = same output) are easiest to understand and test.

### Avoid Flag Arguments

Boolean flag arguments indicate the function does more than one thing. Split into separate functions instead.

### Avoid Output Arguments

If a function must change state, have it change the state of the object it is called on.

### Encapsulate Conditionals

Extract complex conditional logic into well-named methods.

## How to Detect Violations

- Function longer than ~20 lines
- More than 3 arguments
- Boolean flag parameters
- Name doesn't describe what function does
- Function modifies things unexpectedly
- Multiple levels of abstraction in one function
- Deep nesting (>2 levels)

## Anti-Patterns

### Selector/Flag Arguments

Functions like `process(data, isVerbose)` where the flag changes behavior should be split into `processVerbose(data)` and `process(data)`.

### Inappropriate Static Methods

Static methods that should be instance methods - they often hide dependencies.

### Method with Out/Ref Arguments

Prevent usage. Return complex objects holding all values, or split into several methods.

## Related Concepts

- [Clean Code Principles](principles.md) - Core principles
- [Naming](naming.md) - Function naming
- [SRP](../solid/srp.md) - Single Responsibility

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [Functions in C#](../../implementations/dotnet/clean-code.md#functions) |
| React/TS | [Functions in React](../../implementations/react/clean-code.md#functions) |

## Sources

- Clean Code by Robert C. Martin, Chapter 3
- Clean Code Cheatsheet V2.4 by Urs Enzler
