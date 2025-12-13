# Tool Permissions Reference

> Complete reference for tool permissions and access patterns.

## Available Tools

| Tool | Purpose | Modifies Files |
|------|---------|----------------|
| `Read` | Read file contents | No |
| `Write` | Create/overwrite files | Yes |
| `Edit` | Targeted string replacement | Yes |
| `Bash` | Execute shell commands | Potentially |
| `Glob` | Find files by pattern | No |
| `Grep` | Search file contents | No |
| `WebFetch` | Fetch URL content | No |
| `WebSearch` | Search the web | No |
| `Task` | Spawn subagents | No |
| `TodoWrite` | Manage task list | No |

## Permission Strategies by Role

### Read-Only Agents

**Use for**: Reviewers, auditors, analyzers

```yaml
tools: Read, Glob, Grep
```

**Examples**:
- `abp-code-reviewer`
- `react-code-reviewer`
- `security-engineer`

**Rationale**: Cannot modify code, only analyze.

### Research Agents

**Use for**: Information gatherers, documentation readers

```yaml
tools: Read, Glob, Grep, WebFetch, WebSearch
```

**Examples**:
- `business-analyst` (requirements research)

**Rationale**: Needs web access for research, but no code modification.

### Implementation Agents

**Use for**: Code writers, developers

```yaml
tools: Read, Write, Edit, Bash, Glob, Grep
```

**Examples**:
- `abp-developer`
- `react-developer`
- `devops-engineer`

**Rationale**: Full file system access for implementation.

### Documentation Agents

**Use for**: Technical writers, documentation generators

```yaml
tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
```

**Rationale**: Needs web access for references plus file writing.

## Tool Selection Best Practices

### Principle: Least Privilege

Only grant tools necessary for the agent's role.

```yaml
# BAD: Reviewer with write access
name: code-reviewer
tools: Read, Write, Edit, Bash, Glob, Grep

# GOOD: Reviewer with read-only access
name: code-reviewer
tools: Read, Glob, Grep
```

### Principle: Specific Over Broad

Use specific tools instead of Bash when possible.

| Instead of | Use |
|------------|-----|
| `Bash` with `cat` | `Read` |
| `Bash` with `grep` | `Grep` |
| `Bash` with `find` | `Glob` |
| `Bash` with `sed` | `Edit` |
| `Bash` with `echo >` | `Write` |

## Default Behavior

**Warning**: Omitting the `tools` field grants access to **ALL available tools** (including MCP tools).

```yaml
# This agent has access to EVERYTHING
name: dangerous-agent
# tools: not specified = all tools

# This agent has restricted access
name: safe-agent
tools: Read, Glob, Grep
```

**Always explicitly declare tools.**

## Permission Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `default` | Standard permission prompts | Normal operation |
| `acceptEdits` | Auto-accept edit operations | Trusted agents |
| `bypassPermissions` | Skip all permission checks | Fully automated workflows |

```yaml
name: trusted-agent
permissionMode: acceptEdits
```

**Warning**: Use `bypassPermissions` only for fully trusted, automated workflows.

## Tool Combinations

### Minimal Set (Analysis)

```yaml
tools: Read, Glob, Grep
```

Sufficient for: Code review, security audit, documentation reading.

### Standard Set (Implementation)

```yaml
tools: Read, Write, Edit, Bash, Glob, Grep
```

Sufficient for: Most development tasks.

### Extended Set (Research + Implementation)

```yaml
tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
```

Sufficient for: Tasks requiring external documentation lookup.

### Task Delegation

```yaml
tools: Read, Glob, Grep, Task
```

For: Orchestrator agents that delegate to specialized subagents.

## MCP Tools

When MCP servers are configured, their tools become available.

**Important**: If you omit `tools` field, MCP tools are also granted.

```yaml
# Explicitly exclude MCP tools
tools: Read, Write, Edit, Bash, Glob, Grep
# Only these core tools, no MCP
```

## Security Considerations

### High-Risk Tools

| Tool | Risk | Mitigation |
|------|------|------------|
| `Bash` | Command injection, system access | Limit to trusted agents |
| `Write` | Overwrite critical files | Use Edit for modifications |
| `WebFetch` | Data exfiltration | Limit to research agents |

### Audit Checklist

- [ ] All agents have explicit `tools` field
- [ ] Reviewers have read-only tools
- [ ] No unnecessary Bash access
- [ ] Permission mode appropriate for trust level

## Related

- [Tool Usage Patterns](../patterns/tool-usage-patterns.md)
- [Decision Matrices](decision-matrices.md)
- [Agent Examples](../examples/agent-examples.md)
