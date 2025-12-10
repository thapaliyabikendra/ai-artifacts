# **Business Requirements**

## **1. System Overview**

The **Clinic Management System (CMS)** is a web-based application that provides administrative, scheduling, and patient-management functionality for a small clinic. The system exposes a **secure REST API** and supports multiple **role-based user types** with specific access permissions. Core domains include:

* **Patient Management**
* **Doctor Management**
* **Doctor Weekly Schedule Management**
* **Appointment Management**

---

## **2. Objectives**

The CMS aims to:

1. Digitize and streamline clinic workflow.
2. Reduce scheduling conflicts and improve staff productivity.
3. Provide accurate patient and doctor information.
4. Enforce consistent appointment rules and doctor availability.
5. Provide role-specific access to system operations.

---

## **3. User Roles and Permissions**

### **3.1 Admin**

* Full system access.
* Manages users and roles.
* Manages doctor profiles.
* Manages doctor weekly schedules.
* Views all appointments across the clinic.

### **3.2 Doctor**

* Views **only their own** appointments.
* Views **only their own** assigned patients.
* Updates appointment status (e.g., mark as “Completed”).

### **3.3 Receptionist**

* Manages patient records.
* Creates, reschedules, and cancels appointments.
* Views doctor availability for scheduling.
* Cannot modify doctor profiles or doctor weekly schedules.

---

## **4. Functional Requirements**

### **4.1 Patient Management**

The system must allow:

1. **Create Patient**

   * Input: personal details (e.g., name, DOB, gender, contact info).
2. **Update Patient**
3. **List/Search Patients**
4. **View Patient Profile**
5. **Soft Delete Patient**

   * Patient remains in database but hidden from standard lists.

**Role Access:** Receptionist, Admin.

---

### **4.2 Doctor Management**

The system must allow:

1. **Add New Doctor Profile**
2. **Update Doctor Profile**
3. **List/Search Doctors**
4. **Deactivate/Delete Doctor**

   * Only Admin can deactivate or delete.

**Role Access:** Admin.

---

### **4.3 Appointment Management**

#### **Actions by Receptionist**

* Create appointment.
* Reschedule appointment.
* Cancel appointment.

#### **Actions by Doctor**

* View daily appointments.
* View upcoming appointments.
* Mark appointment as completed.

#### **Actions by Admin**

* View all appointments for the entire clinic.

#### **Business Rules**

1. **No Overlapping Appointments**

   * A doctor cannot have two appointments that overlap.
2. **Respect Doctor Availability**

   * Appointments must fall within the doctor’s weekly schedule.
3. **Block Unavailable Days**

   * System must prevent appointment creation on days the doctor is unavailable.
4. **Appointment Statuses**

   * Example: *Scheduled*, *Completed*, *Cancelled*.

---

### **4.4 Doctor Weekly Schedule Management**

**Admin** defines recurring weekly availability:

* Available days of the week.
* Start/end working hours per day.
* Break periods (optional, if needed for later expansion).

**Receptionist**:

* Can view the schedule but cannot edit it.
* Scheduling UI/API must show real-time availability.

**System Enforcement**:

* Appointment creation must validate against weekly rules.

---

## **5. Non-Functional Requirements**

### **5.1 Security**

* JWT-based authentication.
* Role-based authorization.
* Each API endpoint must enforce role permissions.
* Sensitive operations require authentication tokens.

### **5.2 API Requirements**

* RESTful design principles.
* Consistent request and response DTOs.
* Unified error handling structure including:

  * error code
  * message
  * validation details (if any)
* API documentation available via Swagger/OpenAPI.

### **5.3 Performance**

* Support pagination for lists (patients, doctors, appointments).
* Support filtering and search queries.
* Response time should be fast for typical use-case volumes (clinic-scale operations).

### **5.4 Quality & Reliability**

* Input validation for all fields (server-side).
* Logging for:

  * Authentication events
  * Appointment changes
  * CRUD operations
* System should maintain data consistency at all times.

---

## **6. Optional Future Enhancements**

(Not required in current scope but helpful for future-proofing technical architecture.)

* Email reminders for upcoming appointments.
* SMS notifications.
* Audit log reporting dashboard.
* Export appointments to PDF/Excel.
* Multi-language UI support.
* Patient portal for self-scheduling (future consideration).
* Integration with billing or EMR systems.
