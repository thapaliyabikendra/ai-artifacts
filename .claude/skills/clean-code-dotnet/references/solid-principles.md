# SOLID Principles - Complete Examples

## Single Responsibility Principle (SRP)

> "There should never be more than one reason for a class to change."

### Problem

```csharp
// ❌ Bad - Multiple responsibilities
class UserSettings
{
    private User User;

    public UserSettings(User user)
    {
        User = user;
    }

    public void ChangeSettings(Settings settings)
    {
        if (VerifyCredentials())
        {
            // Change settings
        }
    }

    private bool VerifyCredentials()
    {
        // Authentication logic - DIFFERENT responsibility!
    }
}
```

### Solution

```csharp
// ✅ Good - Separated responsibilities
class UserAuth
{
    private User User;

    public UserAuth(User user)
    {
        User = user;
    }

    public bool VerifyCredentials()
    {
        // Authentication logic
    }
}

class UserSettings
{
    private User User;
    private UserAuth Auth;

    public UserSettings(User user)
    {
        User = user;
        Auth = new UserAuth(user);
    }

    public void ChangeSettings(Settings settings)
    {
        if (Auth.VerifyCredentials())
        {
            // Change settings
        }
    }
}
```

---

## Open/Closed Principle (OCP)

> "Software entities should be open for extension, but closed for modification."

### Problem

```csharp
// ❌ Bad - Must modify class to add new adapter
class HttpRequester
{
    private readonly AdapterBase Adapter;

    public HttpRequester(AdapterBase adapter)
    {
        Adapter = adapter;
    }

    public bool Fetch(string url)
    {
        var adapterName = Adapter.GetName();

        if (adapterName == "ajaxAdapter")
        {
            return MakeAjaxCall(url);
        }
        else if (adapterName == "httpNodeAdapter")
        {
            return MakeHttpCall(url);
        }
        // Adding new adapter requires modifying this class!
    }

    private bool MakeAjaxCall(string url) { /* ... */ }
    private bool MakeHttpCall(string url) { /* ... */ }
}
```

### Solution

```csharp
// ✅ Good - Open for extension, closed for modification
interface IAdapter
{
    bool Request(string url);
}

class AjaxAdapter : IAdapter
{
    public bool Request(string url)
    {
        // Ajax implementation
    }
}

class NodeAdapter : IAdapter
{
    public bool Request(string url)
    {
        // Node implementation
    }
}

// New adapter - no modification to HttpRequester needed!
class FetchAdapter : IAdapter
{
    public bool Request(string url)
    {
        // Fetch implementation
    }
}

class HttpRequester
{
    private readonly IAdapter Adapter;

    public HttpRequester(IAdapter adapter)
    {
        Adapter = adapter;
    }

    public bool Fetch(string url)
    {
        return Adapter.Request(url);
    }
}
```

---

## Liskov Substitution Principle (LSP)

> "Objects of a superclass should be replaceable with objects of its subclasses without breaking the application."

### Problem

```csharp
// ❌ Bad - Square violates Rectangle contract
class Rectangle
{
    protected double Width = 0;
    protected double Height = 0;

    public virtual void SetWidth(double width)
    {
        Width = width;
    }

    public virtual void SetHeight(double height)
    {
        Height = height;
    }

    public double GetArea()
    {
        return Width * Height;
    }
}

class Square : Rectangle
{
    public override void SetWidth(double width)
    {
        Width = Height = width;  // Violates expectations!
    }

    public override void SetHeight(double height)
    {
        Width = Height = height;  // Violates expectations!
    }
}

// This breaks!
void RenderLargeRectangles(Rectangle[] rectangles)
{
    foreach (var rectangle in rectangles)
    {
        rectangle.SetWidth(4);
        rectangle.SetHeight(5);
        var area = rectangle.GetArea();
        // BAD: Returns 25 for Square, should be 20!
    }
}
```

### Solution

```csharp
// ✅ Good - Proper abstraction
abstract class Shape
{
    public abstract double GetArea();
    public void Render(double area) { /* ... */ }
}

class Rectangle : Shape
{
    private double Width;
    private double Height;

    public void SetWidth(double width) => Width = width;
    public void SetHeight(double height) => Height = height;

    public override double GetArea() => Width * Height;
}

class Square : Shape
{
    private double Length;

    public void SetLength(double length) => Length = length;

    public override double GetArea() => Length * Length;
}

// Each shape handles its own behavior correctly
void RenderShapes(Shape[] shapes)
{
    foreach (var shape in shapes)
    {
        var area = shape.GetArea();
        shape.Render(area);
    }
}
```

---

## Interface Segregation Principle (ISP)

> "Clients should not be forced to depend upon interfaces they do not use."

### Problem

```csharp
// ❌ Bad - Fat interface
public interface IEmployee
{
    void Work();
    void Eat();
}

public class Human : IEmployee
{
    public void Work()
    {
        // Working
    }

    public void Eat()
    {
        // Eating lunch
    }
}

public class Robot : IEmployee
{
    public void Work()
    {
        // Working
    }

    public void Eat()
    {
        // Robot can't eat! But must implement
        throw new NotImplementedException();
    }
}
```

### Solution

```csharp
// ✅ Good - Segregated interfaces
public interface IWorkable
{
    void Work();
}

public interface IFeedable
{
    void Eat();
}

public interface IEmployee : IFeedable, IWorkable
{
}

public class Human : IEmployee
{
    public void Work()
    {
        // Working
    }

    public void Eat()
    {
        // Eating lunch
    }
}

// Robot only implements what it needs
public class Robot : IWorkable
{
    public void Work()
    {
        // Working
    }
}
```

---

## Dependency Inversion Principle (DIP)

> "High-level modules should not depend on low-level modules. Both should depend on abstractions."

### Problem

```csharp
// ❌ Bad - Depends on concrete types
public class Human : EmployeeBase
{
    public override void Work()
    {
        // Working
    }
}

public class Robot : EmployeeBase
{
    public override void Work()
    {
        // Working harder
    }
}

public class Manager
{
    private readonly Robot _robot;  // Concrete dependency!
    private readonly Human _human;  // Concrete dependency!

    public Manager(Robot robot, Human human)
    {
        _robot = robot;
        _human = human;
    }

    public void Manage()
    {
        _robot.Work();
        _human.Work();
    }
}
```

### Solution

```csharp
// ✅ Good - Depends on abstractions
public interface IEmployee
{
    void Work();
}

public class Human : IEmployee
{
    public void Work()
    {
        // Working
    }
}

public class Robot : IEmployee
{
    public void Work()
    {
        // Working harder
    }
}

public class Manager
{
    private readonly IEnumerable<IEmployee> _employees;

    public Manager(IEnumerable<IEmployee> employees)
    {
        _employees = employees;
    }

    public void Manage()
    {
        foreach (var employee in _employees)
        {
            employee.Work();
        }
    }
}

// Registration (in ABP module)
context.Services.AddTransient<IEmployee, Human>();
context.Services.AddTransient<IEmployee, Robot>();
```

---

## DRY (Don't Repeat Yourself)

### Problem

```csharp
// ❌ Bad - Duplicate code
public List<EmployeeData> ShowDeveloperList(Developer[] developers)
{
    foreach (var developer in developers)
    {
        var expectedSalary = developer.CalculateExpectedSalary();
        var experience = developer.GetExperience();
        var githubLink = developer.GetGithubLink();
        Render(new[] { expectedSalary, experience, githubLink });
    }
}

public List<EmployeeData> ShowManagerList(Manager[] managers)
{
    foreach (var manager in managers)
    {
        var expectedSalary = manager.CalculateExpectedSalary();
        var experience = manager.GetExperience();
        var githubLink = manager.GetGithubLink();
        Render(new[] { expectedSalary, experience, githubLink });
    }
}
```

### Solution

```csharp
// ✅ Good - Single abstraction
public List<EmployeeData> ShowList(IEmployee[] employees)
{
    foreach (var employee in employees)
    {
        Render(new[]
        {
            employee.CalculateExpectedSalary(),
            employee.GetExperience(),
            employee.GetGithubLink()
        });
    }
}
```
