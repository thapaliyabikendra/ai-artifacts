# Architecture Decision Records (ADR)

> **Owner**: backend-architect
> **Purpose**: Document significant technical and architectural decisions
> **Format**: Based on [Michael Nygard's ADR format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

---

## Decision Log

| ID | Title | Status | Date |
|----|-------|--------|------|
| ADR-001 | Use ABP Framework for Application Architecture | Accepted | 2025-12-10 |
| ADR-002 | Use PostgreSQL as Primary Database | Accepted | 2025-12-10 |
| ADR-003 | Use OpenIddict for OAuth 2.0 Authentication | Accepted | 2025-12-10 |

---

## ADR-001: Use ABP Framework for Application Architecture

**Status**: Accepted
**Date**: 2025-12-10
**Deciders**: backend-architect

### Context

We need to build a Clinic Management System with:
- RESTful API
- Domain-Driven Design patterns
- Role-based authorization
- Multi-tenancy support (future)
- Rapid development capabilities

### Decision

Use ABP Framework 10.0.1 as the application foundation.

### Rationale

**Pros**:
- Built-in DDD patterns (entities, repositories, domain services)
- Pre-built modules for auth, permissions, audit logging
- Code generation tools reduce boilerplate
- Active community and documentation
- Layered architecture enforces separation of concerns

**Cons**:
- Learning curve for developers new to ABP
- Framework updates may require migration effort
- Opinionated structure may limit flexibility

### Consequences

- All backend developers must learn ABP conventions
- Project structure follows ABP layered architecture
- Use ABP's repository and unit of work patterns
- Leverage ABP's permission system for RBAC

### Alternatives Considered

1. **Clean Architecture from scratch**: More flexibility but more boilerplate
2. **ASP.NET Core minimal APIs**: Simpler but lacks DDD infrastructure
3. **MediatR + CQRS**: Good for complex domains but overkill for this scope

---

## ADR-002: Use PostgreSQL as Primary Database

**Status**: Accepted
**Date**: 2025-12-10
**Deciders**: backend-architect

### Context

Need a relational database that supports:
- ACID transactions
- Complex queries for reporting
- JSON data types for flexible fields
- Good performance at clinic scale

### Decision

Use PostgreSQL as the primary database with Entity Framework Core.

### Rationale

**Pros**:
- Open source and cost-effective
- Excellent JSON support for semi-structured data
- Strong ACID compliance
- Rich feature set (CTEs, window functions)
- Good EF Core support

**Cons**:
- Team may have more SQL Server experience
- Fewer managed hosting options than SQL Server in some clouds

### Consequences

- Use Npgsql as the EF Core provider
- Database migrations via EF Core code-first
- Connection strings use PostgreSQL format
- May need to handle PostgreSQL-specific syntax in raw queries

### Alternatives Considered

1. **SQL Server**: Better tooling but licensing costs
2. **MySQL**: Similar features but PostgreSQL has better JSON support
3. **MongoDB**: Good for documents but relational model suits clinic data better

---

## ADR-003: Use OpenIddict for OAuth 2.0 Authentication

**Status**: Accepted
**Date**: 2025-12-10
**Deciders**: backend-architect, security-engineer

### Context

Need OAuth 2.0 / OpenID Connect authentication for:
- Secure token-based authentication
- Support for multiple client types (SPA, mobile)
- Integration with ASP.NET Identity
- ABP Framework compatibility

### Decision

Use OpenIddict as the OAuth 2.0 / OpenID Connect server.

### Rationale

**Pros**:
- Native ABP Framework integration
- Full OAuth 2.0 and OpenID Connect support
- Works with ASP.NET Identity
- Active development and community
- Supports authorization code flow with PKCE

**Cons**:
- Requires dedicated AuthServer project
- More complex than simple JWT authentication

### Consequences

- Separate AuthServer project for token management
- Frontend must implement OAuth flows (PKCE for SPA)
- Token validation middleware in API
- Refresh token support for long-lived sessions

### Alternatives Considered

1. **IdentityServer4/Duende**: Mature but commercial licensing
2. **Simple JWT**: Easier but lacks standard OAuth flows
3. **Azure AD B2C**: Good for large scale but external dependency

---

## ADR Template

```markdown
## ADR-XXX: [Title]

**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Date**: YYYY-MM-DD
**Deciders**: [agent-names or human names]

### Context

[What is the issue that we're seeing that is motivating this decision?]

### Decision

[What is the change that we're proposing and/or doing?]

### Rationale

**Pros**:
- [Benefit 1]
- [Benefit 2]

**Cons**:
- [Drawback 1]
- [Drawback 2]

### Consequences

[What becomes easier or more difficult because of this change?]

### Alternatives Considered

1. **[Alternative 1]**: [Why not chosen]
2. **[Alternative 2]**: [Why not chosen]
```

---

## 🔗 Related Documents

- [[technical-specification]] - Implementation of these decisions
- [[security-audit]] - Security implications
- [[center-knowledge-base]] - Project overview
