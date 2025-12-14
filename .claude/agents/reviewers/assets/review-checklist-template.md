# Code Review Checklist Template

Use this template to generate developer-actionable checklists for fixing review issues.

---

## Header Template

```markdown
# Code Review Checklist: {FEATURE_NAME}

**Branch:** `{BRANCH_NAME}`
**Commits:** `{START_COMMIT}` → `{END_COMMIT}` ({COMMIT_COUNT} commits)
**Reviewers:** {REVIEWER_NAMES}
**Date:** {YYYY-MM-DD}

---
```

## Severity Section Template

### Critical Issues

```markdown
## 🚨 CRITICAL (Must Fix Before Merge)

### {CATEGORY}

- [ ] **{FILE_PATH}:{LINE}** - {ISSUE_DESCRIPTION}
- [ ] **{FILE_PATH}:{LINE}** - {ISSUE_DESCRIPTION}

### {CATEGORY_2}

- [ ] **{FILE_PATH}:{LINE}** - {ISSUE_DESCRIPTION}

---
```

### High Priority Issues

```markdown
## ⚠️ HIGH Priority

### {CATEGORY}

- [ ] **{FILE_PATH}:{LINE}** - {ISSUE_DESCRIPTION}
- [ ] **{FILE_PATH}:{LINE}** - {ISSUE_DESCRIPTION}

---
```

### Medium Priority Issues

```markdown
## 📝 MEDIUM Priority

### {CATEGORY}

- [ ] **{FILE_PATH}:{LINE}** - {ISSUE_DESCRIPTION}
- [ ] Standardize {PATTERN} across all services

---
```

## Category Templates

### Security - Authorization

```markdown
### Security - Authorization

- [ ] **{AppService}.cs:{LINE}** - Uncomment `[Authorize]` attribute on class
- [ ] **{AppService}.cs:{LINE}** - Uncomment `[Authorize]` on `CreateAsync`
- [ ] **{AppService}.cs:{LINE}** - Uncomment `[Authorize]` on `UpdateAsync`
- [ ] **{AppService}.cs:{LINE}** - Uncomment `[Authorize]` on `DeleteAsync`
- [ ] **{AppService}.cs:{LINE}** - Add `[Authorize]` on `ActivateAsync`
- [ ] **{AppService}.cs:{LINE}** - Add `[Authorize]` on `DeactivateAsync`
```

### Security - Permissions

```markdown
### Security - Permissions

- [ ] **{Permissions}.cs** - Add `{Feature}` permission group
- [ ] **{PermissionDefinitionProvider}.cs** - Register new permissions
```

### Security - SQL Injection

```markdown
### Security - SQL Injection

- [ ] **{File}.cs:{LINE}** - Validate sorting input against whitelist
```

### Validation - FluentValidation

```markdown
### Validation - FluentValidation

- [ ] **{Dto}.cs** - Remove data annotations, create FluentValidation validator
- [ ] Create `{Dto}Validator.cs` with proper rules
```

### Performance - N+1

```markdown
### Performance - N+1 Queries

- [ ] **{File}.cs:{LINE}** - Refactor to use single query with joins
- [ ] **{File}.cs:{LINE}** - Add `.Include()` for navigation properties
- [ ] **{File}.cs:{LINE}** - Move `CountAsync` before projection
```

### ABP Patterns - Unit of Work

```markdown
### ABP Patterns - Unit of Work

- [ ] **{File}.cs:{LINE}** - Remove manual `SaveChangesAsync()`
- [ ] **{File}.cs:{LINE}** - Remove manual `SaveChangesAsync()`
```

### DDD - Entity Encapsulation

```markdown
### DDD - Entity Encapsulation

- [ ] **{Entity}.cs:{LINE}** - Change public setters to `private set`
```

### Code Quality

```markdown
### Code Quality

- [ ] **{File}.cs:{LINE}** - Remove redundant null check after method that throws
- [ ] **{File}.cs:{LINE}** - Replace magic string with permission constant
- [ ] **{File}.cs:{LINE}** - Replace `.ToLower().Contains()` with `EF.Functions.Like()`
```

## Verification Steps Section

```markdown
## ✅ Verification Steps

After fixing all issues:

1. [ ] Run `dotnet build {SOLUTION}` - No errors
2. [ ] Run `dotnet test {TEST_PROJECT}` - All tests pass
3. [ ] Verify authorization with Swagger/Postman (endpoints should return 401/403 without token)
4. [ ] Test bulk import with invalid data (validation errors should be returned)
5. [ ] Performance test {METHOD_NAME} with production-like data
```

## Progress Tracker Section

```markdown
## 📊 Progress Tracker

| Category | Total | Fixed | Remaining |
|----------|-------|-------|-----------|
| CRITICAL - Security | {N} | ☐ | {N} |
| CRITICAL - Permissions | {N} | ☐ | {N} |
| CRITICAL - Validation | {N} | ☐ | {N} |
| CRITICAL - Performance | {N} | ☐ | {N} |
| HIGH | {N} | ☐ | {N} |
| MEDIUM | {N} | ☐ | {N} |
| **TOTAL** | **{TOTAL}** | **0** | **{TOTAL}** |
```

## Assignment Section

```markdown
## 👥 Assignment Suggestions

### @{DEVELOPER_1}
- {FOCUS_AREA_1}
- {FOCUS_AREA_2}

### @{DEVELOPER_2}
- {FOCUS_AREA_3}
- {FOCUS_AREA_4}

---

**Estimated effort:** {X}-{Y} hours combined
**Priority:** CRITICAL items must be fixed before merge
```

---

## Complete Example

```markdown
# Code Review Checklist: {Feature Name}

**Branch:** `feat/{feature-branch}`
**Commits:** `{start_hash}` → `{end_hash}` ({N} commits)
**Reviewers:** @{reviewer-1}, @{reviewer-2}
**Date:** {YYYY-MM-DD}

---

## 🚨 CRITICAL (Must Fix Before Merge)

### Security - Authorization

- [ ] **{Entity}AppService.cs:{LINE}** - Add `[Authorize]` attribute on class
- [ ] **{Entity}AppService.cs:{LINE}** - Add `[Authorize]` on `CreateAsync`
- [ ] **{Entity}AppService.cs:{LINE}** - Add `[Authorize]` on `UpdateAsync`
- [ ] **{Entity}AppService.cs:{LINE}** - Add `[Authorize]` on `DeleteAsync`

### Security - Permissions

- [ ] **{Project}Permissions.cs** - Add `{Entity}` permission group
- [ ] **{Project}PermissionDefinitionProvider.cs** - Register new permissions

### Validation - FluentValidation

- [ ] **CreateUpdate{Entity}Dto.cs** - Remove data annotations, create FluentValidation validator

### Performance - N+1 Queries

- [ ] **{Entity}AppService.cs:{LINE}** - Refactor to use single query with joins

### DDD - Entity Encapsulation

- [ ] **{Entity}.cs:{LINE}** - Change public setters to `private set`

---

## ⚠️ HIGH Priority

### ABP Patterns - Unit of Work

- [ ] **{Entity}AppService.cs:{LINE}** - Remove manual `SaveChangesAsync()`

### Code Quality

- [ ] **{File}.cs:{LINE}** - Replace magic string with permission constant
- [ ] **{File}.cs:{LINE}** - Replace `.ToLower().Contains()` with `EF.Functions.Like()`

---

## 📝 MEDIUM Priority

### Mapping

- [ ] **{Entity}AppService.cs:{LINE}** - Replace `ObjectMapper` with Mapperly mapper

### Response Consistency

- [ ] Standardize response types across all services (`ResponseDto<T>`)

---

## ✅ Verification Steps

After fixing all issues:

1. [ ] Run `dotnet build {solution-path}` - No errors
2. [ ] Run `dotnet test {test-project}` - All tests pass
3. [ ] Verify authorization with Swagger (endpoints should return 401/403 without token)

---

## 📊 Progress Tracker

| Category | Total | Fixed | Remaining |
|----------|-------|-------|-----------|
| CRITICAL - Security | {N} | ☐ | {N} |
| CRITICAL - Permissions | {N} | ☐ | {N} |
| CRITICAL - Validation | {N} | ☐ | {N} |
| CRITICAL - Performance | {N} | ☐ | {N} |
| CRITICAL - DDD | {N} | ☐ | {N} |
| HIGH | {N} | ☐ | {N} |
| MEDIUM | {N} | ☐ | {N} |
| **TOTAL** | **{TOTAL}** | **0** | **{TOTAL}** |

---

## 👥 Assignment Suggestions

### @{developer-1}
- {Focus area 1}
- {Focus area 2}

### @{developer-2}
- {Focus area 3}
- {Focus area 4}

---

**Priority:** CRITICAL items must be fixed before merge
```
