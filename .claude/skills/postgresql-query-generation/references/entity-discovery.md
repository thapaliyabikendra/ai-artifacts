# Entity Discovery Reference

This document details how the PostgreSQL Query Generation skill discovers and analyzes domain entities.

## Discovery Process Overview

```
Step 1: Locate Entity Files
├── Search: src/*/Domain/Entities/**/*.cs
├── Pattern: public class X : FullAuditedAggregateRoot, etc.
└── Output: List of entity file paths

Step 2: Parse Each Entity
├── Extract: namespace, class name, base class
├── Parse: properties (name, type, nullable, attributes)
├── Detect: interfaces (IMultiTenant, ISoftDelete)
└── Build: EntityInfo object

Step 3: Build Relationship Graph
├── Find: FK properties (ending in "Id")
├── Match: {EntityName}Id to known entity
├── Detect: collection navigation properties
└── Identify: many-to-many join tables

Step 4: Infer Schema
├── Table names: Pluralize class name
├── Schema: Based on namespace
│   ├── "AbpIdentity" → AbpIdentity schema
│   └── Default → public
└── Column types: Map C# → PostgreSQL

Step 5: Generate Queries
├── Template: SELECT with auto-filled placeholders
├── Join: Based on relationship graph
├── Filter: TenantId, IsDeleted automatically
└── Optimize: Selective columns, proper indexes
```

## Entity Detection Patterns

The skill recognizes entities based on base classes:

| Pattern | Example | Notes |
|---------|---------|-------|
| `FullAuditedAggregateRoot<T>` | `public class Product : FullAuditedAggregateRoot<Guid>` | ABP standard |
| `AuditedAggregateRoot<T>` | `public class Category : AuditedAggregateRoot<Guid>` | Includes audit only |
| `AggregateRoot<T>` | `public class Tag : AggregateRoot<Guid>` | Minimal base |
| `SetupEntity` | `public class Country : SetupEntity` | ABP setup entities |
| `Entity<T>` | `public class Log : Entity<long>` | Plain EF Core |
| `IMultiTenant` | `public class Tenant : IMultiTenant, Entity<Guid>` | Interface detection |

### Custom Base Classes

The skill automatically discovers and inherits properties from **any** base class:

```csharp
// Extract properties from base classes automatically
public class DescriptiveEntityBase : Entity<Guid>
{
    public string Name { get; set; }
    public string Description { get; set; }
    public string Code { get; set; }
    public bool IsActive { get; set; }
}

// All derived entities inherit these properties
public class Application : DescriptiveEntityBase // Has Name, Description, Code, IsActive
{
    public string SystemName { get; set; }
    // Code inherits Name, Description, Code, IsActive automatically
}
```

## Property Parsing

### Recognized Property Patterns

```csharp
// Standard properties automatically detected
public Guid Id { get; set; }                        // PrimaryKey
public Guid? TenantId { get; set; }                 // Multi-tenancy
public bool IsDeleted { get; set; }                 // Soft delete
public string SystemName { get; set; }              // Regular column
public DateTime CreationTime { get; set; }          // Audit
public Guid? CreatorId { get; set; }                // Audit
public DateTime? LastModificationTime { get; set; } // Audit

// Foreign key detection (by naming convention)
public Guid ApplicationId { get; set; }             // FK → Application entity
public Guid? ParentId { get; set; }                 // Self-referencing FK
public int? StatusId { get; set; }                  // FK → Status entity

// Navigation properties
public virtual Application Application { get; set; }                   // ManyToOne
public virtual ICollection<WorkflowStage> WorkflowStages { get; set; } // OneToMany
```

### Type Mapping

| C# Type | PostgreSQL | Nullable | Notes |
|---------|------------|----------|-------|
| `Guid` | `UUID` | NO | Primary keys |
| `Guid?` | `UUID` | YES | Foreign keys |
| `int` | `INTEGER` | NO | Enums, counts |
| `int?` | `INTEGER` | YES | Optional int |
| `long` | `BIGINT` | NO | IDs > 2^31 |
| `string` | `VARCHAR(256)` | - | Adjust length from StringLength attr |
| `string` (long) | `TEXT` | - | > 256 chars or no attribute |
| `bool` | `BOOLEAN` | - | Flags |
| `DateTime` | `TIMESTAMPTZ` | - | With timezone |
| `decimal` | `NUMERIC` | - | Financial |
| `JObject`/`object` | `JSONB` | - | Structured data |
| `enum` | `INTEGER` | - | Enum stored as int |

**JSONB Fields** (PostgreSQL-specific):
- `FormData`, `JsonSchema`, `InitialData`, `Configuration`
- `OperationParameters`, `EventSourceConfiguration`
- `ImportConfig`, `ExportConfig`

## Relationship Detection

### Many-to-One (Child → Parent)

```csharp
// Child entity
public class Order
{
    public Guid ProductId { get; set; }        // FK
    public virtual Product Product { get; set; }  // Navigation
}
```

**Detected relationship:**
```
Order many-to-one Product
ON "Orders"."ProductId" = "Products"."Id"
```

### One-to-Many (Parent → Children)

```csharp
// Child entity
public class OrderItem
{
    public Guid OrderId { get; set; }
    public virtual Order Order { get; set; }
}

// Parent entity
public class Order
{
    public virtual ICollection<OrderItem> OrderItems { get; set; }  // Collection
}
```

**Detected relationship:**
```
Order one-to-many OrderItem
ON "OrderItems"."OrderId" = "Orders"."Id"
```

### Many-to-Many (via Join Table)

```csharp
// Join entity
public class OperationUserAccountType
{
    public Guid OperationId { get; set; }
    public Guid UserAccountTypeId { get; set; }

    public virtual Operation Operation { get; set; }
    public virtual UserAccountType UserAccountType { get; set; }
}

// Optional navigation properties
public class Operation
{
    public virtual ICollection<OperationUserAccountType> UserAccountTypes { get; set; }
}
```

**Detected relationship:**
```
Operation many-to-many UserAccountType
via OperationUserAccountType
ON Operation.Id = OperationUserAccountType.OperationId
AND UserAccountType.Id = OperationUserAccountType.UserAccountTypeId
```

### Self-Referencing (Hierarchical)

```csharp
public class Category
{
    public Guid? ParentId { get; set; }
    public virtual Category Parent { get; set; }
    public virtual ICollection<Category> Children { get; set; }
}
```

**Enables recursive CTE queries automatically.**

## Schema Inference

### Table Names

| Entity Class | Table Name |
|--------------|------------|
| `Application` | `Applications` |
| `WorkflowStage` | `WorkflowStages` |
| `OperationWorkflowInstance` | `OperationWorkflowInstances` |
| `DynamicForm` | `DynamicForms` |

**Rules:**
- Default: Pluralize class name (simple english rules)
- Override: `[Table("CustomName")]` attribute (not yet implemented)

### Schema Names

- Domain entities: `public`
- Identity: `AbpIdentity`
- Permission management: `PermissionManagement`
- Extracted from namespace where possible

### Column Names

- Property `SystemName` → Column `"SystemName"`
- Preserves casing (use quotes in PostgreSQL)
- Override: `[Column("CustomColumn")]` (not yet implemented)

## Discovery Output Format

```json
{
  "entities": {
    "Application": {
      "name": "Application",
      "namespace": "Amnil.Domain.Applications",
      "base_class": "FullAuditedAggregateRoot<Guid>",
      "table_name": "Applications",
      "schema": "public",
      "is_multi_tenant": true,
      "is_soft_delete": true,
      "properties": [
        {
          "name": "Id",
          "type": "Guid",
          "is_nullable": false,
          "is_primary_key": true,
          "is_foreign_key": false
        },
        {
          "name": "TenantId",
          "type": "Guid",
          "is_nullable": true,
          "is_foreign_key": false
        },
        {
          "name": "SystemName",
          "type": "string",
          "is_nullable": false,
          "is_foreign_key": false
        },
        {
          "name": "ApplicationTypeId",
          "type": "Guid",
          "is_nullable": true,
          "is_foreign_key": true,
          "referenced_entity": "ApplicationType"
        }
      ]
    }
  },
  "relationships": [
    {
      "source_entity": "Application",
      "target_entity": "ApplicationType",
      "relationship_type": "many-to-one",
      "source_fk": "ApplicationTypeId",
      "source_navigation": "ApplicationType"
    }
  ]
}
```

## Advanced Features

### Base Class Property Inheritance

Properties from base classes are **automatically** added to derived entities:

```csharp
// Base class
public abstract class DescriptiveEntityBase : Entity<Guid>
{
    public string Name { get; set; }
    public string Description { get; set; }
    public string Code { get; set; }
    public bool IsActive { get; set; }
}

// Derived
public class Product : DescriptiveEntityBase
{
    public decimal Price { get; set; }
}

// Skill discovers Product with properties: Id, Name, Description, Code, IsActive, Price
```

### Interface-Based Feature Detection

| Interface | Adds Filter |
|-----------|-------------|
| `IMultiTenant` | `TenantId = @tenantId` |
| `ISoftDelete` | `IsDeleted = false` |

Detected automatically - no configuration needed.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Entity not found | File not in scanned directories | Use correct directory structure |
| FK relationships missing | Navigation property not public | Ensure public/protected virtual |
| Wrong table name | Custom [Table] attribute not detected | Add custom naming logic |
| Missing properties | Base class not recognized | Check base class in Domain/Entities/Base/ |

## Caching

Discovery results are cached per-run. For long-running processes:
- Store schema JSON to disk
- Reload on subsequent queries within same session
- Invalidate when project files change

## See Also

- **[Query Patterns](query-patterns.md)** - Common SQL templates
- **[Type Mappings](type-mappings.md)** - Complete type conversion table
- **[Query Examples](query-examples.md)** - Real-world examples
