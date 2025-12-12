---
description: Scaffold complete ABP entity with all layers (Entity, DTOs, AppService, Validator)
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <EntityName> [--properties "Name:string,Email:string"] [--fast] [--audit full|basic|none]
model: sonnet
---

# Generate Entity Command

Scaffold a complete ABP Framework entity with all layers.

**Arguments**: $ARGUMENTS

## Pre-flight

**Project**: !`basename $(pwd)`
**Domain**: !`find api/src -maxdepth 1 -type d -name "*Domain" ! -name "*Shared" 2>/dev/null | head -1`
**Application**: !`find api/src -maxdepth 1 -type d -name "*Application" ! -name "*Contracts" 2>/dev/null | head -1`

Required context:
- Read `CLAUDE.md` for project conventions
- Read `docs/architecture/README.md` for project paths

## Mode Selection

| Mode | Stages | Speed | Use When |
|------|--------|-------|----------|
| (default) | Full scaffolding with docs | ~3 min | Complete feature setup |
| `--fast` | Code only, no docs | ~2 min | Quick CRUD, prototyping |
| `--minimal` | Entity + DTO only | ~1 min | Minimal scaffolding |

## Workflow

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ 1.Entity │ → │ 2. DTOs  │ → │ 3.Service│ → │ 4.Valid- │ → │ 5.DbCtx  │
│ (Domain) │   │(Contract)│   │  (App)   │   │  ator    │   │  + Perm  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

## Execution

Use Task tool with `subagent_type="abp-developer"`:

```
Generate complete ABP entity scaffolding for: {EntityName}

Properties: {properties or prompt for them}
Audit: {audit-level: full|basic|none, default: full}
Mode: {default|fast|minimal}

Skills: Apply abp-framework-patterns, abp-entity-patterns, abp-service-patterns, efcore-patterns, fluentvalidation-patterns

## Output Files

### 1. Domain Layer: Entity
api/src/{Project}.Domain/{EntityPlural}/{Entity}.cs
- Inherit FullAuditedAggregateRoot<Guid>
- Private setters with SetXxx() methods
- Private parameterless constructor
- Validation in setters using Check.NotNullOrWhiteSpace

### 2. Application.Contracts: DTOs + Interface
api/src/{Project}.Application.Contracts/{EntityPlural}/
- {Entity}Dto.cs
- CreateUpdate{Entity}Dto.cs
- Get{Entity}ListInput.cs (extends PagedAndSortedResultRequestDto)
- I{Entity}AppService.cs

### 3. Application: AppService + Validator
api/src/{Project}.Application/{EntityPlural}/
- {Entity}AppService.cs (CRUD with [Authorize] attributes)
- CreateUpdate{Entity}DtoValidator.cs (FluentValidation)

### 4. EntityFrameworkCore: Configuration
api/src/{Project}.EntityFrameworkCore/{EntityPlural}/
- {Entity}Configuration.cs (IEntityTypeConfiguration)
- Add DbSet<{Entity}> to DbContext

### 5. Permissions (edit existing)
- Add constants to {Project}Permissions.cs
- Register in PermissionDefinitionProvider.cs

### 6. Mapperly (edit existing)
- Add mapping methods to ApplicationMappers.cs

## Build Verification
Run: dotnet build api/*.slnx
```

## Options

| Option | Effect |
|--------|--------|
| `--properties` | Property definitions (Name:type format) |
| `--fast` | Skip documentation, code only (~2 min) |
| `--minimal` | Entity + DTO only, no service |
| `--audit full` | FullAuditedAggregateRoot (default) |
| `--audit basic` | AuditedAggregateRoot |
| `--audit none` | AggregateRoot |
| `--with-filter` | Generate separate Filter DTO |
| `--with-response-wrapper` | Use ResponseModel wrapper |
| `--no-validator` | Skip FluentValidation validator |
| `--no-permissions` | Skip permission scaffolding |

## Property Type Reference

| Type | C# Type | Example |
|------|---------|---------|
| `string` | `string` | `Name:string` |
| `int` | `int` | `Quantity:int` |
| `decimal` | `decimal` | `Price:decimal` |
| `bool` | `bool` | `IsActive:bool` |
| `DateTime` | `DateTime` | `DueDate:DateTime` |
| `Guid` | `Guid` | `CategoryId:Guid` |
| `Guid?` | `Guid?` | `ParentId:Guid?` |
| `{EnumName}` | enum | `Status:OrderStatus` |

## Examples

```bash
# Basic entity (full mode)
/generate:entity Product --properties "Name:string,Price:decimal,Stock:int"

# Fast CRUD (no docs)
/generate:entity Invoice --properties "Number:string,Amount:decimal" --fast

# With filter DTO for advanced querying
/generate:entity Patient --properties "Name:string,Status:PatientStatus" --with-filter

# Without soft delete
/generate:entity AuditLog --audit basic

# Minimal scaffolding
/generate:entity Category --properties "Name:string" --minimal
```

## Output Summary

```
## Entity Generated: {EntityName}

### Files Created
- api/src/{Project}.Domain/{EntityPlural}/{Entity}.cs
- api/src/{Project}.Application.Contracts/{EntityPlural}/{Entity}Dto.cs
- api/src/{Project}.Application.Contracts/{EntityPlural}/CreateUpdate{Entity}Dto.cs
- api/src/{Project}.Application.Contracts/{EntityPlural}/I{Entity}AppService.cs
- api/src/{Project}.Application/{EntityPlural}/{Entity}AppService.cs
- api/src/{Project}.Application/{EntityPlural}/CreateUpdate{Entity}DtoValidator.cs
- api/src/{Project}.EntityFrameworkCore/{EntityPlural}/{Entity}Configuration.cs

### Files Modified
- Permissions, PermissionDefinitionProvider, DbContext, ApplicationMappers

### API Endpoints (auto-generated)
- GET    /api/app/{entity}
- GET    /api/app/{entity}/{id}
- POST   /api/app/{entity}
- PUT    /api/app/{entity}/{id}
- DELETE /api/app/{entity}/{id}

### Next Steps
1. /generate:migration Add{Entity}
2. dotnet run --project api/src/{Project}.DbMigrator
3. Test API via Swagger
```

## Checkpoint

- [ ] Entity created with proper encapsulation
- [ ] DTOs created
- [ ] AppService implements CRUD with authorization
- [ ] Validator uses FluentValidation
- [ ] DbSet added to DbContext
- [ ] Permissions defined
- [ ] Build succeeds
