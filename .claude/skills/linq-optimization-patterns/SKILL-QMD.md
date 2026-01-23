---
name: linq-optimization-patterns
description: "LINQ and EF Core query optimization for ABP Framework."
keywords: [N+1, Include, projection, pagination, CountAsync, ToListAsync]
version: 2.0
---

# LINQ Optimization Patterns

## Summary

Optimize LINQ queries and prevent common performance anti-patterns in EF Core/ABP applications. Focus: N+1 prevention, efficient pagination, projections.

---

## Quick Reference

| Problem | Solution | Severity | Detect |
|---------|----------|----------|--------|
| N+1 queries | Include or batch load | HIGH | `foreach.*await.*Repository` |
| Count after pagination | Count first | HIGH | `\.Count\(\).*ToList` |
| Load full table | Filter with GetQueryableAsync | HIGH | `GetListAsync\(\)` then filter |
| FirstOrDefault in loop | ToDictionary lookup | MEDIUM | `\.FirstOrDefault.*inside.*Select` |
| Missing projection | Select to DTO | MEDIUM | `ToListAsync()` then map |

---

## Patterns

### Eager Loading

**When**: Need related entities in single query.

```csharp
var doctors = await query
    .Include(d => d.Appointments)
    .ToListAsync();
```

### Batch Loading

**When**: Need related data for multiple parents.

```csharp
var doctorIds = doctors.Select(d => d.Id).ToList();
var appointments = await _repo.GetQueryableAsync()
    .Where(a => doctorIds.Contains(a.DoctorId))
    .GroupBy(a => a.DoctorId)
    .ToDictionaryAsync(g => g.Key, g => g.ToList());
```

### Projection

**When**: Returning DTOs, not full entities.

```csharp
return await query
    .Select(p => new PatientDto { Id = p.Id, Name = p.FullName })
    .ToListAsync();
```

### Count Before Pagination

**When**: Need total count with paged results.

```csharp
var totalCount = await query.CountAsync();  // Count FIRST
var items = await query.Skip(skip).Take(take).ToListAsync();
```

---

## Anti-Patterns

### N+1 Query

**Severity**: HIGH
**Detect**: `foreach.*await.*Repository|\.GetListAsync.*inside.*loop`

**Bad**:
```csharp
foreach (var doctor in doctors)
{
    // Executes query N times!
    doctor.Appointments = await _repo.GetListAsync(a => a.DoctorId == doctor.Id);
}
```

**Why**: Executes 1 + N database queries. 100 doctors = 101 queries.

**Fix**:
```csharp
var doctorIds = doctors.Select(d => d.Id).ToList();
var appointments = await (await _repo.GetQueryableAsync())
    .Where(a => doctorIds.Contains(a.DoctorId))
    .ToListAsync();
var grouped = appointments.GroupBy(a => a.DoctorId).ToDictionary(g => g.Key, g => g.ToList());

foreach (var doctor in doctors)
{
    doctor.Appointments = grouped.GetValueOrDefault(doctor.Id, new());
}
```

---

### Count After Pagination

**Severity**: HIGH
**Detect**: `\.Count\(\).*after.*ToListAsync|ToListAsync.*then.*Count`

**Bad**:
```csharp
var items = await query.Skip(skip).Take(take).ToListAsync();
var total = query.Count();  // Executes AGAIN!
```

**Why**: Runs the query twice - once for data, once for count.

**Fix**:
```csharp
var total = await query.CountAsync();  // Count FIRST
var items = await query.Skip(skip).Take(take).ToListAsync();
```

---

### Load Full Table

**Severity**: HIGH
**Detect**: `GetListAsync\(\).*then.*Where|ToListAsync\(\).*\.Where`

**Bad**:
```csharp
var allMenus = await _menuRepository.GetListAsync();  // Loads ALL
var activeMenus = allMenus.Where(x => x.IsActive);    // Filters in memory
```

**Why**: Loads entire table into memory before filtering. Table with 10K rows = 10K objects in memory.

**Fix**:
```csharp
var activeMenus = await (await _menuRepository.GetQueryableAsync())
    .Where(x => x.IsActive)
    .ToListAsync();  // Filters at database level
```

---

### FirstOrDefault in Loop

**Severity**: MEDIUM
**Detect**: `\.FirstOrDefault.*inside.*Select|Select\(.*FirstOrDefault`

**Bad**:
```csharp
var result = categories.Select(cat => new CategoryDto
{
    Name = cat.Name,
    // FirstOrDefault runs for EACH category!
    TopItem = items.FirstOrDefault(i => i.CategoryId == cat.Id)
}).ToList();
```

**Why**: O(n*m) complexity. 100 categories × 1000 items = 100,000 iterations.

**Fix**:
```csharp
var itemsByCategory = items.GroupBy(i => i.CategoryId)
    .ToDictionary(g => g.Key, g => g.First());

var result = categories.Select(cat => new CategoryDto
{
    Name = cat.Name,
    TopItem = itemsByCategory.GetValueOrDefault(cat.Id)  // O(1) lookup
}).ToList();
```

---

### In-Memory Join

**Severity**: HIGH
**Detect**: `ToListAsync.*ToListAsync.*then.*join|multiple.*GetListAsync.*then.*linq`

**Bad**:
```csharp
var categories = await _categoryRepo.GetQueryableAsync().ToListAsync();
var menus = await _menuRepo.GetQueryableAsync().ToListAsync();
var mappings = await _mappingRepo.GetQueryableAsync().ToListAsync();

// All data in memory, then LINQ join
var result = categories.Select(c => new {
    Category = c,
    Menus = menus.Where(m => m.CategoryId == c.Id)
});
```

**Why**: Loads all tables to memory. Memory explosion with large datasets.

**Fix**:
```csharp
var query = from c in await _categoryRepo.GetQueryableAsync()
            join m in await _menuRepo.GetQueryableAsync() on c.Id equals m.CategoryId
            select new { Category = c.Name, Menu = m.Name };

var result = await query.ToListAsync();  // Single query with join
```

---

## Rules

### R001: Count Before Pagination
Always execute `CountAsync()` before applying `Skip/Take`.

### R002: Filter at Database
Apply `Where` clauses before `ToListAsync()`, not after.

### R003: Batch Related Data
Load related entities in batch, not inside loops.

### R004: Project to DTOs
Use `Select()` projection instead of loading full entities.

---

## Checklist

- [ ] No `foreach` with `await` repository calls inside
- [ ] Count executed before Skip/Take
- [ ] No `GetListAsync()` followed by `.Where()` in memory
- [ ] No `FirstOrDefault` inside `Select` projections
- [ ] Related data loaded via Include or batch query
- [ ] Projections used for DTO returns

---
