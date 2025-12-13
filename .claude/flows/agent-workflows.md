# Agent Workflows

Multi-agent orchestration patterns for common development tasks.

## Feature Development (Full)

End-to-end feature implementation with all quality gates.

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEATURE DEVELOPMENT FLOW                      │
└─────────────────────────────────────────────────────────────────┘

User Request: "Add invoice management feature"
    │
    ▼
┌─────────────────┐
│ business-analyst│  Stage 1: ANALYZE
│                 │  ─────────────────
│ • User stories  │  Outputs:
│ • Domain rules  │  • docs/features/{feature}/requirements.md
│ • Permissions   │  • docs/domain/entities/{entity}.md
└────────┬────────┘  • docs/domain/business-rules.md (updated)
         │
         ▼
┌─────────────────┐
│backend-architect│  Stage 2: DESIGN
│                 │  ─────────────────
│ • API contract  │  Outputs:
│ • DB schema     │  • docs/features/{feature}/technical-design.md
│ • TSD document  │  • API endpoints, DTOs, database schema
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  abp-developer  │  Stage 3: IMPLEMENT
│                 │  ─────────────────
│ • Entity        │  Outputs:
│ • DTOs          │  • api/src/{Project}.Domain/{Feature}/
│ • AppService    │  • api/src/{Project}.Application/{Feature}/
│ • Validator     │  • api/src/{Project}.EntityFrameworkCore/{Feature}/
│ • EF Config     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   qa-engineer   │  Stage 4: TEST
│                 │  ─────────────────
│ • Unit tests    │  Outputs:
│ • Integration   │  • api/test/{Project}.Application.Tests/{Feature}/
│ • Test seeders  │  • api/test/{Project}.TestBase/{Feature}/
└────────┬────────┘  • docs/features/{feature}/test-cases.md
         │
         ▼
┌─────────────────┐
│abp-code-reviewer│  Stage 5: REVIEW
│                 │  ─────────────────
│ • Code quality  │  Outputs:
│ • ABP patterns  │  • Review comments
│ • Best practices│  • Suggested improvements
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│security-engineer│  Stage 6: SECURITY
│                 │  ─────────────────
│ • STRIDE review │  Outputs:
│ • OWASP check   │  • Security findings
│ • Auth audit    │  • Remediation recommendations
└─────────────────┘
```

### Command
```bash
/feature:add-feature invoice-management "Invoice creation with line items, PDF generation, payment tracking"
```

---

## Feature Development (Fast)

Skip analysis phase for well-defined requirements.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│backend-architect│ →  │  abp-developer  │ →  │   qa-engineer   │
│                 │    │                 │    │                 │
│ Design API      │    │ Implement       │    │ Write tests     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### When to Use
- Requirements are already clear
- Simple CRUD features
- Time-sensitive delivery

### Command
```bash
/feature:add-feature teacher-management "CRUD with Name, IsActive" --stage design
```

---

## Bug Fix Workflow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    debugger     │ →  │  abp-developer  │ →  │   qa-engineer   │
│                 │    │                 │    │                 │
│ Root cause      │    │ Implement fix   │    │ Add regression  │
│ analysis        │    │                 │    │ tests           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Inputs
- Error message/stack trace
- Reproduction steps
- Affected component

### Command
```bash
/debug:smart-debug "NullReferenceException in PatientAppService.GetAsync" --fix --verify
```

---

## Security Hardening Workflow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│security-engineer│ →  │  abp-developer  │ →  │abp-code-reviewer│
│                 │    │                 │    │                 │
│ Identify        │    │ Implement       │    │ Verify          │
│ vulnerabilities │    │ fixes           │    │ implementation  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Inputs
- Feature/component to audit
- Security requirements

### Example
```
Use the security-engineer agent to audit the authentication flow, then use abp-developer to implement fixes
```

---

## Database Migration Workflow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│backend-architect│ →  │database-migrator│ →  │  abp-developer  │
│                 │    │                 │    │                 │
│ Schema design   │    │ Generate        │    │ Update entity   │
│                 │    │ migration       │    │ configurations  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Command
```bash
/generate:migration AddTeacherTable --apply
```

---

## Code Review Workflow

```
┌─────────────────┐    ┌─────────────────┐
│abp-code-reviewer│ →  │security-engineer│
│                 │    │                 │
│ Quality review  │    │ Security review │
└─────────────────┘    └─────────────────┘
```

### Inputs
- PR number or file paths
- Review scope

### Example
```
Use the abp-code-reviewer agent to review the PatientAppService changes, then use security-engineer for security audit
```

---

## Test-Driven Development Workflow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   qa-engineer   │ →  │  abp-developer  │ →  │abp-code-reviewer│
│                 │    │                 │    │                 │
│ Write failing   │    │ Implement to    │    │ Review          │
│ tests (RED)     │    │ pass (GREEN)    │    │ (REFACTOR)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Command
```bash
/tdd:tdd-cycle "InvoiceAppService.CreateAsync"
```

---

## API Design Workflow

```
┌─────────────────┐    ┌─────────────────┐
│ business-analyst│ →  │backend-architect│
│                 │    │                 │
│ Requirements    │    │ API contract    │
│ User stories    │    │ Schema design   │
└─────────────────┘    └─────────────────┘
```

### Outputs
- `docs/features/{feature}/requirements.md`
- `docs/features/{feature}/technical-design.md`

---

## Agent Selection Matrix

| Workflow | Required Agents | Optional |
|----------|-----------------|----------|
| Feature (full) | BA → Arch → Dev → QA → Review | Security |
| Feature (fast) | Arch → Dev → QA | - |
| Bug fix | Debug → Dev | QA |
| Security hardening | Security → Dev → Review | - |
| DB migration | Arch → Migrator → Dev | - |
| Code review | Review | Security |
| TDD | QA → Dev → Review | - |
| API design | BA → Arch | - |

---

## Cross-References

- [AGENT-QUICK-REF.md](../AGENT-QUICK-REF.md) - Quick agent lookup
- [COMMAND-INDEX.md](../COMMAND-INDEX.md) - Command reference
- [crud-implementation.md](crud-implementation.md) - CRUD workflow
