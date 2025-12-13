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
| `<path>` | Yes | File, folder, or glob pattern |
| `--profile <type>` | No | Force profile (auto-detected if omitted) |
| `--mode <mode>` | No | `audit` (default), `apply`, `check` |
| `--max-lines <N>` | No | Override line limit |

## Modes

| Mode | Description |
|------|-------------|
| `audit` | Analyze and produce report (default) |
| `apply` | Implement changes (**requires confirmation**) |
| `check` | CI-friendly validation (exit 0/1) |

## Profiles

Auto-detected from path. See [profiles.md](../../skills/markdown-optimization/references/profiles.md) for full definitions.

| Profile | Pattern | Max Lines |
|---------|---------|-----------|
| `claude-md` | `**/CLAUDE.md` | 300 |
| `guidelines` | `.claude/GUIDELINES.md`, `.claude/guidelines/**` | Varies* |
| `architecture` | `docs/architecture/**` | 500 |
| `domain` | `docs/domain/**` | 400 |
| `feature-spec` | `docs/features/**` | 600 |
| `readme` | `**/README.md` | 200 |
| `skill` | `.claude/skills/**` | 500 |
| `agent` | `.claude/agents/**` | 150 |
| `generic` | Default | 500 |

## Context

Apply the `markdown-optimization` skill before analysis for patterns and profile details.

## Execution

### 1. Parse Arguments

Extract from `$ARGUMENTS`: path (required), profile, mode, max-lines.

### 2. Discover & Profile Files

Use Glob to find `.md` files. Auto-detect profile from path patterns.

### 3. Run Analysis

For each file, check:
1. **Size** - Lines vs profile limit
2. **Structure** - Heading hierarchy, TOC presence
3. **Duplication** - Repeated content across files
4. **Links** - Broken internal links
5. **Compaction** - Prose → table opportunities

**Guidelines profile adds**: INDEX.md completeness, cross-references, folder structure, orphan detection. See [profiles.md](../../skills/markdown-optimization/references/profiles.md#profile-guidelines).

### 4. Execute Mode

**Audit**: Generate report, no modifications.

**Apply**: Show summary → `AskUserQuestion` for confirmation → implement approved changes.

**Check**: Return exit 0 (pass) or 1 (fail).

## Output

### Audit Report Structure

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
✅ PASS: file.md (245/500 lines)
❌ FAIL: other.md (620/400 lines)
Result: FAILED (1 of 2 over limit)
```

## Examples

```bash
# Basic audit
/docs:optimize-md CLAUDE.md
/docs:optimize-md docs/

# Apply with confirmation
/docs:optimize-md docs/domain/ --mode apply

# CI validation
/docs:optimize-md . --mode check

# Force profile / override limit
/docs:optimize-md my-doc.md --profile architecture
/docs:optimize-md README.md --max-lines 300

# Guidelines ecosystem
/docs:optimize-md .claude/GUIDELINES.md
/docs:optimize-md .claude/guidelines/ --mode check
```

## Related

- `markdown-optimization` skill - Profile definitions, compaction patterns
- `/refactor:tech-debt` - Code-focused analysis
