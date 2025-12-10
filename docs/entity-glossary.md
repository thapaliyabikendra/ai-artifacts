# Entity Glossary

> **Purpose**: Central reference for all domain entities, user roles, and permission structures.
> **Usage**: Agents should read this file for project-specific domain context.
> **Last Updated**: 2025-12-11

---

## Domain Entities

### Patient
Primary entity representing clinic patients.

| Property | Type | Constraints | Description |
|----------|------|-------------|-------------|
| Id | Guid | PK | Unique identifier |
| FirstName | string | Required, max 100 | Patient's first name |
| LastName | string | Required, max 100 | Patient's last name |
| Email | string | Required, unique, max 255 | Contact email |
| Phone | string? | Optional, max 20 | Contact phone number |
| DateOfBirth | DateTime | Required, past date | Birth date |

**Business Rules**:
- Email must be unique across all patients
- DateOfBirth cannot be a future date
- Soft delete enabled (IsDeleted flag)

---

### Doctor
Entity representing medical staff who provide services.

| Property | Type | Constraints | Description |
|----------|------|-------------|-------------|
| Id | Guid | PK | Unique identifier |
| FullName | string | Required, max 200 | Doctor's full name |
| Specialization | string | Required, max 100 | Medical specialty |
| Email | string | Required, unique | Contact email |
| Phone | string? | Optional | Contact phone |
| UserId | Guid? | Optional, FK | Linked system user |

**Business Rules**:
- Doctors can be linked to system users for self-service
- Specialization should be from a predefined list (future enhancement)

---

### Appointment
Entity representing scheduled patient-doctor meetings.

| Property | Type | Constraints | Description |
|----------|------|-------------|-------------|
| Id | Guid | PK | Unique identifier |
| PatientId | Guid | Required, FK | Reference to Patient |
| DoctorId | Guid | Required, FK | Reference to Doctor |
| AppointmentDate | DateTime | Required, future | Scheduled date/time |
| Description | string? | Optional, max 500 | Reason for visit |
| Status | AppointmentStatus | Required | Current status |

**Status Values**:
- `Scheduled` - Confirmed appointment
- `Completed` - Visit completed
- `Cancelled` - Appointment cancelled
- `NoShow` - Patient did not attend

**Business Rules**:
- No overlapping appointments for the same doctor
- Must fall within doctor's weekly schedule
- Cannot book on days doctor is unavailable
- Only future dates allowed for new appointments

---

### DoctorSchedule
Entity defining weekly availability patterns for doctors.

| Property | Type | Constraints | Description |
|----------|------|-------------|-------------|
| Id | Guid | PK | Unique identifier |
| DoctorId | Guid | Required, FK | Reference to Doctor |
| DayOfWeek | DayOfWeek | Required | Day (0=Sunday to 6=Saturday) |
| StartTime | TimeSpan | Required | Shift start time |
| EndTime | TimeSpan | Required | Shift end time |

**Business Rules**:
- EndTime must be greater than StartTime
- No overlapping schedules for same doctor on same day
- Multiple shifts per day allowed (e.g., morning and afternoon)

---

## User Roles

### Admin
Full system access and administrative control.

**Capabilities**:
- Manage all users and roles
- CRUD operations on all entities
- View all appointments across the clinic
- Manage doctor profiles and schedules
- Access system reports and audit logs

---

### Doctor
Limited access focused on personal schedule and assigned patients.

**Capabilities**:
- View own appointments only
- View patients assigned via appointments
- Update appointment status (mark completed)
- View own schedule

**Restrictions**:
- Cannot view other doctors' appointments
- Cannot modify patient records
- Cannot manage schedules

---

### Receptionist
Front-desk operations focused on patient and appointment management.

**Capabilities**:
- Full CRUD on patient records
- Create, reschedule, cancel appointments
- View all doctor schedules (read-only)
- Search patients and appointments

**Restrictions**:
- Cannot modify doctor profiles
- Cannot modify doctor schedules
- Cannot access system administration

---

## Permission Structure

```
{ProjectName}.{Resource}.{Action}
```

### Patient Permissions
| Permission | Description | Roles |
|------------|-------------|-------|
| `Clinic.Patients` | View patients | Admin, Receptionist |
| `Clinic.Patients.Create` | Create patients | Admin, Receptionist |
| `Clinic.Patients.Edit` | Update patients | Admin, Receptionist |
| `Clinic.Patients.Delete` | Soft delete patients | Admin, Receptionist |

### Appointment Permissions
| Permission | Description | Roles |
|------------|-------------|-------|
| `Clinic.Appointments` | View all appointments | Admin |
| `Clinic.Appointments.ViewOwn` | View own appointments | Doctor |
| `Clinic.Appointments.Create` | Create appointments | Admin, Receptionist |
| `Clinic.Appointments.Edit` | Reschedule appointments | Admin, Receptionist |
| `Clinic.Appointments.Cancel` | Cancel appointments | Admin, Receptionist |
| `Clinic.Appointments.MarkCompleted` | Mark as completed | Admin, Doctor |

### Doctor Permissions
| Permission | Description | Roles |
|------------|-------------|-------|
| `Clinic.Doctors` | View doctors | Admin, Receptionist |
| `Clinic.Doctors.Create` | Add doctors | Admin |
| `Clinic.Doctors.Edit` | Update doctors | Admin |
| `Clinic.Doctors.Delete` | Remove doctors | Admin |
| `Clinic.Doctors.ManageSchedule` | Manage schedules | Admin |

### Schedule Permissions
| Permission | Description | Roles |
|------------|-------------|-------|
| `Clinic.Schedules` | View schedules | Admin, Doctor, Receptionist |
| `Clinic.Schedules.Manage` | Create/edit schedules | Admin |

---

## Enumerations

### AppointmentStatus
```csharp
public enum AppointmentStatus
{
    Scheduled = 0,
    Completed = 1,
    Cancelled = 2,
    NoShow = 3
}
```

### DayOfWeek (System)
```csharp
// System.DayOfWeek
Sunday = 0,
Monday = 1,
Tuesday = 2,
Wednesday = 3,
Thursday = 4,
Friday = 5,
Saturday = 6
```

---

## Entity Relationships

```
Patient 1 ←──────── N Appointment
                           │
Doctor  1 ←──────── N ─────┘
   │
   1
   │
   N
   │
DoctorSchedule
```

- **Patient** has many **Appointments**
- **Doctor** has many **Appointments**
- **Doctor** has many **DoctorSchedules** (one per weekday)
- **Appointment** belongs to one **Patient** and one **Doctor**

---

## API Endpoints Reference

### Patients
| Method | Endpoint | Permission |
|--------|----------|------------|
| GET | `/api/app/patients` | Clinic.Patients |
| GET | `/api/app/patients/{id}` | Clinic.Patients |
| POST | `/api/app/patients` | Clinic.Patients.Create |
| PUT | `/api/app/patients/{id}` | Clinic.Patients.Edit |
| DELETE | `/api/app/patients/{id}` | Clinic.Patients.Delete |

### Doctors
| Method | Endpoint | Permission |
|--------|----------|------------|
| GET | `/api/app/doctors` | Clinic.Doctors |
| GET | `/api/app/doctors/{id}` | Clinic.Doctors |
| POST | `/api/app/doctors` | Clinic.Doctors.Create |
| PUT | `/api/app/doctors/{id}` | Clinic.Doctors.Edit |
| DELETE | `/api/app/doctors/{id}` | Clinic.Doctors.Delete |

### Appointments
| Method | Endpoint | Permission |
|--------|----------|------------|
| GET | `/api/app/appointments` | Clinic.Appointments |
| GET | `/api/app/appointments/my` | Clinic.Appointments.ViewOwn |
| POST | `/api/app/appointments` | Clinic.Appointments.Create |
| PUT | `/api/app/appointments/{id}/reschedule` | Clinic.Appointments.Edit |
| PUT | `/api/app/appointments/{id}/cancel` | Clinic.Appointments.Cancel |
| PUT | `/api/app/appointments/{id}/complete` | Clinic.Appointments.MarkCompleted |

### Doctor Schedules
| Method | Endpoint | Permission |
|--------|----------|------------|
| GET | `/api/app/doctor-schedules` | Clinic.Schedules |
| GET | `/api/app/doctor-schedules/doctor/{doctorId}` | Clinic.Schedules |
| POST | `/api/app/doctor-schedules` | Clinic.Schedules.Manage |
| PUT | `/api/app/doctor-schedules/{id}` | Clinic.Schedules.Manage |
| DELETE | `/api/app/doctor-schedules/{id}` | Clinic.Schedules.Manage |
