# {Feature} Feature Specification

> **Status**: Draft | In Review | Approved | Implemented
> **Created**: {Date}
> **Last Updated**: {Date}

## Overview

### Purpose
{Brief description of what this feature does and why it's needed}

### Scope
- **In Scope**: {What this feature includes}
- **Out of Scope**: {What this feature explicitly excludes}

---

## Business Rules

> **Reference**: See [docs/domain/business-rules.md](../../domain/business-rules.md#{feature-anchor})

{Link to the centralized business rules. Rules are maintained in business-rules.md, not duplicated here.}

**Applicable Rules**:
- BR-{CAT}-001: {Brief description}
- BR-{CAT}-002: {Brief description}

---

## Data Model

### Entity: {Entity}

| Property | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| `Id` | `Guid` | Yes | Primary Key | Unique identifier |
| `{Property}` | `{type}` | Yes/No | MaxLength({N}) | {Description} |
| `IsActive` | `bool` | Yes | Default: true | Active status |

**Base Class**: `FullAuditedAggregateRoot<Guid>`

### Relationships
- {Entity} → {RelatedEntity}: {Relationship type (1:N, N:1, etc.)}

---

## API Contract

### Endpoints

| Method | Route | Permission | Description | Response |
|--------|-------|------------|-------------|----------|
| GET | `/api/app/{entities}` | {Entity}s | List with pagination | `PagedResultDto<{Entity}Dto>` |
| GET | `/api/app/{entities}/{id}` | {Entity}s | Get by ID | `{Entity}Dto` |
| POST | `/api/app/{entities}` | {Entity}s.Create | Create new | `{Entity}Dto` |
| PUT | `/api/app/{entities}/{id}` | {Entity}s.Edit | Update existing | `{Entity}Dto` |
| DELETE | `/api/app/{entities}/{id}` | {Entity}s.Delete | Soft delete | `204 No Content` |

### DTOs

**Output DTO** (`{Entity}Dto`):
```csharp
public class {Entity}Dto : FullAuditedEntityDto<Guid>
{
    public {type} {Property} { get; set; }
    public bool IsActive { get; set; }
}
```

**Create Input** (`Create{Entity}Dto`):
```csharp
public class Create{Entity}Dto
{
    public {type} {Property} { get; set; }
}
```

**Update Input** (`Update{Entity}Dto`):
```csharp
public class Update{Entity}Dto
{
    public {type} {Property} { get; set; }
}
```

**Filter Input** (`Get{Entity}sInput`):
```csharp
public class Get{Entity}sInput : PagedAndSortedResultRequestDto
{
    public string? Filter { get; set; }
    public bool? IsActive { get; set; }
}
```

---

## Permissions

| Permission | Display Name | Roles |
|------------|--------------|-------|
| `{ProjectName}.{Entity}s` | View {Entity}s | Admin, User |
| `{ProjectName}.{Entity}s.Create` | Create {Entity}s | Admin |
| `{ProjectName}.{Entity}s.Edit` | Edit {Entity}s | Admin |
| `{ProjectName}.{Entity}s.Delete` | Delete {Entity}s | Admin |

---

## Test Coverage

### Test Categories

| Category | Test Scenarios |
|----------|----------------|
| **Happy Path** | Create with valid data, Get existing, Update existing, Delete existing, List with pagination |
| **Validation** | Empty required fields, Max length exceeded, Invalid formats |
| **Authorization** | Access without permission, Access with correct permission |
| **Edge Cases** | Get non-existent, Empty list, Concurrent updates |

### Key Test Scenarios

1. **Create {Entity} - Valid Data**: Should create and return DTO with ID
2. **Create {Entity} - Empty Name**: Should throw `AbpValidationException`
3. **Get {Entity} - Not Found**: Should throw `EntityNotFoundException`
4. **List {Entity}s - With Filter**: Should return filtered results
5. **Delete {Entity}** - Should soft delete (IsDeleted=true)

---

## Implementation Notes

### Technical Decisions
- {Any architectural decisions or trade-offs}

### Dependencies
- {Other features or services this depends on}

### Migration Notes
- {Database migration considerations}

---

## User Stories

### US-{NNN}: {Story Title}

**As a** {role}
**I want to** {action}
**So that** {benefit}

**Acceptance Criteria**:
- [ ] Given {precondition}, When {action}, Then {expected result}
- [ ] Given {precondition}, When {action}, Then {expected result}
