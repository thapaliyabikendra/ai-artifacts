# Claude Sub-Agent System

> **Location**: `.claude/agents/`
> **Guidelines**: `.claude/GUIDELINES.md`
> **Project Context**: `CLAUDE.md`

---

## Directory Structure

Agents are organized **by role** following `.claude/GUIDELINES.md`:

```
agents/
├── architects/         # System designers and planners (2 agents)
├── engineers/          # Implementation specialists (3 agents)
├── reviewers/          # Code and security reviewers (3 agents)
├── specialists/        # Domain-specific experts (2 agents)
└── language-experts/   # Programming language specialists (2 agents)
```

**Total: 12 specialized agents** for the Clinic Management System (ABP + React)

---

## Architects

System designers who plan implementations and make architectural decisions.

| Agent | Purpose | Model | Skills |
|-------|---------|-------|--------|
| [`product-architect`](architects/product-architect.md) | Requirements, user stories, BRD | haiku | - |
| [`backend-architect`](architects/backend-architect.md) | API design, database schema, TSD | sonnet | abp-framework-patterns, api-design-principles, postgresql, sql-optimization-patterns |

---

## Engineers

Implementation specialists who build and integrate solutions.

| Agent | Purpose | Model | Skills |
|-------|---------|-------|--------|
| [`abp-developer`](engineers/abp-developer.md) | .NET/ABP Framework backend | sonnet | abp-framework-patterns, crud-service, dotnet-async-patterns, error-handling-patterns |
| [`react-developer`](engineers/react-developer.md) | React 18+ frontend with UI/UX | sonnet | typescript-advanced-types, modern-javascript-patterns, javascript-testing-patterns |
| [`devops-engineer`](engineers/devops-engineer.md) | CI/CD, Docker, releases | sonnet | docker-dotnet-containerize, git-advanced-workflows |

---

## Reviewers

Analysts who ensure code quality and security.

| Agent | Purpose | Model | Skills |
|-------|---------|-------|--------|
| [`code-reviewer`](reviewers/code-reviewer.md) | Code quality, PR reviews | sonnet | code-review-excellence, abp-framework-patterns, typescript-advanced-types |
| [`security-engineer`](reviewers/security-engineer.md) | Security audits, STRIDE, OWASP | sonnet | error-handling-patterns, abp-framework-patterns |
| [`qa-engineer`](reviewers/qa-engineer.md) | Test automation, xUnit, Playwright | sonnet | e2e-testing-patterns, javascript-testing-patterns |

---

## Specialists

Domain experts for specific tasks.

| Agent | Purpose | Model | Skills |
|-------|---------|-------|--------|
| [`orchestrator`](specialists/orchestrator.md) | Multi-agent workflow coordination | sonnet | - |
| [`debugger`](specialists/debugger.md) | Root cause analysis, error diagnosis | sonnet | error-handling-patterns, dotnet-async-patterns |

---

## Language Experts

Programming language specialists for complex patterns.

| Agent | Purpose | Model | Skills |
|-------|---------|-------|--------|
| [`csharp-pro`](language-experts/csharp-pro.md) | Advanced C#, .NET 10 patterns | sonnet | dotnet-async-patterns, error-handling-patterns |
| [`typescript-pro`](language-experts/typescript-pro.md) | Advanced TypeScript, generics, React types | sonnet | typescript-advanced-types, modern-javascript-patterns |

---

## Skills Reference

Skills provide specialized knowledge that agents can invoke:

| Skill | Linked Agents |
|-------|---------------|
| `abp-framework-patterns` | backend-architect, abp-developer, code-reviewer, security-engineer |
| `api-design-principles` | backend-architect |
| `crud-service` | abp-developer |
| `dotnet-async-patterns` | abp-developer, debugger, csharp-pro |
| `error-handling-patterns` | abp-developer, security-engineer, debugger, csharp-pro |
| `postgresql` | backend-architect |
| `sql-optimization-patterns` | backend-architect, abp-developer |
| `docker-dotnet-containerize` | devops-engineer |
| `git-advanced-workflows` | devops-engineer |
| `typescript-advanced-types` | react-developer, code-reviewer, typescript-pro |
| `modern-javascript-patterns` | react-developer, typescript-pro |
| `javascript-testing-patterns` | react-developer, qa-engineer |
| `e2e-testing-patterns` | qa-engineer |
| `code-review-excellence` | code-reviewer |

---

## Agent Workflow (Clinic Management System)

```
                            ┌─────────────────────┐
                            │    orchestrator     │
                            │   (specialists/)    │
                            └──────────┬──────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
        ▼                              ▼                              ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ product-architect │    │ security-engineer │    │  devops-engineer  │
│  (architects/)    │    │   (reviewers/)    │    │   (engineers/)    │
└─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
          │                        │                        │
          ▼                        │                        │
┌───────────────────┐              │                        │
│ backend-architect │◄─────────────┘                        │
│  (architects/)    │                                       │
└─────────┬─────────┘                                       │
          │                                                 │
          ├────────────────────────┬────────────────────────┤
          ▼                        ▼                        ▼
┌───────────────────┐    ┌───────────────────┐              │
│   abp-developer   │    │  react-developer  │              │
│   (engineers/)    │    │   (engineers/)    │              │
└─────────┬─────────┘    └─────────┬─────────┘              │
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   ▼
                         ┌───────────────────┐
                         │    qa-engineer    │
                         │   (reviewers/)    │
                         └───────────────────┘
```

### Workflow Patterns

**Feature Development**:
1. `product-architect` → Define requirements
2. `backend-architect` → Design API & schema
3. `abp-developer` + `react-developer` → Implement (parallel)
4. `qa-engineer` → Write and run tests
5. `code-reviewer` → Review code
6. `security-engineer` → Security review
7. `devops-engineer` → Deploy

**Bug Fix**:
1. `debugger` → Identify root cause
2. `abp-developer` or `react-developer` → Implement fix
3. `qa-engineer` → Verify fix
4. `code-reviewer` → Review

---

## How to Use

### Invoke by Category/Name
```
Use the architects/backend-architect agent to design the API
Use the engineers/abp-developer agent to implement the service
Use the reviewers/qa-engineer agent to write tests
```

### Chain Agents
```
First use architects/product-architect to define requirements,
then architects/backend-architect to create the TSD,
then engineers/abp-developer to implement
```

### Parallel Execution
```
Run engineers/abp-developer and engineers/react-developer in parallel
```

### Language Experts for Complex Patterns
```
Use language-experts/csharp-pro for advanced C# pattern implementation
Use language-experts/typescript-pro for complex TypeScript types
```

---

## Knowledge Base Files

Agents read/write to `docs/` folder:

| Document | Owner Agent | Purpose |
|----------|-------------|---------|
| `business-requirements.md` | product-architect | BRD |
| `technical-specification.md` | backend-architect | TSD |
| `backlog.md` | product-architect | User stories |
| `decisions.md` | backend-architect | ADRs |
| `ui-designs.md` | react-developer | Wireframes |
| `test-cases.md` | qa-engineer | Test plans |
| `security-audit.md` | security-engineer | Security findings |
| `releases.md` | devops-engineer | Release history |
| `dev-progress.md` | orchestrator | Activity log |

---

## Related

- Agent organization rules: `.claude/GUIDELINES.md`
- Project context: `CLAUDE.md`
- Agent creation skill: `.claude/skills/agent-creator/`
- Available skills: `.claude/skills/`
