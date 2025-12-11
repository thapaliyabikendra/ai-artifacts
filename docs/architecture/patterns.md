# Code Patterns and Conventions

> **Purpose**: Coding patterns, naming conventions, and best practices for the Clinic Management System.
> **Maintained By**: `backend-architect` agent

## Entity Patterns

### Base Class

All domain entities inherit from:

```csharp
FullAuditedAggregateRoot<Guid>
```

Provides:
- Soft delete: `IsDeleted`, `DeletionTime`, `DeleterId`
- Audit: `CreationTime`, `CreatorId`, `LastModificationTime`, `LastModifierId`
- Concurrency: `ConcurrencyStamp`

### Entity Structure

```csharp
public class {Entity} : FullAuditedAggregateRoot<Guid>
{
    // Properties with private setters
    public string Name { get; private set; } = string.Empty;

    // EF Core constructor
    private {Entity}() { }

    // Public constructor with validation
    public {Entity}(Guid id, string name) : base(id)
    {
        SetName(name);
    }

    // Setter methods with validation
    public void SetName(string name)
    {
        Name = Check.NotNullOrWhiteSpace(name, nameof(name), maxLength: 100);
    }
}
```

## Naming Conventions

### DTOs

| Type | Pattern | Example |
|------|---------|---------|
| Output | `{Entity}Dto` | `DoctorDto` |
| Create/Update | `CreateUpdate{Entity}Dto` | `CreateUpdateDoctorDto` |
| List Input | `Get{Entity}ListInput` | `GetDoctorListInput` |

### AppServices

| Type | Pattern | Example |
|------|---------|---------|
| Interface | `I{Entity}AppService` | `IDoctorAppService` |
| Implementation | `{Entity}AppService` | `DoctorAppService` |

### Permissions

```
ClinicManagementSystem.{Resource}.{Action}
```

Example:
- `ClinicManagementSystem.Doctors` (view)
- `ClinicManagementSystem.Doctors.Create`
- `ClinicManagementSystem.Doctors.Edit`
- `ClinicManagementSystem.Doctors.Delete`

### Tests

| Type | Pattern | Example |
|------|---------|---------|
| Test Class | `{Entity}AppService_Tests` | `DoctorAppService_Tests` |
| Test Data | `{Entity}TestData` | `DoctorTestData` |
| Test Seeder | `{Entity}TestDataSeedContributor` | `DoctorTestDataSeedContributor` |

## AppService Patterns

### Standard CRUD

```csharp
[Authorize(Permissions.{Feature}.Default)]
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

        return new PagedResultDto<{Entity}Dto>(totalCount,
            ObjectMapper.Map<List<{Entity}>, List<{Entity}Dto>>(items));
    }

    [Authorize(Permissions.{Feature}.Create)]
    public async Task<{Entity}Dto> CreateAsync(CreateUpdate{Entity}Dto input)
    {
        var entity = new {Entity}(GuidGenerator.Create(), input.Name);
        await _repository.InsertAsync(entity);
        _logger.LogInformation("Created {Entity} {Id}", entity.Id);
        return ObjectMapper.Map<{Entity}, {Entity}Dto>(entity);
    }

    [Authorize(Permissions.{Feature}.Edit)]
    public async Task<{Entity}Dto> UpdateAsync(Guid id, CreateUpdate{Entity}Dto input)
    {
        var entity = await _repository.GetAsync(id);
        entity.SetName(input.Name);
        await _repository.UpdateAsync(entity);
        return ObjectMapper.Map<{Entity}, {Entity}Dto>(entity);
    }

    [Authorize(Permissions.{Feature}.Delete)]
    public async Task DeleteAsync(Guid id)
    {
        await _repository.DeleteAsync(id);
        _logger.LogInformation("Deleted {Entity} {Id}", id);
    }
}
```

## Validation Patterns

### FluentValidation

```csharp
public class CreateUpdate{Entity}DtoValidator : AbstractValidator<CreateUpdate{Entity}Dto>
{
    public CreateUpdate{Entity}DtoValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required.")
            .MaximumLength(100).WithMessage("Name cannot exceed 100 characters.");

        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email is required.")
            .EmailAddress().WithMessage("Invalid email format.");
    }
}
```

## Testing Patterns

### Test Structure

```csharp
public class {Entity}AppService_Tests : ApplicationTestBase
{
    private readonly I{Entity}AppService _service;

    public {Entity}AppService_Tests()
    {
        _service = GetRequiredService<I{Entity}AppService>();
    }

    [Fact]
    public async Task Should_Get_{Entity}_By_Id()
    {
        // Arrange
        var id = {Entity}TestData.{Entity}1Id;

        // Act
        var result = await _service.GetAsync(id);

        // Assert
        result.ShouldNotBeNull();
        result.Id.ShouldBe(id);
    }
}
```

## Libraries

| Library | Purpose |
|---------|---------|
| FluentValidation | Input validation |
| AutoMapper | Object mapping |
| xUnit | Testing |
| Shouldly | Assertions |
| NSubstitute | Mocking |
