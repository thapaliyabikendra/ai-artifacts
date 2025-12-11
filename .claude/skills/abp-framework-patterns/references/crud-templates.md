# CRUD Service Templates

Code templates for generating ABP Framework CRUD services.

## Table of Contents

- [Entity Template](#entity-template)
- [AppService Interface](#appservice-interface)
- [AppService Implementation](#appservice-implementation)
- [DTO Templates](#dto-templates)
- [FluentValidation Template](#fluentvalidation-template)
- [Permission Template](#permission-template)
- [AutoMapper Profile](#automapper-profile)
- [Placeholder Reference](#placeholder-reference)

---

## Entity Template

File: `{ProjectName}.Domain/{Feature}/{Entity}.cs`

```csharp
using Volo.Abp;
using Volo.Abp.Domain.Entities.Auditing;

namespace {ProjectName}.{Feature};

public class {Entity} : FullAuditedAggregateRoot<Guid>
{
    public string Name { get; private set; } = string.Empty;
    // Add properties from requirements

    private {Entity}() { } // EF Core constructor

    public {Entity}(
        Guid id,
        string name)
        : base(id)
    {
        SetName(name);
    }

    public void SetName(string name)
    {
        Name = Check.NotNullOrWhiteSpace(name, nameof(name), maxLength: 100);
    }
}
```

---

## AppService Interface

File: `{ProjectName}.Application.Contracts/{Feature}/I{Entity}AppService.cs`

```csharp
using System;
using System.Threading.Tasks;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;

namespace {ProjectName}.{Feature};

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

## AppService Implementation

File: `{ProjectName}.Application/{Feature}/{Entity}AppService.cs`

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Dynamic.Core;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Logging;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;

namespace {ProjectName}.{Feature};

[Authorize({ProjectName}Permissions.{Feature}.Default)]
public class {Entity}AppService : ApplicationService, I{Entity}AppService
{
    private readonly IRepository<{Entity}, Guid> _repository;
    private readonly ILogger<{Entity}AppService> _logger;

    public {Entity}AppService(
        IRepository<{Entity}, Guid> repository,
        ILogger<{Entity}AppService> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public async Task<{Entity}Dto> GetAsync(Guid id)
    {
        var entity = await _repository.GetAsync(id);
        return ObjectMapper.Map<{Entity}, {Entity}Dto>(entity);
    }

    public async Task<PagedResultDto<{Entity}Dto>> GetListAsync(Get{Entity}ListInput input)
    {
        var queryable = await _repository.GetQueryableAsync();

        queryable = queryable
            .WhereIf(!input.Filter.IsNullOrWhiteSpace(),
                x => x.Name.Contains(input.Filter!))
            .OrderBy(input.Sorting ?? nameof({Entity}.Name));

        var totalCount = await AsyncExecuter.CountAsync(queryable);
        var items = await AsyncExecuter.ToListAsync(
            queryable.PageBy(input.SkipCount, input.MaxResultCount));

        _logger.LogInformation("Retrieved {Count} {Entity} records", items.Count);

        return new PagedResultDto<{Entity}Dto>(
            totalCount,
            ObjectMapper.Map<List<{Entity}>, List<{Entity}Dto>>(items));
    }

    [Authorize({ProjectName}Permissions.{Feature}.Create)]
    public async Task<{Entity}Dto> CreateAsync(CreateUpdate{Entity}Dto input)
    {
        var entity = new {Entity}(
            GuidGenerator.Create(),
            input.Name);

        await _repository.InsertAsync(entity);

        _logger.LogInformation("Created {Entity} {Id}: {Name}",
            entity.Id, entity.Name);

        return ObjectMapper.Map<{Entity}, {Entity}Dto>(entity);
    }

    [Authorize({ProjectName}Permissions.{Feature}.Edit)]
    public async Task<{Entity}Dto> UpdateAsync(Guid id, CreateUpdate{Entity}Dto input)
    {
        var entity = await _repository.GetAsync(id);

        entity.SetName(input.Name);

        await _repository.UpdateAsync(entity);

        _logger.LogInformation("Updated {Entity} {Id}", id);

        return ObjectMapper.Map<{Entity}, {Entity}Dto>(entity);
    }

    [Authorize({ProjectName}Permissions.{Feature}.Delete)]
    public async Task DeleteAsync(Guid id)
    {
        await _repository.DeleteAsync(id);

        _logger.LogInformation("Deleted {Entity} {Id}", id);
    }
}
```

---

## DTO Templates

### EntityDto

File: `{ProjectName}.Application.Contracts/{Feature}/{Entity}Dto.cs`

```csharp
using System;
using Volo.Abp.Application.Dtos;

namespace {ProjectName}.{Feature};

public class {Entity}Dto : EntityDto<Guid>
{
    public string Name { get; set; } = string.Empty;
    // Add properties matching entity
}
```

### CreateUpdateDto

File: `{ProjectName}.Application.Contracts/{Feature}/CreateUpdate{Entity}Dto.cs`

```csharp
namespace {ProjectName}.{Feature};

public class CreateUpdate{Entity}Dto
{
    public string Name { get; set; } = string.Empty;
    // Add input properties (exclude Id)
}
```

### GetListInput

File: `{ProjectName}.Application.Contracts/{Feature}/Get{Entity}ListInput.cs`

```csharp
using Volo.Abp.Application.Dtos;

namespace {ProjectName}.{Feature};

public class Get{Entity}ListInput : PagedAndSortedResultRequestDto
{
    public string? Filter { get; set; }
    // Add filter properties based on entity fields
}
```

---

## FluentValidation Template

File: `{ProjectName}.Application/{Feature}/{Entity}DtoValidator.cs`

```csharp
using FluentValidation;

namespace {ProjectName}.{Feature};

public class CreateUpdate{Entity}DtoValidator : AbstractValidator<CreateUpdate{Entity}Dto>
{
    public CreateUpdate{Entity}DtoValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required.")
            .MaximumLength(100).WithMessage("Name cannot exceed 100 characters.");

        // Add validation rules based on business requirements
    }
}
```

### Common Validation Patterns

```csharp
// String - required with max length
RuleFor(x => x.Name)
    .NotEmpty().WithMessage("{PropertyName} is required.")
    .MaximumLength(100).WithMessage("{PropertyName} cannot exceed 100 characters.");

// Email
RuleFor(x => x.Email)
    .NotEmpty().WithMessage("Email is required.")
    .EmailAddress().WithMessage("Invalid email format.")
    .MaximumLength(255);

// Phone - optional
RuleFor(x => x.Phone)
    .MaximumLength(20)
    .Matches(@"^\+?[\d\s\-()]+$").WithMessage("Invalid phone format.")
    .When(x => !string.IsNullOrEmpty(x.Phone));

// Date range
RuleFor(x => x.StartDate)
    .NotEmpty().WithMessage("Start date is required.")
    .LessThan(x => x.EndDate).WithMessage("Start date must be before end date.")
    .When(x => x.EndDate.HasValue);

// Numeric range
RuleFor(x => x.Price)
    .GreaterThan(0).WithMessage("Price must be greater than zero.");

// Guid - foreign key
RuleFor(x => x.CategoryId)
    .NotEmpty().WithMessage("Category is required.");
```

---

## Permission Template

File: `{ProjectName}.Application.Contracts/Permissions/{ProjectName}Permissions.cs`

```csharp
namespace {ProjectName}.Permissions;

public static class {ProjectName}Permissions
{
    public const string GroupName = "{ProjectName}";

    public static class {Feature}
    {
        public const string Default = GroupName + ".{Feature}";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
    }

    // Add more features as defined in requirements
}
```

### Permission Definition Provider

File: `{ProjectName}.Application.Contracts/Permissions/{ProjectName}PermissionDefinitionProvider.cs`

```csharp
using Volo.Abp.Authorization.Permissions;
using Volo.Abp.Localization;

namespace {ProjectName}.Permissions;

public class {ProjectName}PermissionDefinitionProvider : PermissionDefinitionProvider
{
    public override void Define(IPermissionDefinitionContext context)
    {
        var group = context.AddGroup({ProjectName}Permissions.GroupName);

        var {entityName}Permission = group.AddPermission(
            {ProjectName}Permissions.{Feature}.Default,
            L("Permission:{Feature}"));

        {entityName}Permission.AddChild(
            {ProjectName}Permissions.{Feature}.Create,
            L("Permission:{Feature}.Create"));

        {entityName}Permission.AddChild(
            {ProjectName}Permissions.{Feature}.Edit,
            L("Permission:{Feature}.Edit"));

        {entityName}Permission.AddChild(
            {ProjectName}Permissions.{Feature}.Delete,
            L("Permission:{Feature}.Delete"));
    }

    private static LocalizableString L(string name)
    {
        return LocalizableString.Create<{ProjectName}Resource>(name);
    }
}
```

---

## AutoMapper Profile

File: `{ProjectName}.Application/{ProjectName}ApplicationAutoMapperProfile.cs`

```csharp
using AutoMapper;

namespace {ProjectName};

public class {ProjectName}ApplicationAutoMapperProfile : Profile
{
    public {ProjectName}ApplicationAutoMapperProfile()
    {
        CreateMap<{Entity}, {Entity}Dto>();
        // Add mappings for all entities
    }
}
```

---

## Placeholder Reference

| Placeholder | Format | Example |
|-------------|--------|---------|
| `{ProjectName}` | PascalCase | ClinicManagementSystem |
| `{Feature}` | PascalCase plural | Doctors |
| `{Entity}` | PascalCase singular | Doctor |
| `{entityName}` | camelCase singular | doctor |

---

## Post-Generation Checklist

1. [ ] Register validator in module's `ConfigureServices`
2. [ ] Add entity to DbContext DbSet
3. [ ] Configure entity in `OnModelCreating`
4. [ ] Add AutoMapper mappings
5. [ ] Add permissions to PermissionDefinitionProvider
6. [ ] Add localization strings
7. [ ] Create migration: `dotnet ef migrations add Add{Entity}`
8. [ ] Run tests: `dotnet test`
