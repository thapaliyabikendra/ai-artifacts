---
description: Audit ABP permission definitions and usage across the codebase
allowed-tools: Read, Glob, Grep
argument-hint: [--unused] [--unprotected] [--matrix]
---

# Review Permissions Command

Audit permission definitions and their usage in ABP Framework application.

**Arguments**: $ARGUMENTS

## Pre-flight

**Project**: !`basename $(pwd)`
**Permissions File**: !`find api/src -name "*Permissions.cs" -path "*/Permissions/*" 2>/dev/null | head -1`

## Workflow

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. Scan      │ → │ 2. Check     │ → │ 3. Find      │ → │ 4. Generate  │
│ Definitions  │   │   Usage      │   │   Gaps       │   │   Report     │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

## Execution

### Step 1: Scan Permission Definitions

Search for permission constants:
```
Pattern: public const string .* = .*Permission
Files: api/src/**/Permissions/*.cs
```

Extract all defined permissions into a list.

### Step 2: Check Permission Usage

For each permission, search for usage:

**In AppServices (Authorize attribute):**
```
Pattern: \[Authorize\(.*{PermissionName}.*\)\]
Files: api/src/**/*AppService.cs
```

**In code (AuthorizationService):**
```
Pattern: AuthorizationService\.(Check|IsGranted).*{PermissionName}
Files: api/src/**/*.cs
```

**In PermissionDefinitionProvider:**
```
Pattern: AddPermission\(.*{PermissionName}
Files: api/src/**/*PermissionDefinitionProvider.cs
```

### Step 3: Find Gaps

**Unused Permissions:**
- Defined in Permissions.cs but never used in code

**Unprotected Endpoints:**
- AppService methods without `[Authorize]` attribute
- Mutations (Create, Update, Delete) without permission checks

**Unregistered Permissions:**
- Used in code but not registered in PermissionDefinitionProvider

### Step 4: Generate Report

## Output Format

```markdown
## Permission Audit Report

**Project**: {ProjectName}
**Date**: {Date}
**Total Permissions**: {Count}

### Permission Matrix

| Permission | AppService | Method | Status |
|------------|------------|--------|--------|
| {Group}.{Feature}.Create | {Feature}AppService | CreateAsync | ✓ Protected |
| {Group}.{Feature}.Edit | {Feature}AppService | UpdateAsync | ✓ Protected |
| {Group}.{Feature}.Delete | - | - | ⚠️ Unused |

### Unused Permissions (--unused)

| Permission | Defined In | Recommendation |
|------------|------------|----------------|
| {Group}.{Feature}.Export | {Project}Permissions.cs | Remove or implement |

### Unprotected Endpoints (--unprotected)

| AppService | Method | Risk | Recommendation |
|------------|--------|------|----------------|
| ReportAppService | GenerateAsync | HIGH | Add [Authorize] |
| PublicAppService | GetInfoAsync | LOW | Verify intentional |

### Role-Permission Matrix (--matrix)

| Permission | Admin | Role2 | Role3 |
|------------|-------|-------|-------|
| {Feature}.Create | ✓ | - | ✓ |
| {Feature}.Edit | ✓ | - | - |
| {Feature}.Delete | ✓ | - | - |

### Recommendations

1. **Remove unused permissions**: {List}
2. **Add protection to endpoints**: {List}
3. **Register missing permissions**: {List}

### Next Steps

- [ ] Review unused permissions with product owner
- [ ] Add [Authorize] to unprotected mutations
- [ ] Update role assignments if needed
```

## Options

| Option | Effect |
|--------|--------|
| `--unused` | List permissions defined but never used |
| `--unprotected` | List AppService methods without authorization |
| `--matrix` | Generate role-permission matrix |
| `--fix` | Suggest code fixes for issues found |

## Common Patterns to Check

### Correct Pattern
```csharp
[Authorize({Project}Permissions.{Feature}.Create)]
public async Task<{Entity}Dto> CreateAsync(CreateUpdate{Entity}Dto input)
```

### Missing Authorization (Flag)
```csharp
// No [Authorize] attribute - should flag
public async Task<{Entity}Dto> CreateAsync(CreateUpdate{Entity}Dto input)
```

### Intentionally Public (Skip)
```csharp
[AllowAnonymous] // Explicitly public - skip
public async Task<PublicInfoDto> GetPublicInfoAsync()
```

## Security Risk Levels

| Pattern | Risk |
|---------|------|
| Unprotected Create/Update/Delete | HIGH |
| Unprotected data retrieval | MEDIUM |
| Missing permission registration | LOW |
| Unused permission | INFO |
