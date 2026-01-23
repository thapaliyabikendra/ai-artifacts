# Eager Loading Pattern

Load related entities in a single database query using JOIN operations.

---

## When to Use

- Need related entities for a single parent
- Related data is always needed (not conditional)
- Avoiding N+1 queries for navigation properties

---

## Basic Include

```csharp
var query = await _appointmentRepository.GetQueryableAsync();

var appointments = await query
    .Include(a => a.Patient)
    .Include(a => a.Doctor)
    .ToListAsync();
```

**Generated SQL**:
```sql
SELECT a.*, p.*, d.*
FROM Appointments a
LEFT JOIN Patients p ON a.PatientId = p.Id
LEFT JOIN Doctors d ON a.DoctorId = d.Id
```

---

## Nested Include (ThenInclude)

For multi-level relationships:

```csharp
var doctors = await (await _doctorRepository.GetQueryableAsync())
    .Include(d => d.Appointments)
        .ThenInclude(a => a.Patient)
    .Include(d => d.Specializations)
        .ThenInclude(s => s.Specialization)
    .ToListAsync();
```

---

## ABP WithDetails

ABP provides `WithDetailsAsync()` for default includes:

```csharp
public class DoctorRepository : EfCoreRepository<ClinicDbContext, Doctor, Guid>, IDoctorRepository
{
    public async Task<Doctor> GetWithAppointmentsAsync(Guid id)
    {
        var query = await WithDetailsAsync();
        return await query.FirstOrDefaultAsync(d => d.Id == id);
    }

    public override async Task<IQueryable<Doctor>> WithDetailsAsync()
    {
        return (await GetQueryableAsync())
            .Include(d => d.Appointments)
            .Include(d => d.Specializations);
    }
}
```

---

## Split Queries

When including multiple collections, use `AsSplitQuery()` to avoid Cartesian explosion:

```csharp
// Without split: Cartesian product (doctors × appointments × schedules)
// With split: 3 separate queries, combined in memory

var doctors = await (await _doctorRepository.GetQueryableAsync())
    .Include(d => d.Appointments)
    .Include(d => d.Schedules)
    .Include(d => d.Specializations)
    .AsSplitQuery()  // Executes 4 queries instead of 1 massive join
    .ToListAsync();
```

**When to use AsSplitQuery**:
- Including 2+ collection navigation properties
- Large datasets where Cartesian product would explode
- When individual queries are faster than complex join

---

## Conditional Include

Include only when needed:

```csharp
public async Task<DoctorDto> GetAsync(Guid id, bool includeAppointments = false)
{
    var query = await _doctorRepository.GetQueryableAsync();

    if (includeAppointments)
    {
        query = query.Include(d => d.Appointments);
    }

    var doctor = await query.FirstOrDefaultAsync(d => d.Id == id);
    return doctor.ToDto();
}
```

---

## Filtered Include (EF Core 5+)

Include only specific related entities:

```csharp
var doctors = await (await _doctorRepository.GetQueryableAsync())
    .Include(d => d.Appointments.Where(a => a.Status == AppointmentStatus.Scheduled))
    .ToListAsync();
```

---

## Best Practices

| Do | Don't |
|----|-------|
| Use `Include` for always-needed relations | Include everything "just in case" |
| Use `AsSplitQuery` for multiple collections | Ignore Cartesian explosion warnings |
| Use `ThenInclude` for nested relations | Chain multiple `Include` for nested |
| Use filtered includes when applicable | Load all then filter in memory |

---

## Related

- [batch-loading.md](batch-loading.md) - Alternative for multiple parents
- [projection.md](projection.md) - When you only need specific fields
- [../anti-patterns/n-plus-one.md](../anti-patterns/n-plus-one.md) - What Include prevents

---
