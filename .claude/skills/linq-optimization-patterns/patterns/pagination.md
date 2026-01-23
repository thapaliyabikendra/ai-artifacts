# Pagination Pattern

Efficient paging for list endpoints with total count optimization.

---

## When to Use

- Implementing list/grid APIs
- Large datasets that can't be returned entirely
- Need total count for UI pagination controls

---

## Standard ABP Pagination

```csharp
public async Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientsInput input)
{
    var query = await _patientRepository.GetQueryableAsync();

    // Apply filters
    query = query
        .WhereIf(!input.Filter.IsNullOrWhiteSpace(),
            p => p.FirstName.Contains(input.Filter!) ||
                 p.LastName.Contains(input.Filter!))
        .WhereIf(input.IsActive.HasValue, p => p.IsActive == input.IsActive);

    // Count FIRST (before pagination)
    var totalCount = await AsyncExecuter.CountAsync(query);

    // Then paginate and project
    var patients = await AsyncExecuter.ToListAsync(
        query
            .OrderBy(input.Sorting ?? nameof(Patient.LastName))
            .PageBy(input)  // ABP extension: Skip + Take
            .Select(p => new PatientDto { ... })
    );

    return new PagedResultDto<PatientDto>(totalCount, patients);
}
```

---

## Critical: Count Before Pagination

```csharp
// ✅ CORRECT: Count on unfiltered (by pagination) query
var totalCount = await query.CountAsync();
var items = await query.Skip(skip).Take(take).ToListAsync();

// ❌ WRONG: Count after Skip/Take (counts only the page!)
var items = await query.Skip(skip).Take(take).ToListAsync();
var totalCount = items.Count;  // Always <= pageSize!

// ❌ WRONG: Re-executing query for count
var items = await query.Skip(skip).Take(take).ToListAsync();
var totalCount = await query.CountAsync();  // Query executes AGAIN!
```

See [../anti-patterns/count-after-pagination.md](../anti-patterns/count-after-pagination.md) for details.

---

## Skip Count Optimization

For very large offsets, consider cursor-based pagination:

```csharp
// Offset pagination: Slow for large skip values
// Skip(10000) still scans 10000 rows

// Cursor pagination: O(1) regardless of position
public async Task<List<PatientDto>> GetPatientsAfterAsync(
    DateTime? lastCreatedAt,
    Guid? lastId,
    int take = 20)
{
    var query = await _patientRepository.GetQueryableAsync();

    if (lastCreatedAt.HasValue && lastId.HasValue)
    {
        // Cursor: Start after the last item seen
        query = query.Where(p =>
            p.CreationTime < lastCreatedAt.Value ||
            (p.CreationTime == lastCreatedAt.Value &&
             p.Id.CompareTo(lastId.Value) < 0));
    }

    return await query
        .OrderByDescending(p => p.CreationTime)
        .ThenByDescending(p => p.Id)
        .Take(take)
        .Select(p => new PatientDto { ... })
        .ToListAsync();
}
```

---

## Conditional Count

Skip count query when not needed (e.g., infinite scroll):

```csharp
public async Task<PagedResultDto<PatientDto>> GetListAsync(
    GetPatientsInput input,
    bool includeCount = true)  // Flag to skip count
{
    var query = await _patientRepository.GetQueryableAsync();
    query = ApplyFilters(query, input);

    long totalCount = 0;
    if (includeCount)
    {
        totalCount = await query.LongCountAsync();
    }

    var items = await query
        .OrderBy(input.Sorting ?? "CreationTime desc")
        .Skip(input.SkipCount)
        .Take(input.MaxResultCount)
        .Select(p => new PatientDto { ... })
        .ToListAsync();

    return new PagedResultDto<PatientDto>(totalCount, items);
}
```

---

## WhereIf Pattern

ABP's `WhereIf` for clean optional filters:

```csharp
var query = await _repository.GetQueryableAsync();

query = query
    .WhereIf(!filter.IsNullOrWhiteSpace(),
        x => x.Name.Contains(filter!))
    .WhereIf(status.HasValue,
        x => x.Status == status)
    .WhereIf(fromDate.HasValue,
        x => x.CreationTime >= fromDate)
    .WhereIf(toDate.HasValue,
        x => x.CreationTime <= toDate)
    .WhereIf(categoryId.HasValue,
        x => x.CategoryId == categoryId);
```

---

## Sorting with Dynamic Columns

```csharp
using System.Linq.Dynamic.Core;  // Required for string-based sorting

var query = await _repository.GetQueryableAsync();

// Dynamic sorting from input
var sortedQuery = query.OrderBy(
    input.Sorting.IsNullOrWhiteSpace()
        ? "CreationTime desc"
        : input.Sorting);

// Safe: Validate allowed sort columns
var allowedColumns = new[] { "Name", "CreationTime", "Status" };
var sortColumn = input.Sorting?.Split(' ')[0];
if (!allowedColumns.Contains(sortColumn))
{
    sortColumn = "CreationTime";
}
```

---

## Best Practices

| Do | Don't |
|----|-------|
| Count before Skip/Take | Count after pagination |
| Use `PageBy` extension | Manual Skip/Take calculation |
| Use `WhereIf` for optional filters | Null checks everywhere |
| Consider cursor for deep pages | Skip(100000) |
| Make count optional | Always count for infinite scroll |

---

## Related

- [projection.md](projection.md) - Combine with Select for efficiency
- [../anti-patterns/count-after-pagination.md](../anti-patterns/count-after-pagination.md) - Common mistake

---
