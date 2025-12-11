# Development Team

> **Purpose**: Map human team members to roles for escalation and accountability.
> **Last Updated**: 2025-12-12

---

## Team Members

| Name | Role | Expertise | Escalation Contact |
|------|------|-----------|-------------------|
| Amit | Project Manager / BA | Banking, Finance, Healthcare | Requirements clarification |
| Bikendra | Tech Lead | .NET, ABP Framework, PostgreSQL | Architecture decisions |
| Nishant | Backend Developer | .NET, ABP, API Development | Backend implementation |
| Sonu | Frontend Developer | React, TypeScript | Frontend implementation |
| Prabin | UI/UX Designer | Wireframes, Design Systems | UI/UX decisions |
| Akash | Security Engineer | OWASP, OAuth, Compliance | Security concerns |
| Sujan | DevOps Engineer | CI/CD, Docker, Kubernetes | Deployment issues |
| Min | Release Manager | Versioning, Deployments | Release approval |
| Sajesh | QA Engineer | Test Automation, E2E | Test failures |

---

## Escalation Matrix

| Decision Type | Primary Contact | Backup |
|---------------|-----------------|--------|
| Business requirements | Amit | Bikendra |
| Architecture decisions | Bikendra | Nishant |
| Security concerns | Akash | Bikendra |
| Deployment approval | Sujan | Min |
| Test failures | Sajesh | Nishant |
| UI/UX decisions | Prabin | Sonu |

---

## Agent Output Review

When agents produce artifacts, these humans should review:

| Agent Output | Human Reviewer |
|--------------|----------------|
| `requirements.md`, `impact-analysis.md` | Amit |
| `technical-design.md`, ADRs | Bikendra |
| Backend code (ABP) | Nishant, Bikendra |
| Frontend code (React) | Sonu, Prabin |
| `test-cases.md`, test code | Sajesh |
| `security-audit.md` | Akash |
| CI/CD pipelines, Dockerfiles | Sujan |
| Release notes, changelogs | Min |

---

## Notes

- Agent outputs should include reviewer assignment in comments
- Escalations logged in `docs/dev-progress.md`
- Human approvals required for production deployments
