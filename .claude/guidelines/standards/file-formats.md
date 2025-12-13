# File Formats

> Standard file format requirements for all Claude Code artifacts.

## Agent File Format

```yaml
---
name: agent-name                    # Required: kebab-case
description: |                      # Required: max 1024 chars
  Purpose. Use PROACTIVELY when [trigger].
tools: Read, Write, Edit            # Optional: defaults to ALL
model: sonnet                       # Optional: haiku|sonnet|opus
permissionMode: default             # Optional: default|acceptEdits|bypassPermissions
skills: skill1, skill2              # Optional: auto-load skills
---

You are a [role description].

## Project Context
[What to read before starting]

## Responsibilities
[Core duties]

## Constraints
[Rules and limitations]
```

### Required Fields

| Field | Type | Constraints |
|-------|------|-------------|
| `name` | string | kebab-case, lowercase, max 64 chars |
| `description` | string | max 1024 chars, no XML tags |

### Optional Fields

| Field | Type | Default | Options |
|-------|------|---------|---------|
| `tools` | string | All tools | Comma-separated tool names |
| `model` | string | Inherited | `haiku`, `sonnet`, `opus` |
| `permissionMode` | string | `default` | `default`, `acceptEdits`, `bypassPermissions` |
| `skills` | string | None | Comma-separated skill names |

### Body Structure

```markdown
[Role introduction - 1-2 sentences]

## Project Context
[Files to read before starting]

## Responsibilities
[Bulleted list of duties]

## Constraints
[Bulleted list of rules]
```

**Max length**: 150 lines total

---

## Skill File Format

### SKILL.md

```yaml
---
name: skill-name                    # Required: max 64 chars, kebab-case
description: |                      # Required: max 1024 chars
  What it does. Use when: (1) scenario, (2) scenario, (3) scenario.
tech_stack: [dotnet, csharp]        # Required: languages/frameworks
allowed-tools: Read, Grep           # Optional: restrict tools
---

# Skill Name

## Quick Start
[Immediate actionable content - 20-30 lines]

## Core Patterns
[Essential patterns - 100-200 lines]

## Advanced Topics
**Topic A**: See [topic-a.md](references/topic-a.md)
```

### Required Fields

| Field | Type | Constraints |
|-------|------|-------------|
| `name` | string | max 64 chars, lowercase, hyphens only |
| `description` | string | max 1024 chars, no XML tags, include triggers |
| `tech_stack` | array | Valid tech identifiers |

### Tech Stack Values

| Category | Values |
|----------|--------|
| Backend | `dotnet`, `csharp`, `abp`, `efcore`, `grpc` |
| Frontend | `typescript`, `react`, `javascript` |
| Testing | `xunit`, `playwright`, `jest`, `vitest` |
| Infrastructure | `docker`, `postgresql`, `redis`, `git`, `bash` |
| Design | `agnostic`, `markdown`, `mermaid`, `yaml` |

### Body Structure

```markdown
# Skill Name

## Quick Start
[Immediate value - code example]

## Core Patterns
[Essential patterns with examples]

## Advanced Topics
[Links to references/ folder]
```

**Max length**: 500 lines for SKILL.md

### Folder Structure

```
skills/{skill-name}/
├── SKILL.md              # Required
├── references/           # Optional
│   ├── advanced.md
│   └── examples.md
├── assets/               # Optional
└── scripts/              # Optional
```

---

## Command File Format

```yaml
---
description: Brief description      # Required for SlashCommand
allowed-tools: Bash(git:*)          # Optional: restrict tools
argument-hint: <required> [opt]     # Optional: shown in autocomplete
model: sonnet                       # Optional: override model
---

# Command Name

## Context
[Files to read, setup needed]

## Steps
1. [Step using $ARGUMENTS]
2. [Step 2]
3. [Step 3]

## Output
[Expected output format]
```

### Required Fields

| Field | Type | Purpose |
|-------|------|---------|
| `description` | string | Shows in autocomplete |

### Optional Fields

| Field | Type | Purpose |
|-------|------|---------|
| `allowed-tools` | string | Restrict available tools |
| `argument-hint` | string | Usage hint in autocomplete |
| `model` | string | Override default model |

### Special Variables

| Variable | Expands To |
|----------|------------|
| `$ARGUMENTS` | User input after command name |
| `!`command`` | Bash execution inline |

### Body Structure

```markdown
## Context
[What to read/check first]

## Steps
[Numbered steps using $ARGUMENTS]

## Output
[Expected result format]
```

---

## Output Style Format

```yaml
---
name: My Custom Style               # Required
description: Description for UI     # Required
keep-coding-instructions: false     # Optional: keep default coding prompt
---

# Custom Instructions

[System prompt modifications]
```

---

## Hook Configuration

Location: `.claude/settings.local.json` or `~/.claude/settings.json`

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

### Hook Events

| Event | When |
|-------|------|
| `PreToolUse` | Before tool call |
| `PostToolUse` | After tool call |
| `PermissionRequest` | Permission dialog shown |
| `Notification` | On notification |
| `Stop` | Response complete |
| `SubagentStop` | Subagent completes |
| `UserPromptSubmit` | Before processing |
| `SessionStart` | Session begins |
| `SessionEnd` | Session ends |
| `PreCompact` | Before compaction |

### Matcher Syntax

| Pattern | Matches |
|---------|---------|
| `Edit` | Exact match |
| `Edit\|Write` | Either |
| `*` | All tools |

---

## Validation Rules

### All Artifacts

- [ ] Frontmatter is valid YAML
- [ ] Required fields present
- [ ] Name is kebab-case, lowercase
- [ ] Description under 1024 characters
- [ ] No XML tags in description

### Agents

- [ ] Total under 150 lines
- [ ] Has "Use PROACTIVELY when" in description
- [ ] Tools explicitly declared
- [ ] Third-person description

### Skills

- [ ] SKILL.md under 500 lines
- [ ] tech_stack declared
- [ ] 3+ trigger scenarios in description
- [ ] References one level deep

### Commands

- [ ] Has description frontmatter
- [ ] Uses $ARGUMENTS for input
- [ ] Atomic action (not workflow)

## Related

- [Naming Conventions](naming-conventions.md)
- [Creating Artifacts](../workflows/creating-artifacts.md)
- [Antipatterns](../examples/antipatterns.md)
