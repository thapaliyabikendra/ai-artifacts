# Portability Patterns

> Extracted from GUIDELINES.md for modularity. Rules for creating reusable, project-agnostic artifacts.

## Core Principle

**All Claude artifacts (agents, skills, commands) must be generic and reusable.** They should work across any project without modification.

## Prohibited Content in Artifacts

| Content Type | Example (BAD) | Alternative (GOOD) |
|--------------|---------------|-------------------|
| **Project names** | `ClinicManagementSystem`, `MyApp` | `{ProjectName}` placeholder |
| **Entity names** | `Patient`, `Doctor`, `Order` | `{Entity}`, `{EntityName}` placeholders |
| **Hardcoded paths** | `api/src/ClinicManagementSystem.Domain/` | Dynamic detection or `{ProjectName}` |
| **Solution files** | `ClinicManagementSystem.slnx` | `{SolutionName}.slnx` or `find` command |
| **Permission names** | `ClinicPermissions.Patients.Create` | `{Project}Permissions.{Feature}.{Action}` |
| **Namespace prefixes** | `ClinicManagementSystem.` | `{ProjectName}.` |

## Dynamic Project Detection

For commands and agents that need to locate project files:

```bash
# Find EntityFrameworkCore project
EF_PROJECT=$(find api/src -maxdepth 1 -type d -name "*EntityFrameworkCore" | head -1)

# Find DbMigrator project
MIGRATOR=$(find api/src -maxdepth 1 -type d -name "*DbMigrator" | head -1)

# Find solution file
SOLUTION=$(find api -maxdepth 1 -name "*.slnx" -o -name "*.sln" | head -1)

# Find project name from solution
PROJECT_NAME=$(basename "$SOLUTION" | sed 's/\.slnx\|\.sln//')
```

## Placeholder Conventions

| Placeholder | Meaning | Example Usage |
|-------------|---------|---------------|
| `{ProjectName}` | Solution/project name | `{ProjectName}.Domain` |
| `{Entity}` | Entity class name | `public class {Entity}` |
| `{EntityName}` | Entity name (same as above) | `{EntityName}Dto` |
| `{Feature}` | Feature/module name | `{Feature}AppService` |
| `{SolutionName}` | Solution file name | `{SolutionName}.slnx` |
| `{Project}` | Short project prefix | `{Project}Permissions` |

## Where Project-Specific Content Belongs

| Location | Purpose | Example Content |
|----------|---------|-----------------|
| `CLAUDE.md` | Project overview, entity list | "Entities: Patient, Doctor, Appointment" |
| `docs/architecture/README.md` | Project structure, paths | "Solution: api/ClinicManagementSystem.slnx" |
| `docs/domain/entities/` | Entity definitions | "Patient has Name, DOB, Email" |
| `docs/project-context.md` | All project values in one place | Project name, paths, conventions |

## Artifact Examples

### BAD: Hardcoded Project

```markdown
# ABP Developer Agent

## Project Structure
api/src/ClinicManagementSystem.Domain/Entities/
api/src/ClinicManagementSystem.Application/Services/

## Build
dotnet build api/ClinicManagementSystem.slnx
```

### GOOD: Portable Agent

```markdown
# ABP Developer Agent

## Project Context
Before implementation, read:
- `CLAUDE.md` for project overview
- `docs/architecture/README.md` for structure

## Build
Use solution file found via: `find api -name "*.slnx" -o -name "*.sln"`
```

### BAD: Hardcoded Skill

```csharp
// In skill code example
public class PatientAppService : ApplicationService
{
    // Uses ClinicManagementSystem-specific code
}
```

### GOOD: Portable Skill

```csharp
// In skill code example
public class {Entity}AppService : ApplicationService, I{Entity}AppService
{
    // Generic pattern that works for any entity
}
```

## Validation Checklist

Before committing any artifact:

- [ ] No hardcoded project names (search for your project name)
- [ ] No specific entity names in examples (use `{Entity}`, `Product`, `Order`)
- [ ] Paths use placeholders or dynamic detection
- [ ] Code samples use generic class names
- [ ] Permissions use `{Project}Permissions.{Feature}.{Action}` pattern
- [ ] Skills reference `CLAUDE.md` or `docs/` for project context
- [ ] Commands use dynamic file discovery

## Testing Portability

```bash
# Search for project-specific content
grep -r "ClinicManagementSystem" .claude/
grep -r "MyProjectName" .claude/

# Should return zero results for portable artifacts

# Check for hardcoded entity names
grep -r "Patient\|Doctor\|Invoice" .claude/skills/ .claude/agents/
# Review each match - examples should use generic names
```

## Context Loading Pattern

Agents and skills should load project context dynamically:

```markdown
## Project Context

Before proceeding, read:
1. `CLAUDE.md` - Project overview and conventions
2. `docs/architecture/README.md` - Project structure (if exists)
3. Relevant `docs/domain/` files for entity context

This ensures the artifact works across any ABP project.
```

## Related

- [Agent Separation](agent-separation.md) - What belongs in agents
- [GUIDELINES.md](../../GUIDELINES.md#artifact-portability-rules) - Overview
