# Agent Separation of Concerns

> Extracted from GUIDELINES.md for modularity. Core pattern for lean, maintainable agents.

## Core Principle

Agents should be **thin coordinators**, not repositories of embedded knowledge.

| Component | Contains | Does NOT Contain |
|-----------|----------|------------------|
| **Agent** | Identity, coordination, tool permissions, skill references | Code templates, output formats, CLI commands |
| **Skill** | Procedural knowledge, patterns, templates, domain expertise | Execution logic, atomic actions |
| **Command** | Executable atomic actions, user-invoked shortcuts | Domain knowledge, reusable patterns |

## What Belongs Where

```
Agent ("What I am")           Skill ("What to know")         Command ("What to do")
─────────────────────        ──────────────────────         ────────────────────────
• Role definition            • Code patterns                • /add-migration
• Core responsibilities      • Output format templates      • /run-tests
• Tool permissions           • Best practices               • /scaffold-entity
• Skill references           • Step-by-step procedures
• Coordination logic         • Domain-specific knowledge
• Context management         • Reusable templates
```

## Detection Rules

### Extract to Skill When Agent Contains:

| Indicator | Lines | Action |
|-----------|-------|--------|
| Code samples (```csharp, ```typescript) | >20 | Extract to skill |
| Output format templates | >15 | Extract to skill |
| Step-by-step procedures | >10 | Extract to skill |
| Domain-specific patterns | Any | Extract to skill |
| Content repeated across agents | Any | Create shared skill |

### Extract to Command When Agent Contains:

| Indicator | Action |
|-----------|--------|
| "Run this command: ..." | Extract to command |
| "Execute the following: ..." | Extract to command |
| Single-purpose atomic tasks | Extract to command |
| Tasks with arguments/flags | Extract to command |
| Frequently invoked tasks | Extract to command |

## Before/After Example

### BEFORE: Agent with Embedded Knowledge (345 lines)

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

### AFTER: Lean Agent with References (85 lines)

```markdown
# ABP Developer Agent

You are a Senior .NET Developer specializing in ABP Framework.

## Project Context

Before implementation, read:
1. `docs/architecture/README.md` - Project structure
2. `docs/domain/entities/` - Entity definitions
3. Technical specification (if provided)

## Implementation Approach

1. **Apply skills** (auto-loaded via frontmatter):
   - `abp-framework-patterns` - Entity, AppService patterns
   - `efcore-patterns` - Database configuration
   - `fluentvalidation-patterns` - Input validation

2. **Use commands** for atomic tasks:
   - `/generate:entity <name>` - Scaffold entity files
   - `/generate:migration <name>` - Create EF Core migration
   - Build and test using standard dotnet commands

3. **Follow existing patterns** in the codebase

## Constraints
[Concise list of rules - 10-15 lines]
```

## Agent Size Guidelines

| Metric | Target | If Exceeded |
|--------|--------|-------------|
| Total lines | <150 | Extract to skills/commands |
| Code blocks | <30 lines total | Extract to skill |
| CLI commands | <10 | Extract to command |
| Repeated content | 0 | Create shared skill |

## Refactoring Checklist

When agents grow too large (>150 lines):

- [ ] Audit agent size: `wc -l agents/**/*.md`
- [ ] Identify code blocks (```csharp, ```typescript, etc.)
- [ ] Extract code patterns to skills
- [ ] Identify CLI commands and build scripts
- [ ] Extract atomic actions to commands
- [ ] Move project-specific paths to `docs/`
- [ ] Update agent to reference skills and commands
- [ ] Verify agent produces same outputs
- [ ] Update agent frontmatter with `skills:` field

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Code templates in agent | Agent too large, not reusable | Extract to skill |
| CLI commands in agent | Not reusable, hard to maintain | Extract to command |
| Repeated content across agents | Duplication, inconsistency | Create shared skill |
| Project-specific paths in agent | Not portable | Move to `docs/` or dynamic detection |
| Embedded output formats | Can't be reused | Extract to skill |

## Related

- [Skill Optimization](skill-optimization.md) - Writing effective skills
- [Tool Permissions](../reference/tool-permissions.md) - Agent tool access
- [GUIDELINES.md](../../GUIDELINES.md#agents-agents) - Agent overview
