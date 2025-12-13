# Document Profiles

> Detailed profile definitions for markdown optimization. Each profile defines rules specific to a document type.

## Authoritative Limits

For Claude Code artifacts (`agent`, `skill`, `command`, `guidelines`), size limits are defined in [GUIDELINES.md](../../../GUIDELINES.md#size-limits). This file provides:
- **Detection patterns** - How to auto-detect profile from path
- **Optimization rules** - What to check and how to fix
- **Expected structure** - Recommended document organization

Limits here must match GUIDELINES.md. If they diverge, GUIDELINES.md is authoritative.

## Profile Detection

Profiles are auto-detected from file paths:

```
Path Pattern                    → Profile
─────────────────────────────────────────────
**/CLAUDE.md                   → claude-md
*.claude.md                    → claude-md
docs/architecture/**           → architecture
docs/domain/**                 → domain
docs/features/**               → feature-spec
**/README.md                   → readme
.claude/skills/**/SKILL.md     → skill
.claude/skills/**/*.md         → skill
.claude/agents/**/*.md         → agent
.claude/commands/**/*.md       → command
.claude/GUIDELINES.md          → guidelines
.claude/guidelines/**          → guidelines
**/*.md (default)              → generic
```

---

## Profile: `claude-md`

**Purpose**: Project context files for Claude Code.

### Constraints

| Rule | Value | Rationale |
|------|-------|-----------|
| Max lines | 300 | Always loaded, token cost |
| Max section | 50 | Quick scanning |
| Require TOC | No | Usually short enough |

### Expected Structure

```markdown
# CLAUDE.md

## Project Overview
[2-3 sentences max]

## Tech Stack
[Table format]

## Quick Reference
| Action | Command |
[Build, test, run commands]

## Conventions
[Tables, not prose]

## Key Files
[Bulleted list with paths]
```

### Optimization Rules

| Pattern | Action |
|---------|--------|
| Prose descriptions | Convert to tables |
| Long command explanations | Table with command + description |
| Entity lists > 20 items | Link to docs/domain/ |
| Embedded examples | Link to docs/ |
| Repeated from README | Remove, link to README |

### Anti-Patterns

- ❌ Full architecture documentation (move to docs/)
- ❌ Complete API reference (move to docs/)
- ❌ Long code examples (link instead)
- ❌ Changelog or history

---

## Profile: `architecture`

**Purpose**: System architecture and design documentation.

### Constraints

| Rule | Value | Rationale |
|------|-------|-----------|
| Max lines | 500 | Moderate detail |
| Max section | 150 | Readable chunks |
| Require TOC | Yes (>100 lines) | Navigation |

### Expected Structure

```markdown
# Architecture: {Component}

## Overview
[High-level summary]

## Diagrams
[Mermaid or links to images]

## Components
[Table or subsections]

## Data Flow
[Sequence diagrams or description]

## Decisions
[Links to ADRs]

## Related
[Links to other docs]
```

### Optimization Rules

| Pattern | Action |
|---------|--------|
| Large Mermaid diagrams | Extract to separate file or collapse |
| Inline ADR content | Link to docs/decisions/ |
| Repeated patterns | Reference shared pattern doc |
| Implementation details | Move to code comments or separate doc |

---

## Profile: `domain`

**Purpose**: Business domain documentation (entities, rules, permissions).

### Constraints

| Rule | Value | Rationale |
|------|-------|-----------|
| Max lines | 400 | Focused documents |
| Max section | 100 | Scannable |
| Require TOC | Yes (>80 lines) | Quick lookup |

### Expected Structure

```markdown
# {Domain Concept}

## Overview
[Brief description]

## Entities
| Entity | Key Fields | Description |
[Table format]

## Business Rules
- BR-001: [Rule description]
- BR-002: [Rule description]

## Permissions
| Permission | Role | Description |
[Matrix format]
```

### Optimization Rules

| Pattern | Action |
|---------|--------|
| Entity prose descriptions | Convert to table |
| Unnumbered business rules | Add BR-XXX identifiers |
| Permission prose | Convert to matrix |
| Example scenarios | Move to separate examples file |

---

## Profile: `feature-spec`

**Purpose**: Feature specifications and requirements.

### Constraints

| Rule | Value | Rationale |
|------|-------|-----------|
| Max lines | 600 | Complex features |
| Max section | 150 | Manageable sections |
| Require TOC | Yes | Multi-section navigation |

### Expected Structure

```markdown
# Feature: {Name}

## Overview
## Requirements
### Functional
### Non-Functional
## User Stories
## Technical Design
## API Contracts
## Test Cases
## Acceptance Criteria
```

### Optimization Rules

| Pattern | Action |
|---------|--------|
| Mixed requirements/design | Split into sections |
| Inline test code | Link to test files |
| Full API examples | Summarize, link to spec |
| Long acceptance criteria | Checkboxes, concise |

---

## Profile: `readme`

**Purpose**: Project/folder entry points.

### Constraints

| Rule | Value | Rationale |
|------|-------|-----------|
| Max lines | 200 | Quick orientation |
| Max section | 50 | Scannable |
| Require TOC | No | Short enough |

### Expected Structure

```markdown
# {Project/Component}

## Overview
[1-2 paragraphs max]

## Quick Start
[Minimal steps to get running]

## Documentation
[Links to detailed docs]

## Contributing
[Brief or link]
```

### Optimization Rules

| Pattern | Action |
|---------|--------|
| Full documentation inline | Move to docs/, link |
| Long prerequisites | Summarize, link to setup guide |
| Complete API reference | Link to API docs |
| Changelog inline | Move to CHANGELOG.md |

---

## Profile: `skill`

**Purpose**: Claude Code skill definitions.

### Constraints

> **Limits**: See [GUIDELINES.md § Skills](../../../GUIDELINES.md#skills) for authoritative limits (500 lines).

| Rule | Rationale |
|------|-----------|
| Max section: 100 lines | Focused content |
| Require TOC: No | References handle depth |

### Expected Structure

```markdown
# Skill Name

## Quick Start
[Immediate value - 20-30 lines]

## Core Patterns
[Essential patterns - 100-200 lines]

## Advanced Topics
**Topic A**: See [topic-a.md](references/topic-a.md)
```

### Optimization Rules

| Pattern | Action |
|---------|--------|
| Advanced content inline | Extract to references/ |
| Verbose explanations | Claude knows this, remove |
| Large code examples | Condense or extract |
| Multiple similar examples | One example + variations |

---

## Profile: `agent`

**Purpose**: Claude Code agent definitions.

### Constraints

> **Limits**: See [GUIDELINES.md § Agents](../../../GUIDELINES.md#agents) for authoritative limits (150 lines).

| Rule | Rationale |
|------|-----------|
| Max section: 30 lines | Very concise |
| Require TOC: No | Too short |

### Expected Structure

```markdown
---
[YAML frontmatter]
---

You are a [role].

## Project Context
[What to read]

## Responsibilities
[Bulleted list]

## Constraints
[Concise rules]
```

### Optimization Rules

| Pattern | Action |
|---------|--------|
| Code templates | Extract to skill |
| CLI commands | Extract to command |
| Long explanations | Reference skill |
| Hardcoded paths | Use placeholders |

---

## Profile: `command`

**Purpose**: Claude Code command definitions.

### Constraints

> **Limits**: See [GUIDELINES.md § Commands](../../../GUIDELINES.md#commands) for authoritative format (200 lines recommended).

| Rule | Rationale |
|------|-----------|
| Max section: 50 lines | Clear steps |
| Require TOC: No | Usually short |

### Optimization Rules

| Pattern | Action |
|---------|--------|
| Domain knowledge | Reference skill |
| Complex workflows | Consider agent instead |
| Repeated patterns | Use command references |

---

## Profile: `guidelines`

**Purpose**: Claude Code organization guidelines ecosystem (GUIDELINES.md + modular guidelines/).

### Constraints

> **Limits**: See [GUIDELINES.md § Size Limits](../../../GUIDELINES.md#size-limits) for authoritative limits.

| Document | Rationale |
|----------|-----------|
| GUIDELINES.md: 1,000 | Core reference, always loaded by artifact creator |
| INDEX.md: 200 | Navigation hub only |
| Sub-documents: 400-500 | Focused deep-dives |

### Expected Structure

```
.claude/
├── GUIDELINES.md           # Core (entry point)
└── guidelines/
    ├── INDEX.md           # Navigation hub
    ├── patterns/          # Design patterns
    ├── standards/         # Rules & conventions
    ├── examples/          # Good/bad examples
    ├── workflows/         # How-to guides
    └── reference/         # Lookup tables
```

### Additional Validation

Beyond standard checks, the `guidelines` profile validates:

| Check | Description |
|-------|-------------|
| **INDEX.md completeness** | All files in `guidelines/` listed in INDEX.md |
| **Cross-references** | Links between GUIDELINES.md ↔ guidelines/ valid |
| **Folder structure** | Required folders exist |
| **Orphan detection** | Files not linked from GUIDELINES.md or INDEX.md |

### Optimization Rules

| Pattern | Action |
|---------|--------|
| GUIDELINES.md > 1,000 lines | Extract section to guidelines/ |
| Section > 200 lines | Split into sub-document |
| Concept in 2+ places | Consolidate to single location |
| Missing from INDEX.md | Add entry or delete orphan |
| Inline examples > 20 lines | Move to examples/ |

### Anti-Patterns

- ❌ Embedding full examples in GUIDELINES.md (link instead)
- ❌ Duplicating content between GUIDELINES.md and guidelines/
- ❌ Deep nesting in guidelines/ (max 1 level)
- ❌ Files not linked from anywhere (orphans)

---

## Profile: `generic`

**Purpose**: Default for unclassified markdown.

### Constraints

| Rule | Value | Rationale |
|------|-------|-----------|
| Max lines | 500 | Reasonable default |
| Max section | 150 | Readable |
| Require TOC | Yes (>100 lines) | Navigation |

### General Rules

Apply universal optimization:
- Convert prose to tables where possible
- Extract large code blocks
- Add TOC for long files
- Fix heading hierarchy
- Remove duplication

---

## Custom Profile Schema

Define in `.claude/config/md-profiles.yaml`:

```yaml
profiles:
  {profile-name}:
    # Path patterns for auto-detection
    patterns:
      - "glob/pattern/**"
      - "another/pattern/*.md"

    # Size constraints
    max_lines: 500
    max_section_lines: 150

    # Structure rules
    rules:
      require_toc: true          # Require table of contents
      require_toc_threshold: 100 # Only if > N lines
      require_frontmatter: false # YAML frontmatter required
      max_heading_depth: 4       # h1-h4 only
      require_overview: true     # Must have overview section

    # Compaction preferences
    compaction:
      prose_to_table: true       # Suggest table conversions
      extract_examples: true     # Suggest example extraction
      extract_threshold: 30      # Extract code blocks > N lines

    # Expected sections (optional)
    expected_sections:
      - "Overview"
      - "Quick Start"
      - "Related"
```

## Profile Precedence

When multiple profiles match:

1. **Explicit** (`--profile X`) - Highest priority
2. **Custom** (from config file) - Second priority
3. **Built-in specific** (e.g., `claude-md`) - Third
4. **Built-in generic** - Default fallback
