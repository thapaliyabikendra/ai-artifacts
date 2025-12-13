# Model Selection Reference

> Guide for choosing the right model for agents and tasks.

## Available Models

| Model | Characteristics | Token Cost | Speed |
|-------|-----------------|------------|-------|
| **haiku** | Fast, economical | Lowest | Fastest |
| **sonnet** | Balanced performance | Medium | Medium |
| **opus** | Powerful reasoning | Highest | Slower |

## Selection by Task Type

### Use Haiku

**Best for**: Quick, straightforward tasks

| Task Type | Example |
|-----------|---------|
| Simple scaffolding | Generate boilerplate |
| Template expansion | Fill in placeholders |
| Quick lookups | Find specific patterns |
| Formatting | Code formatting, linting |
| Simple analysis | Line counts, basic stats |

```yaml
name: quick-scaffold
model: haiku
```

### Use Sonnet

**Best for**: Standard development tasks (default choice)

| Task Type | Example |
|-----------|---------|
| Code implementation | Write AppService |
| Code review | Review PR changes |
| Debugging | Investigate errors |
| Testing | Write unit tests |
| Documentation | Generate docs |

```yaml
name: abp-developer
model: sonnet
```

### Use Opus

**Best for**: Complex reasoning, critical decisions

| Task Type | Example |
|-----------|---------|
| Architecture design | System design decisions |
| Security analysis | Threat modeling, audits |
| Complex debugging | Multi-system issues |
| Critical reviews | Production code review |
| Strategic planning | Long-term decisions |

```yaml
name: security-engineer
model: opus
```

## Selection by Agent Type

| Agent Category | Recommended Model | Rationale |
|----------------|-------------------|-----------|
| **Architects** | sonnet/opus | Design requires reasoning |
| **Reviewers** | sonnet | Balance of speed and quality |
| **Engineers** | sonnet | Standard implementation |
| **Specialists** | sonnet/opus | Depends on domain complexity |

### Specific Agent Recommendations

| Agent | Model | Why |
|-------|-------|-----|
| `backend-architect` | sonnet | Design decisions need balance |
| `business-analyst` | sonnet | Requirements analysis |
| `abp-developer` | sonnet | Standard implementation |
| `react-developer` | sonnet | Standard implementation |
| `abp-code-reviewer` | sonnet | Thorough but efficient review |
| `security-engineer` | opus | Security requires deep analysis |
| `qa-engineer` | sonnet | Test writing |
| `debugger` | sonnet | Most bugs don't need opus |
| `database-migrator` | sonnet | Schema changes |
| `devops-engineer` | sonnet | Infrastructure tasks |

## Cost Optimization

### Principle: Start Low, Escalate as Needed

```
1. Try haiku for simple tasks
2. Default to sonnet for standard work
3. Use opus only when necessary
```

### Cost-Effective Patterns

| Pattern | Implementation |
|---------|----------------|
| **Quick scaffolding** | Use haiku for boilerplate |
| **Two-pass review** | Haiku for initial scan, sonnet for flagged items |
| **Staged implementation** | Haiku for planning, sonnet for code |
| **Critical path only** | Opus only for security/architecture |

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Opus for everything | Expensive, slow | Use sonnet by default |
| Haiku for complex code | Quality issues | Upgrade to sonnet |
| Same model for all agents | Inefficient | Match to task complexity |

## Thinking Modes

Enhance model reasoning with thinking prompts:

| Phrase | Effect | Use With |
|--------|--------|----------|
| `"think"` | Baseline extended thinking | sonnet |
| `"think hard"` | Increased reasoning | sonnet/opus |
| `"think harder"` | High reasoning | opus |
| `"ultrathink"` | Maximum reasoning | opus |

**Example**:
```
"Think hard about the security implications of this API design."
```

## Model Inheritance

Agents can inherit parent model or specify their own:

```yaml
# Explicit model
name: my-agent
model: opus

# Inherit from parent (default)
name: my-agent
# model: not specified = inherits
```

## Performance Tuning

### For Speed

- Use haiku where possible
- Parallelize subagent tasks
- Keep prompts concise

### For Quality

- Use opus for critical decisions
- Enable extended thinking
- Provide detailed context

### For Cost

- Default to sonnet
- Reserve opus for security/architecture
- Use haiku for scaffolding

## Decision Matrix

| Priority | Haiku | Sonnet | Opus |
|----------|-------|--------|------|
| **Speed** | ✅ Best | Good | Slow |
| **Cost** | ✅ Best | Medium | High |
| **Quality** | Basic | ✅ Good | ✅ Best |
| **Reasoning** | Limited | Good | ✅ Best |

## Related

- [Decision Matrices](decision-matrices.md)
- [Tool Permissions](tool-permissions.md)
- [Agent Examples](../examples/agent-examples.md)
