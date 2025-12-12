---
description: Compare two git commits based on commit hashes with detailed analysis
allowed-tools: Bash, Read, Glob, Grep
argument-hint: "<past-commit-hash> <latest-commit-hash>"
model: sonnet
---

# Git Commit Duel

Compare two git commits to analyze changes, identify patterns, and understand the evolution of code between two points in history.

**Arguments**: $ARGUMENTS

## Usage

```bash
/duel <past-commit-hash> <latest-commit-hash>
```

**Examples:**
```bash
/duel abc1234 def5678
/duel HEAD~5 HEAD
/duel v1.0.0 v2.0.0
```

## What This Command Does

This command performs a comprehensive comparison between two commits:

1. **Commit Metadata**: Author, date, commit messages
2. **File Changes**: Added, modified, deleted files
3. **Code Statistics**: Lines changed, file types affected
4. **Detailed Diff**: Side-by-side code comparison
5. **Impact Analysis**: Which components/modules were affected
6. **Pattern Detection**: Refactoring, bug fixes, features

## Workflow

### 1. Parse Arguments

Extract commit hashes from: $ARGUMENTS

Expected format: `<commit1> <commit2>`

If not provided or invalid, show usage and exit.

### 2. Validate Commits

Check that both commits exist in the repository:

```bash
git cat-file -e <commit1>^{commit}
git cat-file -e <commit2>^{commit}
```

If either commit is invalid, show error with available recent commits.

### 3. Gather Commit Metadata

For each commit, collect:
- Commit hash (full and short)
- Author name and email
- Commit date
- Commit message (subject and body)
- Parent commit(s)

Use:
```bash
git show --no-patch --format=fuller <commit-hash>
```

### 4. Analyze Changes Between Commits

Get overview statistics:
```bash
git diff --stat <commit1>..<commit2>
```

Get detailed file changes:
```bash
git diff --name-status <commit1>..<commit2>
```

Get full diff:
```bash
git diff <commit1>..<commit2>
```

### 5. Categorize Changes

Group files by:
- **Added** (A): New files introduced
- **Modified** (M): Existing files changed
- **Deleted** (D): Files removed
- **Renamed** (R): Files moved/renamed
- **Copied** (C): Files copied

### 6. Impact Analysis

Analyze which parts of the codebase were affected:
- Source code changes (by language/framework)
- Configuration changes
- Documentation changes
- Test changes
- Build/deployment changes

For this project specifically, identify:
- Backend changes (api/src/**)
- Test changes (api/test/**)
- Documentation changes (docs/**)
- Claude artifacts changes (.claude/**)
- Configuration changes (*.json, *.md, etc.)

### 7. Pattern Detection

Identify change patterns:
- **Feature Addition**: New files, new classes/functions
- **Bug Fix**: Small targeted changes, test additions
- **Refactoring**: File renames, structure changes, no behavior change
- **Performance**: Query optimization, caching, async changes
- **Security**: Authentication, authorization, validation changes
- **Documentation**: README, comments, docs/ changes
- **Dependencies**: Package updates, version changes

### 8. Code Statistics

Calculate:
- Total lines added
- Total lines deleted
- Net change (added - deleted)
- Number of files changed
- Number of commits between the two points
- Average lines changed per file

### 9. Detailed Diff Presentation

For each changed file:
- Show file path
- Show change type (Added/Modified/Deleted)
- Show line statistics (+X -Y)
- Optionally show key code snippets for significant changes

### 10. Generate Summary Report

## Output Format

```markdown
# Git Commit Duel: <commit1> vs <commit2>

## Commit Information

### Past Commit (<commit1>)
- **Hash**: <full-hash> (<short-hash>)
- **Author**: <name> <<email>>
- **Date**: <date>
- **Message**: <subject>

### Latest Commit (<commit2>)
- **Hash**: <full-hash> (<short-hash>)
- **Author**: <name> <<email>>
- **Date**: <date>
- **Message**: <subject>

## Comparison Summary

**Time Range**: <days> days, <hours> hours
**Commits Between**: X commits
**Files Changed**: X files (A added, M modified, D deleted, R renamed)
**Lines Changed**: +X -Y (net: ±Z)

## Changes by Category

### Backend Changes
- api/src/... (X files)
- Key changes: [summary]

### Test Changes
- api/test/... (X files)
- Key changes: [summary]

### Documentation
- docs/... (X files)
- CLAUDE.md, README.md changes

### Claude Artifacts
- .claude/agents/... (X files)
- .claude/skills/... (X files)
- .claude/commands/... (X files)

### Configuration
- *.json, *.config changes

## Change Patterns Detected

- [ ] Feature Addition
- [ ] Bug Fix
- [ ] Refactoring
- [ ] Performance Optimization
- [ ] Security Enhancement
- [ ] Documentation Update
- [ ] Dependency Update

## Impact Analysis

**High Impact** (core functionality):
- [Files with significant changes]

**Medium Impact** (supporting code):
- [Files with moderate changes]

**Low Impact** (docs, tests, config):
- [Files with minor changes]

## Top Changed Files

| File | Lines Added | Lines Deleted | Net Change |
|------|-------------|---------------|------------|
| path/to/file1.cs | +50 | -20 | +30 |
| path/to/file2.ts | +30 | -10 | +20 |
| ... | ... | ... | ... |

## Detailed Diff

[Include key code changes for significant files]

## Recommendations

- Review high-impact changes carefully
- Run tests to verify no regressions
- Update documentation if needed
- Consider security implications
```

## Error Handling

Handle common errors gracefully:

1. **Invalid commit hash**: Show available commits with `git log --oneline -10`
2. **Commits in wrong order**: Automatically swap if commit1 is newer than commit2
3. **No changes**: If commits are identical, show message
4. **Large diffs**: Warn if >1000 files changed, offer to summarize only

## Advanced Options (Future Enhancement)

Consider parsing optional flags from $ARGUMENTS:
- `--files-only`: Show only file list, no diff
- `--stats-only`: Show only statistics
- `--full-diff`: Show complete diff for all files
- `--by-author`: Group changes by author
- `--by-date`: Show timeline of changes

## Integration with Skills

This command can optionally reference:
- `git-advanced-workflows` skill for complex git operations
- `code-review-excellence` skill for analyzing change quality
- `debugging-patterns` skill if comparing bug fix commits

---

**Begin comparison for**: $ARGUMENTS
