---
description: Analyze GUIDELINES.md for optimization opportunities or apply modular refactoring
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [--audit | --apply | --check]
model: opus
---

# Guidelines Optimization Command

Analyze and optimize the Claude Code GUIDELINES.md file for maintainability, compaction, and modularity.

## Modes

| Flag | Purpose | Tools Needed |
|------|---------|--------------|
| `--audit` | Analysis only - propose improvements (default) | Read, Glob, Grep |
| `--apply` | Implement modular structure and refactor | Read, Write, Edit |
| `--check` | Validate existing structure (size limits, duplication) | Read, Glob, Grep, Bash |

## Context

Read these files first:
1. `.claude/GUIDELINES.md` - Main guidelines document
2. `.claude/guidelines/INDEX.md` - Modular guidelines registry (if exists)

## Audit Mode (`--audit` or default)

### Role
You are a **Documentation Architecture & AI Prompt Systems Auditor** specializing in large guideline documents for AI tooling and prompt engineering.

### Analysis Checklist

1. **Size Check**
   - GUIDELINES.md should be under 1,000 lines
   - Any section >200 lines should be extracted
   - Pattern files should be under 400 lines

2. **Duplication Detection**
   - Concepts explained in multiple locations
   - Examples repeated across sections
   - Decision flowcharts in multiple places

3. **Structure Assessment**
   - Clear hierarchy: Principles → Patterns → Implementations
   - Each section has single responsibility
   - Cross-references instead of duplication

4. **Modularity Check**
   - Does `/guidelines/` folder exist?
   - Are patterns extracted to `/guidelines/patterns/`?
   - Are examples in `/guidelines/examples/`?

### Output Format

```markdown
# Guidelines Optimization Report

## Size Metrics
| File | Lines | Status |
|------|-------|--------|
| GUIDELINES.md | X | OK/OVER |

## Duplication Findings
| Concept | Found In | Recommendation |

## Extraction Candidates
| Section | Lines | Target Location |

## Recommended Actions
1. [Prioritized list]
```

## Apply Mode (`--apply`)

### Actions

1. **Create folder structure** (if missing):
   ```
   .claude/guidelines/
   ├── patterns/
   ├── standards/
   ├── examples/
   ├── workflows/
   └── reference/
   ```

2. **Extract large sections** to appropriate folders:
   - "Agentic Coding Best Practices" → `workflows/agentic-coding-practices.md`
   - "Agent Separation of Concerns" → `patterns/agent-separation.md`
   - "Progressive Disclosure" content → `patterns/progressive-disclosure.md`
   - "Tool Usage Best Practices" → `patterns/tool-usage-patterns.md`
   - "Examples" section → `examples/`
   - "Migration Checklist" → `workflows/migration-guide.md`
   - Decision flowcharts → `reference/decision-matrices.md`

3. **Update GUIDELINES.md**:
   - Replace extracted sections with compact summaries + links
   - Target: Under 1,000 lines

4. **Create/Update INDEX.md**:
   - Registry of all guideline documents
   - Quick lookup tables
   - Cross-references

### Extraction Template

When extracting a section:

```markdown
# {Section Title}

> Extracted from GUIDELINES.md for modularity. See [GUIDELINES.md](../GUIDELINES.md) for overview.

{Original content}

## Related
- [Link to related pattern]
- [Link to related example]
```

### Reference Link Template

Replace extracted content in GUIDELINES.md with:

```markdown
### {Section Title}

{2-3 sentence summary}

**Full details**: See [{filename}](guidelines/{folder}/{filename})
```

## Check Mode (`--check`)

Run validation checks:

```bash
# Size check
wc -l .claude/GUIDELINES.md
find .claude/guidelines -name "*.md" -exec wc -l {} \;

# Find potential duplication (repeated paragraphs)
# Look for common patterns mentioned multiple times

# Validate links
# Check all [](links) resolve to existing files
```

### Expected Structure

```
.claude/
├── GUIDELINES.md           # Core (under 1,000 lines)
├── guidelines/
│   ├── INDEX.md           # Navigation hub
│   ├── patterns/          # Design patterns
│   ├── standards/         # Rules & conventions
│   ├── examples/          # Good/bad examples
│   ├── workflows/         # How-to guides
│   └── reference/         # Lookup tables
├── SKILL-INDEX.md
├── CONTEXT-GRAPH.md
├── COMMAND-INDEX.md
└── AGENT-QUICK-REF.md
```

## Maintenance Rules

| Rule | Enforcement |
|------|-------------|
| GUIDELINES.md under 1,000 lines | Extract to guidelines/ |
| Any pattern doc under 400 lines | Split into sub-patterns |
| No duplication | Single source, reference elsewhere |
| New pattern = update INDEX.md | Keep registry current |
| Examples separate from principles | guidelines/examples/ folder |

## Arguments

`$ARGUMENTS` handling:

- No arguments or `--audit`: Run analysis mode
- `--apply`: Implement modular structure
- `--check`: Run validation checks only
