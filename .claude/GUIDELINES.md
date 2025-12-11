# Claude Code Organization Guidelines

This document defines the structure, conventions, and decision framework for organizing agents, commands, skills, and other Claude Code extensibility mechanisms in this repository.

## Table of Contents

1. [Directory Structure](#directory-structure-overview)
2. [Choosing the Right Tool](#choosing-the-right-tool)
3. [Agents](#agents-agents)
4. [Agent Separation of Concerns](#agent-separation-of-concerns)
5. [Artifact Portability Rules](#artifact-portability-rules)
6. [Skills](#skills-skills)
7. [Commands](#commands-commands)
8. [Hooks](#hooks)
9. [Output Styles](#output-styles)
10. [Quick Reference](#quick-reference)

---

## Directory Structure Overview

```
.claude/
├── GUIDELINES.md           # This file
├── agents/                 # AI agent definitions (BY ROLE)
│   ├── architects/         # System designers and planners
│   ├── reviewers/          # Code and security reviewers
│   ├── engineers/          # Implementation specialists
│   └── specialists/        # Domain-specific experts
├── commands/               # Slash commands (BY ACTION)
│   ├── review/             # Code review workflows
│   ├── generate/           # Scaffolding and generation
│   ├── debug/              # Error diagnosis and debugging
│   ├── refactor/           # Code improvement and cleanup
│   ├── tdd/                # Test-driven development
│   ├── feature/            # Feature development workflows
│   ├── git/                # Git and PR workflows
│   ├── explain/            # Code explanation
│   ├── optimize/           # Performance and prompt optimization
│   └── team/               # Team collaboration
└── skills/                 # Knowledge domains (BY TOPIC)
    └── {topic-name}/       # Each skill is a self-contained topic
```

---

## Choosing the Right Tool

Claude Code provides multiple extensibility mechanisms. Choosing the right one depends on **four key factors**:

1. **Nature of the Task** - What are you trying to accomplish?
2. **Invocation Control** - Who/what triggers the action?
3. **Complexity/Structure** - How is the logic organized?
4. **Context Management** - How is context handled?

### Decision Matrix

| Mechanism | Invocation | Context | Best For |
|-----------|------------|---------|----------|
| **Skill** | Model-invoked (automatic) | Progressive disclosure | Reusable domain expertise |
| **Agent** | Auto-delegated or explicit | Isolated (separate window) | Autonomous complex tasks |
| **Command** | User-invoked (`/cmd`) | Expands into main context | Atomic, frequent actions |
| **Hook** | Event-triggered (deterministic) | N/A (shell execution) | Guardrails, automation |
| **Output Style** | User-configured | Modifies system prompt | Persona changes |
| **CLAUDE.md** | Always loaded | Persistent background | Project-wide context |

### Decision Flowchart

```
START: What do you need?
│
├─ "Deterministic action on every tool call" → HOOK
│
├─ "Change Claude's overall behavior/persona" → OUTPUT STYLE
│
├─ "Project-wide context always needed" → CLAUDE.md
│
├─ "User explicitly triggers action" → COMMAND
│   └─ Does it need multiple files, scripts, templates?
│       ├─ YES → Consider SKILL instead (progressive disclosure)
│       └─ NO → COMMAND ✓
│
├─ "Claude should auto-detect when to use" → SKILL or AGENT
│   └─ Does it need context isolation?
│       ├─ YES → AGENT (separate context window)
│       └─ NO → SKILL (progressive disclosure)
│
└─ "Complex multi-step task with specialized persona" → AGENT
```

### Detailed Guidelines

#### 1. Task Nature (What are you building?)

| Use Case | Best Tool | Rationale |
|----------|-----------|-----------|
| **Autonomous Workflow** | **Agent** | Specialized persona with context isolation |
| **Reusable Domain Expertise** | **Skill** | Auto-triggered knowledge with resources |
| **Frequent Atomic Actions** | **Command** | User-controlled shortcuts |
| **Deterministic Guardrails** | **Hook** | Always-run shell commands |
| **Persona/Behavior Change** | **Output Style** | System prompt modification |
| **Background Knowledge** | **CLAUDE.md** | Always-loaded project context |

#### 2. Invocation Control (Who triggers the action?)

| Mechanism | Trigger | Control Level |
|-----------|---------|---------------|
| **Skill** | Model decides based on `description` | Proactive/Automatic |
| **Agent** | Auto-delegated or "Use the X agent" | Semi-automatic |
| **Command** | User types `/command` | Explicit/Manual |
| **Hook** | Lifecycle event (PreToolUse, etc.) | Deterministic |
| **Output Style** | `/output-style` or settings | User-configured |

#### 3. Complexity and Structure

| Feature | File Structure | Multi-File? | Code Integration |
|---------|----------------|-------------|------------------|
| **Agent** | Single `.md` file | No | Full tool access, system prompt |
| **Skill** | Directory with `SKILL.md` | Yes (scripts, refs, assets) | Scripts for deterministic ops |
| **Command** | Single `.md` file | No | Bash via `!` prefix |
| **Hook** | JSON config + scripts | Yes (external scripts) | Shell commands |
| **Output Style** | Single `.md` file | No | System prompt only |

#### 4. Context Management

| Mechanism | Context Behavior | Efficiency |
|-----------|------------------|------------|
| **Skill** | Progressive disclosure (3 levels) | Most efficient |
| **Agent** | Isolated context window | Prevents pollution |
| **Command** | Full expansion into main context | Less efficient for large prompts |
| **Hook** | No context (shell execution) | Zero context cost |

### Common Scenarios

| Scenario | Recommended | Why |
|----------|-------------|-----|
| "Auto-format files after edit" | **Hook** | Deterministic, every time |
| "Code review expertise" | **Skill** | Auto-triggered domain knowledge |
| "Run tests and fix failures" | **Agent** | Complex multi-step, context isolation |
| "Quick commit shortcut" | **Command** | User-invoked atomic action |
| "Teaching mode with insights" | **Output Style** | Behavior change |
| "Project coding standards" | **CLAUDE.md** | Always-needed context |

### Hybrid Architecture

The most powerful workflows combine mechanisms:

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE.md (Always Loaded)                │
│              Project context, coding standards              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Command (Workflow Entry)                    │
│         /add-feature orchestrates multi-agent flow          │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Agent (Specialist)│ │ Skill (Expertise)│ │ Hook (Guardrail)│
│ backend-architect │ │ Domain knowledge │ │ Auto-format     │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## Agents (`agents/`)

Agents are AI personas with specialized capabilities. Organized **by role** (what they ARE).

### Categories

| Folder | Purpose | Examples |
|--------|---------|----------|
| `architects/` | Design systems, plan implementations | backend-architect, business-analyst |
| `reviewers/` | Analyze and critique code | code-reviewer, security-engineer |
| `engineers/` | Build and implement solutions | abp-developer, react-developer |
| `specialists/` | Deep domain expertise | debugger |

### Agent File Format

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

### Decision Tree: Where Does My Agent Go?

```
Is it primarily about designing/planning? → architects/
Is it primarily about reviewing/critiquing? → reviewers/
Is it primarily about building/implementing? → engineers/
Is it a programming language specialist? → language-experts/
Does it have deep domain expertise? → specialists/
```

### Agent Rules

1. **Single responsibility** - One agent, one clear role
2. **No duplicates** - Each agent exists in exactly one location
3. **Least privilege** - Only grant necessary tools
4. **Clear triggers** - Include "Use PROACTIVELY when..." in description
5. **Lean prompts** - Agent prompts should be <150 lines (see [Agent Separation of Concerns](#agent-separation-of-concerns))

---

## Agent Separation of Concerns

Agents should be **thin coordinators**, not repositories of embedded knowledge. This principle ensures maintainability, reusability, and context efficiency.

### The Core Principle

| Component | Contains | Does NOT Contain |
|-----------|----------|------------------|
| **Agent** | Identity, coordination, tool permissions, skill references | Code templates, output formats, CLI commands |
| **Skill** | Procedural knowledge, patterns, templates, domain expertise | Execution logic, atomic actions |
| **Command** | Executable atomic actions, user-invoked shortcuts | Domain knowledge, reusable patterns |

### What Belongs Where

```
Agent ("What I am")           Skill ("What to know")         Command ("What to do")
─────────────────────        ──────────────────────         ────────────────────────
• Role definition            • Code patterns                • /add-migration
• Core responsibilities      • Output format templates      • /run-tests
• Tool permissions           • Best practices               • /scaffold-entity
• Skill references           • Step-by-step procedures      • /generate-user-stories
• Coordination logic         • Domain-specific knowledge    • /design-api
• Context management         • Reusable templates
```

### Detection: When to Extract

**Extract to Skill when agent contains:**

| Indicator | Lines | Action |
|-----------|-------|--------|
| Code samples (`\`\`\`csharp`, `\`\`\`typescript`) | >20 | Extract to skill |
| Output format templates | >15 | Extract to skill |
| Step-by-step procedures | >10 | Extract to skill |
| Domain-specific patterns | Any | Extract to skill |
| Content repeated across agents | Any | Create shared skill |

**Extract to Command when agent contains:**

| Indicator | Action |
|-----------|--------|
| "Run this command: ..." | Extract to command |
| "Execute the following: ..." | Extract to command |
| Single-purpose atomic tasks | Extract to command |
| Tasks with arguments/flags | Extract to command |
| Frequently invoked tasks | Extract to command |

### Before/After Example

**BEFORE (Agent with embedded knowledge - 345 lines):**
```markdown
# ABP Developer Agent

## Project Structure
```
api/src/
├── {ProjectName}.Domain/
[... 40 lines of directory structure]
```

## Code Patterns

### Entity Pattern
```csharp
public class {Entity} : FullAuditedAggregateRoot<Guid>
{
    [... 35 lines of C# code]
}
```

### AppService Pattern
```csharp
[... 80 lines of C# code]
```

## Build Commands
```bash
dotnet build api/{SolutionName}.slnx
dotnet test api/test/{ProjectName}.Application.Tests
[... 20 lines of commands]
```
```

**AFTER (Lean agent - 85 lines):**
```markdown
# ABP Developer Agent

You are a Senior .NET Developer specializing in ABP Framework.

## Project Context

Before implementation, read:
1. `docs/project-context.md` - Project structure, paths, conventions
2. `docs/entity-glossary.md` - Domain entities
3. `docs/technical-specification.md` - API contracts

## Implementation Approach

1. **Apply skills** (auto-loaded via frontmatter):
   - `abp-framework-patterns` - Entity, AppService patterns
   - `crud-service` - CRUD scaffolding workflow
   - `dotnet-async-patterns` - Async best practices

2. **Use commands** for atomic tasks:
   - `/scaffold-entity <name>` - Generate entity files
   - `/add-migration <name>` - Create EF Core migration
   - `/run-tests backend` - Run backend tests

3. **Follow existing patterns** in the codebase

## Constraints
[Concise list of rules]
```

### Refactoring Workflow

1. **Audit**: Count agent lines (`wc -l agents/**/*.md`)
2. **Identify**: Find code blocks, templates, commands
3. **Extract**: Move to skills or commands
4. **Reference**: Update agent to reference extracted content
5. **Validate**: Verify agent produces same outputs

### Reference Syntax in Agents

```markdown
## Implementation Approach

1. Apply `skill-name` skill for:
   - Pattern 1
   - Pattern 2

2. Use `/command-name` for atomic tasks

3. Reference `docs/project-context.md` for project-specific values
```

### Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Code templates in agent | Agent too large, not reusable | Extract to skill |
| CLI commands in agent | Not reusable, hard to maintain | Extract to command |
| Repeated content across agents | Duplication, inconsistency | Create shared skill |
| Project-specific paths in agent | Not portable | Move to `docs/project-context.md` |

---

## Artifact Portability Rules

**CRITICAL**: All Claude artifacts (agents, skills, commands) must be **generic and reusable**. They should work across any project without modification.

### Prohibited Content in Artifacts

| Content Type | Example | Alternative |
|--------------|---------|-------------|
| **Project names** | `ClinicManagementSystem`, `MyApp` | Use `{ProjectName}` placeholder |
| **Entity names** | `Patient`, `Doctor`, `Order` | Use `{Entity}`, `{EntityName}` placeholders |
| **Hardcoded paths** | `api/src/ClinicManagementSystem.Domain/` | Use dynamic detection or `{ProjectName}` |
| **Solution files** | `ClinicManagementSystem.slnx` | Use `{SolutionName}.slnx` or `find` command |
| **Permission names** | `ClinicPermissions.Patients.Create` | Use `{Project}Permissions.{Feature}.{Action}` |
| **Namespace prefixes** | `ClinicManagementSystem.` | Use `{ProjectName}.` |

### Dynamic Project Detection

For commands and agents that need to locate project files, use dynamic detection:

```bash
# Find EntityFrameworkCore project
EF_PROJECT=$(find api/src -maxdepth 1 -type d -name "*EntityFrameworkCore" | head -1)

# Find DbMigrator project
MIGRATOR=$(find api/src -maxdepth 1 -type d -name "*DbMigrator" | head -1)

# Find solution file
SOLUTION=$(find api -maxdepth 1 -name "*.slnx" -o -name "*.sln" | head -1)
```

### Where Project-Specific Content Belongs

| Location | Purpose |
|----------|---------|
| `CLAUDE.md` | Project overview, build commands, entity list |
| `docs/architecture/README.md` | Project structure, paths, conventions |
| `docs/domain/entities/` | Entity definitions, business rules |
| `docs/project-context.md` | All project-specific values in one place |

### Validation Checklist

Before committing any artifact, verify:

- [ ] No hardcoded project names (search for your project name)
- [ ] No specific entity names in examples (use `{Entity}`, `Product`, `Order` as generic examples)
- [ ] Paths use placeholders or dynamic detection
- [ ] Code samples use generic class names
- [ ] Permissions use `{Project}Permissions.{Feature}.{Action}` pattern
- [ ] Skills reference `CLAUDE.md` or `docs/` for project context

### Resources

- Full migration guide: `.claude/skills/claude-artifact-creator/references/agent-refactoring-guide.md`
- Migration analysis: `docs/agent-skill-command-migration.md`

---

## Skills (`skills/`)

Skills are knowledge domains with resources. Organized **by topic**.

### Skill Structure

```
skills/
└── {skill-name}/
    ├── SKILL.md              # Required - entry point (<500 lines)
    ├── references/           # On-demand documentation
    ├── assets/               # Templates, boilerplate
    └── scripts/              # Executable helpers
```

### SKILL.md Format

```yaml
---
name: skill-name                    # Required: kebab-case
description: |                      # Required: trigger mechanism
  What it does. Use when: (1) scenario, (2) scenario, (3) scenario.
allowed-tools: Read, Grep, Glob     # Optional: restrict tools
---

# Skill Name

## When to Use
[Triggers and use cases]

## Core Workflow
[Step-by-step instructions]

## References
- [topic.md](references/topic.md)
```

### Progressive Disclosure

Skills use three-level loading for context efficiency:

1. **Level 1 (Discovery)**: Only `name` + `description` (~50 tokens)
2. **Level 2 (Instructions)**: Full `SKILL.md` body when triggered
3. **Level 3 (Resources)**: Scripts/references loaded on-demand

### Skill Rules

1. **Self-contained** - Each skill folder has everything needed
2. **Topic-focused** - One skill = one knowledge domain
3. **Concise entry** - SKILL.md under 500 lines
4. **Specific triggers** - Description lists 3+ trigger scenarios

---

## Commands (`commands/`)

Commands are slash-invokable workflows. Organized **by action** (what user wants to DO).

### Categories

| Folder | Purpose | Examples |
|--------|---------|----------|
| `review/` | Analyze existing code | code-review, pr-enhance |
| `generate/` | Create new code/docs | scaffold, doc-generate |
| `debug/` | Diagnose and fix issues | error-trace, smart-debug |
| `refactor/` | Improve existing code | cleanup, tech-debt |
| `tdd/` | Test-driven development | tdd-cycle, tdd-red |
| `feature/` | End-to-end feature work | full-stack-feature |
| `git/` | Version control workflows | git-workflow |

### Command File Format

```yaml
---
description: Brief description      # Required for SlashCommand tool
allowed-tools: Bash(git:*), Read    # Optional: restrict tools
argument-hint: [file] [options]     # Optional: shown in autocomplete
model: sonnet                       # Optional: override model
---

[Command instructions using $ARGUMENTS]

## Context
- Current status: !`git status`     # Bash execution with ! prefix

## Steps
1. [Step 1]
2. [Step 2]
```

### Command vs Skill Decision

| Aspect | Command | Skill |
|--------|---------|-------|
| Invocation | Manual (`/cmd`) | Automatic |
| Complexity | Single file | Directory with resources |
| Use case | Frequent shortcuts | Domain expertise |
| Context | Full expansion | Progressive disclosure |

---

## Hooks

Hooks are deterministic shell commands that execute at lifecycle events.

### Hook Events

| Event | When | Use Case |
|-------|------|----------|
| `PreToolUse` | Before tool call | Block/validate operations |
| `PostToolUse` | After tool call | Auto-format, logging |
| `Notification` | On notification | Custom alerts |
| `Stop` | Response complete | Cleanup, summary |
| `UserPromptSubmit` | Before processing | Input validation |

### Hook Configuration

Location: User settings (`~/.claude/settings.json`) or project (`.claude/settings.local.json`)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$(jq -r '.tool_input.file_path')\""
          }
        ]
      }
    ]
  }
}
```

### Hook Rules

1. **Security first** - Review all hook code before registering
2. **Matcher specificity** - Use specific matchers (`Edit|Write`) over wildcards
3. **Error handling** - Hooks should handle failures gracefully
4. **Exit codes** - Return 2 to block, 0 to allow

---

## Output Styles

Output styles modify Claude's system prompt behavior.

### Built-in Styles

| Style | Purpose |
|-------|---------|
| **Default** | Software engineering efficiency |
| **Explanatory** | Educational insights while coding |
| **Learning** | Collaborative learn-by-doing mode |

### Custom Output Style Format

Location: `.claude/output-styles/` or `~/.claude/output-styles/`

```yaml
---
name: My Custom Style
description: Description for UI
keep-coding-instructions: false     # true to keep coding prompt
---

# Custom Instructions

You are an interactive CLI tool that...

## Specific Behaviors
...
```

---

## Quick Reference

### Creating New Artifacts

Use the **claude-artifact-creator** skill for guided artifact creation:

```bash
# Initialize a new skill
python .claude/skills/claude-artifact-creator/scripts/init_skill.py <name> --path .claude/skills --template <type>

# Initialize a new agent
python .claude/skills/claude-artifact-creator/scripts/init_agent.py <name> --path .claude/agents --template <type>

# Initialize a new command
python .claude/skills/claude-artifact-creator/scripts/init_command.py <name> --path .claude/commands --template <type>
```

Or simply ask: "Create an agent for [purpose]" or "Create a skill for [domain]" and Claude will use the skill automatically.

### Adding a New Agent

1. Determine category using decision tree
2. Create `agents/{category}/{agent-name}.md`
3. Include "Use PROACTIVELY when..." in description
4. Grant only necessary tools

**Or use:** `python .claude/skills/claude-artifact-creator/scripts/init_agent.py <name> --path .claude/agents`

### Adding a New Skill

1. Create `skills/{skill-name}/SKILL.md`
2. Add specific trigger scenarios in description
3. Add `references/` for detailed docs
4. Add `scripts/` for deterministic operations

**Or use:** `python .claude/skills/claude-artifact-creator/scripts/init_skill.py <name> --path .claude/skills`

### Adding a New Command

1. Determine category using decision tree
2. Create `commands/{category}/{command-name}.md`
3. Use `$ARGUMENTS` for user input
4. Add `description` frontmatter for SlashCommand tool

**Or use:** `python .claude/skills/claude-artifact-creator/scripts/init_command.py <name> --path .claude/commands`

### Adding a Hook

1. Identify the lifecycle event
2. Create script in `.claude/hooks/` (optional)
3. Configure in settings JSON
4. Test with specific matcher before wildcards

---

## Migration Checklist

When reorganizing existing files:

- [ ] Identify duplicates and consolidate
- [ ] Move agents to role-based categories
- [ ] Move commands to action-based categories
- [ ] Update cross-references between files
- [ ] Remove empty folders
- [ ] Verify all agent/skill references are correct
- [ ] Test hook configurations

### Agent Refactoring Checklist

When agents grow too large (>150 lines):

- [ ] Audit agent size: `wc -l agents/**/*.md`
- [ ] Identify code blocks (```csharp, ```typescript, etc.)
- [ ] Extract code patterns to skills
- [ ] Identify CLI commands and build scripts
- [ ] Extract atomic actions to commands
- [ ] Move project-specific paths to `docs/project-context.md`
- [ ] Update agent to reference skills and commands
- [ ] Verify agent produces same outputs
- [ ] Update agent frontmatter with `skills:` field

---

## Examples

### Good Organization

```
agents/reviewers/code-reviewer.md      # Role-based
commands/review/code-review.md         # Action-based, references agent
skills/code-review-excellence/         # Knowledge domain with resources
hooks/auto-format.py                   # Deterministic formatting
```

### Bad Organization

```
agents/code-review-workflow/           # Workflow-based (wrong)
commands/code-reviewer/                # Role-based folder (wrong)
skills/utils.md                        # Too vague (wrong)
```

### Bad: Agent with Embedded Knowledge

```markdown
# Developer Agent (BAD - 400+ lines)

## Code Patterns
```csharp
// 100 lines of code templates      ← Should be in skill
```

## Build Commands
```bash
dotnet build...                       ← Should be a command
dotnet test...                        ← Should be a command
```

## Project Structure
api/src/{ProjectName}.Domain/         ← Should be in docs/project-context.md
```

### Good: Lean Agent with References

```markdown
# Developer Agent (GOOD - 80 lines)

## Implementation Approach

1. Apply `framework-patterns` skill   ← References skill
2. Use `/run-tests` command           ← References command
3. Read `docs/project-context.md`     ← References docs
```
