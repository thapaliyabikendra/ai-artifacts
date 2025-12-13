# Tool Usage Patterns

> Extracted from GUIDELINES.md for modularity. Core patterns for context-efficient tool usage.

## Core Principle

**Minimize context usage through targeted operations.** Use the most specific tool for the job.

## Tool Selection Matrix

| Need | Use | Instead Of |
|------|-----|------------|
| Search for patterns | **Grep** | Reading entire files |
| Find files by name | **Glob** | `ls` or `find` via Bash |
| Make targeted edits | **Edit** | Rewriting with Write |
| Read specific sections | **Read** with offset/limit | Reading entire large files |
| Create new files | **Write** | N/A |
| Execute commands | **Bash** | N/A |

## Efficiency Guidelines

### 1. Search Before Read

```
BAD:  Read entire file → Search for function
GOOD: Grep for function name → Read only relevant section
```

### 2. Pattern Match First

```
BAD:  List directory → Filter manually
GOOD: Glob with pattern → Get exact matches
```

### 3. Targeted Edits

```
BAD:  Read file → Modify in memory → Write entire file
GOOD: Read file → Use Edit for specific changes
```

### 4. Parallel Operations

```
BAD:  Read file A → Read file B → Read file C (sequential)
GOOD: Read files A, B, C simultaneously (parallel)
```

### 5. Limit Scope

```
BAD:  Read 10,000 line file entirely
GOOD: Read with offset=500, limit=200 for relevant section
```

## Tool Permission Strategy

**Principle**: Least privilege - only grant necessary tools.

| Agent Type | Recommended Tools | Rationale |
|------------|-------------------|-----------|
| **Read-only** (reviewers, auditors) | `Read, Grep, Glob` | Cannot modify code |
| **Research** | `Read, Grep, Glob, WebFetch, WebSearch` | Information gathering |
| **Code writers** | `Read, Write, Edit, Bash, Glob, Grep` | Full implementation |
| **Documentation** | `Read, Write, Edit, Glob, Grep, WebFetch, WebSearch` | Content creation |

**Warning**: Omitting the `tools` field grants access to **all available tools** (including MCP). Always whitelist intentionally.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Reading entire files to find one function | Wastes context | Use Grep first |
| Using Write to change a single line | Overwrites file, loses history | Use Edit |
| Sequential reads that could be parallelized | Slow, inefficient | Parallel tool calls |
| Broad directory scans | Returns too much | Targeted glob patterns |
| Using Bash for file operations | Less efficient, harder to audit | Use Read/Write/Edit |

## Tool-Specific Tips

### Grep
```bash
# Search for pattern, get file list
Grep pattern="class.*Repository" output_mode="files_with_matches"

# Search with context lines
Grep pattern="async.*Task" -C=3 output_mode="content"

# Case-insensitive search
Grep pattern="error" -i=true
```

### Glob
```bash
# Find all TypeScript files
Glob pattern="**/*.ts"

# Find specific config files
Glob pattern="**/tsconfig*.json"

# Find in specific directory
Glob pattern="src/components/**/*.tsx"
```

### Read
```bash
# Read specific section of large file
Read file_path="/path/to/file" offset=100 limit=50

# Read entire small file
Read file_path="/path/to/small/file"
```

### Edit
```bash
# Replace specific string
Edit file_path="/path/to/file" old_string="oldValue" new_string="newValue"

# Replace all occurrences
Edit file_path="/path/to/file" old_string="old" new_string="new" replace_all=true
```

## Decision Flowchart

```
What do you need to do?
│
├─ Find files by name/pattern? → Glob
│
├─ Search file contents? → Grep
│
├─ Read file contents?
│   ├─ Small file (<500 lines)? → Read (full)
│   └─ Large file? → Grep to locate, then Read with offset/limit
│
├─ Modify existing file?
│   ├─ Single/few changes? → Edit
│   └─ Complete rewrite? → Write
│
├─ Create new file? → Write
│
└─ Execute system command? → Bash
```

## Related

- [Context Efficiency](context-efficiency.md) - Overall context strategies
- [Tool Permissions Reference](../reference/tool-permissions.md) - Full permissions list
- [GUIDELINES.md](../../GUIDELINES.md#tool-usage-best-practices) - Overview
