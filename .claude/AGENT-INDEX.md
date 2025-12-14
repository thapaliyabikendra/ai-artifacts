---
name: agent-index
description: "Grep-optimized agent lookup tables. Use Grep to extract rows, not full Read."
type: index
updated: 2024-12-14
total_agents: 11
---

# Agent Index

## Summary

Discovery index for agents. Use `Grep("agent-name", AGENT-INDEX.md)` to extract entries.
Consolidated from AGENT-QUICK-REF.md for grep-friendly lookups.

---
## Master Index

| Agent | Category | Model | Tools | Path |
|-------|----------|-------|-------|------|
| abp-code-reviewer | reviewer | sonnet | Read,Glob,Grep | agents/reviewers/abp-code-reviewer.md |
| abp-developer | engineer | sonnet | Read,Write,Edit,Bash,Glob,Grep | agents/engineers/abp-developer.md |
| backend-architect | architect | sonnet | Read,Write,Glob,Grep | agents/architects/backend-architect.md |
| business-analyst | architect | sonnet | Read,Write,Edit,Glob,Grep | agents/architects/business-analyst.md |
| database-migrator | specialist | sonnet | Read,Write,Edit,Bash,Glob,Grep | agents/specialists/database-migrator.md |
| debugger | specialist | sonnet | Read,Glob,Grep,Bash | agents/specialists/debugger.md |
| devops-engineer | engineer | sonnet | Read,Write,Edit,Bash,Glob,Grep | agents/engineers/devops-engineer.md |
| qa-engineer | reviewer | sonnet | Read,Write,Edit,Bash,Glob,Grep | agents/reviewers/qa-engineer.md |
| react-code-reviewer | reviewer | sonnet | Read,Glob,Grep | agents/reviewers/react-code-reviewer.md |
| react-developer | engineer | sonnet | Read,Write,Edit,Bash,Glob,Grep | agents/engineers/react-developer.md |
| security-engineer | reviewer | opus | Read,Glob,Grep,WebSearch | agents/reviewers/security-engineer.md |
---
## Lookup by Task

| Task | Agent | Skills |
|------|-------|--------|
| Analyze requirements | business-analyst | domain-modeling, requirements-engineering |
| Design API/schema | backend-architect | technical-design-patterns, api-design-principles, efcore-patterns |
| Implement .NET/ABP | abp-developer | abp-framework-patterns, efcore-patterns, fluentvalidation-patterns |
| Implement React | react-developer | react-development-patterns, typescript-advanced-types |
| Review backend code | abp-code-reviewer | abp-framework-patterns, efcore-patterns, fluentvalidation-patterns |
| Review frontend code | react-code-reviewer | react-development-patterns, typescript-advanced-types |
| Security audit | security-engineer | security-patterns, openiddict-authorization |
| Write tests | qa-engineer | xunit-testing-patterns, e2e-testing-patterns |
| Debug errors | debugger | debugging-patterns, error-handling-patterns |
| DB migrations | database-migrator | efcore-patterns, abp-framework-patterns |
| CI/CD setup | devops-engineer | docker-dotnet-containerize, git-advanced-workflows |
---
## Lookup by Category

### architect
| Agent | Purpose | Writes Code |
|-------|---------|-------------|
| backend-architect | API design, schemas, technical specs | No |
| business-analyst | Requirements, domain knowledge, user stories | No |

### engineer
| Agent | Purpose | Writes Code |
|-------|---------|-------------|
| abp-developer | .NET/ABP implementation | Yes |
| devops-engineer | CI/CD, Docker, deployment | Yes |
| react-developer | React/TypeScript implementation | Yes |

### reviewer
| Agent | Purpose | Writes Code |
|-------|---------|-------------|
| abp-code-reviewer | Backend code quality, ABP patterns | No |
| qa-engineer | Test plans, test implementation | Yes |
| react-code-reviewer | Frontend code quality, React patterns | No |
| security-engineer | Security audit, STRIDE, OWASP | No |

### specialist
| Agent | Purpose | Writes Code |
|-------|---------|-------------|
| database-migrator | EF Core migrations, schema changes | Yes |
| debugger | Root cause analysis, bug fixing | Yes |
---
## Lookup by Capability

| Capability | Agents |
|------------|--------|
| Writes code | abp-developer, react-developer, devops-engineer, qa-engineer, database-migrator, debugger |
| Read-only | abp-code-reviewer, react-code-reviewer, security-engineer, backend-architect, business-analyst |
| Uses Bash | abp-developer, react-developer, devops-engineer, qa-engineer, database-migrator, debugger |
| Uses WebSearch | security-engineer |
| Uses opus model | security-engineer |
---
## Agent Chains

| Workflow | Chain |
|----------|-------|
| Feature (full) | business-analyst → backend-architect → abp-developer → qa-engineer → abp-code-reviewer → security-engineer |
| Feature (fast) | backend-architect → abp-developer → qa-engineer |
| Full-stack | backend-architect → [abp-developer, react-developer] → qa-engineer → [abp-code-reviewer, react-code-reviewer] |
| Bug fix | debugger → abp-developer → qa-engineer |
| Security hardening | security-engineer → abp-developer → abp-code-reviewer |
| API design only | business-analyst → backend-architect |
| Database change | backend-architect → database-migrator → abp-developer |
---
## Agent Boundaries

| Agent | Does | Does NOT |
|-------|------|----------|
| abp-code-reviewer | Review backend code quality | Write code, review frontend |
| abp-developer | Implement backend, write tests | Design APIs, define requirements |
| backend-architect | API design, schemas, technical specs | Write implementation code |
| business-analyst | Requirements, user stories, domain docs | Design APIs, write code |
| database-migrator | Generate migrations, review SQL | Design schemas, implement features |
| debugger | Root cause analysis, fix bugs | Implement features, review code |
| devops-engineer | CI/CD pipelines, Docker, deployment | Write application code |
| qa-engineer | Write tests, test plans | Review code, implement features |
| react-code-reviewer | Review frontend code quality | Write code, review backend |
| react-developer | Implement frontend, write tests | Design APIs, backend code |
| security-engineer | Security audits, threat modeling | Write code, general review |
---
## Selection Flowchart

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
│   ├─ Frontend (.tsx) → react-code-reviewer
│   └─ Security → security-engineer
│
├─ Testing?
│   └─ Write tests → qa-engineer
│
├─ Debug/fix bug? → debugger
│
└─ Database migration? → database-migrator
```
---
## Related

- [SKILL-INDEX.md](SKILL-INDEX.md) - Skill lookup tables
- [AGENT-QUICK-REF.md](AGENT-QUICK-REF.md) - Original quick reference
- [content-retrieval](skills/content-retrieval/SKILL.md) - Retrieval protocol
