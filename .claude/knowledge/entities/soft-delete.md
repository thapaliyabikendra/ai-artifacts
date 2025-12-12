# Soft Delete Pattern

ABP Framework soft delete for data preservation.

## How It Works

Instead of physically deleting records, soft delete:
1. Sets `IsDeleted = true`
2. Records `DeletionTime` and `DeleterId`
3. Automatically filters out deleted records from queries

## Implementation

### Entity Setup

Use `FullAudited*` base classes or implement `ISoftDelete`:

```csharp
// Option 1: Use FullAuditedAggregateRoot (recommended)
public class Patient : FullAuditedAggregateRoot<Guid>
{
    // IsDeleted, DeletionTime, DeleterId included automatically
}

// Option 2: Implement ISoftDelete directly
public class Patient : AggregateRoot<Guid>, ISoftDelete
{
    public bool IsDeleted { get; set; }
}
```

### Automatic Filtering

ABP automatically filters soft-deleted entities:

```csharp
// This query automatically excludes IsDeleted = true
var patients = await _patientRepository.GetListAsync();
```

### Including Deleted Records

Use `IRepository.WithDetails()` or disable filter:

```csharp
// Option 1: Using data filter
using (_dataFilter.Disable<ISoftDelete>())
{
    var allPatients = await _patientRepository.GetListAsync();
    // Includes deleted records
}

// Option 2: Direct query
var allPatients = await _patientRepository
    .WithDetailsAsync()
    .Where(p => true) // Bypass filter
    .ToListAsync();
```

### Hard Delete

Force physical deletion when needed:

```csharp
await _patientRepository.HardDeleteAsync(patient);
```

## EF Core Configuration

Soft delete filter is auto-configured:

```csharp
// ABP automatically adds:
builder.HasQueryFilter(x => !x.IsDeleted);
```

## Best Practices

| Do | Don't |
|----|-------|
| Use soft delete for business data | Hard delete user data without consent |
| Implement data retention policies | Keep deleted data forever |
| Consider GDPR for personal data | Ignore data protection regulations |
| Use hard delete for cleanup jobs | Manually set IsDeleted = true |

## Cascade Soft Delete

For related entities, consider:

```csharp
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public ICollection<Appointment> Appointments { get; set; }
}

// When deleting patient, appointments are NOT auto-soft-deleted
// Handle in domain service if needed:
public async Task DeletePatientAsync(Guid patientId)
{
    var patient = await _patientRepository.GetAsync(patientId);

    // Soft delete related appointments
    foreach (var appointment in patient.Appointments)
    {
        await _appointmentRepository.DeleteAsync(appointment);
    }

    await _patientRepository.DeleteAsync(patient);
}
```

## Querying Deleted Records

```csharp
// Get only deleted records
using (_dataFilter.Disable<ISoftDelete>())
{
    var deletedPatients = await _patientRepository
        .Where(p => p.IsDeleted)
        .ToListAsync();
}

// Restore a deleted record
using (_dataFilter.Disable<ISoftDelete>())
{
    var patient = await _patientRepository.GetAsync(id);
    patient.IsDeleted = false;
    await _patientRepository.UpdateAsync(patient);
}
```

## Referenced By

- `abp-framework-patterns` - Entity deletion
- `efcore-patterns` - Query filters
- `security-patterns` - Data retention
