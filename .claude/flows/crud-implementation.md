# Flow: CRUD Entity Implementation

Complete workflow for implementing a new entity with all ABP layers.

## Overview

Creates a fully functional CRUD implementation including:
- Domain entity with validation
- DTOs (read, create/update, list input)
- FluentValidation validators
- AppService with authorization
- EF Core configuration
- Permissions
- Unit tests

## Prerequisites

Before starting:
- [ ] Entity requirements defined (name, properties, relationships)
- [ ] Business rules identified
- [ ] Permission structure planned

## Steps

### Step 1: Domain Modeling

**Apply**: `domain-modeling` skill
**Also read**: `knowledge/entities/base-classes.md`
**Input**: Entity requirements from user
**Output**: Entity definition document

**Actions**:
1. Create entity definition in `docs/domain/entities/{entity}.md`
2. Define properties with types and constraints
3. Document business rules (BR-XXX format)
4. Identify relationships

**Template**:
```markdown
# {Entity} Entity

## Properties
| Property | Type | Required | Constraints |
|----------|------|----------|-------------|
| Name | string | Yes | Max 100 chars |

## Business Rules
- BR-001: {Description}

## Relationships
- Belongs to: {Parent}
- Has many: {Children}
```

---

### Step 2: Constants & Enums

**Apply**: `abp-framework-patterns` skill
**Location**: `{ProjectName}.Domain.Shared/{Feature}/`
**Output**: Constants and enum files

**Create**:
```csharp
// {Entity}Consts.cs
public static class {Entity}Consts
{
    public const int MaxNameLength = 100;
    // ... from entity definition
}

// {Entity}Status.cs (if needed)
public enum {Entity}Status
{
    Active,
    Inactive
}
```

---

### Step 3: Entity Implementation

**Apply**: `abp-framework-patterns` skill (Entity section)
**Also read**: `knowledge/entities/base-classes.md`, `knowledge/entities/audit-properties.md`
**Location**: `{ProjectName}.Domain/{Feature}/`
**Output**: Entity class

**Create**:
```csharp
public class {Entity} : FullAuditedAggregateRoot<Guid>
{
    // Properties with private setters
    // Protected parameterless constructor
    // Public constructor with validation
    // Domain methods
}
```

**Checklist**:
- [ ] Inherits correct base class
- [ ] Uses `Check.NotNullOrWhiteSpace` for validation
- [ ] Private setters for encapsulation
- [ ] Domain methods for state changes

---

### Step 4: DTOs

**Apply**: `abp-framework-patterns` skill (DTO section)
**Location**: `{ProjectName}.Application.Contracts/{Feature}/`
**Output**: DTO classes

**Create**:
1. `{Entity}Dto.cs` - Read DTO (inherits `FullAuditedEntityDto<Guid>`)
2. `CreateUpdate{Entity}Dto.cs` - Write DTO
3. `Get{Entity}ListInput.cs` - List query input (inherits `PagedAndSortedResultRequestDto`)

---

### Step 5: AppService Interface

**Apply**: `abp-framework-patterns` skill (AppService section)
**Location**: `{ProjectName}.Application.Contracts/{Feature}/`
**Output**: Service interface

**Create**:
```csharp
public interface I{Entity}AppService : IApplicationService
{
    Task<{Entity}Dto> GetAsync(Guid id);
    Task<PagedResultDto<{Entity}Dto>> GetListAsync(Get{Entity}ListInput input);
    Task<{Entity}Dto> CreateAsync(CreateUpdate{Entity}Dto input);
    Task<{Entity}Dto> UpdateAsync(Guid id, CreateUpdate{Entity}Dto input);
    Task DeleteAsync(Guid id);
}
```

---

### Step 6: Validation

**Apply**: `fluentvalidation-patterns` skill
**Also read**: `knowledge/examples/validation-chain.md`
**Location**: `{ProjectName}.Application/{Feature}/`
**Output**: Validator class

**Create**:
```csharp
public class CreateUpdate{Entity}DtoValidator : AbstractValidator<CreateUpdate{Entity}Dto>
{
    public CreateUpdate{Entity}DtoValidator()
    {
        // Rules based on entity constraints
    }
}
```

**Checklist**:
- [ ] All required fields have `NotEmpty()`
- [ ] String fields have `MaximumLength()`
- [ ] Email fields have `EmailAddress()`
- [ ] Custom business rule validators

---

### Step 7: Permissions

**Apply**: `openiddict-authorization` skill
**Also read**: `knowledge/conventions/permissions.md`
**Location**: `{ProjectName}.Application.Contracts/Permissions/`
**Output**: Permission constants and provider updates

**Add to** `{ProjectName}Permissions.cs`:
```csharp
public static class {Entity}s
{
    public const string Default = GroupName + ".{Entity}s";
    public const string Create = Default + ".Create";
    public const string Edit = Default + ".Edit";
    public const string Delete = Default + ".Delete";
}
```

**Add to** `{ProjectName}PermissionDefinitionProvider.cs`:
```csharp
var {entity}s = group.AddPermission({ProjectName}Permissions.{Entity}s.Default, L("Permission:{Entity}s"));
{entity}s.AddChild({ProjectName}Permissions.{Entity}s.Create, L("Permission:{Entity}s.Create"));
{entity}s.AddChild({ProjectName}Permissions.{Entity}s.Edit, L("Permission:{Entity}s.Edit"));
{entity}s.AddChild({ProjectName}Permissions.{Entity}s.Delete, L("Permission:{Entity}s.Delete"));
```

---

### Step 8: AppService Implementation

**Apply**: `abp-framework-patterns` skill (AppService section)
**Also read**: `knowledge/patterns/repository.md`
**Location**: `{ProjectName}.Application/{Feature}/`
**Output**: Service implementation

**Create**:
```csharp
[Authorize({ProjectName}Permissions.{Entity}s.Default)]
public class {Entity}AppService : ApplicationService, I{Entity}AppService
{
    // Repository injection
    // CRUD methods with authorization attributes
    // WhereIf pattern for filtering
}
```

**Checklist**:
- [ ] Class-level `[Authorize]` for read
- [ ] Method-level `[Authorize]` for CUD operations
- [ ] Uses `WhereIf` for optional filters
- [ ] Proper pagination with `PageBy()`

---

### Step 9: Object Mapping

**Apply**: `abp-framework-patterns` skill (Mapperly section)
**Location**: `{ProjectName}.Application/{ProjectName}ApplicationMappers.cs`
**Output**: Mapping methods

**Add**:
```csharp
public static partial {Entity}Dto MapToDto(this {Entity} entity);
public static partial List<{Entity}Dto> MapToDtoList(this List<{Entity}> entities);
```

---

### Step 10: EF Core Configuration

**Apply**: `efcore-patterns` skill
**Location**: `{ProjectName}.EntityFrameworkCore/EntityFrameworkCore/`
**Output**: DbContext and entity configuration

**Update DbContext**:
```csharp
public DbSet<{Entity}> {Entity}s { get; set; }
```

**Add Configuration**:
```csharp
builder.Entity<{Entity}>(b =>
{
    b.ToTable("{Entity}s");
    b.ConfigureByConvention();
    // Property configurations
    // Indexes
});
```

---

### Step 11: Migration

**Apply**: `efcore-patterns` skill
**Command**: `dotnet ef migrations add "Added_{Entity}" -p src/{ProjectName}.EntityFrameworkCore -s src/{ProjectName}.HttpApi.Host`

---

### Step 12: Tests

**Apply**: `xunit-testing-patterns` skill
**Also read**: `knowledge/examples/crud-entity.md`
**Location**: `test/{ProjectName}.Application.Tests/{Feature}/`
**Output**: Test class

**Create**:
```csharp
public class {Entity}AppService_Tests : {ProjectName}ApplicationTestBase
{
    // Test CRUD operations
    // Test validation
    // Test authorization
}
```

---

## Skill Chain

```
domain-modeling
       │
       ▼
abp-framework-patterns ──────► Constants, Entity, DTOs, AppService
       │
       ├──► fluentvalidation-patterns (Validation)
       │
       ├──► openiddict-authorization (Permissions)
       │
       └──► efcore-patterns (DbContext, Config)
              │
              ▼
       xunit-testing-patterns (Tests)
```

## Verification Checklist

- [ ] Entity created in Domain layer
- [ ] Constants in Domain.Shared
- [ ] DTOs in Application.Contracts
- [ ] Validator in Application
- [ ] Permissions defined and registered
- [ ] AppService implements interface
- [ ] Mapperly mappings added
- [ ] DbContext updated
- [ ] Migration created
- [ ] Tests pass
- [ ] Build succeeds

## Quick Command

Use `/generate:entity` command for automated scaffolding:
```
/generate:entity {EntityName} --properties "Name:string,Email:string"
```
