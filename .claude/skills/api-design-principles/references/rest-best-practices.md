# REST API Best Practices

Language-agnostic REST API design patterns and guidelines.

## URL Structure

### Resource Naming

```
# Good - Plural nouns
GET /api/v1/patients
GET /api/v1/appointments
GET /api/v1/doctors

# Bad - Verbs or mixed conventions
GET /api/v1/getPatient
GET /api/v1/patient  (inconsistent singular)
POST /api/v1/createAppointment
```

### Nested Resources

```
# Shallow nesting (preferred, max 2 levels)
GET /api/v1/patients/{id}/appointments
GET /api/v1/appointments/{id}

# Deep nesting (avoid)
GET /api/v1/clinics/{id}/doctors/{id}/patients/{id}/appointments/{id}

# Better - Flatten with filters
GET /api/v1/appointments?patientId={id}&doctorId={id}
```

### Query Parameters

```
# Filtering
GET /api/v1/patients?status=active
GET /api/v1/patients?status=active&doctorId=123

# Sorting
GET /api/v1/patients?sorting=name
GET /api/v1/patients?sorting=createdAt desc

# Pagination
GET /api/v1/patients?skipCount=0&maxResultCount=20

# Searching
GET /api/v1/patients?filter=john
```

---

## HTTP Methods

### GET - Retrieve Resources

```
GET /api/v1/patients              → 200 OK (list with pagination)
GET /api/v1/patients/{id}         → 200 OK or 404 Not Found
GET /api/v1/patients?filter=john  → 200 OK (filtered list)
```

**Characteristics**: Safe, Idempotent, Cacheable

### POST - Create Resources

```
POST /api/v1/patients
Request Body: {"name": "John Doe", "email": "john@example.com"}

Response: 201 Created
Location: /api/v1/patients/123
Body: {"id": "123", "name": "John Doe", ...}
```

**Characteristics**: Not idempotent, Not safe

### PUT - Replace Resources

```
PUT /api/v1/patients/{id}
Request Body: {complete patient object with ALL fields}

Response: 200 OK (updated) or 404 Not Found
```

**Characteristics**: Idempotent (multiple calls = same result)

### PATCH - Partial Update

```
PATCH /api/v1/patients/{id}
Request Body: {"status": "inactive"}  (only changed fields)

Response: 200 OK or 404 Not Found
```

**Characteristics**: Idempotent for same patch

### DELETE - Remove Resources

```
DELETE /api/v1/patients/{id}

Response: 204 No Content (deleted)
         404 Not Found (doesn't exist)
         409 Conflict (can't delete due to references)
```

**Characteristics**: Idempotent

---

## Status Codes

### Success (2xx)

| Code | Name | Use When |
|------|------|----------|
| 200 | OK | GET, PUT, PATCH succeeded |
| 201 | Created | POST created new resource |
| 204 | No Content | DELETE succeeded, no body |

### Client Errors (4xx)

| Code | Name | Use When |
|------|------|----------|
| 400 | Bad Request | Malformed JSON, missing required headers |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | State conflict (duplicate, version mismatch) |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |

### Server Errors (5xx)

| Code | Name | Use When |
|------|------|----------|
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Maintenance, overload |

---

## Pagination

### Offset-Based (Simple)

```
Request:
GET /api/v1/patients?page=2&pageSize=20

Response:
{
  "items": [...],
  "totalCount": 150,
  "pageNumber": 2,
  "pageSize": 20,
  "totalPages": 8
}
```

**Pros**: Simple, supports jumping to page
**Cons**: Slow on large datasets, inconsistent with concurrent writes

### Cursor-Based (Scalable)

```
Request:
GET /api/v1/patients?cursor=abc123&limit=20

Response:
{
  "items": [...],
  "nextCursor": "def456",
  "hasMore": true
}
```

**Pros**: Fast, consistent
**Cons**: Can't jump to arbitrary page

### Pagination Metadata

Always include:
- Total count (for offset-based)
- Next/previous indicators
- Current page info

---

## Filtering and Sorting

### Filter Parameters

```
# Single filter
GET /api/v1/patients?status=active

# Multiple filters (AND)
GET /api/v1/patients?status=active&doctorId=123

# Range filters
GET /api/v1/patients?createdAfter=2025-01-01&createdBefore=2025-12-31

# Array filters
GET /api/v1/patients?status=active,pending
```

### Sort Parameters

```
# Single field ascending
GET /api/v1/patients?sorting=name

# Single field descending
GET /api/v1/patients?sorting=createdAt desc

# Multiple fields
GET /api/v1/patients?sorting=lastName,firstName
```

### Search/Filter Pattern

```
# Full-text search across multiple fields
GET /api/v1/patients?filter=john

# Field-specific search
GET /api/v1/patients?email=john@example.com
```

---

## Error Response Format

### Standard Structure

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more validation errors occurred.",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format."
      },
      {
        "field": "dateOfBirth",
        "message": "Date of birth cannot be in the future."
      }
    ],
    "traceId": "00-abc123-def456-00"
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 422 | Input validation failed |
| `NOT_FOUND` | 404 | Resource not found |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `CONFLICT` | 409 | State conflict |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Versioning

### URL Versioning (Recommended)

```
/api/v1/patients
/api/v2/patients
```

**Pros**: Clear, explicit, easy to route
**Cons**: Multiple URLs for same resource

### Header Versioning

```
GET /api/patients
Accept: application/vnd.myapp.v2+json
```

**Pros**: Clean URLs
**Cons**: Hidden, harder to test

### Versioning Policy

- Major version for breaking changes only
- Support at least N-1 version
- 6+ month deprecation notice
- Document migration guides

---

## Rate Limiting

### Response Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1640000000
```

### When Rate Limited

```
HTTP/1.1 429 Too Many Requests
Retry-After: 3600

{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Try again in 3600 seconds."
  }
}
```

---

## Authentication

### Bearer Token (JWT)

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key

```
X-API-Key: your-api-key-here
```

### Auth Errors

- `401 Unauthorized`: Missing/invalid/expired token
- `403 Forbidden`: Valid token but insufficient permissions

---

## Caching

### Cache Headers

```
# Allow caching for 1 hour
Cache-Control: public, max-age=3600

# No caching (sensitive data)
Cache-Control: no-cache, no-store, must-revalidate

# Conditional requests
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
```

### Conditional GET

```
Request:
GET /api/v1/patients/123
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"

Response (if unchanged):
304 Not Modified
```

---

## Bulk Operations

### Batch Create

```
POST /api/v1/patients/batch
{
  "items": [
    {"name": "Patient 1", "email": "p1@example.com"},
    {"name": "Patient 2", "email": "p2@example.com"}
  ]
}

Response:
{
  "results": [
    {"id": "1", "status": "created"},
    {"id": null, "status": "failed", "error": "Email already exists"}
  ],
  "successCount": 1,
  "failedCount": 1
}
```

### Batch Delete

```
DELETE /api/v1/patients/batch
{
  "ids": ["123", "456", "789"]
}
```

---

## Idempotency

### Idempotency Key Header

```
POST /api/v1/appointments
Idempotency-Key: unique-request-id-123
```

Use for:
- Payment processing
- Resource creation that shouldn't be duplicated
- Any non-idempotent operation that might be retried

---

## CORS Configuration

Allow cross-origin requests with appropriate headers:

```
Access-Control-Allow-Origin: https://myapp.com
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

---

## Health Endpoints

### Basic Health Check

```
GET /health

Response:
{
  "status": "healthy"
}
```

### Detailed Health Check (Internal)

```
GET /health/detailed

Response:
{
  "status": "healthy",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "externalApi": "degraded"
  },
  "version": "1.0.0",
  "uptime": "2d 5h 30m"
}
```

---

## Summary Checklist

- [ ] Resources are nouns (plural)
- [ ] HTTP methods used correctly
- [ ] Status codes are meaningful
- [ ] All collections paginated
- [ ] Consistent error format
- [ ] API versioned
- [ ] Rate limiting in place
- [ ] Authentication documented
- [ ] Health endpoints available
