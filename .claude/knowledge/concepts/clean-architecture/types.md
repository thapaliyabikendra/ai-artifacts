---
name: Architecture Types
category: clean-architecture
implementations: {}
used_by_skills: [backend-architect]
---

# Architecture Types

> "The architecture defines the parts of a system that are hard and costly to change."

## The Five Architecture Qualities

### 1. Clean Architecture

An architecture that allows to replace details and is easy to verify.

**Characteristics:**
- Clear layer separation
- Dependencies point inward
- Business rules isolated from frameworks
- Easy to test without external systems

### 2. Simple Architecture

An architecture that is easy to understand. (Simplicity is subjective.)

**Characteristics:**
- **Consistent design decisions** - One problem has one solution
- **Few concepts/technologies** - Simple solutions use few different technologies
- **Minimal interactions** - Less interactions = simpler design
- **Small size** - Small systems/components are easier to grasp
- **Modularity** - Independent modules with clear interfaces

### 3. Flexible Architecture

An architecture that supports change.

**Characteristics:**
- **Separation of concerns** - Features with little overlap
- **Software reflects user's mental model** - Changes in real world apply easily
- **Appropriate abstraction** - (Beware of over-abstraction)
- **Slim interfaces** - Minimal coupling between components
- **Composition over inheritance** - Reduces coupling
- **Cycle-free dependencies** - No circular dependency chains

### 4. Evolvable Architecture

An architecture that is easy to adapt step by step.

**Characteristics:**
- **Matches current needs** - Not future ones (avoid waste)
- **No dead-ends** - Can be extended/adapted
- **Architecture-agnostic components** - Components don't care about surrounding architecture
- **Sacrificial architecture** - Willingness to throw away and rebuild
- **Rolling refactoring** - Max two versions of a concept at once

### 5. Agile Architecture

An architecture that supports agile development (Agile Manifesto principles).

**Characteristics:**
- **Allows quick change** - Through flexibility and evolvability
- **Verifiable at any time** - All quality aspects can be verified (e.g., every Sprint)
- **Rapid deployment** - Supports continuous deployment
- **Always working** - Potentially shippable anytime

## Priorities

When making architecture decisions, prioritize:

| Priority | Over |
|----------|------|
| Simplicity | Generality |
| Hard-coded | Configurable |
| Use | Reuse |
| Working | Optimized |
| Quality attributes | Functional requirements |
| Small systems combined | One big system |

## How to Detect Problems

- Changes ripple through the system
- Simple features take excessive time
- Team can't explain the architecture
- New team members struggle to understand
- Technical debt accumulates rapidly
- Fear of making changes

## Related Concepts

- [Clean Architecture Layers](layers.md) - Layer structure
- [Dependency Rule](dependency-rule.md) - Key principle
- [Architecture Smells](smells.md) - Anti-patterns

## Sources

- Clean Architecture Cheatsheet V1.0 by Urs Enzler
- Agile Manifesto
