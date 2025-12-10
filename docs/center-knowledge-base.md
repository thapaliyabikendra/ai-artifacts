# Central Knowledge Base

> **Purpose**: Shared memory and communication hub for all Claude sub-agents.
> **Usage**: Open this folder in Obsidian for linked navigation. All agents read/write to this vault.

---

## 📚 Document Index

### Core Documents
| Document | Owner | Purpose |
|----------|-------|---------|
| [[business-requirements]] | product-manager | Business Requirements Document (BRD) |
| [[technical-specification]] | backend-architect | Technical Specification Document (TSD) |
| [[backlog]] | product-manager | User stories and sprint tasks |
| [[decisions]] | backend-architect | Architecture Decision Records (ADR) |

### Development Artifacts
| Document | Owner | Purpose |
|----------|-------|---------|
| [[api-contracts]] | backend-architect | API endpoint specifications |
| [[db-schema]] | backend-architect | Database schema and migrations |
| [[ui-designs]] | frontend-developer | UI/UX wireframes and components |

### Quality & Security
| Document | Owner | Purpose |
|----------|-------|---------|
| [[test-cases]] | qa-engineer | Test plans and results |
| [[security-audit]] | security-engineer | Security findings and mitigations |

### Operations
| Document | Owner | Purpose |
|----------|-------|---------|
| [[releases]] | release-manager | Release history and changelog |
| [[dev-progress]] | orchestrator | Daily agent activity logs |
| [[agent-registry]] | orchestrator | Agent capabilities reference |

### Reference
| Document | Owner | Purpose |
|----------|-------|---------|
| [[team]] | - | Team roles and human contacts |

---

## 🤖 Agent Communication Protocol

### How Agents Use This Knowledge Base

1. **Read Before Write**: Always read existing documents before making updates
2. **Atomic Updates**: Make focused, single-purpose updates
3. **Log Activity**: Record significant actions in [[dev-progress]]
4. **Link Documents**: Use `[[document-name]]` for cross-references
5. **Version Awareness**: Note document versions when referencing

### Agent-to-Agent Messaging Pattern

When agents need to communicate tasks or handoffs:

```markdown
## Message: [Agent] → [Agent]

**Date**: YYYY-MM-DD HH:MM
**From**: [source-agent]
**To**: [target-agent]
**Type**: Task | Question | Handoff | Status Update

### Content
[Message content]

### Action Required
- [ ] [Specific action item]

### References
- [[related-document]]
```

---

## 📋 Workflow Reference

### New Feature Development Flow
```
product-manager      → Create BRD, user stories in [[backlog]]
       ↓
backend-architect    → Create TSD in [[technical-specification]]
       ↓                Log decisions in [[decisions]]
security-engineer    → Review architecture, update [[security-audit]]
       ↓
backend-developer    → Implement backend, log in [[dev-progress]]
       ↓
frontend-developer   → Implement UI, log in [[dev-progress]]
       ↓
qa-engineer          → Test and document in [[test-cases]]
       ↓
release-manager      → Prepare release in [[releases]]
```

### Bug Fix Flow
```
qa-engineer          → Document bug in [[test-cases]]
       ↓
backend-architect    → Identify fix in [[decisions]]
       ↓
backend/frontend-dev → Implement fix, log in [[dev-progress]]
       ↓
qa-engineer          → Verify fix in [[test-cases]]
       ↓
release-manager      → Hotfix release in [[releases]]
```

---

## 🏥 Project Context: Clinic Management System

### Domain Overview
A clinic management system for managing patients, appointments, and doctor schedules.

### Entities
- **Patient**: FirstName, LastName, Email, Phone, DateOfBirth
- **Doctor**: FullName, Specialization, Email, Phone
- **Appointment**: PatientId, DoctorId, AppointmentDate, Description, Status
- **DoctorSchedule**: DoctorId, DayOfWeek, StartTime, EndTime

### Roles & Permissions
| Role | Capabilities |
|------|-------------|
| Admin | Full control over all entities |
| Doctor | View own appointments & patients, mark appointments completed |
| Receptionist | Create patients, schedule appointments |

### Tech Stack
- **Backend**: .NET 10, ABP Framework 10.0.1, Entity Framework Core, PostgreSQL
- **Auth**: OpenIddict (OAuth 2.0), JWT, ASP.NET Identity
- **Caching**: Redis
- **Validation**: FluentValidation

---

## 📁 File Organization

```
docs/
├── center-knowledge-base.md  ← You are here
├── business-requirements.md  # BRD
├── technical-specification.md # TSD
├── backlog.md                # User stories
├── decisions.md              # ADRs
├── api-contracts.md          # API specs
├── db-schema.md              # Database design
├── ui-designs.md             # UI/UX specs
├── test-cases.md             # Test plans
├── security-audit.md         # Security findings
├── releases.md               # Release history
├── dev-progress.md           # Daily logs
├── agent-registry.md         # Agent reference
└── team.md                   # Team contacts
```

---

## 🔗 Quick Links

- **Start Here**: [[business-requirements]] for project requirements
- **Architecture**: [[technical-specification]] for system design
- **Current Work**: [[backlog]] for active tasks
- **Progress**: [[dev-progress]] for daily updates
- **Releases**: [[releases]] for version history
