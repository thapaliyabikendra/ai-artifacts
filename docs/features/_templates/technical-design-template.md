# Technical Design: {{Feature Name}}

**Created**: {{Date}}
**Author**: backend-architect
**Status**: Draft | Review | Approved
**Requirements Doc**: [requirements.md](./requirements.md)

---

## 1. Architecture Overview

### 1.1 Solution Structure

```
api/src/
├── {{ProjectName}}.Domain/
│   └── {{Feature}}/
│       ├── {{Entity}}.cs
│       └── {{Entity}}Manager.cs (if needed)
│
├── {{ProjectName}}.Application.Contracts/
│   └── {{Feature}}/
│       ├── I{{Entity}}AppService.cs
│       ├── {{Entity}}Dto.cs
│       ├── CreateUpdate{{Entity}}Dto.cs
│       └── Get{{Entity}}ListInput.cs
│
├── {{ProjectName}}.Application/
│   └── {{Feature}}/
│       ├── {{Entity}}AppService.cs
│       └── {{Entity}}DtoValidator.cs
│
└── {{ProjectName}}.EntityFrameworkCore/
    └── EntityFrameworkCore/
        └── (DbContext configuration)
```

### 1.2 Dependencies
- {{Dependency 1}}
- {{Dependency 2}}

---

## 2. Entity Design

### 2.1 {{Entity}} Entity

```csharp
using Volo.Abp.Domain.Entities.Auditing;

namespace {{ProjectName}}.{{Feature}};

/// <summary>
/// {{Entity description}}
/// </summary>
public class {{Entity}} : FullAuditedAggregateRoot<Guid>
{
    /// <summary>
    /// {{Property description}}
    /// </summary>
    public string {{Property}} { get; private set; } = string.Empty;

    // Add more properties...

    /// <summary>
    /// Private constructor for EF Core
    /// </summary>
    private {{Entity}}() { }

    /// <summary>
    /// Creates a new {{Entity}} instance
    /// </summary>
    public {{Entity}}(
        Guid id,
        string {{property}})
        : base(id)
    {
        Set{{Property}}({{property}});
    }

    /// <summary>
    /// Sets the {{property}} with validation
    /// </summary>
    public void Set{{Property}}(string {{property}})
    {
        {{Property}} = Check.NotNullOrWhiteSpace({{property}}, nameof({{property}}), maxLength: 100);
    }
}
```

### 2.2 Constants

```csharp
namespace {{ProjectName}}.{{Feature}};

public static class {{Entity}}Consts
{
    public const int Max{{Property}}Length = 100;
    // Add more constants...
}
```

---

## 3. DTO Design

### 3.1 {{Entity}}Dto (Output)

```csharp
using Volo.Abp.Application.Dtos;

namespace {{ProjectName}}.{{Feature}};

public class {{Entity}}Dto : FullAuditedEntityDto<Guid>
{
    public string {{Property}} { get; set; } = string.Empty;
    // Add more properties...
}
```

### 3.2 CreateUpdate{{Entity}}Dto (Input)

```csharp
namespace {{ProjectName}}.{{Feature}};

public class CreateUpdate{{Entity}}Dto
{
    public string {{Property}} { get; set; } = string.Empty;
    // Add more properties...
}
```

### 3.3 Get{{Entity}}ListInput (Query)

```csharp
using Volo.Abp.Application.Dtos;

namespace {{ProjectName}}.{{Feature}};

public class Get{{Entity}}ListInput : PagedAndSortedResultRequestDto
{
    public string? Filter { get; set; }
    // Add more filter properties...
}
```

---

## 4. Application Service Interface

```csharp
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;

namespace {{ProjectName}}.{{Feature}};

public interface I{{Entity}}AppService : IApplicationService
{
    /// <summary>
    /// Gets a single {{entity}} by ID
    /// </summary>
    Task<{{Entity}}Dto> GetAsync(Guid id);

    /// <summary>
    /// Gets a paged list of {{entities}}
    /// </summary>
    Task<PagedResultDto<{{Entity}}Dto>> GetListAsync(Get{{Entity}}ListInput input);

    /// <summary>
    /// Creates a new {{entity}}
    /// </summary>
    Task<{{Entity}}Dto> CreateAsync(CreateUpdate{{Entity}}Dto input);

    /// <summary>
    /// Updates an existing {{entity}}
    /// </summary>
    Task<{{Entity}}Dto> UpdateAsync(Guid id, CreateUpdate{{Entity}}Dto input);

    /// <summary>
    /// Deletes a {{entity}} (soft delete)
    /// </summary>
    Task DeleteAsync(Guid id);
}
```

---

## 5. Permissions

### 5.1 Permission Constants

```csharp
namespace {{ProjectName}}.Permissions;

public static partial class {{ProjectName}}Permissions
{
    public static class {{Feature}}
    {
        public const string Default = GroupName + ".{{Feature}}";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
    }
}
```

### 5.2 Permission Definitions

```csharp
// In {{ProjectName}}PermissionDefinitionProvider.cs

var {{feature}}Permission = myGroup.AddPermission(
    {{ProjectName}}Permissions.{{Feature}}.Default,
    L("Permission:{{Feature}}"));

{{feature}}Permission.AddChild(
    {{ProjectName}}Permissions.{{Feature}}.Create,
    L("Permission:{{Feature}}.Create"));

{{feature}}Permission.AddChild(
    {{ProjectName}}Permissions.{{Feature}}.Edit,
    L("Permission:{{Feature}}.Edit"));

{{feature}}Permission.AddChild(
    {{ProjectName}}Permissions.{{Feature}}.Delete,
    L("Permission:{{Feature}}.Delete"));
```

### 5.3 Role Permission Matrix

| Role | Default | Create | Edit | Delete |
|------|---------|--------|------|--------|
| Admin | ✅ | ✅ | ✅ | ✅ |
| {{Role}} | ✅ | ✅ | ✅ | ❌ |
| {{Role}} | ✅ | ❌ | ❌ | ❌ |

---

## 6. API Endpoints

| Method | Route | Description | Permission | Request | Response |
|--------|-------|-------------|------------|---------|----------|
| GET | /api/app/{{entities}} | List {{entities}} | Default | Get{{Entity}}ListInput | PagedResultDto<{{Entity}}Dto> |
| GET | /api/app/{{entities}}/{id} | Get {{entity}} | Default | Guid | {{Entity}}Dto |
| POST | /api/app/{{entities}} | Create {{entity}} | Create | CreateUpdate{{Entity}}Dto | {{Entity}}Dto |
| PUT | /api/app/{{entities}}/{id} | Update {{entity}} | Edit | CreateUpdate{{Entity}}Dto | {{Entity}}Dto |
| DELETE | /api/app/{{entities}}/{id} | Delete {{entity}} | Delete | Guid | - |

---

## 7. Database Schema

### 7.1 Table: {{TableName}}

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| Id | uuid | PK, NOT NULL | Primary key |
| {{Column}} | varchar(100) | NOT NULL | {{Description}} |
| CreationTime | timestamp | NOT NULL | ABP audit field |
| CreatorId | uuid | NULL | ABP audit field |
| LastModificationTime | timestamp | NULL | ABP audit field |
| LastModifierId | uuid | NULL | ABP audit field |
| IsDeleted | boolean | NOT NULL, DEFAULT false | Soft delete |
| DeletionTime | timestamp | NULL | ABP audit field |
| DeleterId | uuid | NULL | ABP audit field |

### 7.2 Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| IX_{{Table}}_{{Column}} | {{Column}} | BTREE | {{Purpose}} |

### 7.3 Foreign Keys

| FK Name | Column | References | On Delete |
|---------|--------|------------|-----------|
| FK_{{Table}}_{{Column}} | {{Column}} | {{Table}}(Id) | RESTRICT / CASCADE |

---

## 8. Validation Rules

### 8.1 FluentValidation

```csharp
using FluentValidation;

namespace {{ProjectName}}.{{Feature}};

public class CreateUpdate{{Entity}}DtoValidator : AbstractValidator<CreateUpdate{{Entity}}Dto>
{
    public CreateUpdate{{Entity}}DtoValidator()
    {
        RuleFor(x => x.{{Property}})
            .NotEmpty()
            .MaximumLength({{Entity}}Consts.Max{{Property}}Length);

        // Add more rules based on business requirements...
    }
}
```

---

## 9. Domain Services (If Needed)

### 9.1 {{Entity}}Manager

```csharp
using Volo.Abp.Domain.Services;

namespace {{ProjectName}}.{{Feature}};

public class {{Entity}}Manager : DomainService
{
    private readonly IRepository<{{Entity}}, Guid> _repository;

    public {{Entity}}Manager(IRepository<{{Entity}}, Guid> repository)
    {
        _repository = repository;
    }

    /// <summary>
    /// {{Business logic description}}
    /// </summary>
    public async Task<{{Entity}}> {{BusinessMethod}}Async(/*params*/)
    {
        // Complex business logic here
    }
}
```

---

## 10. AutoMapper Configuration

```csharp
// In {{ProjectName}}ApplicationAutoMapperProfile.cs

CreateMap<{{Entity}}, {{Entity}}Dto>();
// CreateMap<CreateUpdate{{Entity}}Dto, {{Entity}}>(); // Only if needed
```

---

## 11. EF Core Configuration

```csharp
// In {{ProjectName}}DbContextModelCreatingExtensions.cs

builder.Entity<{{Entity}}>(b =>
{
    b.ToTable({{ProjectName}}Consts.DbTablePrefix + "{{TableName}}", {{ProjectName}}Consts.DbSchema);
    b.ConfigureByConvention();

    b.Property(x => x.{{Property}})
        .HasMaxLength({{Entity}}Consts.Max{{Property}}Length)
        .IsRequired();

    // Add indexes
    b.HasIndex(x => x.{{Property}});

    // Add relationships
    // b.HasOne<{{RelatedEntity}}>()...
});
```

---

## 12. Migration Command

```bash
dotnet ef migrations add Add{{Feature}} \
    -p api/src/{{ProjectName}}.EntityFrameworkCore \
    -s api/src/{{ProjectName}}.DbMigrator
```

---

## 13. Implementation Notes

### 13.1 Considerations
- {{Consideration 1}}
- {{Consideration 2}}

### 13.2 Performance Optimizations
- {{Optimization 1}}
- {{Optimization 2}}

### 13.3 Security Considerations
- {{Security note 1}}
- {{Security note 2}}
