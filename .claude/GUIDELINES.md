# Claude Code Organization Guidelines

This document defines the structure, conventions, and decision framework for organizing agents, commands, skills, and other Claude Code extensibility mechanisms in this repository.

> **Sources**: This guide incorporates best practices from:
> - [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
> - [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
> - [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
> - [Claude Code Docs](https://code.claude.com/docs/en/)

## Table of Contents

1. [Agentic Coding Best Practices](#agentic-coding-best-practices)
2. [Directory Structure](#directory-structure-overview)
3. [Choosing the Right Tool](#choosing-the-right-tool)
4. [Agents](#agents-agents)
5. [Agent Separation of Concerns](#agent-separation-of-concerns)
6. [Artifact Portability Rules](#artifact-portability-rules)
7. [Skills](#skills-skills)
8. [Commands](#commands-commands)
9. [Hooks](#hooks)
10. [Output Styles](#output-styles)
11. [Quick Reference](#quick-reference)

---

## Agentic Coding Best Practices

These practices come directly from Anthropic's official recommendations for effective agentic coding with Claude Code.

### The Agentic Feedback Loop

Claude operates in a fundamental feedback loop:

```
┌─────────────────────────────────────────────────────────────┐
│     GATHER CONTEXT → TAKE ACTION → VERIFY WORK → REPEAT    │
└─────────────────────────────────────────────────────────────┘
```

This pattern enables Claude to autonomously complete complex workflows by iteratively refining outputs.

### Thinking Modes

Use specific phrases to trigger extended thinking with progressively increasing budgets:

| Phrase | Thinking Level | When to Use |
|--------|----------------|-------------|
| `"think"` | Baseline | Standard complex tasks |
| `"think hard"` | Increased | Multi-step reasoning |
| `"think harder"` | High | Complex architectural decisions |
| `"ultrathink"` | Maximum | Critical, high-stakes decisions |

**Example**: "Think hard about the best approach to refactor this authentication system."

### Effective Workflows

#### 1. Explore → Plan → Code → Commit

```
1. Ask Claude to read relevant files without writing code
2. Request a plan (use "think" for extended thinking)
3. Ask Claude to implement the solution
4. Request commit and PR creation
```

#### 2. Test-Driven Development (TDD)

```
1. Write tests based on expected input/output pairs
2. Confirm tests fail (without implementation code)
3. Commit tests
4. Ask Claude to write passing code, iterating until all tests pass
5. Commit successful code
```

**Key**: Be explicit about TDD to prevent Claude from creating mock implementations.

#### 3. Visual Iteration

```
1. Provide screenshot tools (Puppeteer MCP, manual capture)
2. Provide design mock
3. Ask Claude to implement, take screenshots, iterate
4. Commit when satisfied
```

### Prompting Best Practices

**Be specific** - Specificity significantly improves first-attempt success rates.

| Poor | Good |
|------|------|
| "add tests for foo.py" | "write a new test case for foo.py, covering the edge case where the user is logged out. avoid mocks" |
| "fix the bug" | "fix the null reference exception in UserService.GetById when user doesn't exist" |
| "improve performance" | "optimize the N+1 query in OrderRepository.GetWithItems using Include" |

### Context Management Strategies

#### CLAUDE.md Optimization

Your `CLAUDE.md` files become part of Claude's prompts and should document:
- Common bash commands
- Core files and utility functions
- Code style guidelines
- Testing instructions
- Repository etiquette
- Developer environment setup
- Project-specific warnings

**Placement options**:
- Repo root (primary)
- Parent directories (monorepos)
- Child directories (subdirectory-specific)
- `~/.claude/CLAUDE.md` (global)

#### Context Preservation Techniques

| Technique | How |
|-----------|-----|
| **Mention files directly** | Use tab-completion to reference specific files/folders |
| **Provide images** | Paste screenshots, drag-drop, or provide file paths |
| **Include URLs** | Paste links for Claude to fetch |
| **Pass data multiple ways** | Copy-paste, pipe (`cat foo.txt \| claude`), have Claude pull via tools |
| **Use `/clear` frequently** | Reset context between tasks to prevent degradation |

### Subagent Usage

Use subagents for:
- **Parallelization**: Multiple subagents handle different tasks simultaneously
- **Context isolation**: Each operates in its own context window, returning only relevant summaries
- **Information-heavy tasks**: Where most data proves irrelevant to the main thread

**Best practice**: Tell Claude to use subagents to verify details or investigate particular questions, especially early in a conversation.

### Multi-Claude Workflows

#### Parallel Code Review
Have one Claude write code; another reviews/tests it. Maintain separate context for better results.

#### Multiple Worktrees
Run 3-4 Claude sessions on independent tasks simultaneously:

```bash
# Create worktree
git worktree add ../project-feature-a feature-a

# Launch Claude in worktree
cd ../project-feature-a && claude

# Clean up when done
git worktree remove ../project-feature-a
```

### Complex Tasks with Checklists

For large tasks with multiple steps, have Claude use a Markdown checklist:

```markdown
Task Progress:
- [ ] Step 1: Analyze the form
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Execute operation
- [ ] Step 5: Verify output
```

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

### Detailed Comparison

#### Skills vs Prompts vs Subagents

| Aspect | Skills | Prompts | Subagents |
|--------|--------|---------|-----------|
| **Persistence** | Across conversations | Single conversation | Per-task |
| **Activation** | Automatic/dynamic | Each explicit request | Delegated |
| **Context** | Progressive disclosure | In main context | Isolated window |
| **Best Use** | Repeated procedures | One-off requests | Complex workflows |

#### Common Scenarios

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

### Built-in Subagents

Claude Code includes two built-in subagents:

| Agent | Purpose | Tools | Mode |
|-------|---------|-------|------|
| **Plan** | Research and gather information before presenting a plan | Read-only | Plan mode only |
| **Explore** | Fast, lightweight codebase search and analysis | `ls`, `git status`, `find`, `cat`, `head`, `tail` | Read-only |

**Note**: Subagents cannot spawn other subagents (prevents infinite nesting).

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
name: agent-name                    # Required: kebab-case, lowercase letters/numbers/hyphens
description: "Purpose. Use PROACTIVELY when..."  # Required: max 1024 chars
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

### Tool Permissions Strategy

**Principle**: Least privilege - only grant necessary tools.

| Agent Type | Recommended Tools | Rationale |
|------------|-------------------|-----------|
| **Read-only** (reviewers, auditors) | `Read, Grep, Glob` | Cannot modify code |
| **Research** | `Read, Grep, Glob, WebFetch, WebSearch` | Information gathering |
| **Code writers** | `Read, Write, Edit, Bash, Glob, Grep` | Full implementation |
| **Documentation** | `Read, Write, Edit, Glob, Grep, WebFetch, WebSearch` | Content creation |

**Warning**: Omitting the `tools` field grants access to **all available tools** (including MCP). Always whitelist intentionally.

### Permission Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `default` | Standard permission prompts | Normal operation |
| `acceptEdits` | Auto-accept edit operations | Trusted agents |
| `bypassPermissions` | Skip all permission checks | Fully automated workflows |

### Model Selection

| Model | Characteristics | Best For |
|-------|-----------------|----------|
| `haiku` | Fast, economical | Quick tasks, simple operations |
| `sonnet` | Balanced | Standard development tasks |
| `opus` | Powerful reasoning | Complex architectural decisions, security reviews |

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
6. **Third-person descriptions** - Write descriptions in third person for system prompt injection

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

---

## Skills (`skills/`)

Skills are knowledge domains with resources. Organized **by topic**.

### Core Principle: Concise is Key

The context window is a shared resource. Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Default assumption**: Claude is already very smart. Only add context Claude doesn't already have.

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
name: skill-name                    # Required: max 64 chars, lowercase letters/numbers/hyphens only
description: |                      # Required: max 1024 chars, no XML tags
  What it does. Use when: (1) scenario, (2) scenario, (3) scenario.
allowed-tools: Read, Grep, Glob     # Optional: restrict tools
---

# Skill Name

## Quick Start
[Immediate, actionable content]

## Core Workflow
[Step-by-step instructions]

## Advanced Features
**Feature A**: See [FEATURE_A.md](references/feature_a.md)
**Feature B**: See [FEATURE_B.md](references/feature_b.md)
```

### Naming Conventions

Use **gerund form** (verb + -ing) for clarity:

| Good (Gerund) | Acceptable | Avoid |
|---------------|------------|-------|
| `processing-pdfs` | `pdf-processing` | `helper` |
| `analyzing-spreadsheets` | `spreadsheet-analysis` | `utils` |
| `managing-databases` | `database-management` | `tools` |
| `testing-code` | `code-testing` | `documents` |

### Writing Effective Descriptions

**Always write in third person** - descriptions are injected into system prompts.

| Good | Avoid |
|------|-------|
| "Processes Excel files and generates reports" | "I can help you process Excel files" |
| "Extracts text from PDF documents" | "You can use this to extract text" |

**Be specific and include triggers:**

```yaml
# Good: Specific with triggers
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Bad: Vague
description: Helps with documents
```

### Progressive Disclosure

Skills use three-level loading for context efficiency:

| Level | What Loads | Token Cost | When |
|-------|------------|------------|------|
| **1. Discovery** | `name` + `description` only | ~100 tokens | Startup (all skills) |
| **2. Instructions** | Full `SKILL.md` body | <5k tokens | When triggered |
| **3. Resources** | Scripts/references | As needed | On-demand |

### Progressive Disclosure Patterns

#### Pattern 1: High-level guide with references

```markdown
# PDF Processing

## Quick start
[Immediate actionable code]

## Advanced features
**Form filling**: See [FORMS.md](FORMS.md)
**API reference**: See [REFERENCE.md](REFERENCE.md)
**Examples**: See [EXAMPLES.md](EXAMPLES.md)
```

#### Pattern 2: Domain-specific organization

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    └── product.md (API usage, features)
```

#### Pattern 3: Conditional details

```markdown
## Creating documents
Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents
For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
```

### Degrees of Freedom

Match specificity to task fragility:

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** (text instructions) | Multiple valid approaches | "Analyze code structure, check for bugs, suggest improvements" |
| **Medium** (pseudocode/params) | Preferred pattern exists | Template with customizable parameters |
| **Low** (exact scripts) | Fragile, error-prone operations | "Run exactly this script: `python migrate.py --verify`" |

### Skill Best Practices

1. **Keep SKILL.md under 500 lines** - Split content into separate files if needed
2. **Keep references one level deep** - All reference files should link directly from SKILL.md
3. **Include table of contents** - For reference files longer than 100 lines
4. **Test with all models** - What works for Opus might need more detail for Haiku
5. **Avoid time-sensitive information** - Use "old patterns" sections instead of dates
6. **Use consistent terminology** - Choose one term and use it throughout

### Workflow Pattern for Skills

For complex operations, provide a checklist:

```markdown
## Document processing workflow

Copy this checklist and track progress:

```
Task Progress:
- [ ] Step 1: Analyze input
- [ ] Step 2: Create mapping
- [ ] Step 3: Validate
- [ ] Step 4: Execute
- [ ] Step 5: Verify output
```
```

### Skill Rules

1. **Self-contained** - Each skill folder has everything needed
2. **Topic-focused** - One skill = one knowledge domain
3. **Concise entry** - SKILL.md under 500 lines
4. **Specific triggers** - Description lists 3+ trigger scenarios
5. **Third-person descriptions** - Write in third person for system prompt compatibility

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

### Command Storage Locations

| Location | Scope | Priority |
|----------|-------|----------|
| `.claude/commands/` | Project-specific | Highest |
| `~/.claude/commands/` | Personal (all projects) | Lower |
| MCP server prompts | Dynamic | As configured |

Project commands override user commands with identical names.

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

### Using $ARGUMENTS

The `$ARGUMENTS` keyword captures user input after the command name:

```markdown
---
description: Analyze and fix GitHub issue
---

Please analyze and fix the GitHub issue: $ARGUMENTS.

1. Fetch issue details
2. Understand the problem
3. Propose solution
4. Implement fix
```

**Usage**: `/fix-issue 123` → `$ARGUMENTS` becomes `123`

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
| `PreToolUse` | Before tool call | Block/validate operations, custom permissions |
| `PostToolUse` | After tool call | Auto-format, logging |
| `PermissionRequest` | When permission dialog shown | Custom approval logic |
| `Notification` | On notification | Custom alerts |
| `Stop` | Response complete | Cleanup, summary |
| `SubagentStop` | Subagent completes | HITL control, next-step prompts |
| `UserPromptSubmit` | Before processing | Input validation |
| `SessionStart` | Session begins | Initialization |
| `SessionEnd` | Session ends | Cleanup |
| `PreCompact` | Before context compaction | Custom summarization |

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

### Matcher Syntax

| Pattern | Matches |
|---------|---------|
| `Edit` | Exact match |
| `Edit\|Write` | Either Edit or Write |
| `*` | All tools |
| `Task` | Subagent tasks |
| `WebFetch\|WebSearch` | Web operations |

### PreToolUse Decision Control

PreToolUse hooks can control tool execution:

| Exit Code | Effect |
|-----------|--------|
| `0` | Allow tool use |
| `2` | Block tool use |
| Other | Ask for permission |

### Hook Use Cases

| Use Case | Event | Example |
|----------|-------|---------|
| Auto-format on save | `PostToolUse` | Run prettier after Edit/Write |
| Block production changes | `PreToolUse` | Exit 2 for production files |
| Custom notifications | `Notification` | Send to Slack |
| Logging | `PostToolUse` | Log all commands |
| Convention feedback | `PostToolUse` | Check code style |
| HITL workflow | `SubagentStop` | Print next command |

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
5. Write description in third person

**Or use:** `python .claude/skills/claude-artifact-creator/scripts/init_agent.py <name> --path .claude/agents`

### Adding a New Skill

1. Create `skills/{skill-name}/SKILL.md`
2. Add specific trigger scenarios in description (3+)
3. Keep SKILL.md under 500 lines
4. Add `references/` for detailed docs
5. Add `scripts/` for deterministic operations
6. Test with Haiku, Sonnet, and Opus

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

### Skill Quality Checklist

Before sharing a skill:

- [ ] Description is specific and includes key terms
- [ ] Description includes both what the skill does and when to use it
- [ ] SKILL.md body is under 500 lines
- [ ] Additional details are in separate files (if needed)
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep
- [ ] Tested with Haiku, Sonnet, and Opus

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

### Good: Concise Skill Content

```markdown
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

### Bad: Verbose Skill Content

```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but we
recommend pdfplumber because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below...
```

---

## Resources

- **Official Documentation**: [code.claude.com/docs](https://code.claude.com/docs/en/)
- **Best Practices**: [Anthropic Engineering Blog](https://www.anthropic.com/engineering/claude-code-best-practices)
- **Agent SDK**: [Building Agents Guide](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- **Skills Best Practices**: [Skill Authoring Guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Full migration guide**: `.claude/skills/claude-artifact-creator/references/agent-refactoring-guide.md`
- **Migration analysis**: `docs/agent-skill-command-migration.md`
