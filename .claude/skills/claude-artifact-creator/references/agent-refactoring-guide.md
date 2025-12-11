# Agent Refactoring Guide: Extracting Skills and Commands

This guide helps identify when agent system prompts have grown too large and what should be extracted into Skills or Commands.

## The Agent Responsibility Principle

**Agents should contain ONLY:**
1. **Identity** - Role name and core purpose
2. **Coordination** - How to work with other agents
3. **Context Management** - What to read, what to write
4. **Tool Permissions** - What tools are allowed
5. **High-Level Approach** - General workflow steps
6. **Skill References** - Which skills to apply (not skill content)

**Agents should NOT contain:**
- Code templates (belongs in Skills)
- Detailed output formats (belongs in Skills)
- Atomic executable actions (belongs in Commands)
- Procedural multi-step instructions (belongs in Skills)
- Domain-specific patterns (belongs in Skills)

## Detection Checklist

### Signs of Over-Embedded Knowledge (Extract to Skill)

| Indicator | Lines | Action |
|-----------|-------|--------|
| Code samples in markdown | >20 | Extract to skill |
| Output format templates | >15 | Extract to skill |
| Step-by-step procedures | >10 | Extract to skill |
| Domain-specific patterns | Any | Extract to skill |
| Repeated across agents | Any | Extract to shared skill |

### Signs of Embedded Actions (Extract to Command)

| Indicator | Action |
|-----------|--------|
| "Run this command: ..." | Extract to command |
| "Execute the following steps: ..." | Extract to command |
| Single-purpose atomic tasks | Extract to command |
| Tasks with arguments/flags | Extract to command |
| Tasks invoked frequently | Extract to command |

## Refactoring Workflow

### Step 1: Audit Agent Size

```bash
# Count lines excluding frontmatter
wc -l .claude/agents/**/*.md
```

**Guidelines:**
- Agent prompt should be <150 lines (excluding frontmatter)
- If >150 lines, likely has embedded knowledge

### Step 2: Identify Knowledge Blocks

Look for these patterns:

```markdown
## Code Patterns        ← EXTRACT TO SKILL
### Entity Pattern
```csharp
// 50+ lines of code
```

## Output Templates     ← EXTRACT TO SKILL
### API Contract
| Column | Type | ...

## Commands            ← EXTRACT TO COMMAND
```bash
dotnet ef migrations add...
dotnet test...
```
```

### Step 3: Create Extraction Plan

For each block identified:

| Block | Type | Destination | Skill/Command Name |
|-------|------|-------------|-------------------|
| Entity Pattern | Code | Skill | `abp-framework-patterns` |
| Output Template | Format | Skill | `requirements-engineering` |
| Test Command | Action | Command | `/run-tests` |

### Step 4: Extract to Skills

**Original (embedded in agent):**
```markdown
## Code Patterns

### Entity Pattern
```csharp
public class {Entity} : FullAuditedAggregateRoot<Guid>
{
    public string Name { get; private set; }
    // ... 50 lines of code
}
```
```

**After extraction to skill:**
```markdown
## Implementation Approach

Apply `abp-framework-patterns` skill for:
- Entity class structure
- Domain validation patterns
- Repository interfaces
```

### Step 5: Extract to Commands

**Original (embedded in agent):**
```markdown
## Build & Test Commands

```bash
# Build solution
dotnet build api/{SolutionName}.slnx

# Run tests
dotnet test api/test/{ProjectName}.Application.Tests

# Add migration
dotnet ef migrations add {Name} -p api/src/{ProjectName}.EntityFrameworkCore -s api/src/{ProjectName}.DbMigrator
```
```

**After extraction to command:**
```markdown
## Execution

Use commands for atomic tasks:
- `/run-tests backend --filter {feature}` - Run specific tests
- `/add-migration {name}` - Create EF Core migration
```

### Step 6: Update Skill References

Add skills to agent frontmatter:
```yaml
---
name: abp-developer
skills: abp-framework-patterns, crud-service, dotnet-async-patterns
---
```

And in the body, reference them:
```markdown
## Implementation Approach

1. Apply skills (auto-loaded via frontmatter):
   - `abp-framework-patterns` - Entity, AppService patterns
   - `crud-service` - Full CRUD scaffolding

2. Reference project context from docs/project-context.md
```

## Before/After Examples

### Example 1: `abp-developer` Agent

**BEFORE (345 lines):**
```markdown
# ABP Developer Agent

## Project Structure (ABP Framework)
```
api/src/
├── {ProjectName}.Domain.Shared/
│   ├── Enums/
[... 40 lines of directory structure]
```

## Code Patterns

### Entity Pattern
```csharp
public class {Entity} : FullAuditedAggregateRoot<Guid>
{
    public string Name { get; private set; }
    [... 35 lines of C# code]
}
```

### AppService Pattern
```csharp
[Authorize({ProjectName}Permissions.{Feature}.Default)]
public class {Entity}AppService : ApplicationService
{
    [... 80 lines of C# code]
}
```

[... more code patterns ...]

## Build & Test Commands
```bash
dotnet build api/{SolutionName}.slnx
dotnet test api/test/{ProjectName}.Application.Tests
[... 20 lines of commands]
```
```

**AFTER (85 lines):**
```markdown
# ABP Developer Agent

You are a Senior .NET Developer specializing in ABP Framework.

## Project Context

Before starting any implementation, read:
1. `docs/project-context.md` - Project structure, paths, conventions
2. `docs/entity-glossary.md` - Domain entities
3. `docs/technical-specification.md` - API contracts

## Implementation Approach

1. **Apply skills** (auto-loaded):
   - `abp-framework-patterns` - Entity, AppService, Repository patterns
   - `crud-service` - CRUD scaffolding workflow
   - `dotnet-async-patterns` - Async best practices
   - `error-handling-patterns` - Exception handling

2. **Use commands** for atomic tasks:
   - `/scaffold-entity <name>` - Generate entity files
   - `/add-migration <name>` - Create EF Core migration
   - `/run-tests backend` - Run backend tests

3. **Follow existing patterns** - Examine similar entities in the codebase

## Constraints

- Follow ABP Framework conventions strictly
- Use async/await for all database operations
- Implement proper authorization
- Write FluentValidation validators
- Include logging for important operations
- Never expose entities directly; use DTOs
```

### Example 2: `qa-engineer` Agent

**BEFORE (265 lines):**
```markdown
## Test Patterns

### xUnit Pattern (ABP)
```csharp
public class {Entity}AppService_Tests : {ProjectName}ApplicationTestBase
{
    private readonly I{Entity}AppService _{entity}AppService;
    [... 45 lines of C# code]
}
```

### React Testing Library Pattern
```typescript
describe('EntityForm', () => {
  it('should submit valid data', async () => {
    [... 30 lines of TypeScript code]
  });
});
```

### Playwright E2E Pattern
```typescript
test.describe('{Feature} Management', () => {
  [... 25 lines of TypeScript code]
});
```
```

**AFTER (75 lines):**
```markdown
## Testing Approach

1. **Apply skills** (auto-loaded):
   - `xunit-testing-patterns` - Backend test structure, ABP patterns
   - `javascript-testing-patterns` - React Testing Library, Jest
   - `e2e-testing-patterns` - Playwright automation

2. **Reference project context** from docs/project-context.md for:
   - Test directory structure
   - Testing libraries in use
   - Test naming conventions

3. **Use commands** for execution:
   - `/run-tests backend --filter {feature}`
   - `/run-tests e2e`

4. **Follow existing test patterns** in the project
```

## Skill vs Command Decision for Extracted Content

| Extracted Content | Create | Why |
|-------------------|--------|-----|
| Code templates | Skill | Reusable knowledge |
| Output format templates | Skill | Reusable knowledge |
| Build commands list | Command | Atomic executable action |
| Step-by-step procedure | Skill | Procedural knowledge |
| Directory structure | Skill (or docs/) | Reference documentation |
| CLI command sequence | Command | Executable action |

## Common Refactoring Patterns

### Pattern 1: Code Templates → Skill

```markdown
# BEFORE (in agent)
## Entity Pattern
```csharp
[50 lines of code]
```

# AFTER (in agent)
Apply `{framework}-patterns` skill for entity structure.

# NEW SKILL
---
name: {framework}-patterns
---
## Entity Pattern
```csharp
[50 lines of code]
```
```

### Pattern 2: Output Formats → Skill

```markdown
# BEFORE (in agent)
## Output Templates
### API Contract
| Method | Path | Permission |
[detailed table format]

# AFTER (in agent)
Apply `api-design-principles` skill for contract format.

# ENHANCED SKILL
## Output Format: API Contract
| Method | Path | Permission |
[detailed table format]
```

### Pattern 3: Build Commands → Command

```markdown
# BEFORE (in agent)
## Commands
```bash
dotnet build api/{Solution}.slnx
dotnet test api/test/{Project}.Application.Tests --filter "{Entity}"
```

# AFTER (in agent)
Use `/run-tests backend --filter {entity}` for test execution.

# NEW COMMAND
---
description: Run tests for backend, frontend, or E2E
argument-hint: [backend|frontend|e2e] [--filter <pattern>]
---
```

### Pattern 4: Domain Knowledge → docs/ + Skill Reference

```markdown
# BEFORE (in agent)
## Project Structure
api/src/
├── {ProjectName}.Domain/
├── {ProjectName}.Application/
[... detailed structure]

# AFTER (in agent)
Read project structure from docs/project-context.md

# MOVE TO docs/project-context.md
## Directory Structure
api/src/
├── {ProjectName}.Domain/
├── {ProjectName}.Application/
[... detailed structure]
```

## Validation After Refactoring

1. **Size Check**: Agent prompt <150 lines
2. **No Code Blocks**: No `\`\`\`csharp` or `\`\`\`typescript` in agent
3. **Skill References**: Skills mentioned, not embedded
4. **Command References**: Commands referenced, not inline
5. **Project Context**: Uses docs/project-context.md for project-specific values
6. **Functional Test**: Agent produces same outputs with reduced prompt

## Summary

| Content Type | Move To | Reference As |
|--------------|---------|--------------|
| Code patterns | Skill | "Apply `skill-name` skill" |
| Output formats | Skill | "Follow `skill-name` format" |
| CLI commands | Command | "Use `/command-name`" |
| Project structure | docs/project-context.md | "Read docs/project-context.md" |
| Domain entities | docs/entity-glossary.md | "Reference docs/entity-glossary.md" |

**Goal**: Agents become thin coordinators that know WHAT to do (via skills) and HOW to execute (via commands), not repositories of embedded knowledge.
