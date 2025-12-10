---
name: abp-framework-patterns
description: Master ABP Framework patterns including repository pattern, unit of work, domain services, application services, authorization, multi-tenancy, background jobs, and distributed events. Use when building ABP-based applications with DDD architecture, implementing CRUD services, handling authorization, or working with ABP modules.
---

# ABP Framework Patterns

Master ABP Framework patterns and best practices for building maintainable, scalable applications following Domain-Driven Design principles.

## When to Use This Skill

- Building new ABP Framework applications
- Implementing domain logic and business rules
- Setting up authorization and permissions
- Working with ABP repositories and unit of work
- Implementing background jobs
- Handling distributed events
- Understanding ABP module system
- Migrating from older ABP versions

## Core ABP Concepts

### 1. Application Architecture Layers

ABP follows DDD layered architecture:

```
Domain.Shared    → Constants, enums, shared types
Domain           → Entities, repositories, domain services, domain events
Application.Contracts → DTOs, application service interfaces
Application      → Application services, auto mapper profiles
EntityFrameworkCore → DbContext, repository implementations
HttpApi          → Controllers
HttpApi.Host     → Startup, configuration
```

**Key principle**: Dependencies flow downward. Application depends on Domain, but Domain never depends on Application.

### 2. Repository Pattern

**ABP Generic Repository:**
```csharp
public interface IRepository<TEntity, TKey> : IBasicRepository<TEntity, TKey>
    where TEntity : class, IEntity<TKey>
{
    Task<TEntity> GetAsync(TKey id, bool includeDetails = true);
    Task<List<TEntity>> GetListAsync(bool includeDetails = false);
    Task<long> GetCountAsync();
}

// Usage in Application Service
public class PatientAppService : ApplicationService
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

    public async Task<PagedResultDto<PatientDto>> GetListAsync(PagedAndSortedResultRequestDto input)
    {
        var totalCount = await _patientRepository.GetCountAsync();

        var patients = await _patientRepository
            .GetQueryableAsync()
            .ContinueWith(query => query.Result
                .OrderBy(input.Sorting ?? "name")
                .PageBy(input.SkipCount, input.MaxResultCount)
                .ToListAsync());

        return new PagedResultDto<PatientDto>(
            totalCount,
            ObjectMapper.Map<List<Patient>, List<PatientDto>>(patients)
        );
    }
}
```

**Custom Repository Methods:**
```csharp
// Define interface in Domain layer
public interface IPatientRepository : IRepository<Patient, Guid>
{
    Task<List<Patient>> GetActivePatientsByDoctorAsync(Guid doctorId);
    Task<Patient> FindByEmailAsync(string email);
}

// Implement in EntityFrameworkCore layer
public class PatientRepository : EfCoreRepository<ClinicDbContext, Patient, Guid>, IPatientRepository
{
    public PatientRepository(IDbContextProvider<ClinicDbContext> dbContextProvider)
        : base(dbContextProvider)
    {
    }

    public async Task<List<Patient>> GetActivePatientsByDoctorAsync(Guid doctorId)
    {
        var dbSet = await GetDbSetAsync();
        return await dbSet
            .Where(p => p.PrimaryDoctorId == doctorId && p.IsActive)
            .Include(p => p.Appointments)
            .ToListAsync();
    }

    public async Task<Patient> FindByEmailAsync(string email)
    {
        var dbSet = await GetDbSetAsync();
        return await dbSet.FirstOrDefaultAsync(p => p.Email == email);
    }
}
```

### 3. Unit of Work

ABP automatically manages Unit of Work for application service methods.

**Automatic UoW:**
```csharp
public class AppointmentAppService : ApplicationService
{
    private readonly IRepository<Appointment, Guid> _appointmentRepository;
    private readonly IRepository<Patient, Guid> _patientRepository;

    // This method is automatically wrapped in a UoW
    // All changes are committed together or rolled back on exception
    public async Task<AppointmentDto> CreateAsync(CreateAppointmentDto input)
    {
        // Update patient's last appointment date
        var patient = await _patientRepository.GetAsync(input.PatientId);
        patient.LastAppointmentDate = input.AppointmentDate;

        // Create appointment
        var appointment = new Appointment(
            GuidGenerator.Create(),
            input.PatientId,
            input.DoctorId,
            input.AppointmentDate
        );

        await _appointmentRepository.InsertAsync(appointment);

        // Both changes committed together automatically
        return ObjectMapper.Map<Appointment, AppointmentDto>(appointment);
    }
}
```

**Manual UoW Control:**
```csharp
public class ReportService : ApplicationService
{
    private readonly IUnitOfWorkManager _unitOfWorkManager;

    public ReportService(IUnitOfWorkManager unitOfWorkManager)
    {
        _unitOfWorkManager = unitOfWorkManager;
    }

    [UnitOfWork(isTransactional: false)] // Disable transaction for long-running operation
    public async Task GenerateLargeReportAsync()
    {
        // Read-only operation, no transaction needed
        // Improves performance for large data reads
    }

    public async Task ProcessBatchAsync(List<Guid> patientIds)
    {
        foreach (var patientId in patientIds)
        {
            // Create new UoW for each iteration
            using (var uow = _unitOfWorkManager.Begin(requiresNew: true))
            {
                await ProcessPatientAsync(patientId);
                await uow.CompleteAsync();
            }
        }
    }
}
```

### 4. Domain Services vs Application Services

**Domain Service** (in Domain layer):
```csharp
// Use when business logic involves multiple entities or external domain concepts
public class AppointmentManager : DomainService
{
    private readonly IRepository<Appointment, Guid> _appointmentRepository;
    private readonly IRepository<DoctorSchedule, Guid> _scheduleRepository;

    public AppointmentManager(
        IRepository<Appointment, Guid> appointmentRepository,
        IRepository<DoctorSchedule, Guid> scheduleRepository)
    {
        _appointmentRepository = appointmentRepository;
        _scheduleRepository = scheduleRepository;
    }

    public async Task<Appointment> CreateAsync(
        Guid patientId,
        Guid doctorId,
        DateTime appointmentDate,
        string description)
    {
        // Business rule: Check if doctor is available
        await CheckDoctorAvailabilityAsync(doctorId, appointmentDate);

        // Business rule: Check for conflicts
        await CheckAppointmentConflictsAsync(doctorId, appointmentDate);

        var appointment = new Appointment(
            GuidGenerator.Create(),
            patientId,
            doctorId,
            appointmentDate,
            description
        );

        return await _appointmentRepository.InsertAsync(appointment);
    }

    private async Task CheckDoctorAvailabilityAsync(Guid doctorId, DateTime appointmentDate)
    {
        var schedule = await _scheduleRepository.FirstOrDefaultAsync(
            s => s.DoctorId == doctorId && s.DayOfWeek == appointmentDate.DayOfWeek);

        if (schedule == null)
        {
            throw new BusinessException("Doctor not available on this day");
        }

        var timeOfDay = appointmentDate.TimeOfDay;
        if (timeOfDay < schedule.StartTime || timeOfDay > schedule.EndTime)
        {
            throw new BusinessException("Doctor not available at this time");
        }
    }

    private async Task CheckAppointmentConflictsAsync(Guid doctorId, DateTime appointmentDate)
    {
        var hasConflict = await _appointmentRepository.AnyAsync(a =>
            a.DoctorId == doctorId &&
            a.AppointmentDate == appointmentDate &&
            a.Status != AppointmentStatus.Cancelled);

        if (hasConflict)
        {
            throw new BusinessException("Doctor already has an appointment at this time");
        }
    }
}
```

**Application Service** (in Application layer):
```csharp
// Use for orchestration, DTO mapping, authorization
public class AppointmentAppService : ApplicationService, IAppointmentAppService
{
    private readonly AppointmentManager _appointmentManager;
    private readonly IRepository<Patient, Guid> _patientRepository;

    public AppointmentAppService(
        AppointmentManager appointmentManager,
        IRepository<Patient, Guid> patientRepository)
    {
        _appointmentManager = appointmentManager;
        _patientRepository = patientRepository;
    }

    [Authorize(ClinicPermissions.Appointments.Create)]
    public async Task<AppointmentDto> CreateAsync(CreateAppointmentDto input)
    {
        // Validate patient exists
        await _patientRepository.GetAsync(input.PatientId);

        // Delegate to domain service
        var appointment = await _appointmentManager.CreateAsync(
            input.PatientId,
            input.DoctorId,
            input.AppointmentDate,
            input.Description
        );

        return ObjectMapper.Map<Appointment, AppointmentDto>(appointment);
    }
}
```

### 5. Authorization

**Define Permissions:**
```csharp
// Domain.Shared/Permissions/ClinicPermissions.cs
public static class ClinicPermissions
{
    public const string GroupName = "Clinic";

    public static class Patients
    {
        public const string Default = GroupName + ".Patients";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
    }

    public static class Appointments
    {
        public const string Default = GroupName + ".Appointments";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
        public const string ViewAll = Default + ".ViewAll"; // Admins only
    }
}

// Application.Contracts/Permissions/ClinicPermissionDefinitionProvider.cs
public class ClinicPermissionDefinitionProvider : PermissionDefinitionProvider
{
    public override void Define(IPermissionDefinitionContext context)
    {
        var clinicGroup = context.AddGroup(ClinicPermissions.GroupName);

        var patientsPermission = clinicGroup.AddPermission(
            ClinicPermissions.Patients.Default,
            L("Permission:Patients"));

        patientsPermission.AddChild(
            ClinicPermissions.Patients.Create,
            L("Permission:Patients.Create"));

        patientsPermission.AddChild(
            ClinicPermissions.Patients.Edit,
            L("Permission:Patients.Edit"));

        patientsPermission.AddChild(
            ClinicPermissions.Patients.Delete,
            L("Permission:Patients.Delete"));
    }

    private static LocalizableString L(string name)
    {
        return LocalizableString.Create<ClinicResource>(name);
    }
}
```

**Grant Permissions to Roles:**
```csharp
// EntityFrameworkCore/EntityFrameworkCore/ClinicDbMigrationService.cs
public class ClinicDbMigrationService
{
    private readonly IPermissionManager _permissionManager;

    private async Task SeedDataAsync()
    {
        // Grant all permissions to Admin role
        await _permissionManager.SetForRoleAsync(
            "Admin",
            ClinicPermissions.Patients.Default,
            true);

        // Grant limited permissions to Doctor role
        await _permissionManager.SetForRoleAsync(
            "Doctor",
            ClinicPermissions.Appointments.Default,
            true);

        // Receptionist can create patients and appointments
        await _permissionManager.SetForRoleAsync(
            "Receptionist",
            ClinicPermissions.Patients.Create,
            true);

        await _permissionManager.SetForRoleAsync(
            "Receptionist",
            ClinicPermissions.Appointments.Create,
            true);
    }
}
```

**Use Permissions:**
```csharp
// Declarative authorization
[Authorize(ClinicPermissions.Patients.Create)]
public async Task<PatientDto> CreateAsync(CreatePatientDto input)
{
    // Method protected by permission
}

// Imperative authorization
public async Task<AppointmentDto> GetAsync(Guid id)
{
    var appointment = await _appointmentRepository.GetAsync(id);

    // Check if user can view this appointment
    if (appointment.DoctorId != CurrentUser.Id)
    {
        await AuthorizationService.CheckAsync(
            ClinicPermissions.Appointments.ViewAll);
    }

    return ObjectMapper.Map<Appointment, AppointmentDto>(appointment);
}

// Check permission without throwing exception
public async Task<bool> CanCreatePatientAsync()
{
    return await AuthorizationService.IsGrantedAsync(
        ClinicPermissions.Patients.Create);
}
```

### 6. Background Jobs

**Define Background Job:**
```csharp
// Application/BackgroundJobs/AppointmentReminderJob.cs
public class AppointmentReminderJob : AsyncBackgroundJob<AppointmentReminderArgs>, ITransientDependency
{
    private readonly IRepository<Appointment, Guid> _appointmentRepository;
    private readonly IEmailSender _emailSender;

    public AppointmentReminderJob(
        IRepository<Appointment, Guid> appointmentRepository,
        IEmailSender emailSender)
    {
        _appointmentRepository = appointmentRepository;
        _emailSender = emailSender;
    }

    public override async Task ExecuteAsync(AppointmentReminderArgs args)
    {
        var appointment = await _appointmentRepository.GetAsync(args.AppointmentId);

        await _emailSender.SendAsync(
            appointment.Patient.Email,
            "Appointment Reminder",
            $"You have an appointment on {appointment.AppointmentDate}"
        );
    }
}

public class AppointmentReminderArgs
{
    public Guid AppointmentId { get; set; }
}
```

**Enqueue Background Job:**
```csharp
public class AppointmentAppService : ApplicationService
{
    private readonly IBackgroundJobManager _backgroundJobManager;

    public async Task<AppointmentDto> CreateAsync(CreateAppointmentDto input)
    {
        var appointment = await _appointmentManager.CreateAsync(/*...*/);

        // Schedule reminder for 24 hours before appointment
        var reminderTime = appointment.AppointmentDate.AddHours(-24);

        await _backgroundJobManager.EnqueueAsync(
            new AppointmentReminderArgs { AppointmentId = appointment.Id },
            delay: reminderTime - DateTime.Now
        );

        return ObjectMapper.Map<Appointment, AppointmentDto>(appointment);
    }
}
```

### 7. Distributed Events

**Publish Event:**
```csharp
// Domain/Patients/Patient.cs
public class Patient : AggregateRoot<Guid>
{
    // Add domain event to aggregate root
    public void Activate()
    {
        IsActive = true;

        AddDistributedEvent(new PatientActivatedEto
        {
            Id = Id,
            Name = Name,
            Email = Email
        });
    }
}

// Or publish from Application Service
public class PatientAppService : ApplicationService
{
    private readonly IDistributedEventBus _distributedEventBus;

    public async Task ActivateAsync(Guid id)
    {
        var patient = await _patientRepository.GetAsync(id);
        patient.Activate();

        // Event automatically published by ABP when UoW completes
        // Or manually publish:
        await _distributedEventBus.PublishAsync(new PatientActivatedEto
        {
            Id = patient.Id,
            Name = patient.Name,
            Email = patient.Email
        });
    }
}
```

**Handle Event:**
```csharp
// Application/EventHandlers/PatientActivatedEventHandler.cs
public class PatientActivatedEventHandler :
    IDistributedEventHandler<PatientActivatedEto>,
    ITransientDependency
{
    private readonly IEmailSender _emailSender;
    private readonly ILogger<PatientActivatedEventHandler> _logger;

    public PatientActivatedEventHandler(
        IEmailSender emailSender,
        ILogger<PatientActivatedEventHandler> logger)
    {
        _emailSender = emailSender;
        _logger = logger;
    }

    public async Task HandleEventAsync(PatientActivatedEto eventData)
    {
        _logger.LogInformation($"Patient activated: {eventData.Name}");

        await _emailSender.SendAsync(
            eventData.Email,
            "Welcome to the Clinic",
            "Your patient account has been activated"
        );
    }
}
```

### 8. AutoMapper Configuration

```csharp
// Application/ClinicApplicationAutoMapperProfile.cs
public class ClinicApplicationAutoMapperProfile : Profile
{
    public ClinicApplicationAutoMapperProfile()
    {
        // Entity to DTO
        CreateMap<Patient, PatientDto>();
        CreateMap<Appointment, AppointmentDto>()
            .ForMember(dest => dest.PatientName,
                opt => opt.MapFrom(src => src.Patient.Name))
            .ForMember(dest => dest.DoctorName,
                opt => opt.MapFrom(src => src.Doctor.FullName));

        // Create DTO to Entity
        CreateMap<CreatePatientDto, Patient>()
            .Ignore(x => x.Id)
            .Ignore(x => x.ExtraProperties)
            .Ignore(x => x.ConcurrencyStamp);

        // Update DTO to Entity
        CreateMap<UpdatePatientDto, Patient>()
            .Ignore(x => x.Id)
            .Ignore(x => x.ExtraProperties)
            .Ignore(x => x.ConcurrencyStamp);
    }
}
```

## Best Practices

1. **Keep Domain Layer Pure**: No dependencies on infrastructure or application concerns
2. **Use Domain Services**: For complex business logic involving multiple entities
3. **Use Application Services**: For orchestration, authorization, and DTO mapping
4. **Custom Repositories**: Only when you need custom queries beyond LINQ
5. **Background Jobs**: For long-running operations or delayed tasks
6. **Distributed Events**: For loose coupling between modules
7. **Authorization**: Always check permissions in Application Services
8. **Unit of Work**: Trust ABP's automatic management, override only when needed
9. **Validation**: Use FluentValidation in DTOs, business rules in Domain
10. **Logging**: Use ILogger, ABP automatically includes context

## Common Patterns

### Soft Delete
```csharp
public class Patient : FullAuditedAggregateRoot<Guid>, ISoftDelete
{
    public bool IsDeleted { get; set; }
    // ABP automatically filters out soft-deleted entities
}
```

### Multi-Tenancy
```csharp
public class Patient : FullAuditedAggregateRoot<Guid>, IMultiTenant
{
    public Guid? TenantId { get; set; }
    // ABP automatically filters by current tenant
}
```

### Audit Fields
```csharp
public class Patient : FullAuditedAggregateRoot<Guid>
{
    // Provides: CreationTime, CreatorId, LastModificationTime,
    // LastModifierId, IsDeleted, DeletionTime, DeleterId
}
```

## Resources

- **ABP Documentation**: https://docs.abp.io/
- **ABP Community**: https://community.abp.io/
- **ABP GitHub**: https://github.com/abpframework/abp
- **Domain-Driven Design**: Evans, Eric. "Domain-Driven Design"
