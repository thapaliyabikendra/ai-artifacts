# Role-Based Skill Design

Design skills that work effectively for different team roles. Each role has distinct needs, deliverables, and workflow patterns.

## Role Overview

| Role | Primary Skill Types | Key Focus Areas |
|------|---------------------|-----------------|
| Backend Architect | Domain, Analysis, Workflow | System design, API contracts, data modeling |
| Backend Developer | Generator, Tool, Integration | Code generation, CRUD operations, API integration |
| Frontend Developer | Generator, Tool, Workflow | Components, state management, UI patterns |
| Product Manager | Domain, Workflow, Analysis | Requirements, acceptance criteria, prioritization |
| QA Engineer | Analysis, Workflow, Tool | Test generation, coverage analysis, validation |
| Security Engineer | Analysis, Workflow | Vulnerability assessment, compliance, audits |
| DevOps Engineer | Tool, Integration, Workflow | CI/CD, containerization, infrastructure |

---

## Backend Architect

**Primary Concerns:** System boundaries, data flow, API design, scalability, maintainability

### Skill Design Patterns

**Domain Skills for Architects:**
```markdown
# database-schema skill
## Schema Overview
[Entity relationship diagrams, naming conventions]

## Design Patterns
- When to use normalization vs denormalization
- Indexing strategies by query pattern
- Partitioning guidelines

## References
- [references/schema-patterns.md](references/schema-patterns.md)
- [references/migration-strategies.md](references/migration-strategies.md)
```

**Analysis Skills for Architects:**
```markdown
# architecture-review skill
## Review Checklist
- [ ] Single responsibility at service level
- [ ] API contracts well-defined
- [ ] Data ownership clear
- [ ] Failure modes documented

## Classification Framework
- **Critical**: Breaking changes, data loss risks
- **High**: Performance bottlenecks, scaling issues
- **Medium**: Maintainability concerns
- **Low**: Style/convention deviations
```

### Typical Deliverables

| Deliverable | Format | Example Skill |
|-------------|--------|---------------|
| Architecture Decision Records | Markdown template | architecture-decisions |
| API Specifications | OpenAPI/Swagger | api-design-principles |
| Data Models | ERD + SQL schemas | postgresql |
| System Diagrams | Mermaid/PlantUML | system-documentation |

### Example Skills in Codebase

- `postgresql` - Database design patterns and schema guidance
- `api-design-principles` - REST/GraphQL API design standards
- `abp-framework-patterns` - DDD architecture patterns

---

## Backend Developer (.NET, Node.js, etc.)

**Primary Concerns:** Implementation patterns, code quality, testing, performance

### Skill Design Patterns

**Generator Skills for Developers:**
```markdown
# crud-service skill (actual example from codebase)
## Workflow
1. Gather entity information from user
2. Generate files using templates
3. Replace placeholders
4. Create directory structure

## Templates
- AppService → [references/appservice-template.md]
- DTOs → [references/dto-templates.md]
- Validator → [references/validator-template.md]
```

**Tool Skills for Developers:**
```markdown
# docker-dotnet-containerize skill
## What This Skill Does
I will analyze your .NET solution and generate:
1. Optimized Dockerfile with BuildKit features
2. Build scripts (Bash/PowerShell)
3. .dockerignore file
4. Validation checklist
```

### Typical Deliverables

| Deliverable | Format | Example Skill |
|-------------|--------|---------------|
| Service classes | Code files | crud-service |
| API endpoints | Controllers | rest-api-generator |
| Database migrations | SQL/EF migrations | entity-migrations |
| Docker configurations | Dockerfile, compose | docker-dotnet-containerize |
| Unit tests | Test files | test-generator |

### Framework-Specific Considerations

**For .NET/ABP Framework:**
- Include ABP-specific patterns (AppService, DTOs, Validators)
- Reference `common.props` and module structure
- Follow ABP naming conventions

**For Node.js:**
- Include async/await patterns
- Reference package.json structure
- Follow Node.js error handling conventions

### Example Skills in Codebase

- `crud-service` - ABP Framework CRUD generation
- `docker-dotnet-containerize` - .NET Docker optimization
- `dotnet-async-patterns` - Async/await best practices
- `error-handling-patterns` - Exception handling strategies

---

## Frontend Developer (React, Angular, Vue)

**Primary Concerns:** Component architecture, state management, UX patterns, performance

### Skill Design Patterns

**Generator Skills for Frontend:**
```markdown
# component-generator skill
## User Input Required
1. Component name (PascalCase)
2. Component type (functional/class)
3. State management (local/redux/context)
4. Include tests? (yes/no)
5. Include Storybook? (yes/no)

## Generated Files
- `{ComponentName}.tsx` - Component
- `{ComponentName}.styles.ts` - Styles
- `{ComponentName}.test.tsx` - Tests
- `{ComponentName}.stories.tsx` - Storybook
```

**Pattern Skills for Frontend:**
```markdown
# react-patterns skill
## State Management Decision Tree
- Local UI state only? → useState
- Shared across few components? → Context
- Complex app-wide state? → Redux/Zustand
- Server state? → React Query/SWR

## Component Patterns
[Before/after examples for each pattern]
```

### Typical Deliverables

| Deliverable | Format | Example Skill |
|-------------|--------|---------------|
| Components | TSX/JSX files | component-generator |
| Styles | CSS/SCSS/Styled | styling-patterns |
| Tests | Jest/RTL | javascript-testing-patterns |
| Stories | Storybook | storybook-generator |
| State logic | Hooks/stores | state-management |

### Framework-Specific Considerations

**For React:**
- Hooks-first approach
- Functional components default
- React Query for server state

**For Angular:**
- Service-based architecture
- RxJS patterns
- Module organization

### Example Skills in Codebase

- `modern-javascript-patterns` - ES6+ patterns
- `typescript-advanced-types` - Type-safe patterns
- `javascript-testing-patterns` - Jest/RTL testing

---

## Product Manager

**Primary Concerns:** Requirements clarity, acceptance criteria, prioritization, stakeholder communication

### Skill Design Patterns

**Domain Skills for PMs:**
```markdown
# product-requirements skill
## User Story Template
As a [user type]
I want to [action]
So that [benefit]

## Acceptance Criteria Format
Given [context]
When [action]
Then [expected result]

## Priority Framework
- P0: Critical - blocks release
- P1: High - core functionality
- P2: Medium - important but not blocking
- P3: Low - nice to have
```

**Workflow Skills for PMs:**
```markdown
# requirements-gathering skill
## Phase 1: Discovery
- Stakeholder interviews
- User research synthesis
- Competitive analysis

## Phase 2: Definition
- User story mapping
- Acceptance criteria
- Success metrics

## Phase 3: Validation
- Technical feasibility review
- Effort estimation
- Prioritization
```

### Typical Deliverables

| Deliverable | Format | Example Skill |
|-------------|--------|---------------|
| User Stories | Markdown/Jira format | user-story-writer |
| PRDs | Document template | prd-generator |
| Acceptance Criteria | Gherkin/checklist | acceptance-criteria |
| Roadmaps | Timeline format | roadmap-planner |
| Release Notes | Markdown | release-notes |

### Example Skills in Codebase

- Business requirements documentation patterns in `docs/`

---

## QA Engineer

**Primary Concerns:** Test coverage, edge cases, regression prevention, quality gates

### Skill Design Patterns

**Analysis Skills for QA:**
```markdown
# test-coverage-analyzer skill
## Coverage Classification
- **Critical (P0)**: Core user flows untested
- **High (P1)**: Edge cases missing
- **Medium (P2)**: Error paths untested
- **Low (P3)**: Minor scenarios missing

## Report Template
## Coverage Summary
- Statements: X%
- Branches: X%
- Functions: X%

## Gaps Identified
[List of untested scenarios]

## Recommendations
[Prioritized test additions]
```

**Generator Skills for QA:**
```markdown
# test-generator skill
## Test Types
1. Unit tests - isolated function testing
2. Integration tests - component interaction
3. E2E tests - full user flows

## Generation Process
1. Analyze code under test
2. Identify test scenarios
3. Generate test stubs
4. Add assertions
```

### Typical Deliverables

| Deliverable | Format | Example Skill |
|-------------|--------|---------------|
| Test cases | Code files | test-generator |
| Test plans | Markdown | test-plan-creator |
| Coverage reports | HTML/JSON | coverage-analyzer |
| Bug reports | Template | bug-report-template |
| E2E scripts | Playwright/Cypress | e2e-testing-patterns |

### Example Skills in Codebase

- `e2e-testing-patterns` - Playwright/Cypress patterns
- `javascript-testing-patterns` - Unit testing patterns

---

## Security Engineer

**Primary Concerns:** Vulnerability detection, compliance, threat modeling, secure coding

### Skill Design Patterns

**Analysis Skills for Security:**
```markdown
# security-audit skill
## Vulnerability Classification
- **Critical (P0)**: RCE, Auth bypass, Data exposure
- **High (P1)**: SQL injection, XSS, Privilege escalation
- **Medium (P2)**: CSRF, Info disclosure, Misconfigurations
- **Low (P3)**: Missing headers, Verbose errors

## Audit Checklist
### Authentication
- [ ] Password hashing (bcrypt/argon2)
- [ ] Session management
- [ ] MFA implementation

### Authorization
- [ ] RBAC/ABAC implementation
- [ ] API endpoint protection
- [ ] Resource-level permissions

### Input Validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] File upload restrictions
```

**Workflow Skills for Security:**
```markdown
# threat-modeling skill
## STRIDE Framework
- **S**poofing - Identity verification
- **T**ampering - Data integrity
- **R**epudiation - Audit logging
- **I**nformation disclosure - Data protection
- **D**enial of service - Availability
- **E**levation of privilege - Access control

## Process
1. Identify assets
2. Map data flows
3. Identify threats (STRIDE)
4. Rate risks (DREAD)
5. Plan mitigations
```

### Typical Deliverables

| Deliverable | Format | Example Skill |
|-------------|--------|---------------|
| Security audit report | Markdown | security-audit |
| Threat model | Diagram + doc | threat-modeling |
| Compliance checklist | Checklist | compliance-checker |
| Remediation plan | Action items | remediation-planner |
| Secure coding guide | Reference doc | secure-coding-patterns |

### Example Skills in Codebase

- `code-review-excellence` - Includes security review patterns

---

## DevOps Engineer

**Primary Concerns:** CI/CD, infrastructure, monitoring, reliability

### Skill Design Patterns

**Tool Skills for DevOps:**
```markdown
# docker-dotnet-containerize skill (actual example)
## What This Skill Does
1. Optimized Dockerfile with BuildKit features
2. Build scripts (Bash/PowerShell) with version tagging
3. .dockerignore file with comprehensive patterns
4. Validation checklist and troubleshooting guidance
```

**Integration Skills for DevOps:**
```markdown
# ci-cd-pipeline skill
## Pipeline Stages
1. Build - Compile and package
2. Test - Unit, integration, E2E
3. Security - SAST, dependency scan
4. Deploy - Environment-specific

## Platform Support
- GitHub Actions → [references/github-actions.md]
- GitLab CI → [references/gitlab-ci.md]
- Azure DevOps → [references/azure-devops.md]
```

### Typical Deliverables

| Deliverable | Format | Example Skill |
|-------------|--------|---------------|
| Dockerfiles | Dockerfile | docker-dotnet-containerize |
| CI/CD configs | YAML | ci-cd-generator |
| IaC templates | Terraform/Pulumi | infrastructure-generator |
| Monitoring configs | YAML/JSON | monitoring-setup |
| Runbooks | Markdown | incident-runbooks |

### Example Skills in Codebase

- `docker-dotnet-containerize` - Container optimization
- `git-advanced-workflows` - Git operations

---

## Cross-Role Considerations

### Skills That Serve Multiple Roles

Some skills are inherently cross-functional:

| Skill | Roles Served | Design Approach |
|-------|--------------|-----------------|
| code-review-excellence | All developers, QA, Security | Include role-specific checklists |
| api-design-principles | Architects, Backend, Frontend | Separate consumer vs provider views |
| error-handling-patterns | Backend, Frontend, QA | Language-specific sections |

### Adding Role-Specific Sections

For skills serving multiple roles, use conditional sections:

```markdown
## Usage by Role

### For Backend Developers
Focus on: [specific aspects]
Key sections: [relevant sections]

### For Frontend Developers
Focus on: [specific aspects]
Key sections: [relevant sections]

### For QA Engineers
Focus on: [specific aspects]
Key sections: [relevant sections]
```

### Collaboration Patterns

Skills often support handoffs between roles:

```
Product Manager → Backend Architect → Backend Developer → QA Engineer
     │                  │                   │                │
 requirements      api-design         crud-service      test-generator
     skill            skill              skill             skill
```

Design skills to produce outputs that serve as inputs to the next role's workflow.
