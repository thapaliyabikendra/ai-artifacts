# CLAUDE.md

Guidance for Claude Code when working with this repository.

## Project Overview

**Clinic Management System** - A layered monolith built on ABP Framework using Domain Driven Design. Manages patients, appointments, and doctor schedules.

**Tech Stack**: .NET 10, ABP Framework 10.0.1, Entity Framework Core, PostgreSQL, Redis, OpenIddict

## Quick Reference

| Action | Command |
|--------|---------|
| Build | `dotnet build api/ClinicManagementSystem.slnx` |
| Run API | `dotnet run --project api/src/ClinicManagementSystem.HttpApi.Host` |
| Run Migrations | `dotnet run --project api/src/ClinicManagementSystem.DbMigrator` |
| Run Tests | `dotnet test api/` |

For detailed commands and project structure, see **[docs/architecture/README.md](docs/architecture/README.md)**.

## Claude Code Extensions

For choosing between Agents, Skills, Commands, and Hooks, see **[.claude/GUIDELINES.md](.claude/GUIDELINES.md)**.

| Mechanism | Invocation | Best For |
|-----------|------------|----------|
| **Skill** | Automatic | Domain expertise, patterns |
| **Agent** | Delegated | Complex tasks with context isolation |
| **Command** | `/cmd` | Atomic, frequent actions |

**Creating artifacts**: Say "create a skill for..." or "create an agent that..." to auto-trigger the `claude-artifact-creator` skill.

## Available Agents (10)

Located in `.claude/agents/` organized by role:

| Category | Count | Examples |
|----------|-------|----------|
| **Architects** | 2 | business-analyst, backend-architect |
| **Engineers** | 3 | abp-developer, react-developer, devops-engineer |
| **Reviewers** | 3 | code-reviewer, security-engineer, qa-engineer |
| **Specialists** | 2 | debugger, database-migrator |

**Usage**: `Use the abp-developer agent to implement the Patient service`

## Available Skills (27)

Located in `.claude/skills/` organized by topic:

| Category | Count | Key Skills |
|----------|-------|------------|
| **Backend** | 9 | abp-framework-patterns, efcore-patterns, fluentvalidation-patterns |
| **Microservices** | 3 | distributed-events-advanced, grpc-integration-patterns, bulk-operations-patterns |
| **API Design** | 2 | api-response-patterns, api-design-principles |
| **Requirements** | 5 | requirements-engineering, domain-modeling, technical-design-patterns |
| **Testing** | 3 | xunit-testing-patterns, e2e-testing-patterns, javascript-testing-patterns |
| **Security** | 1 | security-patterns |
| **Frontend** | 2 | typescript-advanced-types, modern-javascript-patterns |
| **DevOps** | 2 | docker-dotnet-containerize, git-advanced-workflows |

Skills are auto-triggered based on context. For ABP patterns, the `abp-framework-patterns` skill provides entity, AppService, DTO, and validation patterns.

## Available Commands (9)

Located in `.claude/commands/` organized by action:

| Category | Commands |
|----------|----------|
| **Feature** | `/add-feature` - End-to-end feature development |
| **Generate** | `/generate:entity`, `/generate:filter`, `/generate:migration` |
| **TDD** | `/tdd-cycle`, `/tdd-red`, `/tdd-refactor` |
| **Review** | `/review:permissions` |
| **Debug** | `/smart-debug` |

## Feature Development

Use the `/add-feature` command for end-to-end feature development:

```bash
/add-feature <feature-name> "<requirements>"
```

**Example**: `/add-feature patient-management "CRUD for patients with name, email, phone, DOB"`

The command orchestrates 6 stages through specialized agents (analyze → design → implement → test → review → security). See command help for options (`--stage`, `--review`, `--security`, `--dry-run`).

## Documentation

All domain and project documentation is in **[docs/](docs/README.md)**:

| Folder | Purpose |
|--------|---------|
| `docs/domain/` | Business rules, entities, permissions, roles |
| `docs/architecture/` | Project structure, patterns, API contracts |
| `docs/features/` | Per-feature requirements, designs, test cases |

Agents read from and write to these docs during workflows.

## Prerequisites

- .NET 10.0+ SDK
- PostgreSQL
- Redis
- Node v20.11+ (for AuthServer)

First run: Execute `abp install-libs` in AuthServer, then run DbMigrator.

## Conventions

### Naming

| Type | Pattern | Example |
|------|---------|---------|
| Entity | PascalCase | `Patient`, `DoctorSchedule` |
| DTO | `{Entity}Dto`, `CreateUpdate{Entity}Dto` | `PatientDto` |
| AppService | `{Entity}AppService` | `PatientAppService` |
| Permission | `{Project}.{Resource}.{Action}` | `ClinicManagementSystem.Patients.Create` |

### Critical Patterns

- **Entities**: Inherit `FullAuditedAggregateRoot<Guid>` (soft delete + auditing)
- **Validation**: FluentValidation (not data annotations)
- **Mapping**: Mapperly in `*ApplicationMappers.cs` (NOT AutoMapper)
- **Permissions**: Define in `*Permissions.cs`, check with `[Authorize]`

For detailed patterns, apply the `abp-framework-patterns` skill.

### Warnings

- Always run from `api/` directory for dotnet commands
- Never commit secrets to `.env` files
- All mutations require authorization attributes
- Use `WhereIf` pattern for optional filters in queries
