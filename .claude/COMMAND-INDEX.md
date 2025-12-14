# Command Index

Centralized command discovery. 27 commands organized by action.

## Quick Lookup by Task

| I want to... | Command | Arguments |
|--------------|---------|-----------|
| Add a new feature | `/feature:add-feature` | `<name> "<requirements>"` |
| Scaffold entity | `/generate:entity` | `<EntityName> --properties "..."` |
| Generate filter DTO | `/generate:filter` | `<EntityName>` |
| Create migration | `/generate:migration` | `<migration-name>` |
| Generate docs | `/generate:doc-generate` | `<target>` |
| Create API mocks | `/generate:api-mock` | `<api-spec>` |
| Run TDD cycle | `/tdd:tdd-cycle` | `"<feature>" [--phase red\|green\|refactor]` |
| Audit permissions | `/review:permissions` | `[--unused] [--matrix]` |
| Review before push | `/review:pre-push` | `[--no-block] [--base <branch>]` |
| Audit tech stack | `/review:tech-stack-audit` | `[--fix] [--skills]` |
| Debug an error | `/debug:smart-debug` | `"<error>" [--fix]` |
| Analyze tech debt | `/refactor:tech-debt` | `[<path>]` |
| Clean up code | `/refactor:refactor-clean` | `<file-or-folder>` |
| Audit dependencies | `/refactor:deps-audit` | `[<path>]` |
| Resolve GitHub issue | `/team:issue` | `<issue-number>` |
| Generate standup notes | `/team:standup-notes` | `[--days N]` |
| Explain code | `/explain:code-explain` | `<file-or-code>` |
| Generate test plan | `/qa:test-plan` | `<feature> [--type unit\|integration\|e2e]` |
| Analyze coverage | `/qa:coverage-report` | `[--scope module\|full]` |
| Generate tests | `/qa:generate-tests` | `<target> [--type unit\|integration]` |
| Create user story | `/ba:user-story` | `<feature> [--role user]` |
| Analyze impact | `/ba:impact-analysis` | `<change> [--scope quick\|full]` |
| Generate release notes | `/ba:release-notes` | `<version> [--from tag]` |
| Create ADR | `/arch:adr` | `<title> [--number N]` |
| Create system design | `/arch:system-design` | `<feature> [--scope module\|system]` |
| Design API contract | `/arch:api-contract` | `<resource> [--operations crud]` |
| Optimize markdown docs | `/docs:optimize-md` | `<path> [--profile <type>] [--mode audit\|apply\|check]` |

## Commands by Category

### Feature Development
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/feature:add-feature` | End-to-end feature with agents | `<feature-name> "<requirements>" [--stage <stage>] [--dry-run]` |

### Code Generation
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/generate:entity` | Scaffold ABP entity + all layers | `<EntityName> [--properties "Name:string"] [--fast] [--audit full\|basic\|none]` |
| `/generate:filter` | Generate filter DTO | `<EntityName> [--properties "Name:string,Status:bool?"]` |
| `/generate:migration` | EF Core migration | `<migration-name> [--apply] [--dry-run]` |
| `/generate:doc-generate` | Auto-generate documentation | `<target>` |
| `/generate:api-mock` | Create API mock services | `<api-spec>` |

### Test-Driven Development
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/tdd:tdd-cycle` | Full red-green-refactor | `"<feature>" [--phase red\|green\|refactor] [--incremental]` |

### Quality Assurance
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/qa:test-plan` | Generate test plan from requirements | `<feature> [--type unit\|integration\|e2e\|all]` |
| `/qa:coverage-report` | Analyze test coverage gaps | `[--scope module\|full] [--module name]` |
| `/qa:generate-tests` | Auto-generate tests for untested code | `<target> [--type unit\|integration] [--dry-run]` |

### Business Analysis
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/ba:user-story` | Generate user story with AC | `<feature> [--role user] [--output path]` |
| `/ba:impact-analysis` | Analyze change impact | `<change> [--scope quick\|full]` |
| `/ba:release-notes` | Generate release notes | `<version> [--from tag] [--format markdown\|slack]` |

### Architecture
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/arch:adr` | Create Architecture Decision Record | `<title> [--number N]` |
| `/arch:system-design` | Create system design document | `<feature> [--scope component\|module\|system]` |
| `/arch:api-contract` | Design API contract (OpenAPI) | `<resource> [--operations crud\|read-only] [--format yaml\|markdown]` |

### Code Review & Audit
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/review:permissions` | Audit ABP permissions | `[--unused] [--unprotected] [--matrix]` |
| `/review:pre-push` | Fast security scan before push (<30s) | `[--no-block] [--base <branch>]` |
| `/review:tech-stack-audit` | Audit skills for wrong tech | `[--fix] [--skills] [--commands] [--verbose]` |

### Debugging
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/debug:smart-debug` | AI root cause analysis + fix | `"<error>" [--fix] [--verify]` |

### Refactoring
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/refactor:tech-debt` | Analyze technical debt | `[<path>]` |
| `/refactor:refactor-clean` | Clean code refactoring | `<file-or-folder>` |
| `/refactor:deps-audit` | Dependency security audit | `[<path>]` |

### Team Collaboration
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/team:issue` | Resolve GitHub issue | `<issue-number>` |
| `/team:standup-notes` | Generate standup notes | `[--days N]` |

### Code Explanation
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/explain:code-explain` | Explain complex code | `<file-or-code>` |

### Documentation Optimization
| Command | Purpose | Arguments |
|---------|---------|-----------|
| `/docs:optimize-md` | Analyze and optimize markdown files | `<path> [--profile <type>] [--mode audit\|apply\|check] [--max-lines N]` |

---

## Command Bundles

### development-cycle
Full development workflow commands.

| Command | Purpose |
|---------|---------|
| `/feature:add-feature` | End-to-end feature development |
| `/generate:entity` | Scaffold entity + layers |
| `/generate:filter` | Filter DTO for queries |
| `/generate:migration` | Database migration |

### quality-assurance
Code quality and testing commands.

| Command | Purpose |
|---------|---------|
| `/tdd:tdd-cycle` | TDD red-green-refactor workflow |
| `/qa:test-plan` | Generate test plan from requirements |
| `/qa:coverage-report` | Analyze test coverage gaps |
| `/qa:generate-tests` | Auto-generate tests for untested code |
| `/review:permissions` | Permission audit |
| `/review:pre-push` | AI review before git push |
| `/refactor:tech-debt` | Technical debt analysis |
| `/refactor:refactor-clean` | Code cleanup and refactoring |

### security-compliance
Security and dependency commands.

| Command | Purpose |
|---------|---------|
| `/refactor:deps-audit` | Dependency vulnerabilities |
| `/review:permissions` | Authorization audit |

### collaboration
Team workflow commands.

| Command | Purpose |
|---------|---------|
| `/team:issue` | GitHub issue resolution |
| `/team:standup-notes` | Generate standup notes |
| `/ba:user-story` | Generate user story with acceptance criteria |
| `/ba:impact-analysis` | Analyze change impact |
| `/ba:release-notes` | Generate release notes |

### architecture
Architecture and design commands.

| Command | Purpose |
|---------|---------|
| `/arch:adr` | Create Architecture Decision Record |
| `/arch:system-design` | Create system design document |
| `/arch:api-contract` | Design API contract (OpenAPI) |

### documentation
Documentation and explanation commands.

| Command | Purpose |
|---------|---------|
| `/generate:doc-generate` | Auto-generate docs |
| `/explain:code-explain` | Code explanation |
| `/generate:api-mock` | API mock generation |
| `/docs:optimize-md` | Markdown optimization |

---

## Command-Agent Mapping

Commands that orchestrate specialized agents:

| Command | Agents Used | Models |
|---------|-------------|--------|
| `/feature:add-feature` | business-analyst → backend-architect → abp-developer → qa-engineer → abp-code-reviewer → security-engineer | haiku → haiku → sonnet → haiku → haiku → haiku |
| `/debug:smart-debug` | debugger → abp-developer → qa-engineer → abp-code-reviewer | sonnet → sonnet → haiku → haiku |
| `/tdd:tdd-cycle` | qa-engineer → abp-developer → abp-code-reviewer | sonnet → sonnet → haiku |
| `/review:pre-push` | (none - direct execution) | haiku |
| `/generate:entity` | abp-developer | sonnet |
| `/generate:migration` | database-migrator | sonnet |

**Commands without agents** (direct execution):
- `/generate:filter` - Template-based generation
- `/review:permissions` - Read-only code analysis
- `/refactor:tech-debt` - Static analysis
- `/refactor:refactor-clean` - Direct refactoring
- `/refactor:deps-audit` - Dependency scanning
- `/team:issue` - GitHub API integration
- `/team:standup-notes` - Git/Jira data collection
- `/explain:code-explain` - Code analysis
- `/generate:doc-generate` - Documentation extraction
- `/generate:api-mock` - Mock server setup

---

## Command Selection Flowchart

```
What do you need?
│
├─ New feature end-to-end? → /feature:add-feature
│
├─ Generate code?
│   ├─ Full entity + layers → /generate:entity
│   ├─ Entity + layers (fast) → /generate:entity --fast
│   ├─ Filter DTO → /generate:filter
│   ├─ DB migration → /generate:migration
│   ├─ Documentation → /generate:doc-generate
│   └─ API mocks → /generate:api-mock
│
├─ Test-driven development?
│   ├─ Full TDD cycle → /tdd:tdd-cycle
│   ├─ Write tests only → /tdd:tdd-cycle --phase red
│   ├─ Implement only → /tdd:tdd-cycle --phase green
│   └─ Refactor only → /tdd:tdd-cycle --phase refactor
│
├─ Review/audit?
│   ├─ Before push → /review:pre-push
│   ├─ Permissions → /review:permissions
│   ├─ Tech debt → /refactor:tech-debt
│   └─ Dependencies → /refactor:deps-audit
│
├─ Debug an error? → /debug:smart-debug
│
├─ Refactor code? → /refactor:refactor-clean
│
├─ Team tasks?
│   ├─ GitHub issue → /team:issue
│   └─ Standup notes → /team:standup-notes
│
├─ Understand code? → /explain:code-explain
│
└─ Optimize documentation? → /docs:optimize-md
    (Use `--profile guidelines` for GUIDELINES.md ecosystem)
```

## Argument Patterns

### Standard Patterns
```bash
# Entity-based commands
/generate:entity Teacher --properties "Name:string,IsActive:bool"
/generate:entity Invoice --properties "Number:string,Amount:decimal" --fast
/generate:filter Patient --properties "Name:string,Status:PatientStatus?"

# Feature commands
/feature:add-feature patient-management "CRUD for patients with name, email, DOB"
/feature:add-feature invoice-system "Invoice generation and payment tracking" --stage design

# TDD commands (consolidated with --phase option)
/tdd:tdd-cycle "PatientAppService.CreateAsync"
/tdd:tdd-cycle "Invoice validation rules" --phase red
/tdd:tdd-cycle "Invoice validation rules" --phase refactor

# Debug commands
/debug:smart-debug "NullReferenceException in PatientAppService.GetAsync" --fix

# Review commands
/review:permissions --unused --matrix
```

## Command vs Skill vs Agent

| Need | Use |
|------|-----|
| User-invoked action with arguments | **Command** (`/generate:entity Patient`) |
| Auto-triggered domain knowledge | **Skill** (auto-loaded when needed) |
| Complex multi-step, isolated context | **Agent** (delegated task) |

## Reference Files

Commands reference detailed patterns in `.claude/commands/references/`:

| Reference | Used By |
|-----------|---------|
| `api-mock-templates.md` | `/generate:api-mock` |
| `pre-push-templates.md` | `/review:pre-push` |
| `refactor-patterns.md` | `/refactor:refactor-clean` |
| `code-explain-templates.md` | `/explain:code-explain` |
| `deps-audit-patterns.md` | `/refactor:deps-audit` |
| `standup-templates.md` | `/team:standup-notes` |
| `doc-templates.md` | `/generate:doc-generate` |
