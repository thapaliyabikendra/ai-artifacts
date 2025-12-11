# Test Cases: {{Feature Name}}

**Created**: {{Date}}
**Author**: qa-engineer
**Status**: Draft | Review | Approved
**Requirements Doc**: [requirements.md](./requirements.md)
**Technical Design**: [technical-design.md](./technical-design.md)

---

## 1. Test Strategy

### 1.1 Scope

| Type | Coverage | Tools |
|------|----------|-------|
| Unit Tests | Domain services, validators | xUnit, NSubstitute |
| Integration Tests | AppServices, repositories | xUnit, ABP TestBase |
| API Tests | HTTP endpoints | xUnit, TestServer |
| E2E Tests | User workflows | Playwright (if UI exists) |

### 1.2 Test Environment
- Database: SQLite InMemory (tests)
- Test data: Seed via ABP DataSeedContributor

---

## 2. Test Cases

### 2.1 Create Operations

| ID | Test Case | Type | Preconditions | Steps | Expected Result | Priority |
|----|-----------|------|---------------|-------|-----------------|----------|
| TC-C001 | Create {{entity}} with valid data | Integration | User authenticated with Create permission | 1. Call CreateAsync with valid DTO | Entity created, returns DTO with Id | P1 |
| TC-C002 | Create {{entity}} - required field missing | Integration | User authenticated | 1. Call CreateAsync with empty {{property}} | AbpValidationException thrown | P1 |
| TC-C003 | Create {{entity}} - field exceeds max length | Integration | User authenticated | 1. Call CreateAsync with {{property}} > max | AbpValidationException thrown | P2 |
| TC-C004 | Create {{entity}} - unauthorized | Integration | User NOT authenticated | 1. Call CreateAsync | AbpAuthorizationException thrown | P1 |
| TC-C005 | Create {{entity}} - missing permission | Integration | User authenticated, no Create permission | 1. Call CreateAsync | AbpAuthorizationException thrown | P1 |

### 2.2 Read Operations

| ID | Test Case | Type | Preconditions | Steps | Expected Result | Priority |
|----|-----------|------|---------------|-------|-----------------|----------|
| TC-R001 | Get {{entity}} by ID | Integration | {{Entity}} exists | 1. Call GetAsync with valid Id | Returns {{Entity}}Dto | P1 |
| TC-R002 | Get {{entity}} - not found | Integration | {{Entity}} does not exist | 1. Call GetAsync with invalid Id | EntityNotFoundException thrown | P1 |
| TC-R003 | Get {{entity}} list - empty | Integration | No {{entities}} in DB | 1. Call GetListAsync | Returns empty list with TotalCount=0 | P2 |
| TC-R004 | Get {{entity}} list - with data | Integration | Multiple {{entities}} exist | 1. Call GetListAsync | Returns paged list with correct count | P1 |
| TC-R005 | Get {{entity}} list - with filter | Integration | {{Entities}} with various {{property}} values | 1. Call GetListAsync with Filter | Returns filtered results | P1 |
| TC-R006 | Get {{entity}} list - pagination | Integration | 20+ {{entities}} exist | 1. Call GetListAsync with SkipCount=10, MaxResultCount=5 | Returns correct page of 5 items | P1 |
| TC-R007 | Get {{entity}} list - sorting | Integration | Multiple {{entities}} exist | 1. Call GetListAsync with Sorting="{{property}}" | Returns sorted results | P2 |
| TC-R008 | Get deleted {{entity}} | Integration | {{Entity}} is soft-deleted | 1. Call GetAsync with deleted entity Id | EntityNotFoundException (filtered out) | P1 |

### 2.3 Update Operations

| ID | Test Case | Type | Preconditions | Steps | Expected Result | Priority |
|----|-----------|------|---------------|-------|-----------------|----------|
| TC-U001 | Update {{entity}} with valid data | Integration | {{Entity}} exists, user has Edit permission | 1. Call UpdateAsync with valid DTO | Entity updated, returns updated DTO | P1 |
| TC-U002 | Update {{entity}} - not found | Integration | {{Entity}} does not exist | 1. Call UpdateAsync with invalid Id | EntityNotFoundException thrown | P1 |
| TC-U003 | Update {{entity}} - validation failure | Integration | {{Entity}} exists | 1. Call UpdateAsync with invalid data | AbpValidationException thrown | P1 |
| TC-U004 | Update {{entity}} - unauthorized | Integration | User NOT authenticated | 1. Call UpdateAsync | AbpAuthorizationException thrown | P1 |
| TC-U005 | Update {{entity}} - missing permission | Integration | User authenticated, no Edit permission | 1. Call UpdateAsync | AbpAuthorizationException thrown | P1 |

### 2.4 Delete Operations

| ID | Test Case | Type | Preconditions | Steps | Expected Result | Priority |
|----|-----------|------|---------------|-------|-----------------|----------|
| TC-D001 | Delete {{entity}} (soft delete) | Integration | {{Entity}} exists, user has Delete permission | 1. Call DeleteAsync 2. Try to GetAsync | Delete succeeds, Get returns not found | P1 |
| TC-D002 | Delete {{entity}} - not found | Integration | {{Entity}} does not exist | 1. Call DeleteAsync with invalid Id | EntityNotFoundException thrown | P2 |
| TC-D003 | Delete {{entity}} - unauthorized | Integration | User NOT authenticated | 1. Call DeleteAsync | AbpAuthorizationException thrown | P1 |
| TC-D004 | Delete {{entity}} - missing permission | Integration | User authenticated, no Delete permission | 1. Call DeleteAsync | AbpAuthorizationException thrown | P1 |

### 2.5 Business Rule Tests

| ID | Test Case | Type | Preconditions | Steps | Expected Result | Priority |
|----|-----------|------|---------------|-------|-----------------|----------|
| TC-BR001 | {{Business rule description}} | Integration | {{Preconditions}} | {{Steps}} | {{Expected}} | P1 |

### 2.6 Validation Tests

| ID | Test Case | Type | Input | Expected Result | Priority |
|----|-----------|------|-------|-----------------|----------|
| TC-V001 | Validate {{property}} - empty | Unit | "" | Validation error: "{{Property}} is required" | P1 |
| TC-V002 | Validate {{property}} - too long | Unit | String > max length | Validation error: "{{Property}} must be {{max}} characters or less" | P2 |
| TC-V003 | Validate email - invalid format | Unit | "invalid-email" | Validation error: "Invalid email format" | P1 |
| TC-V004 | Validate {{property}} - valid | Unit | Valid value | No validation errors | P1 |

---

## 3. xUnit Test Code Templates

### 3.1 AppService Tests

```csharp
using System;
using System.Threading.Tasks;
using Shouldly;
using Volo.Abp;
using Volo.Abp.Validation;
using Xunit;

namespace {{ProjectName}}.{{Feature}};

public class {{Entity}}AppService_Tests : {{ProjectName}}ApplicationTestBase
{
    private readonly I{{Entity}}AppService _{{entity}}AppService;

    public {{Entity}}AppService_Tests()
    {
        _{{entity}}AppService = GetRequiredService<I{{Entity}}AppService>();
    }

    [Fact]
    public async Task Should_Create_{{Entity}}_With_Valid_Data()
    {
        // Arrange
        var input = new CreateUpdate{{Entity}}Dto
        {
            {{Property}} = "Test Value"
            // Add more properties
        };

        // Act
        var result = await _{{entity}}AppService.CreateAsync(input);

        // Assert
        result.ShouldNotBeNull();
        result.Id.ShouldNotBe(Guid.Empty);
        result.{{Property}}.ShouldBe("Test Value");
    }

    [Fact]
    public async Task Should_Throw_Validation_Exception_When_{{Property}}_Empty()
    {
        // Arrange
        var input = new CreateUpdate{{Entity}}Dto
        {
            {{Property}} = ""
        };

        // Act & Assert
        await Should.ThrowAsync<AbpValidationException>(
            async () => await _{{entity}}AppService.CreateAsync(input)
        );
    }

    [Fact]
    public async Task Should_Get_{{Entity}}_By_Id()
    {
        // Arrange
        var created = await _{{entity}}AppService.CreateAsync(new CreateUpdate{{Entity}}Dto
        {
            {{Property}} = "Test"
        });

        // Act
        var result = await _{{entity}}AppService.GetAsync(created.Id);

        // Assert
        result.ShouldNotBeNull();
        result.Id.ShouldBe(created.Id);
    }

    [Fact]
    public async Task Should_Get_Paged_List()
    {
        // Arrange
        for (int i = 0; i < 15; i++)
        {
            await _{{entity}}AppService.CreateAsync(new CreateUpdate{{Entity}}Dto
            {
                {{Property}} = $"Test {i}"
            });
        }

        // Act
        var result = await _{{entity}}AppService.GetListAsync(new Get{{Entity}}ListInput
        {
            SkipCount = 0,
            MaxResultCount = 10
        });

        // Assert
        result.TotalCount.ShouldBeGreaterThanOrEqualTo(15);
        result.Items.Count.ShouldBe(10);
    }

    [Fact]
    public async Task Should_Filter_List_By_{{Property}}()
    {
        // Arrange
        await _{{entity}}AppService.CreateAsync(new CreateUpdate{{Entity}}Dto { {{Property}} = "Alpha" });
        await _{{entity}}AppService.CreateAsync(new CreateUpdate{{Entity}}Dto { {{Property}} = "Beta" });
        await _{{entity}}AppService.CreateAsync(new CreateUpdate{{Entity}}Dto { {{Property}} = "Gamma" });

        // Act
        var result = await _{{entity}}AppService.GetListAsync(new Get{{Entity}}ListInput
        {
            Filter = "Alpha"
        });

        // Assert
        result.Items.ShouldContain(x => x.{{Property}} == "Alpha");
        result.Items.ShouldNotContain(x => x.{{Property}} == "Beta");
    }

    [Fact]
    public async Task Should_Update_{{Entity}}()
    {
        // Arrange
        var created = await _{{entity}}AppService.CreateAsync(new CreateUpdate{{Entity}}Dto
        {
            {{Property}} = "Original"
        });

        // Act
        var result = await _{{entity}}AppService.UpdateAsync(created.Id, new CreateUpdate{{Entity}}Dto
        {
            {{Property}} = "Updated"
        });

        // Assert
        result.{{Property}}.ShouldBe("Updated");
    }

    [Fact]
    public async Task Should_Delete_{{Entity}}()
    {
        // Arrange
        var created = await _{{entity}}AppService.CreateAsync(new CreateUpdate{{Entity}}Dto
        {
            {{Property}} = "ToDelete"
        });

        // Act
        await _{{entity}}AppService.DeleteAsync(created.Id);

        // Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            async () => await _{{entity}}AppService.GetAsync(created.Id)
        );
    }

    [Fact]
    public async Task Should_Throw_When_{{Entity}}_Not_Found()
    {
        // Act & Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            async () => await _{{entity}}AppService.GetAsync(Guid.NewGuid())
        );
    }
}
```

### 3.2 Validator Tests

```csharp
using FluentValidation.TestHelper;
using Xunit;

namespace {{ProjectName}}.{{Feature}};

public class CreateUpdate{{Entity}}DtoValidator_Tests
{
    private readonly CreateUpdate{{Entity}}DtoValidator _validator;

    public CreateUpdate{{Entity}}DtoValidator_Tests()
    {
        _validator = new CreateUpdate{{Entity}}DtoValidator();
    }

    [Fact]
    public void Should_Have_Error_When_{{Property}}_Is_Empty()
    {
        var model = new CreateUpdate{{Entity}}Dto { {{Property}} = "" };
        var result = _validator.TestValidate(model);
        result.ShouldHaveValidationErrorFor(x => x.{{Property}});
    }

    [Fact]
    public void Should_Have_Error_When_{{Property}}_Exceeds_Max_Length()
    {
        var model = new CreateUpdate{{Entity}}Dto { {{Property}} = new string('a', 101) };
        var result = _validator.TestValidate(model);
        result.ShouldHaveValidationErrorFor(x => x.{{Property}});
    }

    [Fact]
    public void Should_Not_Have_Error_When_Valid()
    {
        var model = new CreateUpdate{{Entity}}Dto { {{Property}} = "Valid Value" };
        var result = _validator.TestValidate(model);
        result.ShouldNotHaveAnyValidationErrors();
    }
}
```

---

## 4. Test Data Seeds

```csharp
// In {{ProjectName}}TestDataSeedContributor.cs

public class {{Feature}}TestDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    private readonly IRepository<{{Entity}}, Guid> _repository;
    private readonly IGuidGenerator _guidGenerator;

    public async Task SeedAsync(DataSeedContext context)
    {
        if (await _repository.GetCountAsync() > 0)
        {
            return;
        }

        // Seed test data
        await _repository.InsertAsync(new {{Entity}}(
            _guidGenerator.Create(),
            "Test {{Entity}} 1"
        ));

        await _repository.InsertAsync(new {{Entity}}(
            _guidGenerator.Create(),
            "Test {{Entity}} 2"
        ));
    }
}
```

---

## 5. Test Execution

### 5.1 Run All Tests
```bash
dotnet test api/test/{{ProjectName}}.Application.Tests
```

### 5.2 Run Specific Tests
```bash
dotnet test --filter "FullyQualifiedName~{{Entity}}AppService_Tests"
```

### 5.3 Run with Coverage
```bash
dotnet test --collect:"XPlat Code Coverage"
```

---

## 6. Exit Criteria

- [ ] All P1 test cases pass
- [ ] Code coverage ≥ 80%
- [ ] No critical bugs open
- [ ] All validation rules tested
- [ ] Authorization tests pass
- [ ] Soft delete behavior verified
