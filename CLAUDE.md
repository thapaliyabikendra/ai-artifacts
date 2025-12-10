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
│   ├── agents/            # Specialized sub-agents (12 agents)
│   ├── skills/            # Domain knowledge skills (20 skills)
│   └── GUIDELINES.md      # Agent organization rules
└── CLAUDE.md              # This file
```

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

## Domain Entities

- **Patient**: FirstName, LastName, Email, Phone, DateOfBirth
- **Doctor**: FullName, Specialization, Email, Phone
- **Appointment**: PatientId, DoctorId, AppointmentDate, Description, Status
- **DoctorSchedule**: DoctorId, DayOfWeek, StartTime, EndTime

**Roles**: Admin (full control), Doctor (view own appointments/patients), Receptionist (create patients, schedule appointments)

## Available Sub-Agents

The `.claude/agents/` directory contains 12 specialized agents organized by role:

### Architects
| Agent | Purpose |
|-------|---------|
| `product-architect` | Requirements, user stories, BRD |
| `backend-architect` | API design, database schema, TSD |

### Engineers
| Agent | Purpose |
|-------|---------|
| `abp-developer` | .NET/ABP Framework backend implementation |
| `react-developer` | React 18+ frontend with UI/UX |
| `devops-engineer` | CI/CD, Docker, releases |

### Reviewers
| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Code quality, PR reviews |
| `security-engineer` | Security audits, STRIDE, OWASP |
| `qa-engineer` | Test automation (xUnit, Playwright) |

### Specialists
| Agent | Purpose |
|-------|---------|
| `orchestrator` | Multi-agent workflow coordination |
| `debugger` | Root cause analysis, error diagnosis |

### Language Experts
| Agent | Purpose |
|-------|---------|
| `csharp-pro` | Advanced C#, .NET 10 patterns |
| `typescript-pro` | Advanced TypeScript, React types |

**Usage**: `Use the engineers/abp-developer agent to implement the Patient service`

## Available Skills

The `.claude/skills/` directory contains domain knowledge skills:

### Backend Skills
- **abp-framework-patterns**: ABP repository, unit of work, domain services
- **crud-service**: Generate ABP CRUD services with DTOs, validators
- **dotnet-async-patterns**: Async/await, ValueTask, cancellation tokens
- **error-handling-patterns**: Exception handling, Result types
- **postgresql**: PostgreSQL schema design, indexing
- **sql-optimization-patterns**: Query optimization, N+1 prevention

### Frontend Skills
- **typescript-advanced-types**: Generics, conditional types, mapped types
- **modern-javascript-patterns**: ES6+, async patterns
- **javascript-testing-patterns**: Jest, React Testing Library

### DevOps Skills
- **docker-dotnet-containerize**: Multi-stage Dockerfiles for .NET
- **git-advanced-workflows**: Rebasing, cherry-picking, bisect

### Review Skills
- **code-review-excellence**: PR review best practices
- **e2e-testing-patterns**: Playwright automation

### Meta Skills
- **skill-creator**: Guide for creating new skills
- **agent-creator**: Guide for creating new agents

## Prerequisites

- .NET 10.0+ SDK
- Node v20.11+ (for AuthServer client libraries)
- Redis (for distributed caching)
- PostgreSQL

Before first run:
1. Run `abp install-libs` in AuthServer directory for client libraries
2. Run DbMigrator to create database and seed initial data

## Knowledge Base Files

Documentation in `docs/` folder:

| Document | Owner Agent | Purpose |
|----------|-------------|---------|
| `business-requirements.md` | product-architect | BRD |
| `technical-specification.md` | backend-architect | TSD |
| `backlog.md` | product-architect | User stories |
| `decisions.md` | backend-architect | ADRs |
| `test-cases.md` | qa-engineer | Test plans |
| `security-audit.md` | security-engineer | Security findings |
| `releases.md` | devops-engineer | Release history |
| `dev-progress.md` | orchestrator | Activity log |
