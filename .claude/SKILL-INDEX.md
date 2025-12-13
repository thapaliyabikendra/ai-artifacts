# Skill Index

Discovery index for finding the right skill. Like Context7's `resolve-library-id`.

## Quick Lookup by Task

| I need to... | Primary Skill | Also Consider |
|--------------|---------------|---------------|
| Build React components | `react-development-patterns` | `typescript-advanced-types` |
| Create an entity | `abp-framework-patterns` | `efcore-patterns`, `domain-modeling` |
| Create DTOs | `abp-framework-patterns` | - |
| Validate input DTOs | `fluentvalidation-patterns` | `error-handling-patterns` |
| Write an AppService | `abp-framework-patterns` | `openiddict-authorization` |
| Configure EF Core | `efcore-patterns` | `linq-optimization-patterns` |
| Add permissions | `openiddict-authorization` | `security-patterns` |
| Write unit tests | `xunit-testing-patterns` | - |
| Write integration tests | `api-integration-testing` | `xunit-testing-patterns` |
| Write E2E tests | `e2e-testing-patterns` | `javascript-testing-patterns` |
| Generate test data | `test-data-generation` | `xunit-testing-patterns` |
| Design scalable systems | `system-design-patterns` | `technical-design-patterns` |
| Design an API | `api-design-principles` | `technical-design-patterns` |
| Implement an API | `abp-api-implementation` | `abp-service-patterns`, `api-response-patterns` |
| Create technical design | `technical-design-patterns` | `api-design-principles` |
| Generate API contracts | `abp-contract-scaffolding` | `abp-framework-patterns` |
| Model a domain | `domain-modeling` | `requirements-engineering` |
| Handle errors | `error-handling-patterns` | `dotnet-async-patterns` |
| Optimize queries | `linq-optimization-patterns` | `efcore-patterns` |
| Debug an issue | `debugging-patterns` | - |
| Secure an endpoint | `security-patterns` | `openiddict-authorization` |
| Create diagrams | `mermaid-diagram-patterns` | `technical-design-patterns` |
| Containerize app | `docker-dotnet-containerize` | - |
| Advanced git | `git-advanced-workflows` | - |
| Review code | `code-review-excellence` | `clean-code-dotnet` |
| Apply clean code | `clean-code-dotnet` | `code-review-excellence` |
| Bulk operations | `bulk-operations-patterns` | `efcore-patterns` |
| Distributed events | `distributed-events-advanced` | `abp-framework-patterns` |
| gRPC services | `grpc-integration-patterns` | - |
| API responses | `api-response-patterns` | `api-design-principles` |

## Quick Lookup by Keyword

| Keyword | Primary Skill | Related |
|---------|---------------|---------|
| `React` | react-development-patterns | typescript-advanced-types |
| `useQuery` | react-development-patterns | - |
| `useState` | react-development-patterns | - |
| `Component` | react-development-patterns | - |
| `Entity` | abp-framework-patterns | efcore-patterns |
| `AppService` | abp-framework-patterns | - |
| `IAppService` | abp-contract-scaffolding | abp-framework-patterns |
| `DTO` | abp-framework-patterns | fluentvalidation-patterns |
| `CreateDto` | abp-contract-scaffolding | abp-framework-patterns |
| `UpdateDto` | abp-contract-scaffolding | abp-framework-patterns |
| `GetListInput` | abp-contract-scaffolding | abp-service-patterns |
| `Mapperly` | abp-framework-patterns | - |
| `DbContext` | efcore-patterns | linq-optimization-patterns |
| `Migration` | efcore-patterns | - |
| `Include` | linq-optimization-patterns | efcore-patterns |
| `N+1` | linq-optimization-patterns | debugging-patterns |
| `FluentValidation` | fluentvalidation-patterns | - |
| `[Authorize]` | openiddict-authorization | security-patterns |
| `Permission` | openiddict-authorization | abp-framework-patterns |
| `async/await` | dotnet-async-patterns | error-handling-patterns |
| `ValueTask` | dotnet-async-patterns | - |
| `CancellationToken` | dotnet-async-patterns | - |
| `xUnit` | xunit-testing-patterns | - |
| `Shouldly` | xunit-testing-patterns | - |
| `NSubstitute` | xunit-testing-patterns | - |
| `WebApplicationFactory` | api-integration-testing | xunit-testing-patterns |
| `HttpClient` | api-integration-testing | - |
| `Bogus` | test-data-generation | xunit-testing-patterns |
| `Faker` | test-data-generation | - |
| `TestBuilder` | test-data-generation | - |
| `Playwright` | e2e-testing-patterns | - |
| `CAP theorem` | system-design-patterns | - |
| `Scalability` | system-design-patterns | - |
| `Circuit Breaker` | system-design-patterns | error-handling-patterns |
| `STRIDE` | security-patterns | - |
| `OWASP` | security-patterns | - |
| `Polly` | error-handling-patterns | dotnet-async-patterns |
| `SOLID` | clean-code-dotnet | code-review-excellence |
| `SRP` | clean-code-dotnet | abp-framework-patterns |
| `clean code` | clean-code-dotnet | code-review-excellence |
| `code smells` | clean-code-dotnet | debugging-patterns |
| `refactoring` | clean-code-dotnet | csharp-advanced-patterns |
| `Result<T>` | error-handling-patterns | - |
| `OpenAPI` | api-design-principles | api-response-patterns |
| `REST` | api-design-principles | abp-api-implementation |
| `WhereIf` | abp-api-implementation | linq-optimization-patterns |
| `PagedResultDto` | abp-api-implementation | abp-service-patterns |
| `GetListAsync` | abp-api-implementation | - |
| `Docker` | docker-dotnet-containerize | - |
| `rebase` | git-advanced-workflows | - |
| `cherry-pick` | git-advanced-workflows | - |
| `Excel` | bulk-operations-patterns | - |
| `InsertManyAsync` | bulk-operations-patterns | efcore-patterns |
| `DistributedEvent` | distributed-events-advanced | abp-framework-patterns |
| `Saga` | distributed-events-advanced | - |
| `gRPC` | grpc-integration-patterns | - |
| `Protobuf` | grpc-integration-patterns | - |

## Quick Lookup by Error Message

| Error Pattern | Likely Skill | Section |
|---------------|--------------|---------|
| "N+1 query detected" | linq-optimization-patterns | N+1 Prevention |
| "Authorization failed" | openiddict-authorization | Permission Checks |
| "Validation failed for" | fluentvalidation-patterns | Common Validators |
| "DbUpdateException" | efcore-patterns | Error Handling |
| "DbUpdateConcurrencyException" | efcore-patterns | Concurrency |
| "Task was canceled" | dotnet-async-patterns | Cancellation |
| "Deadlock detected" | dotnet-async-patterns | Deadlock Prevention |
| "Object reference not set" | debugging-patterns | Null Reference |
| "Cannot access disposed object" | dotnet-async-patterns | Lifetime |
| "401 Unauthorized" | openiddict-authorization | Authentication |
| "403 Forbidden" | openiddict-authorization | Authorization |
| "The entity type requires a primary key" | efcore-patterns | Entity Config |

## Skill Categories

### Backend Development
| Skill | Purpose |
|-------|---------|
| `abp-framework-patterns` | Entity, AppService, Repository, Mapperly, Permissions |
| `abp-contract-scaffolding` | Interface, DTO, permission constant generation |
| `efcore-patterns` | DbContext, migrations, relationships, PostgreSQL |
| `fluentvalidation-patterns` | DTO validators, async validation |
| `openiddict-authorization` | Permissions, RBAC, claims |
| `linq-optimization-patterns` | Query optimization, N+1 prevention |
| `dotnet-async-patterns` | Async/await, ValueTask, cancellation |
| `csharp-advanced-patterns` | Records, pattern matching, LINQ |
| `error-handling-patterns` | Exceptions, Result types, Polly |

### Architecture & Design
| Skill | Purpose |
|-------|---------|
| `api-design-principles` | REST API design (theory, contracts) |
| `abp-api-implementation` | REST API implementation (C#/ABP code) |
| `api-response-patterns` | Response wrappers, error formats |
| `technical-design-patterns` | TSD templates, API contracts |
| `domain-modeling` | Entity definitions, business rules |
| `requirements-engineering` | User stories, acceptance criteria |
| `mermaid-diagram-patterns` | ERD, sequence, flowchart diagrams |

### Testing
| Skill | Purpose |
|-------|---------|
| `xunit-testing-patterns` | Unit/integration tests, seeders |
| `api-integration-testing` | xUnit + WebApplicationFactory |
| `test-data-generation` | Bogus, builders, fixtures |
| `e2e-testing-patterns` | Playwright automation |
| `javascript-testing-patterns` | Jest, React Testing Library |

### Architecture & System Design
| Skill | Purpose |
|-------|---------|
| `system-design-patterns` | Scalability, reliability, trade-offs |

### Security
| Skill | Purpose |
|-------|---------|
| `security-patterns` | STRIDE, OWASP, audits |
| `openiddict-authorization` | Auth implementation |

### Advanced Patterns
| Skill | Purpose |
|-------|---------|
| `distributed-events-advanced` | Event handlers, sagas, idempotency |
| `grpc-integration-patterns` | gRPC services, Protobuf |
| `bulk-operations-patterns` | Excel import, batch processing |

### DevOps & Tooling
| Skill | Purpose |
|-------|---------|
| `docker-dotnet-containerize` | Dockerfiles for .NET |
| `git-advanced-workflows` | Rebasing, cherry-picking |
| `code-review-excellence` | PR review practices |
| `clean-code-dotnet` | SOLID, naming, code smells |
| `debugging-patterns` | Root cause analysis |

### Frontend
| Skill | Purpose |
|-------|---------|
| `react-development-patterns` | React 18+, components, hooks, state |
| `typescript-advanced-types` | Generics, conditional types |
| `modern-javascript-patterns` | ES6+, async patterns |

### Meta
| Skill | Purpose |
|-------|---------|
| `claude-artifact-creator` | Create skills, agents, commands |
| `feature-development-workflow` | End-to-end feature orchestration |
| `knowledge-discovery` | Find relevant skills and knowledge for tasks |

## Skill Bundles

Pre-defined skill groups for common agent roles. Use bundle name in agent `skills:` field for documentation purposes.

### backend-core
Backend development essentials for .NET/ABP applications.

| Skill | Purpose |
|-------|---------|
| `abp-framework-patterns` | Entity, AppService, Repository patterns |
| `abp-entity-patterns` | Domain layer - entities, repositories, domain services |
| `abp-service-patterns` | Application layer - DTOs, Mapperly, UoW |
| `abp-infrastructure-patterns` | Permissions, background jobs, events |
| `efcore-patterns` | DbContext, migrations, relationships |
| `fluentvalidation-patterns` | Input validation |
| `linq-optimization-patterns` | Query optimization |
| `dotnet-async-patterns` | Async/await patterns |
| `csharp-advanced-patterns` | Modern C# features |
| `error-handling-patterns` | Exception handling, Polly |
| `clean-code-dotnet` | SOLID, naming, code smells |

**Used by**: `abp-developer`, `backend-architect`, `abp-code-reviewer`

### frontend-core
Frontend development for React/TypeScript applications.

| Skill | Purpose |
|-------|---------|
| `react-development-patterns` | React 18+ components, hooks, state |
| `typescript-advanced-types` | Type system, generics |
| `modern-javascript-patterns` | ES6+, functional patterns |

**Used by**: `react-developer`

### testing-full
Complete testing coverage for full-stack applications.

| Skill | Purpose |
|-------|---------|
| `xunit-testing-patterns` | .NET unit/integration tests |
| `api-integration-testing` | xUnit + WebApplicationFactory API tests |
| `test-data-generation` | Bogus, builders, fixtures |
| `javascript-testing-patterns` | Jest/Vitest frontend tests |
| `e2e-testing-patterns` | Playwright E2E tests |

**Used by**: `qa-engineer`

### api-design
API design and documentation (for architects).

| Skill | Purpose |
|-------|---------|
| `api-design-principles` | REST API design (theory, contracts) |
| `api-response-patterns` | Response wrappers |
| `technical-design-patterns` | API contracts, TSD |
| `abp-contract-scaffolding` | Interface + DTO scaffolding |
| `mermaid-diagram-patterns` | API diagrams |

**Used by**: `backend-architect`

### api-implementation
API implementation for ABP developers.

| Skill | Purpose |
|-------|---------|
| `abp-api-implementation` | REST API implementation (C#/ABP) |
| `abp-service-patterns` | AppService patterns |
| `fluentvalidation-patterns` | Input validation |
| `api-response-patterns` | Response wrappers |

**Used by**: `abp-developer`

### security-audit
Security analysis and hardening.

| Skill | Purpose |
|-------|---------|
| `security-patterns` | STRIDE, OWASP, audits |
| `openiddict-authorization` | Auth implementation |
| `abp-infrastructure-patterns` | Permission patterns |

**Used by**: `security-engineer`

### requirements-analysis
Business analysis and requirements.

| Skill | Purpose |
|-------|---------|
| `domain-modeling` | Entity definitions, business rules |
| `requirements-engineering` | User stories, acceptance criteria |
| `technical-design-patterns` | Technical specifications |

**Used by**: `business-analyst`

## Cross-References

See also:
- [CONTEXT-GRAPH.md](CONTEXT-GRAPH.md) - Skill relationships and dependencies
- [flows/INDEX.md](flows/INDEX.md) - Multi-skill workflows
- [knowledge/INDEX.md](knowledge/INDEX.md) - Shared knowledge base
