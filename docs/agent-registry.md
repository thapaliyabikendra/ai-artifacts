# Agent Registry

> **Purpose**: Central reference for all Claude sub-agents, their capabilities, and communication patterns.
> **Location**: `.claude/agents/` directory
> **Last Updated**: 2025-12-11

---

## 🤖 Active Agents (8)

| Agent | Model | Primary Tools | Auto-loaded Skills |
|-------|-------|---------------|-------------------|
| [[#product-manager]] | haiku | Read, Write, Glob | - |
| [[#backend-architect]] | sonnet | Read, Write, Glob, Grep | abp-framework-patterns, api-design-principles, postgresql |
| [[#abp-developer]] | sonnet | Read, Write, Edit, Bash, Glob, Grep | abp-framework-patterns, crud-service, dotnet-async-patterns, error-handling-patterns, sql-optimization-patterns |
| [[#react-developer]] | sonnet | Read, Write, Edit, Bash, Glob, Grep | modern-javascript-patterns, typescript-advanced-types, javascript-testing-patterns |
| [[#qa-engineer]] | sonnet | Read, Write, Edit, Bash, Glob, Grep | e2e-testing-patterns, javascript-testing-patterns |
| [[#security-engineer]] | sonnet | Read, Write, Grep, Glob | error-handling-patterns |
| [[#devops-engineer]] | sonnet | Read, Write, Edit, Bash, Glob, Grep | docker-dotnet-containerize |
| [[#orchestrator]] | haiku | Read, Write, Glob | - |

---

## Agent Details

### product-manager

**Role**: Business Analyst & Product Owner

**Triggers**: Use PROACTIVELY when:
- Analyzing requirements
- Creating user stories
- Validating business logic
- Defining acceptance criteria

**Inputs**:
- Stakeholder requirements
- Customer feedback
- Agent progress reports

**Outputs**:
- Business Requirements Document (BRD)
- User stories with acceptance criteria
- Prioritized backlog
- Task assignments

**Knowledge Base Files**:
- Writes: `business-requirements.md`, `backlog.md`
- Reads: `center-knowledge-base.md`, `dev-progress.md`

---

### backend-architect

**Role**: Tech Lead / Backend Architect

**Triggers**: Use PROACTIVELY when:
- Translating requirements to technical design
- Creating TSD
- Designing APIs and database schema
- Making architecture decisions

**Inputs**:
- BRD from product-manager
- Change requests
- Security requirements

**Outputs**:
- Technical Specification Document (TSD)
- API contracts
- Database schema
- Architecture Decision Records (ADR)

**Knowledge Base Files**:
- Writes: `technical-specification.md`, `decisions.md`, `api-contracts.md`, `db-schema.md`
- Reads: `business-requirements.md`

---

### abp-developer

**Role**: .NET / ABP Framework Developer

**Triggers**: Use PROACTIVELY when:
- Implementing backend features with ABP Framework
- Creating CRUD services and AppServices
- Writing entities, DTOs, and validators
- Building API endpoints
- Working with Entity Framework Core

**Inputs**:
- TSD from backend-architect
- API contracts
- Security requirements

**Outputs**:
- Implemented backend code (entities, domain services, AppServices)
- DTOs and FluentValidation validators
- Unit/integration tests
- API documentation updates

**Knowledge Base Files**:
- Writes: `dev-progress.md`
- Reads: `technical-specification.md`, `api-contracts.md`, `decisions.md`

**Permission Mode**: `acceptEdits` - Can modify code files without confirmation

---

### react-developer

**Role**: React Developer + UI/UX Designer

**Triggers**: Use PROACTIVELY when:
- Building React UI components
- Creating wireframes or mockups
- Defining user flows and design systems
- Integrating APIs
- Writing frontend tests
- Implementing responsive, accessible design

**Inputs**:
- API contracts
- BRD and user stories
- Component requirements
- Design tokens

**Outputs**:
- React components with TypeScript
- Wireframes (text-based)
- User flow diagrams
- Frontend tests (Jest, React Testing Library)
- Design system documentation

**Knowledge Base Files**:
- Writes: `dev-progress.md`, `ui-designs.md`
- Reads: `technical-specification.md`, `api-contracts.md`, `business-requirements.md`

**Permission Mode**: `acceptEdits` - Can modify code files without confirmation

---

### qa-engineer

**Role**: Test Automation & Quality Assurance

**Triggers**: Use PROACTIVELY when:
- Testing features
- Creating test cases
- Analyzing test coverage
- Reporting bugs
- Writing E2E tests with Playwright

**Inputs**:
- BRD with acceptance criteria
- TSD with API specifications
- Completed features from developers

**Outputs**:
- Test plans and test cases
- Bug reports
- Test coverage metrics
- E2E automation scripts
- Quality reports

**Knowledge Base Files**:
- Writes: `test-cases.md`, `dev-progress.md`
- Reads: `business-requirements.md`, `technical-specification.md`

**Permission Mode**: `acceptEdits` - Can write test files without confirmation

---

### security-engineer

**Role**: Application Security & Compliance

**Triggers**: Use PROACTIVELY when:
- Reviewing code security
- Conducting security audits
- Implementing security controls
- Threat modeling (STRIDE)
- OWASP compliance checks

**Inputs**:
- Architecture designs
- Backend/frontend code
- Deployment configurations

**Outputs**:
- Security audit reports
- Vulnerability findings (CVSS scored)
- Mitigation recommendations
- Threat models

**Knowledge Base Files**:
- Writes: `security-audit.md`, `decisions.md`
- Reads: `technical-specification.md`, code files

---

### devops-engineer

**Role**: DevOps & Release Engineer

**Triggers**: Use PROACTIVELY when:
- Setting up CI/CD pipelines
- Creating Dockerfiles
- Configuring infrastructure
- Preparing releases
- Managing versions
- Coordinating deployments

**Inputs**:
- TSD from backend-architect
- Completed features from developers
- Test completion from qa-engineer
- Release scope from product-manager

**Outputs**:
- Dockerfiles and docker-compose.yml
- GitHub Actions / CI/CD workflows
- Infrastructure as Code
- Release plans and changelogs
- Deployment tracking

**Knowledge Base Files**:
- Writes: `releases.md`, `dev-progress.md`, `decisions.md`
- Reads: `technical-specification.md`, `backlog.md`, `test-cases.md`

**Permission Mode**: `acceptEdits` - Can modify infrastructure files without confirmation

---

### orchestrator

**Role**: Multi-Agent Coordinator

**Triggers**: Use PROACTIVELY when:
- Managing multi-agent tasks
- Coordinating complex features
- Resolving conflicts between agents
- Tracking overall progress

**Inputs**:
- High-level feature requests
- Agent outputs
- Status reports

**Outputs**:
- Consolidated deliverables
- Task assignments
- Status reports
- Workflow coordination

**Knowledge Base Files**:
- Writes: `dev-progress.md`
- Reads: All documents

---

## 📊 Agent Dependency Graph

```
                           ┌─────────────────┐
                           │   orchestrator  │
                           │    (routing)    │
                           └────────┬────────┘
                                    │ coordinates
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ product-manager │     │security-engineer│     │ devops-engineer │
│     (BRD)       │     │  (audits)       │     │ (CI/CD+releases)│
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │ BRD                   │ audit                 │
         ▼                       │                       │
┌─────────────────┐              │                       │
│backend-architect│◄─────────────┘                       │
│  (TSD, APIs)    │                                      │
└────────┬────────┘                                      │
         │ TSD                                           │
         ├─────────────────────────┬─────────────────────┤
         ▼                         ▼                     ▼
┌─────────────────┐     ┌─────────────────┐              │
│  abp-developer  │     │ react-developer │              │
│  (.NET, ABP)    │     │ (React, UI/UX)  │              │
└────────┬────────┘     └────────┬────────┘              │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                       ┌─────────────────┐
                       │   qa-engineer   │
                       │  (xUnit, E2E)   │
                       └─────────────────┘
```

---

## 🔀 Future Sub-Agents (On-Demand Specialists)

These can be created as needed for specialized tasks:

| Sub-Agent | Parent Agent | Specialization |
|-----------|--------------|----------------|
| `database-engineer` | backend-architect | EF Core migrations, query tuning, PostgreSQL |
| `auth-architect` | backend-architect | OpenIddict, OAuth 2.0 flows |
| `api-designer` | backend-architect | OpenAPI specifications |
| `playwright-tester` | qa-engineer | E2E test automation |
| `performance-auditor` | qa-engineer | Load testing, profiling |
| `accessibility-auditor` | react-developer | WCAG 2.1 compliance |

---

## 🔧 How to Invoke Agents

### Automatic Invocation
Claude automatically selects agents based on task description and agent `description` field.

### Explicit Invocation
```
> Use the backend-architect agent to design the API for patient management
> Have the qa-engineer agent create test cases for the appointment module
> Ask the security-engineer agent to audit the authentication implementation
```

### Chaining Agents
```
> First use the backend-architect agent to design the schema,
> then use the abp-developer agent to implement it
```

### Parallel Execution
```
> Run abp-developer and react-developer in parallel to implement the patient feature
```

---

## 📝 Adding New Agents

To add a new agent:

1. Create file in `.claude/agents/[agent-name].md`
2. Define frontmatter with required fields:
   - `name`: Unique identifier (lowercase, hyphens)
   - `description`: When to invoke (include "Use PROACTIVELY when...")
   - `tools`: Comma-separated tool list
   - `model`: haiku | sonnet | opus
   - `permissionMode`: default | acceptEdits | bypassPermissions
   - `skills`: Optional comma-separated skill list

3. Write system prompt with:
   - Role description
   - Core responsibilities
   - Input/output specifications
   - Knowledge base file mappings
   - Constraints
   - Inter-agent communication

4. Register in this document
5. Update [[center-knowledge-base]] if new documents are needed
