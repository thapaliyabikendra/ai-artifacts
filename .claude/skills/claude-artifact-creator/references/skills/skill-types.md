# Skill Types and Archetypes

Skills fall into distinct categories, each with characteristic patterns and best practices.

## Overview

| Type | Purpose | Heavy On | Example |
|------|---------|----------|---------|
| Tool | File/format processing | scripts/ | docker-dotnet-containerize |
| Domain | Business knowledge | references/ | postgresql |
| Workflow | Multi-step processes | phases | code-review-excellence |
| Integration | API/service connections | auth + errors | github-api |
| Analysis | Audits/assessments | classification | security-audit |
| Generator | Code/file creation | templates | crud-service |
| Pattern | Best practices | examples | error-handling-patterns |

---

## 1. Tool Skills

**Purpose:** Handle specific file formats, tools, or technologies.

**Examples:** PDF processor, DOCX editor, image manipulator, Docker generator

**Characteristics:**
- Focus on a single format or tool
- Heavy use of `scripts/` for deterministic operations
- Clear input/output transformations
- Often stateless (each operation independent)

**Structure:**
```
pdf-processor/
├── SKILL.md
│   ├── Quick start with common operations
│   ├── Decision tree for operation selection
│   └── Links to detailed references
├── scripts/
│   ├── extract_text.py
│   ├── merge_pdfs.py
│   └── fill_form.py
└── references/
    ├── api-reference.md
    └── troubleshooting.md
```

**SKILL.md Pattern:**
```markdown
# PDF Processor

## Quick Start

**Extract text:**
```bash
python scripts/extract_text.py input.pdf output.txt
```

## Operation Selection

What do you need to do?

| Task | Script | Example |
|------|--------|---------|
| Extract content | `extract.py` | `python scripts/extract.py doc.pdf` |
| Merge files | `merge.py` | `python scripts/merge.py a.pdf b.pdf` |
| Fill forms | `fill_form.py` | See [Form Guide](references/forms.md) |
```

**Best Practices:**
- Scripts should be self-contained and testable
- Provide both CLI usage and programmatic examples
- Include error handling guidance
- Document supported versions/formats

**Codebase Example:** `docker-dotnet-containerize`

---

## 2. Domain Skills

**Purpose:** Encode business logic, schemas, policies, or organizational knowledge.

**Examples:** Database schemas, API documentation, company policies, brand guidelines

**Characteristics:**
- Heavy use of `references/` for domain knowledge
- Minimal or no scripts
- Context-specific constraints
- Often used alongside other skills

**Structure:**
```
company-database/
├── SKILL.md
│   ├── Schema overview
│   ├── Common query patterns
│   └── Navigation to detailed docs
└── references/
    ├── schema/
    │   ├── users.md
    │   ├── orders.md
    │   └── products.md
    ├── relationships.md
    └── naming-conventions.md
```

**SKILL.md Pattern:**
```markdown
# Company Database Schema

## Overview

Core tables: `users`, `orders`, `products`

## Common Patterns

**Find user orders:**
```sql
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.email = ?
```

## Schema References

- [Users Schema](references/schema/users.md)
- [Orders Schema](references/schema/orders.md)
- [Relationships](references/relationships.md)

## Conventions

- Table names: plural, snake_case
- Primary keys: `id` (UUID)
- Timestamps: `created_at`, `updated_at`
```

**Best Practices:**
- Organize references by domain area
- Include examples for common queries/operations
- Document conventions and constraints
- Keep SKILL.md as navigation hub

**Codebase Example:** `postgresql`

---

## 3. Workflow Skills

**Purpose:** Guide multi-step processes with decision points and phases.

**Examples:** Code review process, onboarding procedure, refactoring workflow

**Characteristics:**
- Phased execution (Assessment → Implementation → Validation)
- User input gathering at start
- Decision trees for branching logic
- Explicit deliverables at each phase

**Structure:**
```
code-refactoring/
├── SKILL.md
│   ├── User input gathering
│   ├── Phase overview
│   ├── Decision tree
│   └── Deliverables checklist
└── references/
    ├── patterns/
    │   ├── extract-method.md
    │   └── rename-variable.md
    └── validation-checklist.md
```

**SKILL.md Pattern:**
```markdown
# Code Refactoring Workflow

## User Input Required

Before starting, clarify:
1. **Scope**: Which files/modules?
2. **Goals**: Performance, readability, maintainability?
3. **Constraints**: Breaking changes allowed?

## Process Overview

```
Phase 1: Assessment     → Identify issues
Phase 2: Planning       → Prioritize, design approach
Phase 3: Implementation → Apply changes
Phase 4: Validation     → Verify, document
```

## Phase 1: Assessment

### 1.1 Analyze Current State
[Detailed steps]

### 1.2 Create Inventory
**High Priority:** [criteria]
**Medium Priority:** [criteria]
**Low Priority:** [criteria]

## Deliverables
- [ ] All changes applied
- [ ] Tests pass
- [ ] Documentation updated
```

**Best Practices:**
- Always start with user input gathering
- Provide clear phase boundaries
- Include rollback/recovery guidance
- Define explicit deliverables

**Codebase Example:** `code-review-excellence`

---

## 4. Integration Skills

**Purpose:** Connect with external services, APIs, or systems.

**Examples:** GitHub integration, Slack notifications, cloud APIs

**Characteristics:**
- Authentication/credential handling
- API endpoint documentation
- Error handling for network operations
- Rate limiting awareness

**Structure:**
```
github-integration/
├── SKILL.md
│   ├── Authentication setup
│   ├── Common operations
│   └── Error handling
├── scripts/
│   ├── create_pr.py
│   └── fetch_issues.py
└── references/
    ├── api-endpoints.md
    ├── authentication.md
    └── rate-limits.md
```

**SKILL.md Pattern:**
```markdown
# GitHub Integration

## Authentication

**Required credentials:**
- `GITHUB_TOKEN`: Personal access token with `repo` scope

**Setup:**
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

## Common Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| Create PR | `gh pr create` | Open new pull request |
| List issues | `gh issue list` | Show open issues |

## Error Handling

| Code | Meaning | Resolution |
|------|---------|------------|
| 401 | Unauthorized | Check token |
| 403 | Rate limited | Wait or authenticate |
| 404 | Not found | Verify resource exists |

## Rate Limits

- Authenticated: 5000 requests/hour
- Unauthenticated: 60 requests/hour
```

**Best Practices:**
- Never hardcode credentials
- Document all required permissions
- Include comprehensive error handling
- Provide rate limit guidance

---

## 5. Analysis Skills

**Purpose:** Examine, audit, or assess codebases, data, or systems.

**Examples:** Security audit, performance analysis, code quality assessment

**Characteristics:**
- Classification frameworks for findings
- Severity/priority rankings
- Report generation templates
- Actionable recommendations

**Structure:**
```
security-audit/
├── SKILL.md
│   ├── Scope definition
│   ├── Analysis checklist
│   ├── Classification framework
│   └── Report template
└── references/
    ├── vulnerabilities/
    │   ├── injection.md
    │   └── xss.md
    └── remediation-guides.md
```

**SKILL.md Pattern:**
```markdown
# Security Audit

## Scope Definition

Define boundaries:
1. **Target**: Which components?
2. **Depth**: Quick scan or deep analysis?
3. **Focus**: All vulnerabilities or specific?

## Analysis Checklist

- [ ] Input validation
- [ ] Authentication
- [ ] Authorization
- [ ] Data encryption

## Classification Framework

**Critical (P0):** RCE, auth bypass, data exposure
**High (P1):** SQL injection, XSS, privilege escalation
**Medium (P2):** CSRF, info disclosure
**Low (P3):** Missing headers, verbose errors

## Report Template

# Security Audit Report

## Executive Summary
[Overview]

## Findings

### [Finding Title]
- **Severity**: Critical/High/Medium/Low
- **Location**: [file:line]
- **Description**: [What was found]
- **Remediation**: [How to fix]
```

**Best Practices:**
- Provide clear classification criteria
- Include remediation guidance
- Generate actionable reports
- Link to detailed vulnerability references

---

## 6. Generator Skills

**Purpose:** Create code, files, or configurations from templates.

**Examples:** CRUD service generator, component scaffolder, API endpoint creator

**Characteristics:**
- Template-based generation
- Placeholder conventions
- Multi-file output
- Post-generation steps

**Structure:**
```
crud-service/
├── SKILL.md
│   ├── Workflow (gather → generate → verify)
│   ├── Placeholder conventions
│   └── Post-generation steps
└── references/
    ├── appservice-template.md
    ├── dto-templates.md
    └── validator-template.md
```

**SKILL.md Pattern:**
```markdown
# CRUD Service Generator

## Workflow

1. **Gather information:**
   - Entity Name (e.g., "Product")
   - Properties (e.g., "Name:string, Price:decimal")
   - Namespace (e.g., "ProductManagement")

2. **Generate files:**
   - `{EntityName}AppService.cs` → [appservice-template.md]
   - `I{EntityName}AppService.cs` → [interface-template.md]
   - DTOs → [dto-templates.md]

3. **Replace placeholders:**

| Placeholder | Format | Example |
|-------------|--------|---------|
| `{EntityName}` | PascalCase | Product |
| `{entityName}` | camelCase | product |
| `{entity-name}` | kebab-case | product |

## Post-Generation Steps

1. Register in DI container
2. Configure AutoMapper
3. Add to module
```

**Best Practices:**
- Define placeholder conventions clearly
- Show generated file structure
- Include post-generation checklist
- Provide customization options

**Codebase Example:** `crud-service`

---

## 7. Pattern Skills

**Purpose:** Document best practices, design patterns, and coding standards.

**Examples:** Error handling patterns, async patterns, testing strategies

**Characteristics:**
- Heavy use of before/after examples
- Language/framework-specific sections
- Anti-pattern documentation
- Decision guidance

**Structure:**
```
error-handling-patterns/
├── SKILL.md
│   ├── Pattern overview
│   ├── Decision tree
│   ├── Examples by language
│   └── Anti-patterns
└── references/
    ├── exceptions.md
    ├── result-types.md
    └── logging.md
```

**SKILL.md Pattern:**
```markdown
# Error Handling Patterns

## When to Use What

| Scenario | Pattern | Why |
|----------|---------|-----|
| Expected failures | Result type | Explicit handling |
| Programmer errors | Exceptions | Fail fast |
| Recoverable errors | Retry + fallback | Resilience |

## Pattern Examples

### Exceptions (Traditional)

**Before:**
```python
def get_user(id):
    return db.query(f"SELECT * FROM users WHERE id = {id}")
```

**After:**
```python
def get_user(id: str) -> User:
    try:
        result = db.query("SELECT * FROM users WHERE id = ?", [id])
        if not result:
            raise UserNotFoundError(f"User {id} not found")
        return User.from_row(result)
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise
```

### Result Types (Functional)

```typescript
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

function getUser(id: string): Result<User, UserError> {
    const user = db.findUser(id);
    if (!user) {
        return { ok: false, error: { code: 'NOT_FOUND', id } };
    }
    return { ok: true, value: user };
}
```

## Anti-Patterns

❌ **Swallowing exceptions:**
```python
try:
    risky_operation()
except:
    pass  # Never do this
```

❌ **Using exceptions for control flow:**
```python
try:
    return cache[key]
except KeyError:
    return compute(key)  # Use .get() instead
```
```

**Best Practices:**
- Show concrete before/after examples
- Include multiple language examples
- Document anti-patterns explicitly
- Provide decision trees for choosing patterns

**Codebase Examples:** `error-handling-patterns`, `dotnet-async-patterns`, `api-design-principles`

---

## Choosing the Right Type

| If the skill... | Consider... |
|-----------------|-------------|
| Handles a specific file format | Tool |
| Encodes organizational knowledge | Domain |
| Guides multi-step processes | Workflow |
| Connects to external services | Integration |
| Examines and reports on systems | Analysis |
| Creates files from templates | Generator |
| Documents best practices | Pattern |

**Hybrid Skills:** Many skills combine types:

- A "deployment skill" might be Workflow + Integration + Tool
- A "database skill" might be Domain + Generator + Pattern

Start with the primary type, then incorporate patterns from others as needed.

---

## Role-Based Type Selection

| Role | Common Types | Why |
|------|--------------|-----|
| Backend Architect | Domain, Analysis, Workflow | System design, reviews |
| Backend Developer | Generator, Tool, Integration | Code generation, APIs |
| Frontend Developer | Generator, Tool, Workflow | Components, builds |
| Product Manager | Domain, Workflow, Analysis | Requirements, processes |
| QA Engineer | Analysis, Workflow, Tool | Testing, validation |
| Security Engineer | Analysis, Workflow | Audits, assessments |
| DevOps Engineer | Tool, Integration, Workflow | CI/CD, infrastructure |

See [role-based-design.md](role-based-design.md) for detailed guidance by role.
