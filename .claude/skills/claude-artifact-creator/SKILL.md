---
name: claude-artifact-creator
description: "Create and improve Claude Code artifacts (skills, agents, commands). Use when: (1) \"create a skill for...\", (2) \"create an agent that...\", (3) \"make a command for...\", (4) \"help me extend Claude Code\", (5) \"improve this agent/skill/command\", (6) \"review my artifacts\", (7) analyzing staged changes for artifact improvements, (8) \"consolidate these agents/skills\"."
---

# Claude Artifact Creator

Create, improve, and maintain Claude Code extensions (skills, agents, commands).

## Project Guidelines

**IMPORTANT**: Before creating or modifying artifacts, read:
- `.claude/GUIDELINES.md` - Organization rules, decision flowcharts, agent/skill/command patterns
- `CLAUDE.md` - Project-specific agent inventory and skill list

All created artifacts must follow the guidelines in these files.

## Capabilities

| Capability | Description |
|------------|-------------|
| **Create** | Generate new artifacts from templates |
| **Improve** | Enhance existing artifacts based on context or staged changes |
| **Review** | Audit artifacts against best practices |
| **Consolidate** | Merge duplicate or overlapping artifacts |

## Quick Decision

| If you need... | Create a... | Key Feature |
|----------------|-------------|-------------|
| Auto-triggered domain expertise | **Skill** | Progressive disclosure |
| Complex tasks with context isolation | **Agent** | Separate context window |
| User-invoked shortcuts | **Command** | Explicit `/cmd` trigger |

See [references/decision-guide.md](references/decision-guide.md) for detailed comparison.

## Decision Flowchart

```
What do you need?
│
├─ "User explicitly triggers action" → COMMAND
│   └─ Needs multiple files/scripts? → Consider SKILL instead
│
├─ "Claude should auto-detect when to use" → SKILL or AGENT
│   └─ Needs context isolation?
│       ├─ YES → AGENT (separate context window)
│       └─ NO → SKILL (progressive disclosure)
│
└─ "Complex multi-step task with specialized persona" → AGENT
```

## Creation Workflow

### Step 1: Identify Artifact Type

Ask these questions:

| Question | Yes → | No → |
|----------|-------|------|
| Should user invoke explicitly with `/command`? | Command | Continue |
| Needs separate context window (isolation)? | Agent | Continue |
| Auto-triggered domain knowledge? | Skill | Command |

### Step 2: Gather Requirements

**For all types:**
1. What specific tasks will this handle?
2. Can you show 2-3 example requests?
3. What outputs should it produce?

**Additional for Skills:**
- What resources are needed? (scripts, templates, references)
- What are the trigger scenarios?

**Additional for Agents:**
- What team role does this represent?
- What tools does it need?
- Should it auto-approve edits?

**Additional for Commands:**
- What arguments does it accept?
- What phases does it have?

### Step 3: Initialize

**Skill:**
```bash
python scripts/init_skill.py <name> --path .claude/skills --template <type>
```

Templates: `default`, `tool`, `workflow`, `domain`, `analysis`, `integration`, `generator`, `pattern`

**Agent:**
```bash
python scripts/init_agent.py <name> --path .claude/agents --template <type> [--category <cat>]
```

Templates (by function): `architect`, `reviewer`, `developer`, `coordinator`, `specialist`
Templates (by role): `manager`, `tech-lead`, `qa-engineer`, `devops`, `security`
Categories: `architects`, `reviewers`, `engineers`, `specialists`, `language-experts`

**Command:**
```bash
python scripts/init_command.py <name> --path .claude/commands --template <type> [--category <cat>]
```

Templates: `review`, `generate`, `debug`, `workflow`, `git`, `refactor`
Categories: `review`, `generate`, `debug`, `refactor`, `tdd`, `feature`, `git`, `explain`, `optimize`, `team`

### Step 4: Customize & Test

1. Edit the generated file to customize placeholders
2. Replace `[DOMAIN]`, `[TARGET]`, etc. with specific values
3. Test the artifact:
   - Skill: Request should auto-trigger based on description
   - Agent: "Use the [name] agent to [task]"
   - Command: `/command-name [arguments]`

## Improvement Workflow

### From Staged Changes

When reviewing staged changes (`git diff --staged`):

1. **Identify patterns** - Are there repeated manual tasks?
2. **Suggest automation:**
   - Repeated file operations → New skill
   - Recurring review tasks → New agent
   - Frequent commands → New command
3. **Propose improvements** to existing artifacts

### From Conversation Context

1. **Analyze patterns** - What requests keep recurring?
2. **Identify gaps** - What's missing from current artifacts?
3. **Suggest:**
   - New artifacts for unaddressed needs
   - Improvements to existing artifacts
   - Consolidation of overlapping artifacts

### Review Existing Artifacts

Run the validator:
```bash
python scripts/validate.py <path-to-skill> [--strict]
```

**Quality Checklist:**
- [ ] Description has 3+ explicit trigger scenarios
- [ ] Entry point is clear (user knows where to start)
- [ ] Concrete examples, not abstract descriptions
- [ ] No duplicate content between files
- [ ] Scripts tested and working
- [ ] Placeholders completed

## Type-Specific Guides

### Skills

**Structure:**
```
skill-name/
├── SKILL.md              # Required - entry point (<500 lines)
├── scripts/              # Executable code (Python/Bash)
├── references/           # Documentation loaded on-demand
└── assets/               # Output templates, boilerplate
```

**Key principles:**
- Progressive disclosure (3-level loading)
- Specific triggers in description
- Keep SKILL.md under 500 lines

See [references/skills/skill-types.md](references/skills/skill-types.md) for archetypes.

### Agents

**Structure:**
```yaml
---
name: agent-name
description: "Purpose. Use PROACTIVELY when..."
tools: Read, Write, Edit, Bash
model: sonnet
permissionMode: acceptEdits
---

# Agent instructions...
```

**Key principles:**
- Single responsibility
- Clear triggers ("Use PROACTIVELY when...")
- Least privilege (only necessary tools)
- Context isolation (separate context window)

See [references/agents/agent-categories.md](references/agents/agent-categories.md) for role definitions.

### Commands

**Structure:**
```yaml
---
description: Brief description
allowed-tools: Bash(git:*), Read
argument-hint: [file] [options]
---

# Command instructions using $ARGUMENTS...
```

**Key principles:**
- User-invoked (`/cmd`)
- Use `$ARGUMENTS` for user input
- Use `!` prefix for bash execution in content
- Single file (no subdirectories)

See [references/commands/command-patterns.md](references/commands/command-patterns.md) for patterns.

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Vague triggers | Artifact doesn't activate | List 3+ specific scenarios |
| Abstract-only | Inconsistent outputs | Add before/after examples |
| Monolithic | Wastes context | Split to references (<500 lines) |
| Kitchen sink | Unfocused | Create specialized artifacts |
| Missing validation | Silent failures | Add verification steps |
| Duplicate content | Maintenance burden | Consolidate into one artifact |
| **Embedded code in agents** | Agent too large | Extract to skills |
| **Embedded commands in agents** | Not reusable | Extract to commands |

See [references/anti-patterns.md](references/anti-patterns.md) for detailed guidance.

## Agent Refactoring

When agents grow too large (>150 lines), extract content:

| Content Type | Extract To | Reference As |
|--------------|------------|--------------|
| Code patterns | Skill | "Apply `skill-name` skill" |
| Output templates | Skill | "Follow `skill-name` format" |
| CLI commands | Command | "Use `/command-name`" |
| Project structure | docs/architecture/README.md | "Read docs/architecture/README.md" |

**Detection signs:**
- Code blocks (`\`\`\`csharp`, `\`\`\`typescript`) in agent = Extract to skill
- "Run this command: ..." in agent = Extract to command
- Repeated patterns across agents = Create shared skill

See `.claude/GUIDELINES.md` for detailed agent separation of concerns rules.

## Templates Reference

### Agent Templates by Role

| Role | Template | Best For |
|------|----------|----------|
| Manager | `manager` | Project planning, sprint coordination |
| Tech Lead | `tech-lead` | Architecture decisions, mentoring |
| Developer | `developer` | Implementation, coding |
| QA Engineer | `qa-engineer` | Testing, quality assurance |
| DevOps | `devops` | CI/CD, deployment |
| Security | `security` | Security audits, threat modeling |

### Agent Templates by Function

| Function | Template | Best For |
|----------|----------|----------|
| Architect | `architect` | System design, technical planning |
| Reviewer | `reviewer` | Code review, quality checks |
| Developer | `developer` | Implementation |
| Coordinator | `coordinator` | Multi-agent orchestration |
| Specialist | `specialist` | Deep domain expertise |

### Skill Templates

| Template | Best For | Example |
|----------|----------|---------|
| `default` | General purpose | - |
| `tool` | File processing, CLI tools | PDF processor |
| `workflow` | Multi-step processes | Code review |
| `domain` | Business knowledge, schemas | Database schema |
| `analysis` | Audits, assessments | Security audit |
| `integration` | API/service connections | API connector |
| `generator` | Code/file generation | CRUD service |
| `pattern` | Best practices, standards | Error handling |

### Command Templates

| Template | Best For | Example |
|----------|----------|---------|
| `review` | Code analysis | `/code-review` |
| `generate` | Scaffolding | `/scaffold-module` |
| `debug` | Error diagnosis | `/smart-debug` |
| `workflow` | Multi-phase processes | `/feature-dev` |
| `git` | Git automation | `/pr-workflow` |
| `refactor` | Code improvement | `/cleanup` |

## References

### Skill Documentation
- [references/skills/skill-types.md](references/skills/skill-types.md) - Skill archetypes
- [references/skills/template-patterns.md](references/skills/template-patterns.md) - Template patterns

### Agent Documentation
- [references/agents/agent-categories.md](references/agents/agent-categories.md) - Role categories
- [references/agents/context-isolation.md](references/agents/context-isolation.md) - Context management
- [references/agents/orchestration-patterns.md](references/agents/orchestration-patterns.md) - Multi-agent patterns

### Command Documentation
- [references/commands/command-patterns.md](references/commands/command-patterns.md) - Command patterns

### Cross-Cutting
- [references/decision-guide.md](references/decision-guide.md) - Skill vs Command vs Agent
- [references/anti-patterns.md](references/anti-patterns.md) - What to avoid
- [references/output-patterns.md](references/output-patterns.md) - Output formatting
- [references/workflows.md](references/workflows.md) - Workflow patterns
- [references/agent-refactoring-guide.md](references/agent-refactoring-guide.md) - Extract skills/commands from agents
