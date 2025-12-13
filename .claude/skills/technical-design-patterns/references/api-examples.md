# API Contract Examples

Real-world examples of API contracts for ABP Framework applications.

## Patient Management API

### Overview

| Attribute | Value |
|-----------|-------|
| Base Path | `/api/app/patients` |
| Authentication | Required |
| Rate Limit | 100/min |

### Endpoints

| Method | Path | Description | Permission | Request | Response |
|--------|------|-------------|------------|---------|----------|
| GET | `/patients` | List with pagination | `CMS.Patients` | `GetPatientsInput` | `PagedResultDto<PatientDto>` |
| GET | `/patients/{id}` | Get by ID | `CMS.Patients` | - | `PatientDto` |
| POST | `/patients` | Create new | `CMS.Patients.Create` | `CreatePatientDto` | `PatientDto` |
| PUT | `/patients/{id}` | Update existing | `CMS.Patients.Edit` | `UpdatePatientDto` | `PatientDto` |
| DELETE | `/patients/{id}` | Soft delete | `CMS.Patients.Delete` | - | `204` |

### DTOs

#### PatientDto (Output)

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "phoneNumber": "+1234567890",
  "dateOfBirth": "1985-03-15",
  "gender": 0,
  "address": "123 Main St, City",
  "isActive": true,
  "creationTime": "2024-01-15T10:30:00Z",
  "lastModificationTime": "2024-01-20T14:45:00Z"
}
```

#### CreatePatientDto (Input)

```json
{
  "firstName": "string (required, max 50)",
  "lastName": "string (required, max 50)",
  "email": "string (required, email format, max 255)",
  "phoneNumber": "string (optional, phone format, max 20)",
  "dateOfBirth": "date (required, must be past)",
  "gender": "number (required, enum: 0=Male, 1=Female, 2=Other)",
  "address": "string (optional, max 500)"
}
```

#### GetPatientsInput (Query)

```json
{
  "filter": "string (optional, searches firstName, lastName, email)",
  "isActive": "boolean (optional)",
  "sorting": "string (optional, e.g., 'lastName asc, firstName asc')",
  "skipCount": "number (default 0)",
  "maxResultCount": "number (default 10, max 100)"
}
```

---

## Appointment API

### Overview

| Attribute | Value |
|-----------|-------|
| Base Path | `/api/app/appointments` |
| Authentication | Required |
| Rate Limit | 50/min |

### Endpoints

| Method | Path | Description | Permission | Request | Response |
|--------|------|-------------|------------|---------|----------|
| GET | `/appointments` | List with filters | `CMS.Appointments` | `GetAppointmentsInput` | `PagedResultDto<AppointmentDto>` |
| GET | `/appointments/{id}` | Get by ID | `CMS.Appointments` | - | `AppointmentDto` |
| POST | `/appointments` | Schedule new | `CMS.Appointments.Create` | `CreateAppointmentDto` | `AppointmentDto` |
| PUT | `/appointments/{id}` | Reschedule | `CMS.Appointments.Edit` | `UpdateAppointmentDto` | `AppointmentDto` |
| DELETE | `/appointments/{id}` | Cancel | `CMS.Appointments.Delete` | - | `204` |
| POST | `/appointments/{id}/confirm` | Confirm | `CMS.Appointments.Edit` | - | `AppointmentDto` |
| POST | `/appointments/{id}/complete` | Mark complete | `CMS.Appointments.Edit` | - | `AppointmentDto` |

### DTOs

#### AppointmentDto (Output)

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "patientId": "...",
  "patientName": "John Doe",
  "doctorId": "...",
  "doctorName": "Dr. Smith",
  "appointmentDate": "2024-02-15",
  "startTime": "09:00:00",
  "endTime": "09:30:00",
  "status": 1,
  "statusName": "Confirmed",
  "notes": "Regular checkup",
  "creationTime": "2024-01-15T10:30:00Z"
}
```

#### CreateAppointmentDto (Input)

```json
{
  "patientId": "guid (required)",
  "doctorId": "guid (required)",
  "appointmentDate": "date (required, must be future)",
  "startTime": "time (required)",
  "notes": "string (optional, max 1000)"
}
```

---

## Error Response Format

All APIs return consistent error responses:

```json
{
  "error": {
    "code": "CMS:010001",
    "message": "Patient with this email already exists.",
    "details": "Email: john.doe@example.com",
    "validationErrors": [
      {
        "message": "Email must be unique",
        "members": ["email"]
      }
    ]
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `CMS:010001` | 400 | Validation error |
| `CMS:010002` | 404 | Entity not found |
| `CMS:010003` | 403 | Permission denied |
| `CMS:010004` | 409 | Business rule violation |
