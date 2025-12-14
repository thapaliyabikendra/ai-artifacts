---
implements_concepts:
  - concepts/solid/overview
  - concepts/solid/srp
  - concepts/solid/ocp
  - concepts/solid/lsp
  - concepts/solid/isp
  - concepts/solid/dip
language: csharp
framework: [dotnet, abp]
used_by_skills: [clean-code-dotnet, abp-code-reviewer, abp-framework-patterns]
---

# SOLID Principles in C#/.NET

C# implementations of SOLID principles for ABP Framework applications.

## Single Responsibility Principle (SRP) {#srp}

> "A class should have only one reason to change."

### In ABP Application Services

```csharp
// ❌ Bad - AppService does too much
public class PatientAppService : ApplicationService
{
    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        // Validation
        if (string.IsNullOrEmpty(input.Email))
            throw new ArgumentException("Email required");
        if (!IsValidEmail(input.Email))
            throw new ArgumentException("Invalid email");

        // Business logic
        var patient = new Patient(GuidGenerator.Create(), input.Name, input.Email);

        // Persistence
        await _patientRepository.InsertAsync(patient);

        // Notification (another responsibility!)
        await SendWelcomeEmail(patient.Email);

        // Audit logging (yet another!)
        await LogPatientCreation(patient);

        // Mapping
        return new PatientDto { Id = patient.Id, Name = patient.Name };
    }
}

// ✅ Good - Single responsibility per class
public class PatientAppService : ApplicationService
{
    private readonly IPatientRepository _patientRepository;
    private readonly PatientMapper _mapper;

    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        // Validation is handled by FluentValidation (separate class)
        // Notifications handled by domain events (separate handler)
        // Audit logging handled by ABP audit system (infrastructure)

        var patient = new Patient(GuidGenerator.Create(), input.Name, input.Email);
        await _patientRepository.InsertAsync(patient);

        return _mapper.ToDto(patient);
    }
}

// Separate validator class
public class CreatePatientDtoValidator : AbstractValidator<CreatePatientDto>
{
    public CreatePatientDtoValidator()
    {
        RuleFor(x => x.Email).NotEmpty().EmailAddress();
        RuleFor(x => x.Name).NotEmpty().MaximumLength(100);
    }
}

// Separate event handler for notifications
public class PatientCreatedEventHandler : ILocalEventHandler<EntityCreatedEventData<Patient>>
{
    public async Task HandleEventAsync(EntityCreatedEventData<Patient> eventData)
    {
        await _emailService.SendWelcomeEmailAsync(eventData.Entity.Email);
    }
}
```

### In Domain Entities

```csharp
// ❌ Bad - Entity with multiple responsibilities
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string Name { get; private set; }
    public string Email { get; private set; }

    // Formatting responsibility
    public string GetFormattedName() => $"Patient: {Name}";
    public string GetEmailDisplay() => $"<{Email}>";

    // Notification responsibility
    public void SendAppointmentReminder() { }

    // Reporting responsibility
    public PatientReport GenerateReport() { }
}

// ✅ Good - Entity only manages its own state
public class Patient : FullAuditedAggregateRoot<Guid>
{
    public string Name { get; private set; }
    public string Email { get; private set; }

    public void UpdateName(string name)
    {
        Check.NotNullOrWhiteSpace(name, nameof(name));
        Name = name;
    }

    public void UpdateEmail(string email)
    {
        Check.NotNullOrWhiteSpace(email, nameof(email));
        Email = email;
    }
}

// Separate services for other responsibilities
public class PatientReportGenerator { }
public class PatientNotificationService { }
```

## Open/Closed Principle (OCP) {#ocp}

> "Open for extension, closed for modification."

### Strategy Pattern for Notifications

```csharp
// ❌ Bad - Must modify class to add new notification type
public class NotificationService
{
    public async Task SendAsync(string type, string message, string recipient)
    {
        switch (type)
        {
            case "email":
                await SendEmailAsync(message, recipient);
                break;
            case "sms":
                await SendSmsAsync(message, recipient);
                break;
            // Must add new case for each type!
            case "push":
                await SendPushAsync(message, recipient);
                break;
        }
    }
}

// ✅ Good - Extend by adding new classes
public interface INotificationSender
{
    string Type { get; }
    Task SendAsync(string message, string recipient);
}

public class EmailNotificationSender : INotificationSender
{
    public string Type => "email";
    public async Task SendAsync(string message, string recipient) { /* ... */ }
}

public class SmsNotificationSender : INotificationSender
{
    public string Type => "sms";
    public async Task SendAsync(string message, string recipient) { /* ... */ }
}

// New type - just add new class, no modification to existing code
public class PushNotificationSender : INotificationSender
{
    public string Type => "push";
    public async Task SendAsync(string message, string recipient) { /* ... */ }
}

public class NotificationService
{
    private readonly IEnumerable<INotificationSender> _senders;

    public NotificationService(IEnumerable<INotificationSender> senders)
    {
        _senders = senders;
    }

    public async Task SendAsync(string type, string message, string recipient)
    {
        var sender = _senders.FirstOrDefault(s => s.Type == type)
            ?? throw new NotSupportedException($"Notification type '{type}' not supported");

        await sender.SendAsync(message, recipient);
    }
}
```

### Template Method for Appointment Types

```csharp
// ✅ Good - Base class is closed, extend via inheritance
public abstract class AppointmentBase : FullAuditedAggregateRoot<Guid>
{
    public Guid DoctorId { get; protected set; }
    public Guid PatientId { get; protected set; }
    public DateTime ScheduledTime { get; protected set; }

    // Template method - closed for modification
    public void Schedule(DateTime time)
    {
        ValidateScheduleTime(time);
        ScheduledTime = time;
        OnScheduled();
    }

    // Open for extension
    protected abstract void ValidateScheduleTime(DateTime time);
    protected virtual void OnScheduled() { }
}

public class RegularAppointment : AppointmentBase
{
    protected override void ValidateScheduleTime(DateTime time)
    {
        if (time < DateTime.Now.AddHours(24))
            throw new BusinessException("Regular appointments require 24h notice");
    }
}

public class EmergencyAppointment : AppointmentBase
{
    protected override void ValidateScheduleTime(DateTime time)
    {
        // Emergency appointments have no time restriction
    }

    protected override void OnScheduled()
    {
        // Send urgent notifications
        AddLocalEvent(new EmergencyAppointmentScheduledEvent(this));
    }
}
```

## Liskov Substitution Principle (LSP) {#lsp}

> "Subtypes must be substitutable for their base types."

### Correct Inheritance

```csharp
// ❌ Bad - Violates LSP
public class Bird
{
    public virtual void Fly() { /* ... */ }
}

public class Penguin : Bird
{
    public override void Fly()
    {
        throw new NotSupportedException("Penguins can't fly!");  // Violates LSP!
    }
}

// ✅ Good - Proper abstraction
public abstract class Bird
{
    public abstract void Move();
}

public class Sparrow : Bird
{
    public override void Move() => Fly();
    private void Fly() { /* ... */ }
}

public class Penguin : Bird
{
    public override void Move() => Swim();
    private void Swim() { /* ... */ }
}
```

### Repository Implementations

```csharp
// ❌ Bad - SqlRepository violates contract
public interface IPatientRepository
{
    Task<Patient?> FindByEmailAsync(string email);
}

public class SqlPatientRepository : IPatientRepository
{
    public async Task<Patient?> FindByEmailAsync(string email)
    {
        // Unexpected behavior: throws instead of returning null
        var patient = await _dbContext.Patients.FirstOrDefaultAsync(p => p.Email == email);
        if (patient == null)
            throw new EntityNotFoundException(typeof(Patient), email);  // Violates contract!
        return patient;
    }
}

// ✅ Good - All implementations follow the contract
public interface IPatientRepository : IRepository<Patient, Guid>
{
    /// <summary>
    /// Finds a patient by email. Returns null if not found.
    /// </summary>
    Task<Patient?> FindByEmailAsync(string email);

    /// <summary>
    /// Gets a patient by email. Throws if not found.
    /// </summary>
    Task<Patient> GetByEmailAsync(string email);
}

public class EfCorePatientRepository : EfCoreRepository<ClinicDbContext, Patient, Guid>, IPatientRepository
{
    public async Task<Patient?> FindByEmailAsync(string email)
    {
        return await (await GetDbSetAsync())
            .FirstOrDefaultAsync(p => p.Email == email);
    }

    public async Task<Patient> GetByEmailAsync(string email)
    {
        return await FindByEmailAsync(email)
            ?? throw new EntityNotFoundException(typeof(Patient), email);
    }
}
```

### Covariance in Return Types

```csharp
// ✅ Good - Covariant return types (C# 9+)
public abstract class AppointmentServiceBase
{
    public virtual AppointmentDto CreateAppointment() => new AppointmentDto();
}

public class RegularAppointmentService : AppointmentServiceBase
{
    // Returns more specific type - LSP compliant
    public override RegularAppointmentDto CreateAppointment() => new RegularAppointmentDto();
}

public class RegularAppointmentDto : AppointmentDto
{
    public bool RequiresFollowUp { get; set; }
}
```

## Interface Segregation Principle (ISP) {#isp}

> "Clients should not be forced to depend on interfaces they don't use."

### Fat Interface Problem

```csharp
// ❌ Bad - Fat interface forces unnecessary implementations
public interface IPatientService
{
    Task<PatientDto> GetAsync(Guid id);
    Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientsInput input);
    Task<PatientDto> CreateAsync(CreatePatientDto input);
    Task<PatientDto> UpdateAsync(Guid id, UpdatePatientDto input);
    Task DeleteAsync(Guid id);
    Task<byte[]> ExportToExcelAsync();           // Not all clients need this
    Task ImportFromExcelAsync(byte[] data);      // Not all clients need this
    Task<PatientReportDto> GenerateReportAsync(Guid id);  // Not all clients need this
}

// Read-only consumer forced to implement everything
public class PatientReadOnlyService : IPatientService
{
    public Task<PatientDto> GetAsync(Guid id) { /* ... */ }
    public Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientsInput input) { /* ... */ }

    // Forced to implement these even though not needed
    public Task<PatientDto> CreateAsync(CreatePatientDto input)
        => throw new NotSupportedException();
    public Task<PatientDto> UpdateAsync(Guid id, UpdatePatientDto input)
        => throw new NotSupportedException();
    // ... more not supported methods
}

// ✅ Good - Segregated interfaces
public interface IPatientReadService
{
    Task<PatientDto> GetAsync(Guid id);
    Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientsInput input);
}

public interface IPatientWriteService
{
    Task<PatientDto> CreateAsync(CreatePatientDto input);
    Task<PatientDto> UpdateAsync(Guid id, UpdatePatientDto input);
    Task DeleteAsync(Guid id);
}

public interface IPatientExportService
{
    Task<byte[]> ExportToExcelAsync();
    Task ImportFromExcelAsync(byte[] data);
}

public interface IPatientReportService
{
    Task<PatientReportDto> GenerateReportAsync(Guid id);
}

// Full service implements all
public class PatientAppService :
    IPatientReadService,
    IPatientWriteService,
    IPatientExportService
{
    // Implement only what's needed
}

// Read-only service implements only read operations
public class PatientReadOnlyService : IPatientReadService
{
    public Task<PatientDto> GetAsync(Guid id) { /* ... */ }
    public Task<PagedResultDto<PatientDto>> GetListAsync(GetPatientsInput input) { /* ... */ }
}
```

### ABP Application Service Interfaces

```csharp
// ✅ Good - ABP's segregated interfaces
public interface IPatientAppService :
    ICrudAppService<
        PatientDto,
        Guid,
        GetPatientsInput,
        CreatePatientDto,
        UpdatePatientDto>
{
    // Additional methods specific to patients
}

// Or compose smaller interfaces
public interface IPatientAppService :
    IReadOnlyAppService<PatientDto, Guid, GetPatientsInput>,
    ICreateAppService<PatientDto, CreatePatientDto>,
    IUpdateAppService<PatientDto, Guid, UpdatePatientDto>,
    IDeleteAppService<Guid>
{
}
```

## Dependency Inversion Principle (DIP) {#dip}

> "Depend on abstractions, not concretions."

### High-Level Policy Independence

```csharp
// ❌ Bad - High-level module depends on low-level implementation
public class AppointmentScheduler
{
    private readonly SqlAppointmentRepository _repository;  // Concrete!
    private readonly SmtpEmailService _emailService;        // Concrete!

    public AppointmentScheduler()
    {
        _repository = new SqlAppointmentRepository();
        _emailService = new SmtpEmailService();
    }

    public async Task ScheduleAsync(Appointment appointment)
    {
        await _repository.InsertAsync(appointment);
        await _emailService.SendAsync(appointment.PatientEmail, "Scheduled");
    }
}

// ✅ Good - Depend on abstractions, inject dependencies
public class AppointmentScheduler
{
    private readonly IAppointmentRepository _repository;
    private readonly INotificationService _notificationService;

    public AppointmentScheduler(
        IAppointmentRepository repository,
        INotificationService notificationService)
    {
        _repository = repository;
        _notificationService = notificationService;
    }

    public async Task ScheduleAsync(Appointment appointment)
    {
        await _repository.InsertAsync(appointment);
        await _notificationService.NotifyAsync(
            appointment.PatientEmail,
            "Appointment Scheduled");
    }
}

// Abstractions owned by high-level module
public interface IAppointmentRepository : IRepository<Appointment, Guid>
{
    Task<List<Appointment>> GetByDoctorAsync(Guid doctorId, DateTime date);
}

public interface INotificationService
{
    Task NotifyAsync(string recipient, string message);
}
```

### ABP Module Dependencies

```csharp
// ✅ Good - Module depends on abstractions
[DependsOn(
    typeof(AbpDddDomainModule),           // Abstractions
    typeof(ClinicDomainSharedModule)      // Shared contracts
)]
public class ClinicDomainModule : AbpModule
{
}

[DependsOn(
    typeof(ClinicDomainModule),           // Domain abstractions
    typeof(AbpEntityFrameworkCoreModule)  // EF Core abstractions
)]
public class ClinicEntityFrameworkCoreModule : AbpModule
{
    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        context.Services.AddAbpDbContext<ClinicDbContext>(options =>
        {
            options.AddDefaultRepositories(includeAllEntities: true);
        });
    }
}
```

### Dependency Direction

```csharp
// ✅ Good - Dependencies flow from concrete to abstract
//
// Application Layer (defines interfaces)
public interface IPatientRepository : IRepository<Patient, Guid>
{
    Task<Patient?> FindByEmailAsync(string email);
}

// Infrastructure Layer (implements interfaces)
public class EfCorePatientRepository :
    EfCoreRepository<ClinicDbContext, Patient, Guid>,
    IPatientRepository
{
    public async Task<Patient?> FindByEmailAsync(string email)
    {
        return await (await GetDbSetAsync())
            .FirstOrDefaultAsync(p => p.Email == email);
    }
}

// Registration - concrete depends on abstract
public override void ConfigureServices(ServiceConfigurationContext context)
{
    context.Services.AddTransient<IPatientRepository, EfCorePatientRepository>();
}
```

## Related Concepts

- [SOLID Overview](../../concepts/solid/overview.md)
- [Single Responsibility Principle](../../concepts/solid/srp.md)
- [Open/Closed Principle](../../concepts/solid/ocp.md)
- [Liskov Substitution Principle](../../concepts/solid/lsp.md)
- [Interface Segregation Principle](../../concepts/solid/isp.md)
- [Dependency Inversion Principle](../../concepts/solid/dip.md)

## Sources

- Clean Code by Robert C. Martin
- Agile Software Development by Robert C. Martin
- ABP Framework Documentation
