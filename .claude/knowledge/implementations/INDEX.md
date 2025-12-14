# Implementation Index

Language and framework-specific implementations of concepts. **CODE EXAMPLES** here.

## Quick Lookup by Language

### .NET/C#

| Implementation | Concepts | Status |
|----------------|----------|--------|
| [dotnet/clean-code.md](dotnet/clean-code.md) | clean-code/* | ✅ |
| [dotnet/solid.md](dotnet/solid.md) | solid/* | ✅ |
| [dotnet/code-smells.md](dotnet/code-smells.md) | code-smells/* | ✅ |
| [dotnet/xunit-tdd.md](dotnet/xunit-tdd.md) | testing/* | ✅ |
| [dotnet/async-patterns.md](dotnet/async-patterns.md) | - | ✅ |
| [dotnet/error-handling.md](dotnet/error-handling.md) | - | ✅ |

### React/TypeScript

| Implementation | Concepts | Status |
|----------------|----------|--------|
| [react/clean-code.md](react/clean-code.md) | clean-code/* | ✅ |
| [react/code-smells.md](react/code-smells.md) | code-smells/* | ✅ |
| [react/jest-tdd.md](react/jest-tdd.md) | testing/* | ✅ |
| [react/hooks-patterns.md](react/hooks-patterns.md) | - | ✅ |

### Python (Future)

| Implementation | Concepts | Status |
|----------------|----------|--------|
| python/clean-code.md | clean-code/* | ⏳ Planned |
| python/solid.md | solid/* | ⏳ Planned |

## Implementation by Concept

| Concept | .NET | React | Python |
|---------|------|-------|--------|
| Clean Code Principles | [✓](dotnet/clean-code.md) | [✓](react/clean-code.md) | - |
| SOLID | [✓](dotnet/solid.md) | - | - |
| Code Smells | [✓](dotnet/code-smells.md) | [✓](react/code-smells.md) | - |
| TDD | [✓](dotnet/xunit-tdd.md) | [✓](react/jest-tdd.md) | - |

## Directory Structure

```
implementations/
├── INDEX.md          # This file
├── dotnet/           # C#/.NET implementations
│   ├── clean-code.md
│   ├── solid.md
│   ├── code-smells.md
│   ├── xunit-tdd.md
│   ├── async-patterns.md
│   └── error-handling.md
├── react/            # React/TypeScript implementations
│   ├── clean-code.md
│   ├── code-smells.md
│   ├── jest-tdd.md
│   └── hooks-patterns.md
└── python/           # Python implementations (future)
    └── .gitkeep
```

## Adding New Implementations

1. **Verify concept exists** in `concepts/{topic}/`
2. Create file in `implementations/{lang}/`
3. Use implementation template from [claude-artifact-creator](../../skills/claude-artifact-creator/SKILL.md#creating-implementations)
4. **Link back to concept** in front matter
5. Add to this INDEX.md
6. **Update concept** to link to this implementation

## Template

```yaml
---
implements_concepts:
  - concepts/solid/srp
  - concepts/solid/ocp
language: csharp
framework: [dotnet, abp]
---

# {Concept} in {Language}

## SRP {#srp}

> **Concept**: [Single Responsibility](../../concepts/solid/srp.md)

### ❌ Violation
```csharp
// Bad code
```

### ✅ Correct
```csharp
// Good code
```
```

## Cross-References

- [Concepts INDEX](../concepts/INDEX.md) - Framework-independent principles
- [SKILL-INDEX](../../SKILL-INDEX.md) - Skills that use these implementations
- [GUIDELINES](../../GUIDELINES.md#three-layer-knowledge-architecture) - Architecture rules
