# Context Graph

Knowledge relationships between skills. Like Context7's library dependency graph.

## Skill Dependency Tree

```
                         ┌─────────────────────────────────────────┐
                         │           LAYER 4: WORKFLOWS            │
                         │      feature-development-workflow       │
                         │        claude-artifact-creator          │
                         └────────────────────┬────────────────────┘
                                              │ orchestrates
          ┌───────────────────────────────────┼───────────────────────────────────┐
          │                                   │                                   │
          ▼                                   ▼                                   ▼
┌─────────────────────┐           ┌─────────────────────┐           ┌─────────────────────┐
│   LAYER 3: TESTING  │           │  LAYER 3: SECURITY  │           │  LAYER 3: ADVANCED  │
│ xunit-testing       │           │ security-patterns   │           │ distributed-events  │
│ e2e-testing         │           │                     │           │ grpc-integration    │
│ javascript-testing  │           │                     │           │ bulk-operations     │
└──────────┬──────────┘           └──────────┬──────────┘           └──────────┬──────────┘
           │                                  │                                 │
           │ tests                            │ secures                         │ extends
           ▼                                  ▼                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              LAYER 2: FRAMEWORK                                         │
│                                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │ abp-framework-  │◄──►│ efcore-patterns │◄──►│ fluentvalidation│    │ openiddict-  │ │
│  │ patterns        │    │                 │    │ -patterns       │    │ authorization│ │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘    └──────┬───────┘ │
│           │                      │                      │                    │         │
│           │                      │                      │                    │         │
│  ┌────────┴────────┐    ┌────────┴────────┐    ┌────────┴────────┐          │         │
│  │ api-design-     │    │ linq-optim-     │    │ api-response-   │          │         │
│  │ principles      │    │ ization         │    │ patterns        │          │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘          │         │
│                                                                              │         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          │         │
│  │ technical-      │    │ domain-         │    │ requirements-   │◄─────────┘         │
│  │ design-patterns │    │ modeling        │    │ engineering     │                    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                              │
                                              │ requires
                                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              LAYER 1: FOUNDATIONS                                       │
│                                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │ csharp-advanced │    │ dotnet-async-   │    │ error-handling- │    │ mermaid-     │ │
│  │ -patterns       │    │ patterns        │    │ patterns        │    │ diagram      │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘    └──────────────┘ │
│                                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │ typescript-     │    │ modern-         │    │ git-advanced-   │    │ docker-      │ │
│  │ advanced-types  │    │ javascript      │    │ workflows       │    │ containerize │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘    └──────────────┘ │
│                                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                    │
│  │ code-review-    │◄──►│ clean-code-     │    │ debugging-      │                    │
│  │ excellence      │    │ dotnet          │    │ patterns        │                    │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## Relationship Matrix

### Layer 1: Foundations (No dependencies)

| Skill | Layer | Depends On | Complements | Extended By |
|-------|-------|------------|-------------|-------------|
| csharp-advanced-patterns | 1 | - | dotnet-async-patterns | abp-framework-patterns |
| dotnet-async-patterns | 1 | - | error-handling-patterns | abp-framework-patterns |
| error-handling-patterns | 1 | - | dotnet-async-patterns | fluentvalidation-patterns |
| mermaid-diagram-patterns | 1 | - | technical-design-patterns | - |
| typescript-advanced-types | 1 | - | modern-javascript-patterns | - |
| modern-javascript-patterns | 1 | - | typescript-advanced-types | - |
| git-advanced-workflows | 1 | - | - | - |
| docker-dotnet-containerize | 1 | - | - | - |
| code-review-excellence | 1 | - | clean-code-dotnet | - |
| clean-code-dotnet | 1 | - | code-review-excellence, csharp-advanced-patterns | - |
| debugging-patterns | 1 | - | error-handling-patterns | - |

### Layer 2: Framework (Depend on foundations)

| Skill | Layer | Depends On | Complements | Extended By |
|-------|-------|------------|-------------|-------------|
| abp-framework-patterns | 2 | csharp-advanced, dotnet-async | efcore-patterns, openiddict-auth | distributed-events |
| abp-entity-patterns | 2 | csharp-advanced | efcore-patterns, abp-service-patterns | - |
| abp-service-patterns | 2 | csharp-advanced, dotnet-async | abp-entity-patterns, fluentvalidation | - |
| abp-infrastructure-patterns | 2 | csharp-advanced | openiddict-auth, abp-entity-patterns | distributed-events |
| efcore-patterns | 2 | linq-optimization | abp-framework-patterns | bulk-operations |
| fluentvalidation-patterns | 2 | error-handling-patterns | abp-framework-patterns | - |
| openiddict-authorization | 2 | - | security-patterns, abp-framework | - |
| linq-optimization-patterns | 2 | - | efcore-patterns | - |
| api-design-principles | 2 | - | technical-design-patterns | api-response-patterns |
| api-response-patterns | 2 | api-design-principles | abp-framework-patterns | - |
| technical-design-patterns | 2 | mermaid-diagram-patterns | api-design-principles | - |
| domain-modeling | 2 | - | requirements-engineering | abp-framework-patterns |
| requirements-engineering | 2 | - | domain-modeling | - |

### Layer 3: Features (Depend on framework)

| Skill | Layer | Depends On | Complements | Extended By |
|-------|-------|------------|-------------|-------------|
| xunit-testing-patterns | 3 | abp-framework-patterns | e2e-testing-patterns, api-integration-testing | - |
| api-integration-testing | 3 | xunit-testing-patterns, abp-framework-patterns | test-data-generation | - |
| test-data-generation | 1 | - | xunit-testing-patterns, api-integration-testing | - |
| e2e-testing-patterns | 3 | - | javascript-testing-patterns | - |
| javascript-testing-patterns | 3 | modern-javascript-patterns | e2e-testing-patterns | - |
| system-design-patterns | 2 | - | technical-design-patterns, api-design-principles | - |
| security-patterns | 3 | openiddict-authorization | abp-framework-patterns | - |
| distributed-events-advanced | 3 | abp-framework-patterns | - | - |
| grpc-integration-patterns | 3 | abp-framework-patterns | - | - |
| bulk-operations-patterns | 3 | efcore-patterns | abp-framework-patterns | - |

### Layer 4: Workflows (Orchestrate other skills)

| Skill | Layer | Orchestrates |
|-------|-------|--------------|
| feature-development-workflow | 4 | All skills via agent coordination |
| claude-artifact-creator | 4 | Meta: creates other artifacts |
| knowledge-discovery | 4 | Discovery: finds relevant skills and knowledge |

## Topic to Skill Mapping

### Entity & Domain

| Topic | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| Entity creation | abp-framework-patterns | efcore-patterns | domain-modeling |
| Aggregate roots | abp-framework-patterns | domain-modeling | - |
| Value objects | abp-framework-patterns | csharp-advanced-patterns | - |
| Domain services | abp-framework-patterns | - | - |
| Business rules | domain-modeling | requirements-engineering | - |

### Data Access

| Topic | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| DbContext | efcore-patterns | abp-framework-patterns | - |
| Migrations | efcore-patterns | - | - |
| Repository | abp-framework-patterns | efcore-patterns | - |
| Query optimization | linq-optimization-patterns | efcore-patterns | - |
| Bulk insert/update | bulk-operations-patterns | efcore-patterns | - |

### Application Layer

| Topic | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| AppService | abp-framework-patterns | openiddict-authorization | - |
| DTOs | abp-framework-patterns | - | - |
| Validation | fluentvalidation-patterns | error-handling-patterns | - |
| Object mapping | abp-framework-patterns | - | - |
| Permissions | openiddict-authorization | abp-framework-patterns | security-patterns |

### API & Integration

| Topic | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| REST API design | api-design-principles | api-response-patterns | - |
| Response wrappers | api-response-patterns | api-design-principles | - |
| gRPC services | grpc-integration-patterns | - | - |
| Distributed events | distributed-events-advanced | abp-framework-patterns | - |

### Testing

| Topic | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| Unit tests | xunit-testing-patterns | - | - |
| Integration tests | xunit-testing-patterns | abp-framework-patterns | - |
| E2E tests | e2e-testing-patterns | javascript-testing-patterns | - |
| Test data seeders | xunit-testing-patterns | - | - |

### Security

| Topic | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| Authentication | openiddict-authorization | security-patterns | - |
| Authorization | openiddict-authorization | abp-framework-patterns | - |
| STRIDE modeling | security-patterns | - | - |
| OWASP compliance | security-patterns | - | - |

## Skill Loading Order

When Claude needs multiple skills, load in this order:

### For Backend Implementation
```
1. csharp-advanced-patterns     (foundation)
2. dotnet-async-patterns        (foundation)
3. abp-framework-patterns       (framework - core)
4. efcore-patterns              (framework - data)
5. fluentvalidation-patterns    (framework - validation)
6. openiddict-authorization     (framework - security)
7. xunit-testing-patterns       (feature - tests)
```

### For API Design
```
1. mermaid-diagram-patterns     (foundation - diagrams)
2. domain-modeling              (framework - domain)
3. api-design-principles        (framework - API)
4. technical-design-patterns    (framework - TSD)
5. api-response-patterns        (framework - responses)
```

### For Security Audit
```
1. openiddict-authorization     (framework - auth)
2. security-patterns            (feature - security)
3. abp-framework-patterns       (framework - context)
```

## Cross-References

- [SKILL-INDEX.md](SKILL-INDEX.md) - Quick lookup by task/keyword
- [flows/INDEX.md](flows/INDEX.md) - Multi-skill workflows
- [knowledge/INDEX.md](knowledge/INDEX.md) - Shared knowledge base
