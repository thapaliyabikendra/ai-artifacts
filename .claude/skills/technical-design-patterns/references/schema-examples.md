# Database Schema Examples

Real-world examples of database schemas for ABP Framework applications.

## Patient Entity

### Table: Patients

| Column | Type | Nullable | Default | Constraints | Description |
|--------|------|----------|---------|-------------|-------------|
| `Id` | `uuid` | NO | `gen_random_uuid()` | PK | Unique identifier |
| `FirstName` | `varchar(50)` | NO | - | - | Patient first name |
| `LastName` | `varchar(50)` | NO | - | - | Patient last name |
| `Email` | `varchar(255)` | NO | - | UNIQUE | Contact email |
| `PhoneNumber` | `varchar(20)` | YES | - | - | Contact phone |
| `DateOfBirth` | `date` | NO | - | - | Birth date |
| `Gender` | `smallint` | NO | `0` | - | Enum: 0=Male, 1=Female, 2=Other |
| `Address` | `varchar(500)` | YES | - | - | Full address |
| `IsActive` | `boolean` | NO | `true` | - | Active status |
| `CreationTime` | `timestamp` | NO | `now()` | - | ABP audit |
| `CreatorId` | `uuid` | YES | - | - | ABP audit |
| `LastModificationTime` | `timestamp` | YES | - | - | ABP audit |
| `LastModifierId` | `uuid` | YES | - | - | ABP audit |
| `IsDeleted` | `boolean` | NO | `false` | - | ABP soft delete |
| `DeleterId` | `uuid` | YES | - | - | ABP audit |
| `DeletionTime` | `timestamp` | YES | - | - | ABP audit |

### Indexes

| Name | Columns | Type | Purpose |
|------|---------|------|---------|
| `PK_Patients` | `Id` | Primary | Primary key |
| `IX_Patients_Email` | `Email` | Unique | Email lookup, uniqueness |
| `IX_Patients_Name` | `LastName`, `FirstName` | B-tree | Name search |
| `IX_Patients_IsDeleted` | `IsDeleted` | Partial (false) | Active records |

### EF Core Configuration

```csharp
public class PatientConfiguration : IEntityTypeConfiguration<Patient>
{
    public void Configure(EntityTypeBuilder<Patient> builder)
    {
        builder.ToTable("Patients");

        builder.HasKey(x => x.Id);

        builder.Property(x => x.FirstName)
            .HasMaxLength(PatientConsts.MaxFirstNameLength)
            .IsRequired();

        builder.Property(x => x.LastName)
            .HasMaxLength(PatientConsts.MaxLastNameLength)
            .IsRequired();

        builder.Property(x => x.Email)
            .HasMaxLength(PatientConsts.MaxEmailLength)
            .IsRequired();

        builder.HasIndex(x => x.Email)
            .IsUnique();

        builder.HasIndex(x => new { x.LastName, x.FirstName });

        builder.HasQueryFilter(x => !x.IsDeleted);
    }
}
```

---

## Appointment Entity

### Table: Appointments

| Column | Type | Nullable | Default | Constraints | Description |
|--------|------|----------|---------|-------------|-------------|
| `Id` | `uuid` | NO | `gen_random_uuid()` | PK | Unique identifier |
| `PatientId` | `uuid` | NO | - | FK | Reference to patient |
| `DoctorId` | `uuid` | NO | - | FK | Reference to doctor |
| `AppointmentDate` | `date` | NO | - | - | Scheduled date |
| `StartTime` | `time` | NO | - | - | Start time |
| `EndTime` | `time` | NO | - | - | End time |
| `Status` | `smallint` | NO | `0` | - | Enum: 0=Scheduled, 1=Confirmed, 2=Completed, 3=Cancelled |
| `Notes` | `varchar(1000)` | YES | - | - | Appointment notes |
| `CreationTime` | `timestamp` | NO | `now()` | - | ABP audit |
| `CreatorId` | `uuid` | YES | - | - | ABP audit |
| `LastModificationTime` | `timestamp` | YES | - | - | ABP audit |
| `LastModifierId` | `uuid` | YES | - | - | ABP audit |
| `IsDeleted` | `boolean` | NO | `false` | - | ABP soft delete |
| `DeleterId` | `uuid` | YES | - | - | ABP audit |
| `DeletionTime` | `timestamp` | YES | - | - | ABP audit |

### Indexes

| Name | Columns | Type | Purpose |
|------|---------|------|---------|
| `PK_Appointments` | `Id` | Primary | Primary key |
| `IX_Appointments_PatientId` | `PatientId` | B-tree | Patient appointments |
| `IX_Appointments_DoctorId` | `DoctorId` | B-tree | Doctor schedule |
| `IX_Appointments_DateTime` | `DoctorId`, `AppointmentDate`, `StartTime` | Unique (partial) | Prevent double booking |
| `IX_Appointments_Status` | `Status` | B-tree | Status filtering |

### Relationships

| Relationship | Type | Target | FK Column | On Delete |
|--------------|------|--------|-----------|-----------|
| Patient | N:1 | `Patients` | `PatientId` | RESTRICT |
| Doctor | N:1 | `Doctors` | `DoctorId` | RESTRICT |

### EF Core Configuration

```csharp
public class AppointmentConfiguration : IEntityTypeConfiguration<Appointment>
{
    public void Configure(EntityTypeBuilder<Appointment> builder)
    {
        builder.ToTable("Appointments");

        builder.HasKey(x => x.Id);

        builder.Property(x => x.Notes)
            .HasMaxLength(AppointmentConsts.MaxNotesLength);

        builder.HasOne<Patient>()
            .WithMany()
            .HasForeignKey(x => x.PatientId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasOne<Doctor>()
            .WithMany()
            .HasForeignKey(x => x.DoctorId)
            .OnDelete(DeleteBehavior.Restrict);

        // Prevent double booking
        builder.HasIndex(x => new { x.DoctorId, x.AppointmentDate, x.StartTime })
            .IsUnique()
            .HasFilter("\"IsDeleted\" = false AND \"Status\" != 3");

        builder.HasQueryFilter(x => !x.IsDeleted);
    }
}
```

---

## Index Strategy Guidelines

| Query Pattern | Index Type | Example |
|---------------|------------|---------|
| Exact match | B-tree | `WHERE email = 'x'` |
| Range query | B-tree | `WHERE date BETWEEN x AND y` |
| Soft delete filter | Partial | `WHERE IsDeleted = false` |
| Multiple columns | Composite | `WHERE a = x AND b = y` |
| Uniqueness | Unique | Email, combinations |
| Full-text search | GIN | `WHERE name ILIKE '%x%'` |
