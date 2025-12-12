# Complete CRUD Entity Example

Full example of implementing a Patient entity with all layers.

## 1. Entity (Domain)

```csharp
// src/{ProjectName}.Domain/Patients/Patient.cs
using Volo.Abp.Domain.Entities.Auditing;
using Volo.Abp;

namespace YourProject.Patients;

public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string FirstName { get; private set; }
    public string LastName { get; private set; }
    public string Email { get; private set; }
    public DateTime DateOfBirth { get; private set; }
    public PatientStatus Status { get; private set; }

    protected Patient() { } // For EF Core

    public Patient(
        Guid id,
        string firstName,
        string lastName,
        string email,
        DateTime dateOfBirth)
        : base(id)
    {
        SetName(firstName, lastName);
        SetEmail(email);
        DateOfBirth = dateOfBirth;
        Status = PatientStatus.Active;
    }

    public void SetName(string firstName, string lastName)
    {
        FirstName = Check.NotNullOrWhiteSpace(firstName, nameof(firstName), maxLength: PatientConsts.MaxFirstNameLength);
        LastName = Check.NotNullOrWhiteSpace(lastName, nameof(lastName), maxLength: PatientConsts.MaxLastNameLength);
    }

    public void SetEmail(string email)
    {
        Email = Check.NotNullOrWhiteSpace(email, nameof(email), maxLength: PatientConsts.MaxEmailLength);
    }

    public void Activate() => Status = PatientStatus.Active;
    public void Deactivate() => Status = PatientStatus.Inactive;
}
```

## 2. Constants (Domain.Shared)

```csharp
// src/{ProjectName}.Domain.Shared/Patients/PatientConsts.cs
namespace YourProject.Patients;

public static class PatientConsts
{
    public const int MaxFirstNameLength = 100;
    public const int MaxLastNameLength = 100;
    public const int MaxEmailLength = 256;
}

// src/{ProjectName}.Domain.Shared/Patients/PatientStatus.cs
namespace YourProject.Patients;

public enum PatientStatus
{
    Active,
    Inactive,
    Discharged
}
```

## 3. DTOs (Application.Contracts)

```csharp
// src/{ProjectName}.Application.Contracts/Patients/PatientDto.cs
using Volo.Abp.Application.Dtos;

namespace YourProject.Patients;

public class PatientDto : FullAuditedEntityDto<Guid>
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Email { get; set; }
    public DateTime DateOfBirth { get; set; }
    public PatientStatus Status { get; set; }
    public string FullName => $"{FirstName} {LastName}";
}

// src/{ProjectName}.Application.Contracts/Patients/CreateUpdatePatientDto.cs
namespace YourProject.Patients;

public class CreateUpdatePatientDto
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Email { get; set; }
    public DateTime DateOfBirth { get; set; }
}

// src/{ProjectName}.Application.Contracts/Patients/GetPatientListInput.cs
using Volo.Abp.Application.Dtos;

namespace YourProject.Patients;

public class GetPatientListInput : PagedAndSortedResultRequestDto
{
    public string? Filter { get; set; }
    public PatientStatus? Status { get; set; }
}
```

## 4. AppService Interface (Application.Contracts)

```csharp
// src/{ProjectName}.Application.Contracts/Patients/IPatientAppService.cs
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;

namespace YourProject.Patients;

public interface IPatientAppService : IApplicationService
{
    Task<PatientDto> GetAsync(Guid id);
    Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientListInput input);
    Task<PatientDto> CreateAsync(CreateUpdatePatientDto input);
    Task<PatientDto> UpdateAsync(Guid id, CreateUpdatePatientDto input);
    Task DeleteAsync(Guid id);
}
```

## 5. Validator (Application)

```csharp
// src/{ProjectName}.Application/Patients/CreateUpdatePatientDtoValidator.cs
using FluentValidation;

namespace YourProject.Patients;

public class CreateUpdatePatientDtoValidator : AbstractValidator<CreateUpdatePatientDto>
{
    public CreateUpdatePatientDtoValidator()
    {
        RuleFor(x => x.FirstName)
            .NotEmpty()
            .MaximumLength(PatientConsts.MaxFirstNameLength);

        RuleFor(x => x.LastName)
            .NotEmpty()
            .MaximumLength(PatientConsts.MaxLastNameLength);

        RuleFor(x => x.Email)
            .NotEmpty()
            .MaximumLength(PatientConsts.MaxEmailLength)
            .EmailAddress();

        RuleFor(x => x.DateOfBirth)
            .NotEmpty()
            .LessThan(DateTime.Today)
            .WithMessage("Date of birth must be in the past");
    }
}
```

## 6. AppService (Application)

```csharp
// src/{ProjectName}.Application/Patients/PatientAppService.cs
using Microsoft.AspNetCore.Authorization;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;

namespace YourProject.Patients;

[Authorize(YourProjectPermissions.Patients.Default)]
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

        queryable = queryable
            .WhereIf(!input.Filter.IsNullOrWhiteSpace(),
                p => p.FirstName.Contains(input.Filter!) ||
                     p.LastName.Contains(input.Filter!) ||
                     p.Email.Contains(input.Filter!))
            .WhereIf(input.Status.HasValue,
                p => p.Status == input.Status);

        var totalCount = await AsyncExecuter.CountAsync(queryable);

        queryable = queryable
            .OrderBy(input.Sorting.IsNullOrWhiteSpace() ? nameof(Patient.LastName) : input.Sorting)
            .PageBy(input);

        var patients = await AsyncExecuter.ToListAsync(queryable);

        return new PagedResultDto<PatientDto>(
            totalCount,
            ObjectMapper.Map<List<Patient>, List<PatientDto>>(patients)
        );
    }

    [Authorize(YourProjectPermissions.Patients.Create)]
    public async Task<PatientDto> CreateAsync(CreateUpdatePatientDto input)
    {
        var patient = new Patient(
            GuidGenerator.Create(),
            input.FirstName,
            input.LastName,
            input.Email,
            input.DateOfBirth
        );

        await _patientRepository.InsertAsync(patient);

        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }

    [Authorize(YourProjectPermissions.Patients.Edit)]
    public async Task<PatientDto> UpdateAsync(Guid id, CreateUpdatePatientDto input)
    {
        var patient = await _patientRepository.GetAsync(id);

        patient.SetName(input.FirstName, input.LastName);
        patient.SetEmail(input.Email);

        await _patientRepository.UpdateAsync(patient);

        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }

    [Authorize(YourProjectPermissions.Patients.Delete)]
    public async Task DeleteAsync(Guid id)
    {
        await _patientRepository.DeleteAsync(id);
    }
}
```

## 7. Mapperly Mapping (Application)

```csharp
// src/{ProjectName}.Application/{ProjectName}ApplicationMappers.cs
using Riok.Mapperly.Abstractions;

namespace YourProject;

[Mapper]
public static partial class YourProjectApplicationMappers
{
    public static partial PatientDto MapToDto(this Patient patient);
    public static partial List<PatientDto> MapToDtoList(this List<Patient> patients);
}
```

## 8. DbContext Configuration (EntityFrameworkCore)

```csharp
// In DbContext
public DbSet<Patient> Patients { get; set; }

// In OnModelCreating or separate configuration
builder.Entity<Patient>(b =>
{
    b.ToTable("Patients");
    b.ConfigureByConvention();

    b.Property(x => x.FirstName)
        .IsRequired()
        .HasMaxLength(PatientConsts.MaxFirstNameLength);

    b.Property(x => x.LastName)
        .IsRequired()
        .HasMaxLength(PatientConsts.MaxLastNameLength);

    b.Property(x => x.Email)
        .IsRequired()
        .HasMaxLength(PatientConsts.MaxEmailLength);

    b.HasIndex(x => x.Email);
});
```

## 9. Permissions

```csharp
// Add to {ProjectName}Permissions.cs
public static class Patients
{
    public const string Default = GroupName + ".Patients";
    public const string Create = Default + ".Create";
    public const string Edit = Default + ".Edit";
    public const string Delete = Default + ".Delete";
}

// Add to PermissionDefinitionProvider
var patients = group.AddPermission(YourProjectPermissions.Patients.Default, L("Permission:Patients"));
patients.AddChild(YourProjectPermissions.Patients.Create, L("Permission:Patients.Create"));
patients.AddChild(YourProjectPermissions.Patients.Edit, L("Permission:Patients.Edit"));
patients.AddChild(YourProjectPermissions.Patients.Delete, L("Permission:Patients.Delete"));
```

## Referenced By

- All backend skills - Complete implementation reference
- `xunit-testing-patterns` - Test target
