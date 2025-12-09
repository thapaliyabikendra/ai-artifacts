# Validator Template

File: `{EntityName}Validator.cs`

```csharp
using FluentValidation;
using {Namespace}.{EntityNamePlural};

namespace {Namespace}.Validators;

public class {EntityName}Validator : AbstractValidator<CreateUpdate{EntityName}Dto>
{
    public {EntityName}Validator()
    {
        // Add validation rules here
    }
}
```

## Common Validation Rules

### String Properties
```csharp
RuleFor(x => x.Name)
    .NotEmpty().WithMessage("Name is required.")
    .MaximumLength(100).WithMessage("Name cannot exceed 100 characters.");

RuleFor(x => x.Email)
    .NotEmpty().WithMessage("Email is required.")
    .EmailAddress().WithMessage("Invalid email format.");

RuleFor(x => x.Code)
    .NotEmpty().WithMessage("Code is required.")
    .Matches("^[A-Z0-9]+$").WithMessage("Code must contain only uppercase letters and numbers.");
```

### Numeric Properties
```csharp
RuleFor(x => x.Price)
    .GreaterThan(0).WithMessage("Price must be greater than zero.");

RuleFor(x => x.Quantity)
    .InclusiveBetween(1, 1000).WithMessage("Quantity must be between 1 and 1000.");

RuleFor(x => x.Discount)
    .InclusiveBetween(0, 100).WithMessage("Discount must be between 0 and 100.")
    .When(x => x.Discount.HasValue);
```

### Guid/Foreign Key Properties
```csharp
RuleFor(x => x.CategoryId)
    .NotEmpty().WithMessage("Category is required.");
```

### Date Properties
```csharp
RuleFor(x => x.StartDate)
    .NotEmpty().WithMessage("Start date is required.")
    .LessThan(x => x.EndDate).WithMessage("Start date must be before end date.")
    .When(x => x.EndDate.HasValue);
```

### Conditional Validation
```csharp
RuleFor(x => x.AlternateEmail)
    .EmailAddress().WithMessage("Invalid alternate email format.")
    .When(x => !string.IsNullOrEmpty(x.AlternateEmail));
```

## DI Registration

Register the validator in your module:

```csharp
context.Services.AddTransient<IValidator<CreateUpdate{EntityName}Dto>, {EntityName}Validator>();
```

Or use assembly scanning:

```csharp
context.Services.AddValidatorsFromAssemblyContaining<{EntityName}Validator>();
```
