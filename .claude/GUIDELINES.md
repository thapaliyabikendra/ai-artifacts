# Claude Code Organization Guidelines

This document defines the structure and conventions for organizing agents, commands, and skills in this repository.

## Directory Structure Overview

```
.claude/
├── GUIDELINES.md           # This file
├── agents/                 # AI agent definitions (BY ROLE)
│   ├── architects/         # System designers and planners
│   ├── reviewers/          # Code and security reviewers
│   ├── engineers/          # Implementation specialists
│   ├── specialists/        # Domain-specific experts
│   └── language-experts/   # Programming language specialists
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

## Agents (`agents/`)

Agents are AI personas with specialized capabilities. They are organized **by role/capability** (what they ARE), not by workflow.

### Categories

| Folder | Purpose | Examples |
|--------|---------|----------|
| `architects/` | Design systems, plan implementations, make architectural decisions | backend-architect, database-architect, docs-architect |
| `reviewers/` | Analyze and critique code, identify issues | code-reviewer, security-reviewer |
| `engineers/` | Build and implement solutions | frontend-developer, prompt-engineer, dx-optimizer |
| `specialists/` | Deep expertise in specific domains or tasks | debugger, test-automator, tdd-orchestrator, mermaid-expert |
| `language-experts/` | Programming language-specific knowledge | csharp-pro, typescript-pro, sql-pro |

### Naming Conventions

- Use **kebab-case** for file names: `code-reviewer.md`, `backend-architect.md`
- Name should describe the **role**, not the task: `security-reviewer.md` (not `security-review.md`)
- Suffix patterns:
  - `-architect` for system designers
  - `-reviewer` for analysis/critique roles
  - `-engineer` for builders
  - `-pro` or `-expert` for language/domain specialists
  - `-optimizer` for improvement-focused roles

### Agent File Structure

```yaml
---
name: agent-name
description: One-line description of what this agent does. Use PROACTIVELY when...
model: sonnet | haiku | opus  # Choose appropriate model
---

You are a [role description]...

## Expert Purpose
[Detailed explanation of the agent's mission]

## Capabilities
[Bulleted list of what this agent can do]

## Behavioral Traits
[How the agent should behave]

## Response Approach
[Step-by-step methodology]

## Example Interactions
[Sample prompts this agent handles]
```

### Decision Tree: Where Does My Agent Go?

```
Is it primarily about designing/planning?
  └─ YES → architects/
  └─ NO ↓

Is it primarily about reviewing/critiquing?
  └─ YES → reviewers/
  └─ NO ↓

Is it primarily about building/implementing?
  └─ YES → engineers/
  └─ NO ↓

Is it a programming language specialist?
  └─ YES → language-experts/
  └─ NO ↓

Does it have deep domain expertise for specific tasks?
  └─ YES → specialists/
```

### Rules

1. **No duplicates** - Each agent should exist in exactly one location
2. **Single responsibility** - One agent, one role
3. **Reusable** - Agents should be workflow-agnostic; commands orchestrate agents

---

## Commands (`commands/`)

Commands are slash-invokable workflows. They are organized **by action** (what the user wants to DO).

### Categories

| Folder | Purpose | Examples |
|--------|---------|----------|
| `review/` | Analyze existing code | code-review, pr-enhance, multi-agent-review |
| `generate/` | Create new code/docs | api-mock, component-scaffold, doc-generate |
| `debug/` | Diagnose and fix issues | error-analysis, error-trace, smart-debug |
| `refactor/` | Improve existing code | refactor-clean, tech-debt, deps-audit |
| `tdd/` | Test-driven development | tdd-cycle, tdd-red, tdd-green, tdd-refactor |
| `feature/` | End-to-end feature work | feature-development, full-stack-feature |
| `git/` | Version control workflows | git-workflow |
| `explain/` | Understand code | code-explain |
| `optimize/` | Improve performance | prompt-optimize |
| `team/` | Collaboration tasks | issue, standup-notes |

### Naming Conventions

- Use **kebab-case** for file names: `code-review.md`, `error-trace.md`
- Name should be an **action verb or noun phrase**: `generate`, `review`, `debug`
- Keep names short and memorable (they become `/folder/command`)

### Command File Structure

```markdown
[Brief description of what this command does]

[Extended thinking: Detailed explanation of the workflow...]

## Configuration Options
- **--flag-name**: Description of what this flag does

## Phase 1: [Phase Name]
### Step 1A: [Step Name]
- Use Task tool with subagent_type="category/agent-name"
- Prompt: "..."
- Expected output: ...

## Success Criteria
[What defines successful completion]

Target: $ARGUMENTS
```

### Decision Tree: Where Does My Command Go?

```
Does it analyze/critique existing code?
  └─ YES → review/
  └─ NO ↓

Does it create new files/code/docs?
  └─ YES → generate/
  └─ NO ↓

Does it diagnose errors or unexpected behavior?
  └─ YES → debug/
  └─ NO ↓

Does it improve existing code without adding features?
  └─ YES → refactor/
  └─ NO ↓

Is it part of the TDD workflow?
  └─ YES → tdd/
  └─ NO ↓

Does it implement new functionality end-to-end?
  └─ YES → feature/
  └─ NO ↓

Is it about git/version control/PRs?
  └─ YES → git/
  └─ NO ↓

Does it explain or document code?
  └─ YES → explain/
  └─ NO ↓

Is it about optimization (performance, prompts, etc.)?
  └─ YES → optimize/
  └─ NO ↓

Is it about team collaboration?
  └─ YES → team/
```

### Rules

1. **Commands orchestrate agents** - Commands should reference agents, not duplicate agent logic
2. **Use `$ARGUMENTS`** - Commands should accept user input via `$ARGUMENTS`
3. **Phase-based structure** - Break complex workflows into numbered phases
4. **Reference agents correctly** - Use `subagent_type="category/agent-name"` format

---

## Skills (`skills/`)

Skills are knowledge domains with reference materials. They are organized **by topic**.

### Structure

Each skill is a self-contained folder:

```
skills/
└── {skill-name}/
    ├── SKILL.md              # Main skill definition (required)
    ├── references/           # Reference documentation
    │   ├── concept-1.md
    │   └── concept-2.md
    ├── assets/               # Templates, checklists, examples
    │   ├── template.py
    │   └── checklist.md
    └── scripts/              # Helper scripts (optional)
        └── helper.py
```

### Naming Conventions

- Use **kebab-case** for folder names: `api-design-principles`, `typescript-advanced-types`
- Main file must be named `SKILL.md`
- Name should describe the **knowledge domain**: `postgresql`, `error-handling-patterns`

### SKILL.md Structure

```markdown
# Skill Name

Brief description of what knowledge this skill provides.

## When to Use This Skill
[Triggers and use cases]

## Core Concepts
[Key knowledge areas]

## Best Practices
[Guidelines and patterns]

## Common Patterns
[Reusable solutions]

## Anti-Patterns
[What to avoid]

## References
[Links to reference files in references/]
```

### Decision Tree: Should This Be a Skill?

```
Is it reusable knowledge that applies across multiple tasks?
  └─ NO → Probably belongs in an agent or command
  └─ YES ↓

Does it have reference material, templates, or examples?
  └─ NO → Consider if it's substantial enough
  └─ YES ↓

Is it a coherent knowledge domain?
  └─ YES → Create a skill!
```

### Rules

1. **Self-contained** - Each skill folder should have everything needed
2. **Topic-focused** - One skill = one knowledge domain
3. **Reference-rich** - Include practical examples, templates, and references
4. **Flat skills are OK** - Simple skills can be a single `.md` file at the root

---

## Quick Reference

### Adding a New Agent

1. Determine category using the decision tree
2. Create `agents/{category}/{agent-name}.md`
3. Follow the agent file structure template
4. Ensure no duplicate agents exist

### Adding a New Command

1. Determine category using the decision tree
2. Create `commands/{category}/{command-name}.md`
3. Reference existing agents (don't duplicate agent logic)
4. Use `$ARGUMENTS` for user input

### Adding a New Skill

1. Create `skills/{skill-name}/SKILL.md`
2. Add `references/` folder for documentation
3. Add `assets/` folder for templates and examples
4. Keep it self-contained and topic-focused

---

## Migration Checklist

When reorganizing existing files:

- [ ] Identify duplicates and consolidate
- [ ] Move agents to role-based categories
- [ ] Move commands to action-based categories
- [ ] Update any cross-references between files
- [ ] Remove empty folders
- [ ] Verify all agent references in commands are correct

---

## Examples

### Good Organization

```
agents/reviewers/code-reviewer.md      # Role-based, single location
commands/review/code-review.md         # Action-based, references code-reviewer agent
skills/code-review-excellence/         # Knowledge domain with references
```

### Bad Organization

```
agents/code-review-workflow/code-reviewer.md    # Workflow-based (wrong)
agents/comprehensive-review/code-reviewer.md    # Duplicate (wrong)
commands/code-reviewer/review.md                # Role-based command folder (wrong)
```
