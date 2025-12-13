# Creating Artifacts

> Step-by-step guide for creating new agents, skills, commands, and hooks.

## Quick Reference

| Artifact | Create With | Location |
|----------|-------------|----------|
| Agent | Script or manual | `.claude/agents/{category}/` |
| Skill | Script or manual | `.claude/skills/{skill-name}/` |
| Command | Manual | `.claude/commands/{category}/` |
| Hook | Settings JSON | `.claude/settings.local.json` |

## Creating an Agent

### Option 1: Using Script

```bash
python .claude/skills/claude-artifact-creator/scripts/init_agent.py <name> \
  --path .claude/agents \
  --template <type>
```

### Option 2: Manual Creation

1. **Determine category** using decision tree:
   ```
   Is it primarily about designing/planning? → architects/
   Is it primarily about reviewing/critiquing? → reviewers/
   Is it primarily about building/implementing? → engineers/
   Does it have deep domain expertise? → specialists/
   ```

2. **Create file** at `agents/{category}/{agent-name}.md`

3. **Use template**:
   ```yaml
   ---
   name: agent-name
   description: |
     Purpose. Use PROACTIVELY when [trigger 1], [trigger 2], [trigger 3].
   tools: Read, Write, Edit, Bash, Glob, Grep
   model: sonnet
   skills: skill1, skill2
   ---

   You are a [role description].

   ## Project Context
   Before proceeding, read:
   1. `CLAUDE.md` - Project overview
   2. Relevant docs

   ## Responsibilities
   - [Responsibility 1]
   - [Responsibility 2]

   ## Constraints
   - [Constraint 1]
   - [Constraint 2]
   ```

4. **Validate**:
   - [ ] Under 150 lines
   - [ ] No embedded code templates
   - [ ] No hardcoded project names
   - [ ] Clear trigger description
   - [ ] Appropriate tools (least privilege)

---

## Creating a Skill

### Option 1: Using Script

```bash
python .claude/skills/claude-artifact-creator/scripts/init_skill.py <name> \
  --path .claude/skills \
  --template <type>
```

### Option 2: Manual Creation

1. **Create folder** at `skills/{skill-name}/`

2. **Create SKILL.md**:
   ```yaml
   ---
   name: skill-name
   description: |
     What it does. Use when: (1) scenario, (2) scenario, (3) scenario.
   tech_stack: [dotnet, csharp]
   ---

   # Skill Name

   ## Quick Start
   [Immediate, actionable content - 20-30 lines]

   ## Core Patterns
   [Essential patterns - 100-200 lines]

   ## Advanced Topics
   **Topic A**: See [topic-a.md](references/topic-a.md)
   ```

3. **Add references** (optional):
   ```
   skills/{skill-name}/
   ├── SKILL.md
   └── references/
       ├── advanced.md
       └── examples.md
   ```

4. **Validate**:
   - [ ] SKILL.md under 500 lines
   - [ ] Description includes 3+ trigger scenarios
   - [ ] Tech stack matches code examples
   - [ ] References one level deep
   - [ ] No time-sensitive information

5. **Update indexes**:
   - Add to `.claude/SKILL-INDEX.md`
   - Update `.claude/CONTEXT-GRAPH.md` if dependencies

---

## Creating a Command

### Manual Creation

1. **Determine category**:
   ```
   Generates new code/docs? → generate/
   Reviews/audits code? → review/
   Fixes issues? → debug/
   Improves code? → refactor/
   Test workflows? → tdd/ or qa/
   Team tasks? → team/
   ```

2. **Create file** at `commands/{category}/{command-name}.md`

3. **Use template**:
   ```yaml
   ---
   description: Brief description for autocomplete
   allowed-tools: Read, Write, Edit, Bash, Glob, Grep
   argument-hint: <required> [optional]
   model: sonnet
   ---

   # Command Name

   ## Context
   Read these files first:
   - `CLAUDE.md`

   ## Steps
   1. [Step using $ARGUMENTS]
   2. [Step 2]
   3. [Step 3]

   ## Output
   [Expected output format]
   ```

4. **Validate**:
   - [ ] Has `description` in frontmatter
   - [ ] Uses `$ARGUMENTS` for user input
   - [ ] No embedded domain knowledge (reference skills)
   - [ ] Atomic action (not multi-stage workflow)

5. **Update index**:
   - Add to `.claude/COMMAND-INDEX.md`

---

## Creating a Hook

### Configuration

Edit `.claude/settings.local.json` (project) or `~/.claude/settings.json` (global):

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

| Event | When | Common Use |
|-------|------|------------|
| `PreToolUse` | Before tool call | Block operations |
| `PostToolUse` | After tool call | Auto-format |
| `Stop` | Response complete | Cleanup |
| `SubagentStop` | Subagent completes | HITL control |

### Matcher Patterns

| Pattern | Matches |
|---------|---------|
| `Edit` | Exact match |
| `Edit\|Write` | Either |
| `*` | All tools |

### PreToolUse Exit Codes

| Exit Code | Effect |
|-----------|--------|
| `0` | Allow |
| `2` | Block |
| Other | Ask permission |

---

## Validation Checklists

### Agent Checklist
- [ ] Under 150 lines
- [ ] No embedded code templates
- [ ] No hardcoded project names
- [ ] "Use PROACTIVELY when..." in description
- [ ] Appropriate tools (least privilege)
- [ ] Skills declared in frontmatter
- [ ] Third-person description

### Skill Checklist
- [ ] SKILL.md under 500 lines
- [ ] Description includes 3+ trigger scenarios
- [ ] Tech stack declared and matches examples
- [ ] Uses `{Entity}` placeholders (not hardcoded names)
- [ ] References one level deep
- [ ] Added to SKILL-INDEX.md

### Command Checklist
- [ ] Has `description` frontmatter
- [ ] Uses `$ARGUMENTS`
- [ ] Atomic action
- [ ] No embedded domain knowledge
- [ ] Added to COMMAND-INDEX.md

## Related

- [Agent Examples](../examples/agent-examples.md)
- [Skill Examples](../examples/skill-examples.md)
- [Migration Guide](migration-guide.md)
