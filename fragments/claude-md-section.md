<!-- ai-artifacts:START -->
<!-- This section is managed by ai-artifacts. Do not edit manually. -->

## AI Artifacts

**Version:** {{VERSION}} | **Installed:** {{INSTALL_DATE}}

For choosing between Agents, Skills, Commands, and Hooks, see **[.claude/GUIDELINES.md](.claude/GUIDELINES.md)**.

### Quick Skill Reference

| Task | Skill |
|------|-------|
| Entity/DTO/AppService | `abp-framework-patterns` |
| DbContext/Migration | `efcore-patterns` |
| Input validation | `fluentvalidation-patterns` |
| Permissions/Auth | `openiddict-authorization` |
| Unit/Integration tests | `xunit-testing-patterns` |
| Query optimization | `linq-optimization-patterns` |
| API design | `api-design-principles` + `technical-design-patterns` |
| Debug/errors | `debugging-patterns` |
| Security audit | `security-patterns` |
| React components | `react-development-patterns` |

**For multi-skill tasks**: Read [SKILL-INDEX.md](.claude/SKILL-INDEX.md) and [CONTEXT-GRAPH.md](.claude/CONTEXT-GRAPH.md).

### Available Agents

Located in `.claude/agents/` organized by role. Full reference: [.claude/AGENT-QUICK-REF.md](.claude/AGENT-QUICK-REF.md)

| Task | Agent |
|------|-------|
| Analyze requirements | `business-analyst` |
| Design API/schema | `backend-architect` |
| Implement .NET/ABP | `abp-developer` |
| Implement React | `react-developer` |
| Review backend code | `abp-code-reviewer` |
| Review frontend code | `react-code-reviewer` |
| Security audit | `security-engineer` |
| Write tests | `qa-engineer` |
| Debug errors | `debugger` |
| DB migrations | `database-migrator` |
| CI/CD setup | `devops-engineer` |

**Usage**: `Use the abp-developer agent to implement the Patient service`

### Common Agent Chains

| Workflow | Chain |
|----------|-------|
| Feature (full) | `business-analyst` → `backend-architect` → `abp-developer` → `qa-engineer` → `abp-code-reviewer` |
| Feature (fast) | `backend-architect` → `abp-developer` → `qa-engineer` |
| Bug fix | `debugger` → `abp-developer` → `qa-engineer` |

### Quick Command Reference

Located in `.claude/commands/` organized by action. Full reference: [.claude/COMMAND-INDEX.md](.claude/COMMAND-INDEX.md)

| Task | Command |
|------|---------|
| New feature | `/feature:add-feature <name> "<requirements>"` |
| Scaffold entity | `/generate:entity <Name> --properties "..."` |
| Filter DTO | `/generate:filter <Name>` |
| DB migration | `/generate:migration <name>` |
| TDD cycle | `/tdd:tdd-cycle "<feature>" [--phase red\|green\|refactor]` |
| Audit permissions | `/review:permissions` |
| Debug error | `/debug:smart-debug "<error>" [--fix]` |
| Pre-push review | `/review:pre-push` |

<!-- ai-artifacts:END -->
