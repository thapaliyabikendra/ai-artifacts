---
name: Clean Architecture Layers
category: clean-architecture
implementations: {}
used_by_skills: [abp-framework-patterns, backend-architect]
---

# Clean Architecture Layers

> "An architecture that allows to replace details and is easy to verify."

## The Principle

Clean Architecture organizes code into concentric layers, with dependencies pointing inward. The inner layers contain business logic, while outer layers contain implementation details.

## The Four Layers

```
┌─────────────────────────────────────────────────────────────┐
│                   Frameworks & Drivers                       │
│                    (Outermost Layer)                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Interface Adapters                      │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │              Use Cases                       │    │    │
│  │  │  ┌─────────────────────────────────────┐    │    │    │
│  │  │  │            Entities                  │    │    │    │
│  │  │  │         (Innermost Layer)            │    │    │    │
│  │  │  └─────────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 1. Entities (Enterprise Business Rules)

- Encapsulate enterprise-wide business rules
- Can be an object with methods or a set of data structures and functions
- Least likely to change when something external changes
- **Independent of everything else**

### 2. Use Cases (Application Business Rules)

- Orchestrate the flow of data to and from entities
- Direct entities to use their business rules
- Contains application-specific business rules
- **Depends only on Entities**

### 3. Interface Adapters

- Convert data from the format most convenient for use cases and entities to the format most convenient for external agencies
- Controllers, Presenters, Gateways
- **Depends on Use Cases and Entities**

### 4. Frameworks & Drivers

- Glue code connecting UI, databases, devices to inner circles
- Database, Web Framework, UI Framework
- **Depends on Interface Adapters**

## Why It Matters

### Independent of Frameworks

The architecture does not depend on the existence of some library. This allows you to use frameworks as tools, rather than cramming your system into their constraints.

### Testable

Business rules and use cases can be tested without UI, database, web server, or any other external element.

### Independent of UI

The UI can change easily without changing the rest of the system.

### Independent of Database

You can swap databases without changing business rules.

### Independent of External Agencies

Business rules don't know anything about the outside world.

## How to Detect Violations

- Business logic depends on database implementation
- Entities import framework classes
- Use cases reference UI components
- Core layers import outer layer classes
- Circular dependencies between layers

## Related Concepts

- [Dependency Rule](dependency-rule.md) - How dependencies flow
- [Architecture Types](types.md) - Simple, Flexible, Evolvable
- [Architecture Smells](smells.md) - Anti-patterns
- [Dependency Inversion](../solid/dip.md) - Enabling principle

## Mapping to ABP Framework

| Clean Architecture | ABP Framework |
|-------------------|---------------|
| Entities | Domain Layer (Entities) |
| Use Cases | Application Layer (AppServices) |
| Interface Adapters | HttpApi Layer, EntityFramework |
| Frameworks & Drivers | HttpApi.Host, DbMigrator |

## Sources

- The Clean Architecture by Robert C. Martin
- Clean Architecture Cheatsheet V1.0 by Urs Enzler
