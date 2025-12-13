# Context Efficiency Patterns

> Extracted from GUIDELINES.md for modularity. Strategies for optimal context window usage.

## Core Principle

**The context window is a shared resource.** Every token should justify its presence.

## Context Budget Philosophy

| Question | If No... |
|----------|----------|
| "Does Claude really need this explanation?" | Remove it |
| "Can I assume Claude knows this?" | Don't explain |
| "Does this paragraph justify its token cost?" | Condense it |

**Default assumption**: Claude is already very smart. Only add context Claude doesn't already have.

## Tiered Knowledge Discovery

Select the appropriate tier based on task complexity:

| Tier | Task Complexity | Files Read | Time |
|------|-----------------|------------|------|
| **SKIP** | Simple (typo, comment, single-line edit) | 0 | ~0s |
| **QUICK** | Single-skill (write tests, add validation) | 0 (use CLAUDE.md ref) | ~2s |
| **STANDARD** | Multi-skill (API design, debug complex error) | 2 (INDEX + GRAPH) | ~10s |
| **DEEP** | Full implementation (CRUD, new feature) | 4+ (full protocol) | ~15-20s |

### Tier Selection Flowchart

```
START: What's the task?
│
├─ Single file, obvious change? → SKIP
│
├─ One pattern/skill needed? → QUICK (use CLAUDE.md inline reference)
│
├─ Multiple skills or unfamiliar? → STANDARD (read SKILL-INDEX + CONTEXT-GRAPH)
│
└─ Full feature/CRUD workflow? → DEEP (full 4-step protocol)
```

**Key**: Don't over-discover. A typo fix doesn't need knowledge discovery.

## File Size Limits

| File Type | Max Lines | If Exceeded |
|-----------|-----------|-------------|
| GUIDELINES.md | 1,000 | Extract to guidelines/ |
| SKILL.md | 500 | Extract to references/ |
| Agent prompt | 150 | Extract to skills/commands |
| Reference doc | 400 | Split into sub-docs |

## Writing Concise Content

### Before (Verbose - 8 lines)

```markdown
PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but we
recommend pdfplumber because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below
to extract text from your PDF file.
```

### After (Concise - 3 lines)

```markdown
## Extract PDF Text

Use pdfplumber for text extraction:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

## Degrees of Freedom

Match specificity to task fragility:

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** (text instructions) | Multiple valid approaches | "Analyze code structure, check for bugs" |
| **Medium** (pseudocode/params) | Preferred pattern exists | Template with customizable parameters |
| **Low** (exact scripts) | Fragile, error-prone operations | "Run exactly: `python migrate.py --verify`" |

## Context Preservation Techniques

| Technique | How | Benefit |
|-----------|-----|---------|
| **Mention files directly** | Tab-complete to reference | Loads only mentioned files |
| **Use `/clear` frequently** | Reset context between tasks | Prevents degradation |
| **Progressive disclosure** | Load SKILL.md → references on-demand | Minimizes initial load |
| **Subagent delegation** | Isolate context-heavy tasks | Main thread stays lean |

## Subagent Usage for Context Isolation

Use subagents for:
- **Parallelization**: Multiple subagents handle different tasks simultaneously
- **Context isolation**: Each operates in its own context window
- **Information-heavy tasks**: Where most data proves irrelevant to main thread

```
Main Thread (lean)
│
├─ Subagent A: Research task (isolated context)
├─ Subagent B: Code review (isolated context)
└─ Subagent C: Testing (isolated context)
│
▼
Summaries return to main thread (minimal context)
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Loading all skills at startup | Wastes context | Progressive disclosure |
| Long explanations of common concepts | Claude already knows | Remove or condense |
| Duplicated content across files | Multiplies context cost | Single source, reference |
| Everything in one large file | Must load all or nothing | Modular structure |
| Verbose examples | Token-heavy | Concise, focused examples |

## Measurement

```bash
# Check file sizes
wc -l .claude/GUIDELINES.md
wc -l .claude/skills/*/SKILL.md
wc -l .claude/agents/**/*.md

# Find over-limit files
find .claude -name "*.md" -exec sh -c 'lines=$(wc -l < "$1"); [ "$lines" -gt 500 ] && echo "$1: $lines lines"' _ {} \;
```

## Related

- [Progressive Disclosure](progressive-disclosure.md) - Three-level loading
- [Tool Usage Patterns](tool-usage-patterns.md) - Efficient tool selection
- [GUIDELINES.md](../../GUIDELINES.md#knowledge-architecture) - Overview
