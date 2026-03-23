---
name: postgresql-query-generation
description: >
  Generate optimized PostgreSQL queries for Entity Framework Core projects.
  Automatically discovers domain entities, relationships, and conventions to
  produce production-ready SQL. Use when:

  1. You need complex PostgreSQL queries across multiple related entities

  2. Working with ABP Framework and need multi-tenancy/soft delete patterns

  3. Querying JSONB fields or need recursive CTEs

  4. Building analytics/reporting queries with window functions

  5. Optimizing existing queries with proper indexes and joins.
---

# PostgreSQL Query Generation

Generate production-ready PostgreSQL queries for any .NET project using Entity Framework Core. This skill automatically discovers your domain structure and generates optimized SQL with proper relationships, multi-tenancy, soft delete filters, and ABP Framework conventions.

## Quick Start

```bash
# Interactive mode (output to stdout)
python scripts/generate_query.py --interactive

# Generate query - automatically saves .sql file in current directory
python scripts/generate_query.py --query "get all applications with workflow stages"

# Generate query with custom output filename
python scripts/generate_query.py --query "get all applications" --output my_query.sql

# Only discover domain (output schema as JSON)
python scripts/generate_query.py --discover-only --output schema.json
```

## What It Does

1. **Discovers domain entities** by scanning C# entity files
2. **Analyzes relationships** (foreign keys, navigation properties)
3. **Detects project conventions** (multi-tenancy, soft delete, audit fields)
4. **Generates optimized queries** with proper JOINs and WHERE clauses
5. **Adapts to any domain** (ABP, custom DDD, layered monoliths)

## Capabilities

### Automatic Discovery
- Scans `src/*/Domain/Entities/**/*.cs` for entity classes
- Inherits properties from base classes (FullAuditedAggregateRoot, SetupEntity, etc.)
- Detects foreign keys by `{EntityName}Id` pattern
- Identifies navigation properties (ICollection<T>, T)
- Maps C# types to PostgreSQL types automatically

### Query Patterns Supported
- ✅ Multi-entity JOIN queries
- ✅ Many-to-many relationships via join tables
- ✅ Hierarchical/self-referencing (recursive CTE)
- ✅ JSONB querying (`@>`, `?`, `jsonb_path_query`)
- ✅ Window functions (ROW_NUMBER, FIRST_VALUE, etc.)
- ✅ Pagination with COUNT
- ✅ Permission/security queries with complex joins
- ✅ Aggregations and GROUP BY
- ✅ Full-text search (ILIKE)
- ✅ Bulk operations (INSERT/UPDATE with CASE)

### Project-Specific Patterns
- **ABP Framework**: Auto-detects TenantId, IsDeleted, CreationTime audit fields
- **Multi-tenancy**: Always adds `TenantId = @tenantId` filter
- **Soft delete**: Adds `IsDeleted = false` filter
- **JSONB fields**: Optimized queries for InitialData, FormData, JsonSchema, etc.
- **Naming conventions**: Uses quoted identifiers (e.g., `"SystemName"`)

## Example Output

**Request:** `Get all ApplicationWorkflowInstances with workflow stage, operation, and substage`

```sql
SELECT
  awi."Id",
  awi."TaskNumber",
  awi."WorkflowStageDate",
  app."Name" as "ApplicationName",
  stage."DisplayName" as "StageName",
  substage."DisplayName" as "SubStageName",
  owf."RequestNumber" as "OperationRequestNumber"
FROM "ApplicationWorkflowInstances" awi
JOIN "OperationWorkflowInstances" owf ON owf."Id" = awi."OperationWorkflowInstanceId"
  AND owf."TenantId" = awi."TenantId"
JOIN "WorkflowStages" stage ON stage."Id" = awi."StageId"
  AND stage."TenantId" = awi."TenantId"
LEFT JOIN "WorkflowSubStages" substage ON substage."Id" = awi."SubStageId"
JOIN "Applications" app ON app."Id" = awi."ApplicationWorkflowConfigurationId"
  AND app."TenantId" = awi."TenantId"
WHERE awi."TenantId" = @tenantId
  AND awi."IsDeleted" = false
  AND stage."IsActive" = true
ORDER BY awi."WorkflowStageDate" DESC
LIMIT @maxResultCount OFFSET @skipCount;
```

## Output Files

### Automatic File Generation

When using `--query` without specifying `--output`, the skill automatically creates a `.sql` file in the **current working directory** with:
- **Auto-generated filename** based on the entity name or query keywords (e.g., `application_workflow_instance_1678901234.sql`)
- **Timestamp** to ensure uniqueness
- Complete, production-ready PostgreSQL queries
- Proper parameterization (@paramName style)
- TenantId and soft-delete filters automatically included
- Optimized JOINs based on foreign keys
- Comments explaining key patterns

### Manual Output

Use `--output` to specify a custom filename:
```bash
python scripts/generate_query.py --query "get all users" --output users_query.sql
```

The file is saved in the current working directory by default, or you can provide a full path.

## Configuration

No configuration needed! The skill adapts automatically. If your project uses:
- **Custom base classes**: Automatically inherits their properties
- **Non-standard table names**: Detected from [Table("...")] attributes if present
- **Different schemas**: Detected from [Schema("...")] attributes
- **Composite keys**: Handled as detected

## Cross-Project Portability

Works with **any** EF Core project:

| Project Type | Detection | Adaptation |
|--------------|-----------|------------|
| ABP Framework | FullAuditedAggregateRoot, IMultiTenant | Auto-add TenantId, IsDeleted filters |
| Custom DDD | AggregateRoot, Entity | Respect aggregate boundaries, standard properties |
| Plain EF Core | Entity<TKey> | Basic entity patterns |
| Multi-tenant | TenantId property | Always filter by @tenantId |
| Single-tenant | No TenantId | Skip tenant filtering |
| Soft Delete | IsDeleted property | Auto-add IsDeleted = false |
| No soft delete | No IsDeleted | Skip soft delete filter |

## Requirements

- Python 3.8+
- Access to project source code (to read entity definitions)
- No dependencies required (uses standard library)

## Reference Files

For detailed documentation, see:
- **[Entity Discovery Guide](references/entity-discovery.md)** - How domain analysis works
- **[Query Patterns](references/query-patterns.md)** - Common SQL patterns
- **[Type Mappings](references/type-mappings.md)** - C# to PostgreSQL conversions
- **[Troubleshooting](references/troubleshooting.md)** - Fixing discovery issues

## Examples

See **[query-examples.md](references/query-examples.md)** for 20+ real-world query patterns:
- Multi-tenant filtering
- JSONB queries
- Recursive hierarchies
- Permission checks
- Webhook queries
- Window functions
- Bulk operations
- Full-text search

## Workflow

1. **Discovery** (automatic on first run)
   - Scans entity files
   - Builds schema model
   - Caches results (reuse for subsequent queries)

2. **Generation**
   - Parse natural language request
   - Identify target entity
   - Determine required joins
   - Apply project conventions
   - Output final query

3. **Output**
   - Print to stdout or save to .sql file
   - Include parameter placeholders
   - Add helpful comments

## Tips

- **Refine your request**: Include entity names (e.g., "Products" not just "items")
- **Use natural language**: "Get active Users with Admin roles" or "Show Orders pending approval"
- **Specify joins**: "Applications with workflow stages" automatically joins related entities
- **Schema caching**: First run slower (100ms-2s), subsequent runs instant

## Performance

| Operation | Time |
|-----------|------|
| Discovery (500 entities) | ~500ms - 2s |
| Query generation | ~50-200ms |
| Cached query | ~5-20ms |

Schema is cached in memory for the session.

## Limitations

- **C# parsing**: Simplified parser; complex generic bases may need manual review
- **Dynamic queries**: Not a query builder - generates specific SQL
- **Procedural code**: Cannot generate stored procedures or functions
- **Non-EF data**: Only discovers entities, not raw tables or views
- **Attr. overrides**: Supports [Table] and [Column] attributes (basic)

## License

Open source - part of the ACMS ecosystem.
