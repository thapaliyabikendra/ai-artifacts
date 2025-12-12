---
name: claude-artifact-creator
description: "Creates, improves, and validates Claude Code artifacts (skills, agents, commands, hooks). Use when creating domain expertise skills, specialized task agents, user-invoked commands, extending Claude Code capabilities, improving existing artifacts, reviewing artifact quality, analyzing code for automation opportunities, or consolidating duplicate artifacts."
layer: 4
tech_stack: [agnostic, markdown, yaml]
topics: [skills, agents, commands, hooks, claude-code, artifacts, meta]
depends_on: []
complements: []
keywords: [Skill, Agent, Command, Hook, SKILL.md, frontmatter, YAML, prompt-engineering]
---

# Claude Artifact Creator

Creates, improves, and maintains Claude Code extensions following official best practices.

## FIRST: Read Meta-Knowledge

**Before creating any artifact, READ `.claude/GUIDELINES.md`** for:
- Decision framework (Skill vs Agent vs Command vs Hook)
- Tool permissions strategy by role
- Hook events and configuration
- Agent/Skill/Command file formats
- Quality checklists and anti-patterns

This skill provides quick patterns; GUIDELINES.md provides authoritative rules.

## When to Use This Skill

- Creating a new skill for domain expertise or file processing
- Creating an agent for specialized tasks with context isolation
- Creating a command for user-invoked shortcuts
- Improving or refactoring existing artifacts
- Reviewing artifacts against quality standards
- Analyzing staged changes for automation opportunities
- Consolidating duplicate or overlapping artifacts

## Core Principle: Concise is Key

The context window is a shared resource. Before adding content, ask:
- "Does Claude really need this?" - Claude is already smart
- "Can this be in a reference file?" - Progressive disclosure
- "Does this justify its token cost?" - Every line has a cost

## Core Capabilities

1. **Create** - Generate artifacts from templates with proper structure
2. **Improve** - Enhance based on official best practices and patterns
3. **Review** - Audit against quality checklist and anti-patterns
4. **Consolidate** - Merge duplicate artifacts into focused ones

## Quick Start

**Create a skill:**
```bash
python scripts/init_skill.py pdf-processor --path .claude/skills --template tool
```

**Create an agent:**
```bash
python scripts/init_agent.py code-reviewer --path .claude/agents --template reviewer --category reviewers
```

**Create a command:**
```bash
python scripts/init_command.py run-tests --path .claude/commands --template workflow --category tdd
```

## Key Patterns

### 1. Decision Pattern
```
User triggers explicitly → COMMAND
Claude auto-detects → SKILL (no isolation) or AGENT (with isolation)
Deterministic on events → HOOK
```

### 2. Progressive Disclosure
```
Level 1: description (~100 tokens) → Trigger matching
Level 2: SKILL.md body (<5k tokens) → When activated
Level 3: references/ → On-demand deep dives
```

### 3. Artifact Limits
```
Skill SKILL.md: <500 lines
Agent prompt: <150 lines
References: One level deep (no nested)
```

### 4. Description Pattern
```yaml
# Good: Third-person with triggers
description: Processes PDF files for text extraction and form filling.
  Use when working with PDFs, extracting text, or filling forms.

# Bad: First-person or vague
description: I can help you with documents
```

## YAML Validation Rules

| Field | Requirements |
|-------|--------------|
| `name` | Max 64 chars, lowercase, hyphens only, no reserved words (anthropic, claude) |
| `description` | Max 1024 chars, third-person voice, 3+ trigger scenarios, no XML tags |
| `tools` | Comma-separated; omitting grants ALL tools (including MCP) |
| `model` | `haiku` (fast), `sonnet` (balanced), `opus` (powerful) |
| `permissionMode` | `default`, `acceptEdits`, `bypassPermissions` |

## Decision Flowchart

**Quick Reference:**
```
User triggers explicitly → COMMAND
Claude auto-detects → SKILL (no isolation) or AGENT (with isolation)
Deterministic on events → HOOK
```

**Full decision tree**: See [GUIDELINES.md § Choosing the Right Tool](..\..\GUIDELINES.md#choosing-the-right-tool)

## Creation Workflow

### Step 1: Identify Type

```
Type Decision Checklist:
- [ ] User invokes with /command? → Command
- [ ] Needs separate context window? → Agent
- [ ] Auto-triggered domain knowledge? → Skill
- [ ] Shell action on tool events? → Hook
```

### Step 2: Gather Requirements

**Skills**: Trigger scenarios (3+), resources needed, primary workflow
**Agents**: Team role, tools needed (least privilege), permission mode
**Commands**: Arguments, phases, expected output

### Step 3: Initialize

| Type | Command |
|------|---------|
| Skill | `python scripts/init_skill.py <name> --template <type>` |
| Agent | `python scripts/init_agent.py <name> --template <type> --category <cat>` |
| Command | `python scripts/init_command.py <name> --template <type> --category <cat>` |

**Templates:**
- Skills: `default`, `tool`, `workflow`, `domain`, `analysis`, `integration`, `generator`, `pattern`
- Agents: `architect`, `reviewer`, `developer`, `coordinator`, `specialist`
- Commands: `review`, `generate`, `debug`, `workflow`, `git`, `refactor`

### Step 4: Test

```
Testing Checklist:
- [ ] Customize all placeholders ([DOMAIN], [TARGET])
- [ ] Test with Haiku - enough guidance?
- [ ] Test with Sonnet - clear and efficient?
- [ ] Test with Opus - not over-explained?
- [ ] Verify triggers activate correctly
```

## Built-in Subagents

Claude Code includes built-in agents (cannot be modified):

| Agent | Purpose | Mode |
|-------|---------|------|
| **Plan** | Research before presenting plan | Read-only, plan mode |
| **Explore** | Fast codebase search | Read-only (`ls`, `find`, `cat`, `head`, `tail`) |

**Note**: Subagents cannot spawn other subagents.

## Tool Permissions & Hook Events

⚠️ **Warning**: Omitting `tools` grants ALL tools including MCP. Always whitelist explicitly.

**Full reference**: See [GUIDELINES.md § Agents](..\..\GUIDELINES.md#agents-agents) for tool permissions by role, and [GUIDELINES.md § Hooks](..\..\GUIDELINES.md#hooks) for hook events.

## Best Practices

1. **Concise over comprehensive** - Claude is smart; add only what it doesn't know
2. **Show, don't tell** - Examples beat descriptions
3. **Third-person descriptions** - Required for system prompt injection
4. **3+ trigger scenarios** - Specific scenarios in description ensure activation
5. **Least privilege tools** - Only grant necessary tools
6. **One level deep references** - No nested references (causes partial reads)
7. **Test all models** - What works for Opus may need more detail for Haiku
8. **Validate before shipping** - Run `scripts/validate.py --strict`

## Common Pitfalls

| Pitfall | Detection | Fix |
|---------|-----------|-----|
| Vague triggers | Description <100 chars | Add 3+ specific scenarios |
| Abstract only | No code blocks | Add before/after examples |
| Monolithic | >500 lines | Move to references/ |
| Kitchen sink | Lists 5+ domains | Create specialized artifacts |
| Embedded code in agent | Code blocks in agent | Extract to skill |
| First-person description | "I can help" | Use third-person |

See [references/anti-patterns.md](references/anti-patterns.md) for comprehensive list.

## Agent Refactoring

When agents grow >150 lines:

| Content | Extract To | Reference As |
|---------|------------|--------------|
| Code patterns | Skill | "Apply `skill-name` skill" |
| Output templates | Skill | "Follow `skill-name` format" |
| CLI commands | Command | "Use `/command-name`" |
| Project structure | docs/ | "Read docs/..." |

## Success Metrics

Track these for artifact quality:

| Metric | Target |
|--------|--------|
| Trigger accuracy | Activates on relevant requests |
| Output consistency | Same quality across similar inputs |
| Model compatibility | Works with Haiku, Sonnet, Opus |
| Line count | Skills <500, Agents <150 |
| Description length | 100-1024 chars with triggers |

## Quality Checklist

```
Artifact Quality Review:
- [ ] Description: third-person, 100-1024 chars, 3+ triggers
- [ ] Name: lowercase, hyphens, max 64 chars
- [ ] Entry point clear (user knows where to start)
- [ ] Concrete examples, not just descriptions
- [ ] No duplicate content across files
- [ ] References one level deep only
- [ ] Tested with Haiku, Sonnet, and Opus
- [ ] Under line limits (Skills: 500, Agents: 150)
- [ ] Validation/verification steps included
- [ ] Error recovery guidance present
```

## Integration Patterns

### Command → Agent → Skill

```
/add-feature (command)
  └─ Uses backend-architect (agent)
       └─ Applies api-design-principles (skill)
```

### Skill as Knowledge, Command as Action

```
Rule: "Knowing" = Skill, "Doing" = Command
      "Doing with Knowledge" = Command referencing Skills
```

## References

**Primary (READ FIRST):**
- [`.claude/GUIDELINES.md`](..\..\GUIDELINES.md) - **Authoritative meta-knowledge** for all artifact creation

**Skill-Specific:**
- [references/skills/skill-types.md](references/skills/skill-types.md) - Archetypes
- [references/agents/agent-categories.md](references/agents/agent-categories.md) - Role definitions
- [references/commands/command-patterns.md](references/commands/command-patterns.md) - Patterns
- [references/anti-patterns.md](references/anti-patterns.md) - What to avoid
- [references/agent-refactoring-guide.md](references/agent-refactoring-guide.md) - Extract from agents

**Project Context:**
- `CLAUDE.md` - Project-specific values and quick references
