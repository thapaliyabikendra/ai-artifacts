# CLAUDE.md

Guidance for Claude Code when working with this repository.

## Project Overview

**[Project Name]** - Brief description of your project.

**Tech Stack**

| Component | Technology |
|-----------|------------|
| Runtime | .NET 10 |
| Framework | ABP Framework 10.x |
| Database | PostgreSQL |
| ORM | Entity Framework Core |
| Auth | OpenIddict (OAuth 2.0) |
| Mapping | Mapperly |
| Validation | FluentValidation |
| Testing | xUnit + Shouldly + NSubstitute |

## Quick Reference

| Action | Command |
|--------|---------|
| Build | `dotnet build` |
| Run | `dotnet run --project src/YourProject.HttpApi.Host` |
| Test | `dotnet test` |

<!-- ai-artifacts:START -->
<!-- This section is managed by ai-artifacts. Do not edit manually. -->

## AI Artifacts

**Version:** 1.0.0 | **Installed:** {{INSTALL_DATE}}

### Quick Skill Reference

| Task | Skill |
|------|-------|
| Entity/DTO/AppService | `abp-framework-patterns` |
| DbContext/Migration | `efcore-patterns` |
| Input validation | `fluentvalidation-patterns` |
| Permissions/Auth | `openiddict-authorization` |
| Unit/Integration tests | `xunit-testing-patterns` |
| Query optimization | `linq-optimization-patterns` |
| API design | `api-design-principles` |
| Debug/errors | `debugging-patterns` |
| Security audit | `security-patterns` |
| React components | `react-development-patterns` |

### Available Agents

| Task | Agent |
|------|-------|
| Analyze requirements | `business-analyst` |
| Design API/schema | `backend-architect` |
| Implement .NET/ABP | `abp-developer` |
| Implement React | `react-developer` |
| Review backend code | `abp-code-reviewer` |
| Review frontend code | `react-code-reviewer` |
| Security audit | `security-engineer` |
| Write tests | `qa-engineer` |
| Debug errors | `debugger` |
| DB migrations | `database-migrator` |
| CI/CD setup | `devops-engineer` |

### Quick Commands

| Task | Command |
|------|---------|
| New feature | `/feature:add-feature <name> "<requirements>"` |
| Scaffold entity | `/generate:entity <Name> --properties "..."` |
| DB migration | `/generate:migration <name>` |
| TDD cycle | `/tdd:tdd-cycle "<feature>"` |
| Debug error | `/debug:smart-debug "<error>"` |
| Review permissions | `/review:permissions` |

For full documentation, see `.claude/GUIDELINES.md`.

<!-- ai-artifacts:END -->

## Conventions

### Naming

| Type | Pattern | Example |
|------|---------|---------|
| Entity | PascalCase | `Patient` |
| DTO | `{Entity}Dto` | `PatientDto` |
| AppService | `{Entity}AppService` | `PatientAppService` |

### Critical Patterns

- **Entities**: Inherit `FullAuditedAggregateRoot<Guid>`
- **Validation**: FluentValidation (not data annotations)
- **Mapping**: Mapperly (NOT AutoMapper)
