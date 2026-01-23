# N+1 Query Anti-Pattern

Executing N additional queries to load related data for N parent entities.

---

## Metadata

| Field | Value |
|-------|-------|
| **Severity** | 🔴 HIGH |
| **Category** | Performance |
| **Detect** | `foreach.*await.*Repository` |
| **Impact** | N+1 database round trips |

---

## Concept

The N+1 query problem occurs when code:
1. Executes 1 query to load N parent entities
2. Executes N additional queries to load related data for each parent

**Example**: Loading 100 doctors with their appointments:
- Without fix: 1 + 100 = **101 queries**
- With fix: **1-2 queries**

---

## Detection

### Grep Patterns

```bash
# Query inside foreach
grep -rn "foreach.*await.*Repository\|foreach.*await.*GetAsync" src/

# Query inside for loop
grep -rn "for.*await.*Repository\|for.*await.*GetListAsync" src/

# Select with async
grep -rn "\.Select.*async.*await" src/
```

### Code Patterns to Watch

```csharp
// Pattern 1: foreach with await
foreach (var item in items)
{
    item.Related = await _repo.GetAsync(...);  // ❌
}

// Pattern 2: for loop with query
for (int i = 0; i < items.Count; i++)
{
    items[i].Related = await _repo.GetListAsync(...);  // ❌
}

// Pattern 3: Select with async (subtle)
var results = await Task.WhenAll(
    items.Select(async i => await _repo.GetAsync(i.RelatedId))  // ❌
);
```

---

## Bad Example

```csharp
public async Task<List<DoctorDto>> GetDoctorsWithAppointmentsAsync()
{
    var doctors = await _doctorRepository.GetListAsync();  // Query 1

    foreach (var doctor in doctors)
    {
        // ❌ Executes N times! (one per doctor)
        doctor.Appointments = await _appointmentRepository
            .GetListAsync(a => a.DoctorId == doctor.Id);
    }

    return doctors.Select(d => d.ToDto()).ToList();
}
```

**Query Log** (for 100 doctors):
```sql
SELECT * FROM Doctors                           -- Query 1
SELECT * FROM Appointments WHERE DoctorId = @p0 -- Query 2
SELECT * FROM Appointments WHERE DoctorId = @p1 -- Query 3
SELECT * FROM Appointments WHERE DoctorId = @p2 -- Query 4
... (97 more queries)
```

**Total: 101 queries, ~101 round trips**

---

## Fix 1: Eager Loading (Include)

**When**: Same DbContext, always need related data.

```csharp
public async Task<List<DoctorDto>> GetDoctorsWithAppointmentsAsync()
{
    var query = await _doctorRepository.GetQueryableAsync();

    var doctors = await query
        .Include(d => d.Appointments)  // ✅ JOIN in single query
        .ToListAsync();

    return doctors.Select(d => d.ToDto()).ToList();
}
```

**Query Log**:
```sql
SELECT d.*, a.*
FROM Doctors d
LEFT JOIN Appointments a ON d.Id = a.DoctorId  -- Single query!
```

**Total: 1 query**

See [../patterns/eager-loading.md](../patterns/eager-loading.md) for details.

---

## Fix 2: Batch Loading (Dictionary)

**When**: Different repositories, need O(1) lookup.

```csharp
public async Task<List<DoctorDto>> GetDoctorsWithAppointmentsAsync()
{
    // Query 1: Load all doctors
    var doctors = await _doctorRepository.GetListAsync();
    var doctorIds = doctors.Select(d => d.Id).ToList();

    // Query 2: Load ALL appointments for these doctors
    var appointments = await (await _appointmentRepository.GetQueryableAsync())
        .Where(a => doctorIds.Contains(a.DoctorId))
        .ToListAsync();

    // O(1) lookup via dictionary
    var appointmentsByDoctor = appointments
        .GroupBy(a => a.DoctorId)
        .ToDictionary(g => g.Key, g => g.ToList());

    // Join in memory (no more queries)
    foreach (var doctor in doctors)
    {
        doctor.Appointments = appointmentsByDoctor
            .GetValueOrDefault(doctor.Id, new List<Appointment>());
    }

    return doctors.Select(d => d.ToDto()).ToList();
}
```

**Query Log**:
```sql
SELECT * FROM Doctors                                      -- Query 1
SELECT * FROM Appointments WHERE DoctorId IN (@p0, @p1...) -- Query 2
```

**Total: 2 queries** (regardless of N doctors)

See [../patterns/batch-loading.md](../patterns/batch-loading.md) for details.

---

## Fix 3: Projection (Best for DTOs)

**When**: Only need computed values, not full related entities.

```csharp
public async Task<List<DoctorSummaryDto>> GetDoctorSummariesAsync()
{
    var query = await _doctorRepository.GetQueryableAsync();

    return await query
        .Select(d => new DoctorSummaryDto
        {
            Id = d.Id,
            Name = d.FullName,
            // ✅ Computed in database, not N+1!
            AppointmentCount = d.Appointments.Count,
            NextAppointment = d.Appointments
                .Where(a => a.Date > DateTime.UtcNow)
                .OrderBy(a => a.Date)
                .Select(a => a.Date)
                .FirstOrDefault()
        })
        .ToListAsync();
}
```

**Query Log**:
```sql
SELECT d.Id, d.FullName,
    (SELECT COUNT(*) FROM Appointments WHERE DoctorId = d.Id),
    (SELECT TOP 1 Date FROM Appointments WHERE DoctorId = d.Id
     WHERE Date > @now ORDER BY Date)
FROM Doctors d  -- Single optimized query!
```

**Total: 1 query**

See [../patterns/projection.md](../patterns/projection.md) for details.

---

## Variant: FirstOrDefault in Loop

A subtle N+1 that happens in memory:

```csharp
// ❌ Bad: O(n×m) complexity
var result = categories.Select(cat => new CategoryDto
{
    Name = cat.Name,
    // FirstOrDefault scans ALL items for EACH category!
    TopItem = items.FirstOrDefault(i => i.CategoryId == cat.Id)
}).ToList();
```

**Complexity**: 100 categories × 1000 items = 100,000 iterations

```csharp
// ✅ Good: O(n+m) complexity
var itemsByCategory = items
    .GroupBy(i => i.CategoryId)
    .ToDictionary(g => g.Key, g => g.First());

var result = categories.Select(cat => new CategoryDto
{
    Name = cat.Name,
    TopItem = itemsByCategory.GetValueOrDefault(cat.Id)  // O(1)
}).ToList();
```

**Complexity**: 1000 (build dict) + 100 (lookups) = 1,100 operations

---

## Decision Guide

| Scenario | Best Fix |
|----------|----------|
| Same DbContext, need full entities | Include (eager loading) |
| Different repositories | Batch loading (Dictionary) |
| Only need aggregates/computed | Projection (Select) |
| Multiple collection includes | AsSplitQuery + Include |

---

## Related

- [../patterns/eager-loading.md](../patterns/eager-loading.md) - Include solution
- [../patterns/batch-loading.md](../patterns/batch-loading.md) - Dictionary solution
- [../patterns/projection.md](../patterns/projection.md) - Select solution
- [in-memory-join.md](in-memory-join.md) - Related anti-pattern

---
