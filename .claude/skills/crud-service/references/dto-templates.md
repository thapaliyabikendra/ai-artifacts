# DTO Templates

## Table of Contents
- [EntityDto](#entitydto)
- [CreateUpdateDto](#createupdatedto)
- [ResponseDto](#responsedto)
- [Filter](#filter)

## EntityDto

File: `{EntityName}Dto.cs`

```csharp
using System;

namespace {Namespace}.{EntityNamePlural};

public class {EntityName}Dto
{
    public Guid Id { get; set; }
    // Add entity properties here
}
```

## CreateUpdateDto

File: `CreateUpdate{EntityName}Dto.cs`

```csharp
using System;

namespace {Namespace}.{EntityNamePlural};

public class CreateUpdate{EntityName}Dto
{
    // Add entity properties here (without Id)
}
```

## ResponseDto

File: `{EntityName}ResponseDto.cs`

```csharp
using System;

namespace {Namespace}.{EntityNamePlural};

public class {EntityName}ResponseDto
{
    public Guid Id { get; set; }
}
```

## Filter

File: `{EntityName}Filter.cs`

```csharp
namespace {Namespace}.{EntityNamePlural};

public class {EntityName}Filter
{
    public string SearchKeyword { get; set; }
    // Add additional filter properties based on entity fields
}
```

## Property Mapping Guide

When adding properties to DTOs, follow these patterns:

| Property Type | DTO Example |
|---------------|-------------|
| string | `public string Name { get; set; }` |
| int | `public int Quantity { get; set; }` |
| decimal | `public decimal Price { get; set; }` |
| bool | `public bool IsActive { get; set; }` |
| DateTime | `public DateTime CreatedAt { get; set; }` |
| Guid (FK) | `public Guid CategoryId { get; set; }` |
| Nullable | `public decimal? Discount { get; set; }` |

For related entity display names, add to `{EntityName}Dto`:
```csharp
public string CategoryName { get; set; }  // From join with Category
```
