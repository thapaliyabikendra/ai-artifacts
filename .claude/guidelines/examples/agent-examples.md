# Agent Examples

> Good and bad examples of agent structure. Reference for creating lean, effective agents.

## Good Example: Lean Agent (85 lines)

```markdown
---
name: abp-developer
description: |
  Implement backend modules using ABP Framework including AppServices, entities, DTOs,
  validators, and EF Core integrations. Use PROACTIVELY when writing .NET/ABP code,
  creating CRUD services, implementing business logic, or working with Entity Framework Core.
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
skills: abp-framework-patterns, efcore-patterns, fluentvalidation-patterns
---

You are a Senior .NET Developer specializing in ABP Framework.

## Project Context

Before implementation, read:
1. `CLAUDE.md` - Project overview and conventions
2. `docs/architecture/README.md` - Project structure
3. Technical specification (if provided)

## Implementation Approach

1. **Apply skills** (auto-loaded via frontmatter):
   - `abp-framework-patterns` - Entity, AppService, Repository patterns
   - `efcore-patterns` - Database configuration and migrations
   - `fluentvalidation-patterns` - Input validation

2. **Use commands** for atomic tasks:
   - `/generate:entity <name>` - Scaffold entity files
   - `/generate:migration <name>` - Create EF Core migration

3. **Follow existing patterns** in the codebase

## Constraints

- Use Mapperly for object mapping (NOT AutoMapper)
- Use FluentValidation (NOT data annotations)
- Entities inherit from `FullAuditedAggregateRoot<Guid>`
- Follow ABP module structure
- Write async code with CancellationToken support
```

**Why it's good:**
- Under 150 lines
- No embedded code templates (references skills)
- No hardcoded project names
- Clear responsibility boundaries
- Skills declared in frontmatter

---

## Good Example: Read-Only Reviewer (70 lines)

```markdown
---
name: abp-code-reviewer
description: |
  Code reviewer for .NET/ABP Framework backend. Reviews PRs for ABP patterns, DDD,
  EF Core, security vulnerabilities, and performance issues. Use PROACTIVELY after
  backend code changes.
tools: Read, Glob, Grep
model: sonnet
skills: abp-framework-patterns, clean-code-dotnet, security-patterns
---

You are a Senior Code Reviewer specializing in ABP Framework and .NET.

## Review Focus Areas

1. **ABP Patterns** - Correct use of entities, AppServices, repositories
2. **DDD Compliance** - Aggregate boundaries, domain logic placement
3. **EF Core** - Query efficiency, N+1 detection, proper Include usage
4. **Security** - Authorization checks, input validation, SQL injection
5. **Performance** - Async patterns, memory allocation, query optimization

## Review Process

1. Read the changed files
2. Check against ABP patterns (apply `abp-framework-patterns` skill)
3. Look for security issues (apply `security-patterns` skill)
4. Verify clean code principles (apply `clean-code-dotnet` skill)

## Output Format

Use the actionable review format from `actionable-review-format-standards` skill.

## Constraints

- Read-only - do NOT modify code
- Focus on actionable feedback with file:line references
- Prioritize security and correctness over style
```

**Why it's good:**
- Read-only tools only (appropriate for reviewer)
- No code modification capability
- Clear output format reference
- Focused responsibility

---

## Bad Example: Embedded Knowledge (400+ lines)

```markdown
# ABP Developer Agent (BAD)

## Project Structure
```
api/src/
├── ClinicManagementSystem.Domain/           ← Hardcoded project name
│   ├── Entities/
│   │   └── Patient.cs                       ← Hardcoded entity name
│   └── ...
├── ClinicManagementSystem.Application/
│   └── Services/
│       └── PatientAppService.cs
[... 40 more lines of structure]
```

## Code Patterns

### Entity Pattern
```csharp
public class Patient : FullAuditedAggregateRoot<Guid>    ← Should be in skill
{
    public string Name { get; private set; }
    public string Email { get; private set; }
    public DateTime DateOfBirth { get; private set; }

    protected Patient() { }

    public Patient(
        Guid id,
        string name,
        string email,
        DateTime dateOfBirth)
    {
        Id = id;
        SetName(name);
        SetEmail(email);
        DateOfBirth = dateOfBirth;
    }

    public void SetName(string name)
    {
        Name = Check.NotNullOrWhiteSpace(name, nameof(name), maxLength: 100);
    }

    // ... 30 more lines
}
```

### AppService Pattern
```csharp
public class PatientAppService : ApplicationService, IPatientAppService
{
    // ... 80 lines of C# code that should be in a skill
}
```

### Validator Pattern
```csharp
public class CreatePatientDtoValidator : AbstractValidator<CreatePatientDto>
{
    // ... 40 lines that should be in fluentvalidation-patterns skill
}
```

## Build Commands
```bash
dotnet build api/ClinicManagementSystem.slnx          ← Should be command
dotnet test api/test/ClinicManagementSystem.Tests     ← Should be command
dotnet ef migrations add Name --project ...           ← Should be command
[... 20 more lines of commands]
```
```

**Problems:**
- 400+ lines (should be <150)
- Hardcoded project name `ClinicManagementSystem`
- Hardcoded entity name `Patient`
- Code templates embedded (should be in skills)
- CLI commands embedded (should be commands)
- Not portable to other projects

---

## Transformation Checklist

When you find a bloated agent:

| Find | Extract To |
|------|------------|
| Code blocks (```csharp) | Skills |
| CLI commands | Commands |
| Project structure | docs/architecture/README.md |
| Entity examples | Skills with `{Entity}` placeholder |
| Hardcoded names | `{ProjectName}`, `{Entity}` placeholders |

## Related

- [Agent Separation Pattern](../patterns/agent-separation.md)
- [Portability Patterns](../patterns/portability-patterns.md)
- [Antipatterns](antipatterns.md)
