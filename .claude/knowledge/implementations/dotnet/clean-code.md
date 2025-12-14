---
implements_concepts:
  - concepts/clean-code/principles
  - concepts/clean-code/naming
  - concepts/clean-code/functions
language: csharp
framework: [dotnet, abp]
used_by_skills: [clean-code-dotnet, abp-code-reviewer]
---

# Clean Code in C#/.NET

C# implementations of clean code principles for ABP Framework applications.

## Naming {#naming}

### Use Intention-Revealing Names

```csharp
// ❌ Bad - What is d? What is 86400000?
var d = DateTime.Now;
var x = d.AddMilliseconds(86400000);

// ✅ Good - Clear intent
var currentTime = DateTime.Now;
var oneDayFromNow = currentTime.AddDays(1);
```

### Use Pronounceable Names

```csharp
// ❌ Bad - Unpronounceable
public class DtaRcrd102
{
    public DateTime GenYmDhms { get; set; }
    public DateTime ModYmDhms { get; set; }
}

// ✅ Good - Pronounceable
public class Customer
{
    public DateTime GenerationTimestamp { get; set; }
    public DateTime ModificationTimestamp { get; set; }
}
```

### Use Searchable Names

```csharp
// ❌ Bad - Magic numbers are not searchable
for (int i = 0; i < 7; i++)
{
    totalPay += hours[i] * 22;
}

// ✅ Good - Named constants are searchable
private const int DaysPerWeek = 7;
private const decimal HourlyRate = 22m;

for (int dayIndex = 0; dayIndex < DaysPerWeek; dayIndex++)
{
    totalPay += hours[dayIndex] * HourlyRate;
}
```

### Avoid Encodings

```csharp
// ❌ Bad - Hungarian notation
public class Patient
{
    private string m_sName;
    private int m_iAge;
    private IPatientRepository _patientRepository;
}

// ✅ Good - No encoding needed
public class Patient
{
    private string _name;
    private int _age;
    private IPatientRepository _patientRepository;  // I prefix for interfaces is C# convention
}
```

### Class Names Should Be Nouns

```csharp
// ❌ Bad - Verb-based class names
public class ProcessPayment { }
public class ValidateOrder { }

// ✅ Good - Noun-based class names
public class PaymentProcessor { }
public class OrderValidator { }
```

### Method Names Should Be Verbs

```csharp
// ❌ Bad - Noun-based method names
public string CustomerName() { }
public void PaymentProcess() { }

// ✅ Good - Verb-based method names
public string GetCustomerName() { }
public void ProcessPayment() { }
```

### Pick One Word Per Concept

```csharp
// ❌ Bad - Inconsistent naming
public interface IPatientRepository
{
    Patient FetchPatient(Guid id);      // Fetch?
    Doctor GetDoctor(Guid id);           // Get?
    Appointment RetrieveAppointment(Guid id);  // Retrieve?
}

// ✅ Good - Consistent naming
public interface IPatientRepository
{
    Patient GetPatient(Guid id);
    Doctor GetDoctor(Guid id);
    Appointment GetAppointment(Guid id);
}
```

### Use Domain Names

```csharp
// ❌ Bad - Generic technical names
public class DataProcessor
{
    public void HandleItem(object item) { }
}

// ✅ Good - Domain-specific names
public class AppointmentScheduler
{
    public void ScheduleAppointment(Appointment appointment) { }
}
```

## Functions {#functions}

### Small Functions

```csharp
// ❌ Bad - Function does too much
public async Task<AppointmentDto> CreateAppointmentAsync(CreateAppointmentDto input)
{
    // Validate doctor exists
    var doctor = await _doctorRepository.GetAsync(input.DoctorId);
    if (doctor == null) throw new EntityNotFoundException(typeof(Doctor), input.DoctorId);

    // Validate patient exists
    var patient = await _patientRepository.GetAsync(input.PatientId);
    if (patient == null) throw new EntityNotFoundException(typeof(Patient), input.PatientId);

    // Check doctor availability
    var existingAppointments = await _appointmentRepository.GetListAsync(a =>
        a.DoctorId == input.DoctorId &&
        a.AppointmentTime >= input.AppointmentTime.AddMinutes(-30) &&
        a.AppointmentTime <= input.AppointmentTime.AddMinutes(30));
    if (existingAppointments.Any()) throw new BusinessException("Doctor not available");

    // Check patient doesn't have conflicting appointment
    var patientAppointments = await _appointmentRepository.GetListAsync(a =>
        a.PatientId == input.PatientId &&
        a.AppointmentTime.Date == input.AppointmentTime.Date);
    if (patientAppointments.Any()) throw new BusinessException("Patient already has appointment");

    // Create appointment
    var appointment = new Appointment(GuidGenerator.Create(), input.DoctorId, input.PatientId, input.AppointmentTime);
    await _appointmentRepository.InsertAsync(appointment);

    // Send notification
    await _notificationService.SendAsync(patient.Email, "Appointment Confirmed", $"Your appointment is scheduled for {input.AppointmentTime}");

    return ObjectMapper.Map<Appointment, AppointmentDto>(appointment);
}

// ✅ Good - Small, focused functions
public async Task<AppointmentDto> CreateAppointmentAsync(CreateAppointmentDto input)
{
    var doctor = await GetDoctorOrThrowAsync(input.DoctorId);
    var patient = await GetPatientOrThrowAsync(input.PatientId);

    await EnsureDoctorAvailableAsync(doctor.Id, input.AppointmentTime);
    await EnsurePatientHasNoConflictAsync(patient.Id, input.AppointmentTime);

    var appointment = await CreateAndSaveAppointmentAsync(input);
    await NotifyPatientAsync(patient, appointment);

    return ObjectMapper.Map<Appointment, AppointmentDto>(appointment);
}

private async Task<Doctor> GetDoctorOrThrowAsync(Guid doctorId)
{
    return await _doctorRepository.GetAsync(doctorId)
        ?? throw new EntityNotFoundException(typeof(Doctor), doctorId);
}
```

### Single Level of Abstraction

```csharp
// ❌ Bad - Mixed abstraction levels
public async Task ProcessOrderAsync(Order order)
{
    // High-level: validate order
    await ValidateOrderAsync(order);

    // Low-level: database operations mixed in
    using var connection = new SqlConnection(_connectionString);
    await connection.OpenAsync();
    var command = new SqlCommand("UPDATE Inventory SET Quantity = Quantity - @qty", connection);

    // High-level again: send notification
    await _notificationService.NotifyAsync(order.CustomerId);
}

// ✅ Good - Consistent abstraction level
public async Task ProcessOrderAsync(Order order)
{
    await ValidateOrderAsync(order);
    await UpdateInventoryAsync(order);
    await NotifyCustomerAsync(order.CustomerId);
}
```

### Command Query Separation

```csharp
// ❌ Bad - Query that also modifies state
public Patient GetOrCreatePatient(string email)
{
    var patient = _patients.FirstOrDefault(p => p.Email == email);
    if (patient == null)
    {
        patient = new Patient { Email = email };
        _patients.Add(patient);  // Side effect!
    }
    return patient;
}

// ✅ Good - Separate query and command
public Patient? FindPatientByEmail(string email)
{
    return _patients.FirstOrDefault(p => p.Email == email);
}

public Patient CreatePatient(string email)
{
    var patient = new Patient { Email = email };
    _patients.Add(patient);
    return patient;
}

// Usage
var patient = FindPatientByEmail(email) ?? CreatePatient(email);
```

### Prefer Exceptions Over Error Codes

```csharp
// ❌ Bad - Error codes
public enum RegistrationResult { Success, InvalidEmail, EmailTaken, WeakPassword }

public RegistrationResult Register(string email, string password)
{
    if (!IsValidEmail(email)) return RegistrationResult.InvalidEmail;
    if (EmailExists(email)) return RegistrationResult.EmailTaken;
    if (!IsStrongPassword(password)) return RegistrationResult.WeakPassword;

    // ... register
    return RegistrationResult.Success;
}

// Caller must check
var result = Register(email, password);
if (result != RegistrationResult.Success)
{
    // Handle each case...
}

// ✅ Good - Exceptions with domain meaning
public void Register(string email, string password)
{
    if (!IsValidEmail(email))
        throw new InvalidEmailException(email);
    if (EmailExists(email))
        throw new EmailAlreadyRegisteredException(email);
    if (!IsStrongPassword(password))
        throw new WeakPasswordException();

    // ... register
}

// Caller - cleaner flow
try
{
    Register(email, password);
}
catch (RegistrationException ex)
{
    // Handle registration failures
}
```

### Don't Use Flag Arguments

```csharp
// ❌ Bad - Boolean flag changes behavior
public void SendEmail(string to, string subject, string body, bool isHtml)
{
    if (isHtml)
    {
        // Send HTML email
    }
    else
    {
        // Send plain text email
    }
}

// ✅ Good - Separate methods
public void SendHtmlEmail(string to, string subject, string htmlBody) { }
public void SendPlainTextEmail(string to, string subject, string textBody) { }

// Or use a type
public void SendEmail(string to, string subject, EmailContent content) { }

public abstract record EmailContent;
public record HtmlContent(string Html) : EmailContent;
public record PlainTextContent(string Text) : EmailContent;
```

## Comments {#comments}

### Good Comments

```csharp
// ✅ Legal comments
// Copyright (c) 2024 Clinic Management System. All rights reserved.

// ✅ Explanation of intent
// We use a binary search here because the list is always sorted
// and can contain millions of records
private int FindPatientIndex(List<Patient> patients, Guid id) { }

// ✅ Warning of consequences
// WARNING: This operation cannot be undone. All patient records
// including appointments and medical history will be permanently deleted.
public async Task PermanentlyDeletePatientAsync(Guid patientId) { }

// ✅ TODO comments (tracked in backlog)
// TODO: Replace with proper caching when Redis is available (#1234)
private Patient? _cachedPatient;
```

### Bad Comments (Remove These)

```csharp
// ❌ Redundant comment
// Gets the patient by id
public Patient GetPatient(Guid id) { }

// ❌ Noise comment
// Default constructor
public Patient() { }

// ❌ Journal comment (use git history)
// 2024-01-15: Added validation - John
// 2024-01-20: Fixed null check - Jane
// 2024-02-01: Refactored loop - Bob
public void Process() { }

// ❌ Commented-out code (delete it!)
public void Calculate()
{
    // var oldResult = OldCalculation();
    // if (oldResult > 0) { ... }
    var result = NewCalculation();
}

// ❌ Position markers
//////////////////////////
// PATIENT METHODS
//////////////////////////

// ❌ Attribution comment (use git blame)
// Added by John Smith on 2024-01-15
```

## Error Handling {#errors}

### Use Exceptions, Not Return Codes

```csharp
// ❌ Bad - Returning null or error codes
public Patient? GetPatient(Guid id)
{
    return _patients.FirstOrDefault(p => p.Id == id);  // Returns null if not found
}

// ✅ Good - Throw meaningful exception
public Patient GetPatient(Guid id)
{
    return _patients.FirstOrDefault(p => p.Id == id)
        ?? throw new EntityNotFoundException(typeof(Patient), id);
}

// Or provide both options
public Patient? FindPatient(Guid id)  // Returns null - caller expects it
public Patient GetPatient(Guid id)     // Throws if not found
```

### Don't Return Null for Collections

```csharp
// ❌ Bad - Returns null
public List<Appointment>? GetAppointments(Guid patientId)
{
    if (!PatientExists(patientId))
        return null;

    return _appointments.Where(a => a.PatientId == patientId).ToList();
}

// ✅ Good - Returns empty collection
public List<Appointment> GetAppointments(Guid patientId)
{
    return _appointments
        .Where(a => a.PatientId == patientId)
        .ToList();  // Returns empty list if none found
}
```

### Define Exception Classes for Domain Errors

```csharp
// ✅ Good - Domain-specific exceptions
public class PatientNotFoundException : EntityNotFoundException
{
    public PatientNotFoundException(Guid patientId)
        : base(typeof(Patient), patientId, $"Patient with ID {patientId} was not found.")
    {
    }
}

public class AppointmentConflictException : BusinessException
{
    public AppointmentConflictException(DateTime requestedTime, DateTime conflictingTime)
        : base(ClinicDomainErrorCodes.AppointmentConflict)
    {
        WithData("requestedTime", requestedTime);
        WithData("conflictingTime", conflictingTime);
    }
}
```

## Related Concepts

- [Clean Code Principles](../../concepts/clean-code/principles.md)
- [Naming Principles](../../concepts/clean-code/naming.md)
- [Function Principles](../../concepts/clean-code/functions.md)

## Sources

- Clean Code by Robert C. Martin
- Clean Code Cheatsheet V2.4 by Urs Enzler
