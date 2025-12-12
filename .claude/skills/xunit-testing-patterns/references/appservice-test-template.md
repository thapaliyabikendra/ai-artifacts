# AppService Test Class Template

Complete test class template for ABP Framework AppServices.

## Full Test Class

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

[Trait("Category", "Integration")]
[Trait("Feature", "{Feature}")]
public class {Entity}AppService_Tests : {ProjectName}ApplicationTestBase
{
    private readonly I{Entity}AppService _{entity}AppService;

    public {Entity}AppService_Tests()
    {
        _{entity}AppService = GetRequiredService<I{Entity}AppService>();
    }

    #region GetAsync Tests

    [Fact]
    public async Task GetAsync_WithValidId_Returns{Entity}()
    {
        // Act
        var result = await _{entity}AppService.GetAsync({Entity}TestData.{Entity}1Id);

        // Assert
        result.ShouldNotBeNull();
        result.Id.ShouldBe({Entity}TestData.{Entity}1Id);
        result.Name.ShouldBe({Entity}TestData.{Entity}1Name);
    }

    [Fact]
    public async Task GetAsync_WithNonExistentId_ThrowsEntityNotFoundException()
    {
        // Act & Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            async () => await _{entity}AppService.GetAsync({Entity}TestData.NonExistentId));
    }

    #endregion

    #region GetListAsync Tests

    [Fact]
    public async Task GetListAsync_WithDefaults_ReturnsPaginatedList()
    {
        // Act
        var result = await _{entity}AppService.GetListAsync(
            new Get{Entity}sInput { MaxResultCount = 10 });

        // Assert
        result.ShouldNotBeNull();
        result.TotalCount.ShouldBeGreaterThanOrEqualTo(2);
        result.Items.Count.ShouldBeGreaterThanOrEqualTo(2);
    }

    [Fact]
    public async Task GetListAsync_WithFilter_ReturnsFilteredResults()
    {
        // Act
        var result = await _{entity}AppService.GetListAsync(
            new Get{Entity}sInput { Filter = {Entity}TestData.{Entity}1Name });

        // Assert
        result.Items.ShouldContain(x => x.Name == {Entity}TestData.{Entity}1Name);
    }

    [Fact]
    public async Task GetListAsync_WithPagination_RespectsPageSize()
    {
        // Act
        var result = await _{entity}AppService.GetListAsync(
            new Get{Entity}sInput { MaxResultCount = 1 });

        // Assert
        result.Items.Count.ShouldBeLessThanOrEqualTo(1);
    }

    #endregion

    #region CreateAsync Tests

    [Fact]
    public async Task CreateAsync_WithValidInput_CreatesAndReturns{Entity}()
    {
        // Arrange
        var input = new Create{Entity}Dto
        {
            Name = {Entity}TestData.ValidName,
            // Add other required properties
        };

        // Act
        var result = await _{entity}AppService.CreateAsync(input);

        // Assert
        result.ShouldNotBeNull();
        result.Id.ShouldNotBe(Guid.Empty);
        result.Name.ShouldBe(input.Name);

        // Verify persisted
        var fetched = await _{entity}AppService.GetAsync(result.Id);
        fetched.ShouldNotBeNull();
    }

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData(null)]
    public async Task CreateAsync_WithEmptyName_ThrowsValidationException(string? name)
    {
        // Arrange
        var input = new Create{Entity}Dto
        {
            Name = name!,
        };

        // Act & Assert
        await Should.ThrowAsync<AbpValidationException>(
            async () => await _{entity}AppService.CreateAsync(input));
    }

    [Fact]
    public async Task CreateAsync_WithTooLongName_ThrowsValidationException()
    {
        // Arrange
        var input = new Create{Entity}Dto
        {
            Name = {Entity}TestData.TooLongName,
        };

        // Act & Assert
        await Should.ThrowAsync<AbpValidationException>(
            async () => await _{entity}AppService.CreateAsync(input));
    }

    #endregion

    #region UpdateAsync Tests

    [Fact]
    public async Task UpdateAsync_WithValidInput_Updates{Entity}()
    {
        // Arrange
        var input = new Update{Entity}Dto
        {
            Name = "Updated Name",
        };

        // Act
        var result = await _{entity}AppService.UpdateAsync({Entity}TestData.{Entity}1Id, input);

        // Assert
        result.Name.ShouldBe(input.Name);
    }

    [Fact]
    public async Task UpdateAsync_WithNonExistentId_ThrowsEntityNotFoundException()
    {
        // Arrange
        var input = new Update{Entity}Dto
        {
            Name = "Updated Name",
        };

        // Act & Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            async () => await _{entity}AppService.UpdateAsync({Entity}TestData.NonExistentId, input));
    }

    #endregion

    #region DeleteAsync Tests

    [Fact]
    public async Task DeleteAsync_WithValidId_Deletes{Entity}()
    {
        // Act
        await _{entity}AppService.DeleteAsync({Entity}TestData.{Entity}2Id);

        // Assert - Should throw when trying to get deleted entity
        await Should.ThrowAsync<EntityNotFoundException>(
            async () => await _{entity}AppService.GetAsync({Entity}TestData.{Entity}2Id));
    }

    [Fact]
    public async Task DeleteAsync_WithNonExistentId_ThrowsEntityNotFoundException()
    {
        // Act & Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            async () => await _{entity}AppService.DeleteAsync({Entity}TestData.NonExistentId));
    }

    #endregion
}
```

## Lifecycle Tests (Activate/Deactivate)

```csharp
#region Lifecycle Tests

[Fact]
public async Task ActivateAsync_WhenInactive_SetsIsActiveTrue()
{
    // Arrange - ensure entity is inactive
    await _{entity}AppService.DeactivateAsync({Entity}TestData.{Entity}1Id);

    // Act
    var result = await _{entity}AppService.ActivateAsync({Entity}TestData.{Entity}1Id);

    // Assert
    result.IsActive.ShouldBeTrue();
}

[Fact]
public async Task DeactivateAsync_WhenActive_SetsIsActiveFalse()
{
    // Act
    var result = await _{entity}AppService.DeactivateAsync({Entity}TestData.{Entity}1Id);

    // Assert
    result.IsActive.ShouldBeFalse();
}

[Fact]
public async Task ActivateAsync_WhenAlreadyActive_IsIdempotent()
{
    // Act - activate already active entity
    var result = await _{entity}AppService.ActivateAsync({Entity}TestData.{Entity}1Id);

    // Assert - should succeed without error
    result.IsActive.ShouldBeTrue();
}

[Fact]
public async Task GetListAsync_WithIsActiveFilter_ReturnsFilteredResults()
{
    // Arrange - deactivate one entity
    await _{entity}AppService.DeactivateAsync({Entity}TestData.{Entity}1Id);

    // Act
    var activeOnly = await _{entity}AppService.GetListAsync(
        new Get{Entity}sInput { IsActive = true });
    var inactiveOnly = await _{entity}AppService.GetListAsync(
        new Get{Entity}sInput { IsActive = false });

    // Assert
    activeOnly.Items.ShouldAllBe(x => x.IsActive);
    inactiveOnly.Items.ShouldAllBe(x => !x.IsActive);
}

#endregion
```

## Mocking with NSubstitute

```csharp
using NSubstitute;

public class {Entity}AppService_UnitTests
{
    private readonly IRepository<{Entity}, Guid> _repository;
    private readonly {Entity}AppService _service;

    public {Entity}AppService_UnitTests()
    {
        _repository = Substitute.For<IRepository<{Entity}, Guid>>();
        _service = new {Entity}AppService(_repository);
    }

    [Fact]
    public async Task Should_Call_Repository_GetAsync()
    {
        // Arrange
        var entityId = Guid.NewGuid();
        var entity = new {Entity}(entityId, "Test");
        _repository.GetAsync(entityId).Returns(entity);

        // Act
        await _service.GetAsync(entityId);

        // Assert
        await _repository.Received(1).GetAsync(entityId);
    }

    [Fact]
    public async Task Should_Call_Repository_InsertAsync()
    {
        // Arrange
        var input = new Create{Entity}Dto { Name = "Test" };
        _repository.InsertAsync(Arg.Any<{Entity}>(), Arg.Any<bool>())
            .Returns(callInfo => callInfo.Arg<{Entity}>());

        // Act
        await _service.CreateAsync(input);

        // Assert
        await _repository.Received(1).InsertAsync(
            Arg.Is<{Entity}>(x => x.Name == "Test"),
            Arg.Any<bool>());
    }
}
```

## Authorization Tests

```csharp
[Fact]
public async Task CreateAsync_WithoutPermission_ThrowsAuthorizationException()
{
    // Arrange - login as user without create permission
    await WithUnitOfWorkAsync(async () =>
    {
        var input = new Create{Entity}Dto { Name = "Test" };

        // Act & Assert
        await Should.ThrowAsync<AbpAuthorizationException>(
            () => _{entity}AppService.CreateAsync(input));
    });
}

[Fact]
public async Task DeleteAsync_WithoutPermission_ThrowsAuthorizationException()
{
    // Arrange - login as user without delete permission
    await WithUnitOfWorkAsync(async () =>
    {
        // Act & Assert
        await Should.ThrowAsync<AbpAuthorizationException>(
            () => _{entity}AppService.DeleteAsync({Entity}TestData.{Entity}1Id));
    });
}
```
