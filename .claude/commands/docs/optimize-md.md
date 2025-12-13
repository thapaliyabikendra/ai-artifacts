---
description: Analyze and optimize markdown files for size, structure, and maintainability
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
argument-hint: <path> [--profile <type>] [--mode audit|apply|check] [--max-lines N]
model: opus
---

# Markdown Optimization Command

Analyze and optimize markdown files for maintainability, compaction, and structure.

## Usage

```bash
/docs:optimize-md <path> [options]
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<path>` | Yes | File, folder, or glob pattern to analyze |
| `--profile <type>` | No | Force specific profile (auto-detected if omitted) |
| `--mode <mode>` | No | `audit` (default), `apply`, or `check` |
| `--max-lines <N>` | No | Override default line limit |

## Modes

| Mode | Description | Output |
|------|-------------|--------|
| `audit` | Analyze and produce report (default) | Markdown report |
| `apply` | Implement suggested changes (**requires confirmation**) | Modified files |
| `check` | CI-friendly validation | Exit code 0 (pass) or 1 (fail) |

## Profiles

Profiles define document-specific rules. Auto-detected from path or use `--profile`:

| Profile | Auto-Detected From | Max Lines |
|---------|-------------------|-----------|
| `claude-md` | `CLAUDE.md`, `*.claude.md` | 300 |
| `architecture` | `docs/architecture/**` | 500 |
| `domain` | `docs/domain/**` | 400 |
| `feature-spec` | `docs/features/**` | 600 |
| `readme` | `README.md` | 200 |
| `skill` | `.claude/skills/**/SKILL.md` | 500 |
| `agent` | `.claude/agents/**/*.md` | 150 |
| `generic` | Any other `.md` | 500 |

**Custom profiles**: Define in `.claude/config/md-profiles.yaml` (see skill reference).

## Context

Before analysis, apply the `markdown-optimization` skill for patterns and profiles.

## Execution Flow

### 1. Parse Arguments

Extract from `$ARGUMENTS`:
- `path`: Required target (file/folder/glob)
- `profile`: Optional, auto-detect if not provided
- `mode`: Default to `audit`
- `max-lines`: Optional override

### 2. Discover Files

```bash
# Single file
if [[ -f "$path" ]]; then files=("$path")

# Folder
elif [[ -d "$path" ]]; then files=$(find "$path" -name "*.md")

# Glob pattern
else files=$(glob "$path")
fi
```

### 3. Auto-Detect Profile (if not specified)

| Path Pattern | Profile |
|--------------|---------|
| `**/CLAUDE.md` | `claude-md` |
| `docs/architecture/**` | `architecture` |
| `docs/domain/**` | `domain` |
| `docs/features/**` | `feature-spec` |
| `**/README.md` | `readme` |
| `.claude/skills/**` | `skill` |
| `.claude/agents/**` | `agent` |
| Default | `generic` |

### 4. Run Analysis

For each file, check:

1. **Size** - Lines vs profile limit
2. **Structure** - Heading hierarchy, TOC presence
3. **Duplication** - Repeated content across files
4. **Links** - Broken internal links
5. **Compaction** - Prose → table opportunities

### 5. Execute Mode

#### Audit Mode (default)
Generate report without modifications.

#### Apply Mode
**IMPORTANT**: Before making any changes:
1. Show proposed changes summary
2. Use `AskUserQuestion` to confirm:
   - "Proceed with all changes?"
   - "Select specific changes to apply"
   - "Cancel"

Only proceed with explicit user confirmation.

#### Check Mode
Return exit code:
- `0` if all files pass limits
- `1` if any file fails

## Output Format

### Audit Report

```markdown
# Markdown Optimization Report

## Target: {path}
## Profile: {profile} {auto-detected|specified}
## Date: {timestamp}

## Summary
| Metric | Value |
|--------|-------|
| Files analyzed | N |
| Total lines | N |
| Over limit | N |
| Broken links | N |
| Duplications | N |

## Size Issues
| File | Lines | Limit | Status | Action |
|------|-------|-------|--------|--------|

## Structure Issues
| File | Issue | Severity | Fix |
|------|-------|----------|-----|

## Duplication Findings
| Concept | Found In | Recommendation |
|---------|----------|----------------|

## Compaction Opportunities
| File | Section | Lines | Technique | Potential Savings |
|------|---------|-------|-----------|-------------------|

## Link Issues
| File:Line | Link | Issue |
|-----------|------|-------|

## Recommended Actions
1. [Prioritized by impact]
2. ...
```

### Check Output

```
✅ PASS: docs/architecture/README.md (245/500 lines)
✅ PASS: docs/domain/enums.md (89/400 lines)
❌ FAIL: docs/domain/business-rules.md (620/400 lines)
❌ FAIL: CLAUDE.md (380/300 lines)

Result: FAILED (2 of 4 files over limit)
```

## Examples

```bash
# Audit CLAUDE.md
/docs:optimize-md CLAUDE.md

# Audit all docs
/docs:optimize-md docs/

# Apply optimizations with confirmation
/docs:optimize-md docs/domain/ --mode apply

# CI validation
/docs:optimize-md . --mode check

# Override line limit
/docs:optimize-md docs/architecture/README.md --max-lines 600

# Force specific profile
/docs:optimize-md my-doc.md --profile architecture
```

## Related Commands

- `/optimize-guidelines` - Specialized for GUIDELINES.md (more comprehensive)
- `/refactor:tech-debt` - Code-focused technical debt analysis

## Skill Reference

Apply the `markdown-optimization` skill for:
- Detailed profile definitions
- Compaction patterns and techniques
- Custom profile configuration
