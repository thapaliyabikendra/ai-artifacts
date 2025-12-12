# Unit of Work Pattern

ABP Framework Unit of Work for transaction management.

## How It Works

ABP automatically wraps each:
- AppService method
- Controller action
- Background job execution

in a Unit of Work (UoW) that:
1. Opens a transaction
2. Executes all operations
3. Commits on success / Rolls back on failure

## Automatic UoW

```csharp
public class PatientAppService : ApplicationService
{
    // This method is automatically wrapped in a UoW
    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        var patient = new Patient(...);
        await _patientRepository.InsertAsync(patient);

        var audit = new PatientAuditLog(...);
        await _auditLogRepository.InsertAsync(audit);

        // Both inserts commit together or roll back together
        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }
}
```

## Manual UoW Control

### Using IUnitOfWorkManager

```csharp
public class PatientService : ApplicationService
{
    private readonly IUnitOfWorkManager _unitOfWorkManager;

    public async Task ProcessPatientsAsync()
    {
        // Start a new UoW
        using (var uow = _unitOfWorkManager.Begin())
        {
            await _repository.InsertAsync(entity1);
            await _repository.InsertAsync(entity2);

            // Explicitly commit
            await uow.CompleteAsync();
        }
    }
}
```

### Using [UnitOfWork] Attribute

```csharp
// Disable automatic UoW
[UnitOfWork(IsDisabled = true)]
public async Task NonTransactionalMethodAsync()
{
    // Each repository call is independent
}

// Force new UoW
[UnitOfWork(IsolationLevel = IsolationLevel.Serializable)]
public async Task StrictTransactionAsync()
{
    // Uses Serializable isolation
}
```

## SaveChanges Behavior

| Scenario | Behavior |
|----------|----------|
| Method completes normally | Auto SaveChanges |
| Exception thrown | Auto rollback |
| `autoSave: true` on repository | Immediate save within UoW |

```csharp
public async Task ExampleAsync()
{
    // Change tracked but not saved yet
    await _repository.InsertAsync(entity1);

    // Change tracked but not saved yet
    await _repository.UpdateAsync(entity2);

    // Exception here = both operations rolled back
    throw new Exception();

    // This line never reached, nothing committed
}
```

## Nested UoW

```csharp
public async Task OuterMethodAsync()
{
    await _repository.InsertAsync(outerEntity);

    // Inner UoW joins outer UoW by default
    await InnerMethodAsync();

    // Both commit together
}

public async Task InnerMethodAsync()
{
    await _repository.InsertAsync(innerEntity);
}
```

### Requiring New UoW

```csharp
[UnitOfWork(IsDisabled = true)]
public async Task OuterMethodAsync()
{
    using (var uow = _unitOfWorkManager.Begin(requiresNew: true))
    {
        // This is an independent transaction
        await _repository.InsertAsync(entity);
        await uow.CompleteAsync();
    }
}
```

## Common Patterns

### Ensure Save Before Query

```csharp
public async Task<Patient> CreateAndQueryAsync(CreatePatientDto input)
{
    var patient = new Patient(...);

    // Save immediately to get ID
    await _repository.InsertAsync(patient, autoSave: true);

    // Now we can query related data
    var relatedData = await _otherRepository
        .Where(x => x.PatientId == patient.Id)
        .ToListAsync();

    return patient;
}
```

### Multiple Database Support

```csharp
[UnitOfWork]
public async Task CrossDatabaseOperationAsync()
{
    // Operations on different DbContexts
    await _patientRepository.InsertAsync(patient);    // DbContext1
    await _auditLogRepository.InsertAsync(auditLog);  // DbContext2

    // ABP coordinates both transactions
}
```

## Best Practices

1. **Trust automatic UoW** - Don't create manual UoWs unnecessarily
2. **Use `autoSave: true`** - When you need the ID immediately
3. **Avoid long transactions** - Keep UoW scope small
4. **Handle exceptions** - Let them propagate for rollback
5. **Don't mix manual and auto** - Stick to one pattern

## Referenced By

- `abp-framework-patterns` - Transaction handling
- `efcore-patterns` - SaveChanges behavior
- `error-handling-patterns` - Transaction rollback
