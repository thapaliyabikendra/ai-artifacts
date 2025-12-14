# Concept Index

Framework-independent design principles and patterns. **NO CODE** - just principles.

## Quick Lookup by Topic

| Concept | Definition | .NET | React | Python |
|---------|------------|------|-------|--------|
| **Clean Code** |||||
| Clean Code Principles | [clean-code/principles.md](clean-code/principles.md) | [✓](../implementations/dotnet/clean-code.md) | [✓](../implementations/react/clean-code.md) | - |
| Naming | [clean-code/naming.md](clean-code/naming.md) | [✓](../implementations/dotnet/clean-code.md#naming) | [✓](../implementations/react/clean-code.md#naming) | - |
| Functions | [clean-code/functions.md](clean-code/functions.md) | [✓](../implementations/dotnet/clean-code.md#functions) | - | - |
| Comments | [clean-code/comments.md](clean-code/comments.md) | [✓](../implementations/dotnet/clean-code.md#comments) | - | - |
| **SOLID** |||||
| SOLID Overview | [solid/overview.md](solid/overview.md) | [✓](../implementations/dotnet/solid.md) | - | - |
| Single Responsibility | [solid/srp.md](solid/srp.md) | [✓](../implementations/dotnet/solid.md#srp) | - | - |
| Open/Closed | [solid/ocp.md](solid/ocp.md) | [✓](../implementations/dotnet/solid.md#ocp) | - | - |
| Liskov Substitution | [solid/lsp.md](solid/lsp.md) | [✓](../implementations/dotnet/solid.md#lsp) | - | - |
| Interface Segregation | [solid/isp.md](solid/isp.md) | [✓](../implementations/dotnet/solid.md#isp) | - | - |
| Dependency Inversion | [solid/dip.md](solid/dip.md) | [✓](../implementations/dotnet/solid.md#dip) | - | - |
| **Clean Architecture** |||||
| Architecture Layers | [clean-architecture/layers.md](clean-architecture/layers.md) | - | - | - |
| Dependency Rule | [clean-architecture/dependency-rule.md](clean-architecture/dependency-rule.md) | - | - | - |
| Architecture Types | [clean-architecture/types.md](clean-architecture/types.md) | - | - | - |
| Architecture Smells | [clean-architecture/smells.md](clean-architecture/smells.md) | - | - | - |
| **Code Smells** |||||
| Smell Taxonomy | [code-smells/taxonomy.md](code-smells/taxonomy.md) | [✓](../implementations/dotnet/code-smells.md) | [✓](../implementations/react/code-smells.md) | - |
| Change Resistance | [code-smells/change-resistance.md](code-smells/change-resistance.md) | - | - | - |
| Coupling Smells | [code-smells/coupling.md](code-smells/coupling.md) | - | - | - |
| **Testing** |||||
| TDD Principles | [testing/tdd-principles.md](testing/tdd-principles.md) | [✓](../implementations/dotnet/xunit-tdd.md) | [✓](../implementations/react/jest-tdd.md) | - |
| FIRST Principles | [testing/first.md](testing/first.md) | - | - | - |
| Test Smells | [testing/test-smells.md](testing/test-smells.md) | - | - | - |
| Test Pyramid | [testing/test-pyramid.md](testing/test-pyramid.md) | - | - | - |
| **Package Design** |||||
| Package Cohesion | [package-design/cohesion.md](package-design/cohesion.md) | - | - | - |
| Package Coupling | [package-design/coupling.md](package-design/coupling.md) | - | - | - |
| **Refactoring** |||||
| Refactoring Patterns | [refactoring/patterns.md](refactoring/patterns.md) | - | - | - |
| Legacy Transformation | [refactoring/legacy-transformation.md](refactoring/legacy-transformation.md) | - | - | - |

## Concept Categories

### Clean Code
Principles for writing readable, maintainable code.

| Concept | Description |
|---------|-------------|
| [principles.md](clean-code/principles.md) | Why clean code matters, cost of change |
| [naming.md](clean-code/naming.md) | Meaningful, pronounceable names |
| [functions.md](clean-code/functions.md) | Single purpose, few arguments |
| [comments.md](clean-code/comments.md) | When to comment, when not to |

### SOLID
Object-oriented design principles.

| Concept | Description |
|---------|-------------|
| [overview.md](solid/overview.md) | SOLID as a whole |
| [srp.md](solid/srp.md) | One reason to change |
| [ocp.md](solid/ocp.md) | Open for extension, closed for modification |
| [lsp.md](solid/lsp.md) | Substitutability of subtypes |
| [isp.md](solid/isp.md) | Client-specific interfaces |
| [dip.md](solid/dip.md) | Depend on abstractions |

### Clean Architecture
Architectural principles for flexible, testable systems.

| Concept | Description |
|---------|-------------|
| [layers.md](clean-architecture/layers.md) | Entities, Use Cases, Interface Adapters, Frameworks |
| [dependency-rule.md](clean-architecture/dependency-rule.md) | Dependencies point inward |
| [types.md](clean-architecture/types.md) | Simple, Flexible, Evolvable, Agile architectures |
| [smells.md](clean-architecture/smells.md) | Overlayered, Overabstraction, Overkill |

### Code Smells
Indicators of design problems.

| Concept | Description |
|---------|-------------|
| [taxonomy.md](code-smells/taxonomy.md) | Full smell classification |
| [change-resistance.md](code-smells/change-resistance.md) | Rigidity, Fragility, Immobility |
| [coupling.md](code-smells/coupling.md) | Feature Envy, Law of Demeter |

### Testing
Test-driven development and quality.

| Concept | Description |
|---------|-------------|
| [tdd-principles.md](testing/tdd-principles.md) | Red-Green-Refactor cycle |
| [first.md](testing/first.md) | Fast, Isolated, Repeatable, Self-validating, Timely |
| [test-smells.md](testing/test-smells.md) | Test anti-patterns |
| [test-pyramid.md](testing/test-pyramid.md) | Unit → Integration → E2E |

### Package Design
Module and package organization.

| Concept | Description |
|---------|-------------|
| [cohesion.md](package-design/cohesion.md) | RREP, CCP, CRP |
| [coupling.md](package-design/coupling.md) | ADP, SDP, SAP |

### Refactoring
Code improvement patterns.

| Concept | Description |
|---------|-------------|
| [patterns.md](refactoring/patterns.md) | Reconcile, Isolate, Migrate |
| [legacy-transformation.md](refactoring/legacy-transformation.md) | 8-step legacy to clean process |

## Adding New Concepts

1. Create file in appropriate `concepts/{topic}/` directory
2. Use concept template from [claude-artifact-creator](../../skills/claude-artifact-creator/SKILL.md#creating-concepts)
3. Add to this INDEX.md
4. Create corresponding implementation(s) if applicable

## Cross-References

- [Implementations INDEX](../implementations/INDEX.md) - Language-specific code
- [SKILL-INDEX](../../SKILL-INDEX.md) - Skills that use these concepts
- [GUIDELINES](../../GUIDELINES.md#three-layer-knowledge-architecture) - Architecture rules
