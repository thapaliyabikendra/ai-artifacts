---
name: skill-index
description: "Grep-optimized skill lookup tables. Use Grep to extract rows, not full Read."
type: index
updated: 2024-12-14
total_skills: 32
---

# Skill Index

## Summary

Discovery index for skills. Use `Grep("skill-name", SKILL-INDEX.md)` to extract entries.
Like Context7's `resolve-library-id` but grep-friendly.

---
## Master Index

| Skill | L | Category | Keywords | Path |
|-------|---|----------|----------|------|
| abp-api-implementation | 2 | backend | api,rest,crud,getlist | skills/abp-api-implementation/SKILL.md |
| abp-contract-scaffolding | 2 | backend | interface,dto,permission,contracts | skills/abp-contract-scaffolding/SKILL.md |
| abp-entity-patterns | 2 | backend | entity,aggregate,repository,domain | skills/abp-entity-patterns/SKILL.md |
| abp-framework-patterns | 2 | backend | entity,appservice,dto,mapperly,permissions | skills/abp-framework-patterns/skill.md |
| abp-infrastructure-patterns | 2 | backend | permissions,jobs,events,multitenancy | skills/abp-infrastructure-patterns/SKILL.md |
| abp-service-patterns | 2 | backend | appservice,dto,mapperly,uow,filter | skills/abp-service-patterns/SKILL.md |
| actionable-review-format-standards | 1 | meta | review,format,severity,actionable | skills/actionable-review-format-standards/SKILL.md |
| api-design-principles | 2 | arch | rest,openapi,endpoints,contracts | skills/api-design-principles/SKILL.md |
| api-integration-testing | 3 | test | xunit,webapplicationfactory,http | skills/api-integration-testing/SKILL.md |
| api-response-patterns | 2 | arch | response,wrapper,error,pagination | skills/api-response-patterns/SKILL.md |
| bulk-operations-patterns | 3 | advanced | excel,import,batch,insertmany | skills/bulk-operations-patterns/SKILL.md |
| claude-artifact-creator | 4 | meta | skill,agent,command,hook,artifact | skills/claude-artifact-creator/SKILL.md |
| clean-code-dotnet | 1 | quality | solid,naming,functions,refactoring | skills/clean-code-dotnet/SKILL.md |
| code-review-excellence | 1 | quality | review,pr,feedback,standards | skills/code-review-excellence/SKILL.md |
| content-retrieval | 4 | meta | grep,read,tokens,efficient,qmd | skills/content-retrieval/SKILL.md |
| csharp-advanced-patterns | 1 | backend | records,pattern-matching,linq,span | skills/csharp-advanced-patterns/SKILL.md |
| debugging-patterns | 1 | quality | debug,error,rootcause,stacktrace | skills/debugging-patterns/SKILL.md |
| distributed-events-advanced | 3 | advanced | events,saga,idempotent,eto | skills/distributed-events-advanced/SKILL.md |
| docker-dotnet-containerize | 1 | devops | docker,container,alpine,multistage | skills/docker-dotnet-containerize/SKILL.md |
| domain-modeling | 2 | arch | entity,aggregate,rules,permissions | skills/domain-modeling/SKILL.md |
| dotnet-async-patterns | 1 | backend | async,await,valuetask,cancellation | skills/dotnet-async-patterns/SKILL.md |
| e2e-testing-patterns | 3 | test | playwright,e2e,browser,automation | skills/e2e-testing-patterns/SKILL.md |
| efcore-patterns | 2 | backend | dbcontext,migration,repository,postgresql | skills/efcore-patterns/SKILL.md |
| error-handling-patterns | 1 | backend | exception,result,polly,retry | skills/error-handling-patterns/SKILL.md |
| feature-development-workflow | 4 | meta | workflow,stages,agents,orchestration | skills/feature-development-workflow/SKILL.md |
| fluentvalidation-patterns | 2 | backend | validator,rulefor,mustasync,dto | skills/fluentvalidation-patterns/SKILL.md |
| git-advanced-workflows | 1 | devops | rebase,cherry-pick,bisect,worktree | skills/git-advanced-workflows/SKILL.md |
| grpc-integration-patterns | 3 | advanced | grpc,protobuf,streaming,client | skills/grpc-integration-patterns/SKILL.md |
| javascript-testing-patterns | 3 | test | jest,vitest,rtl,mock | skills/javascript-testing-patterns/SKILL.md |
| knowledge-discovery | 4 | meta | discover,find,skills,tiers | skills/knowledge-discovery/SKILL.md |
| linq-optimization-patterns | 2 | backend | linq,n+1,include,projection | skills/linq-optimization-patterns/SKILL.md |
| markdown-optimization | 4 | meta | markdown,compaction,size,verbose | skills/markdown-optimization/SKILL.md |
| mermaid-diagram-patterns | 1 | arch | mermaid,erd,sequence,flowchart | skills/mermaid-diagram-patterns/SKILL.md |
| modern-javascript-patterns | 1 | frontend | es6,async,destructuring,modules | skills/modern-javascript-patterns/SKILL.md |
| openiddict-authorization | 2 | security | oauth,permissions,rbac,claims | skills/openiddict-authorization/SKILL.md |
| react-code-review-patterns | 3 | frontend | react,review,hooks,accessibility | skills/react-code-review-patterns/SKILL.md |
| react-development-patterns | 2 | frontend | react,hooks,state,components | skills/react-development-patterns/SKILL.md |
| requirements-engineering | 2 | arch | userstory,acceptance,requirements | skills/requirements-engineering/SKILL.md |
| security-patterns | 3 | security | stride,owasp,audit,threats | skills/security-patterns/SKILL.md |
| system-design-patterns | 2 | arch | scalability,cap,reliability,tradeoffs | skills/system-design-patterns/SKILL.md |
| technical-design-patterns | 2 | arch | tsd,api-contract,schema,design | skills/technical-design-patterns/SKILL.md |
| test-data-generation | 1 | test | bogus,faker,builder,fixture | skills/test-data-generation/SKILL.md |
| typescript-advanced-types | 1 | frontend | generics,conditional,utility,infer | skills/typescript-advanced-types/SKILL.md |
| xunit-testing-patterns | 3 | test | xunit,shouldly,nsubstitute,fact | skills/xunit-testing-patterns/SKILL.md |
---
## Lookup by Task

| Task | Primary | Also Consider |
|------|---------|---------------|
| Build React components | react-development-patterns | typescript-advanced-types |
| Create an entity | abp-framework-patterns | efcore-patterns, domain-modeling |
| Create DTOs | abp-framework-patterns | abp-contract-scaffolding |
| Validate input DTOs | fluentvalidation-patterns | error-handling-patterns |
| Write an AppService | abp-framework-patterns | openiddict-authorization |
| Configure EF Core | efcore-patterns | linq-optimization-patterns |
| Add permissions | openiddict-authorization | security-patterns |
| Write unit tests | xunit-testing-patterns | test-data-generation |
| Write integration tests | api-integration-testing | xunit-testing-patterns |
| Write E2E tests | e2e-testing-patterns | javascript-testing-patterns |
| Generate test data | test-data-generation | xunit-testing-patterns |
| Design scalable systems | system-design-patterns | technical-design-patterns |
| Design an API | api-design-principles | technical-design-patterns |
| Implement an API | abp-api-implementation | abp-service-patterns |
| Create technical design | technical-design-patterns | api-design-principles |
| Generate API contracts | abp-contract-scaffolding | abp-framework-patterns |
| Model a domain | domain-modeling | requirements-engineering |
| Handle errors | error-handling-patterns | dotnet-async-patterns |
| Optimize queries | linq-optimization-patterns | efcore-patterns |
| Debug an issue | debugging-patterns | error-handling-patterns |
| Secure an endpoint | security-patterns | openiddict-authorization |
| Create diagrams | mermaid-diagram-patterns | technical-design-patterns |
| Containerize app | docker-dotnet-containerize | - |
| Advanced git | git-advanced-workflows | - |
| Review code | code-review-excellence | clean-code-dotnet |
| Apply clean code | clean-code-dotnet | code-review-excellence |
| Bulk operations | bulk-operations-patterns | efcore-patterns |
| Distributed events | distributed-events-advanced | abp-framework-patterns |
| gRPC services | grpc-integration-patterns | - |
| API responses | api-response-patterns | api-design-principles |
| Optimize markdown | markdown-optimization | - |
| Token-efficient retrieval | content-retrieval | knowledge-discovery |
---
## Lookup by Keyword

| Keyword | Skills |
|---------|--------|
| AppService | abp-framework-patterns, abp-service-patterns, abp-api-implementation |
| async | dotnet-async-patterns, csharp-advanced-patterns |
| authorize | openiddict-authorization, security-patterns |
| DbContext | efcore-patterns, abp-framework-patterns |
| DTO | abp-framework-patterns, abp-service-patterns, abp-contract-scaffolding |
| Entity | abp-framework-patterns, abp-entity-patterns, efcore-patterns, domain-modeling |
| FluentValidation | fluentvalidation-patterns |
| grep | content-retrieval |
| gRPC | grpc-integration-patterns |
| Mapperly | abp-framework-patterns, abp-service-patterns |
| Migration | efcore-patterns |
| N+1 | linq-optimization-patterns, debugging-patterns |
| OWASP | security-patterns |
| PagedResultDto | abp-api-implementation, abp-service-patterns |
| Permission | openiddict-authorization, abp-infrastructure-patterns |
| Playwright | e2e-testing-patterns |
| Polly | error-handling-patterns |
| React | react-development-patterns, react-code-review-patterns |
| Repository | abp-framework-patterns, abp-entity-patterns, efcore-patterns |
| Result<T> | error-handling-patterns |
| SOLID | clean-code-dotnet |
| STRIDE | security-patterns |
| tokens | content-retrieval, markdown-optimization |
| WhereIf | abp-api-implementation, abp-service-patterns, linq-optimization-patterns |
| xUnit | xunit-testing-patterns, api-integration-testing |
---
## Lookup by Error

| Error Pattern | Skill | Section |
|---------------|-------|---------|
| Authorization failed | openiddict-authorization | Permission Checks |
| Cannot access disposed object | dotnet-async-patterns | Lifetime |
| DbUpdateConcurrencyException | efcore-patterns | Concurrency |
| DbUpdateException | efcore-patterns | Error Handling |
| Deadlock detected | dotnet-async-patterns | Deadlock Prevention |
| Entity type requires primary key | efcore-patterns | Entity Config |
| N+1 query detected | linq-optimization-patterns | N+1 Prevention |
| Object reference not set | debugging-patterns | Null Reference |
| Task was canceled | dotnet-async-patterns | Cancellation |
| Validation failed | fluentvalidation-patterns | Common Validators |
| 401 Unauthorized | openiddict-authorization | Authentication |
| 403 Forbidden | openiddict-authorization | Authorization |
---
## Lookup by Agent

| Agent | Skills |
|-------|--------|
| abp-code-reviewer | abp-framework-patterns, efcore-patterns, fluentvalidation-patterns, clean-code-dotnet |
| abp-developer | abp-framework-patterns, abp-entity-patterns, abp-service-patterns, abp-infrastructure-patterns, efcore-patterns, fluentvalidation-patterns, openiddict-authorization, linq-optimization-patterns, dotnet-async-patterns, error-handling-patterns, csharp-advanced-patterns |
| backend-architect | api-design-principles, technical-design-patterns, efcore-patterns, domain-modeling, mermaid-diagram-patterns |
| business-analyst | domain-modeling, requirements-engineering |
| database-migrator | efcore-patterns, abp-framework-patterns |
| debugger | debugging-patterns, error-handling-patterns |
| devops-engineer | docker-dotnet-containerize, git-advanced-workflows |
| qa-engineer | xunit-testing-patterns, api-integration-testing, e2e-testing-patterns, test-data-generation |
| react-code-reviewer | react-development-patterns, react-code-review-patterns, typescript-advanced-types |
| react-developer | react-development-patterns, typescript-advanced-types, modern-javascript-patterns |
| security-engineer | security-patterns, openiddict-authorization |
---
## Lookup by Category

### backend
| Skill | L | Purpose |
|-------|---|---------|
| abp-api-implementation | 2 | REST API implementation (C#/ABP) |
| abp-contract-scaffolding | 2 | Interface, DTO, permission generation |
| abp-entity-patterns | 2 | Entity, aggregate, repository, domain service |
| abp-framework-patterns | 2 | Entity, AppService, Repository, Mapperly |
| abp-infrastructure-patterns | 2 | Permissions, jobs, events, multi-tenancy |
| abp-service-patterns | 2 | AppService, DTOs, Mapperly, UoW |
| csharp-advanced-patterns | 1 | Records, pattern matching, LINQ |
| dotnet-async-patterns | 1 | Async/await, ValueTask, cancellation |
| efcore-patterns | 2 | DbContext, migrations, PostgreSQL |
| error-handling-patterns | 1 | Exceptions, Result types, Polly |
| fluentvalidation-patterns | 2 | DTO validators, async validation |
| linq-optimization-patterns | 2 | Query optimization, N+1 prevention |

### arch
| Skill | L | Purpose |
|-------|---|---------|
| api-design-principles | 2 | REST API design (theory) |
| api-response-patterns | 2 | Response wrappers, error formats |
| domain-modeling | 2 | Entity definitions, business rules |
| mermaid-diagram-patterns | 1 | ERD, sequence, flowchart |
| requirements-engineering | 2 | User stories, acceptance criteria |
| system-design-patterns | 2 | Scalability, reliability |
| technical-design-patterns | 2 | TSD templates, API contracts |

### test
| Skill | L | Purpose |
|-------|---|---------|
| api-integration-testing | 3 | xUnit + WebApplicationFactory |
| e2e-testing-patterns | 3 | Playwright automation |
| javascript-testing-patterns | 3 | Jest, React Testing Library |
| test-data-generation | 1 | Bogus, builders, fixtures |
| xunit-testing-patterns | 3 | Unit/integration tests |

### frontend
| Skill | L | Purpose |
|-------|---|---------|
| modern-javascript-patterns | 1 | ES6+, async patterns |
| react-code-review-patterns | 3 | React review checklist |
| react-development-patterns | 2 | React 18+, hooks, state |
| typescript-advanced-types | 1 | Generics, conditional types |

### security
| Skill | L | Purpose |
|-------|---|---------|
| openiddict-authorization | 2 | OAuth, permissions, RBAC |
| security-patterns | 3 | STRIDE, OWASP, audits |

### advanced
| Skill | L | Purpose |
|-------|---|---------|
| bulk-operations-patterns | 3 | Excel import, batch processing |
| distributed-events-advanced | 3 | Events, sagas, idempotency |
| grpc-integration-patterns | 3 | gRPC services, Protobuf |

### devops
| Skill | L | Purpose |
|-------|---|---------|
| docker-dotnet-containerize | 1 | Dockerfiles for .NET |
| git-advanced-workflows | 1 | Rebase, cherry-pick, bisect |

### quality
| Skill | L | Purpose |
|-------|---|---------|
| clean-code-dotnet | 1 | SOLID, naming, code smells |
| code-review-excellence | 1 | PR review practices |
| debugging-patterns | 1 | Root cause analysis |

### meta
| Skill | L | Purpose |
|-------|---|---------|
| actionable-review-format-standards | 1 | Review output format |
| claude-artifact-creator | 4 | Create skills, agents, commands |
| content-retrieval | 4 | Token-efficient retrieval protocol |
| feature-development-workflow | 4 | End-to-end orchestration |
| knowledge-discovery | 4 | Find relevant skills |
| markdown-optimization | 4 | Optimize markdown docs |
---
## Skill Bundles

Pre-defined skill groups for agents.

| Bundle | Skills |
|--------|--------|
| backend-core | abp-framework-patterns, abp-entity-patterns, abp-service-patterns, abp-infrastructure-patterns, efcore-patterns, fluentvalidation-patterns, linq-optimization-patterns, dotnet-async-patterns, csharp-advanced-patterns, error-handling-patterns |
| frontend-core | react-development-patterns, typescript-advanced-types, modern-javascript-patterns |
| testing-full | xunit-testing-patterns, api-integration-testing, test-data-generation, javascript-testing-patterns, e2e-testing-patterns |
| api-design | api-design-principles, api-response-patterns, technical-design-patterns, abp-contract-scaffolding, mermaid-diagram-patterns |
| api-implementation | abp-api-implementation, abp-service-patterns, fluentvalidation-patterns, api-response-patterns |
| security-audit | security-patterns, openiddict-authorization, abp-infrastructure-patterns |
| requirements-analysis | domain-modeling, requirements-engineering, technical-design-patterns |
---
## Related

- [AGENT-INDEX.md](AGENT-INDEX.md) - Agent lookup tables
- [CONTEXT-GRAPH.md](CONTEXT-GRAPH.md) - Skill relationships
- [content-retrieval](skills/content-retrieval/SKILL.md) - Retrieval protocol
