---
name: abp-framework-patterns
description: "Master ABP Framework patterns including repository pattern, unit of work, domain services, application services, authorization, multi-tenancy, background jobs, and distributed events. Use when: (1) building ABP-based applications with DDD architecture, (2) creating CRUD services with Entity, AppService, DTOs, validators, (3) handling authorization/permissions, (4) generating ABP module code."
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

**Robust Event Handler Pattern (with Multi-Tenancy & Idempotency):**
```csharp
// For cross-tenant event processing with error handling
public class EntitySyncEventHandler :
    IDistributedEventHandler<EntityUpdatedEto>,
    ITransientDependency
{
    private readonly IRepository<Entity, Guid> _repository;
    private readonly IDataFilter _dataFilter;
    private readonly ILogger<EntitySyncEventHandler> _logger;

    public EntitySyncEventHandler(
        IRepository<Entity, Guid> repository,
        IDataFilter dataFilter,
        ILogger<EntitySyncEventHandler> logger)
    {
        _repository = repository;
        _dataFilter = dataFilter;
        _logger = logger;
    }

    public async Task HandleEventAsync(EntityUpdatedEto eto)
    {
        // Disable tenant filter for cross-tenant sync
        using (_dataFilter.Disable<IMultiTenant>())
        {
            try
            {
                _logger.LogInformation("Processing entity sync: {Id}", eto.Id);

                // Idempotency check - find existing by unique identifier
                var existing = await _repository.FirstOrDefaultAsync(
                    x => x.ExternalId == eto.ExternalId);

                if (existing != null)
                {
                    // Update existing
                    ObjectMapper.Map(eto, existing);
                    await _repository.UpdateAsync(existing);
                }
                else
                {
                    // Create new
                    var entity = ObjectMapper.Map<EntityUpdatedEto, Entity>(eto);
                    await _repository.InsertAsync(entity);
                }

                _logger.LogInformation("Entity sync completed: {Id}", eto.Id);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Entity sync failed: {Id}", eto.Id);
                throw new UserFriendlyException($"Failed to sync entity: {ex.Message}");
            }
        }
    }
}
```

**Key Patterns:**
- **Idempotency**: Check for existing entity before insert to handle duplicate events
- **Multi-Tenancy**: Use `_dataFilter.Disable<IMultiTenant>()` for cross-tenant events
- **Error Handling**: Catch, log, and throw `UserFriendlyException`
- **Logging**: Log at start, end, and exception points

### 8. Object Mapping with Mapperly

ABP 10.x uses **Mapperly** (source generator) instead of AutoMapper for better performance.

**Configure Mapper:**
```csharp
// Application/ClinicManagementSystemApplicationMappers.cs
[Mapper]
public partial class ClinicManagementSystemApplicationMappers
{
    // Entity to DTO
    public partial PatientDto PatientToDto(Patient patient);
    public partial List<PatientDto> PatientsToDtos(List<Patient> patients);

    // DTO to Entity (for creation)
    public partial Patient CreateDtoToPatient(CreateUpdatePatientDto dto);

    // DTO to Entity (for update) - ignores Id
    [MapperIgnoreTarget(nameof(Patient.Id))]
    public partial void UpdatePatientFromDto(CreateUpdatePatientDto dto, Patient patient);

    // Complex mapping with navigation properties
    [MapProperty(nameof(Appointment.Patient.FirstName), nameof(AppointmentDto.PatientName))]
    [MapProperty(nameof(Appointment.Doctor.FullName), nameof(AppointmentDto.DoctorName))]
    public partial AppointmentDto AppointmentToDto(Appointment appointment);
}
```

**Usage in AppService:**
```csharp
public class PatientAppService : ApplicationService, IPatientAppService
{
    private readonly IRepository<Patient, Guid> _patientRepository;
    private readonly ClinicManagementSystemApplicationMappers _mapper;

    public PatientAppService(
        IRepository<Patient, Guid> patientRepository,
        ClinicManagementSystemApplicationMappers mapper)
    {
        _patientRepository = patientRepository;
        _mapper = mapper;
    }

    public async Task<PatientDto> GetAsync(Guid id)
    {
        var patient = await _patientRepository.GetAsync(id);
        return _mapper.PatientToDto(patient);
    }

    public async Task<PatientDto> CreateAsync(CreateUpdatePatientDto input)
    {
        var patient = _mapper.CreateDtoToPatient(input);
        patient = await _patientRepository.InsertAsync(patient);
        return _mapper.PatientToDto(patient);
    }

    public async Task<PatientDto> UpdateAsync(Guid id, CreateUpdatePatientDto input)
    {
        var patient = await _patientRepository.GetAsync(id);
        _mapper.UpdatePatientFromDto(input, patient);
        await _patientRepository.UpdateAsync(patient);
        return _mapper.PatientToDto(patient);
    }
}
```

**Register in Module:**
```csharp
public override void ConfigureServices(ServiceConfigurationContext context)
{
    // Mapperly mappers are auto-registered as singletons
    context.Services.AddSingleton<ClinicManagementSystemApplicationMappers>();
}
```

### 9. Data Seeding

**IDataSeedContributor Pattern:**
```csharp
// Domain/Data/ClinicDataSeedContributor.cs
public class ClinicDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    private readonly IRepository<Doctor, Guid> _doctorRepository;
    private readonly IGuidGenerator _guidGenerator;

    public ClinicDataSeedContributor(
        IRepository<Doctor, Guid> doctorRepository,
        IGuidGenerator guidGenerator)
    {
        _doctorRepository = doctorRepository;
        _guidGenerator = guidGenerator;
    }

    public async Task SeedAsync(DataSeedContext context)
    {
        // Check if data already exists (idempotent)
        if (await _doctorRepository.GetCountAsync() > 0)
        {
            return;
        }

        // Seed initial data
        var doctors = new List<Doctor>
        {
            new Doctor(_guidGenerator.Create(), "Dr. Smith", "Cardiology", "smith@clinic.com"),
            new Doctor(_guidGenerator.Create(), "Dr. Jones", "Pediatrics", "jones@clinic.com"),
        };

        foreach (var doctor in doctors)
        {
            await _doctorRepository.InsertAsync(doctor);
        }
    }
}
```

**Tenant-Specific Seeding:**
```csharp
public async Task SeedAsync(DataSeedContext context)
{
    // context.TenantId is available for tenant-specific seeding
    if (context.TenantId.HasValue)
    {
        await SeedTenantDataAsync(context.TenantId.Value);
    }
    else
    {
        await SeedHostDataAsync();
    }
}
```

**Test Data Seeding:**
```csharp
// Test/TestBase/ClinicManagementSystemTestDataSeedContributor.cs
public class ClinicManagementSystemTestDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    public static readonly Guid TestPatientId = Guid.Parse("2e701e62-0953-4dd3-910b-dc6cc93ccb0d");
    public static readonly Guid TestDoctorId = Guid.Parse("3a801f73-1064-5ee4-a21c-ed7dd4ddc1e");

    private readonly IRepository<Patient, Guid> _patientRepository;
    private readonly IRepository<Doctor, Guid> _doctorRepository;

    public async Task SeedAsync(DataSeedContext context)
    {
        await _patientRepository.InsertAsync(new Patient(
            TestPatientId,
            "Test",
            "Patient",
            "test@example.com"
        ));

        await _doctorRepository.InsertAsync(new Doctor(
            TestDoctorId,
            "Test Doctor",
            "General",
            "doctor@example.com"
        ));
    }
}
```

### 10. Module Configuration

**Module Class Pattern:**
```csharp
[DependsOn(
    typeof(ClinicManagementSystemDomainModule),
    typeof(AbpIdentityDomainModule),
    typeof(AbpPermissionManagementDomainModule)
)]
public class ClinicManagementSystemApplicationModule : AbpModule
{
    public override void PreConfigureServices(ServiceConfigurationContext context)
    {
        // Configure options before other services
        PreConfigure<AbpIdentityOptions>(options =>
        {
            options.ExternalLoginProviders.Add<GoogleExternalLoginProvider>();
        });
    }

    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        // Configure ABP features
        Configure<AbpAutoMapperOptions>(options =>
        {
            options.AddMaps<ClinicManagementSystemApplicationModule>();
        });

        // Register application services
        context.Services.AddTransient<IPatientAppService, PatientAppService>();

        // Configure distributed cache
        Configure<AbpDistributedCacheOptions>(options =>
        {
            options.KeyPrefix = "Clinic:";
        });
    }

    public override void OnApplicationInitialization(ApplicationInitializationContext context)
    {
        var app = context.GetApplicationBuilder();
        var env = context.GetEnvironment();

        // Application initialization logic
        if (env.IsDevelopment())
        {
            app.UseDeveloperExceptionPage();
        }
    }
}
```

**Object Extension Configuration:**
```csharp
// Domain.Shared/ClinicManagementSystemModuleExtensionConfigurator.cs
public static class ClinicManagementSystemModuleExtensionConfigurator
{
    public static void Configure()
    {
        // Add custom properties to ABP entities
        ObjectExtensionManager.Instance.Modules()
            .ConfigureIdentity(identity =>
            {
                identity.ConfigureUser(user =>
                {
                    user.AddOrUpdateProperty<string>(
                        "Title",
                        property =>
                        {
                            property.Attributes.Add(new StringLengthAttribute(64));
                        }
                    );
                });
            });
    }
}
```

### 11. Multi-Tenancy Patterns

**Tenant-Aware Entities:**
```csharp
public class Patient : FullAuditedAggregateRoot<Guid>, IMultiTenant
{
    public Guid? TenantId { get; set; }
    public string FirstName { get; private set; }
    // ABP automatically filters by TenantId
}
```

**Cross-Tenant Operations:**
```csharp
public class CrossTenantService : ApplicationService
{
    private readonly IDataFilter _dataFilter;
    private readonly ICurrentTenant _currentTenant;

    public async Task<List<PatientDto>> GetAllTenantsPatients()
    {
        // Disable tenant filter
        using (_dataFilter.Disable<IMultiTenant>())
        {
            return await _patientRepository.GetListAsync();
        }
    }

    public async Task OperateOnTenant(Guid tenantId)
    {
        // Switch to specific tenant
        using (_currentTenant.Change(tenantId))
        {
            await DoTenantSpecificOperation();
        }
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

## CRUD Service Generation

For generating complete CRUD services with all ABP artifacts:

**See: [references/crud-templates.md](references/crud-templates.md)**

The templates include:
- Entity with proper base class and encapsulation
- AppService interface and implementation
- DTOs (EntityDto, CreateUpdateDto, GetListInput)
- FluentValidation validators
- Permission definitions
- AutoMapper profiles

### Generation Workflow

1. **Gather requirements** from technical design
2. **Create entity** in Domain layer
3. **Create DTOs** in Application.Contracts
4. **Create AppService** in Application layer
5. **Create validator** with FluentValidation
6. **Configure DbContext** in EntityFrameworkCore
7. **Add permissions** to PermissionDefinitionProvider
8. **Run migration** and test

## References

- [references/crud-templates.md](references/crud-templates.md) - CRUD service code templates

## External Resources

- **ABP Documentation**: https://docs.abp.io/
- **ABP Community**: https://community.abp.io/
- **ABP GitHub**: https://github.com/abpframework/abp
- **Domain-Driven Design**: Evans, Eric. "Domain-Driven Design"
