# Refactoring Patterns Reference

SOLID principles, code smells catalog, and refactoring decision frameworks for C#/.NET and React/TypeScript.

> **See also**: `clean-code-dotnet` skill for comprehensive clean code patterns.

## SOLID Principles Examples

### Single Responsibility Principle (SRP)

```csharp
// ❌ BEFORE: Multiple responsibilities
class UserManager
{
    public async Task CreateUserAsync(CreateUserDto data)
    {
        // Validate, save, email, log, cache - all mixed
        if (string.IsNullOrEmpty(data.Email)) throw new Exception();
        await _dbContext.Users.AddAsync(new User(data));
        await _emailService.SendWelcomeEmail(data.Email);
        _logger.LogInformation("User created");
    }
}

// ✅ AFTER: Separated concerns
class UserValidator : AbstractValidator<CreateUserDto> { }
class UserRepository : IUserRepository { }
class WelcomeEmailSender : IWelcomeEmailSender { }

class UserAppService : ApplicationService
{
    private readonly IUserRepository _repository;
    private readonly IWelcomeEmailSender _emailSender;

    public async Task<UserDto> CreateAsync(CreateUserDto input)
    {
        var user = await _repository.InsertAsync(new User(input));
        await _emailSender.SendAsync(user.Email);
        return ObjectMapper.Map<User, UserDto>(user);
    }
}
```

### Open/Closed Principle (OCP)

```csharp
// ❌ BEFORE: Modification required for new types
class DiscountCalculator
{
    public decimal Calculate(Order order, string discountType)
    {
        if (discountType == "percentage") return order.Total * 0.1m;
        else if (discountType == "fixed") return 10m;
        // Must add more else-if for new discount types!
        return 0;
    }
}

// ✅ AFTER: Open for extension, closed for modification
interface IDiscountStrategy
{
    decimal Calculate(Order order);
}

class PercentageDiscount : IDiscountStrategy
{
    private readonly decimal _percentage;
    public PercentageDiscount(decimal percentage) => _percentage = percentage;
    public decimal Calculate(Order order) => order.Total * _percentage;
}

class FixedDiscount : IDiscountStrategy
{
    private readonly decimal _amount;
    public FixedDiscount(decimal amount) => _amount = amount;
    public decimal Calculate(Order order) => _amount;
}

class DiscountCalculator
{
    public decimal Calculate(Order order, IDiscountStrategy strategy)
        => strategy.Calculate(order);
}
```

### Liskov Substitution Principle (LSP)

```csharp
// ❌ BEFORE: Violates LSP
class Rectangle
{
    public virtual void SetWidth(double width) => Width = width;
    public virtual void SetHeight(double height) => Height = height;
}

class Square : Rectangle
{
    public override void SetWidth(double width)
    {
        Width = Height = width; // Breaks expectations!
    }
}

// ✅ AFTER: Proper abstraction
abstract class Shape
{
    public abstract double GetArea();
}

class Rectangle : Shape
{
    public double Width { get; set; }
    public double Height { get; set; }
    public override double GetArea() => Width * Height;
}

class Square : Shape
{
    public double Side { get; set; }
    public override double GetArea() => Side * Side;
}
```

### Interface Segregation Principle (ISP)

```csharp
// ❌ BEFORE: Fat interface
interface IEmployee
{
    void Work();
    void Eat();
    void Sleep();
}

class Robot : IEmployee
{
    public void Work() { /* ok */ }
    public void Eat() => throw new NotImplementedException(); // Robot can't eat!
    public void Sleep() => throw new NotImplementedException();
}

// ✅ AFTER: Segregated interfaces
interface IWorkable { void Work(); }
interface IFeedable { void Eat(); }

class Human : IWorkable, IFeedable
{
    public void Work() { }
    public void Eat() { }
}

class Robot : IWorkable
{
    public void Work() { }
}
```

### Dependency Inversion Principle (DIP)

```csharp
// ❌ BEFORE: Tight coupling
class UserService
{
    private readonly MySqlDatabase _db = new(); // Concrete dependency!
}

// ✅ AFTER: Depends on abstraction
interface IDatabase
{
    Task SaveAsync<T>(T entity);
}

class UserService
{
    private readonly IDatabase _db;

    public UserService(IDatabase db) // Injected
    {
        _db = db;
    }
}

// Registration in ABP Module
context.Services.AddTransient<IDatabase, PostgreSqlDatabase>();
```

---

## Code Smells Catalog (C#)

### Long Parameter List

```csharp
// ❌ BEFORE
public void CreateUser(string firstName, string lastName, string email,
    string phone, string address, string city, string state, string zip) { }

// ✅ AFTER: Parameter Object
public record CreateUserDto(
    string FirstName,
    string LastName,
    string Email,
    AddressDto Address);

public async Task CreateUserAsync(CreateUserDto input) { }
```

### Feature Envy

```csharp
// ❌ BEFORE: Method uses another class's data
class Order
{
    public decimal CalculateShipping(Customer customer)
    {
        return customer.IsPremium ? 0
            : customer.Address.IsInternational ? 20 : 10;
    }
}

// ✅ AFTER: Move to appropriate class
class Customer
{
    public decimal CalculateShippingCost()
    {
        return IsPremium ? 0 : Address.IsInternational ? 20 : 10;
    }
}
```

### Primitive Obsession

```csharp
// ❌ BEFORE: Raw primitives
string userEmail = "test@example.com";

// ✅ AFTER: Value Object
public record Email
{
    public string Value { get; }

    public Email(string email)
    {
        if (!IsValid(email))
            throw new BusinessException("Invalid email");
        Value = email;
    }

    private static bool IsValid(string email)
        => Regex.IsMatch(email, @"^[^\s@]+@[^\s@]+\.[^\s@]+$");
}
```

### Magic Strings/Numbers

```csharp
// ❌ BEFORE
if (user.Role == "admin") { }
if (retryCount > 3) { }

// ✅ AFTER
public enum UserRole { Admin, User, Guest }
private const int MaxRetries = 3;

if (user.Role == UserRole.Admin) { }
if (retryCount > MaxRetries) { }
```

---

## Clean Code Checklist

> Reference: `clean-code-dotnet` skill

### Naming
- [ ] Meaningful, pronounceable names
- [ ] No Hungarian notation (`strName`, `iCount`)
- [ ] Domain terms used appropriately

### Functions
- [ ] Single responsibility
- [ ] <3 parameters (use DTOs for more)
- [ ] No flag parameters
- [ ] No side effects
- [ ] Guard clauses / early returns

### Classes
- [ ] <200 lines
- [ ] Single responsibility
- [ ] Composition over inheritance

### Error Handling
- [ ] No `throw ex` (use `throw`)
- [ ] No silent catch blocks
- [ ] Specific exception types

### Comments
- [ ] No commented-out code
- [ ] No `#region` blocks
- [ ] Explains WHY, not WHAT

---

## Quality Metrics

| Metric | Good | Warning | Critical | Action |
|--------|------|---------|----------|--------|
| Cyclomatic Complexity | <10 | 10-15 | >15 | Split into smaller methods |
| Method Lines | <20 | 20-50 | >50 | Extract methods |
| Class Lines | <200 | 200-500 | >500 | Decompose into classes |
| Test Coverage | >80% | 60-80% | <60% | Add unit tests |
| Code Duplication | <3% | 3-5% | >5% | Extract common code |
| Parameter Count | ≤3 | 4-5 | >5 | Use DTO |

---

## Decision Tree

```
Is it causing production bugs?
├─ YES → Priority: CRITICAL (Fix immediately)
└─ NO → Is it blocking new features?
    ├─ YES → Priority: HIGH (Schedule this sprint)
    └─ NO → Is it frequently modified?
        ├─ YES → Priority: MEDIUM (Next quarter)
        └─ NO → Priority: LOW (Backlog)
```

---

## Static Analysis (.NET)

```xml
<!-- .editorconfig -->
<!-- See clean-code-dotnet/references/editorconfig-template.md -->

<!-- Directory.Build.props -->
<PropertyGroup>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  <AnalysisLevel>latest</AnalysisLevel>
  <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
</PropertyGroup>
```

---

## Quality Checklist

- [ ] All methods < 20 lines
- [ ] All classes < 200 lines
- [ ] No method has > 3 parameters
- [ ] Cyclomatic complexity < 10
- [ ] No nested loops > 2 levels
- [ ] All names are descriptive
- [ ] No commented-out code
- [ ] Async/await used correctly
- [ ] Tests achieve > 80% coverage
