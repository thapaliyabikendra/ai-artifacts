# User Story Examples

Real-world examples of well-written user stories with acceptance criteria.

## CRUD Operations

### Create Entity

```markdown
**US-001: Create New Patient Record**

As a Receptionist,
I want to create a new patient record with their personal information,
So that the patient can be registered in the system for appointments.

**Acceptance Criteria:**
- [ ] Given I am logged in as Receptionist, when I navigate to Patients and click "Add New", then I see a patient creation form
- [ ] Given I fill in all required fields (Name, Email, Phone, DOB), when I click Save, then the patient is created and I see a success message
- [ ] Given I submit a form with an existing email, when the system validates, then I see "Email already exists" error
- [ ] Given I submit a form with invalid email format, when the system validates, then I see "Invalid email format" error
- [ ] Given I leave required fields empty, when I click Save, then I see validation errors for each missing field

**Priority**: Must Have
**Effort**: M
**Dependencies**: None
```

### Read/List Entity

```markdown
**US-002: View Patient List**

As a Receptionist,
I want to view a paginated list of all patients,
So that I can find and manage patient records efficiently.

**Acceptance Criteria:**
- [ ] Given I am logged in as Receptionist, when I navigate to Patients, then I see a paginated list (20 per page)
- [ ] Given I am on the patient list, when I type in the search box, then the list filters by name or email
- [ ] Given I am on the patient list, when I click a column header, then the list sorts by that column
- [ ] Given there are more than 20 patients, when I click Next, then I see the next page of results
- [ ] Given I am a Doctor, when I navigate to Patients, then I only see patients assigned to me

**Priority**: Must Have
**Effort**: M
**Dependencies**: US-001
```

### Update Entity

```markdown
**US-003: Update Patient Information**

As a Receptionist,
I want to update an existing patient's information,
So that patient records remain accurate and current.

**Acceptance Criteria:**
- [ ] Given I am viewing a patient's details, when I click "Edit", then I see an editable form with current values
- [ ] Given I modify fields and click Save, when validation passes, then changes are saved and I see a success message
- [ ] Given I try to change email to one that exists, when I save, then I see "Email already exists" error
- [ ] Given I am a Doctor, when I try to edit a patient, then I cannot modify sensitive fields (email, phone)
- [ ] Given changes were made, when I view the patient again, then I see the audit trail showing who modified and when

**Priority**: Must Have
**Effort**: S
**Dependencies**: US-001, US-002
```

### Delete Entity

```markdown
**US-004: Delete Patient Record**

As an Admin,
I want to delete a patient record,
So that I can remove patients who are no longer active or were created in error.

**Acceptance Criteria:**
- [ ] Given I am an Admin viewing a patient, when I click "Delete", then I see a confirmation dialog
- [ ] Given I confirm deletion, when the system processes, then the patient is soft-deleted and no longer appears in lists
- [ ] Given I am a Receptionist, when I try to delete a patient, then I see "Permission denied" error
- [ ] Given a patient has upcoming appointments, when I try to delete, then I see "Cannot delete patient with appointments" error
- [ ] Given a patient is deleted, when I search for them, then they do not appear (unless I filter for deleted records)

**Priority**: Should Have
**Effort**: S
**Dependencies**: US-001, US-002
```

## Complex Business Logic

### Appointment Scheduling

```markdown
**US-010: Schedule Patient Appointment**

As a Receptionist,
I want to schedule an appointment for a patient with a doctor,
So that patients can receive medical consultations at scheduled times.

**Acceptance Criteria:**
- [ ] Given I am scheduling an appointment, when I select a doctor, then I see only their available time slots
- [ ] Given I select a date and time within doctor's schedule, when I save, then the appointment is created
- [ ] Given I select a time slot that is already booked, when I try to save, then I see "Time slot not available" error
- [ ] Given I select a time outside doctor's working hours, when I try to save, then I see "Doctor not available at this time" error
- [ ] Given the appointment is created, when I view it, then both patient and doctor can see it in their schedules
- [ ] Given the appointment is created, when 24 hours remain, then an email reminder is sent to the patient

**Priority**: Must Have
**Effort**: L
**Dependencies**: US-001, Doctor Management feature

**Business Rules:**
- BR-010: Appointments must be within doctor's schedule
- BR-011: No double-booking for same doctor at same time
- BR-012: Appointment duration is 30 minutes by default
```

### Authorization Scenario

```markdown
**US-020: Role-Based Patient Access**

As a System Administrator,
I want doctors to only access their assigned patients,
So that patient confidentiality is maintained per HIPAA requirements.

**Acceptance Criteria:**
- [ ] Given I am a Doctor, when I view the patient list, then I only see patients I have treated
- [ ] Given I am a Doctor, when I try to access another doctor's patient by URL, then I see "Access Denied"
- [ ] Given I am an Admin, when I view the patient list, then I see all patients regardless of assignment
- [ ] Given I am a Receptionist, when I view the patient list, then I see all patients (for scheduling purposes)
- [ ] Given unauthorized access is attempted, when the system blocks it, then the attempt is logged for audit

**Priority**: Must Have
**Effort**: M
**Dependencies**: Role management, Audit logging

**Business Rules:**
- BR-020: Doctors can only view/edit patients they have appointments with
- BR-021: Receptionists can view all patients but not medical records
- BR-022: Admins have full access to all patient data
```

## Reporting

```markdown
**US-030: Generate Appointment Report**

As a Clinic Manager,
I want to generate a report of appointments by date range,
So that I can analyze clinic utilization and doctor workload.

**Acceptance Criteria:**
- [ ] Given I am a Manager, when I access Reports, then I see "Appointment Report" option
- [ ] Given I select a date range and click Generate, when processing completes, then I see a tabular report
- [ ] Given the report is displayed, when I click Export, then I can download as Excel or PDF
- [ ] Given I filter by doctor, when I generate the report, then I see only that doctor's appointments
- [ ] Given the date range exceeds 1 year, when I try to generate, then I see "Please select a shorter range" warning

**Priority**: Should Have
**Effort**: M
**Dependencies**: Appointment data, Export functionality
```

## Integration

```markdown
**US-040: Send Appointment Reminders via Email**

As a Clinic,
I want automated email reminders sent 24 hours before appointments,
So that patients are reminded and no-show rates decrease.

**Acceptance Criteria:**
- [ ] Given an appointment exists, when 24 hours remain until the appointment, then an email is sent to the patient
- [ ] Given the email is sent, when the patient receives it, then it contains appointment date, time, doctor name, and clinic address
- [ ] Given the email service is unavailable, when sending fails, then the system retries 3 times with exponential backoff
- [ ] Given all retries fail, when the system gives up, then an alert is sent to the admin and logged
- [ ] Given a patient has no email, when reminder time comes, then no email is sent and this is logged

**Priority**: Could Have
**Effort**: M
**Dependencies**: Email service integration, Background job infrastructure
```
