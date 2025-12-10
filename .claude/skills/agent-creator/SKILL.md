---
name: agent-creator
description: "Creates specialized AI subagents for Claude Code. Use when the user wants to create new agents, define agent configurations, build custom automation workflows, or understand existing agent architecture."
---

# Agent Creator Skill

Create deployable Claude Code sub-agents with proper configuration, tools, and inter-agent communication.

## Table of Contents

1. [Quick Reference](#quick-reference) - Field definitions
2. [Agent Creation Workflow](#agent-creation-workflow) - Step-by-step process
3. [Understanding Agents](#understanding-agents-vs-skills-vs-commands) - Agents vs Skills vs Commands
4. [Available Tools](#available-tools-reference) - Tool capabilities
5. [Permission Modes](#permission-modes) - Security settings
6. [Model Selection](#model-selection-guide) - Speed vs capability
7. [Agent Templates](#agent-templates) - Ready-to-use templates
8. [Communication Patterns](#inter-agent-communication-patterns) - Handoffs and status updates
9. [Orchestration](#orchestration-patterns) - Parallel vs sequential execution
10. [Project Agents](#project-agent-registry) - Deployed agents in this project
11. [Best Practices](#best-practices) - Design principles
12. [Troubleshooting](#troubleshooting) - Common issues
13. [Related Resources](#related-resources) - Additional documentation

---

## Quick Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Lowercase with hyphens (e.g., `backend-developer`) |
| `description` | ✅ | Include "Use PROACTIVELY when..." for auto-invocation |
| `tools` | ❌ | Comma-separated; inherits all if omitted |
| `model` | ❌ | `haiku` \| `sonnet` \| `opus` \| `inherit` |
| `permissionMode` | ❌ | `default` \| `acceptEdits` \| `bypassPermissions` |
| `skills` | ❌ | Auto-load skills when agent starts |

---

## Agent Creation Workflow

### Step 1: Gather Requirements

Ask the user:
1. **Purpose**: What specific tasks will this agent handle?
2. **Triggers**: When should Claude invoke this agent?
3. **Tools**: What capabilities does it need? (Read, Write, Edit, Bash, etc.)
4. **Model**: Speed vs capability tradeoff?
5. **Permissions**: Should it auto-approve edits?
6. **Skills**: Any project skills to auto-load?
7. **Knowledge Base**: What docs should it read/write?

### Step 2: Choose Agent Type

| Type | Use Case | Model | Example Tools |
|------|----------|-------|---------------|
| **Coordinator** | Orchestrate workflows | haiku | Read, Write, Glob |
| **Architect** | Design systems | sonnet | Read, Write, Glob, Grep |
| **Developer** | Write code | sonnet | Read, Write, Edit, Bash |
| **Reviewer** | Audit/analyze | sonnet | Read, Grep, Glob |
| **Documenter** | Create docs | haiku | Read, Write |

### Step 3: Write Agent Definition

Create file at `.claude/agents/[agent-name].md`:

```markdown
---
name: agent-name
description: "[What it does]. Use PROACTIVELY when [trigger conditions]."
tools: Read, Write, Edit, Bash
model: sonnet
permissionMode: acceptEdits
skills: skill1, skill2
---

# Agent Title

You are a [role description].

## Core Responsibilities

1. **[Category 1]**
   - [Specific task]
   - [Specific task]

2. **[Category 2]**
   - [Specific task]

## Shared Knowledge Base

You read and write within the `docs/` folder:
- `docs/[file].md` - [Purpose]

## Output Formats

### [Output Type] Template
```markdown
[Template structure]
```

## Constraints

- [Limitation 1]
- [Limitation 2]

## Inter-Agent Communication

- **From [agent]**: [What it receives]
- **To [agent]**: [What it sends]
```

### Step 4: Register & Test

1. Verify agent loads: `/agents`
2. Test invocation: `"Use the [agent-name] agent to [task]"`
3. Update `docs/agent-registry.md` with new agent

---

## Available Tools Reference

| Tool | Purpose | Use When |
|------|---------|----------|
| `Read` | Read files | Always needed |
| `Write` | Create/overwrite files | Creating new files |
| `Edit` | Modify existing files | Code changes |
| `Glob` | Find files by pattern | Searching codebase |
| `Grep` | Search file contents | Finding code patterns |
| `Bash` | Run shell commands | Build, test, git |
| `WebFetch` | Fetch URLs | External APIs |
| `WebSearch` | Search web | Research |

---

## Permission Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `default` | Asks for approval | Security-sensitive |
| `acceptEdits` | Auto-approves file edits | Developers |
| `bypassPermissions` | No approvals needed | Trusted automation |

---

## Model Selection Guide

| Model | Speed | Cost | Capability | Use For |
|-------|-------|------|------------|---------|
| `haiku` | ⚡⚡⚡ | 💰 | ⭐⭐ | Coordinators, simple tasks |
| `sonnet` | ⚡⚡ | 💰💰 | ⭐⭐⭐⭐ | Development, analysis |
| `opus` | ⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ | Complex reasoning |
| `inherit` | - | - | - | Match parent session |

---

## Agent Templates

Copy and customize these templates for your agents:

### 1. Developer Agent
**Use for**: Backend/Frontend developers, language specialists

See: [assets/developer-agent-template.md](assets/developer-agent-template.md)

**Key features**:
- Implements code following specifications
- Writes tests alongside implementation
- Updates documentation
- Permission mode: `acceptEdits`
- Model: `sonnet`

### 2. Reviewer Agent
**Use for**: Code reviewers, security auditors, quality assurance

See: [assets/reviewer-agent-template.md](assets/reviewer-agent-template.md)

**Key features**:
- Analyzes code/docs for issues
- Provides prioritized feedback
- Structured review reports
- Permission mode: `default`
- Model: `sonnet`

### 3. Coordinator Agent
**Use for**: Orchestrators, workflow managers, task routers

See: [assets/coordinator-agent-template.md](assets/coordinator-agent-template.md)

**Key features**:
- Breaks down complex tasks
- Routes to specialized agents
- Tracks progress across workflows
- Permission mode: `default`
- Model: `haiku` (fast coordination)

---

## Inter-Agent Communication Patterns

### Task Handoff
```markdown
## Handoff: [from-agent] → [to-agent]

**Task**: [Description]
**Priority**: High | Medium | Low
**Inputs**: [[document-reference]]
**Expected Output**: [What to produce]
**Deadline**: [If applicable]
```

### Status Update
```markdown
## Status: [agent-name]

**Date**: YYYY-MM-DD
**Task**: [Task ID or description]
**Status**: Working | Complete | Blocked
**Progress**: [What was done]
**Next**: [Next steps]
```

---

## Project Agent Registry

This project has **8 deployed agents** organized by role in `.claude/agents/`:

| Category | Agent | Purpose | Model |
|----------|-------|---------|-------|
| **Architects** | product-architect | Requirements, BRD, user stories | haiku |
| **Architects** | backend-architect | TSD, API design, database schema | sonnet |
| **Engineers** | abp-developer | .NET/ABP implementation | sonnet |
| **Engineers** | react-developer | React/UI implementation | sonnet |
| **Engineers** | devops-engineer | CI/CD, Docker, releases | sonnet |
| **Reviewers** | code-reviewer | Code quality review | sonnet |
| **Reviewers** | qa-engineer | Testing, E2E automation | sonnet |
| **Reviewers** | security-engineer | Security audits, OWASP | sonnet |
| **Specialists** | debugger | Root cause analysis | sonnet |
| **Specialists** | orchestrator | Multi-agent coordination | haiku |

**Language Experts** (used by other agents):
- `csharp-pro` - Advanced C# patterns
- `typescript-pro` - Advanced TypeScript patterns

See [docs/agent-registry.md](../../docs/agent-registry.md) for complete details including triggers, inputs/outputs, and inter-agent dependencies.

---

## Best Practices

### 1. Single Responsibility Principle
Each agent should have **one clear purpose**. Don't create a "do everything" agent.

✅ **Good**: `backend-architect`, `code-reviewer`, `qa-engineer`
❌ **Bad**: `full-stack-everything-agent`

**Why**: Focused agents are more predictable, easier to maintain, and perform better.

### 2. Principle of Least Privilege
Only grant **necessary tools**. More tools = more complexity + security risk.

```yaml
# Developer needs to write code
tools: Read, Write, Edit, Bash, Glob, Grep  ✅

# Reviewer only analyzes
tools: Read, Grep, Glob  ✅

# Coordinator orchestrates
tools: Read, Write, Glob  ✅
```

### 3. Clear Trigger Phrases
Include **"Use PROACTIVELY when..."** in descriptions for automatic invocation.

✅ **Good**: "Use PROACTIVELY when implementing backend features with ABP Framework"
❌ **Bad**: "Helps with backend development"

### 4. Explicit Inputs & Outputs
Define what agents **read** and **write** to ensure smooth handoffs.

```markdown
## Shared Knowledge Base

**Read**:
- docs/technical-specification.md
- docs/business-requirements.md

**Write**:
- docs/dev-progress.md
- Code files in src/
```

### 5. Define Constraints
State what agents should **NOT do** to prevent scope creep.

```markdown
## Constraints

- DO NOT modify core framework code
- DO NOT introduce dependencies without approval
- DO NOT skip writing tests
```

### 6. Version Control Integration
**Commit agents to git** so they're shared across your team.

```bash
git add .claude/agents/
git commit -m "feat: add backend-architect agent"
git push
```

### 7. Human-in-the-Loop Checkpoints
For safety, pause before destructive actions:

- Major architectural changes
- Database schema modifications
- Security-sensitive operations
- Production deployments

### 8. Context Efficiency
Leverage **context isolation** - sub-agents work in separate context windows, preventing pollution of the main conversation.

See [references/context-isolation.md](references/context-isolation.md) for details.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not invoked | Check description includes trigger phrases |
| Wrong agent selected | Make descriptions more specific |
| Permission errors | Check tool list and permissionMode |
| Skill not loaded | Verify skill name in `skills:` field |
| Output inconsistent | Add detailed output format templates |

---

## Understanding Agents vs Skills vs Commands

| Type | Invocation | Primary Purpose | Key Benefit |
|------|------------|-----------------|-------------|
| **Skill** | Automatic (Model decides) | Provides domain expertise/instructions | Progressive disclosure (efficiency) |
| **Slash Command** | Manual (User types /cmd) | Executes explicit, atomic actions | User-controlled automation |
| **Sub-Agent** | Automatic or explicit | Autonomous execution of complex tasks | **Context isolation** (separate window) |

**Context Isolation**: Sub-agents operate in their **own context window**, separate from the main conversation. This prevents context pollution and leads to faster, cheaper responses.

---

## Orchestration Patterns

### 1. Parallel Execution
The orchestrator spawns multiple sub-agents simultaneously:
- Example: `backend-architect`, `security-engineer`, and `qa-engineer` analyze requirements in parallel
- Consolidates outputs into comprehensive plan

### 2. Sequential Pipeline
Output of one agent becomes input for the next:
```
backend-architect (TSD) → abp-developer (Code) → qa-engineer (Tests) → devops-engineer (Deploy)
```

For detailed orchestration strategies, see [references/orchestration-patterns.md](references/orchestration-patterns.md).

---

## Related Resources

- **Agent Templates**: [assets/](assets/) directory
- **Orchestration**: [references/orchestration-patterns.md](references/orchestration-patterns.md)
- **Context Isolation**: [references/context-isolation.md](references/context-isolation.md)
- **Project Agents**: `.claude/agents/` directory
- **Agent Registry**: [docs/agent-registry.md](../../docs/agent-registry.md)
- **Claude Code Docs**: https://code.claude.com/docs/en/sub-agents