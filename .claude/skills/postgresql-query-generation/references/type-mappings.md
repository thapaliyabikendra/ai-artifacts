# Type Mappings Reference

Complete mapping from C# types to PostgreSQL types for the query generator.

## Direct Type Mappings

| C# Type | PostgreSQL Type | Nullable | Notes |
|---------|-----------------|----------|-------|
| `Guid` | `UUID` | NO | Primary keys |
| `Guid?` | `UUID` | YES | Foreign keys |
| `int` | `INTEGER` | NO | Enums, counts, order |
| `int?` | `INTEGER` | YES | Optional int |
| `long` | `BIGINT` | NO | Big IDs |
| `long?` | `BIGINT` | YES | Optional long |
| `short` | `SMALLINT` | NO | Small ints |
| `byte` | `SMALLINT` | NO | Byte values |
| `bool` | `BOOLEAN` | NO | True/False |
| `bool?` | `BOOLEAN` | YES | Optional boolean |
| `DateTime` | `TIMESTAMPTZ` | NO | With timezone |
| `DateTime?` | `TIMESTAMPTZ` | YES | Nullable timestamp |
| `decimal` | `NUMERIC` | NO | Financial (unlimited precision) |
| `decimal?` | `NUMERIC` | YES | Optional decimal |
| `double` | `DOUBLE PRECISION` | NO | Double precision float |
| `double?` | `DOUBLE PRECISION` | YES | Optional double |
| `float` | `REAL` | NO | Single precision |
| `float?` | `REAL` | YES | Optional float |
| `string` | `VARCHAR(256)` | - | See String Length below |
| `string` (long) | `TEXT` | - | >256 or unspecified |
| `JObject` or `object` | `JSONB` | - | Structured data |
| `JsonDocument` | `JSONB` | - | .NET System.Text.Json |
| `enum` | `INTEGER` | NO | Enum underlying type |
| `byte[]` | `BYTEA` | - | Binary data |
| `TimeSpan` | `INTERVAL` | NO | Time intervals |
| `DateOnly` | `DATE` | NO | .NET 6+ |
| `TimeOnly` | `TIME` | NO | .NET 6+ |

## String Length Handling

The skill determines VARCHAR length from:

1. **`[StringLength(N)]` attribute**
   ```csharp
   [StringLength(128)]
   public string SystemName { get; set; }
   ```
   → `VARCHAR(128)`

2. **`[MaxLength(N)]` attribute**
   ```csharp
   [MaxLength(64)]
   public string Code { get; set; }
   ```
   → `VARCHAR(64)`

3. **No attribute**
   - Default: `VARCHAR(256)`
   - For descriptions, histories, logs: `TEXT`

## Common String Columns and Their Typical Lengths

| Property Name | Typical Length | PostgreSQL Type |
|---------------|----------------|-----------------|
| `Id` | Guid | UUID |
| `TenantId` | Guid | UUID |
| `SystemName` | 64-128 chars | `VARCHAR(128)` |
| `DisplayName` | 128-256 chars | `VARCHAR(256)` |
| `Name` | 128 chars | `VARCHAR(128)` |
| `Code` | 32-64 chars | `VARCHAR(64)` |
| `Description` | Unlimited | `TEXT` |
| `Email` | 256 chars | `VARCHAR(256)` |
| `PhoneNumber` | 32 chars | `VARCHAR(32)` |
| `Url` | 512 chars | `VARCHAR(512)` |
| `FormData` | Unlimited | `JSONB` |
| `JsonSchema` | Unlimited | `JSONB` |
| `ErrorMessage` | Unlimited | `TEXT` |

## ABP Framework Standard Types

ABP uses specific types with defined mappings:

| ABP Type | C# Type | PostgreSQL | Notes |
|----------|---------|------------|-------|
| `Guid` (Id) | `Guid` | `UUID` | All aggregate roots |
| `DateTime` | `DateTime` | `TIMESTAMPTZ` | Always with timezone |
| `bool` | `bool` | `BOOLEAN` | IsActive, IsDeleted |
| `string` | `string` | `VARCHAR` | Length by attribute |
| `virtual ICollection<T>` | Navigation | - | Relationship only |

## Nullability

- **`T`** → `NOT NULL`
- **`T?`** (nullable) → `NULL`
- **Reference types** (string, class) → `NULL` unless `[Required]`

**Example:**
```csharp
public string Name { get; set; }              // VARCHAR (NOT NULL)
public string? Description { get; set; }      // VARCHAR (NULL)
public DateTime CreatedAt { get; set; }       // TIMESTAMPTZ (NOT NULL)
public DateTime? DeletedAt { get; set; }      // TIMESTAMPTZ (NULL)
```

## JSONB Fields

Common JSONB usage in ACMS/ABP:

| Field Name | Content | Query Examples |
|------------|---------|----------------|
| `FormData` | User-submitted form data | `@> '{"fieldName": "value"}'` |
| `FormSchema` | Form configuration | `? 'properties'` (check key) |
| `JsonSchema` | Schema definition | `->>'version'` (extract value) |
| `InitialData` | Default values | `jsonb_path_query()` |
| `OperationParameters` | Job configuration | `@> '{"priority": "high"}'` |
| `EventSourceConfiguration` | Event config | `? 'eventType'` |
| `ImportConfig` | Import settings | `->>'mapping'` |
| `ExportConfig` | Export settings | `->>'format'` |
| `UiSchema` | UI layout config | `? 'layout'` |

**JSONB Operators:**

| Operator | Meaning | Example |
|----------|---------|---------|
| `@>` | Contains | `col @> '{"key":"value"}'` |
| `<@` | Is contained by | `'{"k":"v"}' <@ col` |
| `?` | Key exists | `col ? 'key'` |
| `?|` | Any key exists | `col ?| array['k1','k2']` |
| `?&` | All keys exist | `col ?& array['k1','k2']` |
| `->` | Get JSON object | `col->'key'` |
| `->>` | Get text | `col->>'key'` |
| `#>` | Get nested JSON | `col#>'{a,b}'` |
| `#>>` | Get nested text | `col#>>'{a,b}'` |
| `@?` | JSON path match | `col @? '$.key ? (@ == "value")'` |

## Enum Mapping

C# enums are stored as integers by default:

```csharp
public enum OrderStatus
{
    Pending = 1,
    Approved = 2,
    Rejected = 3,
    Completed = 4
}

// Stored as INTEGER in database
public int Status { get; set; } = (int)OrderStatus.Pending;
```

**Querying:** Compare with integer values:

```sql
WHERE "Status" = 2  -- Approved
```

If using `[JsonConverter]` to store as string, adjust mapping to `VARCHAR`.

## Special Types

### TimeZone Handling

- **`DateTime`** in .NET → `TIMESTAMPTZ` in PostgreSQL
- ASP.NET Core stores UTC by default
- Convert when displaying: `"CreationTime" AT TIME ZONE 'Asia/Kathmandu'`

### Precision for Financial Data

```csharp
public decimal Amount { get; set; }  -- → NUMERIC (unlimited precision)
```

Avoid `float`/`double` for financial calculations - use `decimal` → `NUMERIC`.

### Binary Data

```csharp
public byte[] ImageData { get; set; }  -- → BYTEA
```

---

## Type Conversion Examples

### Before (C#) → After (PostgreSQL)

```csharp
public Guid Id { get; set; }
```
```sql
"Id" UUID NOT NULL
```

```csharp
public string Email { get; set; }
[MaxLength(256)]
public string Email { get; set; }
```
```sql
"Email" VARCHAR(256) NOT NULL
```

```csharp
public DateTimeOffset CreatedAt { get; set; }
```
```sql
"CreatedAt" TIMESTAMPTZ NOT NULL
```

```csharp
[Required]
public string Name { get; set; }
```
```sql
"Name" VARCHAR(256) NOT NULL
```

```csharp
public Dictionary<string, object> Metadata { get; set; }
```
```sql
"Metadata" JSONB
```

```csharp
public bool IsActive { get; set; } = true;
```
```sql
"IsActive" BOOLEAN NOT NULL DEFAULT true
```

---

## Column Constraints from EF Core

The skill infers constraints from EF Core data annotations:

| Attribute | PostgreSQL Equivalent |
|-----------|-----------------------|
| `[Required]` | `NOT NULL` |
| `[MaxLength(N)]` | `VARCHAR(N)` |
| `[StringLength(N)]` | `VARCHAR(N)` |
| `[Column(TypeName = "TEXT")]` | `TEXT` |
| `[Precision(18, 2)]` | `NUMERIC(18,2)` |
| `[Unicode(false)]` | No specific PG type |

---

## Index Recommendations by Type

| Column Type | Index Type | When to Use |
|-------------|------------|-------------|
| UUID (FK) | B-tree default | Standard foreign key |
| VARCHAR (short) | B-tree | Filtering, searching |
| TEXT (long) | GIN (trigram) | Full-text search with `pg_trgm` |
| JSONB | GIN | Containment queries (`@>`) |
| BOOLEAN | Partial B-tree | `WHERE "IsActive" = true` |
| TIMESTAMPTZ | B-tree DESC | Date ranges, recent records |
| NUMERIC | B-tree | Range queries (exact match) |
| ENUM (integer) | B-tree | Status fields |

---

## See Also

- **[Entity Discovery](entity-discovery.md)** - How properties are parsed
- **[Query Patterns](query-patterns.md)** - Using the right types in queries
- **[Troubleshooting](troubleshooting.md)** - Fix type mapping issues
