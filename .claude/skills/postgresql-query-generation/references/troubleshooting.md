# Troubleshooting

Common issues and solutions when using the PostgreSQL Query Generation skill.

## Discovery Issues

### Entity Not Found

**Symptom:** Skill can't find your entity when generating queries.

**Causes:**
1. Entity file not in scanned directories
2. Entity class doesn't match expected patterns
3. Entity is abstract or internal

**Solutions:**

```
✓ Ensure entity follows naming pattern:
   public class Product : FullAuditedAggregateRoot<Guid>
   (or AuditedAggregateRoot, AggregateRoot, Entity<T>, SetupEntity)

✓ Place files in standard location:
   src/YourProject.Domain/Entities/Products/Product.cs
   or
   src/YourProject.Domain/Entities/Product.cs

✓ Make entity public and non-abstract
   public (not internal) class Product
```

**Manual override:** Add entity manually to discovered entities if needed (future enhancement).

---

### Missing Relationships

**Symptom:** Relationships between entities not detected automatically.

**Causes:**
1. Foreign key property not following `{EntityName}Id` naming pattern
2. Navigation property is not public
3. Missing explicit foreign key (only navigation property)
4. Composite foreign keys

**Solutions:**

```
✓ Use conventional naming:
   public Guid CategoryId { get; set; }      -- FK detected
   public virtual Category Category { get; set; }  -- Navigation detected

✗ Avoid: public Guid CatId { get; set; }  -- Not detected (missing "Category")

✓ Make navigation properties public/protected virtual:
   public virtual ICollection<Product> Products { get; set; }
   public virtual Category Category { get; set; }

✗ Private navigation properties NOT detected:
   private ICollection<Product> Products { get; set; }
```

**Manual workaround:** Queries can still manually JOIN on correctly named FK columns even if relationships not auto-detected.

---

### Wrong Table Name

**Symptom:** Generated query uses incorrect table name (e.g., `Products` instead of `tbl_Product`).

**Causes:**
1. Table name uses custom prefix/suffix
2. Entity uses `[Table("CustomName")]` attribute
3. Custom naming convention in OnModelCreating

**Solutions:**

```
Current: Table name inferred from class name
  - Product → Products (pluralized)
  - Category → Categories

If using custom names, the skill currently:
  - Does NOT parse [Table] attributes (not implemented)
  - Does NOT read OnModelCreating (future enhancement)

Workaround: Manually adjust generated query with correct table name.

Future: Add attribute parsing support.
```

---

### Missing Base Class Properties

**Symptom:** Entities don't show expected properties like `TenantId`, `IsDeleted`, `CreationTime`.

**Causes:**
1. Base class not recognized (custom naming)
2. Base class properties have different names
3. Base class file not in scan path

**Solutions:**

```
✓ Ensure base class in: Domain/Entities/Base/ or Domain/Entities/
✓ Ensure base class defines properties as public/virtual:

public abstract class MyBaseEntity : Entity<Guid>
{
    public Guid? TenantId { get; set; }
    public bool IsActive { get; set; }
    public DateTime CreatedAt { get; set; }
}

✓ Derived entities will inherit these properties automatically.
```

**Custom base names:**
The skill inspects all base classes. If your project uses:
```csharp
public class MyEntity : MyCustomBase<Guid>
```
The properties from `MyCustomBase` are automatically collected.

---

### TenantId Filter Missing

**Symptom:** Generated query doesn't include `TenantId = @tenantId` filter.

**Causes:**
1. Entity doesn't implement `IMultiTenant`
2. Entity doesn't have a `TenantId` property
3. Property named differently (e.g., `OrganizationId`)

**Solutions:**

```csharp
// Standard ABP:
public class MyEntity : FullAuditedAggregateRoot<Guid>, IMultiTenant
{
    public Guid? TenantId { get; set; }  // → Auto-filter added
}

// If using custom property name:
// Currently NOT supported - must use TenantId
// Future: Add configurable tenant column name
```

---

### Soft Delete Filter Missing

**Symptom:** Query doesn't add `IsDeleted = false` filter.

**Causes:**
1. Entity doesn't have `IsDeleted` property
2. Entity doesn't implement `ISoftDelete`
3. Using `IsArchived` or custom soft delete field

**Solutions:**

```csharp
// ABP standard:
public class MyEntity : FullAuditedAggregateRoot<Guid>
{
    public bool IsDeleted { get; set; }  // → Auto-filter added
}

// Custom soft delete field:
// Currently NOT supported - must use IsDeleted
// Future: Configurable soft delete column name
```

---

## Type Mapping Issues

### Incorrect PostgreSQL Type

**Symptom:** Generated column has wrong type (e.g., `VARCHAR(256)` should be `TEXT`).

**Causes:**
1. Missing `[StringLength]` attribute for short strings
2. Long text not explicitly marked (skill defaults to 256)
3. JSONB type not detected

**Solutions:**

```
Add attributes for clarity:

[StringLength(64)]
public string Code { get; set; }          -- VARCHAR(64)

[StringLength(4000)]
public string Notes { get; set; }        -- VARCHAR(4000)

public string Description { get; set; }  -- VARCHAR(256) (default)

// For truly unlimited text, add attribute or the skill will guess:
[Text]
public string JsonData { get; set; }     -- → TEXT (but JSONB would be better)
```

**Custom type mapping:** Add `[Column(TypeName = "JSONB")]` for JSON fields (not yet parsed).

---

## Performance Issues

### Slow Discovery

**Symptom:** First query takes several seconds.

**Cause:** Domain discovery scans many files.

**Solutions:**

```
✓ Discovery is one-time cost per session
✓ Results are cached for subsequent queries
✓ For CLI tool: schema saved to cache file

If repeatedly slow:
  - Reduce number of entity files scanned
  - Ensure Domain/Entities structure is flat, not deeply nested
  - Cache schema JSON and reload: --schema-cache schema.json
```

### Large Result Sets

**Symptom:** Query returns too many rows, slow execution.

**Solution:** Always add `LIMIT` and `OFFSET` (skill adds default if missing).

```sql
-- Always include pagination
LIMIT @maxResultCount OFFSET @skipCount;
```

---

## Syntax Errors in Generated SQL

### Column Name Case Issues

**Symptom:** `column "systemname" does not exist`

**Cause:** PostgreSQL folds unquoted identifiers to lowercase.

**Solution:** Skill uses quoted identifiers: `"SystemName"` preserves camelCase/PascalCase.

Correct:
```sql
SELECT "SystemName" FROM "Applications"  -- Case preserved
```

Incorrect (unquoted):
```sql
SELECT SystemName FROM Applications  -- Becomes systemname in PostgreSQL
```

The skill always quotes both table and column names. Ensure your database schema matches.

---

### Schema Missing

**Symptom:** `relation "Applications" does not exist`

**Causes:**
1. Table name differs from entity class name
2. Different schema (not `public`)
3. Database not migrated

**Solutions:**

```
Check actual table name:
  \d "Applications"  -- In psql
  \dt *Applications*  -- Find table

If schema is different:
  "AbpIdentity"."Users" (not "Users")

Skill detects schema from namespace - verify:
  └── namespace Amnil.AccessControlManagementSystem.Domain
      → public schema

If using custom schema via [Schema("custom")] - not yet supported.
```

---

### Mixed Guid/string UUID Cast Issues

**Symptom:** `operator does not exist: uuid = character varying`

**Cause:** Comparing Guid UUID with string without casting.

**Solution:**
```sql
-- Wrong
WHERE "UserId" = '123e4567-e89b-12d3-a456-426614174000'

-- Correct
WHERE "UserId" = '123e4567-e89b-12d3-a456-426614174000'::uuid
-- or
WHERE "UserId" = CAST('123e4567...' AS UUID)
```

Skill generates `@userId` parameter (Npgsql handles automatic conversion).

---

## Working with ABP Framework Specifics

### AbpIdentity Schema

**Issue:** Identity tables are in `AbpIdentity` schema, not `public`.

**Skill handling:** Automatically detects namespace with "Identity" → `AbpIdentity` schema.

```sql
SELECT u."UserName"
FROM "AbpIdentity"."Users" u
JOIN "AbpIdentity"."UserRoles" ur ON ur."UserId" = u."Id"
```

Make sure entities from `AbpIdentity` namespace are detected with correct `schema: "AbpIdentity"`.

---

### TenantId Null for System Records

**Issue:** Some records have `TenantId = NULL` (system-wide).

**Query handling:**

```sql
-- To get both tenant and system records:
WHERE "TenantId" IS NULL OR "TenantId" = @tenantId

-- To get ONLY tenant records:
WHERE "TenantId" = @tenantId

-- To get ONLY system records:
WHERE "TenantId" IS NULL
```

---

### Soft Delete + Active Filter Combo

**Standard pattern:**

```sql
WHERE "TenantId" = @tenantId
  AND "IsDeleted" = false
  AND "IsActive" = true    -- Often needed
```

If entity uses both soft delete AND active flag, both filters should be applied.

---

## Debugging Discovery

### View Discovered Schema

```bash
python scripts/generate_query.py --discover-only --output schema.json
```

Inspect schema.json to verify:
- All expected entities present
- Properties correctly extracted
- Relationships detected
- Table names and schemas correct

### Verbose Debugging

Add debug logging to script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Run:
```bash
python scripts/generate_query.py --discover-only 2>&1 | grep -i "parsed"
```

---

## Request Clarification

### Ambiguous Entity Names

**Symptom:** "User" could mean `User`, `ApplicationUser`, `AdminUser`.

**Skill response:** Picks first match or asks for clarification.

**Solution:** Be specific in request:
```
❌ "get all users"
✓ "get all ApplicationUsers"
✓ "get AbpIdentity Users"
✓ "get all users from UserManagement"
```

---

### Missing Context

**Symptom:** "Show pending items" - too vague.

**Solution:** Include entity name and relationship hints:
```
✓ "Show pending ApplicationTasks with workflow stages"
✓ "Get Orders with status=Pending and customer name"
✓ "Find workflow instances in 'Processing' stage for operation X"
```

---

## Advanced Customization

### Adding Support for Custom Attributes

**Current limitation:** `[Table]`, `[Column]`, `[Schema]` attributes not parsed.

**Future work:**

```python
# In _parse_entity_file():
# Extract [Table("CustomName")] attribute
table_attr_match = re.search(r'\[Table\("([^"]+)"\)\]', content)
if table_attr_match:
    table_name = table_attr_match.group(1)
```

---

### Custom Naming Conventions

If project uses non-standard conventions:

1. **Modify `_infer_table_name()`** to use your naming strategy
2. **Adjust `_infer_schema()`** for custom schemas
3. **Extend `_parse_properties()`** to detect additional FK patterns

Example: Tables with `tbl_` prefix:

```python
def _infer_table_name(self, class_name, namespace):
    return f"tbl_{class_name}"  # Custom convention
```

---

## Common Error Messages

| Error | Meaning | Fix |
|-------|---------|-----|
| `Entity not found` | No matching entity in schema | Check entity name, add entity, refine request |
| `Table "X" does not exist` | Wrong table name or schema | Verify `\d` in psql, check schema override |
| `Column "X" does not exist` | Property not found or misspelled | Check entity properties (`--discover-only`) |
| `syntax error at or near "..."` | Invalid SQL generation | Report bug with entity and request |
| `permission denied for schema` | DB user lacks access | Check connection user permissions |

---

## Getting Help

1. **View schema:** `--discover-only` to inspect discovered entities
2. **Check logs:** Enable debug logging for detailed parsing output
3. **Compare examples:** See `query-examples.md` for similar use cases
4. **Verify attributes:** Ensure entities follow expected patterns

---

## See Also

- **[Entity Discovery](entity-discovery.md)** - Detailed discovery mechanism
- **[Query Patterns](query-patterns.md)** - Pattern reference for manual queries
- **[Query Examples](query-examples.md)** - Real-world ACMS query examples
- **[Type Mappings](type-mappings.md)** - C# → PostgreSQL conversions
