---
name: data-seeder-generator
description: "Generate ABP Framework data seeder contributors following project conventions. Auto-detects project structure, existing entities, namespaces, permission constants, and seeder patterns from the codebase — no manual configuration needed. Creates IDataSeedContributor implementations with proper dependency injection, logging, and tenant/feature awareness. Use when: (1) creating new seed data for entities, (2) adding initial/reference data, (3) scaffolding data initialization code, (4) maintaining data consistency across environments."
layer: 1
tech_stack: [dotnet, csharp, abp, entityframework, data-seeding]
topics: [data-seeding, idataseedcontributor, abp-framework, initial-data, reference-data, dependency-injection]
depends_on: [abp-framework-patterns, entity-framework-core, repository-pattern]
complements: [crud-generator, migration-management]
keywords: [IDataSeedContributor, SeedAsync, DataSeedContext, ITransientDependency, IRepository, repository.InsertAsync, autoSave, unit-of-work]
---

# ABP Data Seeder Contributor Generator

Generates production-ready data seeder contributors following this project's conventions and ABP Framework best practices. This skill creates classes that implement `IDataSeedContributor` for seeding initial, reference, or lookup data into the database.

**Key feature: Auto-detects project structure, existing entities, namespaces, and seeder patterns before generating — no manual configuration needed.**

---

## When to Use

- Adding initial lookup/reference data (e.g., categories, types, enumerations)
- Seeding default configuration or system data
- Setting up multi-tenant default data
- Creating data migrations with seed content
- Populating test/development data
- **Any data that should exist when the application first runs or when a new tenant is provisioned**

---

## Step 0 — Auto-Detect Project Structure

**Do this automatically before asking the user anything. Never ask what you can detect.**

### 0.1 Find Solution and Project Name

```bash
# Find solution file
find . -name "*.sln" | head -3

# Extract project/solution name
basename $(find . -name "*.sln" | head -1) .sln

# Find all .csproj files and classify layers
find . -name "*.csproj" | sort
# *.Domain.csproj                  → Domain layer
# *.Domain.Shared.csproj           → Domain Shared (constants, enums)
# *.Application.csproj             → Application layer
# *.EntityFrameworkCore.csproj     → EF Core layer
# *.DbMigrator.csproj              → DbMigrator (tenant-aware seeders go here)
# *.HttpApi.Host.csproj            → Host layer
```

### 0.2 Detect Root Namespace

```bash
# Extract namespace from any existing AppService or entity
grep -m1 "^namespace " $(find . -name "*AppService.cs" ! -path "*/bin/*" | head -1) 2>/dev/null

# Fallback: read from .csproj RootNamespace
grep "RootNamespace" $(find . -name "*.Domain.csproj" | head -1) 2>/dev/null
```

### 0.3 Detect Existing Seeder Patterns

```bash
# Find all existing seeders — most important step
find . -name "*DataSeed*" -o -name "*SeedContributor*" -o -name "*SeederContributor*" \
  | grep "\.cs$" ! -path "*/bin/*" ! -path "*/obj/*" | head -10

# Read EVERY existing seeder found — learn the exact pattern used
# view each file found above
```

**From existing seeders, extract:**
- Constructor style (primary constructor vs traditional)
- Logging pattern (`_logger.LogInformation` messages format)
- Existence check pattern (`AnyAsync` vs `FirstOrDefaultAsync` vs count)
- Insert pattern (`InsertAsync` vs `InsertManyAsync`)
- UoW pattern (`[UnitOfWork]` vs explicit `IUnitOfWorkManager`)
- Whether `IClientSeedingService` is used
- Whether feature flags are used
- Namespace convention

### 0.4 Detect Existing Entities

```bash
# Find all domain entities
find . -name "*.cs" -path "*/Domain/*" ! -path "*/bin/*" ! -path "*/obj/*" \
  ! -path "*/Tests/*" ! -path "*/Data/*" | head -30

# Detect which use AggregateRoot vs Entity base class
grep -rl "AggregateRoot\|FullAuditedAggregateRoot\|Entity<" \
  --include="*.cs" . | grep -v "bin\|obj\|Tests" | head -20

# Read each entity to extract:
# - Property names and types
# - Required vs optional fields
# - Any SystemName / unique identifier property
# - Enum properties (need Domain.Shared scan too)
# Example:
view("src/{Project}.Domain/Entities/Customers/Customer.cs")
```

### 0.5 Detect Entity Constants (Domain.Shared)

```bash
# Find constants files in Domain.Shared
find . -name "*Consts*" -path "*/Domain.Shared/*" ! -path "*/bin/*" | head -10

# Read to find Items collections
grep -rn "public static class Items" --include="*.cs" . | head -10

# Read each consts file found
# view each consts file
```

### 0.6 Detect Enums

```bash
# Find all enum definitions
grep -rn "public enum" --include="*.cs" . \
  ! -path "*/bin/*" ! -path "*/obj/*" | head -20

# Read enum files for first/default values
find . -name "*.cs" -path "*/Domain.Shared/*" | xargs grep -l "public enum" 2>/dev/null | head -5
# view each found
```

### 0.7 Detect Permission Constants

```bash
# Find permission files
find . -name "*Permissions*.cs" ! -path "*/bin/*" | head -5

# Extract all permission constants
grep -rn "public const string" --include="*Permissions*.cs" . | head -30

# Find PermissionDefinitionProvider
find . -name "*PermissionDefinitionProvider.cs" | head -3
# view it
```

### 0.8 Detect Multi-Tenancy

```bash
# Check if multi-tenancy is enabled
grep -rn "IsMultiTenant\|MultiTenancy\|ITenantRepository\|ITenantManager" \
  --include="*.cs" . | head -5

# Check if IClientSeedingService exists (project-specific)
grep -rn "IClientSeedingService" --include="*.cs" . | head -5

# Find tenant constants
find . -name "*TenantConsts*" ! -path "*/bin/*" | head -3
# view if found
```

### 0.9 Detect Seeder File Locations

```bash
# Check all 3 possible seeder locations
ls src/*.Domain/Entities/ 2>/dev/null
ls src/*.Domain/Data/ 2>/dev/null
ls src/*.DbMigrator/ 2>/dev/null

# Determine which is used by existing seeders
find . -name "*DataSeed*" -o -name "*SeedContributor*" | grep "\.cs$" \
  ! -path "*/bin/*" | head -5
```

### 0.10 Build Project Profile

After scanning, compile:

```json
{
  "projectName": "Amnil.AccessControlManagementSystem",
  "rootNamespace": "Amnil.AccessControlManagementSystem",
  "domainProject": "src/Amnil.AccessControlManagementSystem.Domain",
  "domainSharedProject": "src/Amnil.AccessControlManagementSystem.Domain.Shared",
  "dbMigratorProject": "src/Amnil.AccessControlManagementSystem.DbMigrator",

  "existingEntities": [
    {
      "name": "Customer",
      "path": "src/.../Domain/Entities/Customers/Customer.cs",
      "properties": ["Name", "Email", "Phone", "IsActive"],
      "hasSystemName": true,
      "constsFile": "CustomerConsts.cs"
    }
  ],

  "existingSeederPattern": {
    "constructorStyle": "primary",
    "existenceCheck": "AnyAsync",
    "insertPattern": "InsertAsync",
    "uowPattern": "explicit",
    "usesClientSeedingService": true,
    "usesFeatureFlags": false,
    "loggingFormat": "Starting {EntityName} data seeding..."
  },

  "isMultiTenant": true,
  "permissionPrefix": "ACMSPermissions",
  "seederLocations": {
    "domainEntities": "src/.../Domain/Entities/{EntityPlural}/",
    "domainData": "src/.../Domain/Data/",
    "dbMigrator": "src/.../DbMigrator/{Category}/"
  }
}
```

**Use this profile for all code generation below.**

---

## What Gets Generated

A complete `IDataSeedContributor` implementation following this project's patterns.

### File Structure

Data seeder contributors can be placed in different locations depending on scope:

**For Domain/Entity-specific seeders:**
```
src/{Project}.Domain/Entities/{EntityPlural}/{EntityName}DataSeederContributor.cs
```

**For DbMigrator-specific seeders (tenant-aware, blob storage, file-based):**
```
src/{Project}.DbMigrator/{Category}/{EntityName}DataSeederContributor.cs
```

**For System-wide seeders:**
```
src/{Project}.Domain/Data/{EntityName}DataSeedContributor.cs
```

**Location is auto-selected based on seeder type:**
- Tenant-aware or blob storage → DbMigrator
- Entity-specific reference data → Domain/Entities/{EntityPlural}
- System-wide → Domain/Data

### Generated Code Structure

```csharp
using {RequiredNamespaces};
using Volo.Abp.Data;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Domain.Repositories;

namespace {TargetNamespace};

public class {EntityName}DataSeederContributor(
    {Dependencies}
) : IDataSeedContributor, ITransientDependency
{
    private readonly ILogger<{EntityName}DataSeederContributor> _logger;
    {OtherPrivateFields}

    public async Task SeedAsync(DataSeedContext context)
    {
        _logger.LogInformation("Starting {EntityName} data seeding...");

        try
        {
            {SeedLogic}

            _logger.LogInformation("{EntityName} data seeding completed successfully.");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "{EntityName} data seeding failed.");
            throw;
        }
    }

    {HelperMethods}
}
```

---

## Pattern Guidelines (From Codebase Analysis)

**Always use the pattern detected in Step 0.3 from existing seeders.
The patterns below are fallbacks if no existing seeder is found.**

### 1. Basic Repository-Based Seeder (Simple)

**Used for:** Simple entities with just property data, no complex dependencies

**Example Pattern:**
```csharp
public async Task SeedAsync(DataSeedContext context)
{
    var items = new List<(string SystemName, string DisplayName, string? Description, bool IsActive)>
    {
        (EntityConsts.Items.Value1, "Display Name 1", "Description", true),
        (EntityConsts.Items.Value2, "Display Name 2", "Description", true),
    };

    await SeedItems(items);
}

private async Task SeedItems(List<(string SystemName, string DisplayName, string? Description, bool IsActive)> items)
{
    foreach (var (SystemName, DisplayName, Description, IsActive) in items)
    {
        await AddItem(SystemName, DisplayName, Description, IsActive);
    }
}

private async Task AddItem(string systemName, string displayName, string? description, bool isActive)
{
    var exists = await _repository.AnyAsync(x => x.SystemName == systemName);
    if (!exists)
    {
        await _repository.InsertAsync(new Entity
        {
            SystemName = systemName,
            DisplayName = displayName,
            Description = description,
            IsActive = isActive
        });
    }
}
```

**Key Points:**
- Always check existence using `AnyAsync` or `FirstOrDefaultAsync` before insert
- Use tuple collections for clean data definition
- Separate seeding logic into private helper methods
- No `autoSave: true` in multi-step operations (rely on UoW)

### 2. Repository-Based Seeder with autoSave (Simple, Single Insert)

**Used for:** Simple bulk inserts where each item is independent

```csharp
await _repository.InsertManyAsync(items, autoSave: true);
```

**Example:** `NotificationDataSeedContributor`, `ConfigurationDataSeederContributor`

### 3. Tenant-Aware Seeder

**Used for:** Seeders in `DbMigrator` project that need multi-tenant logic

```csharp
public async Task SeedAsync(DataSeedContext context)
{
    if (!_clientSeedingService.IsDevelopment)
    {
        _logger.LogWarning("Tenant data seed will only take place in the Development environment.");
        return;
    }

    var tenantNames = new List<string>
    {
        // Auto-detected from TenantConsts if found, else use placeholders
        ACMSTenantConsts.Items.MBL,
        ACMSTenantConsts.Items.NMB,
        ACMSTenantConsts.Items.NCELL
    };

    await SeedTenants(tenantNames);
    _logger.LogInformation("Tenant seeding completed. Summary: {TotalTenants} tenants processed, {AddedTenants} added, {SkippedTenants} skipped.",
        totalTenants, addedTenants, skippedTenants);
}
```

**Key Points:**
- Use `IClientSeedingService.IsDevelopment` to check environment
- Use `IClientSeedingService.ValidFor([...])` to filter by tenant
- Track added/skipped counts for summary logging

### 4. Feature-Flagged Seeder

**Used for:** Seeders that should only run when specific features are enabled

```csharp
if (_featureManagementService.IsEnabled("FeatureName"))
{
    // Seed feature-specific data
}
```

**Example:** WorkflowStageDataSeederContributor uses this for conditional sub-stage seeding

### 5. User/Role Seeder (Complex, with UserManager)

**Used for:** Seeders that need identity operations (password hashing, role assignment)

```csharp
private readonly IdentityUserManager _userManager;
private readonly IGuidGenerator _guidGenerator;
private readonly IConfiguration _configuration;
private readonly IUnitOfWorkManager _unitOfWorkManager;
private readonly IRepository<IdentityRole, Guid> _roleRepository;

public async Task SeedAsync(DataSeedContext context)
{
    var defaultPassword = _configuration.GetValue<string?>("User:DefaultPassword")
                              ?? IdentityDataSeedContributor.AdminPasswordDefaultValue;

    var users = new List<(string UserName, string Email, string Name, string Surname, string Password, List<string> Roles, bool IsActive)>
    {
        ("system", "system.acms@yopmail.com", "System", "Administrator", defaultPassword, new List<string> { "admin" }, true),
    };

    await SeedUsers(users);
}

private async Task SeedUsers(List<...> users)
{
    using (var uow = _unitOfWorkManager.Begin(requiresNew: true))
    {
        foreach (var userData in users)
        {
            await AddUser(...);
        }
        await uow.CompleteAsync();
    }
}

private async Task AddUser(...)
{
    var existingUser = await _userManager.FindByNameAsync(userName)
                    ?? await _userManager.FindByEmailAsync(email);
    if (existingUser != null)
    {
        _logger.LogWarning("User {UserName} already exists. Skipping creation.", userName);
        return;
    }

    var userId = _guidGenerator.Create();
    var user = new IdentityUser(userId, userName, email) { ... };

    var result = await _userManager.CreateAsync(user);
    result.CheckErrors();

    var addPasswordResult = await _userManager.AddPasswordAsync(user, password);
    addPasswordResult.CheckErrors();

    (await _userManager.SetLockoutEnabledAsync(user, true)).CheckErrors();

    if (roles != null && roles.Any())
    {
        await _userManager.SetRolesAsync(user, validRoles);
    }
}
```

**Key Points:**
- Use `IdentityUserManager` for user operations (not repository)
- Use `IGuidGenerator.Create()` for GUIDs
- Always use `CheckErrors()` on IdentityResult
- Wrap in explicit UoW if not using `[UnitOfWork]` attribute
- Check both user name and email for existing users

### 6. Blob Storage Seeder

**Used for:** Seeding files into blob storage

```csharp
private readonly IBlobContainer<{ContainerName}> _fileContainer;

public async Task SeedAsync(DataSeedContext context)
{
    var templatePath = Path.Combine(baseDirectory, "Templates");
    var templateFileNames = new[]
    {
        BulkImportFileConsts.TemplateFileNames.Application,
        BulkImportFileConsts.TemplateFileNames.PMTransfer,
    };

    foreach (var fileName in templateFileNames)
    {
        var fullPath = Path.Combine(templatePath, fileName);
        await TrySeedFileAsync(fullPath, fileName);
    }
}

private async Task TrySeedFileAsync(string filePath, string fileName)
{
    if (!File.Exists(filePath))
    {
        _logger.LogWarning("File not found: {Path}", filePath);
        return;
    }

    try
    {
        await using var fileStream = File.OpenRead(filePath);
        await _fileContainer.SaveAsync(fileName, fileStream, true);
        _logger.LogInformation("Seeded file: {FileName}", fileName);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Failed to seed file: {FileName}", fileName);
        throw;
    }
}
```

**Key Points:**
- Use `IBlobContainer<T>` for blob operations
- Handle file-not-found gracefully (log warning, return)
- Use `true` for overwrite parameter in `SaveAsync`

---

## Common Dependencies and Their Uses

| Dependency | Purpose | Where Used | Auto-Detected? |
|---|---|---|---|
| `IRepository<Entity, Guid>` | Basic CRUD operations | All entity seeders | ✅ From entity scan |
| `ILogger<T>` | Structured logging | All seeders | ✅ Always added |
| `IdentityUserManager` | User creation/password/roles | User seeder | ✅ If user seeder requested |
| `ITenantManager` | Tenant creation | Tenant seeder | ✅ If multi-tenant detected |
| `IClientSeedingService` | Development/tier check | DbMigrator seeders | ✅ If found in codebase |
| `IFeatureManagementService` | Feature flag checks | Feature-gated seeders | ✅ If found in codebase |
| `IGuidGenerator` | Generate GUIDs | When creating entities manually | ✅ If user seeder |
| `IUnitOfWorkManager` | Manual UoW control | Complex multi-repo operations | ✅ From existing pattern |
| `IBlobContainer<T>` | File/blob storage | Template/file seeders | ❌ User must request |
| `IConfiguration` | Read config values | Password, API keys | ✅ If user seeder |

---

## Interface Contract

All data seeder contributors **must**:
- Implement `IDataSeedContributor` from `Volo.Abp.Data`
- Implement `ITransientDependency` (enables DI as transient)
- Have a single public method: `Task SeedAsync(DataSeedContext context)`
- Accept `DataSeedContext` parameter (provides tenant ID, properties)
- Use `[UnitOfWork]` attribute OR explicit `IUnitOfWorkManager` for transactions

---

## Logging Best Practices

```csharp
_logger.LogInformation("Starting {EntityName} data seeding...");      // At start
_logger.LogDebug("Seeding item: {ItemKey}", key);                     // Per-item (verbose)
_logger.LogInformation("Created {Count} items");                       // Summary with counts
_logger.LogWarning("Item already exists: {Key}");                     // For skipped items
_logger.LogInformation("{EntityName} data seeding completed successfully."); // At end

// In catch:
_logger.LogError(ex, "{EntityName} data seeding failed.");
throw; // Re-throw to abort seeding
```

---

## DataSeedContext Properties

The `DataSeedContext` provides:
- `context.TenantId` — current tenant ID (null for host)
- Custom properties via `WithProperty()` — used by ABP built-in seeders

Typically only needed for multi-tenant-aware logic.

---

## Usage Instructions

### 1. Auto-Detection First (NEW)

The skill runs Step 0 automatically before asking anything. It will:
- Detect your project name, namespace, and layer paths
- Find all existing entities and their properties
- Find all existing seeders and learn their pattern
- Detect multi-tenancy, permissions, and constants
- Pre-fill most answers so you confirm rather than type

### 2. Confirm or Override Detected Values

After auto-detection the skill will show:

```
Auto-Detected Project Profile:
  Project:     Amnil.AccessControlManagementSystem
  Namespace:   Amnil.AccessControlManagementSystem
  Entities:    Customer, Operation, WorkflowStage, Notification
  Pattern:     Primary constructor, AnyAsync check, InsertAsync
  Multi-tenant: Yes (IClientSeedingService detected)
  Seeder style: Matches NotificationDataSeedContributor.cs

Entities available for seeding:
  1. Customer     (Name, Email, Phone, IsActive, SystemName)
  2. Operation    (SystemName, DisplayName, Description, IsActive)
  3. WorkflowStage (SystemName, DisplayName, Order, IsActive)

Which entity do you want to seed? (or "all" for all entities)
What type of seeder? (basic / tenant-aware / user-role / blob / feature-flagged)
```

### 3. Prepare Entity and Constants

Ensure your entity:
- Has a `SystemName` property (string, unique) for programmatic identification
- Has appropriate constructors
- Has a constants class with `Items` collection (recommended):

```csharp
// Auto-generated if not found:
public static class {EntityName}Consts
{
    public static class Items
    {
        public const string Value1 = "VALUE1";
        public const string Value2 = "Value2";
    }
}
```

### 4. Generate and Integrate

The skill will generate:
- Complete C# class file with correct namespace (auto-detected)
- All required using statements (auto-detected from entity + pattern)
- Constructor with dependency injection (matches detected constructor style)
- SeedAsync implementation with try-catch and logging
- Private helper methods
- EntityConsts class if not already present

**After generation:**
1. File is placed in the correct auto-detected location
2. Seeder is automatically discovered by `IDataSeeder` on migration/startup
3. Test with: `dotnet run` in the DbMigrator project

---

## Print Summary After Generation

```
═══════════════════════════════════════════════════════════════════
Data Seeder Generator — Complete
═══════════════════════════════════════════════════════════════════

Auto-Detected:
  ✓ Project:        Amnil.AccessControlManagementSystem
  ✓ Namespace:      Amnil.AccessControlManagementSystem
  ✓ Entities Found: 4 (Customer, Operation, WorkflowStage, Notification)
  ✓ Pattern From:   NotificationDataSeedContributor.cs
  ✓ Multi-Tenant:   Yes — IClientSeedingService detected
  ✓ Constructor:    Primary constructor style
  ✓ Existence Check: AnyAsync
  ✓ Insert Pattern: InsertAsync (no autoSave)

Files Generated:
  ✓ CustomerDataSeederContributor.cs
    → src/.../Domain/Entities/Customers/
    → Pattern: Basic (AnyAsync + InsertAsync)
    → 2 sample records seeded

Next Steps:
  1. Review generated seed values
  2. Update {EntityName}Consts.Items if needed
  3. Run: dotnet run --project src/{Project}.DbMigrator
  4. Verify data in database

═══════════════════════════════════════════════════════════════════
```

---

## Examples from This Project

### Simple Entity Seeder
- `NotificationDataSeedContributor.cs` — Notification mediums and recipient types
- `ConfigurationDataSeederContributor.cs` — System configuration values
- `OperationDataSeederContributor.cs` — Operation definitions with tenant filtering

### Complex Seeder
- `UserDataSeederContributor.cs` — User creation with passwords and roles
- `WorkflowStageDataSeederContributor.cs` — Multi-entity (stages + sub-stages) with relationships and feature flags

### DbMigrator-Specific Seeder
- `TenantDataSeederContributor.cs` — Tenant creation with statistics
- `BulkImportTemplateDataSeederContributor.cs` — File seeding to blob storage

---

## Important Notes

- **Seeding is Idempotent**: Always check existence before insert (`AnyAsync`, `FirstOrDefaultAsync`, or count checks)
- **No Hard-Coded IDs**: Use `Guid.NewGuid()` or repository-generated IDs
- **Context Matters**: Seeders in `Domain` layer run for all tenants; `DbMigrator` seeders have access to tenant management services
- **Order Not Guaranteed**: If ordering needed (FK dependencies), seed in sequence within same contributor
- **Development vs Production**: Use `IClientSeedingService.IsDevelopment` to skip certain seeds in non-development environments
- **Performance**: Batch inserts with `InsertManyAsync` when possible, but be careful with `autoSave: false` in loops (wrap in UoW)

---

## Related Skills

- `crud-generator` — Generate CRUD AppServices for entities
- `api-spec-to-service` — Generate services from API specifications

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Seeder not running | Check that the class implements both `IDataSeedContributor` and `ITransientDependency` |
| Duplicate data | Ensure idempotency checks (existence checks) are in place |
| Guid issues | Use `Guid.NewGuid()` or `IGuidGenerator.Create()` |
| Missing dependencies | Add required services to constructor; ensure they're registered in DI |
| Order dependency | Add explicit ordering logic within SeedAsync or seed related entities in same contributor |
| Tenant data not seeding | Use DbMigrator project for tenant operations; ensure multi-tenancy is enabled |
| Auto-detection failed | Skill falls back to asking user — provide entity name and namespace manually |
