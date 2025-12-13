# Entity Definition Examples

Real-world examples of well-structured entity definitions.

## Patient Entity

> **Aggregate Root**: Yes
> **Base Class**: `FullAuditedAggregateRoot<Guid>`
> **Table**: `Patients`

### Description

Represents a patient registered in the clinic management system. Central entity for appointments and medical records.

### Properties

| Property | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| `Id` | `Guid` | Yes | PK | Unique identifier |
| `FirstName` | `string` | Yes | MaxLength(50) | Patient first name |
| `LastName` | `string` | Yes | MaxLength(50) | Patient last name |
| `Email` | `string` | Yes | Email format, Unique, MaxLength(255) | Contact email |
| `PhoneNumber` | `string` | No | Phone format, MaxLength(20) | Contact phone |
| `DateOfBirth` | `DateTime` | Yes | Must be past date | Birth date |
| `Gender` | `Gender` | Yes | Enum | Male, Female, Other |
| `Address` | `string` | No | MaxLength(500) | Full address |
| `IsActive` | `bool` | Yes | Default: true | Active status |

### Relationships

| Relationship | Type | Target Entity | FK Column | Description |
|--------------|------|---------------|-----------|-------------|
| Appointments | 1:N | `Appointment` | - | Patient's appointments |
| MedicalRecords | 1:N | `MedicalRecord` | - | Patient's medical history |

### Business Rules

| Rule ID | Rule | Validation Point |
|---------|------|------------------|
| BR-PAT-001 | Email must be unique | Create, Update |
| BR-PAT-002 | Date of birth must be in the past | Create, Update |
| BR-PAT-003 | Cannot delete patient with future appointments | Delete |

### API Access

| Operation | Permission | Roles |
|-----------|------------|-------|
| List | `CMS.Patients` | Admin, Receptionist, Doctor |
| View | `CMS.Patients` | Admin, Receptionist, Doctor |
| Create | `CMS.Patients.Create` | Admin, Receptionist |
| Update | `CMS.Patients.Edit` | Admin, Receptionist |
| Delete | `CMS.Patients.Delete` | Admin |

### Sample Data

| Id | FirstName | LastName | Email | IsActive |
|----|-----------|----------|-------|----------|
| `{guid-1}` | John | Doe | john.doe@example.com | true |
| `{guid-2}` | Jane | Smith | jane.smith@example.com | true |

---

## Appointment Entity

> **Aggregate Root**: Yes
> **Base Class**: `FullAuditedAggregateRoot<Guid>`
> **Table**: `Appointments`

### Description

Represents a scheduled appointment between a patient and doctor at a specific date and time.

### Properties

| Property | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| `Id` | `Guid` | Yes | PK | Unique identifier |
| `PatientId` | `Guid` | Yes | FK | Reference to patient |
| `DoctorId` | `Guid` | Yes | FK | Reference to doctor |
| `AppointmentDate` | `DateTime` | Yes | Must be future | Scheduled date |
| `StartTime` | `TimeSpan` | Yes | - | Start time |
| `EndTime` | `TimeSpan` | Yes | > StartTime | End time |
| `Status` | `AppointmentStatus` | Yes | Enum | Current status |
| `Notes` | `string` | No | MaxLength(1000) | Additional notes |

### State Transitions

```
[Scheduled] → [Confirmed] → [Completed]
     ↓            ↓
[Cancelled]  [Cancelled]
```

### Relationships

| Relationship | Type | Target Entity | FK Column | Description |
|--------------|------|---------------|-----------|-------------|
| Patient | N:1 | `Patient` | `PatientId` | Appointment patient |
| Doctor | N:1 | `Doctor` | `DoctorId` | Assigned doctor |

### Business Rules

| Rule ID | Rule | Validation Point |
|---------|------|------------------|
| BR-APT-001 | Appointments cannot overlap for same doctor | Create |
| BR-APT-002 | Appointments must be within doctor schedule | Create |
| BR-APT-003 | Cannot schedule in the past | Create |
| BR-APT-004 | Only Scheduled/Confirmed can be cancelled | Update |
| BR-APT-005 | Duration must be 15-120 minutes | Create |

### API Access

| Operation | Permission | Roles |
|-----------|------------|-------|
| List | `CMS.Appointments` | Admin, Receptionist, Doctor |
| View | `CMS.Appointments` | Admin, Receptionist, Doctor |
| Create | `CMS.Appointments.Create` | Admin, Receptionist |
| Update | `CMS.Appointments.Edit` | Admin, Receptionist |
| Delete | `CMS.Appointments.Delete` | Admin |
| Confirm | `CMS.Appointments.Edit` | Admin, Receptionist |
| Complete | `CMS.Appointments.Edit` | Doctor |

---

## Doctor Entity

> **Aggregate Root**: Yes
> **Base Class**: `FullAuditedAggregateRoot<Guid>`
> **Table**: `Doctors`

### Description

Represents a medical professional who can receive appointments and access patient records.

### Properties

| Property | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| `Id` | `Guid` | Yes | PK | Unique identifier |
| `UserId` | `Guid` | Yes | FK, Unique | Link to identity user |
| `Specialty` | `string` | Yes | MaxLength(100) | Medical specialty |
| `LicenseNumber` | `string` | Yes | Unique, MaxLength(50) | Medical license |
| `IsAvailable` | `bool` | Yes | Default: true | Accepting appointments |

### Relationships

| Relationship | Type | Target Entity | FK Column | Description |
|--------------|------|---------------|-----------|-------------|
| User | 1:1 | `IdentityUser` | `UserId` | Identity link |
| Appointments | 1:N | `Appointment` | - | Doctor's appointments |
| Schedules | 1:N | `DoctorSchedule` | - | Working hours |

### Business Rules

| Rule ID | Rule | Validation Point |
|---------|------|------------------|
| BR-DOC-001 | License number must be unique | Create, Update |
| BR-DOC-002 | Cannot delete doctor with future appointments | Delete |
| BR-DOC-003 | User can only be linked to one doctor | Create |
