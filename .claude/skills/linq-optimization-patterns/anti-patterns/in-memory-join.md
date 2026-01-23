# In-Memory Join Anti-Pattern

Loading multiple tables to memory, then joining with LINQ-to-Objects.

---

## Metadata

| Field | Value |
|-------|-------|
| **Severity** | 🔴 HIGH |
| **Category** | Performance / Memory |
| **Detect** | Multiple `ToListAsync` then LINQ join |
| **Impact** | Cartesian product in memory, OOM risk |

---

## Concept

This anti-pattern occurs when code:
1. Loads multiple tables entirely into memory
2. Joins them using LINQ-to-Objects
3. Database join optimization is completely bypassed

This causes:
- Multiple large result sets in memory
- Cartesian explosion risk
- No database query optimization

---

## Detection

### Grep Patterns

```bash
# Multiple ToListAsync in same method
grep -rn "ToListAsync.*ToListAsync\|GetListAsync.*GetListAsync" src/

# Sequential loads followed by LINQ
grep -rn "\.ToListAsync();\n.*\.ToListAsync()" src/

# In-memory Where after load
grep -rn "categories\.Select.*menus\.Where" src/
```

### Code Review Signs

- Multiple `await _repository.GetListAsync()` calls
- Collections stored in variables then filtered
- `.Where()` referencing other loaded collections

---

## Bad Example

```csharp
public async Task<List<CategoryWithMenusDto>> GetCategoriesWithMenusAsync()
{
    // ❌ Load all categories (500 rows)
    var categories = await (await _categoryRepo.GetQueryableAsync())
        .ToListAsync();

    // ❌ Load all menus (5,000 rows)
    var menus = await (await _menuRepo.GetQueryableAsync())
        .ToListAsync();

    // ❌ Load all mappings (10,000 rows)
    var mappings = await (await _mappingRepo.GetQueryableAsync())
        .ToListAsync();

    // ❌ Join in memory
    var result = categories.Select(c => new CategoryWithMenusDto
    {
        Id = c.Id,
        Name = c.Name,
        Menus = menus
            .Where(m => m.CategoryId == c.Id)  // O(n) scan per category!
            .Select(m => new MenuDto
            {
                Id = m.Id,
                Name = m.Name,
                // Another O(n) scan!
                PageId = mappings.FirstOrDefault(mp => mp.MenuId == m.Id)?.PageId
            })
            .ToList()
    }).ToList();

    return result;
}
```

**Problems**:
- 15,500 objects loaded to memory
- O(categories × menus × mappings) complexity
- Database indexes completely ignored

---

## Fix 1: Database Join with Projection

```csharp
public async Task<List<CategoryWithMenusDto>> GetCategoriesWithMenusAsync()
{
    var categoryQuery = await _categoryRepo.GetQueryableAsync();
    var menuQuery = await _menuRepo.GetQueryableAsync();
    var mappingQuery = await _mappingRepo.GetQueryableAsync();

    // ✅ Join at database level
    var query = from c in categoryQuery
                where c.IsActive
                select new CategoryWithMenusDto
                {
                    Id = c.Id,
                    Name = c.Name,
                    Menus = (from m in menuQuery
                             where m.CategoryId == c.Id && m.IsActive
                             join mp in mappingQuery on m.Id equals mp.MenuId into mappings
                             from mp in mappings.DefaultIfEmpty()
                             select new MenuDto
                             {
                                 Id = m.Id,
                                 Name = m.Name,
                                 PageId = mp != null ? mp.PageId : (Guid?)null
                             }).ToList()
                };

    return await query.ToListAsync();
}
```

---

## Fix 2: Eager Loading with Include

```csharp
public async Task<List<CategoryWithMenusDto>> GetCategoriesWithMenusAsync()
{
    var categories = await (await _categoryRepo.GetQueryableAsync())
        .Include(c => c.Menus)
            .ThenInclude(m => m.PageMapping)
        .Where(c => c.IsActive)
        .AsSplitQuery()  // Avoid Cartesian with multiple collections
        .ToListAsync();

    return categories.Select(c => new CategoryWithMenusDto
    {
        Id = c.Id,
        Name = c.Name,
        Menus = c.Menus.Select(m => new MenuDto
        {
            Id = m.Id,
            Name = m.Name,
            PageId = m.PageMapping?.PageId
        }).ToList()
    }).ToList();
}
```

---

## Fix 3: Batch Loading with Dictionary

When Include isn't possible (different DbContexts):

```csharp
public async Task<List<CategoryWithMenusDto>> GetCategoriesWithMenusAsync()
{
    // Load categories (filtered)
    var categories = await (await _categoryRepo.GetQueryableAsync())
        .Where(c => c.IsActive)
        .ToListAsync();

    var categoryIds = categories.Select(c => c.Id).ToList();

    // ✅ Batch load related data (single query each)
    var menus = await (await _menuRepo.GetQueryableAsync())
        .Where(m => categoryIds.Contains(m.CategoryId))
        .ToListAsync();

    var menuIds = menus.Select(m => m.Id).ToList();

    var mappings = await (await _mappingRepo.GetQueryableAsync())
        .Where(mp => menuIds.Contains(mp.MenuId))
        .ToDictionaryAsync(mp => mp.MenuId, mp => mp.PageId);

    // ✅ O(1) dictionary lookups
    var menusByCategory = menus
        .GroupBy(m => m.CategoryId)
        .ToDictionary(g => g.Key, g => g.ToList());

    return categories.Select(c => new CategoryWithMenusDto
    {
        Id = c.Id,
        Name = c.Name,
        Menus = menusByCategory.GetValueOrDefault(c.Id, new())
            .Select(m => new MenuDto
            {
                Id = m.Id,
                Name = m.Name,
                PageId = mappings.GetValueOrDefault(m.Id)
            }).ToList()
    }).ToList();
}
```

**Queries**: 3 (regardless of data size)

---

## Visual Comparison

```
❌ IN-MEMORY JOIN:
┌─────────────────────────────────────────────────────────────┐
│ Categories (500) ────────┐                                  │
│ Menus (5,000) ───────────┼──► Memory ──► LINQ Join          │
│ Mappings (10,000) ───────┘             (O(n×m×p) scans)     │
└─────────────────────────────────────────────────────────────┘

✅ DATABASE JOIN:
┌─────────────────────────────────────────────────────────────┐
│ Single Query with JOINs ──► Database ──► Optimized Result   │
│ (Uses indexes, query planner)                               │
└─────────────────────────────────────────────────────────────┘

✅ BATCH + DICTIONARY:
┌─────────────────────────────────────────────────────────────┐
│ Query 1: Categories (filtered) ─┐                           │
│ Query 2: Menus (filtered) ──────┼──► Dictionary ──► O(1)    │
│ Query 3: Mappings (filtered) ───┘    Lookups                │
└─────────────────────────────────────────────────────────────┘
```

---

## Decision Guide

| Scenario | Best Approach |
|----------|---------------|
| Same DbContext, navigation properties | Include + AsSplitQuery |
| Need complex projection | Database JOIN in query |
| Different DbContexts | Batch load + Dictionary |
| Small reference tables | Load once, cache |

---

## Related

- [full-table-load.md](full-table-load.md) - Simpler version of this problem
- [n-plus-one.md](n-plus-one.md) - Related performance issue
- [../patterns/batch-loading.md](../patterns/batch-loading.md) - Fix pattern
- [../patterns/eager-loading.md](../patterns/eager-loading.md) - Include approach

---
