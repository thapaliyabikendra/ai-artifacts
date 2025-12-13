# Naming Conventions

> Standard naming rules for all Claude Code artifacts.

## General Rules

| Rule | Applies To | Example |
|------|------------|---------|
| Lowercase | All artifact names | `abp-developer`, not `ABP-Developer` |
| Kebab-case | File names, skill names | `code-review-patterns` |
| Hyphens only | Separators | `my-skill`, not `my_skill` |
| Max 64 chars | Skill names | Enforced by system |
| Descriptive | All names | `pdf-processing`, not `helper` |

## Agents

### File Naming

```
agents/{category}/{agent-name}.md
```

**Pattern**: `{role-description}.md`

| Good | Bad | Why |
|------|-----|-----|
| `abp-developer.md` | `developer.md` | Too generic |
| `security-engineer.md` | `security.md` | Missing role |
| `backend-architect.md` | `architect-backend.md` | Role first is convention |

### Name Field

```yaml
name: abp-developer  # lowercase, kebab-case
```

### Category Names

| Category | Contains |
|----------|----------|
| `architects/` | Design, planning roles |
| `reviewers/` | Analysis, critique roles |
| `engineers/` | Implementation roles |
| `specialists/` | Domain expert roles |

## Skills

### Folder Naming

```
skills/{skill-name}/
```

**Pattern**: `{topic-or-action}` or `{verb}ing-{noun}s`

| Good (Topic) | Good (Gerund) | Bad |
|--------------|---------------|-----|
| `pdf-processing` | `processing-pdfs` | `pdf-helper` |
| `abp-framework-patterns` | `building-abp-apps` | `utils` |
| `efcore-patterns` | `configuring-efcore` | `database` |

### Name Field

```yaml
name: abp-framework-patterns  # max 64 chars, lowercase, hyphens
```

### Reference File Naming

```
skills/{skill-name}/references/{topic}.md
```

| Good | Bad |
|------|-----|
| `advanced-queries.md` | `ADVANCED.md` |
| `error-handling.md` | `errors.MD` |
| `api-reference.md` | `ref.md` |

## Commands

### File Naming

```
commands/{category}/{command-name}.md
```

**Pattern**: `{verb}` or `{verb}-{noun}`

| Good | Bad | Why |
|------|-----|-----|
| `entity.md` | `generate-entity.md` | Category provides context |
| `smart-debug.md` | `debug.md` | Specific is better |
| `tdd-cycle.md` | `tdd.md` | Describes full action |

### Category Names

| Category | Purpose | Examples |
|----------|---------|----------|
| `generate/` | Create new code | entity, migration |
| `review/` | Analyze code | permissions, code-review |
| `debug/` | Fix issues | smart-debug |
| `refactor/` | Improve code | tech-debt, cleanup |
| `tdd/` | Test workflows | tdd-cycle |
| `feature/` | Feature development | add-feature |
| `team/` | Collaboration | issue, standup |

## Hooks

Hook names aren't files but identifiers in settings:

```json
{
  "hooks": {
    "PostToolUse": [...]  // Event name, PascalCase
  }
}
```

## Output Styles

### File Naming

```
output-styles/{style-name}.md
```

| Good | Bad |
|------|-----|
| `teaching-mode.md` | `teach.md` |
| `verbose-explanations.md` | `verbose.md` |

## Descriptions

### Third-Person Rule

**Always write descriptions in third person** - they're injected into system prompts.

| Good | Bad |
|------|-----|
| "Processes PDFs and extracts text" | "I can help you process PDFs" |
| "Reviews code for security issues" | "Use this to review code" |

### Trigger Inclusion

Include 3+ trigger scenarios:

```yaml
# Good
description: |
  Extract text and tables from PDF files, fill forms, merge documents.
  Use when: (1) working with PDFs, (2) extracting content, (3) filling forms.

# Bad
description: Helps with documents
```

## Placeholders

For portable artifacts:

| Placeholder | Use For |
|-------------|---------|
| `{ProjectName}` | Solution/project name |
| `{Entity}` | Entity class name |
| `{Feature}` | Feature/module name |
| `{SolutionName}` | Solution file name |
| `{Project}` | Short project prefix |

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| `utils.md` | Too vague | Describe what it does |
| `helper.md` | Non-descriptive | Name the domain |
| `misc/` | Catch-all category | Create proper category |
| `UPPERCASE.md` | Inconsistent | Use lowercase |
| `snake_case` | Wrong convention | Use kebab-case |
| First-person description | Awkward in prompts | Use third person |

## Checklist

- [ ] Name is lowercase
- [ ] Uses kebab-case (hyphens)
- [ ] Under 64 characters
- [ ] Descriptive of purpose
- [ ] Follows category conventions
- [ ] Description in third person
- [ ] Includes trigger scenarios

## Related

- [File Formats](file-formats.md)
- [Creating Artifacts](../workflows/creating-artifacts.md)
- [Antipatterns](../examples/antipatterns.md)
