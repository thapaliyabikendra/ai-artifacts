# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Clinic Management System** - a layered monolith application built on **ABP Framework** using Domain Driven Design (DDD). The system manages patients, appointments, and doctor schedules for a local clinic.

**Tech Stack**: .NET 10, ABP Framework 10.0.1, Entity Framework Core, PostgreSQL, Redis, OpenIddict (OAuth 2.0)

## Repository Structure

```
ai-artifacts/
├── api/                    # .NET Backend (ABP Framework)
│   ├── src/               # Source projects
│   └── test/              # Test projects
├── ui/                    # Frontend (React 18+ - planned)
├── docs/                  # Business requirements documentation
├── .claude/
│   ├── agents/            # Specialized sub-agents (BY ROLE)
│   ├── commands/          # Slash commands (BY ACTION)
│   ├── skills/            # Domain knowledge skills (BY TOPIC)
│   └── GUIDELINES.md      # Organization rules & tool selection guide
└── CLAUDE.md              # This file
```

## Claude Code Extension Guide

For choosing between Agents, Skills, Commands, Hooks, and Output Styles, see **[.claude/GUIDELINES.md](.claude/GUIDELINES.md)**. Key decision factors:

| Mechanism | Invocation | Best For |
|-----------|------------|----------|
| **Skill** | Automatic (model-invoked) | Reusable domain expertise |
| **Agent** | Auto-delegated or explicit | Complex tasks with context isolation |
| **Command** | Manual (`/cmd`) | Atomic, frequent actions |

### Creating or Modifying Claude Artifacts

When creating new agents, skills, or commands, or improving existing ones:
- Say "create a skill for..." or "create an agent that..." to auto-trigger the `claude-artifact-creator` skill
- The skill provides templates, validation, and ensures guideline compliance
- All artifacts must follow `.claude/GUIDELINES.md` rules (agents <150 lines, skills <500 lines, etc.)

## Build Commands

All commands should be run from `api/` directory:

```bash
# Build solution
dotnet build ClinicManagementSystem.slnx

# Run API host
dotnet run --project src/ClinicManagementSystem.HttpApi.Host

# Run AuthServer
dotnet run --project src/ClinicManagementSystem.AuthServer

# Run database migrations
dotnet run --project src/ClinicManagementSystem.DbMigrator

# Run all tests
dotnet test

# Run specific test project
dotnet test test/ClinicManagementSystem.Application.Tests
```

## ABP Framework Architecture

### Layer Dependencies (bottom to top)
```
Domain.Shared → Domain → EntityFrameworkCore
                ↓
Application.Contracts → Application → HttpApi → HttpApi.Host
                                  ↓
                           HttpApi.Client
```

### Project Responsibilities

| Layer | Purpose |
|-------|---------|
| `Domain.Shared` | Enums, constants, localization resources shared across all layers |
| `Domain` | Entities, aggregate roots, domain services, repository interfaces |
| `Application.Contracts` | DTOs, application service interfaces |
| `Application` | Application services implementing business logic |
| `HttpApi` | API controllers, REST endpoints |
| `HttpApi.Host` | API startup, configuration, dependency injection |
| `EntityFrameworkCore` | EF Core DbContext, repository implementations, migrations |
| `AuthServer` | OAuth 2.0 authentication server (OpenIddict) |
| `DbMigrator` | Database migration console app |

### Key ABP Patterns

- **AppServices**: Inherit from `ApplicationService` or implement `IApplicationService`
- **DTOs**: Use `CreateUpdateDtoBase`, `EntityDto<TKey>` patterns
- **Validation**: FluentValidation with ABP integration
- **AutoMapper**: Configure in `*ApplicationAutoMapperProfile.cs`
- **Permissions**: Define in `*Permissions.cs`, grant in module configuration

## Available Sub-Agents

The `.claude/agents/` directory contains 11 specialized agents organized by role:

### Architects (4)
| Agent | Purpose |
|-------|---------|
| `business-analyst` | Requirements, domain management, impact analysis |
| `backend-architect` | API design, database schema, TSD |
| `api-documenter` | OpenAPI documentation, developer portals |
| `docs-architect` | Technical documentation from codebases |

### Engineers (3)
| Agent | Purpose |
|-------|---------|
| `abp-developer` | .NET/ABP Framework backend implementation |
| `react-developer` | React 18+ frontend with UI/UX |
| `devops-engineer` | CI/CD, Docker, releases |

### Reviewers (3)
| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Code quality, PR reviews |
| `security-engineer` | Security audits, STRIDE, OWASP |
| `qa-engineer` | Test automation (xUnit, Playwright) |

### Specialists (1)
| Agent | Purpose |
|-------|---------|
| `debugger` | Root cause analysis, error diagnosis |

**Usage**: `Use the engineers/abp-developer agent to implement the Patient service`

## Available Skills

The `.claude/skills/` directory contains domain knowledge skills:

### Backend Skills
- **abp-framework-patterns**: ABP repository, unit of work, domain services, CRUD templates
- **efcore-patterns**: EF Core entity configuration, DbContext, migrations, relationships
- **linq-optimization-patterns**: N+1 prevention, Include patterns, projections, AsNoTracking
- **debugging-patterns**: Root cause analysis, common ABP/EF/React issues and fixes
- **csharp-advanced-patterns**: Records, pattern matching, async, LINQ, performance
- **dotnet-async-patterns**: Async/await, ValueTask, cancellation tokens
- **error-handling-patterns**: Exception handling, Result types

### Requirements & Design Skills
- **requirements-engineering**: User stories, acceptance criteria, BRD patterns
- **domain-modeling**: Entity definitions, business rules (BR-XXX), impact analysis
- **technical-design-patterns**: TSD templates, API contracts, database schemas, ADRs
- **api-design-principles**: REST/GraphQL API design patterns
- **mermaid-diagram-patterns**: ERD, sequence, flowchart, architecture diagrams

### Testing Skills
- **xunit-testing-patterns**: xUnit tests for ABP, test data seeders
- **e2e-testing-patterns**: Playwright automation
- **javascript-testing-patterns**: Jest, React Testing Library

### Security Skills
- **security-patterns**: STRIDE threat modeling, OWASP Top 10, security audits

### Frontend Skills
- **typescript-advanced-types**: Generics, conditional types, mapped types
- **modern-javascript-patterns**: ES6+, async patterns

### DevOps Skills
- **docker-dotnet-containerize**: Multi-stage Dockerfiles for .NET
- **git-advanced-workflows**: Rebasing, cherry-picking, bisect

### Review Skills
- **code-review-excellence**: PR review best practices

### Workflow Skills
- **feature-development-workflow**: End-to-end feature development orchestration

### Meta Skills
- **claude-artifact-creator**: Create and improve Claude artifacts (skills, agents, commands)

## Feature Development Workflow

This project uses automated workflows for end-to-end feature development.

### Quick Start: Add New Feature

```bash
/add-feature <feature-name> "<requirements>"
```

**Example:**
```bash
/add-feature patient-management "CRUD for patients with name, email, phone, DOB. Search and filter patients."
```

### Workflow Stages

```
┌─────────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
│ 1.Analyze & │ → │ 2.Design  │ → │ 3.Implement│ → │ 4.Test    │ → │ 5.Review  │ → │ 6.Security│
│   Require   │   │ (backend- │   │ (abp-     │   │ (qa-      │   │ (code-    │   │ (security-│
│ (business-  │   │ architect)│   │ developer)│   │ engineer) │   │ reviewer) │   │ engineer) │
│  analyst)   │   │           │   │           │   │           │   │           │   │           │
└─────────────┘   └───────────┘   └───────────┘   └───────────┘   └───────────┘   └───────────┘
```

**Note**: Stages 5-6 are optional (use `--review`, `--security`, or `--full-review`)

| Stage | Agent | Output | Optional |
|-------|-------|--------|----------|
| 1. Analyze & Require | `business-analyst` | `requirements.md`, `impact-analysis.md`, domain updates | No |
| 2. Design | `backend-architect` | `technical-design.md` | No |
| 3. Implementation | `abp-developer` | ABP source code | No |
| 4. Testing | `qa-engineer` | `test-cases.md` + tests | No |
| 5. Code Review | `code-reviewer` | `review-report.md` | Yes |
| 6. Security | `security-engineer` | `security-audit.md` | Yes |

### Command Options

```bash
# Full workflow (Stages 1-4)
/add-feature patient "Patient CRUD"

# Single stage only
/add-feature patient --stage analyze
/add-feature patient --stage design
/add-feature patient --stage implement
/add-feature patient --stage test
/add-feature patient --stage review
/add-feature patient --stage security

# With optional stages
/add-feature patient "Patient CRUD" --review        # Stages 1-5
/add-feature patient "Patient CRUD" --security      # Stages 1-4 + 6
/add-feature patient "Patient CRUD" --full-review   # Stages 1-6

# Preview without creating files
/add-feature patient "Patient CRUD" --dry-run
```

### Generated Code Structure

For a feature named `patient`:

```
api/src/
├── ClinicManagementSystem.Domain/
│   └── Patients/
│       ├── Patient.cs              # Entity
│       └── PatientManager.cs       # Domain service (if needed)
│
├── ClinicManagementSystem.Application.Contracts/
│   └── Patients/
│       ├── IPatientAppService.cs
│       ├── PatientDto.cs
│       ├── CreateUpdatePatientDto.cs
│       └── GetPatientListInput.cs
│
├── ClinicManagementSystem.Application/
│   └── Patients/
│       ├── PatientAppService.cs
│       └── PatientDtoValidator.cs
│
└── ClinicManagementSystem.EntityFrameworkCore/
    └── (DbContext configuration)
```

### ABP Conventions Enforced

- All entities inherit `FullAuditedAggregateRoot<Guid>` (soft delete + auditing)
- All list endpoints support pagination (`PagedAndSortedResultRequestDto`)
- All mutations require authorization attributes
- All input DTOs have FluentValidation validators
- All code follows ABP naming conventions

### Feature Documentation Templates

Located in `docs/features/_templates/`:
- `requirements-template.md` - User stories, acceptance criteria
- `technical-design-template.md` - Entity design, API contracts
- `test-cases-template.md` - Test cases with xUnit templates

## Prerequisites

- .NET 10.0+ SDK
- Node v20.11+ (for AuthServer client libraries)
- Redis (for distributed caching)
- PostgreSQL

Before first run:
1. Run `abp install-libs` in AuthServer directory for client libraries
2. Run DbMigrator to create database and seed initial data

## Documentation Structure

The `docs/` folder is organized for efficient agent workflows:

```
docs/
├── README.md                    # Documentation hub
├── domain/                      # Business domain knowledge
│   ├── README.md               # Domain overview
│   ├── entities/               # Entity definitions (one per file)
│   ├── business-rules.md       # BR-XXX format rules
│   ├── roles.md                # User roles and capabilities
│   ├── permissions.md          # Permission structure
│   └── enums.md                # Enumeration definitions
├── architecture/               # Technical architecture
│   ├── README.md               # Project paths, build commands
│   └── patterns.md             # Code patterns, conventions
├── features/                   # Feature-specific docs
│   └── {feature}/             # Per-feature documentation
│       ├── requirements.md
│       ├── technical-design.md
│       ├── test-cases.md
│       ├── review-report.md
│       └── security-audit.md
├── backlog.md                  # User stories
├── decisions.md                # ADRs
├── releases.md                 # Release history
└── dev-progress.md             # Activity log
```

### Agent → Document Access

| Agent | Primary Docs | Writes |
|-------|--------------|--------|
| `business-analyst` | `domain/*` | Entity definitions, rules, permissions, `requirements.md`, `impact-analysis.md` |
| `backend-architect` | `architecture/`, `domain/entities/` | `technical-design.md` |
| `abp-developer` | `architecture/`, `features/` | Implementation code |
| `qa-engineer` | `domain/business-rules.md` | `test-cases.md` |
| `code-reviewer` | `architecture/patterns.md` | `review-report.md` |
| `security-engineer` | `domain/permissions.md` | `security-audit.md` |
