# Projection Pattern

Transform entities to DTOs at the database level, selecting only needed columns.

---

## When to Use

- Returning DTOs from AppService methods
- Need only subset of entity columns
- Computing aggregates (count, sum) in query
- Read-only operations (no entity tracking needed)

---

## Basic Projection

```csharp
public async Task<List<PatientListDto>> GetListAsync()
{
    var query = await _patientRepository.GetQueryableAsync();

    return await query
        .Select(p => new PatientListDto
        {
            Id = p.Id,
            FullName = $"{p.FirstName} {p.LastName}",
            Email = p.Email,
            IsActive = p.IsActive
        })
        .ToListAsync();
}
```

**Generated SQL** (only needed columns):
```sql
SELECT p.Id, p.FirstName, p.LastName, p.Email, p.IsActive
FROM Patients p
```

---

## Projection with Aggregates

Compute counts/sums at database level:

```csharp
return await query
    .Select(d => new DoctorSummaryDto
    {
        Id = d.Id,
        Name = d.FullName,
        AppointmentCount = d.Appointments.Count,  // Computed in DB
        TotalRevenue = d.Appointments.Sum(a => a.Fee),
        NextAppointment = d.Appointments
            .Where(a => a.Date > DateTime.UtcNow)
            .OrderBy(a => a.Date)
            .Select(a => a.Date)
            .FirstOrDefault()
    })
    .ToListAsync();
```

**Generated SQL**:
```sql
SELECT d.Id, d.FullName,
    (SELECT COUNT(*) FROM Appointments WHERE DoctorId = d.Id),
    (SELECT SUM(Fee) FROM Appointments WHERE DoctorId = d.Id),
    (SELECT TOP 1 Date FROM Appointments WHERE DoctorId = d.Id AND Date > @now ORDER BY Date)
FROM Doctors d
```

---

## Projection with Related Data

Include related entity fields without loading full entities:

```csharp
return await query
    .Select(a => new AppointmentDto
    {
        Id = a.Id,
        Date = a.AppointmentDate,
        PatientName = $"{a.Patient.FirstName} {a.Patient.LastName}",
        DoctorName = a.Doctor.FullName,
        Status = a.Status
    })
    .ToListAsync();
```

---

## AsNoTracking (Implicit)

Projections to non-entity types are automatically untracked:

```csharp
// AsNoTracking is IMPLICIT when projecting to DTO
var dtos = await query
    .Select(p => new PatientDto { ... })
    .ToListAsync();

// Explicit AsNoTracking only needed when returning entities
var entities = await query
    .AsNoTracking()  // Explicit needed here
    .ToListAsync();
```

---

## Conditional Projection

Return different shapes based on parameters:

```csharp
public async Task<PatientDto> GetAsync(Guid id, bool includeDetails = false)
{
    var query = await _patientRepository.GetQueryableAsync();

    if (includeDetails)
    {
        return await query
            .Where(p => p.Id == id)
            .Select(p => new PatientDto
            {
                Id = p.Id,
                FullName = $"{p.FirstName} {p.LastName}",
                Email = p.Email,
                // Include extra fields
                Appointments = p.Appointments.Select(a => new AppointmentDto
                {
                    Id = a.Id,
                    Date = a.AppointmentDate
                }).ToList()
            })
            .FirstOrDefaultAsync();
    }

    return await query
        .Where(p => p.Id == id)
        .Select(p => new PatientDto
        {
            Id = p.Id,
            FullName = $"{p.FirstName} {p.LastName}"
        })
        .FirstOrDefaultAsync();
}
```

---

## Select vs Include

| Use Projection (Select) | Use Include |
|------------------------|-------------|
| Returning DTOs | Need full entity for update |
| Read-only operations | Will modify related entities |
| Specific columns only | Need all entity properties |
| Computing aggregates | Need navigation for business logic |

---

## Anti-Pattern: Load Then Map

```csharp
// ❌ Bad: Loads all columns, maps in memory
var entities = await query.ToListAsync();
var dtos = entities.Select(e => new Dto { Id = e.Id, Name = e.Name });

// ✅ Good: Maps at database level
var dtos = await query
    .Select(e => new Dto { Id = e.Id, Name = e.Name })
    .ToListAsync();
```

---

## Best Practices

| Do | Don't |
|----|-------|
| Project to DTO in query | Load entity then map |
| Include only needed columns | Select * equivalent |
| Compute aggregates in projection | Load all then count in memory |
| Use `Select` with `FirstOrDefault` | `First()` then map |

---

## Related

- [eager-loading.md](eager-loading.md) - When full entities needed
- [pagination.md](pagination.md) - Projection with paging
- [../anti-patterns/full-table-load.md](../anti-patterns/full-table-load.md) - What projection prevents

---
