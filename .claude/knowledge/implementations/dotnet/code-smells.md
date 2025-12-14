---
implements_concepts:
  - concepts/code-smells/taxonomy
language: csharp
framework: [dotnet, abp]
used_by_skills: [clean-code-dotnet, abp-code-reviewer, debugging-patterns]
---

# Code Smells in C#/.NET

C# examples of code smells and their refactorings for ABP Framework applications.

## Change Resistance Smells {#change-resistance}

### Rigidity - Hard to Change

```csharp
// ❌ Bad - Change to email format requires changes everywhere
public class PatientService
{
    public void SendReminder(Patient patient)
    {
        var message = $"Dear {patient.Title} {patient.LastName}, your appointment is tomorrow.";
        var subject = "Appointment Reminder";

        using var client = new SmtpClient("smtp.example.com");
        var mailMessage = new MailMessage("clinic@example.com", patient.Email, subject, message);
        client.Send(mailMessage);
    }
}

public class BillingService
{
    public void SendInvoice(Patient patient, Invoice invoice)
    {
        var message = $"Dear {patient.Title} {patient.LastName}, please find attached invoice #{invoice.Number}.";
        var subject = "Invoice";

        using var client = new SmtpClient("smtp.example.com");  // Duplicated!
        var mailMessage = new MailMessage("clinic@example.com", patient.Email, subject, message);
        client.Send(mailMessage);
    }
}

// ✅ Good - Email logic centralized
public interface IEmailService
{
    Task SendAsync(string to, string subject, string body);
}

public class SmtpEmailService : IEmailService
{
    private readonly EmailSettings _settings;

    public async Task SendAsync(string to, string subject, string body)
    {
        // Single place to change email logic
    }
}

public class PatientService
{
    private readonly IEmailService _emailService;
    private readonly IEmailTemplateRenderer _templateRenderer;

    public async Task SendReminderAsync(Patient patient)
    {
        var body = await _templateRenderer.RenderAsync("AppointmentReminder", patient);
        await _emailService.SendAsync(patient.Email, "Appointment Reminder", body);
    }
}
```

### Fragility - Breaks in Unexpected Places

```csharp
// ❌ Bad - Shared mutable state causes fragility
public static class AppointmentConfig
{
    public static int MaxAppointmentsPerDay = 10;
    public static TimeSpan DefaultDuration = TimeSpan.FromMinutes(30);
}

public class DoctorScheduler
{
    public void ConfigureForSpecialist()
    {
        AppointmentConfig.MaxAppointmentsPerDay = 5;  // Affects ALL doctors!
    }
}

// ✅ Good - Immutable configuration per entity
public class DoctorScheduleSettings
{
    public int MaxAppointmentsPerDay { get; init; } = 10;
    public TimeSpan DefaultDuration { get; init; } = TimeSpan.FromMinutes(30);
}

public class Doctor : FullAuditedAggregateRoot<Guid>
{
    public DoctorScheduleSettings ScheduleSettings { get; private set; }

    public void ConfigureSchedule(DoctorScheduleSettings settings)
    {
        ScheduleSettings = settings;
    }
}
```

## Complexity Smells {#complexity}

### Needless Complexity

```csharp
// ❌ Bad - Over-engineered for simple requirement
public interface IPatientFactory
{
    Patient Create(PatientCreationContext context);
}

public class PatientCreationContext
{
    public string Name { get; set; }
    public string Email { get; set; }
    public IPatientCreationStrategy Strategy { get; set; }
}

public interface IPatientCreationStrategy
{
    void ApplyTo(Patient patient);
}

public class StandardPatientCreationStrategy : IPatientCreationStrategy { }
public class VipPatientCreationStrategy : IPatientCreationStrategy { }

// ✅ Good - Simple factory method in entity
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string Name { get; private set; }
    public string Email { get; private set; }
    public bool IsVip { get; private set; }

    public Patient(Guid id, string name, string email, bool isVip = false)
        : base(id)
    {
        Name = Check.NotNullOrWhiteSpace(name, nameof(name));
        Email = Check.NotNullOrWhiteSpace(email, nameof(email));
        IsVip = isVip;
    }
}
```

### Needless Repetition (DRY Violation)

```csharp
// ❌ Bad - Repeated validation logic
public class PatientAppService : ApplicationService
{
    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        if (string.IsNullOrEmpty(input.Email))
            throw new BusinessException("Email is required");
        if (!input.Email.Contains("@"))
            throw new BusinessException("Invalid email format");
        if (input.Email.Length > 256)
            throw new BusinessException("Email too long");
        // ...
    }

    public async Task<PatientDto> UpdateAsync(Guid id, UpdatePatientDto input)
    {
        if (string.IsNullOrEmpty(input.Email))
            throw new BusinessException("Email is required");
        if (!input.Email.Contains("@"))
            throw new BusinessException("Invalid email format");
        if (input.Email.Length > 256)
            throw new BusinessException("Email too long");
        // ...
    }
}

// ✅ Good - Centralized validation with FluentValidation
public class EmailValidator : AbstractValidator<string>
{
    public EmailValidator()
    {
        RuleFor(x => x)
            .NotEmpty().WithMessage("Email is required")
            .EmailAddress().WithMessage("Invalid email format")
            .MaximumLength(256).WithMessage("Email too long");
    }
}

public class CreatePatientDtoValidator : AbstractValidator<CreatePatientDto>
{
    public CreatePatientDtoValidator()
    {
        RuleFor(x => x.Email).SetValidator(new EmailValidator());
    }
}
```

## Understandability Smells {#understandability}

### Opacity - Hard to Understand

```csharp
// ❌ Bad - Dense, unclear code
public decimal C(List<Appointment> a, Guid d)
{
    return a.Where(x => x.DoctorId == d && x.Status == 1)
            .Sum(x => x.Duration.TotalMinutes * (x.Type == 1 ? 1.5m : 1.0m) * 0.05m);
}

// ✅ Good - Clear, self-documenting code
private const decimal BaseRatePerMinute = 0.05m;
private const decimal SpecialistMultiplier = 1.5m;

public decimal CalculateDoctorRevenue(List<Appointment> appointments, Guid doctorId)
{
    var completedAppointments = appointments
        .Where(apt => apt.DoctorId == doctorId)
        .Where(apt => apt.Status == AppointmentStatus.Completed);

    return completedAppointments.Sum(CalculateAppointmentRevenue);
}

private decimal CalculateAppointmentRevenue(Appointment appointment)
{
    var durationMinutes = (decimal)appointment.Duration.TotalMinutes;
    var typeMultiplier = appointment.Type == AppointmentType.Specialist
        ? SpecialistMultiplier
        : 1.0m;

    return durationMinutes * typeMultiplier * BaseRatePerMinute;
}
```

### Magic Numbers

```csharp
// ❌ Bad - Magic numbers scattered through code
public class AppointmentScheduler
{
    public bool CanSchedule(Doctor doctor, DateTime time)
    {
        if (time.Hour < 9 || time.Hour >= 17) return false;
        if (time.DayOfWeek == DayOfWeek.Saturday || time.DayOfWeek == DayOfWeek.Sunday) return false;

        var appointments = GetAppointmentsForDay(doctor.Id, time.Date);
        return appointments.Count < 20;
    }

    public TimeSpan GetDefaultDuration(int appointmentType)
    {
        return appointmentType switch
        {
            1 => TimeSpan.FromMinutes(15),
            2 => TimeSpan.FromMinutes(30),
            3 => TimeSpan.FromMinutes(60),
            _ => TimeSpan.FromMinutes(30)
        };
    }
}

// ✅ Good - Named constants and enums
public static class ClinicSchedule
{
    public const int OpeningHour = 9;
    public const int ClosingHour = 17;
    public const int MaxDailyAppointments = 20;
}

public enum AppointmentType
{
    QuickCheckup = 1,
    StandardVisit = 2,
    ExtendedConsultation = 3
}

public static class AppointmentDurations
{
    public static readonly TimeSpan QuickCheckup = TimeSpan.FromMinutes(15);
    public static readonly TimeSpan StandardVisit = TimeSpan.FromMinutes(30);
    public static readonly TimeSpan ExtendedConsultation = TimeSpan.FromMinutes(60);

    public static TimeSpan GetDuration(AppointmentType type) => type switch
    {
        AppointmentType.QuickCheckup => QuickCheckup,
        AppointmentType.StandardVisit => StandardVisit,
        AppointmentType.ExtendedConsultation => ExtendedConsultation,
        _ => StandardVisit
    };
}
```

## Dependency Smells {#dependency}

### Feature Envy

```csharp
// ❌ Bad - AppointmentService is too interested in Doctor's data
public class AppointmentService
{
    public bool IsDoctorAvailable(Doctor doctor, DateTime time)
    {
        // Accessing multiple Doctor properties - Feature Envy!
        if (!doctor.WorkingDays.Contains(time.DayOfWeek)) return false;
        if (time.TimeOfDay < doctor.WorkStartTime) return false;
        if (time.TimeOfDay > doctor.WorkEndTime) return false;
        if (doctor.VacationDays.Contains(time.Date)) return false;

        return true;
    }
}

// ✅ Good - Logic belongs in Doctor
public class Doctor : FullAuditedAggregateRoot<Guid>
{
    public List<DayOfWeek> WorkingDays { get; private set; }
    public TimeSpan WorkStartTime { get; private set; }
    public TimeSpan WorkEndTime { get; private set; }
    public HashSet<DateTime> VacationDays { get; private set; }

    public bool IsAvailableAt(DateTime time)
    {
        if (!WorkingDays.Contains(time.DayOfWeek)) return false;
        if (time.TimeOfDay < WorkStartTime) return false;
        if (time.TimeOfDay > WorkEndTime) return false;
        if (VacationDays.Contains(time.Date)) return false;

        return true;
    }
}

public class AppointmentService
{
    public bool IsDoctorAvailable(Doctor doctor, DateTime time)
    {
        return doctor.IsAvailableAt(time);
    }
}
```

### Law of Demeter Violation

```csharp
// ❌ Bad - Train wreck / chained calls
public class AppointmentReport
{
    public string GetDoctorDepartmentName(Appointment appointment)
    {
        return appointment.Doctor.Department.Manager.Name;  // Too many dots!
    }
}

// ✅ Good - Ask, don't dig
public class Appointment : FullAuditedAggregateRoot<Guid>
{
    public string DoctorDepartmentManagerName { get; private set; }  // Denormalized

    // Or expose a method
    public string GetResponsibleDepartmentHead() => _responsibleDepartmentHead;
}

// Or use a proper query
public class AppointmentReport
{
    private readonly IAppointmentRepository _repository;

    public async Task<string> GetDoctorDepartmentNameAsync(Guid appointmentId)
    {
        return await _repository.GetDepartmentManagerNameAsync(appointmentId);
    }
}
```

### Hidden Temporal Coupling

```csharp
// ❌ Bad - Must call methods in specific order, but order not enforced
public class PatientRegistration
{
    private Patient _patient;
    private bool _validated;

    public void CreatePatient(string name) => _patient = new Patient { Name = name };
    public void ValidatePatient() => _validated = ValidateInternal();
    public void SavePatient() => _repository.Insert(_patient);  // Fails if not validated!
}

// Usage - easy to get wrong
var reg = new PatientRegistration();
reg.SavePatient();  // Oops! NullReferenceException
reg.CreatePatient("John");
reg.SavePatient();  // Oops! Not validated

// ✅ Good - Enforce order through API design
public class PatientRegistration
{
    public UnvalidatedPatient CreatePatient(string name)
    {
        return new UnvalidatedPatient(name);
    }
}

public class UnvalidatedPatient
{
    public string Name { get; }

    public UnvalidatedPatient(string name) => Name = name;

    public ValidatedPatient Validate(IPatientValidator validator)
    {
        validator.ValidateAndThrow(this);
        return new ValidatedPatient(Name);
    }
}

public class ValidatedPatient
{
    public string Name { get; }

    internal ValidatedPatient(string name) => Name = name;

    public Patient Save(IPatientRepository repository)
    {
        var patient = new Patient { Name = Name };
        return repository.Insert(patient);
    }
}

// Usage - compiler enforces order
var reg = new PatientRegistration();
var unvalidated = reg.CreatePatient("John");
var validated = unvalidated.Validate(validator);
var patient = validated.Save(repository);
```

## Class Design Smells {#class-design}

### God Class

```csharp
// ❌ Bad - Class does everything
public class PatientManager
{
    // Patient CRUD
    public Patient CreatePatient() { }
    public Patient GetPatient() { }
    public void UpdatePatient() { }
    public void DeletePatient() { }

    // Appointment management
    public void ScheduleAppointment() { }
    public void CancelAppointment() { }
    public List<Appointment> GetAppointments() { }

    // Billing
    public Invoice GenerateInvoice() { }
    public void ProcessPayment() { }

    // Reports
    public byte[] GeneratePatientReport() { }
    public byte[] GenerateBillingReport() { }

    // Notifications
    public void SendReminder() { }
    public void SendInvoice() { }
}

// ✅ Good - Separated concerns
public class PatientAppService : CrudAppService<...>, IPatientAppService { }
public class AppointmentAppService : ApplicationService, IAppointmentAppService { }
public class BillingAppService : ApplicationService, IBillingAppService { }
public class ReportingAppService : ApplicationService, IReportingAppService { }
public class NotificationService : INotificationService { }
```

### Data Class (Anemic Domain Model)

```csharp
// ❌ Bad - Entity is just a data container
public class Patient
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public PatientStatus Status { get; set; }
    public DateTime? DeactivatedAt { get; set; }
}

// Logic scattered in services
public class PatientService
{
    public void Deactivate(Patient patient)
    {
        patient.Status = PatientStatus.Inactive;
        patient.DeactivatedAt = DateTime.UtcNow;
    }
}

// ✅ Good - Rich domain model
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string Name { get; private set; }
    public string Email { get; private set; }
    public PatientStatus Status { get; private set; }
    public DateTime? DeactivatedAt { get; private set; }

    public void Deactivate()
    {
        if (Status == PatientStatus.Inactive)
            throw new BusinessException("Patient is already inactive");

        Status = PatientStatus.Inactive;
        DeactivatedAt = DateTime.UtcNow;

        AddLocalEvent(new PatientDeactivatedEvent(this));
    }

    public void Reactivate()
    {
        if (Status == PatientStatus.Active)
            throw new BusinessException("Patient is already active");

        Status = PatientStatus.Active;
        DeactivatedAt = null;
    }
}
```

## Detecting Smells

### Code Review Checklist

| Smell | Detection Question |
|-------|-------------------|
| Rigidity | Does a "simple" change require many file edits? |
| Fragility | Do changes break unrelated features? |
| God Class | Does the class have >500 lines or >10 methods? |
| Feature Envy | Does the method use more external data than its own class? |
| Magic Numbers | Are there unexplained literals in the code? |
| Duplication | Can you find similar code in other places? |

### Static Analysis Tools

```xml
<!-- Directory.Build.props -->
<PropertyGroup>
    <EnableNETAnalyzers>true</EnableNETAnalyzers>
    <AnalysisLevel>latest-all</AnalysisLevel>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup>

<ItemGroup>
    <PackageReference Include="SonarAnalyzer.CSharp" Version="9.*" />
    <PackageReference Include="Roslynator.Analyzers" Version="4.*" />
</ItemGroup>
```

## Related Concepts

- [Code Smell Taxonomy](../../concepts/code-smells/taxonomy.md)
- [Clean Code in C#](clean-code.md)
- [SOLID in C#](solid.md)

## Sources

- Refactoring by Martin Fowler
- Clean Code by Robert C. Martin
- Clean Code Cheatsheet V2.4 by Urs Enzler
