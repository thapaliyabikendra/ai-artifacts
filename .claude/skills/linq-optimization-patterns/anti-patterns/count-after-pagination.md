# Count After Pagination Anti-Pattern

Executing count query after pagination, causing double query execution or wrong counts.

---

## Metadata

| Field | Value |
|-------|-------|
| **Severity** | 🔴 HIGH |
| **Category** | Performance |
| **Detect** | `Count.*after.*ToList\|ToList.*Count` |
| **Impact** | Double query execution |

---

## Concept

When implementing paginated lists, the total count must be obtained **before** applying Skip/Take. Counting after pagination either:
1. Returns wrong count (only counts the page)
2. Executes the query twice

---

## Detection

### Grep Patterns

```bash
# Count after ToList
grep -rn "ToListAsync.*\n.*Count\|ToList.*\.Count" src/

# Sync count after async list
grep -rn "ToListAsync.*CountAsync\|CountAsync.*after" src/

# Count on paginated result
grep -rn "\.Count().*Skip\|\.Count.*Take" src/
```

---

## Bad Example 1: Wrong Count

```csharp
public async Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientsInput input)
{
    var query = await _patientRepository.GetQueryableAsync();

    // ❌ Pagination applied first
    var patients = await query
        .Skip(input.SkipCount)
        .Take(input.MaxResultCount)
        .ToListAsync();

    // ❌ Count on paginated result = always <= MaxResultCount!
    var totalCount = patients.Count;

    return new PagedResultDto<PatientDto>(totalCount, patients.ToDto());
}
```

**Problem**: If there are 1000 patients and page size is 20, `totalCount` will be 20, not 1000.

---

## Bad Example 2: Double Query

```csharp
public async Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientsInput input)
{
    var query = await _patientRepository.GetQueryableAsync();

    // Query 1: Get data
    var patients = await query
        .Skip(input.SkipCount)
        .Take(input.MaxResultCount)
        .ToListAsync();

    // ❌ Query 2: Count executes the ENTIRE query again!
    var totalCount = await query.CountAsync();

    return new PagedResultDto<PatientDto>(totalCount, patients.ToDto());
}
```

**Problem**: The `CountAsync()` re-executes the full query. With complex filters, this can be expensive.

---

## Fix: Count Before Pagination

```csharp
public async Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientsInput input)
{
    var query = await _patientRepository.GetQueryableAsync();

    // Apply filters (shared by count and data queries)
    query = query
        .WhereIf(!input.Filter.IsNullOrWhiteSpace(),
            p => p.FirstName.Contains(input.Filter!) ||
                 p.LastName.Contains(input.Filter!))
        .WhereIf(input.IsActive.HasValue, p => p.IsActive == input.IsActive);

    // ✅ Count FIRST (on filtered but unpaginated query)
    var totalCount = await AsyncExecuter.CountAsync(query);

    // ✅ Then paginate
    var patients = await AsyncExecuter.ToListAsync(
        query
            .OrderBy(input.Sorting ?? nameof(Patient.LastName))
            .Skip(input.SkipCount)
            .Take(input.MaxResultCount)
    );

    return new PagedResultDto<PatientDto>(totalCount, patients.ToDto());
}
```

**Queries executed**:
1. `SELECT COUNT(*) FROM Patients WHERE ...` (count)
2. `SELECT * FROM Patients WHERE ... ORDER BY ... OFFSET ... FETCH ...` (data)

---

## ABP Pattern

Using ABP's `AsyncExecuter`:

```csharp
// ✅ ABP recommended pattern
var totalCount = await AsyncExecuter.CountAsync(query);
var items = await AsyncExecuter.ToListAsync(
    query
        .OrderBy(input.Sorting.IsNullOrWhiteSpace() ? "Id" : input.Sorting)
        .PageBy(input)  // ABP extension for Skip/Take
);
```

---

## Optimization: Skip Count When Not Needed

For infinite scroll or when count isn't displayed:

```csharp
public async Task<PagedResultDto<PatientDto>> GetListAsync(
    GetPatientsInput input,
    bool includeCount = true)
{
    var query = await _patientRepository.GetQueryableAsync();
    query = ApplyFilters(query, input);

    // Only count when needed
    long totalCount = 0;
    if (includeCount)
    {
        totalCount = await query.LongCountAsync();
    }

    var items = await query
        .OrderBy(input.Sorting ?? "Id")
        .Skip(input.SkipCount)
        .Take(input.MaxResultCount)
        .ToListAsync();

    return new PagedResultDto<PatientDto>(totalCount, items.ToDto());
}
```

---

## Visual Summary

```
❌ WRONG ORDER:
┌─────────────────────────────────────────┐
│ query.Skip().Take().ToList()            │ ── Data (20 items)
│ items.Count                             │ ── Wrong! Returns 20
└─────────────────────────────────────────┘

❌ DOUBLE QUERY:
┌─────────────────────────────────────────┐
│ query.Skip().Take().ToList()            │ ── Query 1
│ query.CountAsync()                      │ ── Query 2 (duplicates work!)
└─────────────────────────────────────────┘

✅ CORRECT ORDER:
┌─────────────────────────────────────────┐
│ query.CountAsync()                      │ ── Count (1000)
│ query.Skip().Take().ToList()            │ ── Data (20 items)
└─────────────────────────────────────────┘
```

---

## Related

- [../patterns/pagination.md](../patterns/pagination.md) - Correct pagination pattern
- [full-table-load.md](full-table-load.md) - Another pagination-related issue

---
