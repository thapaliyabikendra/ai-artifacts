# ABP Entity Base Classes

Quick reference for choosing the right entity base class.

## Decision Tree

```
Is it an aggregate root (owns other entities)?
├── YES → Does it need audit trail?
│         ├── YES → FullAuditedAggregateRoot<Guid>
│         └── NO  → AggregateRoot<Guid>
└── NO  → Is it owned by an aggregate?
          ├── YES → Does it need audit trail?
          │         ├── YES → FullAuditedEntity<Guid>
          │         └── NO  → Entity<Guid>
          └── NO  → Consider if it should be a Value Object
```

## Base Class Reference

| Base Class | Use When | Includes |
|------------|----------|----------|
| `Entity<TKey>` | Simple entity, no audit | `Id` |
| `AggregateRoot<TKey>` | Domain aggregate, no audit | `Id`, domain events |
| `AuditedEntity<TKey>` | Need creation/modification audit | `Id`, `CreationTime`, `CreatorId`, `LastModificationTime`, `LastModifierId` |
| `AuditedAggregateRoot<TKey>` | Aggregate with creation/mod audit | Above + domain events |
| `FullAuditedEntity<TKey>` | Need full audit + soft delete | Above + `IsDeleted`, `DeletionTime`, `DeleterId` |
| `FullAuditedAggregateRoot<TKey>` | **Most common** - aggregate + full audit | All of the above |

## Code Examples

### Most Common: FullAuditedAggregateRoot

```csharp
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string FirstName { get; private set; }
    public string LastName { get; private set; }
    public DateTime DateOfBirth { get; private set; }

    // Parameterless constructor for EF Core
    protected Patient() { }

    // Domain constructor with validation
    public Patient(Guid id, string firstName, string lastName, DateTime dateOfBirth)
        : base(id)
    {
        SetName(firstName, lastName);
        DateOfBirth = dateOfBirth;
    }

    // Domain method with encapsulation
    public void SetName(string firstName, string lastName)
    {
        FirstName = Check.NotNullOrWhiteSpace(firstName, nameof(firstName), maxLength: 100);
        LastName = Check.NotNullOrWhiteSpace(lastName, nameof(lastName), maxLength: 100);
    }
}
```

**Automatically includes:**
- `Id` (Guid)
- `CreationTime`, `CreatorId`
- `LastModificationTime`, `LastModifierId`
- `IsDeleted`, `DeletionTime`, `DeleterId`
- `ExtraProperties` (for extensibility)
- `ConcurrencyStamp` (for optimistic concurrency)

### Child Entity: FullAuditedEntity

```csharp
public class PatientAddress : FullAuditedEntity<Guid>
{
    public Guid PatientId { get; private set; }
    public string Street { get; private set; }
    public string City { get; private set; }

    protected PatientAddress() { }

    public PatientAddress(Guid id, Guid patientId, string street, string city)
        : base(id)
    {
        PatientId = patientId;
        Street = street;
        City = city;
    }
}
```

### Simple Entity (No Audit)

```csharp
public class LookupItem : Entity<Guid>
{
    public string Code { get; set; }
    public string Name { get; set; }
}
```

## Multi-Tenancy

Add `IMultiTenant` interface for tenant isolation:

```csharp
public class Patient : FullAuditedAggregateRoot<Guid>, IMultiTenant
{
    public Guid? TenantId { get; set; }
    // ... rest of entity
}
```

## Common Interfaces

| Interface | Purpose | Adds |
|-----------|---------|------|
| `IMultiTenant` | Tenant isolation | `TenantId` |
| `ISoftDelete` | Soft delete only | `IsDeleted` |
| `IHasCreationTime` | Creation timestamp | `CreationTime` |
| `IMustHaveCreator` | Required creator | `CreatorId` |
| `IHasModificationTime` | Modification timestamp | `LastModificationTime` |

## Referenced By

- `abp-framework-patterns` - Entity creation section
- `efcore-patterns` - Entity configuration
- `domain-modeling` - Entity design
