---
name: crud-generator
description: "Generate complete CRUD application services for ABP Framework following DDD patterns. Creates interface in Contracts layer, implementation in AppServices, and DTOs in Contracts. Use when: (1) creating new entity services, (2) scaffolding CRUD operations, (3) implementing standard ABP service patterns, (4) accelerating feature development."
layer: 2
tech_stack: [dotnet, csharp, abp, entityframework]
topics: [crud, scaffolding, code-generation, ddd, repository-pattern]
depends_on: [abp-framework-patterns, entity-framework-core]
complements: [unit-testing-patterns, integration-testing-patterns]
keywords: [CreateAsync, GetAsync, GetListAsync, UpdateAsync, DeleteAsync, ActivateAsync, DeactivateAsync, BulkImportAsync, ExportAsync, AppService, DTO, CRUD, scaffold]
---

# ABP CRUD Service Generator (Project-Agnostic)

Generates complete, production-ready CRUD application services following ABP Framework best practices and DDD patterns. This skill is **framework-agnostic** and works with any ABP-based project.

## When to Use

- Creating a new entity service from scratch in any ABP project
- Scaffolding standard CRUD operations quickly
- Ensuring consistency with existing service patterns
- Implementing reference-based service architecture
- Accelerating feature development with proven templates
- **Interface-first development** (generate implementation after interface exists)

## What Gets Generated

The skill generates **files in two separate layers** following standard ABP architecture:

### Contracts Layer (`{Project}.Application.Contracts/`)

The **interface** and **DTOs** are generated in the Contracts project. This layer is shared between server and client.

#### 1. Interface (`I{EntityName}AppService.cs`)

```csharp
using System;
using System.Threading.Tasks;
using {Project}.Dtos; // Adjust based on your project's DTO namespace
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;

namespace {Project}.Application.Contracts.{PluralEntityName};

public interface I{EntityName}AppService : IApplicationService
{
    Task<ResponseDataDto<object>> CreateAsync(CreateUpdate{EntityName}Dto input);
    Task<ResponseDataDto<object>> UpdateAsync(Guid id, CreateUpdate{EntityName}Dto input);
    Task<ResponseDataDto<object>> DeleteAsync(Guid id);
    Task<ResponseDataDto<{EntityName}Dto>> GetAsync(Guid id);
    Task<ResponseDataDto<PagedResultDto<{EntityName}Dto>>> GetListAsync(PagedAndSortedResultRequestDto input, {EntityName}Filter filter);
    Task<ResponseDataDto<object>> ActivateAsync(Guid id);          // If hasIsActive=true
    Task<ResponseDataDto<object>> DeactivateAsync(Guid id);       // If hasIsActive=true
    Task<ResponseDataDto<object>> ManageConfigAsync(ManageConfigDto input); // If hasConfig=true
    Task<ResponseDataDto<object>> BulkImportAsync([FromForm] BulkImportFileDto input); // If needsBulkImport=true
    Task<ResponseDataDto<ExportFileBlobDto>> ExportAsync({EntityName}Filter filter); // If needsBulkImport=true
    Task<ResponseDataDto<DropDownDto[]>> Get{EntityName}sAsync();
}
```

**Note**: Adjust the `using` statements and namespace to match your project conventions.

#### 2. DTOs (`{EntityName}Dtos.cs`)

All required DTO classes:
- `{EntityName}Dto` - Response DTO (extends `EntityDto<Guid>` or plain class)
- `CreateUpdate{EntityName}Dto` - Input for create/update with validation attributes
- `{EntityName}Filter` - Filter and pagination (extends `PagedAndSortedResultRequestDto`)
- `{EntityName}ExportDto` - For export operations
- `ManageConfigDto` - If `hasConfig=true`
- `{EntityName}ImportDto` - If `needsBulkImport=true`

### Application Layer (`{Project}.Application/AppServices/`)

#### 3. Implementation (`{EntityName}AppService.cs`)

Complete implementation with:
- Constructor injection of all dependencies
- Full CRUD methods with try-catch and structured logging
- Validation methods (`ValidateInputAsync`, etc.)
- Optional activation/deactivation methods with business rules
- Optional config management
- Optional bulk import/export with validation
- Helper methods (`Get{EntityName}Async`, etc.)

# ABP CRUD Service Generator

Generates complete, production-ready CRUD application services following ABP Framework best practices and DDD patterns.

## When to Use

- Creating a new entity service from scratch
- Scaffolding standard CRUD operations quickly
- Ensuring consistency with existing service patterns
- Implementing reference-based service architecture
- Accelerating feature development with proven templates
- **Interface-first development** (generate implementation after interface exists)

## What Gets Generated

The skill generates **files in two separate layers** following standard ABP architecture:

### Contracts Layer (`{Project}.Application.Contracts/`)

The **interface** and **DTOs** are generated in the Contracts project. This layer is shared between server and client.

#### 1. Interface (`I{EntityName}AppService.cs`)

```csharp
public interface I{EntityName}AppService : IApplicationService
{
    Task<ResponseDataDto<object>> CreateAsync(CreateUpdate{EntityName}Dto input);
    Task<ResponseDataDto<object>> UpdateAsync(Guid id, CreateUpdate{EntityName}Dto input);
    Task<ResponseDataDto<object>> DeleteAsync(Guid id);
    Task<ResponseDataDto<{EntityName}Dto>> GetAsync(Guid id);
    Task<ResponseDataDto<PagedResultDto<{EntityName}Dto>>> GetListAsync(PagedAndSortedResultRequestDto input, {EntityName}Filter filter);
    Task<ResponseDataDto<object>> ActivateAsync(Guid id);          // If hasIsActive=true
    Task<ResponseDataDto<object>> DeactivateAsync(Guid id);       // If hasIsActive=true
    Task<ResponseDataDto<object>> ManageConfigAsync(ManageConfigDto input); // If hasConfig=true
    Task<ResponseDataDto<object>> BulkImportAsync([FromForm] BulkImportFileDto input); // If needsBulkImport=true
    Task<ResponseDataDto<ExportFileBlobDto>> ExportAsync({EntityName}Filter filter); // If needsBulkImport=true
    Task<ResponseDataDto<DropDownDto[]>> Get{EntityName}sAsync();
}
```

#### 2. DTOs (`{EntityName}Dtos.cs`)

All required DTO classes:
- `{EntityName}Dto` - Response DTO (extends EntityDto<Guid>)
- `CreateUpdate{EntityName}Dto` - Input for create/update
- `{EntityName}Filter` - Filter and pagination
- `{EntityName}ExportDto` - For export operations
- `ManageConfigDto` - If hasConfig=true
- `{EntityName}ImportDto` - If needsBulkImport=true

### Application Layer (`{Project}.Application/AppServices/`)

#### 3. Implementation (`{EntityName}AppService.cs`)

Complete implementation with:
- Constructor injection of all dependencies
- Full CRUD methods with try-catch and logging
- Validation methods (ValidateInput, ValidateDeletion, etc.)
- Optional activation/deactivation methods
- Optional config management
- Optional bulk import/export
- Helper methods (Get{EntityName}Async, BulkImportAsync)

## Usage

```
/crud-generator EntityName [options]
```

### Required Argument

- **EntityName**: PascalCase singular entity name (e.g., `User`, `Product`, `Department`)

### Options (key=value pairs, comma-separated)

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `hasIsActive` | `true` \| `false` | `true` | Include Activate/Deactivate methods |
| `hasConfig` | `true` \| `false` | `false` | Generate config management methods |
| `needsBulkImport` | `true` \| `false` | `false` | Include Export and BulkImport methods |
| `permission` | string | EntityName | Base permission name (e.g., `ApiClients`, `Users`) |
| `contractsNamespace` | string | `{RootNamespace}.Application.Contracts.{PluralEntityName}` | Namespace for interface & DTOs |
| `appServiceNamespace` | string | `{RootNamespace}.Application.AppServices.{PluralEntityName}` | Namespace for implementation |
| `dtoSuffix` | `Dto` \| `Input` \| custom | `Dto` | Suffix for DTO classes |

**Note**: `{RootNamespace}` should be replaced with your project's root namespace (e.g., `Acme.Crm`, `MyCompany.Ecommerce`).

## Examples

```bash
# Standard CRUD with activation (like User) - auto-detects layered architecture
/crud-generator User

# Entity without IsActive (like AuditLog)
/crud-generator AuditLog hasIsActive:false,permission:AuditLogs

# Full-featured with config + bulk import (like ApiClient)
/crud-generator ApiClient hasConfig:true,needsBulkImport:true,permission:ApiClients

# Specify custom namespaces (generic example)
/crud-generator Order \
  contractsNamespace:{RootNamespace}.Application.Contracts.Orders \
  appServiceNamespace:{RootNamespace}.Application.AppServices.Orders

# Entity with custom DTO naming convention
/crud-generator Customer dtoSuffix:Input permission:Customers

# Full customization
/crud-generator Product \
  hasIsActive:false \
  hasConfig:false \
  needsBulkImport:false \
  permission:Products \
  contractsNamespace:{RootNamespace}.Application.Contracts.Products \
  appServiceNamespace:{RootNamespace}.Application.AppServices.Products
```

## Output Location

The skill generates files in **two separate layers** using **namespace-based paths**. You can run the command from any directory, but must provide namespace paths.

### Standard ABP Layered Architecture (Recommended)

Files are distributed across two projects:

```
{ProjectRoot}/
├── src/
│   ├── {Project}.Application.Contracts/
│   │   └── {PluralEntityName}/
│   │       ├── I{EntityName}AppService.cs
│   │       └── {EntityName}Dtos.cs
│   └── {Project}.Application/
│       └── AppServices/
│           └── {PluralEntityName}/
│               └── {EntityName}AppService.cs
```

**Generated files**:

1. **Contracts** (`{contractsNamespace}`):
   - `I{EntityName}AppService.cs` (interface)
   - `{EntityName}Dtos.cs` (all DTOs: `{EntityName}Dto`, `CreateUpdate{EntityName}Dto`, `{EntityName}Filter`, `{EntityName}ExportDto`, etc.)

2. **Application** (`{appServiceNamespace}`):
   - `{EntityName}AppService.cs` (implementation)

### Namespace-to-Path Conversion

The skill converts namespace paths to directory paths automatically:

```bash
# Namespace: {RootNamespace}.Application.Contracts.Customers
# Creates: src/{RootNamespace}.Application.Contracts/Customers/

# Namespace: {RootNamespace}.Application.AppServices.Customers
# Creates: src/{RootNamespace}.Application/AppServices/Customers/
```

### Single-Layer Mode (Legacy)

If your project uses a single `AppServices` folder for everything:

```bash
# Navigate to the AppServices directory
cd src/MyProject.Application/AppServices/

# Generate all files here (no contractsNamespace needed)
/crud-generator Customer
```

This creates:
- `ICustomerAppService.cs`
- `CustomerAppService.cs`
- `CustomerDtos.cs`

---

## Auto-Detection Logic

The skill attempts to intelligently detect your project structure:

1. **Look for Contracts layer**:
   - Searches current and parent directories for folder named `{RootNamespace}.Application.Contracts`
   - If found, sets default `contractsNamespace` to `{DetectedNamespace}.{PluralEntityName}`

2. **Look for Application layer**:
   - Searches for folder named `{RootNamespace}.Application`
   - If found, sets default `appServiceNamespace` to `{DetectedNamespace}.AppServices.{PluralEntityName}`

3. **Decision**:
   - If **both** contracts and app service patterns detected → **Layered mode**
   - If **only** application folder found → **Single-layer mode**
   - If **neither** found → You must explicitly specify namespaces

### Explicit Override

Always use explicit namespaces for reproducibility:

```bash
/crud-generator EntityName \
  contractsNamespace:YourCompany.YourApp.Application.Contracts.EntityNamePlural \
  appServiceNamespace:YourCompany.YourApp.Application.AppServices.EntityNamePlural
```

**Tip**: Use placeholders like `{RootNamespace}` throughout your codebase for consistency. Replace `{RootNamespace}` with your actual root namespace (e.g., `Acme`, `Contoso`, `MyCompany`).

## Reference Pattern

The generated code follows ABP Framework best practices and standard DDD patterns.

### Key Characteristics

**Logging Pattern**:
```csharp
_logger.LogInformation("{EntityName}AppService - {MethodName}: Requested by {UserId}", nameof(CreateAsync), currentUser.Id);
_logger.LogDebug("{EntityName}AppService - {MethodName}: Input = {@Input}", nameof(CreateAsync), input);
_logger.LogWarning("{EntityName}AppService - Validation: {Message}", validationMessage);
_logger.LogError(ex, "{EntityName}AppService - {MethodName}: Error occurred", nameof(CreateAsync));
```

**Error Handling**:
```csharp
try
{
    // Business logic with validation first
    await ValidateInputAsync(input);
    // Perform operation
}
catch (UserFriendlyException)
{
    // Re-throw user-friendly validation errors
    throw;
}
catch (Exception ex)
{
    _logger.LogError(ex, "{EntityName}AppService - {MethodName}: Unexpected error", methodName);
    throw new UserFriendlyException("An unexpected error occurred. Please try again.");
}
```

**Response Wrapper**:
```csharp
return new ResponseDataDto<T>
{
    Success = true,
    Code = 200,
    Message = "Operation completed successfully",
    Data = result
};
```

**Unit of Work**:
```csharp
using var uow = _unitOfWorkManager.Begin();
// Perform operations
await uow.CompleteAsync();
```

**Repository Access**:
```csharp
private readonly IRepository<{EntityName}, Guid> _{entityName}Repository;
// Use AsyncExecuter for async queries
var queryable = await _{entityName}Repository.GetQueryableAsync();
var result = await AsyncExecuter.FirstOrDefaultAsync(queryable.Where(...));
```

## Customization Points

After generation, customize these sections:

### 1. DTO Properties (Contracts Layer)

Update `{EntityName}Dto` to include all entity fields you want to expose:

```csharp
// In {EntityName}Dtos.cs
public class {EntityName}Dto
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public int StockQuantity { get; set; }
    public Guid CategoryId { get; set; }
    public string CategoryName { get; set; } // Navigation property
    public bool IsActive { get; set; }
    public DateTime CreationTime { get; set; }
    // Add other fields as needed
}

// In CreateUpdate{EntityName}Dto
public class CreateUpdate{EntityName}Dto
{
    [Required]
    [StringLength(100)]
    public string Name { get; set; }

    [Range(0, double.MaxValue)]
    public decimal Price { get; set; }

    [Range(0, int.MaxValue)]
    public int StockQuantity { get; set; }

    public Guid CategoryId { get; set; }

    // Add other fields with appropriate validation attributes
}
```

### 2. Entity Mapping (Implementation)

In `CreateAsync` and `UpdateAsync`, map DTO properties to Entity:

```csharp
// CreateAsync
var entity = new {EntityName}
{
    Name = input.Name,
    Price = input.Price,
    StockQuantity = input.StockQuantity,
    CategoryId = input.CategoryId,
    IsActive = input.IsActive,
    // Map all other properties
};
await _{entityName}Repository.InsertAsync(entity);

// UpdateAsync
var entity = await Get{EntityName}Async(id);
entity.Name = input.Name;
entity.Price = input.Price;
// Update all other properties
await _{entityName}Repository.UpdateAsync(entity);
```

### 3. Validation Rules

Extend `ValidateInputAsync` with business rules:

```csharp
private async Task ValidateInputAsync(CreateUpdate{EntityName}Dto input, Guid? id = null)
{
    // Required field validation
    if (string.IsNullOrWhiteSpace(input.Name))
    {
        throw new UserFriendlyException("{EntityName} name is required.");
    }

    // Numeric validation
    if (input.Price <= 0)
    {
        throw new UserFriendlyException("Price must be greater than zero.");
    }

    // Foreign key validation
    var categoryExists = await _categoryRepository.AnyAsync(c => c.Id == input.CategoryId);
    if (!categoryExists)
    {
        throw new UserFriendlyException("Selected category does not exist.");
    }

    // Uniqueness validation (optional)
    var queryable = await _{entityName}Repository.GetQueryableAsync();
    var duplicate = await AsyncExecuter.FirstOrDefaultAsync(
        queryable.Where(e => e.SKU == input.SKU && (!id.HasValue || e.Id != id.Value))
    );
    if (duplicate != null)
    {
        throw new UserFriendlyException("An item with the same SKU already exists.");
    }
}
```

### 4. Search & Filter Logic

Enhance `GetListAsync` to support filtering on additional fields:

```csharp
var query = _{entityName}Repository.GetQueryableAsync()
    .WhereIf(!string.IsNullOrWhiteSpace(filter.SearchKeyword),
        e => e.Name.ToLower().Contains(filter.SearchKeyword) ||
             e.SKU.ToLower().Contains(filter.SearchKeyword) ||
             e.Description.ToLower().Contains(filter.SearchKeyword))
    .WhereIf(filter.MinPrice.HasValue,
        e => e.Price >= filter.MinPrice.Value)
    .WhereIf(filter.MaxPrice.HasValue,
        e => e.Price <= filter.MaxPrice.Value)
    .WhereIf(filter.CategoryId.HasValue,
        e => e.CategoryId == filter.CategoryId.Value);
```

### 5. Foreign Key Lookups

Implement `Get{EntityName}sAsync` for dropdown lists (if referenced by other entities):

```csharp
public async Task<ResponseDataDto<DropDownDto[]>> Get{EntityName}sAsync()
{
    var items = await _{entityName}Repository.GetQueryableAsync()
        .Select(e => new DropDownDto
        {
            Value = e.Id.ToString(),
            Name = e.Name,
            // Optional: Description = e.Description
        })
        .ToArrayAsync();

    return new ResponseDataDto<DropDownDto[]>
    {
        Success = true,
        Data = items,
        Code = 200
    };
}
```

### 6. Deletion Validation

Check for dependent records before deletion:

```csharp
private async Task<ResponseDataDto<object>> Validate{EntityName}DeletionAsync(Guid id)
{
    var errors = new List<string>();

    // Check for orders
    var hasOrders = await _orderRepository.AnyAsync(o => o.{EntityName}Id == id);
    if (hasOrders)
    {
        errors.Add("This {entityName} has associated orders.");
    }

    // Check for active subscriptions
    var hasSubscriptions = await _subscriptionRepository.AnyAsync(s => s.{EntityName}Id == id && s.IsActive);
    if (hasSubscriptions)
    {
        errors.Add("This {entityName} has active subscriptions.");
    }

    if (errors.Any())
    {
        return new ResponseDataDto<object>
        {
            Success = false,
            Code = 400,
            Message = string.Join(" ", errors)
        };
    }

    return null; // No errors
}
```

Call this in `DeleteAsync`:

```csharp
var validationResult = await Validate{EntityName}DeletionAsync(id);
if (validationResult != null)
{
    return validationResult;
}
```

### 7. Deactivation Rules (Optional)

Override `ValidateDeactivationAsync` to prevent deactivation under certain conditions:

```csharp
private async Task ValidateDeactivationAsync(Guid id)
{
    var entity = await Get{EntityName}Async(id);

    // Prevent deactivation if entity is in use
    var isInUse = await _usageRepository.AnyAsync(u => u.{EntityName}Id == id && u.IsActive);
    if (isInUse)
    {
        throw new UserFriendlyException("Cannot deactivate {entityName} because it is currently in use.");
    }
}
```

### 8. Permissions (Authorization)

Define permission constants in your `PermissionDefinitionProvider`:

```csharp
public const string {EntityName}Default = PermissionGroupName + ".{EntityName}s.Default";
public const string {EntityName}Create = {EntityName}Default + ".Create";
public const string {EntityName}Edit = {EntityName}Default + ".Edit";
public const string {EntityName}Delete = {EntityName}Default + ".Delete";
public const string {EntityName}Activate = {EntityName}Default + ".Activate";
public const string {EntityName}Deactivate = {EntityName}Default + ".Deactivate";
```

Apply to methods:

```csharp
[Authorize(Permissions.{EntityName}.Create)]
public async Task<ResponseDataDto<object>> CreateAsync(CreateUpdate{EntityName}Dto input) { ... }

[Authorize(Permissions.{EntityName}.Activate)]
public async Task<ResponseDataDto<object>> ActivateAsync(Guid id) { ... }
```

### 9. Localization

Add localized error messages to your resource files:

```json
// en.json
{
  "texts": {
    "{EntityName}:NameRequired": "{EntityName} name is required.",
    "{EntityName}:DuplicateName": "A {entityName} with this name already exists.",
    "{EntityName}:DeletionBlocked": "Cannot delete {entityName} because it has associated records."
  }
}
```

And reference them:

```csharp
throw new UserFriendlyException(L["{EntityName}:NameRequired"]);
```

## Required Dependencies

Ensure these NuGet packages are referenced in your **Application.Contracts** and **Application** projects:

```xml
<PackageReference Include="Volo.Abp.Application" Version="8.0.0" />
<PackageReference Include="Volo.Abp.Domain" Version="8.0.0" />
<PackageReference Include="Volo.Abp.AspNetCore.Mvc" Version="8.0.0" />
```

**Project References** (for layered architecture):

```xml
<!-- In Application project .csproj -->
<ProjectReference Include="..\..\Application.Contracts\{Project}.Application.Contracts.csproj" />
```

**Note**: Adjust package versions to match your ABP Framework version (7.x, 8.x, or later).

### Optional Dependencies (for specific features)

If using `needsBulkImport:true` or `hasConfig:true`, you may need:

```xml
<!-- Project-specific Blob DTO library (create your own or use existing) -->
<PackageReference Include="{Project}.BlobDto" Version="1.0.0" />

<!-- Generic Bulk Import service (create your own or use existing) -->
<PackageReference Include="{Project}.GenericBulkImport" Version="1.0.0" />

<!-- JSON Export/Import services -->
<PackageReference Include="{Project}.JsonServices" Version="1.0.0" />
```

**Note**: Bulk import and export dependencies are project-specific. You may need to:
- Create your own `IExportService` implementation (using `CsvHelper`, `ClosedXML`, `Newtonsoft.Json`, etc.)
- Implement `IBulkImportService` for file parsing
- Or reuse existing services from your project's infrastructure

## Integration Checklist

After generating files:

### Contracts Layer (`{Project}.Application.Contracts/`)

- [ ] **Review DTO properties**: Ensure they match your Entity class properties
- [ ] **Add validation attributes**: Update `CreateUpdate{EntityName}Dto` with [Required], [StringLength], etc.
- [ ] **Update interface**: Verify method signatures match between contracts and implementation
- [ ] **Add permission constants**: Define in `PermissionDefinitionProvider` if using authorization

### Application Layer (`{Project}.Application/AppServices/`)

- [ ] **Update constructor dependencies**: Add required repositories (IRepository<Entity, Guid>, etc.)
- [ ] **Implement entity mapping**: Replace property assignments in CreateAsync/UpdateAsync
- [ ] **Add custom validations**: Extend `ValidateInput` method with business rules
- [ ] **Add reference lookups**: Implement `Get{EntityName}Async` helper methods for foreign keys
- [ ] **Check activation rules**: Verify `ActivateAsync`/`DeactivateAsync` have correct logic
- [ ] **Configure export** (if applicable): Ensure `ExportAsync` uses correct DTO and filter
- [ ] **Update filtering**: Add entity-specific fields to `GetListAsync` WhereIf clauses
- [ ] **Register service**: Usually auto-discovered via ABP's conventional registration
- [ ] **Verify DI container**: All dependencies should be registered in your DbContext and module

### Database & Testing

- [ ] **Create migration** (if entity is new): `dotnet ef migrations add Add{EntityName}`
- [ ] **Apply migration**: `dotnet ef database update`
- [ ] **Test endpoints**: Verify all CRUD operations work correctly
  - POST `/api/app/{entityName}/create`
  - PUT `/api/app/{entityName}/{id}`
  - DELETE `/api/app/{entityName}/{id}`
  - GET `/api/app/{entityName}/{id}`
  - GET `/api/app/{entityName}?page=1&pageSize=10`
  - POST `/api/app/{entityName}/activate/{id}` (if hasIsActive)
  - POST `/api/app/{entityName}/deactivate/{id}` (if hasIsActive)
  - GET `/api/app/{entityName}/export` (if needsBulkImport)
- [ ] **Update Swagger**: Add XML comments for API documentation
- [ ] **Add unit tests**: Follow `xunit-testing-patterns` skill

## Common Scenarios

### Scenario 1: New Entity - Standard ABP Layered (Auto-detection)

```bash
# Navigate to project root (where .sln is)
cd /path/to/{RootNamespace}

# Skill auto-detects layered architecture
/crud-generator Product hasIsActive:false,permission:Products

# Result ( Creates in standard locations ):
# - src/{RootNamespace}.Application.Contracts/Products/IProductAppService.cs
# - src/{RootNamespace}.Application.Contracts/Products/ProductDtos.cs
# - src/{RootNamespace}.Application/AppServices/Products/ProductAppService.cs
```

### Scenario 2: New Entity - Explicit Namespaces (Guaranteed)

```bash
# From any directory, specify exact namespaces
/crud-generator Customer \
  contractsNamespace:Acme.Crm.Application.Contracts.Customers \
  appServiceNamespace:Acme.Crm.Application.AppServices.Customers \
  permission:Customers

# Result:
# - src/Acme.Crm.Application.Contracts/Customers/ICustomerAppService.cs
# - src/Acme.Crm.Application.Contracts/Customers/CustomerDtos.cs
# - src/Acme.Crm.Application/AppServices/Customers/CustomerAppService.cs
```

### Scenario 3: Entity with Configuration & Bulk Import

```bash
/crud-generator Subscription \
  hasConfig:true \
  needsBulkImport:true \
  permission:Subscriptions \
  contractsNamespace:Contoso.Billing.Application.Contracts.Subscriptions \
  appServiceNamespace:Contoso.Billing.Application.AppServices.Subscriptions

# Includes:
# - ISubscriptionAppService.cs with ManageConfigAsync
# - SubscriptionConfig repository (you'll need to implement)
# - ExportAsync and BulkImportAsync
# - SubscriptionImportDto
```

### Scenario 4: Simple Entity (No Activation, No Bulk Import)

```bash
/crud-generator Tag hasIsActive:false,permission:Tags
# Generates: Create, Update, Delete, Get, GetList only
```

### Scenario 5: Single-Layer Project (Everything in AppServices)

```bash
cd src/LegacyProject.Application/AppServices/

/crud-generator Log hasIsActive:false,permission:Logs

# All 3 files in current directory:
# - ILogAppService.cs
# - LogAppService.cs
# - LogDtos.cs
```

### Scenario 6: Different DTO Naming Convention

Some teams prefer `Create{Entity}Input` instead of `CreateUpdate{Entity}Dto`:

```bash
/crud-generator Invoice dtoSuffix:Input permission:Invoices

# Generates:
# - CreateInvoiceInput (instead of CreateUpdateInvoiceDto)
# - InvoiceDto
# - InvoiceFilter
# - InvoiceExportDto
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Files not generated | Ensure you're in a writable directory |
| Compilation errors | Check all required using statements are present |
| Repository not found | Add `IRepository<{EntityName}, Guid>` to your DbContext |
| Permission errors | Verify permissions exist in `PermissionDefinitionProvider` |
| Duplicate SystemName error | Case-insensitive; check for existing data with different case |
| JSON validation fails | Ensure RequestConfig is valid JSON Schema format |
| Import file format error | Verify file matches `{EntityName}ImportDto` structure exactly |
| NSubstitute not found | Install `NSubstitute` NuGet package in test project |

## Design Decisions Explained

### Why This Pattern?

1. **Single Responsibility**: Each method handles one operation
2. **Consistent Error Handling**: All methods follow same try-catch pattern
3. **Structured Logging**: Every operation logs start, success, failure
4. **Authorization Granularity**: Separate permissions per operation
5. **User-Friendly Errors**: UserFriendlyException for client errors
6. **Transaction Management**: Unit of Work per operation
7. **Validation First**: Validate before any database operation
8. **DTO Boundaries**: No entity leakage beyond repository layer

### Why Include Activation Pattern?

Enables soft delete / archival pattern while maintaining referential integrity and audit trails.

### Why Bulk Import with Upsert?

Allows efficient data synchronization and initial data seeding without duplication.

## References

- **ABP Documentation**: https://docs.abp.io
- **DDD Guidelines**: https://docs.abp.io/en/abp/latest/Domain-Driven-Design
- **Entity Framework Core**: https://docs.microsoft.com/ef/core
- **ASP.NET Core**: https://docs.microsoft.com/aspnet/core

## Design Decisions Explained

### Why This Pattern?

1. **Single Responsibility**: Each method handles one operation
2. **Consistent Error Handling**: All methods follow same try-catch pattern
3. **Structured Logging**: Every operation logs start, success, failure
4. **Authorization Granularity**: Separate permissions per operation
5. **User-Friendly Errors**: UserFriendlyException for client errors
6. **Transaction Management**: Unit of Work per operation
7. **Validation First**: Validate before any database operation
8. **DTO Boundaries**: No entity leakage beyond repository layer

### Why Include Activation Pattern?

Enables soft delete / archival pattern while maintaining referential integrity and audit trails. Instead of physically deleting records, you mark them as inactive, preserving historical data and maintaining relationships.

### Why Bulk Import with Upsert?

Allows efficient data synchronization and initial data seeding without duplication. The generated upsert logic:
- Inserts new records (by unique key, e.g., Name/Code)
- Updates existing records (by unique key)
- Validates each row individually, collecting all errors

### Why Separate Contracts and Application?

Standard ABP layered architecture provides:
- **Separation of concerns**: Contracts define the API surface, Application implements it
- **Shared contracts**: Clients can reference only Contracts project, not full Application
- **Versioning**: Contracts can be versioned independently
- **Clean architecture**: Dependencies flow inward (Application → Contracts)

---

## Architecture Considerations

### Multi-Tenancy

If your ABP project uses multi-tenancy, ensure your queries include tenant filtering:

```csharp
var queryable = await _{entityName}Repository.GetQueryableAsync();
// ABP automatically filters by CurrentTenant.Id when using repositories
// No additional code needed if using standard ABP repositories
```

### Soft Delete vs. IsActive

The generated code uses an `IsActive` boolean for activation/deactivation. This is separate from ABP's built-in `ISoftDelete` pattern. If you prefer soft delete:

1. Make your entity implement `ISoftDelete`
2. Use `DeleteAsync` for soft delete (sets `IsDeleted = true`)
3. Use `RestoreAsync` for recovery
4. Remove `IsActive` field and Activate/Deactivate methods (or repurpose them)

Choose based on your business requirements:
- **Soft Delete**: Data is hidden but retained for audit/history
- **IsActive**: Entity can be toggled on/off while still visible in queries

### Authorization Strategies

Generated methods are permission-ready but not decorated with `[Authorize]` by default. Choose your approach:

**Per-method authorization**:
```csharp
[Authorize(Permissions.{EntityName}.Create)]
public async Task<ResponseDataDto<object>> CreateAsync(...) { ... }
```

**Controller-level authorization** (API Controllers):
```csharp
[Authorize(Permissions.{EntityName}.Default)]
[Route("api/app/{entityName-plural}")]
public class {EntityName}Controller : AbpController
```

**No authorization** (public APIs): Don't add `[Authorize]`

---

## Performance Tips

1. **Index your database**: Add indexes on frequently queried columns (Name, Code, foreign keys)
2. **Use pagination**: `GetListAsync` already uses pagination via `PagedAndSortedResultRequestDto`
3. **Select only needed fields**: DTO projection already optimizes this
4. **Cache dropdown data**: `Get{EntityName}sAsync` can benefit from caching if data is static
5. **Batch operations**: For bulk updates, consider implementing batch endpoints separately

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Files not generated | Ensure you're in a writable directory and have permission to create files |
| Compilation errors | Check using statements match your project's namespace structure |
| Repository not found | Add `DbSet<Entity>` to your DbContext and ensure `IRepository<Entity, Guid>` is registered |
| Permission errors | Define permission constants in your `PermissionDefinitionProvider` or remove `[Authorize]` attributes |
| Duplicate name error | Uniqueness checks are case-insensitive; check for existing data with different casing |
| Auto-detection fails | Provide explicit `contractsNamespace` and `appServiceNamespace` options |
| Namespace conflicts | Use unique plural forms for entity name (e.g., `Person` → `People`, not `Persons`) |
| AsyncExecuter not found | Add `using Volo.Abp.Linq;` to your implementation file |

---

## Contributing

This skill is designed to be **generic and reusable** across all ABP projects. When customizing:

1. **Preserve placeholders**: Keep `{EntityName}`, `{PluralEntityName}`, `{Project}` for reusability
2. **Test with multiple projects**: Verify generation works with different namespace patterns
3. **Document edge cases**: Update this doc with lessons learned
4. **Share improvements**: Contribute back to the team's skill library

---

## Glossary

- **Entity**: Your domain entity class (e.g., `Product`, `Customer`, `Order`)
- **PluralEntityName**: Plural form of entity name (e.g., `Products`, `Customers`, `Orders`)
- **Contracts Layer**: `{Project}.Application.Contracts` - Contains DTOs and interfaces
- **AppServices Layer**: `{Project}.Application.AppServices` - Contains business logic implementations
- **ABP**: ASP.NET Boilerplate (modern ABP Framework)
- **DDD**: Domain-Driven Design
- **DTO**: Data Transfer Object
- **CRUD**: Create, Read, Update, Delete
- **UoW**: Unit of Work pattern
- **EF Core**: Entity Framework Core

## Post-Generation Workflow

### Immediate Post-Generation

1. **Verify file locations**:
   - Interface and DTOs in `{Project}.Application.Contracts/{PluralEntityName}/`
   - Implementation in `{Project}.Application/AppServices/{PluralEntityName}/`

2. **Contracts layer updates** (`{Project}.Application.Contracts/`):
   - Review and customize `{EntityName}Dto` properties to match your Entity
   - Add validation attributes to `CreateUpdate{EntityName}Dto`
   - Update `{EntityName}Filter` with additional filter fields if needed
   - Ensure interface matches implementation

3. **Application layer updates** (`{Project}.Application/AppServices/`):
   - Update constructor to inject all required repositories
   - Implement property mapping in `CreateAsync` and `UpdateAsync`
   - Add business-specific validation in `ValidateInputAsync`
   - Update `GetListAsync` filtering logic for your entity's searchable fields
   - Implement `Get{EntityName}Async` helper if not already present
   - Customize `ActivateAsync`/`DeactivateAsync` logic as needed
   - Add foreign key dependency checks in deletion validation

4. **Permissions**: Add to your `PermissionDefinitionProvider`:
   ```csharp
   public const string {EntityName}Default = PermissionGroupName + ".{EntityName}s.Default";
   public const string {EntityName}Create = {EntityName}Default + ".Create";
   public const string {EntityName}Edit = {EntityName}Default + ".Edit";
   public const string {EntityName}Delete = {EntityName}Default + ".Delete";
   // Optional:
   public const string {EntityName}Activate = {EntityName}Default + ".Activate";
   public const string {EntityName}Deactivate = {EntityName}Default + ".Deactivate";
   ```

5. **Database**: Create and apply migrations if entity table doesn't exist:
   ```bash
   dotnet ef migrations add Add{EntityName}Table --project src/{RootNamespace}.Domain
   dotnet ef database update --project src/{RootNamespace}.Domain
   ```

6. **Testing**: Write unit tests and integration tests following your project's testing patterns.

7. **Localization**: Add error message keys to resource files for internationalization.

8. **API Documentation**: Add XML comments to interface methods for Swagger/OpenAPI.

### Ongoing Maintenance

- Keep Contracts and Implementation in sync when modifying interfaces
- Update both layers when adding new methods or changing signatures
- Follow the established patterns in existing services for consistency

## Notes

### ABP Layered Architecture

This skill supports both **single-layer** and **two-layer** architectures:

- **Two-layer (Standard ABP)**: Interface & DTOs in `{Project}.Application.Contracts`, implementation in `{Project}.Application.AppServices`
- **Single-layer (Legacy)**: All files in one `AppServices` folder (for reference compatibility)

The skill auto-detects based on project structure, or you can explicitly specify namespaces.

### Code Readiness

- Generated code is **ready to compile** after property customization
- Follows **ABP 8.0+** conventions and .NET 8.0
- Assumes **EF Core** with Guid primary keys
- Uses `ApplicationService` as base class (standard ABP)
- Response wrapper is `ResponseDataDto<T>` (project-specific)
- Adjust base class and response types for other ABP projects

### Namespace Conventions

- Contracts: `{RootNamespace}.Application.Contracts.{PluralEntityName}` (e.g., `Acme.Crm.Application.Contracts.Customers`)
- AppServices: `{RootNamespace}.Application.AppServices.{PluralEntityName}` (e.g., `Acme.Crm.Application.AppServices.Customers`)

### Auto-Detection

The skill looks for folders named `{Project}.Application.Contracts` and `{Project}.Application` in the current or parent directories. If both exist, layered mode is automatic.
