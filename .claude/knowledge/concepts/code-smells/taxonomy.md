---
name: Code Smell Taxonomy
category: code-smells
implementations:
  dotnet: ../../implementations/dotnet/code-smells.md
  react: ../../implementations/react/code-smells.md
used_by_skills: [clean-code-dotnet, code-review-excellence, debugging-patterns]
---

# Code Smell Taxonomy

> "Code smells are indicators of potential problems in code that may warrant refactoring."

## The Principle

Code smells are surface indications that usually correspond to deeper problems in the system. They are not bugs - the code still works - but they indicate weaknesses in design that may slow development or increase the risk of bugs.

## Smell Categories

### 1. Change Resistance Smells

Smells that make the system resistant to change.

#### Rigidity

The software is difficult to change. A small change causes a cascade of subsequent changes.

**Symptoms:**
- "Simple" change takes weeks
- Estimates are always wrong
- Changes keep getting bigger
- Fear of touching the code

#### Fragility

The software breaks in many places due to a single change.

**Symptoms:**
- Bug fixes introduce new bugs
- Changes in module A break module B
- No confidence in deployments
- "Don't touch that code"

#### Immobility

You cannot reuse parts of the code in other projects because of involved risks and high effort.

**Symptoms:**
- Copy-paste instead of reuse
- Can't extract libraries
- Tangled dependencies prevent extraction
- Everything depends on everything

### 2. Design Viscosity Smells

Smells where doing things wrong is easier than doing them right.

#### Viscosity of Design

Taking a shortcut and introducing technical debt requires less effort than doing it right.

**Symptoms:**
- Hacks are easier than proper solutions
- Architecture fights against changes
- Proper way takes too long
- Shortcuts become the norm

#### Viscosity of Environment

Building, testing, and other tasks take too long, so they're not executed properly.

**Symptoms:**
- Builds take hours
- Tests take too long to run
- Deployment is painful
- CI/CD is avoided

### 3. Complexity Smells

Smells indicating unnecessary complexity.

#### Needless Complexity

Design contains elements not currently useful. Added complexity makes code harder to comprehend.

**Symptoms:**
- Unused abstractions
- Over-engineered solutions
- Premature optimization
- "We might need this someday"

#### Needless Repetition

Code contains exact duplications or design duplicates (same thing done differently).

**Symptoms:**
- Copy-pasted code
- Same logic in multiple places
- DRY violations
- Changes needed in multiple places

### 4. Understandability Smells

Smells that make code hard to understand.

#### Opacity

The code is hard to understand. Changes take extra time to re-engineer the code.

**Symptoms:**
- Dense algorithms
- No explanatory variables
- Magic numbers/strings
- Unclear intent

#### Obscured Intent

Too dense algorithms that lose all expressiveness.

#### Poorly Written Comments

Comments that don't add value, are redundant, or have incorrect grammar.

#### Obvious Behavior Is Unimplemented

Violations of "Principle of Least Astonishment" - what you expect is not what you get.

### 5. Dependency Smells

Smells related to how components depend on each other.

#### Feature Envy

Methods of a class are more interested in variables and functions of other classes than their own.

**Symptom:** Using accessors and mutators of another object to manipulate its data.

#### Artificial Coupling

Things that don't depend upon each other are artificially coupled.

#### Hidden Temporal Coupling

Order of method calls is important, but not enforced or visible.

#### Transitive Navigation (Law of Demeter)

A module knows too much about its dependencies' internals.

**Principle:** A module should know only its direct dependencies.

### 6. Class Design Smells

Smells in class structure.

#### Misplaced Responsibility

Something put in the wrong place.

#### Code at Wrong Level of Abstraction

Functionality is at wrong level of abstraction.

#### Fields Not Defining State

Fields hold temporary data, not instance state. Should be local variables.

#### Base Classes Depending On Their Derivatives

Base classes should work with any derived class.

#### Too Much Information

Interface exposes too much. Minimize interface to minimize coupling.

### 7. Maintainability Killers

#### Magic Numbers/Strings

Hardcoded values without named constants. Meaning cannot be derived from value itself.

#### Duplication

Violation of DRY (Don't Repeat Yourself) principle.

#### Tangles

Class dependencies have cycles. No point to start changing without side effects.

## How to Use This Taxonomy

1. **Detection** - Use as checklist during code review
2. **Prioritization** - Focus on smells blocking current work
3. **Refactoring** - Address smells during regular development
4. **Prevention** - Design to avoid common smells

## Related Concepts

- [Clean Code Principles](../clean-code/principles.md) - Prevention
- [SOLID Principles](../solid/overview.md) - Design guidelines
- [Refactoring Patterns](../refactoring/patterns.md) - Solutions
- [Architecture Smells](../clean-architecture/smells.md) - Higher-level smells

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [Code Smells in C#](../../implementations/dotnet/code-smells.md) |
| React | [Code Smells in React](../../implementations/react/code-smells.md) |

## Sources

- Clean Code by Robert C. Martin
- Refactoring by Martin Fowler
- Clean Code Cheatsheet V2.4 by Urs Enzler
