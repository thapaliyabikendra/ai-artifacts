# Naming Conventions

ABP Framework and .NET naming standards for this project.

## Quick Reference

| Type | Convention | Example |
|------|------------|---------|
| Entity | PascalCase, singular | `Patient`, `Appointment` |
| DTO | `{Entity}Dto` | `PatientDto` |
| Create/Update DTO | `CreateUpdate{Entity}Dto` | `CreateUpdatePatientDto` |
| List Input DTO | `Get{Entity}ListInput` | `GetPatientListInput` |
| AppService Interface | `I{Entity}AppService` | `IPatientAppService` |
| AppService | `{Entity}AppService` | `PatientAppService` |
| Repository Interface | `I{Entity}Repository` | `IPatientRepository` |
| Validator | `{Dto}Validator` | `CreateUpdatePatientDtoValidator` |
| Domain Service | `{Entity}Manager` | `PatientManager` |
| Permission | `{Project}.{Resource}.{Action}` | `ClinicManagement.Patients.Create` |

## Entities

```csharp
// ✅ Good
public class Patient { }
public class Appointment { }
public class MedicalRecord { }

// ❌ Bad
public class PatientEntity { }    // Don't suffix with Entity
public class Patients { }         // Don't pluralize
public class patient { }          // Must be PascalCase
```

## DTOs

```csharp
// Standard DTO set for an entity
public class PatientDto { }                    // Read DTO
public class CreateUpdatePatientDto { }        // Create/Update DTO (combined)
public class GetPatientListInput { }           // List query input

// Or separate Create/Update (when different)
public class CreatePatientDto { }
public class UpdatePatientDto { }

// Specialized DTOs
public class PatientLookupDto { }              // Minimal for dropdowns
public class PatientDetailDto { }              // Extended for detail view
public class PatientExportDto { }              // For exports
```

## AppServices

```csharp
// Interface in Application.Contracts
public interface IPatientAppService : IApplicationService
{
    Task<PatientDto> GetAsync(Guid id);
    Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientListInput input);
    Task<PatientDto> CreateAsync(CreateUpdatePatientDto input);
    Task<PatientDto> UpdateAsync(Guid id, CreateUpdatePatientDto input);
    Task DeleteAsync(Guid id);
}

// Implementation in Application
public class PatientAppService : ApplicationService, IPatientAppService
{
    // Implementation
}
```

## Methods

| Operation | Method Name | HTTP Verb |
|-----------|-------------|-----------|
| Get single | `GetAsync` | GET |
| Get list | `GetListAsync` | GET |
| Create | `CreateAsync` | POST |
| Update | `UpdateAsync` | PUT |
| Delete | `DeleteAsync` | DELETE |
| Custom action | `{Verb}{Noun}Async` | Varies |

```csharp
// Standard CRUD
Task<PatientDto> GetAsync(Guid id);
Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientListInput input);
Task<PatientDto> CreateAsync(CreateUpdatePatientDto input);
Task<PatientDto> UpdateAsync(Guid id, CreateUpdatePatientDto input);
Task DeleteAsync(Guid id);

// Custom actions
Task<PatientDto> ActivateAsync(Guid id);
Task<List<PatientDto>> GetByDoctorAsync(Guid doctorId);
Task<int> CountActiveAsync();
```

## Variables and Parameters

```csharp
// ✅ Good
var patient = await _patientRepository.GetAsync(id);
var patients = await _patientRepository.GetListAsync();
var patientDto = ObjectMapper.Map<Patient, PatientDto>(patient);

// ❌ Bad
var p = await _patientRepository.GetAsync(id);        // Too short
var patientEntity = await _repository.GetAsync(id);   // Don't suffix
var Patient = await _repository.GetAsync(id);         // Must be camelCase
```

## Private Fields

```csharp
public class PatientAppService : ApplicationService
{
    // ✅ Good: underscore prefix for private fields
    private readonly IRepository<Patient, Guid> _patientRepository;
    private readonly IPatientManager _patientManager;

    // ❌ Bad
    private readonly IRepository<Patient, Guid> patientRepository;  // No underscore
    private readonly IRepository<Patient, Guid> PatientRepository;  // Not camelCase
}
```

## Constants and Enums

```csharp
// Constants: PascalCase
public static class PatientConsts
{
    public const int MaxNameLength = 100;
    public const int MaxEmailLength = 256;
}

// Enums: PascalCase for type and members
public enum PatientStatus
{
    Active,
    Inactive,
    Discharged
}
```

## File Names

| Type | File Name |
|------|-----------|
| Entity | `Patient.cs` |
| DTO | `PatientDto.cs` |
| AppService | `PatientAppService.cs` |
| Interface | `IPatientAppService.cs` |
| Validator | `CreateUpdatePatientDtoValidator.cs` |
| Test | `PatientAppService_Tests.cs` |

## Referenced By

- `abp-framework-patterns` - All sections
- `fluentvalidation-patterns` - Validator naming
- All backend skills
