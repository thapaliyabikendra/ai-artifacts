---
description: Write failing xUnit tests following TDD red phase for ABP/.NET
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "<feature-or-component>"
---

# TDD Red Phase - Write Failing Tests

Generate failing xUnit tests for ABP Framework applications.

**Arguments**: $ARGUMENTS

## Execution

Use Task tool with `subagent_type="qa-engineer"`:

```
Generate comprehensive FAILING xUnit tests for: {feature-or-component}

Context: Read existing tests in test/ folder
Skills: Apply xunit-testing-patterns

## Test Structure

- Use xUnit with Shouldly assertions
- Arrange-Act-Assert pattern
- Should_ExpectedBehavior_When_Condition naming
- Inherit from appropriate ABP test base class

## Coverage Categories

1. **Happy Path**: Normal successful operations
2. **Validation**: Invalid inputs, missing required fields
3. **Authorization**: Permission checks, role-based access
4. **Edge Cases**: Empty collections, boundary values, nulls
5. **Error Handling**: Expected exceptions, error responses

## ABP Test Patterns

**Application Service Test:**
```csharp
public class PatientAppService_Tests : ClinicManagementSystemApplicationTestBase
{
    private readonly IPatientAppService _patientAppService;

    public PatientAppService_Tests()
    {
        _patientAppService = GetRequiredService<IPatientAppService>();
    }

    [Fact]
    public async Task Should_Create_Patient_With_Valid_Input()
    {
        // Arrange
        var input = new CreateUpdatePatientDto
        {
            FirstName = "John",
            LastName = "Doe",
            Email = "john@example.com"
        };

        // Act
        var result = await _patientAppService.CreateAsync(input);

        // Assert
        result.ShouldNotBeNull();
        result.Id.ShouldNotBe(Guid.Empty);
        result.FirstName.ShouldBe("John");
    }

    [Fact]
    public async Task Should_Throw_When_Email_Invalid()
    {
        // Arrange
        var input = new CreateUpdatePatientDto
        {
            FirstName = "John",
            Email = "invalid-email"
        };

        // Act & Assert
        await Should.ThrowAsync<AbpValidationException>(
            () => _patientAppService.CreateAsync(input)
        );
    }
}
```

## Requirements

- Tests MUST fail when run (missing implementation)
- Failures for RIGHT reasons (not syntax errors)
- Each test verifies ONE behavior
- Use meaningful test data
- Mock external dependencies with NSubstitute

## Output

- Test files in test/ClinicManagementSystem.Application.Tests/
- Run command: `dotnet test`
- Next step: Proceed to GREEN phase
```

**Checkpoint**: All tests fail with meaningful error messages.

---

Test requirements: $ARGUMENTS
