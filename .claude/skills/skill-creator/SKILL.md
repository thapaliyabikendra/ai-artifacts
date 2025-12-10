---
name: skill-creator
description: Guide for creating effective skills that extend Claude's capabilities. Use when users want to create, update, or improve a skill. Triggers include: (1) "create a skill for...", (2) "make a skill that...", (3) "improve this skill", (4) "help me build a skill", (5) reviewing/analyzing existing skills, (6) converting commands or workflows into reusable skills, (7) "package this as a skill", (8) "convert this to a skill".
---

# Skill Creator

Create effective, reusable skills that extend Claude's capabilities for any role or domain.

## Quick Reference

| Decision | Guidance |
|----------|----------|
| Skill vs Command? | See [references/skill-vs-command.md](references/skill-vs-command.md) |
| Which skill type? | See [references/skill-types.md](references/skill-types.md) |
| Role-specific design? | See [references/role-based-design.md](references/role-based-design.md) |
| Workflow patterns? | See [references/workflows.md](references/workflows.md) |
| Output formats? | See [references/output-patterns.md](references/output-patterns.md) |
| What to avoid? | See [references/anti-patterns.md](references/anti-patterns.md) |

## About Skills

Skills are modular packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a domain specialist.

**Skills provide:**
- Specialized workflows and multi-step procedures
- Tool integrations for specific file formats or APIs
- Domain expertise (schemas, business logic, conventions)
- Bundled resources (scripts, templates, references)
- Guardrails to prevent common mistakes

## Core Principles

### 1. Concise is Key

The context window is shared. Only add what Claude doesn't already know.

**Challenge each addition:** "Does Claude really need this?" and "Does this justify its token cost?"

### 2. Set Appropriate Freedom

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** (text instructions) | Multiple valid approaches | "Choose the best library" |
| **Medium** (pseudocode/parameters) | Preferred pattern with variation | "Use this pattern, adapt to framework" |
| **Low** (specific scripts) | Fragile/critical operations | "Run exactly this script" |

### 3. Show, Don't Tell

```markdown
# Weak
"Format commit messages properly"

# Strong
**Example:**
Input: Added user authentication with JWT tokens
Output: `feat(auth): implement JWT-based authentication`
```

## Skill Structure

```
skill-name/
├── SKILL.md              # Required - entry point (<500 lines)
├── scripts/              # Executable code (Python/Bash)
├── references/           # Documentation loaded on-demand
└── assets/               # Output templates, boilerplate
```

### SKILL.md Components

**Frontmatter (YAML) - Required:**
```yaml
---
name: skill-name          # kebab-case, matches directory
description: |            # Primary trigger mechanism
  What it does. Use when: (1) scenario, (2) scenario, (3) scenario.
---
```

**Body (Markdown):** Core workflow, essential examples, links to references.

### Bundled Resources

| Directory | Purpose | Load Behavior |
|-----------|---------|---------------|
| `scripts/` | Deterministic operations | Execute without loading |
| `references/` | Detailed documentation | Load on-demand |
| `assets/` | Templates, boilerplate | Copy/use in output |

## Skill Creation Process

### Step 1: Understand with Examples

Gather concrete usage examples:
- "What would a user say to trigger this skill?"
- "Can you show me 2-3 example requests?"
- "What outputs should this skill produce?"

**Skip only when** usage patterns are already clearly understood.

### Step 2: Plan Reusable Contents

For each example, identify:
1. What code gets rewritten repeatedly? → `scripts/`
2. What reference info is needed? → `references/`
3. What templates or boilerplate are needed? → `assets/`

**Example Analysis:**

| Skill | User Request | Reusable Resource |
|-------|--------------|-------------------|
| pdf-editor | "Rotate this PDF" | `scripts/rotate_pdf.py` |
| crud-service | "Create CRUD for Product" | `references/appservice-template.md` |
| frontend-builder | "Build me a todo app" | `assets/react-template/` |

### Step 3: Initialize the Skill

```bash
scripts/init_skill.py <skill-name> --path <output-dir> [--template <type>]
```

**Templates:**

| Template | Best For | Example Skills |
|----------|----------|----------------|
| `default` | General purpose | - |
| `tool` | File processing, CLI tools | docker-dotnet-containerize |
| `workflow` | Multi-step processes | code-review-excellence |
| `domain` | Business knowledge, schemas | postgresql |
| `analysis` | Audits, assessments | security-audit |
| `integration` | API/service connections | github-api |
| `generator` | Code/file generation | crud-service |
| `pattern` | Best practices, standards | error-handling-patterns |

### Step 4: Edit the Skill

1. **Start with resources** (`scripts/`, `references/`, `assets/`)
2. **Test scripts** by running them
3. **Write SKILL.md** with core workflow + navigation
4. **Delete unused** example files from initialization

**Writing Guidelines:**
- Use imperative form ("Run the script" not "Running the script")
- Keep SKILL.md under 500 lines
- Move detailed content to `references/`
- Include concrete before/after examples

### Step 5: Package the Skill

```bash
scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

Validates and creates a `.skill` distribution file.

### Step 6: Iterate

| Problem | Solution |
|---------|----------|
| Too verbose | Move details to `references/` |
| Inconsistent outputs | Add before/after examples |
| Missing context | Add user input gathering section |
| Fragile execution | Add scripts with lower freedom |

## Frontmatter Description Formula

The description is the **primary trigger mechanism**. Make it comprehensive:

```
[What it does] + Use when: (1) [trigger], (2) [trigger], (3) [trigger].
```

**Real Examples:**

```yaml
# crud-service
description: Generate complete ABP Framework CRUD services following
  established patterns with AppService, Interface, DTOs, and FluentValidation.
  Use when creating new entity services for Volo.Abp projects that need
  standard CRUD operations (Create, Read, Update, Delete, List), logging,
  validation, and optional import/export capabilities.

# docker-dotnet-containerize
description: Generate production-ready Docker configurations for .NET APIs
  with multi-stage builds, Alpine optimization, layer caching, and build
  scripts. Use when containerizing .NET applications, creating Dockerfiles,
  or optimizing existing Docker setups.

# code-review-excellence
description: Master effective code review practices to provide constructive
  feedback, catch bugs early, and foster knowledge sharing while maintaining
  team morale. Use when reviewing pull requests, establishing review standards,
  or mentoring developers.
```

## Progressive Disclosure

Skills use three-level loading:

1. **Metadata** (~100 words) - Always loaded for discovery
2. **SKILL.md body** (<5k words) - Loaded when skill triggers
3. **Bundled resources** (unlimited) - Loaded on-demand

**Key Pattern:** When supporting multiple frameworks/variants, keep selection guidance in SKILL.md; move variant-specific details to references.

```markdown
# In SKILL.md
## Framework Selection
- **React**: See [references/react.md](references/react.md)
- **Angular**: See [references/angular.md](references/angular.md)
- **Vue**: See [references/vue.md](references/vue.md)
```

## Quality Checklist

Before packaging:

- [ ] Description has explicit trigger scenarios (not just "helps with X")
- [ ] SKILL.md under 500 lines
- [ ] Clear entry point - user knows where to start
- [ ] Concrete examples, not abstract descriptions
- [ ] No duplicate content between SKILL.md and references
- [ ] Scripts tested and working
- [ ] Unused example files deleted
- [ ] Verification/validation phase included

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Vague triggers | Skill doesn't activate | List 3+ specific scenarios |
| Abstract-only | Inconsistent outputs | Add before/after examples |
| Monolithic | Wastes context | Split to references (<500 lines) |
| Kitchen sink | Unfocused | Create specialized skills |
| Missing validation | Silent failures | Add verification steps |

See [references/anti-patterns.md](references/anti-patterns.md) for complete list.

## Additional Resources

- **Skill Types**: [references/skill-types.md](references/skill-types.md) - Detailed archetypes with examples
- **Role-Based Design**: [references/role-based-design.md](references/role-based-design.md) - Guidance by role
- **Skill vs Command**: [references/skill-vs-command.md](references/skill-vs-command.md) - When to create each
- **Workflows**: [references/workflows.md](references/workflows.md) - Sequential, conditional, phased patterns
- **Output Patterns**: [references/output-patterns.md](references/output-patterns.md) - Templates, deliverables, reports
- **Template Patterns**: [references/template-patterns.md](references/template-patterns.md) - Placeholder conventions
- **Anti-Patterns**: [references/anti-patterns.md](references/anti-patterns.md) - What to avoid
