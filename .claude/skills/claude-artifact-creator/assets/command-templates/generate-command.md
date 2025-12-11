---
description: Generate [ARTIFACT_TYPE] scaffolding with consistent patterns
allowed-tools: Read, Write, Glob, Grep
argument-hint: <name> [options]
---

# {Command Title}

Generate code scaffolding with consistent patterns and structure.

## Usage

```
/{command-name} <name> [--option value]
```

**Arguments:**
- `name`: Name of the artifact to generate (PascalCase or kebab-case)

**Options:**
- `--type <type>`: Type of artifact (default: [DEFAULT_TYPE])
- `--with-tests`: Include test files
- `--with-docs`: Include documentation

## Context

**Current directory**: !`pwd`
**Existing patterns**: !`ls -la` (check existing structure)

## Generation Process

### Step 1: Gather Information

From $ARGUMENTS, extract:
- Name: [Will be converted to appropriate case]
- Type: [default or specified]
- Options: [tests, docs, etc.]

### Step 2: Check Existing Patterns

Before generating, review existing code for patterns:
- File naming conventions
- Directory structure
- Code style

### Step 3: Generate Files

**Files to create:**
1. `[path]/[Name].[ext]` - Primary file
2. `[path]/[Name].test.[ext]` - Test file (if --with-tests)
3. `[path]/[Name].md` - Documentation (if --with-docs)

### Step 4: Post-Generation

- [ ] Files created in correct locations
- [ ] Naming conventions followed
- [ ] No conflicts with existing files

## Templates

### Primary File Template
```
// [TODO: Add template content]
```

### Test File Template
```
// [TODO: Add test template]
```

## Output

After generation, display:
- List of created files
- Next steps for the user
- Any manual steps required
