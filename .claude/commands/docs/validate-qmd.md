---
description: Validate Queryable Markdown (QMD) compliance using heading-based sections
allowed-tools: Read, Glob, Grep
argument-hint: <path> [--fix] [--verbose]
model: haiku
---

# QMD Validation Command

Validate files against Queryable Markdown (QMD) standard for token-efficient retrieval.

## Usage

```bash
/docs:validate-qmd <path> [options]
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<path>` | Yes | File, folder, or glob pattern |
| `--fix` | No | Show fix suggestions |
| `--verbose` | No | Show all checks (not just failures) |

---

## Validation Rules

### Frontmatter (Required)

| Rule | Check | Fix |
|------|-------|-----|
| FM-01 | Has frontmatter (`---` delimiters) | Add YAML frontmatter |
| FM-02 | Has `name:` field | Add identifier |
| FM-03 | Has `description:` (< 100 chars) | Shorten description |
| FM-04 | Has `layer:` (1-4) | Add layer number |
| FM-05 | Has `keywords:` array | Add grep targets |
| FM-06 | Frontmatter ≤ 20 lines | Reduce frontmatter |

### Structure (Required)

| Rule | Check | Fix |
|------|-------|-----|
| ST-01 | Has `## Summary` heading | Add summary section |
| ST-02 | Summary ≤ 10 lines | Shorten summary |
| ST-03 | Has `## Quick Reference` heading | Add quick ref section |
| ST-04 | Major sections separated by `---` | Add horizontal rules |

### Heading Hierarchy (Recommended)

| Rule | Check | Fix |
|------|-------|-----|
| HH-01 | Single `# Title` at top | Fix heading levels |
| HH-02 | `## ` for major sections | Use level-2 headings |
| HH-03 | `### ` for subsections | Use level-3 for subs |
| HH-04 | No skipped levels | Fix `#` → `###` gaps |

### Grep-Friendliness (Index Files)

| Rule | Check | Fix |
|------|-------|-----|
| GF-01 | Tables use `\| col \|` format | Reformat to tables |
| GF-02 | One entry per line | Split multi-line entries |

---

## Section Detection

QMD uses **markdown-native** section detection:

```markdown
## Section A          ← Section starts at ## heading
Content...

---                   ← Section ends at --- or next ##

## Section B          ← Next section starts
```

**Validation checks**:
1. Required headings exist: `## Summary`, `## Quick Reference`
2. Sections are separated by `---` horizontal rules
3. No orphaned content before first `## `

---

## Output Format

```
FILE: .claude/agents/engineers/abp-developer.md

✅ FM-01: Has frontmatter
✅ FM-02: Has name field
⚠️ FM-03: Description 142 chars (max 100)
✅ FM-04: Has layer field
✅ FM-05: Has keywords
✅ FM-06: Frontmatter 17 lines
✅ ST-01: Has ## Summary
✅ ST-02: Summary 3 lines
✅ ST-03: Has ## Quick Reference
⚠️ ST-04: Missing --- separator after Summary

Score: 8/10 passed, 2 warnings
```

---

## Execution Steps

1. **Glob files** matching `<path>`
2. **For each file**:
   - `Read(limit: 25)` for frontmatter check
   - `Grep("^## ")` for section headings
   - `Grep("^---$")` for separators
   - Verify required headings exist
3. **Report** per-file and summary

---

## Examples

```bash
# Validate single agent
/docs:validate-qmd .claude/agents/engineers/abp-developer.md

# Validate all agents
/docs:validate-qmd ".claude/agents/**/*.md"

# Validate all skills with fix suggestions
/docs:validate-qmd ".claude/skills/**/*.md" --fix

# Validate indexes
/docs:validate-qmd ".claude/*-INDEX.md"
```

---

## Related

- [content-retrieval](../../skills/content-retrieval/SKILL.md) - QMD standard definition
- [GUIDELINES.md](../../GUIDELINES.md#queryable-markdown-qmd-standard) - QMD overview
