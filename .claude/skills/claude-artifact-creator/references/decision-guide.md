# Skill vs Command: When to Create Each

Skills and commands serve different purposes in the Claude ecosystem. This guide helps you decide which to create.

## Quick Decision Matrix

| If your goal is... | Create a... | Why |
|-------------------|-------------|-----|
| Reusable knowledge/patterns | **Skill** | Skills provide reference material |
| End-to-end orchestrated workflow | **Command** | Commands coordinate multi-phase processes |
| Domain-specific reference | **Skill** | Skills are knowledge containers |
| Multi-agent coordination | **Command** | Commands delegate to agents |
| File format processing | **Skill** | Skills bundle processing scripts |
| User-invoked action with phases | **Command** | Commands are action-oriented |
| Best practices documentation | **Skill** | Skills provide guidance |
| CI/CD or deployment automation | **Command** | Commands orchestrate actions |

## Key Differences

| Aspect | Skills | Commands |
|--------|--------|----------|
| **Purpose** | Provide reusable knowledge | Orchestrate action workflows |
| **Organization** | By TOPIC (knowledge domain) | By ACTION (what user does) |
| **Invocation** | Referenced by agents/commands | Slash commands (`/command-name`) |
| **Structure** | SKILL.md + resources | Markdown with phases |
| **Agent Use** | Referenced for knowledge | Delegates to agents via Task tool |
| **Complexity** | Single topic focus | Can be very complex (12+ phases) |
| **Output** | Documentation, templates | Deliverables (code, PRs, fixes) |
| **Configuration** | Not parameterized | Flags and arguments |
| **State** | Stateless knowledge | Phased execution with context |

## Detailed Comparison

### Skills: Knowledge Containers

**Skills provide:**
- Specialized workflows and procedures
- Domain expertise (schemas, conventions)
- Bundled resources (scripts, templates)
- Reference documentation

**Skills are triggered by:**
- User requests matching the description
- Agent references during execution
- Commands needing domain knowledge

**Example skill (crud-service):**
```yaml
---
name: crud-service
description: Generate complete ABP Framework CRUD services...
---
# Workflow
1. Gather entity information
2. Generate files using templates
3. Replace placeholders
```

### Commands: Action Orchestrators

**Commands provide:**
- Multi-phase coordinated processes
- Agent delegation and orchestration
- Configuration via flags
- Context passing between phases

**Commands are invoked by:**
- User typing `/command-name [args]`
- Direct slash command invocation

**Example command (feature-development):**
```markdown
# Feature Development

[Extended thinking: 12-phase workflow...]

## Configuration Options
- --methodology (traditional|tdd|bdd|ddd)
- --complexity (simple|medium|complex|epic)

## Phase 1: Discovery
Use Task tool with subagent_type="business-analyst"
Prompt: "Analyze requirements..."

## Phase 2: Architecture
Use Task tool with subagent_type="backend-architect"
Context from Phase 1...
```

## When to Choose Skills

### 1. Encoding Domain Knowledge

**Create a skill when** you need to capture organizational or domain-specific knowledge that Claude doesn't have.

**Examples:**
- Company database schemas
- API specifications
- Business rules and policies
- Coding standards

**Skill pattern:**
```markdown
# company-database skill
## Schema Overview
[Tables, relationships, conventions]

## Common Queries
[Frequently used patterns]

## References
- [references/schema.md] - Full schema docs
```

### 2. File Format Processing

**Create a skill when** you need to process specific file formats with scripts.

**Examples:**
- PDF manipulation
- Document editing (DOCX, XLSX)
- Image processing
- Data transformation

**Skill pattern:**
```markdown
# pdf-processor skill
## Operations
- Extract text: `scripts/extract.py`
- Merge files: `scripts/merge.py`
- Fill forms: `scripts/fill_form.py`
```

### 3. Best Practices and Patterns

**Create a skill when** you want to document best practices for reference.

**Examples:**
- Error handling patterns
- API design principles
- Testing strategies
- Security guidelines

**Skill pattern:**
```markdown
# error-handling-patterns skill
## Exception vs Result Types
[Comparison with examples]

## Language-Specific Patterns
### Python
[Python examples]

### TypeScript
[TypeScript examples]
```

### 4. Code Generation Templates

**Create a skill when** you have templates for generating code.

**Examples:**
- CRUD service generation
- Component scaffolding
- API endpoint creation
- Test file generation

**Skill pattern:**
```markdown
# crud-service skill
## Templates
- [references/appservice-template.md]
- [references/dto-templates.md]
- [references/validator-template.md]
```

## When to Choose Commands

### 1. Multi-Phase Workflows

**Create a command when** the task requires coordinated phases with dependencies.

**Examples:**
- Feature development (discovery → design → implement → test → deploy)
- Code review (quality → security → testing → summary)
- TDD cycle (red → green → refactor)

**Command pattern:**
```markdown
## Phase 1: Discovery
Use Task tool with subagent_type="analyst"...

## Phase 2: Design
Context from Phase 1...
Use Task tool with subagent_type="architect"...

## Phase 3: Implementation
Context from Phases 1-2...
```

### 2. Multi-Agent Coordination

**Create a command when** multiple specialized agents need to collaborate.

**Examples:**
- Full-stack feature (backend + frontend + QA)
- Security audit (multiple scanners)
- Release process (build + test + deploy)

**Command pattern:**
```markdown
## Phase 1: Backend Implementation
Use Task tool with subagent_type="backend-developer"

## Phase 2: Frontend Implementation (parallel possible)
Use Task tool with subagent_type="frontend-developer"
Context: API contracts from Phase 1

## Phase 3: QA Validation
Use Task tool with subagent_type="qa-engineer"
Context: Implementations from Phases 1-2
```

### 3. User-Configurable Actions

**Create a command when** users need to customize behavior via flags.

**Examples:**
- Review with different focus areas
- Deploy with different strategies
- Generate with different templates

**Command pattern:**
```markdown
## Configuration Options
- --security-focus: Emphasize security review
- --performance-critical: Add performance analysis
- --tdd-review: Include TDD compliance check
```

### 4. Action-Oriented Tasks

**Create a command when** the user is performing an action, not seeking knowledge.

**Examples:**
- `/review-pr 123` - Review a specific PR
- `/feature add-login` - Implement a feature
- `/deploy staging` - Deploy to environment

## Hybrid Patterns

### Commands Using Skills

Commands often reference skills for domain knowledge:

```markdown
# /feature-development command
## Phase 1: Architecture Design
Use Task tool with subagent_type="backend-architect"
Prompt: "Design the architecture. Reference the api-design-principles
skill for REST conventions and the postgresql skill for schema design."
```

### Skills Supporting Commands

Design skills to produce outputs that commands consume:

```
Command: /feature-development
    │
    ├── Phase 1 → Uses: business-requirements (skill)
    ├── Phase 2 → Uses: api-design-principles (skill)
    ├── Phase 3 → Uses: crud-service (skill)
    └── Phase 4 → Uses: e2e-testing-patterns (skill)
```

## Decision Flowchart

```
START
  │
  ├── Is this reusable knowledge?
  │     │
  │     ├── YES → Does it need multi-agent coordination?
  │     │           │
  │     │           ├── YES → Create COMMAND that references SKILL
  │     │           └── NO  → Create SKILL
  │     │
  │     └── NO → Continue...
  │
  ├── Is this a multi-phase workflow?
  │     │
  │     ├── YES → Create COMMAND
  │     └── NO  → Continue...
  │
  ├── Does user invoke it directly with arguments?
  │     │
  │     ├── YES → Create COMMAND
  │     └── NO  → Create SKILL
  │
  └── DEFAULT → Create SKILL
```

## Examples from This Codebase

### Skills (in `.claude/skills/`)

| Skill | Type | Purpose |
|-------|------|---------|
| crud-service | Generator | Generate ABP CRUD services |
| docker-dotnet-containerize | Tool | Create Docker configurations |
| code-review-excellence | Pattern | Code review best practices |
| efcore-patterns | Domain | EF Core entity configuration, migrations |
| error-handling-patterns | Pattern | Exception handling strategies |
| api-design-principles | Pattern | REST/GraphQL API design |

### Commands (in `.claude/commands/`)

| Command | Type | Purpose |
|---------|------|---------|
| feature/feature-development | Workflow | 12-phase feature implementation |
| review/code-review | Workflow | Multi-aspect code review |
| tdd/tdd-cycle | Workflow | Red-green-refactor cycle |
| debug/smart-debug | Workflow | Systematic debugging |
| git/git-workflow | Workflow | Git operations with PR creation |

## Summary

| Create a... | When you need... |
|-------------|------------------|
| **Skill** | Knowledge, templates, scripts, patterns |
| **Command** | Orchestration, multi-phase actions, agent coordination |
| **Both** | Complex workflows needing reusable knowledge |

**Rule of thumb:** If it's about **knowing**, create a skill. If it's about **doing**, create a command. If it's about **doing with knowledge**, create a command that references skills.
