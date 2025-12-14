# Generate Commit Message

Generate conventional commit message from staged changes.

## Arguments

`$ARGUMENTS`: `[--full]` `[--scope <scope>]` `[--type <type>]`

| Argument | Default | Description |
|----------|---------|-------------|
| `--full` | off | Include markdown body with summary and changes |
| `--scope` | auto | Override scope (e.g., `api`, `ui`, `docs`) |
| `--type` | auto | Override type (e.g., `feat`, `fix`, `refactor`) |

## Workflow

1. Run `git diff --staged` — if empty, tell user to stage files first
2. Analyze changes and generate message in format: `<type>(<scope>): <summary>`

## Output Format

**Quick Mode** (default):
```
<type>(<scope>): <summary>
```

**Full Mode** (`--full`):
```
<type>(<scope>): <summary>

<Brief summary of what changed and why>

- <change 1>
- <change 2>
```

## Constraints

- Max 72 characters for title
- No emojis, no markdown in title

**CRITICAL**: Output ONLY the raw commit message. No explanations, no analysis, no "Here's the message:", no code blocks. Just the message text itself.
