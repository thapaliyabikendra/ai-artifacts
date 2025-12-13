# Decision Matrices

> Consolidated decision flowcharts and matrices for choosing artifacts.

## Master Decision Flowchart

```
START: What do you need?
│
├─ "Deterministic action on every tool call" → HOOK
│   └─ Example: Auto-format after every Edit/Write
│
├─ "Change Claude's overall behavior/persona" → OUTPUT STYLE
│   └─ Example: Teaching mode, verbose explanations
│
├─ "Project-wide context always needed" → CLAUDE.md
│   └─ Example: Coding standards, build commands
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

## Mechanism Comparison Matrix

| Mechanism | Invocation | Context | Best For |
|-----------|------------|---------|----------|
| **Skill** | Auto (model-invoked) | Progressive disclosure | Reusable domain expertise |
| **Agent** | Auto-delegated or explicit | Isolated window | Autonomous complex tasks |
| **Command** | Manual (`/cmd`) | Expands into main | Atomic, frequent actions |
| **Hook** | Event-triggered | N/A (shell execution) | Guardrails, automation |
| **Output Style** | User-configured | Modifies system prompt | Persona changes |
| **CLAUDE.md** | Always loaded | Persistent background | Project-wide context |

## Common Scenario Mapping

| Scenario | Recommended | Why |
|----------|-------------|-----|
| Auto-format files after edit | **Hook** | Deterministic, every time |
| Code review expertise | **Skill** | Auto-triggered domain knowledge |
| Run tests and fix failures | **Agent** | Complex multi-step, context isolation |
| Quick commit shortcut | **Command** | User-invoked atomic action |
| Teaching mode with insights | **Output Style** | Behavior change |
| Project coding standards | **CLAUDE.md** | Always-needed context |

---

## Agent Category Decision Tree

```
Is it primarily about designing/planning?
├─ YES → agents/architects/
│   └─ Examples: backend-architect, business-analyst
│
Is it primarily about reviewing/critiquing?
├─ YES → agents/reviewers/
│   └─ Examples: abp-code-reviewer, security-engineer
│
Is it primarily about building/implementing?
├─ YES → agents/engineers/
│   └─ Examples: abp-developer, react-developer
│
Does it have deep domain expertise?
└─ YES → agents/specialists/
    └─ Examples: debugger, database-migrator
```

## Command Category Decision Tree

```
What does the command DO?

Generates new code/docs?
├─ YES → commands/generate/
│   └─ entity, migration, doc-generate

Reviews/audits existing code?
├─ YES → commands/review/
│   └─ permissions, code-review

Diagnoses and fixes issues?
├─ YES → commands/debug/
│   └─ smart-debug

Improves existing code?
├─ YES → commands/refactor/
│   └─ tech-debt, refactor-clean

Test-driven development?
├─ YES → commands/tdd/
│   └─ tdd-cycle

Feature development workflow?
├─ YES → commands/feature/
│   └─ add-feature

Team collaboration?
└─ YES → commands/team/
    └─ issue, standup-notes
```

---

## Skill vs Command vs Agent

| Aspect | Skill | Command | Agent |
|--------|-------|---------|-------|
| **Invocation** | Automatic | Manual (`/cmd`) | Delegated |
| **Complexity** | Directory with resources | Single file | Single file |
| **Use case** | Domain expertise | Frequent shortcuts | Complex workflows |
| **Context** | Progressive disclosure | Full expansion | Isolated window |
| **Persistence** | Across conversations | Single use | Per-task |

### When to Use Each

```
Need reusable patterns/knowledge? → SKILL
Need user-triggered shortcut? → COMMAND
Need autonomous multi-step task? → AGENT
Need deterministic automation? → HOOK
```

---

## Knowledge Discovery Tier Selection

```
START: What's the task?
│
├─ Single file, obvious change?
│   └─ SKIP (no discovery needed)
│
├─ One pattern/skill needed?
│   └─ QUICK (use CLAUDE.md inline reference)
│
├─ Multiple skills or unfamiliar?
│   └─ STANDARD (read SKILL-INDEX + CONTEXT-GRAPH)
│
└─ Full feature/CRUD workflow?
    └─ DEEP (full 4-step protocol)
```

| Tier | Task Complexity | Files Read | Time |
|------|-----------------|------------|------|
| **SKIP** | Simple (typo, comment) | 0 | ~0s |
| **QUICK** | Single-skill | 0 | ~2s |
| **STANDARD** | Multi-skill | 2 | ~10s |
| **DEEP** | Full implementation | 4+ | ~15-20s |

---

## Model Selection Matrix

| Model | Characteristics | Best For |
|-------|-----------------|----------|
| **haiku** | Fast, economical | Quick tasks, simple operations |
| **sonnet** | Balanced | Standard development tasks |
| **opus** | Powerful reasoning | Complex architecture, security |

### By Agent Type

| Agent Type | Recommended Model |
|------------|-------------------|
| Code reviewers | sonnet |
| Security auditors | opus |
| Implementers | sonnet |
| Quick scaffolding | haiku |

---

## Tool Permission Matrix

| Agent Type | Recommended Tools |
|------------|-------------------|
| **Read-only** (reviewers) | `Read, Grep, Glob` |
| **Research** | `Read, Grep, Glob, WebFetch, WebSearch` |
| **Code writers** | `Read, Write, Edit, Bash, Glob, Grep` |
| **Documentation** | `Read, Write, Edit, Glob, Grep, WebFetch` |

### Tool Selection for Tasks

| Task | Use | Not |
|------|-----|-----|
| Find files | Glob | Bash ls/find |
| Search content | Grep | Bash grep/rg |
| Read file | Read | Bash cat |
| Edit file | Edit | Bash sed |
| Create file | Write | Bash echo |

## Related

- [Tool Usage Patterns](../patterns/tool-usage-patterns.md)
- [Tool Permissions Reference](tool-permissions.md)
- [Model Selection Reference](model-selection.md)
