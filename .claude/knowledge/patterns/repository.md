# Repository Pattern

ABP Framework repository pattern for data access abstraction.

## Core Concepts

| Interface | Purpose | Use When |
|-----------|---------|----------|
| `IRepository<TEntity, TKey>` | Basic CRUD | Most cases |
| `IReadOnlyRepository<TEntity, TKey>` | Read-only access | Query-only services |
| `IBasicRepository<TEntity, TKey>` | Minimal operations | Simple needs |

## Built-in Methods

### IRepository<TEntity, TKey>

```csharp
// Create
Task<TEntity> InsertAsync(TEntity entity, bool autoSave = false);
Task InsertManyAsync(IEnumerable<TEntity> entities, bool autoSave = false);

// Read
Task<TEntity> GetAsync(TKey id);
Task<TEntity?> FindAsync(TKey id);
Task<List<TEntity>> GetListAsync();
Task<long> GetCountAsync();

// Update
Task<TEntity> UpdateAsync(TEntity entity, bool autoSave = false);
Task UpdateManyAsync(IEnumerable<TEntity> entities, bool autoSave = false);

// Delete
Task DeleteAsync(TEntity entity, bool autoSave = false);
Task DeleteAsync(TKey id, bool autoSave = false);
Task DeleteManyAsync(IEnumerable<TEntity> entities, bool autoSave = false);
```

### Query Extensions

```csharp
// Get queryable
IQueryable<TEntity> await repository.GetQueryableAsync();

// With navigation properties
Task<IQueryable<TEntity>> WithDetailsAsync();
Task<IQueryable<TEntity>> WithDetailsAsync(params Expression<Func<TEntity, object>>[] propertySelectors);
```

## Usage Patterns

### In AppService

```csharp
public class PatientAppService : ApplicationService, IPatientAppService
{
    private readonly IRepository<Patient, Guid> _patientRepository;

    public PatientAppService(IRepository<Patient, Guid> patientRepository)
    {
        _patientRepository = patientRepository;
    }

    public async Task<PatientDto> GetAsync(Guid id)
    {
        var patient = await _patientRepository.GetAsync(id);
        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }

    public async Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientListInput input)
    {
        var queryable = await _patientRepository.GetQueryableAsync();

        var patients = await queryable
            .WhereIf(!input.Filter.IsNullOrWhiteSpace(),
                p => p.FirstName.Contains(input.Filter) || p.LastName.Contains(input.Filter))
            .OrderBy(input.Sorting ?? nameof(Patient.LastName))
            .PageBy(input)
            .ToListAsync();

        var totalCount = await queryable.CountAsync();

        return new PagedResultDto<PatientDto>(
            totalCount,
            ObjectMapper.Map<List<Patient>, List<PatientDto>>(patients)
        );
    }
}
```

### Custom Repository

When you need custom queries, create a custom repository:

```csharp
// 1. Define interface in Domain layer
public interface IPatientRepository : IRepository<Patient, Guid>
{
    Task<Patient?> FindByEmailAsync(string email);
    Task<List<Patient>> GetActivePatientsByDoctorAsync(Guid doctorId);
}

// 2. Implement in EntityFrameworkCore layer
public class PatientRepository : EfCoreRepository<YourDbContext, Patient, Guid>, IPatientRepository
{
    public PatientRepository(IDbContextProvider<YourDbContext> dbContextProvider)
        : base(dbContextProvider)
    {
    }

    public async Task<Patient?> FindByEmailAsync(string email)
    {
        var dbSet = await GetDbSetAsync();
        return await dbSet.FirstOrDefaultAsync(p => p.Email == email);
    }

    public async Task<List<Patient>> GetActivePatientsByDoctorAsync(Guid doctorId)
    {
        var dbContext = await GetDbContextAsync();
        return await dbContext.Patients
            .Where(p => p.DoctorId == doctorId && p.IsActive)
            .ToListAsync();
    }
}
```

## AutoSave Parameter

| Value | Behavior | Use When |
|-------|----------|----------|
| `false` (default) | Changes saved at unit of work end | Multiple operations |
| `true` | Immediate save | Need ID immediately |

```csharp
// Default: saved at end of method
await _repository.InsertAsync(entity);

// Immediate save: get ID now
await _repository.InsertAsync(entity, autoSave: true);
var newId = entity.Id; // Available immediately
```

## Best Practices

1. **Inject `IRepository<T,K>`** - Not `DbContext` directly
2. **Use custom repository** - For complex queries only
3. **Prefer LINQ** - Over raw SQL
4. **Use `GetQueryableAsync()`** - For complex filtering
5. **Don't expose `IQueryable`** - From AppService to controller

## Referenced By

- `abp-framework-patterns` - Repository usage
- `efcore-patterns` - Custom repository implementation
- `linq-optimization-patterns` - Query patterns
