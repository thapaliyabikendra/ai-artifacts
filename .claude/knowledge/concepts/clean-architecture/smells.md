---
name: Architecture Smells
category: clean-architecture
implementations: {}
used_by_skills: [backend-architect, abp-code-reviewer]
---

# Architecture Smells

> "Causes: applying a design solution in an inappropriate context, mixing design fragments that have undesirable emergent behaviors."

## Architecture Smells

### Overlayered Architecture

When there are layers on layers on layers in your application.

**Symptoms:**
- Not providing abstraction, just pass-through
- Lots of boilerplate code
- Changes require touching many layers
- Each layer just delegates to the next

**Fix:** Remove unnecessary layers. A layer should add value.

### Overabstraction

Too abstract to be understandable.

**Symptoms:**
- Concrete designs would be clearer
- Abstractions don't match real concepts
- Excessive interface hierarchies
- Hard to trace actual execution

**Fix:** Concrete implementations are easier to understand. Abstract only when you have multiple implementations.

### Overconfigurability

Everything is configurable because no decisions were made.

**Symptoms:**
- Configuration files longer than code
- Behavior impossible to predict
- Testing all configurations is impractical
- Default values everywhere

**Fix:** Make decisions. Configure only what truly varies by deployment.

### Overkill Architecture

A simple problem with a complex (however technically interesting) solution.

**Symptoms:**
- Solution more complex than the problem
- "Interesting" technologies used unnecessarily
- Simple CRUD needs microservices
- Resume-driven development

**Fix:** Match solution complexity to problem complexity.

### Futuristic Architecture

The architecture wants to anticipate a lot of future possible changes.

**Symptoms:**
- Features built "just in case"
- Excessive abstraction for future flexibility
- YAGNI violations everywhere
- Waste when predicted changes don't happen

**Fix:** Build for today's requirements. Refactor when needed.

### Technology Enthusiastic Architecture

Lots of new cool technology introduced just for the sake of it.

**Symptoms:**
- New tech for solved problems
- Team expertise spread thin
- Multiple technologies doing same thing
- Learning curve impacts delivery

**Fix:** Choose boring technology. New tech needs justification.

### Paper Tiger Architecture

The architecture exists only on paper (UML diagrams) with no connection to reality.

**Symptoms:**
- Diagrams don't match code
- Architecture docs never updated
- New developers ignore the docs
- Reality diverged long ago

**Fix:** Generate docs from code, or keep them minimal and current.

## Architecture Killers

More severe than smells - these can destroy a system.

### Split Brain

Different parts of the system claim ownership of the same data or their interpretation.

**Symptoms:**
- Inconsistent data across components
- Synchronization nightmares
- "Which is the source of truth?"
- Data conflicts and corruption

**Fix:** Establish clear data ownership. Single source of truth.

### Coupling in Space and Time

**Space coupling:** Shared code to remove duplication hinders independent advancement.

**Time coupling:**
- A service that needs other services to be up
- An `Initialize()` method that must be called before any other method
- Temporal dependencies not visible in code

**Fix:** Use constructor injection, factories, or events for time coupling. Accept some duplication for space coupling.

### Dead-end

A design decision that prevents further adaptability without a major refactoring or rewrite.

**Symptoms:**
- "We can't do X because of Y"
- Framework lock-in
- Database lock-in
- Irreversible technology choices

**Fix:** Prefer reversible decisions. Use abstractions at boundaries.

## Connector Smells

### Connector Envy

A component doing the job that should be delegated to a connector:
- **Communication** (transfer of data)
- **Coordination** (transfer of control)
- **Conversion** (bridge different formats/protocols)
- **Facilitation** (load-balancing, monitoring, fault tolerance)

### Scattered Parasitic Functionality

A single concern scattered across multiple components, with at least one component addressing multiple orthogonal concerns.

### Ambiguous Interfaces

Interfaces that offer only a single general entry point into a component. They are not explorable or self-documenting.

### Extraneous Adjacent Connector

Two connectors of different types used to link a pair of components (e.g., both event and service call).

## How to Detect Smells

- New features take increasingly longer
- Bugs in one area cause failures in unrelated areas
- Team dreads working in certain parts of codebase
- Architecture discussions are contentious
- "It's technical debt, we'll fix it later" (but never do)

## Related Concepts

- [Architecture Types](types.md) - Healthy architecture patterns
- [Clean Architecture Layers](layers.md) - Proper structure
- [Code Smells](../code-smells/taxonomy.md) - Code-level smells

## Sources

- Clean Architecture Cheatsheet V1.0 by Urs Enzler
- Toward a Catalogue of Architectural Bad Smells by Garcia et al.
