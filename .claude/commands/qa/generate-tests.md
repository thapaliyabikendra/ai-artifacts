---
name: generate-tests
description: "Auto-generate tests for untested code using xUnit patterns"
args:
  - name: target
    description: "File path, class name, or 'gaps' to generate for coverage gaps"
    required: true
  - name: type
    description: "Test type: unit | integration | both"
    required: false
    default: "unit"
  - name: dry-run
    description: "Show what would be generated without writing files"
    required: false
---

# Generate Tests

Generate tests for: **$ARGUMENTS.target**
Test type: **$ARGUMENTS.type**
Dry run: **$ARGUMENTS.dry-run**

## Instructions

### Step 1: Identify Target

**If target is 'gaps':**
1. Run coverage analysis (see `/qa:coverage-report`)
2. Identify top 5 files without tests
3. Generate tests for each

**If target is file path:**
1. Read the source file
2. Parse public methods and their signatures
3. Identify validators if any

**If target is class name:**
1. Search for the class in `api/src/`
2. Read the source file

### Step 2: Analyze Source Code

For each public method, extract:
- Method name
- Parameters and types
- Return type
- Dependencies (injected services)
- Validation rules (if validator)
- Authorization attributes

### Step 3: Generate Unit Tests

For AppServices:
```csharp
using Shouldly;
using Xunit;
using NSubstitute;

namespace [Namespace].Tests;

public class [ClassName]Tests : [Module]ApplicationTestBase
{
    private readonly [ClassName] _sut;
    private readonly I[Dependency] _[dependency];

    public [ClassName]Tests()
    {
        _[dependency] = Substitute.For<I[Dependency]>();
        _sut = new [ClassName](_[dependency]);
    }

    #region [MethodName]

    [Fact]
    public async Task [MethodName]_ValidInput_ReturnsExpectedResult()
    {
        // Arrange
        var input = new [InputDto]
        {
            // Set valid properties
        };

        // Act
        var result = await _sut.[MethodName](input);

        // Assert
        result.ShouldNotBeNull();
    }

    [Fact]
    public async Task [MethodName]_InvalidInput_ThrowsValidationException()
    {
        // Arrange
        var input = new [InputDto](); // Missing required fields

        // Act & Assert
        await Should.ThrowAsync<AbpValidationException>(
            () => _sut.[MethodName](input)
        );
    }

    [Fact]
    public async Task [MethodName]_NotFound_ThrowsEntityNotFoundException()
    {
        // Arrange
        var nonExistentId = Guid.NewGuid();

        // Act & Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            () => _sut.[MethodName](nonExistentId)
        );
    }

    #endregion
}
```

For Validators:
```csharp
using FluentValidation.TestHelper;
using Xunit;

namespace [Namespace].Tests;

public class [ValidatorName]Tests
{
    private readonly [ValidatorName] _validator;

    public [ValidatorName]Tests()
    {
        _validator = new [ValidatorName]();
    }

    [Fact]
    public void Should_HaveError_When_[Property]_IsEmpty()
    {
        var model = new [DtoType] { [Property] = "" };
        var result = _validator.TestValidate(model);
        result.ShouldHaveValidationErrorFor(x => x.[Property]);
    }

    [Fact]
    public void Should_NotHaveError_When_[Property]_IsValid()
    {
        var model = new [DtoType] { [Property] = "Valid Value" };
        var result = _validator.TestValidate(model);
        result.ShouldNotHaveValidationErrorFor(x => x.[Property]);
    }

    [Theory]
    [InlineData("")]
    [InlineData(null)]
    [InlineData("   ")]
    public void [Property]_InvalidValues_ShouldFail(string value)
    {
        var model = new [DtoType] { [Property] = value };
        var result = _validator.TestValidate(model);
        result.ShouldHaveValidationErrorFor(x => x.[Property]);
    }
}
```

### Step 4: Generate Integration Tests (if type includes integration)

```csharp
using System.Net;
using System.Net.Http.Json;
using Shouldly;
using Xunit;

namespace [Namespace].HttpApi.Tests;

public class [ClassName]IntegrationTests : [Module]HttpApiTestBase
{
    [Fact]
    public async Task GetList_ReturnsPagedResult()
    {
        // Act
        var response = await Client.GetAsync("/api/app/[entity]");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.OK);
        var result = await response.Content.ReadFromJsonAsync<PagedResultDto<[Entity]Dto>>();
        result.ShouldNotBeNull();
    }

    [Fact]
    public async Task Get_ExistingId_ReturnsEntity()
    {
        // Arrange
        var existingId = TestData.[Entity]Id;

        // Act
        var response = await Client.GetAsync($"/api/app/[entity]/{existingId}");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.OK);
    }

    [Fact]
    public async Task Get_NonExistingId_Returns404()
    {
        // Act
        var response = await Client.GetAsync($"/api/app/[entity]/{Guid.NewGuid()}");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.NotFound);
    }

    [Fact]
    public async Task Create_ValidInput_Returns201()
    {
        // Arrange
        var input = new Create[Entity]Dto
        {
            // Valid properties
        };

        // Act
        var response = await Client.PostAsJsonAsync("/api/app/[entity]", input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.Created);
    }

    [Fact]
    public async Task Create_InvalidInput_Returns400()
    {
        // Arrange
        var input = new Create[Entity]Dto(); // Missing required

        // Act
        var response = await Client.PostAsJsonAsync("/api/app/[entity]", input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.BadRequest);
    }

    [Fact]
    public async Task Delete_Unauthorized_Returns403()
    {
        // Arrange: Login as user without delete permission
        await AuthenticateAsAsync("user-without-delete");

        // Act
        var response = await Client.DeleteAsync($"/api/app/[entity]/{TestData.[Entity]Id}");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.Forbidden);
    }
}
```

### Step 5: Output

**If dry-run:**
- Print generated test code to console
- Show file paths where tests would be written

**If not dry-run:**
- Write test files to appropriate locations:
  - Unit tests: `api/test/[Module].Application.Tests/[ClassName]Tests.cs`
  - Integration tests: `api/test/[Module].HttpApi.Tests/[ClassName]IntegrationTests.cs`
- Report files created

### Test Naming Convention

```
[MethodName]_[Scenario]_[ExpectedBehavior]

Examples:
- CreateAsync_ValidInput_CreatesAndReturnsDto
- CreateAsync_DuplicateEmail_ThrowsBusinessException
- GetAsync_NonExistentId_ThrowsEntityNotFoundException
- Validate_EmptyName_FailsValidation
```

## Related Skills

- `xunit-testing-patterns` - Detailed testing patterns
- `test-data-generation` - Test data setup
- `api-integration-testing` - WebApplicationFactory patterns
