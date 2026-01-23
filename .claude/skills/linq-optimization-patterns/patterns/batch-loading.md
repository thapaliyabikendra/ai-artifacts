# Batch Loading Pattern

Load related data for multiple parent entities in a single query, then join in memory.

---

## When to Use

- Have a list of parent entities, need related data for each
- Can't use Include (e.g., data from different repository)
- Need to avoid N+1 queries for multiple parents
- Processing data in batches

---

## Basic Pattern

```csharp
public async Task<List<DoctorDto>> GetDoctorsWithAppointmentsAsync()
{
    // Step 1: Load parents
    var doctors = await _doctorRepository.GetListAsync();
    var doctorIds = doctors.Select(d => d.Id).ToList();

    // Step 2: Batch load related data (SINGLE query for ALL)
    var appointments = await (await _appointmentRepository.GetQueryableAsync())
        .Where(a => doctorIds.Contains(a.DoctorId))
        .ToListAsync();

    // Step 3: Group by foreign key for O(1) lookup
    var appointmentsByDoctor = appointments
        .GroupBy(a => a.DoctorId)
        .ToDictionary(g => g.Key, g => g.ToList());

    // Step 4: Join in memory
    return doctors.Select(d => new DoctorDto
    {
        Id = d.Id,
        Name = d.FullName,
        Appointments = appointmentsByDoctor
            .GetValueOrDefault(d.Id, new List<Appointment>())
            .Select(a => a.ToDto())
            .ToList()
    }).ToList();
}
```

**Queries executed**: 2 (regardless of N doctors)

---

## With Aggregate Computation

```csharp
// Load appointment counts per doctor in single query
var appointmentCounts = await (await _appointmentRepository.GetQueryableAsync())
    .Where(a => doctorIds.Contains(a.DoctorId))
    .GroupBy(a => a.DoctorId)
    .Select(g => new { DoctorId = g.Key, Count = g.Count() })
    .ToDictionaryAsync(x => x.DoctorId, x => x.Count);

// Use in projection
return doctors.Select(d => new DoctorDto
{
    Id = d.Id,
    Name = d.FullName,
    AppointmentCount = appointmentCounts.GetValueOrDefault(d.Id, 0)
}).ToList();
```

---

## Multiple Related Types

Load data from multiple repositories in parallel:

```csharp
public async Task<List<DoctorDto>> GetDoctorsWithDetailsAsync()
{
    var doctors = await _doctorRepository.GetListAsync();
    var doctorIds = doctors.Select(d => d.Id).ToList();

    // Parallel batch loads
    var appointmentsTask = (await _appointmentRepository.GetQueryableAsync())
        .Where(a => doctorIds.Contains(a.DoctorId))
        .ToListAsync();

    var schedulesTask = (await _scheduleRepository.GetQueryableAsync())
        .Where(s => doctorIds.Contains(s.DoctorId))
        .ToListAsync();

    await Task.WhenAll(appointmentsTask, schedulesTask);

    var appointmentsByDoctor = (await appointmentsTask)
        .GroupBy(a => a.DoctorId)
        .ToDictionary(g => g.Key, g => g.ToList());

    var schedulesByDoctor = (await schedulesTask)
        .GroupBy(s => s.DoctorId)
        .ToDictionary(g => g.Key, g => g.ToList());

    return doctors.Select(d => new DoctorDto
    {
        Id = d.Id,
        Appointments = appointmentsByDoctor.GetValueOrDefault(d.Id, new()),
        Schedules = schedulesByDoctor.GetValueOrDefault(d.Id, new())
    }).ToList();
}
```

---

## Chunked Batch Loading

For very large ID lists, chunk to avoid SQL parameter limits:

```csharp
public async Task<Dictionary<Guid, List<Appointment>>> GetAppointmentsForDoctorsAsync(
    List<Guid> doctorIds)
{
    const int chunkSize = 1000;  // SQL Server limit considerations
    var result = new Dictionary<Guid, List<Appointment>>();

    foreach (var chunk in doctorIds.Chunk(chunkSize))
    {
        var chunkIds = chunk.ToList();
        var appointments = await (await _appointmentRepository.GetQueryableAsync())
            .Where(a => chunkIds.Contains(a.DoctorId))
            .ToListAsync();

        foreach (var group in appointments.GroupBy(a => a.DoctorId))
        {
            result[group.Key] = group.ToList();
        }
    }

    return result;
}
```

---

## Dictionary Lookup Pattern

Always use Dictionary for O(1) lookups:

```csharp
// ❌ Bad: O(n×m) - FirstOrDefault scans for each item
foreach (var doctor in doctors)
{
    doctor.TopAppointment = appointments
        .FirstOrDefault(a => a.DoctorId == doctor.Id);  // Scans all!
}

// ✅ Good: O(n+m) - Dictionary lookup is O(1)
var appointmentsByDoctor = appointments
    .GroupBy(a => a.DoctorId)
    .ToDictionary(g => g.Key, g => g.First());

foreach (var doctor in doctors)
{
    doctor.TopAppointment = appointmentsByDoctor
        .GetValueOrDefault(doctor.Id);  // O(1) lookup
}
```

---

## Batch vs Include

| Use Batch Loading | Use Include |
|-------------------|-------------|
| Data from different DbContext/repository | Same DbContext |
| Need to process in chunks | Small to medium dataset |
| Complex aggregation needed | Simple navigation |
| Multiple unrelated queries can run parallel | Single query preferred |

---

## Best Practices

| Do | Don't |
|----|-------|
| Use `Contains` for filtering | Loop with individual queries |
| Create Dictionary for lookups | Use `FirstOrDefault` in loops |
| Chunk large ID lists | Send 10K+ IDs in one query |
| Parallelize independent queries | Sequential when parallel possible |

---

## Related

- [eager-loading.md](eager-loading.md) - Alternative using Include
- [../anti-patterns/n-plus-one.md](../anti-patterns/n-plus-one.md) - What batch loading prevents

---
