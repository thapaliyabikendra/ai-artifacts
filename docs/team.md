# Team & Agent Registry

> **Purpose**: Map between Claude sub-agents and human team members for this project.
> **Last Updated**: 2025-12-11

---

## 🤖 Deployed Claude Sub-Agents (8)

| Agent Name | Role | Model | Location |
|------------|------|-------|----------|
| `product-manager` | BA / Product Owner | haiku | `.claude/agents/product-manager.md` |
| `backend-architect` | Tech Lead / Architect | sonnet | `.claude/agents/backend-architect.md` |
| `abp-developer` | .NET / ABP Developer | sonnet | `.claude/agents/abp-developer.md` |
| `react-developer` | React Developer + UI/UX | sonnet | `.claude/agents/react-developer.md` |
| `qa-engineer` | Test Automation / QA | sonnet | `.claude/agents/qa-engineer.md` |
| `security-engineer` | AppSec / Compliance | sonnet | `.claude/agents/security-engineer.md` |
| `devops-engineer` | DevOps + Release | sonnet | `.claude/agents/devops-engineer.md` |
| `orchestrator` | Multi-Agent Coordinator | haiku | `.claude/agents/orchestrator.md` |

---

## 👥 Human Team Members (Reference)

These are the human personas that inspired the agent capabilities:

| Name | Role | Domain Expertise | Agent Equivalent |
|------|------|------------------|------------------|
| Amit | Project Manager / BA | Banking, Finance, Healthcare | `product-manager` |
| Bikendra | Tech Lead | .NET, ABP Framework, EF Core, PostgreSQL | `backend-architect` |
| Nishant | Backend Developer | .NET, ABP, API Development | `abp-developer` |
| Sonu | Frontend Developer | React, TypeScript | `react-developer` |
| Prabin | UI/UX Designer | Wireframes, Design Systems | `react-developer` |
| Akash | Security Engineer | OWASP, OAuth, Compliance | `security-engineer` |
| Sujan | DevOps Engineer | CI/CD, Docker, Kubernetes | `devops-engineer` |
| Min | Release Manager | Versioning, Deployments | `devops-engineer` |
| Sajesh | QA Engineer | Test Automation, E2E | `qa-engineer` |
| Biki | Orchestrator | Coordination, Workflow | `orchestrator` |

---

## 📋 Agent-to-Human Escalation

When agents encounter blockers or need human decisions:

| Situation | Escalate To | How |
|-----------|-------------|-----|
| Business requirement clarification | Amit | Log in `dev-progress.md`, await human input |
| Architecture decision | Bikendra | Create ADR draft in `decisions.md` |
| Security concern | Akash | Document in `security-audit.md` |
| Deployment approval | Sujan / Min | Update `releases.md`, mark for human approval |
| Test failure investigation | Sajesh | Document in `test-cases.md` |

---

## 🔧 Agent Capabilities Summary

### product-manager
- **Domain**: Healthcare clinic management
- **Creates**: BRD, User Stories, Acceptance Criteria
- **Reads**: Stakeholder requirements, Progress reports
- **Skills**: Requirement analysis, Prioritization (MoSCoW, RICE)

### backend-architect
- **Domain**: .NET Core, ABP Framework, PostgreSQL, Redis
- **Creates**: TSD, API Contracts, DB Schema, ADRs
- **Reads**: BRD, Security requirements
- **Skills**: System design, DDD, Code review

### abp-developer
- **Domain**: .NET, ABP Framework, Entity Framework Core
- **Creates**: Entities, AppServices, DTOs, Validators, Unit tests
- **Reads**: TSD, API Contracts
- **Skills**: CRUD services, Domain services, FluentValidation, async/await

### react-developer
- **Domain**: React 18+, TypeScript, Tailwind, UI/UX Design
- **Creates**: React components, Wireframes, User flows, Frontend tests
- **Reads**: API Contracts, Design tokens
- **Skills**: State management, React Query, Accessibility (WCAG), Design systems

### qa-engineer
- **Domain**: xUnit, Playwright, Jest
- **Creates**: Test plans, Test cases, Bug reports, E2E scripts
- **Reads**: BRD, TSD, Completed features
- **Skills**: Unit testing, Integration testing, E2E automation

### security-engineer
- **Domain**: OWASP, OAuth 2.0, JWT, RBAC
- **Creates**: Security audits, Threat models (STRIDE), Guidelines
- **Reads**: Architecture, Code, Deployments
- **Skills**: Vulnerability assessment, CVSS scoring, Compliance

### devops-engineer
- **Domain**: Docker, GitHub Actions, Kubernetes, Azure, Git
- **Creates**: Dockerfiles, CI/CD pipelines, Release plans, Changelogs
- **Reads**: TSD, Backlog, Test results
- **Skills**: Container optimization, Semantic versioning, Rollback planning

### orchestrator
- **Domain**: Multi-agent coordination
- **Creates**: Task assignments, Status reports
- **Reads**: All documents
- **Skills**: Workflow management, Conflict resolution, Task routing

---

## 🔀 Agent Merges (Option B)

The following consolidations were made for efficiency:

| Original Agents | Merged Into | Rationale |
|-----------------|-------------|-----------|
| `frontend-developer` + `ui-ux-designer` | `react-developer` | Both UI-focused, project uses React only |
| `release-manager` + `devops-engineer` | `devops-engineer` | Both handle deployment lifecycle |
| `backend-developer` | `abp-developer` | Renamed for project specificity (ABP Framework) |

---

## 📁 Related Documents

- [[agent-registry]] - Detailed agent specifications
- [[center-knowledge-base]] - Central documentation index
- [[dev-progress]] - Daily agent activity log
