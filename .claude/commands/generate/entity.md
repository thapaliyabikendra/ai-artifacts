---
description: Scaffold complete ABP entity with all layers (Entity, DTOs, AppService, Validator)
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <EntityName> [--properties "Name:string,Email:string,DateOfBirth:DateTime"] [--audit full|basic|none]
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
- Read `docs/domain/entities/` for existing entity patterns

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
Audit: {audit-level: full|basic|none}

Skills: Apply abp-framework-patterns, efcore-patterns, fluentvalidation-patterns

## 1. Domain Layer: Entity

Create: api/src/{Project}.Domain/{EntityPlural}/{Entity}.cs

```csharp
public class {Entity} : FullAuditedAggregateRoot<Guid>
{
    // Properties with private setters
    public string Name { get; private set; }

    // Private constructor for EF Core
    private {Entity}() { }

    // Public constructor with validation
    public {Entity}(Guid id, string name) : base(id)
    {
        SetName(name);
    }

    // Encapsulated setters
    public void SetName(string name)
    {
        Name = Check.NotNullOrWhiteSpace(name, nameof(name), maxLength: 100);
    }
}
```

## 2. Application.Contracts: DTOs + Interface

Create: api/src/{Project}.Application.Contracts/{EntityPlural}/

- {Entity}Dto.cs
- CreateUpdate{Entity}Dto.cs
- Get{Entity}ListInput.cs
- I{Entity}AppService.cs

## 3. Application: AppService + Validator

Create: api/src/{Project}.Application/{EntityPlural}/

- {Entity}AppService.cs (with CRUD + authorization)
- CreateUpdate{Entity}DtoValidator.cs (FluentValidation)

## 4. EntityFrameworkCore: DbContext

Edit: api/src/{Project}.EntityFrameworkCore/.../DbContext.cs
- Add DbSet<{Entity}> {EntityPlural}

Edit: OnModelCreating
- Add entity configuration

## 5. Permissions

Edit: api/src/{Project}.Application.Contracts/Permissions/
- Add {Entity} permission constants
- Register in PermissionDefinitionProvider

## Output Files

```
api/src/
├── {Project}.Domain/{EntityPlural}/
│   └── {Entity}.cs
├── {Project}.Application.Contracts/{EntityPlural}/
│   ├── {Entity}Dto.cs
│   ├── CreateUpdate{Entity}Dto.cs
│   ├── Get{Entity}ListInput.cs
│   └── I{Entity}AppService.cs
├── {Project}.Application/{EntityPlural}/
│   ├── {Entity}AppService.cs
│   └── CreateUpdate{Entity}DtoValidator.cs
└── {Project}.EntityFrameworkCore/
    └── (DbContext updated)
```
```

## Checkpoint

After generation:
- [ ] Entity created with proper encapsulation
- [ ] DTOs created with validation attributes
- [ ] AppService implements CRUD with authorization
- [ ] Validator uses FluentValidation
- [ ] DbSet added to DbContext
- [ ] Permissions defined
- [ ] Build succeeds: `dotnet build api/*.slnx`

## Next Steps

```
1. Run: /generate:migration Add{Entity}
2. Review migration
3. Apply: Run DbMigrator
4. Test: dotnet test api/test/*.Application.Tests
```

## Options

| Option | Effect |
|--------|--------|
| `--properties` | Property definitions (Name:type format) |
| `--audit full` | FullAuditedAggregateRoot (default) |
| `--audit basic` | AuditedAggregateRoot |
| `--audit none` | AggregateRoot |
| `--no-validator` | Skip FluentValidation validator |
| `--no-permissions` | Skip permission scaffolding |
| `--with-filter` | Generate accompanying Filter DTO for list queries |
| `--with-response-wrapper` | Use ResponseModel wrapper in AppService methods |

## Examples

```bash
# Basic entity
/generate:entity Product

# With properties
/generate:entity Product --properties "Name:string,Price:decimal,Stock:int,IsActive:bool"

# Without soft delete
/generate:entity AuditLog --audit basic

# With filter DTO for advanced querying
/generate:entity Product --properties "Name:string,Price:decimal,CategoryId:Guid?" --with-filter

# With response wrapper pattern
/generate:entity Order --properties "OrderNumber:string,Total:decimal,Status:OrderStatus" --with-response-wrapper
```

## Filter DTO Generation (--with-filter)

When `--with-filter` is specified, generate an additional filter class:

```csharp
// Application.Contracts/{EntityPlural}/{Entity}Filter.cs
public class {Entity}Filter
{
    // For each string property: contains search
    public string? {StringProperty} { get; set; }

    // For each Guid property: exact match
    public Guid? {GuidProperty} { get; set; }

    // For each bool property: exact match
    public bool? {BoolProperty} { get; set; }

    // For each DateTime property: range
    public DateTime? {DateProperty}From { get; set; }
    public DateTime? {DateProperty}To { get; set; }

    // For each numeric property: range
    public decimal? {NumericProperty}Min { get; set; }
    public decimal? {NumericProperty}Max { get; set; }

    // Standard audit filters
    public DateTime? CreatedAfter { get; set; }
    public DateTime? CreatedBefore { get; set; }
}
```

Update AppService interface:
```csharp
Task<PagedResultDto<{Entity}Dto>> GetListAsync(
    PagedAndSortedResultRequestDto input,
    {Entity}Filter filter);
```

Update AppService implementation with WhereIf pattern:
```csharp
public async Task<PagedResultDto<{Entity}Dto>> GetListAsync(
    PagedAndSortedResultRequestDto input,
    {Entity}Filter filter)
{
    var queryable = await _repository.GetQueryableAsync();

    var query = queryable
        .WhereIf(!filter.Name.IsNullOrWhiteSpace(),
            x => x.Name.ToLower().Contains(filter.Name.ToLower()))
        .WhereIf(filter.CategoryId.HasValue,
            x => x.CategoryId == filter.CategoryId)
        .WhereIf(filter.CreatedAfter.HasValue,
            x => x.CreationTime >= filter.CreatedAfter.Value);

    // ... rest of implementation
}
```
