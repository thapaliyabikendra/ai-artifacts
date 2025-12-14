# Claude Code Organization Guidelines

> **Meta-Knowledge Source**: This document is the authoritative reference for creating and organizing Claude Code artifacts (agents, skills, commands, hooks). The `claude-artifact-creator` skill reads this file before creating any artifact.

This document defines the structure, conventions, and decision framework for organizing agents, commands, skills, and other Claude Code extensibility mechanisms.

> **Sources**: [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) | [Building Agents](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) | [Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## Table of Contents

1. [Core Principles](#core-principles)
2. [Directory Structure](#directory-structure)
3. [Choosing the Right Tool](#choosing-the-right-tool)
4. [Knowledge Architecture](#knowledge-architecture)
   - [Content Retrieval Protocol](#content-retrieval-protocol)
   - [Queryable Markdown Standard](#queryable-markdown-qmd-standard)
5. [Three-Layer Knowledge Architecture](#three-layer-knowledge-architecture)
6. [Agents](#agents)
7. [Skills](#skills)
8. [Commands](#commands)
9. [Hooks](#hooks)
10. [Output Styles](#output-styles)
11. [Quick Reference](#quick-reference)

---

## Core Principles

Five principles guide all Claude Code artifacts:

### 1. Single Responsibility
Each artifact does one thing well. Agents coordinate, skills provide knowledge, commands execute actions.

### 2. Progressive Disclosure
Load information in stages: discovery → instructions → resources. See [progressive-disclosure.md](guidelines/patterns/progressive-disclosure.md).

### 3. Portability First
All artifacts must be project-agnostic. Use `{ProjectName}`, `{Entity}` placeholders. See [portability-patterns.md](guidelines/patterns/portability-patterns.md).

### 4. Context Efficiency
Every token must justify its presence. Challenge: "Does Claude need this?" See [context-efficiency.md](guidelines/patterns/context-efficiency.md).

### 5. Least Privilege
Grant only necessary tools. Reviewers get read-only; implementers get write access. See [tool-permissions.md](guidelines/reference/tool-permissions.md).

---

## Directory Structure

```
.claude/
├── GUIDELINES.md           # This file (core reference)
├── guidelines/             # Modular deep-dives
│   ├── INDEX.md           # Navigation hub
│   ├── patterns/          # Design patterns
│   ├── standards/         # Rules & conventions
│   ├── examples/          # Good/bad examples
│   ├── workflows/         # How-to guides
│   └── reference/         # Lookup tables
├── agents/                 # AI agent definitions (BY ROLE)
│   ├── architects/        # System designers
│   ├── reviewers/         # Code reviewers
│   ├── engineers/         # Implementers
│   └── specialists/       # Domain experts
├── commands/               # Slash commands (BY ACTION)
│   ├── generate/          # Create new code
│   ├── review/            # Analyze code
│   ├── debug/             # Fix issues
│   └── ...
├── skills/                 # Knowledge domains (BY TOPIC)
│   └── {skill-name}/      # Self-contained topic
├── SKILL-INDEX.md         # Skill discovery
├── CONTEXT-GRAPH.md       # Skill dependencies
├── COMMAND-INDEX.md       # Command discovery
└── AGENT-QUICK-REF.md     # Agent selection
```

---

## Choosing the Right Tool

### Decision Matrix

| Mechanism | Invocation | Context | Best For |
|-----------|------------|---------|----------|
| **Skill** | Auto (model-invoked) | Progressive disclosure | Reusable domain expertise |
| **Agent** | Auto-delegated | Isolated window | Autonomous complex tasks |
| **Command** | Manual (`/cmd`) | Expands into main | Atomic, frequent actions |
| **Hook** | Event-triggered | N/A (shell) | Guardrails, automation |
| **Output Style** | User-configured | Modifies system prompt | Persona changes |
| **CLAUDE.md** | Always loaded | Persistent | Project-wide context |

### Decision Flowchart

```
START: What do you need?
│
├─ Deterministic action on every tool call? → HOOK
├─ Change Claude's overall behavior? → OUTPUT STYLE
├─ Project-wide context always needed? → CLAUDE.md
├─ User explicitly triggers action? → COMMAND
├─ Claude should auto-detect when to use?
│   └─ Needs context isolation? → AGENT (else SKILL)
└─ Complex multi-step with specialized persona? → AGENT
```

**Full decision matrices**: See [decision-matrices.md](guidelines/reference/decision-matrices.md)

### Common Scenarios

| Scenario | Use | Why |
|----------|-----|-----|
| Auto-format after edit | Hook | Deterministic |
| Code review expertise | Skill | Auto-triggered knowledge |
| Run tests and fix failures | Agent | Multi-step, isolated |
| Quick commit shortcut | Command | User-invoked atomic |
| Teaching mode | Output Style | Behavior change |
| Project standards | CLAUDE.md | Always needed |

---

## Knowledge Architecture

A tiered system for knowledge discovery and sharing between skills.

### Tiered Discovery

| Tier | Task Complexity | Files Read | Use When |
|------|-----------------|------------|----------|
| **SKIP** | Simple (typo, comment) | 0 | Obvious changes |
| **QUICK** | Single-skill | 0 | One pattern needed |
| **STANDARD** | Multi-skill | 2 | Multiple skills |
| **DEEP** | Full implementation | 4+ | CRUD, new feature |

**Key**: Don't over-discover. A typo fix doesn't need knowledge discovery.

### Core Components

| File | Purpose |
|------|---------|
| `SKILL-INDEX.md` | Find skills by task/keyword/error |
| `CONTEXT-GRAPH.md` | Skill dependencies and load order |
| `knowledge/` | Shared patterns across skills |
| `flows/` | Multi-skill workflows |

### Skill Layers

| Layer | Purpose | Examples |
|-------|---------|----------|
| **1 - Foundation** | Language basics | csharp-advanced, dotnet-async |
| **2 - Framework** | ABP, EF Core | abp-framework-patterns |
| **3 - Features** | Testing, security | xunit-testing, security-patterns |
| **4 - Workflows** | Orchestration | feature-development-workflow |

**Rule**: Load Layer 1-2 dependencies before Layer 3-4 skills.

### Content Retrieval Protocol

Token-efficient retrieval rules. **Never full-read when partial suffices.**

| Depth | Need | Method | Lines |
|-------|------|--------|-------|
| L0 | Exists? | `Grep(output: files_with_matches)` | ~1 |
| L1 | Count? | `Grep(output: count)` | ~1 |
| L2 | Lookup | `Grep(pattern, -C:2)` | ~5 |
| L3 | Overview | `Read(limit: 40)` | ~40 |
| L4 | Section | Grep heading → Read(offset, limit) | ~50 |
| L5 | Full | `Read()` - justify first | All |

**Section Extraction** (markdown-native):
```
1. Grep("^## Section Name$", file) → line 15
2. Grep("^---|^## ", file, offset: 16) → end at line 30
3. Read(file, offset: 15, limit: 15)
```

**Full skill**: [content-retrieval](skills/content-retrieval/SKILL.md)

### Queryable Markdown (QMD) Standard

**Markdown-native** structure using headings and horizontal rules:

```markdown
---
name: identifier
description: "One-line (< 100 chars)"
layer: 1-4
keywords: [grep, targets]
---

# Title

## Summary

2-3 sentences. Quick understanding.

---

## Quick Reference

| Pattern | Usage |
|---------|-------|

---

## Patterns

Detailed content...

---

## Related

- [link](path)
```

**Section Detection**: `## Heading` starts section, `---` or next `## ` ends it.

**Reserved Headings**: `## Summary`, `## Quick Reference`, `## Scope`, `## Patterns`, `## Related`

**Frontmatter**: Max 20 lines. Required: `name`, `description`, `layer`, `keywords`.

---

## Three-Layer Knowledge Architecture

Separates **concepts** (framework-independent principles) from **implementations** (language-specific patterns).

### The Three Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LAYER 1: CONCEPTS                                 │
│                 (Framework-Independent)                              │
│                                                                     │
│  "WHAT is the principle?" "WHY does it matter?"                     │
│  NO CODE - just principles, rationale, detection criteria           │
│                                                                     │
│  concepts/solid/srp.md, concepts/clean-code/naming.md               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ "How is this done in X?"
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  LAYER 2: IMPLEMENTATIONS                            │
│                 (Language/Framework-Specific)                        │
│                                                                     │
│  CODE EXAMPLES showing how to apply concepts in specific context    │
│  Links back to concepts it implements                               │
│                                                                     │
│  implementations/dotnet/solid.md, implementations/react/hooks.md    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ Orchestrates both
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     LAYER 3: SKILLS                                  │
│                  (Context-Aware Orchestration)                       │
│                                                                     │
│  References concepts + implementations, adds context                 │
│  "When to use", "How it fits with this project"                     │
│                                                                     │
│  skills/clean-code-dotnet/SKILL.md                                  │
└─────────────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
knowledge/
├── concepts/                          # LAYER 1: Pure principles
│   ├── INDEX.md                       # Concept registry + implementation links
│   ├── clean-code/                    # Grouped by topic
│   │   ├── principles.md
│   │   ├── naming.md
│   │   └── functions.md
│   ├── solid/
│   │   ├── overview.md
│   │   ├── srp.md
│   │   └── ...
│   ├── clean-architecture/
│   ├── code-smells/
│   ├── testing/
│   └── refactoring/
│
├── implementations/                   # LAYER 2: Language-specific
│   ├── INDEX.md                       # Implementation registry
│   ├── dotnet/
│   │   ├── clean-code.md
│   │   ├── solid.md
│   │   └── xunit.md
│   └── react/
│       ├── clean-code.md
│       └── jest.md
│
├── conventions/                       # Project conventions (existing)
├── patterns/                          # ABP patterns (existing)
└── examples/                          # Complete examples (existing)
```

### Layer Rules

#### CONCEPTS (`knowledge/concepts/`)

**Must contain:**
- Principle definition (framework-independent)
- Why it matters (rationale)
- How to detect violations
- Related concepts links
- Implementation links (in front matter)

**Must NOT contain:**
- Code examples (no code!)
- Framework-specific details
- Language-specific syntax

**Format:**
```yaml
---
name: Single Responsibility Principle
category: solid
implementations:
  dotnet: ../implementations/dotnet/solid.md#srp
  react: ../implementations/react/solid.md#srp
used_by_skills: [clean-code-dotnet, code-review-excellence]
---

# Single Responsibility Principle

> "A class should have one, and only one, reason to change."

## The Principle
[Framework-independent explanation]

## Why It Matters
[Rationale]

## How to Detect Violations
- [Detection criteria - no code]

## See Also
- **Implementations**: [.NET](#) | [React](#)
```

#### IMPLEMENTATIONS (`knowledge/implementations/{lang}/`)

**Must contain:**
- Link to concept(s) it implements
- Language-specific code examples (❌ Bad / ✅ Good)
- Framework-specific notes

**Must NOT contain:**
- Principle definitions (link to concepts instead)
- "Why" explanations (that's concept layer)

**Format:**
```yaml
---
implements_concepts:
  - concepts/solid/srp
  - concepts/solid/ocp
language: csharp
framework: [dotnet, abp]
---

# SOLID in C#

## SRP - Single Responsibility {#srp}

> **Concept**: [Single Responsibility Principle](../../concepts/solid/srp.md)

### ❌ Violation
```csharp
// Code showing anti-pattern
```

### ✅ Correct
```csharp
// Code showing correct implementation
```
```

#### SKILLS (`skills/{name}/`)

**Must contain:**
- References to concepts (in front matter)
- References to implementations (in front matter)
- Orchestration context ("When to use", "How it fits")

**Should NOT contain:**
- Embedded principle definitions (link to concepts)
- Duplicated code examples (link to implementations)

**Format:**
```yaml
---
name: clean-code-dotnet
applies_concepts:
  - knowledge/concepts/clean-code/principles
  - knowledge/concepts/solid/overview
uses_implementations:
  - knowledge/implementations/dotnet/clean-code
  - knowledge/implementations/dotnet/solid
---

# Clean Code .NET

Apply [Clean Code Principles](../../knowledge/concepts/clean-code/principles.md)
in C#/.NET projects.

## When to Use
[Contextual guidance]

## Quick Reference
See [C# Implementation](../../knowledge/implementations/dotnet/clean-code.md)
```

### Concept Registry (INDEX.md)

Both layers have INDEX.md files for discovery:

**`knowledge/concepts/INDEX.md`:**
```markdown
| Concept | Definition | .NET | React | Python |
|---------|------------|------|-------|--------|
| SOLID | [solid/overview.md] | [✓](../implementations/dotnet/solid.md) | - | - |
| Clean Code | [clean-code/principles.md] | [✓](../implementations/dotnet/clean-code.md) | [✓](../implementations/react/clean-code.md) | - |
```

### Decision Flow: What to Create

```
User requests new knowledge artifact
              │
              ▼
┌─────────────────────────────────────┐
│ Does it apply to ANY language?      │
│ (No code, just principle)           │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │ YES           │ NO
       ▼               ▼
   CONCEPT      ┌─────────────────────┐
   (concepts/)  │ Is it specific to   │
                │ a language/framework?│
                └──────────┬──────────┘
                           │
                   ┌───────┴───────┐
                   │ YES           │ NO
                   ▼               ▼
             IMPLEMENTATION    SKILL
             (implementations/) (skills/)
```

### Migration Path

Existing skills with embedded concepts should be migrated:

1. **Extract concepts** → `knowledge/concepts/{topic}/`
2. **Extract code examples** → `knowledge/implementations/{lang}/`
3. **Update skill** → Reference both via front matter
4. **Remove duplicated content** from skill

**Migrate on touch**: When updating a skill, migrate its embedded content.

---

## Artifact Knowledge Rules

Governance rules for how each artifact type relates to the knowledge base.

### Rules by Artifact Type

| Artifact | Must | Must Not |
|----------|------|----------|
| **Skill** | Reference concepts/implementations via front matter | Duplicate code patterns >10 lines inline |
| **Agent** | Declare knowledge profile (`understands`/`applies`) | List skills without concept mapping |
| **Command** | Delegate domain logic to skills | Contain inline patterns or business rules |
| **Hook** | Stay procedural (shell scripts) | Embed framework-specific knowledge |

### Agent Knowledge Profiles

Agents declare what concepts they understand and what implementations they can apply:

```yaml
---
name: agent-name
description: "..."
tools: Read, Write, Edit
model: sonnet
skills: skill1, skill2
understands:                    # Concepts (framework-independent)
  - solid/srp
  - solid/dip
  - clean-code/naming
  - clean-architecture/layers
applies:                        # Implementations (language-specific code)
  - dotnet/solid
  - dotnet/clean-code
---
```

### Field Definitions

| Field | Purpose | Format | Validation |
|-------|---------|--------|------------|
| `understands` | Concepts the agent knows | Paths relative to `knowledge/concepts/` | Must exist in concepts INDEX |
| `applies` | Implementations the agent uses | Paths relative to `knowledge/implementations/` | Must exist in implementations INDEX |

### Role Requirements

| Role | `understands` (min) | `applies` (min) | Rationale |
|------|---------------------|-----------------|-----------|
| `reviewers/` | 3 | 1 | Need to detect violations |
| `engineers/` | 2 | 2 | Need to write correct code |
| `architects/` | 3 | 0 | Design focus, less implementation |
| `specialists/` | 1 | 0 | Domain-specific, flexible |

### Wildcard Support

Use `*` to include all concepts in a category:

```yaml
understands:
  - solid/*              # All SOLID concepts
  - clean-code/*         # All clean code concepts
  - testing/tdd-principles  # Single specific concept
```

### Validation

The `claude-artifact-creator` skill validates:
1. All concept paths exist in `knowledge/concepts/INDEX.md`
2. All implementation paths exist in `knowledge/implementations/INDEX.md`
3. Agents meet minimum requirements for their role category
4. Skills reference knowledge instead of duplicating it

**Cross-reference**: See [ARTIFACT-KNOWLEDGE-MATRIX.md](ARTIFACT-KNOWLEDGE-MATRIX.md) for full coverage.

---

## Agents

Agents are AI personas with specialized capabilities. Organized **by role** (what they ARE).

### Categories

| Folder | Purpose | Examples |
|--------|---------|----------|
| `architects/` | Design, plan | backend-architect, business-analyst |
| `reviewers/` | Analyze, critique | abp-code-reviewer, security-engineer |
| `engineers/` | Build, implement | abp-developer, react-developer |
| `specialists/` | Domain expertise | debugger, database-migrator |

### File Format

```yaml
---
name: agent-name                    # kebab-case, lowercase
description: "Purpose. Use PROACTIVELY when..."
tools: Read, Write, Edit            # Only necessary tools
model: sonnet                       # haiku|sonnet|opus
skills: skill1, skill2              # Auto-load skills
---

You are a [role description].

## Project Context
[What to read before starting]

## Responsibilities
[Core duties]

## Constraints
[Rules - keep concise]
```

### Tool Permissions

| Agent Type | Tools | Rationale |
|------------|-------|-----------|
| Read-only (reviewers) | `Read, Grep, Glob` | Cannot modify |
| Research | + `WebFetch, WebSearch` | Info gathering |
| Code writers | + `Write, Edit, Bash` | Implementation |

**Full reference**: See [tool-permissions.md](guidelines/reference/tool-permissions.md)

### Agent Rules

1. **Single responsibility** - One agent, one clear role
2. **Under 150 lines** - Extract to skills/commands if larger
3. **Least privilege** - Only necessary tools
4. **Clear triggers** - "Use PROACTIVELY when..." in description
5. **Third-person descriptions** - Injected into system prompts
6. **No embedded code** - Reference skills for patterns

**Separation of concerns**: See [agent-separation.md](guidelines/patterns/agent-separation.md)
**Examples**: See [agent-examples.md](guidelines/examples/agent-examples.md)

---

## Skills

Skills are knowledge domains with resources. Organized **by topic**.

### Core Principle: Concise is Key

Challenge each piece of information: "Does Claude need this?" Default: Claude is already smart.

### Structure

```
skills/
└── {skill-name}/
    ├── SKILL.md              # Required (<500 lines)
    ├── references/           # On-demand docs
    ├── assets/               # Templates
    └── scripts/              # Helpers
```

### SKILL.md Format

```yaml
---
name: skill-name                    # max 64 chars, kebab-case
description: |
  What it does. Use when: (1) scenario, (2) scenario, (3) scenario.
tech_stack: [dotnet, csharp, abp]   # Languages/frameworks
---

# Skill Name

## Quick Start
[Immediate, actionable - 20-30 lines]

## Core Patterns
[Essential patterns - 100-200 lines]

## Advanced Topics
**Topic A**: See [topic-a.md](references/topic-a.md)
```

### Progressive Disclosure

| Level | What Loads | Token Cost | When |
|-------|------------|------------|------|
| **Discovery** | name + description | ~100 | Startup |
| **Instructions** | Full SKILL.md | <5k | Triggered |
| **Resources** | References | As needed | On-demand |

**Full pattern**: See [progressive-disclosure.md](guidelines/patterns/progressive-disclosure.md)

### Skill Rules

1. **SKILL.md under 500 lines** - Extract to references/
2. **3+ trigger scenarios** - In description
3. **Third-person descriptions** - For system prompts
4. **References one level deep** - Direct links from SKILL.md
5. **Test with all models** - Haiku may need more detail

**Optimization guide**: See [skill-optimization.md](guidelines/patterns/skill-optimization.md)
**Examples**: See [skill-examples.md](guidelines/examples/skill-examples.md)

---

## Commands

Commands are slash-invokable workflows. Organized **by action** (what user wants to DO).

### Categories

| Folder | Purpose | Examples |
|--------|---------|----------|
| `generate/` | Create new code | entity, migration |
| `review/` | Analyze code | permissions |
| `debug/` | Fix issues | smart-debug |
| `refactor/` | Improve code | tech-debt |
| `tdd/` | Test workflows | tdd-cycle |
| `feature/` | End-to-end | add-feature |
| `team/` | Collaboration | issue, standup |

### File Format

```yaml
---
description: Brief description      # Required
allowed-tools: Bash(git:*), Read    # Optional
argument-hint: <required> [opt]     # Optional
model: sonnet                       # Optional
---

## Context
[What to read first]

## Steps
1. [Step using $ARGUMENTS]
2. [Step 2]

## Output
[Expected format]
```

### $ARGUMENTS

Captures user input after command name:

```markdown
Please analyze: $ARGUMENTS
```

**Usage**: `/fix-issue 123` → `$ARGUMENTS` = `123`

### Command Rules

1. **Has `description`** - For autocomplete
2. **Uses `$ARGUMENTS`** - For user input
3. **Atomic action** - Not multi-stage workflows
4. **No domain knowledge** - Reference skills instead

---

## Hooks

Hooks are deterministic shell commands at lifecycle events.

### Events

| Event | When | Use Case |
|-------|------|----------|
| `PreToolUse` | Before tool | Block operations |
| `PostToolUse` | After tool | Auto-format |
| `Stop` | Response done | Cleanup |
| `SubagentStop` | Subagent done | HITL control |

### Configuration

Location: `.claude/settings.local.json` or `~/.claude/settings.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "npx prettier --write \"$(jq -r '.tool_input.file_path')\""
        }]
      }
    ]
  }
}
```

### Matcher Syntax

| Pattern | Matches |
|---------|---------|
| `Edit` | Exact |
| `Edit\|Write` | Either |
| `*` | All tools |

### PreToolUse Exit Codes

| Code | Effect |
|------|--------|
| `0` | Allow |
| `2` | Block |
| Other | Ask permission |

---

## Output Styles

Output styles modify Claude's system prompt behavior.

### Built-in Styles

| Style | Purpose |
|-------|---------|
| Default | Software engineering efficiency |
| Explanatory | Educational insights |
| Learning | Collaborative mode |

### Custom Style Format

Location: `.claude/output-styles/` or `~/.claude/output-styles/`

```yaml
---
name: My Custom Style
description: Description for UI
keep-coding-instructions: false
---

[Custom instructions]
```

---

## Quick Reference

### Creating Artifacts

| Artifact | Command |
|----------|---------|
| Agent | `python .claude/skills/claude-artifact-creator/scripts/init_agent.py <name>` |
| Skill | `python .claude/skills/claude-artifact-creator/scripts/init_skill.py <name>` |
| Command | Manual creation in `commands/{category}/` |

Or ask: "Create an agent for [purpose]" / "Create a skill for [domain]"

**Full guide**: See [creating-artifacts.md](guidelines/workflows/creating-artifacts.md)

### Size Limits

| Artifact | Max Lines |
|----------|-----------|
| Agent | 150 |
| SKILL.md | 500 |
| Command | 200 |
| Reference doc | 400 |
| GUIDELINES.md | 1,000 |

### Quality Checklists

**Agent**:
- [ ] Under 150 lines
- [ ] No embedded code
- [ ] Tools explicitly declared
- [ ] "Use PROACTIVELY when..."

**Skill**:
- [ ] SKILL.md under 500 lines
- [ ] 3+ trigger scenarios
- [ ] Tech stack declared
- [ ] References one level deep

**Command**:
- [ ] Has description
- [ ] Uses $ARGUMENTS
- [ ] Atomic action

### Key Resources

| Need | Location |
|------|----------|
| Find a skill | [SKILL-INDEX.md](SKILL-INDEX.md) |
| Skill dependencies | [CONTEXT-GRAPH.md](CONTEXT-GRAPH.md) |
| Find a command | [COMMAND-INDEX.md](COMMAND-INDEX.md) |
| Choose an agent | [AGENT-QUICK-REF.md](AGENT-QUICK-REF.md) |
| Deep-dive guides | [guidelines/INDEX.md](guidelines/INDEX.md) |

### Antipatterns to Avoid

| Don't | Do Instead |
|-------|------------|
| Embed code in agents | Reference skills |
| Hardcode project names | Use `{ProjectName}` |
| Grant all tools | Least privilege |
| Explain what Claude knows | Jump to actionable content |
| Put everything in SKILL.md | Use progressive disclosure |

**Full antipatterns**: See [antipatterns.md](guidelines/examples/antipatterns.md)

---

## Modular Guidelines

This document is the entry point. Deep-dives are in `guidelines/`:

| Category | Documents |
|----------|-----------|
| **Patterns** | progressive-disclosure, agent-separation, tool-usage, portability, context-efficiency, skill-optimization |
| **Standards** | naming-conventions, file-formats |
| **Examples** | agent-examples, skill-examples, antipatterns |
| **Workflows** | agentic-coding-practices, creating-artifacts, migration-guide |
| **Reference** | decision-matrices, tool-permissions, model-selection |

**Navigation hub**: See [guidelines/INDEX.md](guidelines/INDEX.md)
