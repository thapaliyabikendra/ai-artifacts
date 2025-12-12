---
description: Fast CRUD scaffolding - generates entity, DTOs, AppService, validator in one pass (~2 min)
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <EntityName> --properties "Name:string,Price:decimal" [--no-docs]
model: sonnet
---

# Generate CRUD Command

Fast, single-pass CRUD generation without documentation overhead.

**Arguments**: $ARGUMENTS

## Pre-flight

**Project**: !`basename $(pwd)`
**Solution**: !`find api -maxdepth 1 -name "*.slnx" -o -name "*.sln" 2>/dev/null | head -1`

## Usage

```bash
# Basic CRUD
/generate:crud Product --properties "Name:string,Price:decimal,Stock:int"

# With all options
/generate:crud Order --properties "OrderNumber:string,Total:decimal,Status:OrderStatus" --no-docs

# Minimal (infer properties from name)
/generate:crud Category
```

## Execution

Use Task tool with `subagent_type="abp-developer"`, `model="sonnet"`:

```
Generate complete CRUD for {EntityName} in ONE pass.

Properties: {properties or infer from entity name}
Context: Read docs/architecture/README.md, docs/architecture/patterns.md
Skills: Apply abp-framework-patterns, efcore-patterns, fluentvalidation-patterns

## Required Output Files

### 1. Domain.Shared: Enum (if needed)
api/src/{Project}.Domain.Shared/{EntityPlural}/{EntityName}Status.cs

### 2. Domain: Entity
api/src/{Project}.Domain/{EntityPlural}/{EntityName}.cs

Pattern:
- Inherit FullAuditedAggregateRoot<Guid>
- Private setters with SetXxx() methods
- Private parameterless constructor
- Validation in setters

### 3. Application.Contracts: DTOs + Interface
api/src/{Project}.Application.Contracts/{EntityPlural}/
- {EntityName}Dto.cs
- CreateUpdate{EntityName}Dto.cs
- Get{EntityName}ListInput.cs (with Filter property)
- I{EntityName}AppService.cs

### 4. Application: Service + Validator
api/src/{Project}.Application/{EntityPlural}/
- {EntityName}AppService.cs (CRUD with WhereIf filtering)
- CreateUpdate{EntityName}DtoValidator.cs

### 5. EntityFrameworkCore: Configuration
api/src/{Project}.EntityFrameworkCore/{EntityPlural}/{EntityName}Configuration.cs

### 6. Permissions (edit existing files)
- Add {EntityName} constants to {Project}Permissions.cs
- Register in PermissionDefinitionProvider.cs

### 7. DbContext (edit existing)
- Add DbSet<{EntityName}> {EntityPlural}

### 8. Mapperly (edit existing)
- Add mapping methods to ApplicationMappers.cs

## Build Verification
Run: dotnet build api/*.slnx
If build fails, fix errors and retry.
```

## Output

```
## CRUD Generated: {EntityName}

### Files Created
- api/src/{Project}.Domain/{EntityPlural}/{EntityName}.cs
- api/src/{Project}.Application.Contracts/{EntityPlural}/{EntityName}Dto.cs
- api/src/{Project}.Application.Contracts/{EntityPlural}/CreateUpdate{EntityName}Dto.cs
- api/src/{Project}.Application.Contracts/{EntityPlural}/Get{EntityName}ListInput.cs
- api/src/{Project}.Application.Contracts/{EntityPlural}/I{EntityName}AppService.cs
- api/src/{Project}.Application/{EntityPlural}/{EntityName}AppService.cs
- api/src/{Project}.Application/{EntityPlural}/CreateUpdate{EntityName}DtoValidator.cs
- api/src/{Project}.EntityFrameworkCore/{EntityPlural}/{EntityName}Configuration.cs

### Files Modified
- Permissions, PermissionDefinitionProvider, DbContext, ApplicationMappers

### API Endpoints (auto-generated)
- GET    /api/app/{entity}
- GET    /api/app/{entity}/{id}
- POST   /api/app/{entity}
- PUT    /api/app/{entity}/{id}
- DELETE /api/app/{entity}/{id}

### Next Steps
1. /generate:migration Add{EntityName}
2. dotnet run --project api/src/{Project}.DbMigrator
3. Test API via Swagger
```

## Options

| Option | Effect |
|--------|--------|
| `--properties` | Property definitions (Name:type format) |
| `--no-docs` | Skip creating feature documentation |
| `--with-filter` | Generate separate Filter DTO |
| `--audit full` | FullAuditedAggregateRoot (default) |
| `--audit basic` | AuditedAggregateRoot |
| `--audit none` | AggregateRoot |

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
# E-commerce product
/generate:crud Product --properties "Name:string,Description:string?,Price:decimal,Stock:int,CategoryId:Guid,IsActive:bool"

# Simple lookup
/generate:crud Category --properties "Name:string,Description:string?"

# Order with enum
/generate:crud Order --properties "OrderNumber:string,CustomerId:Guid,Total:decimal,Status:OrderStatus,OrderDate:DateTime"
```
