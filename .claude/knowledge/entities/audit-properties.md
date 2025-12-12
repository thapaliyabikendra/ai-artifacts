# Audit Properties

ABP Framework audit properties for tracking entity changes.

## Property Reference

| Property | Type | Set By | Purpose |
|----------|------|--------|---------|
| `CreationTime` | `DateTime` | ABP automatically | When entity was created |
| `CreatorId` | `Guid?` | ABP automatically | Who created the entity |
| `LastModificationTime` | `DateTime?` | ABP automatically | When last modified |
| `LastModifierId` | `Guid?` | ABP automatically | Who last modified |
| `IsDeleted` | `bool` | ABP automatically | Soft delete flag |
| `DeletionTime` | `DateTime?` | ABP automatically | When soft deleted |
| `DeleterId` | `Guid?` | ABP automatically | Who deleted |

## Audit Combinations

| Base Class | Creation | Modification | Deletion |
|------------|----------|--------------|----------|
| `Entity<T>` | ❌ | ❌ | ❌ |
| `AuditedEntity<T>` | ✅ | ✅ | ❌ |
| `FullAuditedEntity<T>` | ✅ | ✅ | ✅ |
| `AggregateRoot<T>` | ❌ | ❌ | ❌ |
| `AuditedAggregateRoot<T>` | ✅ | ✅ | ❌ |
| `FullAuditedAggregateRoot<T>` | ✅ | ✅ | ✅ |

## How It Works

### Automatic Population

ABP automatically sets audit properties via `IAuditPropertySetter`:

```csharp
// You write this:
await _patientRepository.InsertAsync(new Patient(...));

// ABP automatically does this:
patient.CreationTime = Clock.Now;
patient.CreatorId = CurrentUser.Id;
```

### Querying by Audit Properties

```csharp
// Find recently created
var recentPatients = await _patientRepository
    .Where(p => p.CreationTime > DateTime.UtcNow.AddDays(-7))
    .ToListAsync();

// Find modified by specific user
var modifiedByAdmin = await _patientRepository
    .Where(p => p.LastModifierId == adminUserId)
    .ToListAsync();
```

## EF Core Configuration

Audit properties are auto-configured, but you can customize:

```csharp
builder.Property(x => x.CreationTime)
    .HasColumnName("created_at")
    .IsRequired();

builder.Property(x => x.CreatorId)
    .HasColumnName("created_by");
```

## Best Practices

1. **Don't manually set audit properties** - ABP handles this
2. **Use `Clock.Now`** - Not `DateTime.Now` or `DateTime.UtcNow`
3. **Include in DTOs when needed** - For display purposes
4. **Filter by audit properties** - For recent changes, user activity

## DTO Mapping

Include audit properties in DTOs for display:

```csharp
public class PatientDto : FullAuditedEntityDto<Guid>
{
    // Automatically includes:
    // - CreationTime, CreatorId
    // - LastModificationTime, LastModifierId
    // - IsDeleted, DeletionTime, DeleterId

    public string FirstName { get; set; }
    public string LastName { get; set; }
}
```

## Referenced By

- `abp-framework-patterns` - Entity and DTO sections
- `efcore-patterns` - Entity configuration
