# Full Table Load Anti-Pattern

Loading entire table into memory, then filtering with LINQ.

---

## Metadata

| Field | Value |
|-------|-------|
| **Severity** | 🔴 HIGH |
| **Category** | Performance / Memory |
| **Detect** | `GetListAsync()` then `.Where` |
| **Impact** | Memory explosion, slow queries |

---

## Concept

This anti-pattern occurs when code:
1. Loads ALL records from a table into memory
2. Then filters using LINQ-to-Objects

The database is bypassed for filtering, causing:
- All rows transferred over network
- All objects instantiated in memory
- Filtering happens in application, not database

---

## Detection

### Grep Patterns

```bash
# GetListAsync followed by Where
grep -rn "GetListAsync().*\.Where\|GetListAsync()\n.*\.Where" src/

# ToListAsync followed by LINQ
grep -rn "ToListAsync().*\.Where\|ToListAsync().*\.FirstOrDefault" src/

# Assigning to variable then filtering
grep -rn "= await.*GetListAsync\|= await.*ToListAsync" src/
```

### Code Review Signs

- Variable assigned from `GetListAsync()` without parameters
- In-memory LINQ after `ToListAsync()`
- Multiple collections loaded then joined in memory

---

## Bad Example

```csharp
public async Task<List<PatientDto>> GetActivePatientsAsync()
{
    // ❌ Loads ALL patients (could be 100,000+)
    var allPatients = await _patientRepository.GetListAsync();

    // ❌ Filters in memory (database ignored)
    var activePatients = allPatients
        .Where(p => p.IsActive)
        .ToList();

    return activePatients.ToDto();
}
```

**What happens**:
```sql
SELECT * FROM Patients  -- Returns 100,000 rows
```
Then C# iterates 100,000 objects to find active ones.

---

## Fix: Filter at Database Level

```csharp
public async Task<List<PatientDto>> GetActivePatientsAsync()
{
    // ✅ Filter at database level
    var activePatients = await (await _patientRepository.GetQueryableAsync())
        .Where(p => p.IsActive)
        .ToListAsync();

    return activePatients.ToDto();
}
```

**What happens**:
```sql
SELECT * FROM Patients WHERE IsActive = 1  -- Returns only active
```

---

## Bad Example: Validation with Full Load

```csharp
public async Task ValidateImportAsync(List<ImportDto> items)
{
    // ❌ Loads ENTIRE tables for validation
    var allProjects = await _projectRepository.GetListAsync();
    var allCustomers = await _customerRepository.GetListAsync();
    var allProducts = await _productRepository.GetListAsync();

    foreach (var item in items)
    {
        // In-memory lookup
        var project = allProjects.FirstOrDefault(p => p.Code == item.ProjectCode);
        if (project == null)
        {
            errors.Add($"Invalid project: {item.ProjectCode}");
        }
        // ... more validations
    }
}
```

---

## Fix: Load Only What's Needed

```csharp
public async Task ValidateImportAsync(List<ImportDto> items)
{
    // Extract unique values from import
    var projectCodes = items.Select(x => x.ProjectCode).Distinct().ToList();
    var customerNames = items.Select(x => x.CustomerName).Distinct().ToList();

    // ✅ Load only matching records
    var projects = await (await _projectRepository.GetQueryableAsync())
        .Where(p => projectCodes.Contains(p.Code))
        .ToDictionaryAsync(p => p.Code, p => p);

    var customers = await (await _customerRepository.GetQueryableAsync())
        .Where(c => customerNames.Contains(c.Name))
        .ToDictionaryAsync(c => c.Name, c => c);

    foreach (var item in items)
    {
        if (!projects.ContainsKey(item.ProjectCode))
        {
            errors.Add($"Invalid project: {item.ProjectCode}");
        }
        // ... more validations with O(1) dictionary lookup
    }
}
```

---

## Bad Example: Multiple Tables Joined in Memory

```csharp
public async Task<MenusByCategoryDto> GetMenusGroupedAsync()
{
    // ❌ Loads ALL records from 3 tables
    var categories = await _categoryRepo.GetListAsync();
    var menus = await _menuRepo.GetListAsync();
    var mappings = await _mappingRepo.GetListAsync();

    // ❌ Joins in memory
    return categories.Select(c => new CategoryDto
    {
        Name = c.Name,
        Menus = menus.Where(m => m.CategoryId == c.Id).ToList()
    }).ToList();
}
```

---

## Fix: Query with Joins or Projection

```csharp
public async Task<MenusByCategoryDto> GetMenusGroupedAsync()
{
    // ✅ Join at database level
    var query = from c in await _categoryRepo.GetQueryableAsync()
                join m in await _menuRepo.GetQueryableAsync()
                    on c.Id equals m.CategoryId into menus
                where c.IsActive
                select new CategoryDto
                {
                    Name = c.Name,
                    Menus = menus.Select(m => new MenuDto
                    {
                        Id = m.Id,
                        Name = m.Name
                    }).ToList()
                };

    return await query.ToListAsync();
}
```

Or with Include:

```csharp
var categories = await (await _categoryRepo.GetQueryableAsync())
    .Include(c => c.Menus)
    .Where(c => c.IsActive)
    .ToListAsync();
```

---

## When Full Load is Acceptable

| Acceptable | Not Acceptable |
|------------|----------------|
| Lookup tables (< 100 rows, rarely changes) | Transaction tables |
| Cached reference data | Growing datasets |
| Enum-like data | User/customer data |
| Configuration | Audit logs |

```csharp
// Acceptable: Small, static reference data
var statuses = await _statusRepository.GetListAsync();  // 10 rows, cached

// Not acceptable: Transaction data
var orders = await _orderRepository.GetListAsync();  // 1M+ rows
```

---

## Related

- [in-memory-join.md](in-memory-join.md) - Related anti-pattern
- [../patterns/projection.md](../patterns/projection.md) - Alternative approach
- [../patterns/batch-loading.md](../patterns/batch-loading.md) - For validation scenarios

---
