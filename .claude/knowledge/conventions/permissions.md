# Permission Conventions

ABP Framework permission naming and structure.

## Naming Format

```
{ProjectName}.{Resource}.{Action}
```

| Part | Description | Example |
|------|-------------|---------|
| ProjectName | Solution prefix | `ClinicManagement` |
| Resource | Entity/feature (plural) | `Patients`, `Appointments` |
| Action | CRUD operation | `Create`, `Edit`, `Delete` |

## Standard Actions

| Action | Purpose | HTTP Verb |
|--------|---------|-----------|
| `Default` | View/Read access | GET |
| `Create` | Create new | POST |
| `Edit` | Update existing | PUT |
| `Delete` | Delete | DELETE |

## Permission Definition

### Constants File

```csharp
// In Application.Contracts/Permissions/{ProjectName}Permissions.cs
public static class ClinicManagementPermissions
{
    public const string GroupName = "ClinicManagement";

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
        public const string Cancel = Default + ".Cancel";  // Custom action
    }
}
```

### Permission Provider

```csharp
// In Application.Contracts/Permissions/{ProjectName}PermissionDefinitionProvider.cs
public class ClinicManagementPermissionDefinitionProvider : PermissionDefinitionProvider
{
    public override void Define(IPermissionDefinitionContext context)
    {
        var group = context.AddGroup(ClinicManagementPermissions.GroupName);

        // Patients
        var patients = group.AddPermission(
            ClinicManagementPermissions.Patients.Default,
            L("Permission:Patients"));

        patients.AddChild(
            ClinicManagementPermissions.Patients.Create,
            L("Permission:Patients.Create"));

        patients.AddChild(
            ClinicManagementPermissions.Patients.Edit,
            L("Permission:Patients.Edit"));

        patients.AddChild(
            ClinicManagementPermissions.Patients.Delete,
            L("Permission:Patients.Delete"));

        // Appointments
        var appointments = group.AddPermission(
            ClinicManagementPermissions.Appointments.Default,
            L("Permission:Appointments"));

        appointments.AddChild(
            ClinicManagementPermissions.Appointments.Create,
            L("Permission:Appointments.Create"));

        // ... etc
    }

    private static LocalizableString L(string name)
    {
        return LocalizableString.Create<ClinicManagementResource>(name);
    }
}
```

## Using Permissions

### In AppService

```csharp
public class PatientAppService : ApplicationService, IPatientAppService
{
    // Read - requires Default permission
    [Authorize(ClinicManagementPermissions.Patients.Default)]
    public async Task<PatientDto> GetAsync(Guid id)
    {
        // ...
    }

    // Create - requires Create permission
    [Authorize(ClinicManagementPermissions.Patients.Create)]
    public async Task<PatientDto> CreateAsync(CreateUpdatePatientDto input)
    {
        // ...
    }

    // Update - requires Edit permission
    [Authorize(ClinicManagementPermissions.Patients.Edit)]
    public async Task<PatientDto> UpdateAsync(Guid id, CreateUpdatePatientDto input)
    {
        // ...
    }

    // Delete - requires Delete permission
    [Authorize(ClinicManagementPermissions.Patients.Delete)]
    public async Task DeleteAsync(Guid id)
    {
        // ...
    }
}
```

### Checking Permissions Programmatically

```csharp
public class PatientAppService : ApplicationService
{
    public async Task<PatientDto> GetWithActionsAsync(Guid id)
    {
        var patient = await _repository.GetAsync(id);
        var dto = ObjectMapper.Map<Patient, PatientDto>(patient);

        // Check permissions for UI hints
        dto.CanEdit = await AuthorizationService
            .IsGrantedAsync(ClinicManagementPermissions.Patients.Edit);

        dto.CanDelete = await AuthorizationService
            .IsGrantedAsync(ClinicManagementPermissions.Patients.Delete);

        return dto;
    }
}
```

## Permission Hierarchy

```
ClinicManagement (Group)
├── ClinicManagement.Patients (Default = Read)
│   ├── ClinicManagement.Patients.Create
│   ├── ClinicManagement.Patients.Edit
│   └── ClinicManagement.Patients.Delete
├── ClinicManagement.Appointments
│   ├── ClinicManagement.Appointments.Create
│   ├── ClinicManagement.Appointments.Edit
│   ├── ClinicManagement.Appointments.Delete
│   └── ClinicManagement.Appointments.Cancel
└── ClinicManagement.Doctors
    └── ...
```

## Role to Permission Mapping

Document in `docs/domain/roles.md`:

| Role | Permissions |
|------|-------------|
| Admin | All permissions |
| Doctor | Patients.*, Appointments.* |
| Receptionist | Patients.Default, Patients.Create, Appointments.* |
| Patient | Own profile only (handled in code) |

## Best Practices

1. **Always use constants** - Never hardcode permission strings
2. **Parent-child hierarchy** - `Default` is parent, CRUD are children
3. **Localize names** - Use `L("Permission:...")` pattern
4. **Document in roles.md** - Map roles to permissions
5. **Check in AppService** - Use `[Authorize]` attribute

## Referenced By

- `openiddict-authorization` - Permission implementation
- `abp-framework-patterns` - AppService authorization
- `security-patterns` - Permission audits
