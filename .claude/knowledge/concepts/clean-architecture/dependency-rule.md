---
name: Dependency Rule
category: clean-architecture
implementations: {}
used_by_skills: [abp-framework-patterns, backend-architect]
---

# The Dependency Rule

> "Source code dependencies can only point inwards."

## The Principle

The overriding rule that makes Clean Architecture work:

**Nothing in an inner circle can know anything at all about something in an outer circle.**

This includes:
- Classes
- Functions
- Variables
- Data formats
- Any named software entity

## Why It Matters

- **Isolation** - Business rules are protected from external changes
- **Testability** - Inner layers can be tested without outer layers
- **Flexibility** - Outer layers can be swapped without affecting inner
- **Independence** - Core logic doesn't depend on frameworks

## Direction of Dependencies

```
                Direction of Dependencies
                         │
                         │
                         ▼
┌─────────────────────────────────────────────┐
│           Frameworks & Drivers               │
│                    │                         │
│                    ▼                         │
│  ┌─────────────────────────────────────┐    │
│  │         Interface Adapters          │    │
│  │                 │                   │    │
│  │                 ▼                   │    │
│  │  ┌─────────────────────────────┐    │    │
│  │  │          Use Cases          │    │    │
│  │  │              │              │    │    │
│  │  │              ▼              │    │    │
│  │  │  ┌─────────────────────┐    │    │    │
│  │  │  │      Entities       │    │    │    │
│  │  │  └─────────────────────┘    │    │    │
│  │  └─────────────────────────────┘    │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

## Crossing Boundaries

When data crosses boundaries, it's always in the form that's most convenient for the inner circle:

### Using Dependency Inversion

Classes in an outer circle implement interfaces defined in an inner circle:

```
Inner Circle:          Outer Circle:
┌──────────────┐       ┌─────────────────┐
│  IRepository │◄──────│ SqlRepository   │
│  (interface) │       │ (implements)    │
└──────────────┘       └─────────────────┘
```

The inner circle defines what it needs. The outer circle provides it.

### Data Transfer

Data that crosses boundaries should be simple data structures:
- DTOs (Data Transfer Objects)
- Simple structs
- Function arguments

**Never pass entities across boundaries** - use DTOs.

## How to Detect Violations

- Inner layer imports outer layer namespace/module
- Entity class references database framework
- Use case references HTTP request/response types
- Domain model has UI validation attributes
- Business rule depends on specific database syntax

## Program Flow vs Dependencies

**Important distinction:**

- **Program Flow**: Can go from outside to inside and back out
  - User clicks button → Controller → Use Case → Entity → Use Case → Presenter → View

- **Dependencies**: Always point inward
  - Source code references only point toward center

## Related Concepts

- [Clean Architecture Layers](layers.md) - The layer structure
- [Dependency Inversion Principle](../solid/dip.md) - Enabling mechanism
- [Interface Adapters](layers.md) - Boundary implementations

## Sources

- The Clean Architecture by Robert C. Martin
- Clean Architecture Cheatsheet V1.0 by Urs Enzler
