---
description: Generate a Filter DTO for ABP entity list queries with WhereIf pattern
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: <EntityName> [--properties "Name:string,Status:bool?,CategoryId:Guid?"]
model: haiku
---

# Generate Filter Command

Generate a Filter DTO for an existing ABP entity to enable advanced list querying.

**Arguments**: $ARGUMENTS

## Pre-flight

**Project**: !`basename $(pwd)`
**Application.Contracts**: !`find api/src -maxdepth 1 -type d -name "*Application.Contracts" 2>/dev/null | head -1`

Required context:
- Read `CLAUDE.md` for project conventions
- Read existing entity DTOs to understand property types

## Workflow

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. Read      │ → │ 2. Generate  │ → │ 3. Update    │
│ Entity DTOs  │   │ Filter DTO   │   │ AppService   │
└──────────────┘   └──────────────┘   └──────────────┘
```

## Filter DTO Template

```csharp
// Application.Contracts/{EntityPlural}/{Entity}Filter.cs
namespace {ProjectName}.{EntityPlural};

/// <summary>
/// Filter criteria for {Entity} list queries.
/// </summary>
public class {Entity}Filter
{
    // String properties: contains/like search
    public string? Name { get; set; }

    // Guid properties: exact match
    public Guid? CategoryId { get; set; }

    // Bool properties: exact match
    public bool? IsActive { get; set; }

    // DateTime properties: range filters
    public DateTime? CreatedAfter { get; set; }
    public DateTime? CreatedBefore { get; set; }

    // Numeric properties: range filters
    public decimal? PriceMin { get; set; }
    public decimal? PriceMax { get; set; }

    // Enum properties: exact match
    public OrderStatus? Status { get; set; }
}
```

## Property Type Mapping

| Entity Property Type | Filter Properties | WhereIf Pattern |
|---------------------|-------------------|-----------------|
| `string` | `string? {Prop}` | `.WhereIf(!filter.{Prop}.IsNullOrWhiteSpace(), x => x.{Prop}.ToLower().Contains(filter.{Prop}.ToLower()))` |
| `Guid` | `Guid? {Prop}` | `.WhereIf(filter.{Prop}.HasValue, x => x.{Prop} == filter.{Prop})` |
| `Guid?` | `Guid? {Prop}` | `.WhereIf(filter.{Prop}.HasValue, x => x.{Prop} == filter.{Prop})` |
| `bool` | `bool? {Prop}` | `.WhereIf(filter.{Prop}.HasValue, x => x.{Prop} == filter.{Prop})` |
| `DateTime` | `DateTime? {Prop}From`, `DateTime? {Prop}To` | `.WhereIf(filter.{Prop}From.HasValue, x => x.{Prop} >= filter.{Prop}From)` |
| `int`, `decimal` | `{Type}? {Prop}Min`, `{Type}? {Prop}Max` | `.WhereIf(filter.{Prop}Min.HasValue, x => x.{Prop} >= filter.{Prop}Min)` |
| `enum` | `{EnumType}? {Prop}` | `.WhereIf(filter.{Prop}.HasValue, x => x.{Prop} == filter.{Prop})` |

## AppService Interface Update

```csharp
// I{Entity}AppService.cs
public interface I{Entity}AppService : IApplicationService
{
    // Update existing method signature
    Task<PagedResultDto<{Entity}Dto>> GetListAsync(
        PagedAndSortedResultRequestDto input,
        {Entity}Filter filter);
}
```

## AppService Implementation Update

```csharp
// {Entity}AppService.cs
public async Task<PagedResultDto<{Entity}Dto>> GetListAsync(
    PagedAndSortedResultRequestDto input,
    {Entity}Filter filter)
{
    // Sanitize string inputs
    filter.Name = filter.Name?.Trim();

    // Default sorting
    if (input.Sorting.IsNullOrWhiteSpace())
    {
        input.Sorting = nameof({Entity}Dto.Name);
    }

    var queryable = await _repository.GetQueryableAsync();

    var query = queryable
        // String filters (contains search)
        .WhereIf(!filter.Name.IsNullOrWhiteSpace(),
            x => x.Name.ToLower().Contains(filter.Name.ToLower()))

        // Guid filters (exact match)
        .WhereIf(filter.CategoryId.HasValue,
            x => x.CategoryId == filter.CategoryId)

        // Bool filters (exact match)
        .WhereIf(filter.IsActive.HasValue,
            x => x.IsActive == filter.IsActive)

        // DateTime range filters
        .WhereIf(filter.CreatedAfter.HasValue,
            x => x.CreationTime >= filter.CreatedAfter.Value)
        .WhereIf(filter.CreatedBefore.HasValue,
            x => x.CreationTime <= filter.CreatedBefore.Value)

        // Numeric range filters
        .WhereIf(filter.PriceMin.HasValue,
            x => x.Price >= filter.PriceMin.Value)
        .WhereIf(filter.PriceMax.HasValue,
            x => x.Price <= filter.PriceMax.Value);

    var totalCount = await AsyncExecuter.CountAsync(query);

    var items = await AsyncExecuter.ToListAsync(
        query
            .OrderBy(input.Sorting)
            .PageBy(input.SkipCount, input.MaxResultCount));

    return new PagedResultDto<{Entity}Dto>(
        totalCount,
        ObjectMapper.Map<List<{Entity}>, List<{Entity}Dto>>(items));
}
```

## Controller Update (if using explicit controllers)

```csharp
// {Entity}Controller.cs
[HttpGet]
public Task<PagedResultDto<{Entity}Dto>> GetListAsync(
    [FromQuery] PagedAndSortedResultRequestDto input,
    [FromQuery] {Entity}Filter filter)
{
    return _{entity}AppService.GetListAsync(input, filter);
}
```

## Execution Steps

1. **Locate entity DTOs**:
   - Read `{Project}.Application.Contracts/{EntityPlural}/{Entity}Dto.cs`
   - Identify all properties and their types

2. **Create Filter DTO**:
   - Create `{Entity}Filter.cs` in same folder
   - Map properties according to type rules above

3. **Update AppService interface**:
   - Modify `GetListAsync` signature to include filter parameter

4. **Update AppService implementation**:
   - Add WhereIf clauses for each filter property
   - Sanitize string inputs with trim

5. **Verify**:
   - Build: `dotnet build api/*.slnx`

## Output Files

```
api/src/{Project}.Application.Contracts/{EntityPlural}/
├── {Entity}Dto.cs              (existing)
├── CreateUpdate{Entity}Dto.cs  (existing)
├── Get{Entity}ListInput.cs     (existing)
├── I{Entity}AppService.cs      (updated)
└── {Entity}Filter.cs           (NEW)

api/src/{Project}.Application/{EntityPlural}/
└── {Entity}AppService.cs       (updated)
```

## Examples

```bash
# Generate filter for existing Product entity
/generate:filter Product

# With explicit properties (overrides auto-detection)
/generate:filter Product --properties "Name:string,Price:decimal,CategoryId:Guid?,IsActive:bool"

# For Order entity with enum
/generate:filter Order --properties "OrderNumber:string,Status:OrderStatus,Total:decimal,CustomerId:Guid"
```

## Checkpoint

After generation:
- [ ] Filter DTO created with appropriate nullable types
- [ ] AppService interface updated with filter parameter
- [ ] AppService implementation uses WhereIf pattern
- [ ] String inputs are trimmed before filtering
- [ ] Build succeeds: `dotnet build api/*.slnx`
