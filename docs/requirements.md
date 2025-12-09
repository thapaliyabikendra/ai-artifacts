# Clinic Management System --- Business Requirements

## 1. Overview

A small local clinic needs a lightweight system to manage **patients**,
**appointments**, and **doctor schedules**. The system should expose a
**RESTful Web API** secured with **JWT authentication** using **ASP.NET
Identity**.

The system will be used by: - **Admin** (full control) - **Doctor**
(view own appointments & patients) - **Receptionist** (create patients &
schedule appointments)

## 2. Core Functional Requirements

### 2.1 User Accounts & Authentication

-   Register, login, receive JWT token
-   Roles:
    -   Admin
    -   Doctor
    -   Receptionist
-   Admin:
    -   Create users
    -   Assign roles

### 3. Domain Entities

#### 3.1 Patient

-   Id (int)
-   FirstName
-   LastName
-   Email
-   Phone
-   DateOfBirth
-   CreatedAt

#### 3.2 Doctor

-   Id (int)
-   FullName
-   Specialization
-   Email
-   Phone

#### 3.3 Appointment

-   Id (int)
-   PatientId (FK)
-   DoctorId (FK)
-   AppointmentDate
-   Description
-   Status (Scheduled, Completed, Cancelled)
-   CreatedAt

#### 3.4 DoctorSchedule

-   Id (int)
-   DoctorId (FK)
-   DayOfWeek
-   StartTime
-   EndTime

## 4. Use Cases

### 4.1 Patient Management

-   Create, update, list, view, soft-delete patients

### 4.2 Doctor Management

-   Admin: add, edit, delete, view doctors

### 4.3 Appointment Management

-   Receptionist: create, reschedule, cancel appointments
-   Doctor: view own appointments, mark completed
-   Admin: view all appointments

### 4.4 Doctor Schedule Management

-   Admin defines doctor weekly availability
-   Receptionist views availability when scheduling

## 5. Non-Functional Requirements

-   RESTful API (ASP.NET Core Web API)
-   Repository Pattern + Unit of Work
-   EF Core (async operations)
-   DTOs for all requests/responses
-   JWT + ASP.NET Identity authentication
-   Role-based authorization
-   Validation via Data Annotations or FluentValidation
-   SQL Server with EF Core Migrations

## 6. Optional Extensions

-   Paging & filtering
-   Audit logs
-   Email reminders
-   Swagger documentation
-   Global exception handling middleware

