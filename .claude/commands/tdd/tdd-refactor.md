---
description: Refactor code while keeping tests green for ABP/.NET
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "<feature-or-component>"
---

# TDD Refactor Phase - Improve Code Quality

Refactor implementation while maintaining green tests.

**Arguments**: $ARGUMENTS

## Execution

Use Task tool with `subagent_type="code-reviewer"`:

```
Refactor implementation for: {feature-or-component}

Context: Read implementation and tests
Skills: Apply code-review-excellence, abp-framework-patterns

## Pre-Assessment

1. Run tests - confirm all green
2. Identify code smells
3. Document current metrics
4. Plan incremental changes

## Code Smell Detection

| Smell | Refactoring |
|-------|-------------|
| Duplicated code | Extract method/class |
| Long method | Decompose into focused methods |
| Large class | Split responsibilities |
| Long parameter list | Parameter object/DTO |
| Feature Envy | Move to appropriate class |
| Primitive Obsession | Value objects |

## SOLID Principles

- **S**: One reason to change per class
- **O**: Open for extension, closed for modification
- **L**: Subtypes substitutable for base types
- **I**: Small, focused interfaces
- **D**: Depend on abstractions

## ABP-Specific Refactoring

**Extract Domain Service:**
```csharp
// Before: Logic in AppService
public async Task<PatientDto> CreateAsync(CreatePatientDto input)
{
    // Validation logic here
    // Business rules here
    // Entity creation here
}

// After: Domain service
public async Task<PatientDto> CreateAsync(CreatePatientDto input)
{
    var patient = await _patientManager.CreateAsync(
        input.FirstName,
        input.LastName,
        input.Email
    );
    return ObjectMapper.Map<Patient, PatientDto>(patient);
}
```

**Extract Specification:**
```csharp
// Before: Query in AppService
var patients = await _patientRepository.GetListAsync(
    p => p.Status == Status.Active && p.DoctorId == doctorId
);

// After: Specification
var patients = await _patientRepository.GetListAsync(
    new ActivePatientsForDoctorSpecification(doctorId)
);
```

## Incremental Steps

1. Make ONE small change
2. Run tests
3. If green, commit
4. If red, revert immediately
5. Repeat

## Safety Checklist

Before each commit:
- [ ] All tests pass
- [ ] No functionality regression
- [ ] Code coverage maintained
- [ ] Build succeeds

## Metrics to Track

- Cyclomatic complexity (target: <10)
- Method length (target: <20 lines)
- Class length (target: <200 lines)
- Duplicate code blocks

## Recovery Protocol

If tests fail:
1. Immediately revert last change
2. Identify breaking refactoring
3. Apply smaller incremental change
4. Use git stash for experiments
```

**Checkpoint**: All tests pass. Code quality improved.

---

Code to refactor: $ARGUMENTS
