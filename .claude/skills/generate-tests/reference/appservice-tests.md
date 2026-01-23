# AppService Unit Tests

## Template

```csharp
using Shouldly;
using Xunit;
using NSubstitute;
using Volo.Abp;
using Volo.Abp.Domain.Entities;

namespace [Namespace].Tests;

public class [Class]Tests : [Module]ApplicationTestBase
{
    private readonly [Class] _sut;
    private readonly I[Repository] _repository;

    public [Class]Tests()
    {
        _repository = Substitute.For<I[Repository]>();
        _sut = new [Class](_repository);
    }

    [Fact]
    public async Task GetAsync_ValidId_ReturnsDto()
    {
        // Arrange
        var id = Guid.NewGuid();
        var entity = new [Entity] { Id = id, Name = "Test" };
        _repository.GetAsync(id).Returns(entity);

        // Act
        var result = await _sut.GetAsync(id);

        // Assert
        result.ShouldNotBeNull();
        result.Id.ShouldBe(id);
    }

    [Fact]
    public async Task GetAsync_NotFound_ThrowsEntityNotFoundException()
    {
        // Arrange
        _repository.GetAsync(Arg.Any<Guid>()).Returns((Entity)null);

        // Act & Assert
        await Should.ThrowAsync<EntityNotFoundException>(
            () => _sut.GetAsync(Guid.NewGuid()));
    }

    [Fact]
    public async Task CreateAsync_ValidInput_ReturnsDto()
    {
        // Arrange
        var input = new Create[Entity]Dto { Name = "Test" };
        _repository.InsertAsync(Arg.Any<[Entity]>(), true)
            .Returns(ci => ci.Arg<[Entity]>());

        // Act
        var result = await _sut.CreateAsync(input);

        // Assert
        result.ShouldNotBeNull();
        result.Name.ShouldBe("Test");
    }

    [Fact]
    public async Task CreateAsync_Duplicate_ThrowsBusinessException()
    {
        // Arrange
        var input = new Create[Entity]Dto { Name = "Existing" };
        _repository.AnyAsync(Arg.Any<Expression<Func<[Entity], bool>>>())
            .Returns(true);

        // Act & Assert
        var ex = await Should.ThrowAsync<BusinessException>(
            () => _sut.CreateAsync(input));
        ex.Code.ShouldBe("[Module]:Duplicate");
    }
}
```

## NSubstitute Patterns

```csharp
// Return value
_repo.GetAsync(id).Returns(entity);

// Capture input and return it
_repo.InsertAsync(Arg.Any<Entity>(), true).Returns(ci => ci.Arg<Entity>());

// Throw exception
_repo.GetAsync(Arg.Any<Guid>()).ThrowsAsync(new EntityNotFoundException(typeof(Entity), id));

// Verify call made
await _repo.Received(1).DeleteAsync(id);

// Verify call NOT made
await _repo.DidNotReceive().InsertAsync(Arg.Any<Entity>());
```

## Test Cases by Method

| Method | Test Cases |
|--------|------------|
| `GetAsync` | Valid ID → returns DTO, Invalid ID → throws `EntityNotFoundException` |
| `GetListAsync` | Returns paged result, Filters work |
| `CreateAsync` | Valid → creates, Invalid → validation error, Duplicate → business exception |
| `UpdateAsync` | Valid → updates, Not found → throws, Conflict → business exception |
| `DeleteAsync` | Valid → deletes, Not found → throws, In use → business exception |
