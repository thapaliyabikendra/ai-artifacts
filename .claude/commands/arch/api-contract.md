---
name: api-contract
description: "Design API contract with OpenAPI specification"
args:
  - name: resource
    description: "Resource name (e.g., patients, appointments)"
    required: true
  - name: operations
    description: "Operations: crud | read-only | custom"
    required: false
    default: "crud"
  - name: format
    description: "Output format: yaml | markdown | both"
    required: false
    default: "both"
---

# Design API Contract

Resource: **$ARGUMENTS.resource**
Operations: **$ARGUMENTS.operations**
Format: **$ARGUMENTS.format**

## Instructions

### Step 1: Gather Context

1. Check if entity exists in `docs/domain/entities/`
2. Review existing API patterns in codebase
3. Identify related resources and relationships
4. Check permission requirements

### Step 2: Generate OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: [Resource] API
  description: API for managing [resource]
  version: 1.0.0

tags:
  - name: [Resource]
    description: [Resource] management operations

paths:
  /api/app/[resource]:
    get:
      tags:
        - [Resource]
      summary: Get list of [resource]
      operationId: get[Resource]List
      parameters:
        - $ref: '#/components/parameters/SkipCount'
        - $ref: '#/components/parameters/MaxResultCount'
        - $ref: '#/components/parameters/Sorting'
        - name: filter
          in: query
          schema:
            type: string
          description: Search filter
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]PagedResult'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
      security:
        - oauth2: ['[resource].read']

    post:
      tags:
        - [Resource]
      summary: Create a new [resource]
      operationId: create[Resource]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Create[Resource]Dto'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]Dto'
        '400':
          $ref: '#/components/responses/ValidationError'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
      security:
        - oauth2: ['[resource].create']

  /api/app/[resource]/{id}:
    get:
      tags:
        - [Resource]
      summary: Get [resource] by ID
      operationId: get[Resource]
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]Dto'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - oauth2: ['[resource].read']

    put:
      tags:
        - [Resource]
      summary: Update [resource]
      operationId: update[Resource]
      parameters:
        - $ref: '#/components/parameters/Id'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Update[Resource]Dto'
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/[Resource]Dto'
        '400':
          $ref: '#/components/responses/ValidationError'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - oauth2: ['[resource].update']

    delete:
      tags:
        - [Resource]
      summary: Delete [resource]
      operationId: delete[Resource]
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '204':
          description: Deleted
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - oauth2: ['[resource].delete']

components:
  schemas:
    [Resource]Dto:
      type: object
      properties:
        id:
          type: string
          format: uuid
        # Add entity-specific properties
        creationTime:
          type: string
          format: date-time
        lastModificationTime:
          type: string
          format: date-time
          nullable: true

    Create[Resource]Dto:
      type: object
      required:
        - name
      properties:
        # Add create-specific properties
        name:
          type: string
          maxLength: 100

    Update[Resource]Dto:
      type: object
      required:
        - name
      properties:
        # Add update-specific properties
        name:
          type: string
          maxLength: 100

    [Resource]PagedResult:
      type: object
      properties:
        totalCount:
          type: integer
          format: int64
        items:
          type: array
          items:
            $ref: '#/components/schemas/[Resource]Dto'

  parameters:
    Id:
      name: id
      in: path
      required: true
      schema:
        type: string
        format: uuid

    SkipCount:
      name: skipCount
      in: query
      schema:
        type: integer
        default: 0
        minimum: 0

    MaxResultCount:
      name: maxResultCount
      in: query
      schema:
        type: integer
        default: 10
        minimum: 1
        maximum: 1000

    Sorting:
      name: sorting
      in: query
      schema:
        type: string
      description: 'Sorting expression (e.g., "name asc, createdAt desc")'

  responses:
    ValidationError:
      description: Validation error
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: object
                properties:
                  code:
                    type: string
                  message:
                    type: string
                  validationErrors:
                    type: array
                    items:
                      type: object
                      properties:
                        field:
                          type: string
                        message:
                          type: string

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: object
                properties:
                  code:
                    type: string
                    example: "EntityNotFound"
                  message:
                    type: string

    Unauthorized:
      description: Authentication required

    Forbidden:
      description: Insufficient permissions

  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: /connect/authorize
          tokenUrl: /connect/token
          scopes:
            '[resource].read': Read [resource]
            '[resource].create': Create [resource]
            '[resource].update': Update [resource]
            '[resource].delete': Delete [resource]
```

### Step 3: Generate Markdown Documentation

```markdown
# [Resource] API Contract

## Overview

| Attribute | Value |
|-----------|-------|
| Base Path | `/api/app/[resource]` |
| Version | 1.0.0 |
| Auth | OAuth 2.0 |

## Endpoints

### List [Resources]

`GET /api/app/[resource]`

**Parameters:**

| Name | In | Type | Required | Description |
|------|----|----|----------|-------------|
| skipCount | query | integer | No | Records to skip (default: 0) |
| maxResultCount | query | integer | No | Max records (default: 10, max: 1000) |
| sorting | query | string | No | Sort expression |
| filter | query | string | No | Search filter |

**Response:** `200 OK`
```json
{
  "totalCount": 100,
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "name": "Example",
      "creationTime": "2024-01-01T00:00:00Z"
    }
  ]
}
```

**Permission:** `[Module].[Resource].Read`

---

### Get [Resource]

`GET /api/app/[resource]/{id}`

**Response:** `200 OK` | `404 Not Found`

**Permission:** `[Module].[Resource].Read`

---

### Create [Resource]

`POST /api/app/[resource]`

**Request Body:**
```json
{
  "name": "string (required, max 100)"
}
```

**Response:** `201 Created` | `400 Bad Request`

**Permission:** `[Module].[Resource].Create`

---

### Update [Resource]

`PUT /api/app/[resource]/{id}`

**Request Body:**
```json
{
  "name": "string (required, max 100)"
}
```

**Response:** `200 OK` | `400 Bad Request` | `404 Not Found`

**Permission:** `[Module].[Resource].Update`

---

### Delete [Resource]

`DELETE /api/app/[resource]/{id}`

**Response:** `204 No Content` | `404 Not Found`

**Permission:** `[Module].[Resource].Delete`

## Error Responses

| Code | Description |
|------|-------------|
| 400 | Validation error - check `validationErrors` array |
| 401 | Authentication required |
| 403 | Insufficient permissions |
| 404 | Resource not found |

## Data Transfer Objects

### [Resource]Dto
| Field | Type | Description |
|-------|------|-------------|
| id | uuid | Unique identifier |
| name | string | Display name |
| creationTime | datetime | Created timestamp |
| lastModificationTime | datetime? | Last update timestamp |

### Create[Resource]Dto
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | string | Yes | Max 100 chars |

### Update[Resource]Dto
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | string | Yes | Max 100 chars |
```

### Step 4: Output

1. Write OpenAPI spec to `docs/api/[resource].yaml`
2. Write Markdown to `docs/api/[resource].md`
3. Summarize endpoints created

## Related Skills

- `api-design-principles` - REST API best practices
- `api-response-patterns` - Response wrapper patterns
- `technical-design-patterns` - Full technical specifications
