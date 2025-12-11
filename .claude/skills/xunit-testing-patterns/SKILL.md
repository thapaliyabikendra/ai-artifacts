---
name: xunit-testing-patterns
description: "Master xUnit testing patterns for ABP Framework applications including unit tests, integration tests, test data seeders, and mocking strategies. Use when: (1) writing xUnit tests for ABP services, (2) creating test data seeders, (3) implementing integration tests, (4) setting up test infrastructure."
---

# xUnit Testing Patterns for ABP Framework

Comprehensive testing patterns for ABP Framework applications using xUnit, Shouldly, and NSubstitute.

## When to Use

- Writing unit tests for AppServices
- Creating integration tests for ABP modules
- Setting up test data seeders
- Mocking repositories and services
- Testing authorization and validation
- Writing domain service tests

## Test Project Structure

```
{ProjectName}.TestBase/
├── {ProjectName}TestBase.cs           # Base class with common setup
├── {ProjectName}TestBaseModule.cs     # Test module configuration
└── {Feature}/
    ├── {Entity}TestData.cs            # Test constants
    └── {Entity}TestDataSeedContributor.cs  # Test data seeder

{ProjectName}.Application.Tests/
├── {ProjectName}ApplicationTestBase.cs  # Application test base
├── {ProjectName}ApplicationTestModule.cs
└── {Feature}/
    └── {Entity}AppService_Tests.cs    # AppService tests

{ProjectName}.Domain.Tests/
├── {ProjectName}DomainTestBase.cs     # Domain test base
├── {ProjectName}DomainTestModule.cs
└── {Feature}/
    └── {Entity}Manager_Tests.cs       # Domain service tests
```

## Core Templates

### Test Data Constants

```csharp
// {ProjectName}.TestBase/{Feature}/{Entity}TestData.cs
namespace {ProjectName}.{Feature};

public static class {Entity}TestData
{
    public static Guid {Entity}1Id { get; } = Guid.Parse("00000000-0000-0000-0000-000000000001");
    public static Guid {Entity}2Id { get; } = Guid.Parse("00000000-0000-0000-0000-000000000002");

    public const string {Entity}1Name = "Test {Entity} 1";
    public const string {Entity}1Email = "test1@example.com";

    public const string {Entity}2Name = "Test {Entity} 2";
    public const string {Entity}2Email = "test2@example.com";

    // Invalid data for negative tests
    public const string InvalidEmail = "not-an-email";
    public const string TooLongName = "This name is way too long and should exceed the maximum length constraint of one hundred characters in the database";
}
```

### Test Data Seeder

```csharp
// {ProjectName}.TestBase/{Feature}/{Entity}TestDataSeedContributor.cs
using System.Threading.Tasks;
using Volo.Abp.Data;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Domain.Repositories;
using Volo.Abp.Guids;

namespace {ProjectName}.{Feature};

public class {Entity}TestDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    private readonly IRepository<{Entity}, Guid> _repository;
    private readonly IGuidGenerator _guidGenerator;

    public {Entity}TestDataSeedContributor(
        IRepository<{Entity}, Guid> repository,
        IGuidGenerator guidGenerator)
    {
        _repository = repository;
        _guidGenerator = guidGenerator;
    }

    public async Task SeedAsync(DataSeedContext context)
    {
        if (await _repository.GetCountAsync() > 0)
        {
            return;
        }

        await _repository.InsertAsync(
            new {Entity}(
                {Entity}TestData.{Entity}1Id,
                {Entity}TestData.{Entity}1Name,
                {Entity}TestData.{Entity}1Email),
            autoSave: true);

        await _repository.InsertAsync(
            new {Entity}(
                {Entity}TestData.{Entity}2Id,
                {Entity}TestData.{Entity}2Name,
                {Entity}TestData.{Entity}2Email),
            autoSave: true);
    }
}
```

### AppService Test Class

```csharp
// {ProjectName}.Application.Tests/{Feature}/{Entity}AppService_Tests.cs
using System;
using System.Threading.Tasks;
using Shouldly;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Domain.Entities;
using Volo.Abp.Validation;
using Xunit;

namespace {ProjectName}.{Feature};

public class {Entity}AppService_Tests : {ProjectName}ApplicationTestBase
{
    private readonly I{Entity}AppService _{entity}AppService;

    public {Entity}AppService_Tests()
    {
        _{entity}AppService = GetRequiredService<I{Entity}AppService>();
    }

    #region GetAsync Tests

    [Fact]
    public async Task Should_Get_{Entity}_By_Id()
    {
        // Act
        var result = await _{entity}AppService.GetAsync({Entity}TestData.{Entity}1Id);

        // Assert
        result.ShouldNotBeNull();
        result.Id.ShouldBe({Entity}TestData.{Entity}1Id);
        result.Name.ShouldBe({Entity}TestData.{Entity}1Name);
    }

    [Fact]
    public async Task Should_Throw_When_{Entity}_Not_Found()
    {
        // Arrange
        var nonExistentId = Guid.NewGuid();

        // Act & Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            async () => await _{entity}AppService.GetAsync(nonExistentId));
    }

    #endregion

    #region GetListAsync Tests

    [Fact]
    public async Task Should_Get_Paginated_{Entity}_List()
    {
        // Act
        var result = await _{entity}AppService.GetListAsync(
            new Get{Entity}ListInput { MaxResultCount = 10 });

        // Assert
        result.ShouldNotBeNull();
        result.TotalCount.ShouldBeGreaterThanOrEqualTo(2);
        result.Items.Count.ShouldBeGreaterThanOrEqualTo(2);
    }

    [Fact]
    public async Task Should_Filter_{Entity}_List_By_Name()
    {
        // Act
        var result = await _{entity}AppService.GetListAsync(
            new Get{Entity}ListInput { Filter = "Test {Entity} 1" });

        // Assert
        result.Items.ShouldContain(x => x.Name == {Entity}TestData.{Entity}1Name);
    }

    #endregion

    #region CreateAsync Tests

    [Fact]
    public async Task Should_Create_{Entity}_With_Valid_Input()
    {
        // Arrange
        var input = new CreateUpdate{Entity}Dto
        {
            Name = "New Test {Entity}",
            Email = "new@example.com"
        };

        // Act
        var result = await _{entity}AppService.CreateAsync(input);

        // Assert
        result.ShouldNotBeNull();
        result.Id.ShouldNotBe(Guid.Empty);
        result.Name.ShouldBe(input.Name);
        result.Email.ShouldBe(input.Email);
    }

    [Fact]
    public async Task Should_Throw_When_Creating_With_Empty_Name()
    {
        // Arrange
        var input = new CreateUpdate{Entity}Dto
        {
            Name = "",
            Email = "test@example.com"
        };

        // Act & Assert
        await Should.ThrowAsync<AbpValidationException>(
            async () => await _{entity}AppService.CreateAsync(input));
    }

    [Fact]
    public async Task Should_Throw_When_Creating_With_Invalid_Email()
    {
        // Arrange
        var input = new CreateUpdate{Entity}Dto
        {
            Name = "Test Name",
            Email = {Entity}TestData.InvalidEmail
        };

        // Act & Assert
        await Should.ThrowAsync<AbpValidationException>(
            async () => await _{entity}AppService.CreateAsync(input));
    }

    #endregion

    #region UpdateAsync Tests

    [Fact]
    public async Task Should_Update_{Entity}_With_Valid_Input()
    {
        // Arrange
        var input = new CreateUpdate{Entity}Dto
        {
            Name = "Updated Name",
            Email = "updated@example.com"
        };

        // Act
        var result = await _{entity}AppService.UpdateAsync(
            {Entity}TestData.{Entity}1Id, input);

        // Assert
        result.Name.ShouldBe(input.Name);
        result.Email.ShouldBe(input.Email);
    }

    [Fact]
    public async Task Should_Throw_When_Updating_Non_Existent_{Entity}()
    {
        // Arrange
        var input = new CreateUpdate{Entity}Dto
        {
            Name = "Updated Name",
            Email = "updated@example.com"
        };

        // Act & Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            async () => await _{entity}AppService.UpdateAsync(Guid.NewGuid(), input));
    }

    #endregion

    #region DeleteAsync Tests

    [Fact]
    public async Task Should_Delete_{Entity}()
    {
        // Act
        await _{entity}AppService.DeleteAsync({Entity}TestData.{Entity}2Id);

        // Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            async () => await _{entity}AppService.GetAsync({Entity}TestData.{Entity}2Id));
    }

    [Fact]
    public async Task Should_Throw_When_Deleting_Non_Existent_{Entity}()
    {
        // Act & Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            async () => await _{entity}AppService.DeleteAsync(Guid.NewGuid()));
    }

    #endregion
}
```

## Test Categories

### 1. Happy Path Tests
Test normal successful operations.

```csharp
[Fact]
public async Task Should_Create_Entity_Successfully()
{
    // Standard create with valid data
}
```

### 2. Validation Tests
Test input validation and constraints.

```csharp
[Theory]
[InlineData("")]
[InlineData(null)]
[InlineData("   ")]
public async Task Should_Reject_Invalid_Name(string name)
{
    var input = new CreateDto { Name = name };
    await Should.ThrowAsync<AbpValidationException>(
        () => _service.CreateAsync(input));
}
```

### 3. Authorization Tests
Test permission enforcement.

```csharp
[Fact]
public async Task Should_Require_Permission_To_Create()
{
    // Login as user without permission
    await WithUnitOfWorkAsync(async () =>
    {
        await Should.ThrowAsync<AbpAuthorizationException>(
            () => _service.CreateAsync(input));
    });
}
```

### 4. Edge Case Tests
Test boundary conditions and edge cases.

```csharp
[Fact]
public async Task Should_Handle_Empty_List()
{
    // Clear all data
    var result = await _service.GetListAsync(new GetListInput());
    result.TotalCount.ShouldBe(0);
    result.Items.ShouldBeEmpty();
}

[Fact]
public async Task Should_Handle_Max_Page_Size()
{
    var result = await _service.GetListAsync(
        new GetListInput { MaxResultCount = 1000 });
    result.Items.Count.ShouldBeLessThanOrEqualTo(100); // Capped
}
```

## Mocking with NSubstitute

```csharp
using NSubstitute;

public class {Entity}AppService_UnitTests
{
    private readonly I{Entity}Repository _repository;
    private readonly {Entity}AppService _service;

    public {Entity}AppService_UnitTests()
    {
        _repository = Substitute.For<I{Entity}Repository>();
        _service = new {Entity}AppService(_repository);
    }

    [Fact]
    public async Task Should_Call_Repository_GetAsync()
    {
        // Arrange
        var entityId = Guid.NewGuid();
        var entity = new {Entity}(entityId, "Test", "test@example.com");
        _repository.GetAsync(entityId).Returns(entity);

        // Act
        await _service.GetAsync(entityId);

        // Assert
        await _repository.Received(1).GetAsync(entityId);
    }
}
```

## Shouldly Assertion Patterns

```csharp
// Null checks
result.ShouldNotBeNull();
result.ShouldBeNull();

// Equality
result.Id.ShouldBe(expectedId);
result.Name.ShouldNotBe(oldName);

// Collections
result.Items.ShouldNotBeEmpty();
result.Items.ShouldContain(x => x.Name == "Test");
result.Items.Count.ShouldBe(5);

// Numeric comparisons
result.TotalCount.ShouldBeGreaterThan(0);
result.TotalCount.ShouldBeLessThanOrEqualTo(100);

// String assertions
result.Name.ShouldStartWith("Test");
result.Email.ShouldContain("@");

// Exception assertions
await Should.ThrowAsync<EntityNotFoundException>(
    async () => await _service.GetAsync(invalidId));

var ex = await Should.ThrowAsync<BusinessException>(
    async () => await _service.CreateAsync(input));
ex.Code.ShouldBe("DuplicateEmail");
```

## References

- [references/integration-test-patterns.md](references/integration-test-patterns.md) - Advanced integration testing
- [references/test-fixtures.md](references/test-fixtures.md) - Shared test fixtures
