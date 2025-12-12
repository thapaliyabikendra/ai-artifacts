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

## Quick Skill Reference

**Use directly for single-skill tasks (no file reads needed):**

| Task | Skill |
|------|-------|
| Entity/DTO/AppService | `abp-framework-patterns` |
| DbContext/Migration | `efcore-patterns` |
| Input validation | `fluentvalidation-patterns` |
| Permissions/Auth | `openiddict-authorization` |
| Unit/Integration tests | `xunit-testing-patterns` |
| Query optimization | `linq-optimization-patterns` |
| API design | `api-design-principles` + `technical-design-patterns` |
| Debug/errors | `debugging-patterns` |
| Security audit | `security-patterns` |
| React components | `react-development-patterns` |

**For multi-skill tasks**: Read [SKILL-INDEX.md](.claude/SKILL-INDEX.md) and [CONTEXT-GRAPH.md](.claude/CONTEXT-GRAPH.md).

**For full Knowledge Discovery Protocol**: See [GUIDELINES.md](.claude/GUIDELINES.md#knowledge-architecture).

## Available Agents (10)

Located in `.claude/agents/` organized by role. Full reference: [.claude/AGENT-QUICK-REF.md](.claude/AGENT-QUICK-REF.md)

### Quick Agent Selection

| Task | Agent |
|------|-------|
| Analyze requirements | `business-analyst` |
| Design API/schema | `backend-architect` |
| Implement .NET/ABP | `abp-developer` |
| Implement React | `react-developer` |
| Review code | `code-reviewer` |
| Security audit | `security-engineer` |
| Write tests | `qa-engineer` |
| Debug errors | `debugger` |
| DB migrations | `database-migrator` |
| CI/CD setup | `devops-engineer` |

### Common Agent Chains

| Workflow | Chain |
|----------|-------|
| Feature (full) | `business-analyst` → `backend-architect` → `abp-developer` → `qa-engineer` → `code-reviewer` |
| Feature (fast) | `backend-architect` → `abp-developer` → `qa-engineer` |
| Bug fix | `debugger` → `abp-developer` → `qa-engineer` |

**Usage**: `Use the abp-developer agent to implement the Patient service`

## Available Skills (34)

Located in `.claude/skills/` organized by topic:

| Category | Count | Key Skills |
|----------|-------|------------|
| **Backend** | 12 | abp-framework-patterns, abp-entity-patterns, abp-service-patterns, abp-infrastructure-patterns, efcore-patterns, fluentvalidation-patterns |
| **Microservices** | 3 | distributed-events-advanced, grpc-integration-patterns, bulk-operations-patterns |
| **API Design** | 2 | api-response-patterns, api-design-principles |
| **Requirements** | 5 | requirements-engineering, domain-modeling, technical-design-patterns |
| **Testing** | 3 | xunit-testing-patterns, e2e-testing-patterns, javascript-testing-patterns |
| **Security** | 1 | security-patterns |
| **Frontend** | 3 | react-development-patterns, typescript-advanced-types, modern-javascript-patterns |
| **DevOps** | 2 | docker-dotnet-containerize, git-advanced-workflows |
| **Meta** | 3 | claude-artifact-creator, feature-development-workflow, knowledge-discovery |

Skills are auto-triggered based on context. For ABP patterns, use `abp-framework-patterns` for overview or the focused skills: `abp-entity-patterns` (domain), `abp-service-patterns` (application), `abp-infrastructure-patterns` (cross-cutting).

## Available Commands (15)

Located in `.claude/commands/` organized by action. Full reference: [.claude/COMMAND-INDEX.md](.claude/COMMAND-INDEX.md)

### Quick Command Reference

| Task | Command |
|------|---------|
| New feature | `/feature:add-feature <name> "<requirements>"` |
| Scaffold entity | `/generate:entity <Name> --properties "..."` |
| Entity (fast mode) | `/generate:entity <Name> --properties "..." --fast` |
| Filter DTO | `/generate:filter <Name>` |
| DB migration | `/generate:migration <name>` |
| TDD cycle | `/tdd:tdd-cycle "<feature>" [--phase red\|green\|refactor]` |
| Audit permissions | `/review:permissions` |
| Debug error | `/debug:smart-debug "<error>" [--fix]` |
| Clean code | `/refactor:refactor-clean <path>` |
| Audit deps | `/refactor:deps-audit` |
| Tech debt | `/refactor:tech-debt` |
| GitHub issue | `/team:issue <number>` |
| Standup notes | `/team:standup-notes` |
| Explain code | `/explain:code-explain <file>` |
| Generate docs | `/generate:doc-generate <target>` |
| API mocks | `/generate:api-mock <spec>` |

Commands use reference templates in `.claude/commands/references/` for detailed patterns.

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
