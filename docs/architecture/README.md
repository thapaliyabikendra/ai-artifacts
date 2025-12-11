# Architecture Overview

> **Purpose**: Technical architecture and project configuration for the Clinic Management System.
> **Maintained By**: `backend-architect` agent
> **Last Updated**: 2025-12-11

## Project Identity

| Setting | Value |
|---------|-------|
| **Project Name** | ClinicManagementSystem |
| **Solution File** | `api/ClinicManagementSystem.slnx` |
| **Root Namespace** | `ClinicManagementSystem` |
| **Framework** | ABP Framework 10.0.1 |
| **Runtime** | .NET 10 |
| **Database** | PostgreSQL |
| **ORM** | Entity Framework Core |
| **Auth** | OpenIddict (OAuth 2.0) |

## Solution Structure

```
api/
├── src/
│   ├── ClinicManagementSystem.Domain.Shared/    # Enums, constants, localization
│   ├── ClinicManagementSystem.Domain/           # Entities, domain services
│   ├── ClinicManagementSystem.Application.Contracts/  # DTOs, interfaces
│   ├── ClinicManagementSystem.Application/      # AppServices, validators
│   ├── ClinicManagementSystem.EntityFrameworkCore/    # DbContext, migrations
│   ├── ClinicManagementSystem.HttpApi/          # Controllers
│   ├── ClinicManagementSystem.HttpApi.Host/     # API startup
│   ├── ClinicManagementSystem.AuthServer/       # OAuth server
│   └── ClinicManagementSystem.DbMigrator/       # Migration runner
└── test/
    ├── ClinicManagementSystem.TestBase/         # Test utilities
    ├── ClinicManagementSystem.Application.Tests/
    ├── ClinicManagementSystem.Domain.Tests/
    └── ClinicManagementSystem.EntityFrameworkCore.Tests/
```

## Layer Dependencies

```
Domain.Shared → Domain → EntityFrameworkCore
                ↓
Application.Contracts → Application → HttpApi → HttpApi.Host
                                  ↓
                           HttpApi.Client
```

## Path Templates

### Source Code

| Layer | Path |
|-------|------|
| Domain.Shared | `api/src/ClinicManagementSystem.Domain.Shared/{Feature}/` |
| Domain | `api/src/ClinicManagementSystem.Domain/{Feature}/` |
| Application.Contracts | `api/src/ClinicManagementSystem.Application.Contracts/{Feature}/` |
| Application | `api/src/ClinicManagementSystem.Application/{Feature}/` |
| EntityFrameworkCore | `api/src/ClinicManagementSystem.EntityFrameworkCore/` |
| Permissions | `api/src/ClinicManagementSystem.Application.Contracts/Permissions/` |

### Test Code

| Layer | Path |
|-------|------|
| TestBase | `api/test/ClinicManagementSystem.TestBase/{Feature}/` |
| Application.Tests | `api/test/ClinicManagementSystem.Application.Tests/{Feature}/` |
| Domain.Tests | `api/test/ClinicManagementSystem.Domain.Tests/{Feature}/` |

### Documentation

| Document | Path |
|----------|------|
| Requirements | `docs/features/{feature-name}/requirements.md` |
| Technical Design | `docs/features/{feature-name}/technical-design.md` |
| Test Cases | `docs/features/{feature-name}/test-cases.md` |

## Build Commands

```bash
# Build solution
dotnet build api/ClinicManagementSystem.slnx

# Run API
dotnet run --project api/src/ClinicManagementSystem.HttpApi.Host

# Run migrations
dotnet run --project api/src/ClinicManagementSystem.DbMigrator

# Run tests
dotnet test api/

# Add migration
dotnet ef migrations add {Name} \
  -p api/src/ClinicManagementSystem.EntityFrameworkCore \
  -s api/src/ClinicManagementSystem.DbMigrator
```

## Related Documentation

| Document | Purpose |
|----------|---------|
| [patterns.md](patterns.md) | Coding patterns and conventions |
| [api-contracts.md](api-contracts.md) | API endpoint reference |
| [../domain/README.md](../domain/README.md) | Business domain knowledge |
