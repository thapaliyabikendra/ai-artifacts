# Agent Quick Reference

Compact lookup for agent selection. Use directly without reading agent files.

## By Task

| Task | Agent | Model | Skills Auto-Loaded |
|------|-------|-------|-------------------|
| Analyze requirements | `business-analyst` | sonnet | domain-modeling, requirements-engineering |
| Design API/schema | `backend-architect` | sonnet | technical-design-patterns, api-design-principles, efcore-patterns |
| Implement .NET/ABP | `abp-developer` | sonnet | abp-framework-patterns, efcore-patterns, fluentvalidation-patterns |
| Implement React | `react-developer` | sonnet | react-development-patterns, typescript-advanced-types |
| Review backend code | `abp-code-reviewer` | sonnet | abp-framework-patterns, efcore-patterns, fluentvalidation-patterns |
| Review frontend code | `react-code-reviewer` | sonnet | react-development-patterns, typescript-advanced-types |
| Security audit | `security-engineer` | opus | security-patterns, openiddict-authorization |
| Write tests | `qa-engineer` | sonnet | xunit-testing-patterns, e2e-testing-patterns |
| Debug errors | `debugger` | sonnet | debugging-patterns, error-handling-patterns |
| DB migrations | `database-migrator` | sonnet | efcore-patterns, abp-framework-patterns |
| CI/CD setup | `devops-engineer` | sonnet | docker-dotnet-containerize, git-advanced-workflows |

## By Category

### Architects (Design, No Code)
| Agent | Purpose | Tools |
|-------|---------|-------|
| `business-analyst` | Requirements, domain knowledge, user stories | Read, Write, Edit, Glob, Grep |
| `backend-architect` | API design, schemas, technical specs | Read, Write, Glob, Grep |

### Engineers (Write Code)
| Agent | Purpose | Tools |
|-------|---------|-------|
| `abp-developer` | .NET/ABP implementation | Read, Write, Edit, Bash, Glob, Grep |
| `react-developer` | React/TypeScript implementation | Read, Write, Edit, Bash, Glob, Grep |
| `devops-engineer` | CI/CD, Docker, deployment | Read, Write, Edit, Bash, Glob, Grep |

### Reviewers (Read-Only Analysis)
| Agent | Purpose | Tools |
|-------|---------|-------|
| `abp-code-reviewer` | Backend code quality, ABP patterns | Read, Glob, Grep |
| `react-code-reviewer` | Frontend code quality, React patterns | Read, Glob, Grep |
| `security-engineer` | Security audit, STRIDE, OWASP | Read, Glob, Grep, WebSearch |
| `qa-engineer` | Test plans, test implementation | Read, Write, Edit, Bash, Glob, Grep |

### Specialists
| Agent | Purpose | Tools |
|-------|---------|-------|
| `debugger` | Root cause analysis, bug fixing | Read, Glob, Grep, Bash |
| `database-migrator` | EF Core migrations, schema changes | Read, Write, Edit, Bash, Glob, Grep |

## Common Agent Chains

### Feature Development (Full)
```
business-analyst → backend-architect → abp-developer → qa-engineer → abp-code-reviewer → security-engineer
```

### Feature Development (Fast)
```
backend-architect → abp-developer → qa-engineer
```

### Full-Stack Feature
```
backend-architect → [abp-developer, react-developer] → qa-engineer → [abp-code-reviewer, react-code-reviewer]
```

### Bug Fix
```
debugger → abp-developer → qa-engineer
```

### Security Hardening
```
security-engineer → abp-developer → abp-code-reviewer
```

### API Design Only
```
business-analyst → backend-architect
```

### Database Change
```
backend-architect → database-migrator → abp-developer
```

## Agent Selection Flowchart

```
What do you need?
│
├─ Requirements/domain analysis? → business-analyst
│
├─ Design (no code)?
│   ├─ API/schema design → backend-architect
│   └─ User stories → business-analyst
│
├─ Write code?
│   ├─ .NET/ABP backend → abp-developer
│   ├─ React frontend → react-developer
│   └─ CI/CD/Docker → devops-engineer
│
├─ Review existing code?
│   ├─ Backend (.cs) → abp-code-reviewer
│   ├─ Frontend (.tsx/.ts) → react-code-reviewer
│   └─ Security → security-engineer
│
├─ Testing?
│   └─ Write tests → qa-engineer
│
├─ Debug/fix bug? → debugger
│
└─ Database migration? → database-migrator
```

## Agent Boundaries (Scope)

| Agent | Does | Does NOT |
|-------|------|----------|
| `business-analyst` | Requirements, user stories, domain docs | Design APIs, write code |
| `backend-architect` | API design, schemas, technical specs | Write implementation code |
| `abp-developer` | Implement backend, write tests | Design APIs, define requirements |
| `abp-code-reviewer` | Review backend code quality | Write code, review frontend |
| `react-code-reviewer` | Review frontend code quality | Write code, review backend |
| `security-engineer` | Security audits, threat modeling | Write code, general code review |
| `qa-engineer` | Write tests, test plans | Review code, implement features |
