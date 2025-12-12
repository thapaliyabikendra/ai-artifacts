# Specification Pattern

ABP Framework specification pattern for reusable query logic.

## When to Use

| Use Specification | Use Direct LINQ |
|-------------------|-----------------|
| Complex business rules | Simple filters |
| Reusable across services | One-time queries |
| Need to combine conditions | Single condition |
| Domain-driven filtering | Infrastructure concerns |

## Basic Specification

```csharp
// 1. Create specification class
public class ActivePatientSpecification : Specification<Patient>
{
    public override Expression<Func<Patient, bool>> ToExpression()
    {
        return patient => patient.IsActive && !patient.IsDeleted;
    }
}

// 2. Use in repository/service
var activePatients = await _repository
    .GetListAsync(new ActivePatientSpecification());
```

## Parameterized Specification

```csharp
public class PatientByDoctorSpecification : Specification<Patient>
{
    private readonly Guid _doctorId;

    public PatientByDoctorSpecification(Guid doctorId)
    {
        _doctorId = doctorId;
    }

    public override Expression<Func<Patient, bool>> ToExpression()
    {
        return patient => patient.DoctorId == _doctorId;
    }
}

// Usage
var patients = await _repository
    .GetListAsync(new PatientByDoctorSpecification(doctorId));
```

## Combining Specifications

```csharp
// AND combination
var spec = new ActivePatientSpecification()
    .And(new PatientByDoctorSpecification(doctorId));

// OR combination
var spec = new AdultPatientSpecification()
    .Or(new MinorWithGuardianSpecification());

// NOT
var spec = new ActivePatientSpecification().Not();

// Complex combination
var spec = new ActivePatientSpecification()
    .And(new PatientByDoctorSpecification(doctorId))
    .And(new RecentVisitSpecification(DateTime.UtcNow.AddMonths(-6)));
```

## With Repository

```csharp
public interface IPatientRepository : IRepository<Patient, Guid>
{
    Task<List<Patient>> GetListAsync(ISpecification<Patient> spec);
    Task<int> CountAsync(ISpecification<Patient> spec);
}

public class PatientRepository : EfCoreRepository<AppDbContext, Patient, Guid>, IPatientRepository
{
    public async Task<List<Patient>> GetListAsync(ISpecification<Patient> spec)
    {
        return await (await GetDbSetAsync())
            .Where(spec.ToExpression())
            .ToListAsync();
    }

    public async Task<int> CountAsync(ISpecification<Patient> spec)
    {
        return await (await GetDbSetAsync())
            .CountAsync(spec.ToExpression());
    }
}
```

## In AppService

```csharp
public class PatientAppService : ApplicationService
{
    public async Task<List<PatientDto>> GetActivePatientsForDoctorAsync(Guid doctorId)
    {
        var spec = new ActivePatientSpecification()
            .And(new PatientByDoctorSpecification(doctorId));

        var patients = await _patientRepository.GetListAsync(spec);
        return ObjectMapper.Map<List<Patient>, List<PatientDto>>(patients);
    }
}
```

## Common Specifications

### Date Range

```csharp
public class CreatedBetweenSpecification<T> : Specification<T>
    where T : IHasCreationTime
{
    private readonly DateTime _start;
    private readonly DateTime _end;

    public CreatedBetweenSpecification(DateTime start, DateTime end)
    {
        _start = start;
        _end = end;
    }

    public override Expression<Func<T, bool>> ToExpression()
    {
        return entity => entity.CreationTime >= _start && entity.CreationTime <= _end;
    }
}
```

### Search/Filter

```csharp
public class PatientSearchSpecification : Specification<Patient>
{
    private readonly string _searchTerm;

    public PatientSearchSpecification(string searchTerm)
    {
        _searchTerm = searchTerm?.ToLower() ?? string.Empty;
    }

    public override Expression<Func<Patient, bool>> ToExpression()
    {
        if (string.IsNullOrWhiteSpace(_searchTerm))
            return _ => true;

        return patient =>
            patient.FirstName.ToLower().Contains(_searchTerm) ||
            patient.LastName.ToLower().Contains(_searchTerm) ||
            patient.Email.ToLower().Contains(_searchTerm);
    }
}
```

## Best Practices

1. **Name specifications clearly** - `ActivePatientSpecification` not `Spec1`
2. **Keep specifications focused** - Single responsibility
3. **Combine at usage site** - Not in specification class
4. **Test specifications** - They contain business logic
5. **Use for domain rules** - Not for pagination/sorting

## Referenced By

- `abp-framework-patterns` - Query patterns
- `linq-optimization-patterns` - Reusable queries
- `domain-modeling` - Business rules
