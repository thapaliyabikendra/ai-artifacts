# Folder Structure

ABP Framework project structure for layered monolith.

## Solution Structure

```
{SolutionName}/
├── src/
│   ├── {ProjectName}.Domain.Shared/        # Shared constants, enums
│   ├── {ProjectName}.Domain/               # Entities, domain services
│   ├── {ProjectName}.Application.Contracts/ # DTOs, service interfaces
│   ├── {ProjectName}.Application/          # AppService implementations
│   ├── {ProjectName}.EntityFrameworkCore/  # EF Core, repositories
│   ├── {ProjectName}.HttpApi/              # Controllers (optional)
│   ├── {ProjectName}.HttpApi.Host/         # API host
│   ├── {ProjectName}.AuthServer/           # Auth server (OpenIddict)
│   └── {ProjectName}.DbMigrator/           # Migration console app
├── test/
│   ├── {ProjectName}.TestBase/             # Test infrastructure
│   ├── {ProjectName}.Domain.Tests/         # Domain unit tests
│   ├── {ProjectName}.Application.Tests/    # AppService tests
│   └── {ProjectName}.EntityFrameworkCore.Tests/ # Repository tests
└── docs/
    ├── domain/                             # Domain documentation
    ├── architecture/                       # Architecture docs
    └── features/                           # Feature docs
```

## Feature-Based Organization

Organize files by feature (not by type):

```
{ProjectName}.Domain/
├── Patients/
│   ├── Patient.cs
│   ├── PatientManager.cs
│   └── IPatientRepository.cs
├── Appointments/
│   ├── Appointment.cs
│   └── AppointmentManager.cs
└── Doctors/
    └── Doctor.cs

{ProjectName}.Application.Contracts/
├── Patients/
│   ├── IPatientAppService.cs
│   ├── PatientDto.cs
│   ├── CreateUpdatePatientDto.cs
│   └── GetPatientListInput.cs
└── Appointments/
    ├── IAppointmentAppService.cs
    └── AppointmentDto.cs

{ProjectName}.Application/
├── Patients/
│   ├── PatientAppService.cs
│   └── CreateUpdatePatientDtoValidator.cs
└── Appointments/
    └── AppointmentAppService.cs

{ProjectName}.EntityFrameworkCore/
├── Patients/
│   └── PatientRepository.cs
└── EntityFrameworkCore/
    ├── {ProjectName}DbContext.cs
    └── {ProjectName}DbContextFactory.cs
```

## Layer Responsibilities

### Domain.Shared

```
{ProjectName}.Domain.Shared/
├── {Feature}/
│   └── {Feature}Consts.cs              # MaxLength constants
├── Enums/
│   └── {EnumName}.cs                   # Shared enums
├── Localization/
│   └── {ProjectName}Resource.cs        # Localization
└── {ProjectName}DomainSharedModule.cs
```

### Domain

```
{ProjectName}.Domain/
├── {Feature}/
│   ├── {Entity}.cs                     # Entity class
│   ├── {Entity}Manager.cs              # Domain service (optional)
│   └── I{Entity}Repository.cs          # Custom repository interface
├── Data/
│   └── I{ProjectName}DbSchemaMigrator.cs
└── {ProjectName}DomainModule.cs
```

### Application.Contracts

```
{ProjectName}.Application.Contracts/
├── {Feature}/
│   ├── I{Entity}AppService.cs          # Service interface
│   ├── {Entity}Dto.cs                  # Read DTO
│   ├── CreateUpdate{Entity}Dto.cs      # Write DTO
│   └── Get{Entity}ListInput.cs         # Query input
├── Permissions/
│   ├── {ProjectName}Permissions.cs     # Permission constants
│   └── {ProjectName}PermissionDefinitionProvider.cs
└── {ProjectName}ApplicationContractsModule.cs
```

### Application

```
{ProjectName}.Application/
├── {Feature}/
│   ├── {Entity}AppService.cs           # Service implementation
│   └── {Dto}Validator.cs               # FluentValidation
├── {ProjectName}ApplicationModule.cs
└── {ProjectName}ApplicationMappers.cs  # Mapperly mappers
```

### EntityFrameworkCore

```
{ProjectName}.EntityFrameworkCore/
├── {Feature}/
│   └── {Entity}Repository.cs           # Custom repository
├── EntityFrameworkCore/
│   ├── {ProjectName}DbContext.cs
│   ├── {ProjectName}DbContextFactory.cs
│   └── {ProjectName}EntityTypeConfigurations.cs
├── Migrations/
│   └── *.cs                            # EF Core migrations
└── {ProjectName}EntityFrameworkCoreModule.cs
```

## Test Structure

```
{ProjectName}.TestBase/
├── {Feature}/
│   ├── {Entity}TestData.cs             # Test constants
│   └── {Entity}TestDataSeedContributor.cs
└── {ProjectName}TestBaseModule.cs

{ProjectName}.Application.Tests/
├── {Feature}/
│   └── {Entity}AppService_Tests.cs
└── {ProjectName}ApplicationTestModule.cs

{ProjectName}.Domain.Tests/
├── {Feature}/
│   └── {Entity}Manager_Tests.cs
└── {ProjectName}DomainTestModule.cs
```

## Documentation Structure

```
docs/
├── domain/
│   ├── entities/
│   │   └── {entity}.md                 # Entity definitions
│   ├── business-rules.md               # BR-XXX rules
│   ├── permissions.md                  # Permission definitions
│   └── roles.md                        # Role mappings
├── architecture/
│   ├── README.md                       # Project overview
│   └── patterns.md                     # Code patterns
└── features/
    └── {feature}/
        ├── requirements.md
        ├── technical-design.md
        └── test-cases.md
```

## Referenced By

- All skills - Project navigation
- `abp-framework-patterns` - File locations
- `efcore-patterns` - DbContext location
