# Validation Chain Example

Complete FluentValidation implementation with async repository checks.

## Basic Validator

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
            .WithMessage("First name is required")
            .MaximumLength(PatientConsts.MaxFirstNameLength)
            .WithMessage($"First name cannot exceed {PatientConsts.MaxFirstNameLength} characters");

        RuleFor(x => x.LastName)
            .NotEmpty()
            .MaximumLength(PatientConsts.MaxLastNameLength);

        RuleFor(x => x.Email)
            .NotEmpty()
            .MaximumLength(PatientConsts.MaxEmailLength)
            .EmailAddress()
            .WithMessage("Invalid email format");

        RuleFor(x => x.DateOfBirth)
            .NotEmpty()
            .LessThan(DateTime.Today)
            .WithMessage("Date of birth must be in the past")
            .GreaterThan(DateTime.Today.AddYears(-150))
            .WithMessage("Invalid date of birth");

        RuleFor(x => x.PhoneNumber)
            .Matches(@"^\+?[\d\s-]{10,}$")
            .When(x => !string.IsNullOrEmpty(x.PhoneNumber))
            .WithMessage("Invalid phone number format");
    }
}
```

## Async Validator with Repository

```csharp
// src/{ProjectName}.Application/Patients/CreatePatientDtoValidator.cs
using FluentValidation;
using Volo.Abp.Domain.Repositories;

namespace YourProject.Patients;

public class CreatePatientDtoValidator : AbstractValidator<CreateUpdatePatientDto>
{
    private readonly IRepository<Patient, Guid> _patientRepository;

    public CreatePatientDtoValidator(IRepository<Patient, Guid> patientRepository)
    {
        _patientRepository = patientRepository;

        // Sync rules
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

        // Async rule: Check email uniqueness
        RuleFor(x => x.Email)
            .MustAsync(BeUniqueEmailAsync)
            .WithMessage("Email is already registered");
    }

    private async Task<bool> BeUniqueEmailAsync(string email, CancellationToken cancellationToken)
    {
        return !await _patientRepository.AnyAsync(p => p.Email == email, cancellationToken);
    }
}
```

## Update Validator (Exclude Current Entity)

```csharp
// src/{ProjectName}.Application/Patients/UpdatePatientDtoValidator.cs
using FluentValidation;
using Volo.Abp.Domain.Repositories;

namespace YourProject.Patients;

public class UpdatePatientDtoValidator : AbstractValidator<UpdatePatientInput>
{
    private readonly IRepository<Patient, Guid> _patientRepository;

    public UpdatePatientDtoValidator(IRepository<Patient, Guid> patientRepository)
    {
        _patientRepository = patientRepository;

        RuleFor(x => x.FirstName)
            .NotEmpty()
            .MaximumLength(PatientConsts.MaxFirstNameLength);

        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress();

        // Check uniqueness excluding current entity
        RuleFor(x => x)
            .MustAsync(BeUniqueEmailExcludingSelfAsync)
            .WithMessage("Email is already registered by another patient");
    }

    private async Task<bool> BeUniqueEmailExcludingSelfAsync(
        UpdatePatientInput input,
        CancellationToken cancellationToken)
    {
        return !await _patientRepository.AnyAsync(
            p => p.Email == input.Email && p.Id != input.Id,
            cancellationToken);
    }
}

// Input DTO that includes Id for update context
public class UpdatePatientInput : CreateUpdatePatientDto
{
    public Guid Id { get; set; }
}
```

## Conditional Validation

```csharp
public class AppointmentDtoValidator : AbstractValidator<CreateAppointmentDto>
{
    public AppointmentDtoValidator()
    {
        RuleFor(x => x.PatientId)
            .NotEmpty();

        RuleFor(x => x.DoctorId)
            .NotEmpty();

        RuleFor(x => x.AppointmentDate)
            .NotEmpty()
            .GreaterThan(DateTime.Now)
            .WithMessage("Appointment must be in the future");

        // Conditional: Emergency appointments can be same-day
        RuleFor(x => x.AppointmentDate)
            .GreaterThan(DateTime.Today.AddDays(1))
            .When(x => !x.IsEmergency)
            .WithMessage("Non-emergency appointments must be at least 1 day in advance");

        // Conditional: Require reason for emergency
        RuleFor(x => x.EmergencyReason)
            .NotEmpty()
            .When(x => x.IsEmergency)
            .WithMessage("Emergency reason is required for emergency appointments");
    }
}
```

## Complex Object Validation

```csharp
public class PatientWithAddressDtoValidator : AbstractValidator<PatientWithAddressDto>
{
    public PatientWithAddressDtoValidator()
    {
        // Patient rules
        RuleFor(x => x.FirstName).NotEmpty();
        RuleFor(x => x.LastName).NotEmpty();

        // Nested object validation
        RuleFor(x => x.Address)
            .SetValidator(new AddressDtoValidator()!)
            .When(x => x.Address != null);

        // Collection validation
        RuleForEach(x => x.PhoneNumbers)
            .SetValidator(new PhoneNumberDtoValidator());

        // Collection count validation
        RuleFor(x => x.PhoneNumbers)
            .Must(x => x == null || x.Count <= 5)
            .WithMessage("Maximum 5 phone numbers allowed");
    }
}

public class AddressDtoValidator : AbstractValidator<AddressDto>
{
    public AddressDtoValidator()
    {
        RuleFor(x => x.Street).NotEmpty().MaximumLength(200);
        RuleFor(x => x.City).NotEmpty().MaximumLength(100);
        RuleFor(x => x.PostalCode).NotEmpty().Matches(@"^\d{5}(-\d{4})?$");
    }
}
```

## Registration in Module

```csharp
// src/{ProjectName}.Application/{ProjectName}ApplicationModule.cs
public override void ConfigureServices(ServiceConfigurationContext context)
{
    // FluentValidation is auto-registered by ABP
    // Custom validators are discovered automatically if they:
    // 1. Inherit from AbstractValidator<T>
    // 2. Are in the Application assembly
}
```

## Localized Messages

```csharp
public class PatientDtoValidator : AbstractValidator<CreateUpdatePatientDto>
{
    private readonly IStringLocalizer<YourProjectResource> _localizer;

    public PatientDtoValidator(IStringLocalizer<YourProjectResource> localizer)
    {
        _localizer = localizer;

        RuleFor(x => x.FirstName)
            .NotEmpty()
            .WithMessage(_ => _localizer["Validation:FirstNameRequired"]);

        RuleFor(x => x.Email)
            .EmailAddress()
            .WithMessage(_ => _localizer["Validation:InvalidEmail"]);
    }
}
```

## Referenced By

- `fluentvalidation-patterns` - Validation implementation
- `abp-framework-patterns` - DTO validation
- `error-handling-patterns` - Validation error handling
