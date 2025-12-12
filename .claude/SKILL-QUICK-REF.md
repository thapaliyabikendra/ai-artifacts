# Skill Quick Reference

Compact lookup for STANDARD tier discovery. ~50 lines vs ~160 lines in SKILL-INDEX.md.

## By Task

| Task | Primary Skill | Secondary |
|------|---------------|-----------|
| Entity/DTO/AppService | `abp-framework-patterns` | `efcore-patterns` |
| DbContext/Migration | `efcore-patterns` | - |
| Validation | `fluentvalidation-patterns` | - |
| Permissions | `openiddict-authorization` | `security-patterns` |
| Unit tests | `xunit-testing-patterns` | - |
| E2E tests | `e2e-testing-patterns` | `javascript-testing-patterns` |
| API design | `api-design-principles` | `technical-design-patterns` |
| Technical spec | `technical-design-patterns` | `domain-modeling` |
| Query optimization | `linq-optimization-patterns` | `efcore-patterns` |
| Error handling | `error-handling-patterns` | `dotnet-async-patterns` |
| Debugging | `debugging-patterns` | - |
| Security audit | `security-patterns` | `openiddict-authorization` |
| Docker | `docker-dotnet-containerize` | - |
| Git operations | `git-advanced-workflows` | - |
| Distributed events | `distributed-events-advanced` | `abp-framework-patterns` |
| gRPC | `grpc-integration-patterns` | - |
| Bulk operations | `bulk-operations-patterns` | `efcore-patterns` |

## By Error

| Error | Skill |
|-------|-------|
| N+1 query | `linq-optimization-patterns` |
| Authorization failed | `openiddict-authorization` |
| Validation failed | `fluentvalidation-patterns` |
| DbUpdateException | `efcore-patterns` |
| DbUpdateConcurrencyException | `efcore-patterns` |
| Task was canceled | `dotnet-async-patterns` |
| Deadlock | `dotnet-async-patterns` |
| 401/403 | `openiddict-authorization` |

## Skill Dependencies (Load Order)

```
Layer 1 → Layer 2 → Layer 3 → Layer 4
csharp   → abp      → xunit   → feature-workflow
dotnet   → efcore   → security
         → fluent
         → openiddict
```

## For DEEP Tier

Read full files: `SKILL-INDEX.md`, `CONTEXT-GRAPH.md`, `knowledge/`, `flows/`
