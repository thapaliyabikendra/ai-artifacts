# Agent Categories

Agents are organized by role (what they ARE) into the following categories.

## Category Overview

| Category | Purpose | Examples |
|----------|---------|----------|
| `architects/` | Design systems, plan implementations | backend-architect, business-analyst |
| `reviewers/` | Analyze and critique | abp-code-reviewer, react-code-reviewer, security-engineer, qa-engineer |
| `engineers/` | Build and implement | abp-developer, react-developer, devops-engineer |
| `specialists/` | Deep domain expertise | debugger |

## Decision Tree: Where Does My Agent Go?

```
Is it primarily about designing/planning? → architects/
Is it primarily about reviewing/critiquing? → reviewers/
Is it primarily about building/implementing? → engineers/
Does it have deep domain expertise? → specialists/
```

## Category Details

### Architects (`architects/`)

**Purpose:** Design systems, create specifications, make architecture decisions.

**Characteristics:**
- Focus on design over implementation
- Create documentation (TSD, ADRs, schemas)
- Make technology and pattern decisions
- Plan before building

**Typical Tools:** `Read, Write, Glob, Grep`

**Examples:**
- `backend-architect` - API design, database schemas
- `product-architect` - BRDs, user stories, acceptance criteria
- `frontend-architect` - Component architecture, state management

### Reviewers (`reviewers/`)

**Purpose:** Analyze, audit, and critique code or systems.

**Characteristics:**
- Read-only operations (typically)
- Produce findings and recommendations
- Don't implement fixes directly
- Focus on quality and compliance

**Typical Tools:** `Read, Glob, Grep`

**Examples:**
- `abp-code-reviewer` - Backend code quality, ABP patterns
- `react-code-reviewer` - Frontend code quality, React patterns
- `security-engineer` - Security audits, STRIDE, OWASP
- `qa-engineer` - Test coverage, quality validation

### Engineers (`engineers/`)

**Purpose:** Build and implement features, write code.

**Characteristics:**
- Write and edit code
- Follow specifications from architects
- Run builds and tests
- May auto-approve edits

**Typical Tools:** `Read, Write, Edit, Bash, Glob, Grep`

**Examples:**
- `backend-developer` - Server-side implementation
- `frontend-developer` - UI/UX implementation
- `devops-engineer` - CI/CD, infrastructure

### Specialists (`specialists/`)

**Purpose:** Deep expertise in specific domains or functions.

**Characteristics:**
- Narrow but deep knowledge
- Called for specific problems
- May coordinate other agents
- Domain-specific guidance

**Typical Tools:** Varies by specialty

**Examples:**
- `debugger` - Root cause analysis, error diagnosis
- `coordinator` - Multi-agent orchestration
- `database-specialist` - Query optimization, schema design

## Templates by Category

### By Role (Team Position)

| Role | Category | Template |
|------|----------|----------|
| Manager | specialists | `manager` |
| Tech Lead | architects | `tech-lead` |
| Developer | engineers | `developer` |
| QA Engineer | reviewers | `qa-engineer` |
| DevOps | engineers | `devops` |
| Security | reviewers | `security` |

### By Function (What They Do)

| Function | Category | Template |
|----------|----------|----------|
| Architect | architects | `architect` |
| Reviewer | reviewers | `reviewer` |
| Developer | engineers | `developer` |
| Coordinator | specialists | `coordinator` |
| Specialist | specialists | `specialist` |

## Agent File Format

```yaml
---
name: agent-name                    # Required: kebab-case
description: "Purpose. Use PROACTIVELY when..."  # Required
tools: Read, Write, Edit, Bash      # Optional: inherits all if omitted
model: sonnet                       # Optional: haiku|sonnet|opus|inherit
permissionMode: default             # Optional: default|acceptEdits|bypassPermissions
skills: skill1, skill2              # Optional: auto-load skills
---

You are a [role description]...

## Core Responsibilities
...

## Constraints
...
```

## Best Practices

### Single Responsibility
One agent = one clear role. Don't create "do everything" agents.

### Clear Triggers
Include "Use PROACTIVELY when..." in description:

```yaml
# Good
description: "Code reviewer. Use PROACTIVELY when reviewing PRs or code changes."

# Bad
description: "Helps with code review"
```

### Least Privilege
Only grant necessary tools:

```yaml
# Developer - needs write access
tools: Read, Write, Edit, Bash, Glob, Grep

# Reviewer - read-only
tools: Read, Grep, Glob
```

### Explicit I/O
Define what agents read and write in their instructions.
