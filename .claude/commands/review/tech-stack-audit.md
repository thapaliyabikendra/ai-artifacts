---
description: Audit Claude artifacts for tech stack violations (wrong languages, frameworks)
allowed-tools: Read, Glob, Grep
argument-hint: [--fix] [--skills] [--commands] [--verbose]
---

# Tech Stack Audit Command

Scan Claude artifacts (skills, commands, references) for code examples that don't match the project's tech stack.

**Arguments**: $ARGUMENTS

## Project Tech Stack

| Layer | Allowed | Forbidden |
|-------|---------|-----------|
| **Backend** | C#, .NET, ABP Framework | Python, Java, Go, Ruby |
| **Frontend** | TypeScript, React, JavaScript | Angular, Vue, Svelte |
| **Database** | PostgreSQL, EF Core | MongoDB, MySQL syntax |
| **Testing Backend** | xUnit, NSubstitute, Shouldly | pytest, JUnit, NUnit |
| **Testing Frontend** | Jest, Vitest, Playwright | Cypress, Mocha, Jasmine |
| **API Mocking** | MSW (Node.js), WireMock.Net | FastAPI mocks, Flask |

## Workflow

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. Scan      │ → │ 2. Extract   │ → │ 3. Classify  │ → │ 4. Report    │
│ Artifacts    │   │ Code Blocks  │   │ Violations   │   │ & Suggest    │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

## Execution

### Step 1: Scan Artifacts

Scan all Claude artifact locations:

```
Skills:    .claude/skills/**/*.md
Commands:  .claude/commands/**/*.md
References: .claude/commands/references/*.md
           .claude/skills/**/references/*.md
```

### Step 2: Extract Code Blocks

For each file, extract fenced code blocks and their language:

**Forbidden Patterns:**
```
```python          → Python code (use C# or TypeScript)
```py              → Python shorthand
```ruby           → Ruby code
```java           → Java code
```go             → Go code
import .* from    → In Python context
def .*:           → Python function
from .* import    → Python import
cy\.              → Cypress syntax
```

**Allowed Patterns:**
```
```csharp         → C# code ✓
```typescript     → TypeScript code ✓
```javascript     → JavaScript code ✓
```sql           → SQL (PostgreSQL) ✓
```yaml          → Configuration ✓
```json          → Data format ✓
```bash          → Shell commands ✓
```mermaid       → Diagrams ✓
```markdown      → Documentation ✓
```

### Step 3: Classify Violations

**Severity Levels:**

| Severity | Condition | Action |
|----------|-----------|--------|
| 🔴 HIGH | Backend code in Python/Java/Go | Must fix |
| 🟡 MEDIUM | Test code using Cypress/pytest | Should fix |
| 🟢 LOW | Minor language inconsistency | Nice to fix |
| ⚪ INFO | Tech stack not declared in frontmatter | Suggest adding |

### Step 4: Generate Report

## Output Format

```markdown
## Tech Stack Audit Report

**Scan Date**: {Date}
**Artifacts Scanned**: {Count}
**Violations Found**: {Count}

### Summary

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 HIGH | {n} | Requires fix |
| 🟡 MEDIUM | {n} | Should fix |
| 🟢 LOW | {n} | Optional |

### Violations by File

#### 🔴 HIGH: {file_path}

**Location**: Line {n}
**Language Found**: `python`
**Expected**: `csharp` or `typescript`

```python
# Violating code block
def example():
    pass
```

**Recommendation**: Replace with C# equivalent:
```csharp
public void Example()
{
}
```

---

#### 🟡 MEDIUM: {file_path}

**Location**: Line {n}
**Issue**: Cypress test syntax found
**Expected**: Playwright

```typescript
// Found
cy.get('[data-testid="email"]').type('test@example.com');

// Expected
await page.getByTestId('email').fill('test@example.com');
```

---

### Missing Tech Stack Declarations

| Skill | Location | Recommendation |
|-------|----------|----------------|
| error-handling-patterns | .claude/skills/... | Add `tech_stack: [dotnet, csharp]` |
| react-development-patterns | .claude/skills/... | Add `tech_stack: [typescript, react]` |

### Quick Fix Commands

To fix HIGH severity issues:
```bash
# Review and fix each file
claude "Fix tech stack violations in {file_path} - replace Python with C#"
```

### Recommendations

1. **Immediate**: Fix all HIGH severity violations
2. **Soon**: Fix MEDIUM severity (testing framework mismatches)
3. **Maintenance**: Add `tech_stack` to all skill frontmatters
```

## Options

| Option | Effect |
|--------|--------|
| `--fix` | Attempt to auto-fix violations (spawns agents) |
| `--skills` | Only scan skills |
| `--commands` | Only scan commands |
| `--verbose` | Show all files, including clean ones |

## Patterns to Detect

### Backend Violations

| Pattern | Severity | Replacement |
|---------|----------|-------------|
| `def .*\(.*\):` | HIGH | C# method |
| `import .*` (Python) | HIGH | C# using |
| `from .* import` | HIGH | C# using |
| `@pytest` | MEDIUM | xUnit attribute |
| `async def` (Python) | HIGH | `async Task` |

### Frontend Violations

| Pattern | Severity | Replacement |
|---------|----------|-------------|
| `cy\.get` | MEDIUM | `page.locator` |
| `cy\.visit` | MEDIUM | `page.goto` |
| `cy\.intercept` | MEDIUM | `page.route` |
| `describe\(.*cy` | MEDIUM | Playwright test |

### Framework Violations

| Pattern | Severity | Replacement |
|---------|----------|-------------|
| `FastAPI` | HIGH | ABP AppService |
| `Flask` | HIGH | ABP AppService |
| `Django` | HIGH | ABP AppService |
| `Express` | MEDIUM | Keep for mocking only |

## Frontmatter Validation

Skills should declare their tech stack:

```yaml
---
name: skill-name
tech_stack: [dotnet, csharp, typescript, react]  # Required
---
```

**Valid tech_stack values:**
- Backend: `dotnet`, `csharp`, `abp`, `efcore`
- Frontend: `typescript`, `react`, `javascript`
- Testing: `xunit`, `playwright`, `jest`, `vitest`
- Infrastructure: `docker`, `postgresql`, `redis`

## Integration

This command can be run:
- **Pre-commit**: Block commits with HIGH violations
- **CI/CD**: Fail pipeline if violations found
- **Scheduled**: Weekly audit for drift detection

```yaml
# .github/workflows/tech-stack-audit.yml
- name: Audit Tech Stack
  run: claude "/review:tech-stack-audit --skills --commands"
```
