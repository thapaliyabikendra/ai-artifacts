---
implements_concepts:
  - concepts/testing/tdd-principles
  - concepts/testing/first
  - concepts/testing/test-smells
language: csharp
framework: [dotnet, xunit, abp]
used_by_skills: [xunit-testing-patterns, qa-engineer, tdd-cycle]
---

# TDD with xUnit in .NET

C# implementations of TDD principles using xUnit for ABP Framework applications.

## TDD Cycle {#tdd-cycle}

### Red - Write a Failing Test

```csharp
public class PatientAppServiceTests : ClinicApplicationTestBase
{
    private readonly IPatientAppService _patientAppService;

    public PatientAppServiceTests()
    {
        _patientAppService = GetRequiredService<IPatientAppService>();
    }

    [Fact]
    public async Task CreateAsync_Should_Create_Patient_With_Valid_Input()
    {
        // Arrange
        var input = new CreatePatientDto
        {
            Name = "John Doe",
            Email = "john.doe@example.com"
        };

        // Act
        var result = await _patientAppService.CreateAsync(input);

        // Assert
        result.ShouldNotBeNull();
        result.Id.ShouldNotBe(Guid.Empty);
        result.Name.ShouldBe("John Doe");
        result.Email.ShouldBe("john.doe@example.com");
    }
}
```

### Green - Write Minimal Code to Pass

```csharp
public class PatientAppService : ApplicationService, IPatientAppService
{
    private readonly IPatientRepository _patientRepository;

    public PatientAppService(IPatientRepository patientRepository)
    {
        _patientRepository = patientRepository;
    }

    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        var patient = new Patient(
            GuidGenerator.Create(),
            input.Name,
            input.Email
        );

        await _patientRepository.InsertAsync(patient);

        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }
}
```

### Refactor - Improve While Keeping Tests Green

```csharp
// After refactoring - extract validation, use domain events
public class PatientAppService : ApplicationService, IPatientAppService
{
    private readonly IPatientRepository _patientRepository;
    private readonly PatientManager _patientManager;

    public async Task<PatientDto> CreateAsync(CreatePatientDto input)
    {
        var patient = await _patientManager.CreateAsync(input.Name, input.Email);
        return ObjectMapper.Map<Patient, PatientDto>(patient);
    }
}
```

## FIRST Principles {#first}

### Fast - Tests Run Quickly

```csharp
// ❌ Bad - Slow test with real database
[Fact]
public async Task Should_Query_Real_Database()
{
    using var connection = new SqlConnection(_connectionString);
    await connection.OpenAsync();
    // ... actual database queries
}

// ✅ Good - Fast test with in-memory database
public class PatientAppServiceTests : ClinicApplicationTestBase
{
    // Uses SQLite in-memory database via ABP test infrastructure

    [Fact]
    public async Task GetAsync_Should_Return_Patient()
    {
        // Uses pre-seeded test data
        var result = await _patientAppService.GetAsync(TestData.PatientJohnId);

        result.ShouldNotBeNull();
        result.Name.ShouldBe("John Doe");
    }
}
```

### Isolated - Tests Don't Affect Each Other

```csharp
// ❌ Bad - Shared mutable state
public class PatientServiceTests
{
    private static Patient _sharedPatient;  // Shared state!

    [Fact]
    public void Test1_CreatePatient()
    {
        _sharedPatient = new Patient { Name = "John" };
    }

    [Fact]
    public void Test2_UsePatient()
    {
        var name = _sharedPatient.Name;  // Depends on Test1 running first!
    }
}

// ✅ Good - Each test is independent
public class PatientServiceTests : ClinicApplicationTestBase
{
    [Fact]
    public async Task CreateAsync_Should_Create_New_Patient()
    {
        // Arrange - create test data for THIS test
        var input = new CreatePatientDto { Name = "John" };

        // Act
        var result = await _patientAppService.CreateAsync(input);

        // Assert
        result.Name.ShouldBe("John");
    }

    [Fact]
    public async Task GetAsync_Should_Return_Seeded_Patient()
    {
        // Uses data seeded in test module - isolated per test
        var result = await _patientAppService.GetAsync(TestData.PatientJohnId);

        result.ShouldNotBeNull();
    }
}
```

### Repeatable - Same Result Every Time

```csharp
// ❌ Bad - Depends on current time
[Fact]
public void Should_Be_Schedulable_Today()
{
    var appointment = new Appointment(DateTime.Now.AddHours(1));  // Different each run!

    appointment.IsSchedulable.ShouldBeTrue();  // Might fail after 11 PM
}

// ✅ Good - Inject clock for deterministic tests
public class AppointmentTests
{
    [Fact]
    public void Should_Be_Schedulable_During_Business_Hours()
    {
        // Fixed time - always 10 AM on a Monday
        var testClock = new TestClock(new DateTime(2024, 1, 15, 10, 0, 0));
        var appointment = new Appointment(testClock.Now.AddHours(1));

        appointment.IsSchedulable(testClock).ShouldBeTrue();
    }

    [Fact]
    public void Should_Not_Be_Schedulable_On_Weekend()
    {
        // Fixed time - Saturday
        var testClock = new TestClock(new DateTime(2024, 1, 20, 10, 0, 0));  // Saturday
        var appointment = new Appointment(testClock.Now.AddHours(1));

        appointment.IsSchedulable(testClock).ShouldBeFalse();
    }
}
```

### Self-Validating - Automated Pass/Fail

```csharp
// ❌ Bad - Requires manual inspection
[Fact]
public void Test_Patient_Creation()
{
    var patient = new Patient("John");

    Console.WriteLine($"Patient created: {patient.Name}");  // Must read output!
    Debug.WriteLine($"ID: {patient.Id}");
}

// ✅ Good - Automated assertions
[Fact]
public void CreatePatient_Should_Set_Properties_Correctly()
{
    // Act
    var patient = new Patient(Guid.NewGuid(), "John", "john@example.com");

    // Assert - automated, no manual inspection
    patient.Name.ShouldBe("John");
    patient.Email.ShouldBe("john@example.com");
    patient.Id.ShouldNotBe(Guid.Empty);
}
```

### Timely - Written at the Right Time

```csharp
// TDD - Test BEFORE implementation
public class AppointmentSchedulerTests
{
    [Fact]
    public async Task ScheduleAsync_Should_Reject_Overlapping_Appointments()
    {
        // This test is written BEFORE the implementation exists
        // Forces us to think about the behavior first

        // Arrange
        var existingAppointment = await CreateAppointmentAsync(
            _doctorId,
            new DateTime(2024, 1, 15, 10, 0, 0),
            TimeSpan.FromMinutes(30));

        // Act & Assert
        var exception = await Should.ThrowAsync<BusinessException>(
            () => _scheduler.ScheduleAsync(
                _doctorId,
                new DateTime(2024, 1, 15, 10, 15, 0),  // Overlaps!
                TimeSpan.FromMinutes(30)));

        exception.Code.ShouldBe(ClinicErrorCodes.AppointmentOverlap);
    }
}
```

## Test Smells {#smells}

### Test Not Testing Anything

```csharp
// ❌ Bad - No meaningful assertions
[Fact]
public async Task CreatePatient_Test()
{
    var input = new CreatePatientDto { Name = "John" };

    var result = await _patientAppService.CreateAsync(input);

    result.ShouldNotBeNull();  // Only checks not null, not the actual behavior
}

// ✅ Good - Meaningful assertions
[Fact]
public async Task CreateAsync_Should_Create_Patient_With_Correct_Properties()
{
    // Arrange
    var input = new CreatePatientDto
    {
        Name = "John Doe",
        Email = "john@example.com",
        DateOfBirth = new DateTime(1990, 5, 15)
    };

    // Act
    var result = await _patientAppService.CreateAsync(input);

    // Assert - verify all properties
    result.ShouldNotBeNull();
    result.Id.ShouldNotBe(Guid.Empty);
    result.Name.ShouldBe("John Doe");
    result.Email.ShouldBe("john@example.com");
    result.DateOfBirth.ShouldBe(new DateTime(1990, 5, 15));
}
```

### Excessive Setup

```csharp
// ❌ Bad - Too much setup in test
[Fact]
public async Task Should_Schedule_Appointment()
{
    // 30 lines of setup!
    var department = new Department { Name = "Cardiology" };
    await _departmentRepository.InsertAsync(department);

    var doctor = new Doctor { Name = "Dr. Smith", DepartmentId = department.Id };
    await _doctorRepository.InsertAsync(doctor);

    var schedule = new DoctorSchedule { DoctorId = doctor.Id, DayOfWeek = DayOfWeek.Monday };
    await _scheduleRepository.InsertAsync(schedule);

    var patient = new Patient { Name = "John" };
    await _patientRepository.InsertAsync(patient);

    // ... more setup

    // Finally the actual test
    var result = await _appointmentService.ScheduleAsync(input);
}

// ✅ Good - Use builders and test data module
[Fact]
public async Task Should_Schedule_Appointment()
{
    // Arrange - minimal, focused setup
    var doctor = TestData.DrSmith;  // Pre-seeded
    var patient = TestData.PatientJohn;  // Pre-seeded

    var input = new ScheduleAppointmentDto
    {
        DoctorId = doctor.Id,
        PatientId = patient.Id,
        Time = TestData.NextAvailableSlot
    };

    // Act
    var result = await _appointmentService.ScheduleAsync(input);

    // Assert
    result.ShouldNotBeNull();
}

// Or use a builder
[Fact]
public async Task Should_Schedule_Appointment_With_Builder()
{
    var input = new AppointmentBuilder()
        .WithDoctor(TestData.DrSmith)
        .WithPatient(TestData.PatientJohn)
        .AtNextAvailableSlot()
        .BuildCreateDto();

    var result = await _appointmentService.ScheduleAsync(input);

    result.ShouldNotBeNull();
}
```

### Testing Multiple Scenarios in One Test

```csharp
// ❌ Bad - Multiple scenarios
[Fact]
public async Task Patient_Validation_Tests()
{
    // Scenario 1: Empty name
    var result1 = await Should.ThrowAsync<ValidationException>(
        () => _service.CreateAsync(new CreatePatientDto { Name = "", Email = "a@b.com" }));

    // Scenario 2: Invalid email
    var result2 = await Should.ThrowAsync<ValidationException>(
        () => _service.CreateAsync(new CreatePatientDto { Name = "John", Email = "invalid" }));

    // Scenario 3: Valid input (totally different concern!)
    var result3 = await _service.CreateAsync(
        new CreatePatientDto { Name = "John", Email = "john@example.com" });
    result3.ShouldNotBeNull();
}

// ✅ Good - One scenario per test
[Fact]
public async Task CreateAsync_Should_Throw_When_Name_Is_Empty()
{
    var input = new CreatePatientDto { Name = "", Email = "a@b.com" };

    await Should.ThrowAsync<ValidationException>(
        () => _service.CreateAsync(input));
}

[Fact]
public async Task CreateAsync_Should_Throw_When_Email_Is_Invalid()
{
    var input = new CreatePatientDto { Name = "John", Email = "invalid" };

    await Should.ThrowAsync<ValidationException>(
        () => _service.CreateAsync(input));
}

[Fact]
public async Task CreateAsync_Should_Succeed_With_Valid_Input()
{
    var input = new CreatePatientDto { Name = "John", Email = "john@example.com" };

    var result = await _service.CreateAsync(input);

    result.ShouldNotBeNull();
}

// Or use Theory for related variations
[Theory]
[InlineData("")]
[InlineData(null)]
[InlineData("   ")]
public async Task CreateAsync_Should_Throw_When_Name_Is_Invalid(string invalidName)
{
    var input = new CreatePatientDto { Name = invalidName, Email = "a@b.com" };

    await Should.ThrowAsync<ValidationException>(
        () => _service.CreateAsync(input));
}
```

### Conditional Test Logic

```csharp
// ❌ Bad - Conditional logic in test
[Fact]
public async Task Should_Handle_Appointment_Status()
{
    var appointment = await GetTestAppointment();

    if (appointment.Status == AppointmentStatus.Scheduled)
    {
        await _service.ConfirmAsync(appointment.Id);
        appointment.Status.ShouldBe(AppointmentStatus.Confirmed);
    }
    else if (appointment.Status == AppointmentStatus.Confirmed)
    {
        await _service.CompleteAsync(appointment.Id);
        appointment.Status.ShouldBe(AppointmentStatus.Completed);
    }
}

// ✅ Good - Separate tests, no conditionals
[Fact]
public async Task ConfirmAsync_Should_Change_Status_From_Scheduled_To_Confirmed()
{
    // Arrange - explicit state
    var appointment = await CreateScheduledAppointment();

    // Act
    await _service.ConfirmAsync(appointment.Id);

    // Assert
    var updated = await _repository.GetAsync(appointment.Id);
    updated.Status.ShouldBe(AppointmentStatus.Confirmed);
}

[Fact]
public async Task CompleteAsync_Should_Change_Status_From_Confirmed_To_Completed()
{
    // Arrange - explicit state
    var appointment = await CreateConfirmedAppointment();

    // Act
    await _service.CompleteAsync(appointment.Id);

    // Assert
    var updated = await _repository.GetAsync(appointment.Id);
    updated.Status.ShouldBe(AppointmentStatus.Completed);
}
```

### Erratic Tests

```csharp
// ❌ Bad - Race condition causes random failures
[Fact]
public async Task Should_Process_Concurrently()
{
    var tasks = Enumerable.Range(0, 100)
        .Select(_ => _service.ProcessAsync())
        .ToList();

    await Task.WhenAll(tasks);

    _counter.Value.ShouldBe(100);  // Sometimes fails due to race condition
}

// ✅ Good - Deterministic concurrent test
[Fact]
public async Task Should_Process_Concurrently_Without_Race_Conditions()
{
    // Arrange
    var results = new ConcurrentBag<ProcessResult>();

    // Act
    var tasks = Enumerable.Range(0, 100)
        .Select(i => Task.Run(async () =>
        {
            var result = await _service.ProcessAsync(i);
            results.Add(result);
        }))
        .ToList();

    await Task.WhenAll(tasks);

    // Assert - check results, not shared mutable state
    results.Count.ShouldBe(100);
    results.Select(r => r.InputId).Distinct().Count().ShouldBe(100);
}
```

## AAA Pattern {#aaa}

### Arrange-Act-Assert Structure

```csharp
[Fact]
public async Task DeactivateAsync_Should_Deactivate_Active_Patient()
{
    // Arrange
    var patientId = TestData.ActivePatientId;

    // Act
    await _patientAppService.DeactivateAsync(patientId);

    // Assert
    var patient = await _patientAppService.GetAsync(patientId);
    patient.IsActive.ShouldBeFalse();
    patient.DeactivatedAt.ShouldNotBeNull();
}

[Fact]
public async Task DeactivateAsync_Should_Throw_When_Patient_Already_Inactive()
{
    // Arrange
    var patientId = TestData.InactivePatientId;

    // Act & Assert (combined for exception tests)
    var exception = await Should.ThrowAsync<BusinessException>(
        () => _patientAppService.DeactivateAsync(patientId));

    exception.Code.ShouldBe(ClinicErrorCodes.PatientAlreadyInactive);
}
```

## Test Data Management {#test-data}

### Test Data Seeding Module

```csharp
public class ClinicTestDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    public static readonly Guid PatientJohnId = Guid.Parse("...");
    public static readonly Guid DrSmithId = Guid.Parse("...");

    public async Task SeedAsync(DataSeedContext context)
    {
        await SeedPatientsAsync();
        await SeedDoctorsAsync();
        await SeedAppointmentsAsync();
    }

    private async Task SeedPatientsAsync()
    {
        await _patientRepository.InsertAsync(
            new Patient(PatientJohnId, "John Doe", "john@example.com"));
    }
}
```

### Test Builders

```csharp
public class PatientBuilder
{
    private Guid _id = Guid.NewGuid();
    private string _name = "Test Patient";
    private string _email = "test@example.com";

    public PatientBuilder WithId(Guid id) { _id = id; return this; }
    public PatientBuilder WithName(string name) { _name = name; return this; }
    public PatientBuilder WithEmail(string email) { _email = email; return this; }

    public Patient Build() => new Patient(_id, _name, _email);
    public CreatePatientDto BuildCreateDto() => new() { Name = _name, Email = _email };
}

// Usage
[Fact]
public async Task Should_Create_Patient()
{
    var input = new PatientBuilder()
        .WithName("Jane Doe")
        .WithEmail("jane@example.com")
        .BuildCreateDto();

    var result = await _service.CreateAsync(input);

    result.Name.ShouldBe("Jane Doe");
}
```

## Related Concepts

- [TDD Principles](../../concepts/testing/tdd-principles.md)
- [FIRST Principles](../../concepts/testing/first.md)
- [Test Smells](../../concepts/testing/test-smells.md)

## Sources

- Test Driven Development: By Example by Kent Beck
- xUnit Test Patterns by Gerard Meszaros
- ABP Framework Testing Documentation
