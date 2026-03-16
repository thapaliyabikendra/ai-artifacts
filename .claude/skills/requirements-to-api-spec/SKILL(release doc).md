---
name: api-release-documentation
description: Generate a professional API Release Documentation (.md) from OpenAPI/Swagger files (.json or .yaml) and/or generated ABP service interfaces (.cs). Use when the team is ready to release new API endpoints and needs a release doc for stakeholders, QA, and consumers. Covers new endpoints, DTOs, breaking changes, permissions, migration checklist, and rollback plan.
tools: Read, Grep, Glob, Write, Edit, bash_tool, view, create_file, str_replace
---

You are an API Release Documentation specialist. Your goal is to **read OpenAPI/Swagger specs and/or ABP service interfaces** and produce a **complete, professional API Release Document** in Markdown format.

---

## Philosophy: Release Docs from Real Code

Release documentation must reflect what was actually built — not what was planned. This skill reads from two authoritative sources:

1. **OpenAPI/Swagger file** — the contract: endpoints, request/response shapes, status codes
2. **Generated service interfaces (.cs)** — the implementation: method signatures, return types, permissions

Both sources are combined to produce a release doc that is accurate, complete, and ready to share.

---

## Step 1 — Locate Sources

### 1.1 Ask for Swagger/OpenAPI file (if available)

```
Ask: "Do you have a Swagger/OpenAPI file? (.json or .yaml) — provide the path or press enter to skip"
```

Read if provided:

```bash
view("/path/to/swagger.json")
# OR
view("/path/to/openapi.yaml")
```

### 1.2 Locate Generated Service Interfaces

```bash
# Find all generated interface files
find . -name "I*AppService.cs" -path "*/Application.Contracts/*" | head -20

# Read each interface file
view("./src/Acme.BookStore.Application.Contracts/Customers/ICustomerAppService.cs")
```

### 1.3 Locate DTO Files

```bash
# Find all DTO files
find . -name "*Dto.cs" -path "*/Application.Contracts/*" | head -30

# Read them
view("./src/Acme.BookStore.Application.Contracts/Customers/Dtos/CustomerDto.cs")
```

### 1.4 Extract Project / Release Info

```bash
# Get project name
find . -name "*.Application.csproj" | head -1

# Get current date for release
date +%Y-%m-%d

# Try to find version info
grep -r "Version" *.csproj | head -3
cat CHANGELOG.md 2>/dev/null | head -20
```

---

## Step 2 — Parse OpenAPI/Swagger File

### 2.1 For JSON format

```bash
# List all paths
cat swagger.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for path, methods in data.get('paths', {}).items():
    for method in methods:
        if method in ['get','post','put','delete','patch']:
            op = methods[method]
            print(f'{method.upper()} {path} — {op.get(\"summary\", \"\")}')
"

# Extract all schemas/DTOs
cat swagger.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
schemas = data.get('components', {}).get('schemas', {})
for name, schema in schemas.items():
    props = schema.get('properties', {})
    print(f'\n### {name}')
    for field, info in props.items():
        ftype = info.get('type', info.get('\$ref','unknown'))
        print(f'  - {field}: {ftype}')
"
```

### 2.2 For YAML format

```bash
# Convert YAML to JSON first
python3 -c "
import yaml, json, sys
with open('openapi.yaml') as f:
    data = yaml.safe_load(f)
print(json.dumps(data, indent=2))
" > /tmp/openapi_converted.json

# Then use same JSON parsing above
```

### 2.3 Extract Per-Endpoint Details

For each endpoint, extract:
- HTTP method + path
- Summary / description
- Request body schema (if POST/PUT/PATCH)
- Response schema
- Status codes
- Security/auth requirements
- Tags (used to group by module)

---

## Step 3 — Parse Service Interfaces

### 3.1 Read each interface file

```bash
# Extract method signatures
grep -E "Task<|void " ICustomerAppService.cs

# Extract authorization attributes
grep -E "\[Authorize" ICustomerAppService.cs

# Extract return types
grep -oP "Task<\K[^>]+" ICustomerAppService.cs
```

### 3.2 Build method inventory

For each method found, record:

```
Method:     CreateAsync
Parameter:  CreateCustomerDto input
Return:     ResponseDto<CustomerDto>
Auth:       [Authorize(CustomerPermissions.Create)]
```

---

## Step 4 — Cross-Reference Sources

If BOTH Swagger and interfaces are available:

```python
# Match swagger paths to interface methods
# POST /api/customers → CreateAsync
# GET /api/customers/{id} → GetAsync
# PUT /api/customers/{id} → UpdateAsync
# DELETE /api/customers/{id} → DeleteAsync
# GET /api/customers → GetListAsync

# Use swagger for: URL, request/response body shape, status codes
# Use interface for: exact return type, permission, C# method name
```

If **only Swagger** available → use swagger for everything, note that C# details are not available.

If **only interfaces** available → infer REST endpoints from method names, note that full swagger details are not available.

---

## Step 5 — Detect Breaking Changes

```bash
# Check git diff for removed/changed methods
git diff HEAD~1 -- "*.cs" | grep "^-.*Task<" 2>/dev/null

# Check for renamed DTOs
git diff HEAD~1 -- "*Dto.cs" 2>/dev/null | head -30

# Check swagger for deprecated flags
grep -i "deprecated" swagger.json
```

**Breaking change indicators:**
- Removed endpoint (was in previous spec, not in new)
- Changed required field to optional or vice versa
- Changed return type
- Renamed endpoint path
- Removed permission

---

## Step 6 — Generate Release Documentation

Using all parsed information, generate the following document:

```markdown
# API Release Documentation
## {Project Name}

---

**Version:** {version or "1.0.0"}
**Release Date:** {today's date}
**Status:** Ready for Release
**Prepared By:** api-release-documentation skill
**Sources:**
- Swagger/OpenAPI: {swagger filename or "Not provided"}
- Service Interfaces: {list of interface files parsed}

---

## 1. Release Summary

{2–3 sentence overview of what is being released, which modules are affected, and any notable changes.}

**Modules Affected:** {comma-separated list of modules/tags from swagger}
**Total New Endpoints:** {count}
**Total New DTOs:** {count}
**Breaking Changes:** {Yes / No}

---

## 2. New Endpoints

### 2.1 Endpoint Summary

| Method | Path | Description | Auth Required | Module |
|---|---|---|---|---|
| POST | /api/{resource} | Create new {resource} | Yes | {Module} |
| GET | /api/{resource}/{id} | Get {resource} by ID | Yes | {Module} |
| GET | /api/{resource} | Get list of {resource} | Yes | {Module} |
| PUT | /api/{resource}/{id} | Update {resource} | Yes | {Module} |
| DELETE | /api/{resource}/{id} | Delete {resource} | Yes | {Module} |

### 2.2 Endpoint Details

{For each endpoint:}

---

#### {METHOD} {path}

**Summary:** {summary from swagger}
**C# Method:** `{MethodName}Async`
**Permission Required:** `{PermissionConstants.Value}`

**Request Body:** *(POST/PUT only)*
```json
{
  "field1": "string",
  "field2": "integer"
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| field1 | string | Yes | Max 100 chars |
| field2 | integer | No | Min 0 |

**Response:** `200 OK`
```json
{
  "id": "guid",
  "field1": "string",
  "field2": "integer",
  "creationTime": "datetime"
}
```

**Error Responses:**

| Status | Code | Description |
|---|---|---|
| 400 | Bad Request | Validation failed |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |

---

## 3. Data Transfer Objects (DTOs)

### 3.1 New DTOs

| DTO Name | Used In | Description |
|---|---|---|
| Create{Entity}Dto | POST /api/{resource} | Input for creating {entity} |
| Update{Entity}Dto | PUT /api/{resource}/{id} | Input for updating {entity} |
| {Entity}Dto | All responses | Standard response shape |
| {Entity}ListDto | GET /api/{resource} | List item response shape |

### 3.2 DTO Field Reference

#### Create{Entity}Dto

| Field | Type | Required | Constraints |
|---|---|---|---|
| {field} | {type} | Yes/No | {Max length, pattern, etc.} |

#### {Entity}Dto

| Field | Type | Nullable | Description |
|---|---|---|---|
| Id | Guid | No | Unique identifier |
| {field} | {type} | Yes/No | {Description} |
| CreationTime | DateTime | No | Auto-set by ABP |

---

## 4. Permissions

### 4.1 New Permission Definitions

Add the following to your `PermissionDefinitionProvider`:

```csharp
var {module}Group = context.AddGroup({ProjectName}Permissions.GroupName, L("{Module}"));

{module}Group.AddPermission({ProjectName}Permissions.{Entity}.Default, L("{Entity}"));
{module}Group.AddPermission({ProjectName}Permissions.{Entity}.Create, L("Create{Entity}"));
{module}Group.AddPermission({ProjectName}Permissions.{Entity}.Edit, L("Edit{Entity}"));
{module}Group.AddPermission({ProjectName}Permissions.{Entity}.Delete, L("Delete{Entity}"));
```

### 4.2 Permission Reference

| Endpoint | Required Permission |
|---|---|
| GET /api/{resource} | {ProjectName}Permissions.{Entity}.Default |
| POST /api/{resource} | {ProjectName}Permissions.{Entity}.Create |
| PUT /api/{resource}/{id} | {ProjectName}Permissions.{Entity}.Edit |
| DELETE /api/{resource}/{id} | {ProjectName}Permissions.{Entity}.Delete |

---

## 5. Breaking Changes

{If none:}
✅ **No breaking changes in this release.** All changes are additive (new endpoints only).

{If yes:}
⚠️ **Breaking changes detected. API consumers must update before upgrading.**

| # | Type | Before | After | Migration |
|---|---|---|---|---|
| 1 | Removed endpoint | DELETE /api/old | — | Use DELETE /api/new instead |
| 2 | Renamed field | `customerName` | `name` | Update request payloads |
| 3 | Changed type | `int id` | `Guid id` | Update all ID references |

---

## 6. Deprecated Endpoints

{If none:}
No endpoints deprecated in this release.

{If yes:}

| Endpoint | Deprecated Since | Removal Target | Replacement |
|---|---|---|---|
| GET /api/old-resource | This release | v{next major} | GET /api/new-resource |

**Migration Notes:**
{Step-by-step migration instructions for deprecated endpoints}

---

## 7. Database Changes

### 7.1 New Tables

| Table | Maps To Entity | Description |
|---|---|---|
| App{Entities} | {Entity} | Stores {entity} records |

### 7.2 Required Migration

```bash
# Generate migration
dotnet ef migrations add Add{Entity}Table --project src/{Project}.EntityFrameworkCore

# Apply migration
dotnet ef database update --project src/{Project}.EntityFrameworkCore
```

### 7.3 Rollback Script

```sql
-- Run this to undo if rollback is needed
DROP TABLE IF EXISTS App{Entities};
```

---

## 8. Integration Checklist

### For Backend Developers
- [ ] Add `DbSet<{Entity}>` to your `DbContext`
- [ ] Run EF Core migration: `dotnet ef database update`
- [ ] Add permission definitions to `PermissionDefinitionProvider`
- [ ] Add permission localization strings to `en.json`
- [ ] Register AutoMapper profiles (auto-registered if in Application project)
- [ ] Build solution: `dotnet build`
- [ ] Run unit tests: `dotnet test`

### For Frontend / API Consumers
- [ ] Import updated Swagger spec into Postman / API client
- [ ] Add new permission grants to roles in admin panel
- [ ] Update any hardcoded endpoint paths
- [ ] Handle new error response shapes (if changed)

### For DevOps / Release
- [ ] Deploy updated backend
- [ ] Verify Swagger UI is accessible at `/swagger`
- [ ] Smoke test all new endpoints
- [ ] Monitor logs for errors after deployment

---

## 9. Testing Guide

### 9.1 Quick Smoke Tests

```bash
# Health check
curl -X GET https://{host}/api/health

# Create (replace token and payload)
curl -X POST https://{host}/api/{resource} \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"field1": "test value"}'

# Get by ID
curl -X GET https://{host}/api/{resource}/{id} \
  -H "Authorization: Bearer {token}"

# List
curl -X GET "https://{host}/api/{resource}?MaxResultCount=10&SkipCount=0" \
  -H "Authorization: Bearer {token}"
```

### 9.2 Recommended Test Coverage

| Scenario | Expected Result |
|---|---|
| Create with valid data | 200 OK, returns created DTO with Id |
| Create with missing required field | 400 Bad Request |
| Get existing record | 200 OK, returns DTO |
| Get non-existent record | 404 Not Found |
| Request without auth token | 401 Unauthorized |
| Request with insufficient permission | 403 Forbidden |
| Update with valid data | 200 OK, returns updated DTO |
| Delete existing record | 200 OK |
| Delete non-existent record | 404 Not Found |

---

## 10. Swagger UI Access

Once deployed, the API can be explored interactively at:

```
https://{host}/swagger
```

To test authenticated endpoints in Swagger UI:
1. Click **Authorize** button (top right)
2. Enter: `Bearer {your_token}`
3. Click **Authorize**, then **Close**
4. All subsequent requests will include the token

---

## 11. Postman Collection

To import into Postman:
1. Open Postman → **Import**
2. Select **URL** tab
3. Enter: `https://{host}/swagger/v1/swagger.json`
4. Click **Import**

All endpoints will be imported with correct request shapes.

---

## 12. Rollback Plan

If critical issues are found after deployment:

1. **Disable endpoints** via feature flags (if configured)
2. **Revert migration:**
   ```bash
   dotnet ef database update {PreviousMigrationName} --project src/{Project}.EntityFrameworkCore
   ```
3. **Drop new tables** (if migration revert fails):
   ```sql
   DROP TABLE IF EXISTS App{Entities};
   ```
4. **Redeploy previous version**
5. **Notify API consumers** of rollback

---

## 13. Support & Contacts

| Role | Contact |
|---|---|
| Development Team | [team contact] |
| API Support | [support contact] |
| Documentation | [link to docs] |

---

*Generated by api-release-documentation skill*
*Sources: {list sources used}*
*Generated on: {datetime}*
```

---

## Step 7 — Write Output File

```bash
create_file(
  path: "{project-name}-api-release-{YYYY-MM-DD}.md",
  file_text: {generated content},
  description: "API release documentation generated from swagger and interfaces"
)
```

---

## Step 8 — Print Summary

```
═══════════════════════════════════════════════════════════════════
API Release Documentation Generated
═══════════════════════════════════════════════════════════════════

Project:        Acme.BookStore
Output File:    acme-bookstore-api-release-2025-01-15.md

Sources Parsed:
  ✓ Swagger/OpenAPI:   swagger.json (v1)
  ✓ Interfaces:        ICustomerAppService.cs, IOrderAppService.cs
  ✓ DTOs:              CustomerDto.cs, OrderDto.cs

Endpoints Documented:
  ✓ POST   /api/app/customer           Create Customer
  ✓ GET    /api/app/customer/{id}      Get Customer
  ✓ GET    /api/app/customer           Get Customer List
  ✓ PUT    /api/app/customer/{id}      Update Customer
  ✓ DELETE /api/app/customer/{id}      Delete Customer

DTOs Documented:    6
Permissions Listed: 8
Breaking Changes:   None
Deprecated:         None

Sections Generated:
  ✓ Release Summary
  ✓ New Endpoints (summary table + details)
  ✓ DTO Field Reference
  ✓ Permission Definitions + Code Snippet
  ✓ Breaking Changes
  ✓ Deprecated Endpoints
  ✓ Database Changes + Migration Script
  ✓ Integration Checklist
  ✓ Testing Guide + Smoke Tests
  ✓ Swagger UI Access Instructions
  ✓ Postman Import Instructions
  ✓ Rollback Plan

Next Steps:
  → Share with QA team for testing
  → Share with frontend team for integration
  → Publish to Swagger UI after deployment

═══════════════════════════════════════════════════════════════════
```

---

## Adaptation Rules

- **Swagger only (no interfaces)** → Generate full doc from swagger, note that C# permission constants are inferred
- **Interfaces only (no swagger)** → Infer REST paths from method names, mark endpoint URLs as "to be confirmed"
- **Both sources available** → Cross-reference for maximum accuracy, prefer swagger for URLs and interfaces for permissions
- **Multiple entities** → Group sections by entity/module using swagger tags
- **Deprecated endpoints found** → Always include migration guide in Section 6
- **Breaking changes found** → Add ⚠️ warning banner at top of document and populate Section 5
