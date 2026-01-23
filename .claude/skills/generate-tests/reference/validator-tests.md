# Validator Unit Tests

## Template

```csharp
using FluentValidation.TestHelper;
using Xunit;

namespace [Namespace].Tests;

public class [Validator]Tests
{
    private readonly [Validator] _validator = new();

    [Fact]
    public void Validate_ValidModel_Passes()
    {
        var model = new [Dto] { Name = "Valid", Email = "valid@example.com" };
        _validator.TestValidate(model).ShouldNotHaveAnyValidationErrors();
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void Name_Empty_Fails(string value)
    {
        var model = new [Dto] { Name = value };
        _validator.TestValidate(model).ShouldHaveValidationErrorFor(x => x.Name);
    }

    [Fact]
    public void Name_TooLong_Fails()
    {
        var model = new [Dto] { Name = new string('x', 256) };
        _validator.TestValidate(model)
            .ShouldHaveValidationErrorFor(x => x.Name)
            .WithErrorMessage("*maximum length*");
    }

    [Theory]
    [InlineData("invalid")]
    [InlineData("@example.com")]
    [InlineData("test@")]
    public void Email_InvalidFormat_Fails(string value)
    {
        var model = new [Dto] { Email = value };
        _validator.TestValidate(model).ShouldHaveValidationErrorFor(x => x.Email);
    }
}
```

## Rule to Test Mapping

| FluentValidation Rule | Test Values |
|-----------------------|-------------|
| `.NotEmpty()` | `null`, `""`, `"   "` |
| `.NotNull()` | `null` |
| `.MaximumLength(n)` | String of length `n+1` |
| `.MinimumLength(n)` | String of length `n-1` |
| `.EmailAddress()` | `"invalid"`, `"@x.com"`, `"x@"` |
| `.GreaterThan(0)` | `0`, `-1` |
| `.InclusiveBetween(a,b)` | `a-1`, `b+1` |

## Conditional Validation

```csharp
// When IsRecurring is true, EndDate is required
[Fact]
public void EndDate_Required_WhenIsRecurring()
{
    var model = new [Dto] { IsRecurring = true, EndDate = null };
    _validator.TestValidate(model).ShouldHaveValidationErrorFor(x => x.EndDate);
}

[Fact]
public void EndDate_NotRequired_WhenNotRecurring()
{
    var model = new [Dto] { IsRecurring = false, EndDate = null };
    _validator.TestValidate(model).ShouldNotHaveValidationErrorFor(x => x.EndDate);
}
```
