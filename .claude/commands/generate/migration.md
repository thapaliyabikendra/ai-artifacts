---
description: Generate EF Core migration for ABP Framework with review
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <migration-name> [--apply] [--dry-run]
---

# Generate Migration Command

Generate and optionally apply EF Core migrations for ABP Framework.

**Arguments**: $ARGUMENTS

## Pre-flight

**Project**: !`basename $(pwd)`
**EF Core Project**: !`find api/src -maxdepth 1 -type d -name "*EntityFrameworkCore" 2>/dev/null | head -1`
**DbMigrator**: !`find api/src -maxdepth 1 -type d -name "*DbMigrator" 2>/dev/null | head -1`

## Workflow

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. Detect    │ → │ 2. Generate  │ → │ 3. Review    │ → │ 4. Apply     │
│   Changes    │   │   Migration  │   │   SQL        │   │  (optional)  │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

## Execution

### Step 1: Detect Pending Changes

```bash
# Locate projects dynamically
EF_PROJECT=$(find api/src -maxdepth 1 -type d -name "*EntityFrameworkCore" | head -1)
MIGRATOR=$(find api/src -maxdepth 1 -type d -name "*DbMigrator" | head -1)

cd "$EF_PROJECT"
dotnet ef dbcontext info --startup-project "../$(basename $MIGRATOR)"
```

Review DbContext for:
- New DbSet<> properties
- Modified entity configurations
- New relationships

### Step 2: Generate Migration

```bash
cd "$EF_PROJECT"
dotnet ef migrations add {migration-name} \
    --startup-project "../$(basename $MIGRATOR)" \
    --output-dir Migrations
```

### Step 3: Review Generated Migration

After generation, review the migration file:

1. Open `Migrations/{timestamp}_{migration-name}.cs`
2. Check `Up()` method for:
   - Table creation with correct columns
   - Index definitions
   - Foreign key constraints
   - Default values
3. Check `Down()` method for proper rollback
4. Verify no data loss operations

**Review Checklist:**
- [ ] Column types match entity properties
- [ ] Required columns have `nullable: false`
- [ ] String columns have `maxLength` constraints
- [ ] Indexes defined for query patterns
- [ ] Foreign keys have appropriate delete behavior
- [ ] No accidental data dropping operations

### Step 4: Apply Migration (if --apply)

```bash
# Option A: Use DbMigrator (recommended)
cd "$MIGRATOR"
dotnet run

# Option B: Direct EF command
cd "$EF_PROJECT"
dotnet ef database update \
    --startup-project "../$(basename $MIGRATOR)"
```

## Output

```
## Migration: {migration-name}

### Changes Detected
- [New/Modified] {Entity} table
- [Added] Index on {Column}
- [Added] Foreign key {FK_Name}

### Files Generated
- api/src/.../Migrations/{timestamp}_{name}.cs
- api/src/.../Migrations/{timestamp}_{name}.Designer.cs

### SQL Preview
```sql
-- Up migration SQL
```

### Next Steps
1. Review migration file for correctness
2. Run DbMigrator to apply
3. Verify database schema
```

## Options

| Option | Effect |
|--------|--------|
| `--apply` | Apply migration after generation |
| `--dry-run` | Show what would be generated without creating files |
| `--script` | Generate SQL script instead of applying |

## Common Issues

### "No migrations were found"
- Ensure DbSet<> added to DbContext
- Check entity configuration is applied

### "Foreign key constraint failed"
- Check relationship configuration
- Verify related entities exist in database

### "Column already exists"
- Migration may be out of sync
- Consider `dotnet ef migrations remove` and regenerate

## Rollback

```bash
# Revert last migration (not applied)
dotnet ef migrations remove --startup-project "../$(basename $MIGRATOR)"

# Revert applied migration
dotnet ef database update {previous-migration-name} \
    --startup-project "../$(basename $MIGRATOR)"
```
