#!/usr/bin/env python3
"""
Command Initializer - Creates a new slash command from template

Usage:
    init_command.py <command-name> --path <path> [--template <type>] [--category <category>]

Templates:
    review      - Code review and analysis commands (default)
    generate    - Scaffolding and generation commands
    debug       - Error diagnosis and debugging commands
    workflow    - Multi-phase workflow commands
    git         - Git and PR automation commands
    refactor    - Code improvement commands

Categories (where to place the command):
    review/     - Code review workflows
    generate/   - Scaffolding and generation
    debug/      - Error diagnosis and debugging
    refactor/   - Code improvement and cleanup
    tdd/        - Test-driven development
    feature/    - Feature development workflows
    git/        - Git and PR workflows
    explain/    - Code explanation
    optimize/   - Performance and optimization
    team/       - Team collaboration

Examples:
    init_command.py code-review --path .claude/commands --category review
    init_command.py scaffold-module --path .claude/commands --template generate --category generate
    init_command.py smart-debug --path .claude/commands --template debug --category debug
    init_command.py pr-workflow --path .claude/commands --template git --category git
"""

import sys
import os
from pathlib import Path


# ==================== TEMPLATE DEFINITIONS ====================

COMMAND_TEMPLATE_REVIEW = """---
description: Review [TARGET] for quality, patterns, and best practices
allowed-tools: Read, Glob, Grep
argument-hint: [file-or-directory]
---

# {command_title} Command

Review code for quality, correctness, and adherence to best practices.

## Context

**Target**: $ARGUMENTS (defaults to current directory if not specified)

**Current status**: !`git status --short`

## Review Process

### Step 1: Understand Scope
- Identify files to review: !`git diff --name-only` or specified files
- Check recent changes: !`git log --oneline -5`

### Step 2: Analyze Code

Review each file for:

**Functionality**
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Error handling appropriate

**Quality**
- [ ] Readable and maintainable
- [ ] Follows project conventions
- [ ] No unnecessary complexity

**Security**
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] No injection vulnerabilities

**Testing**
- [ ] Tests exist for new code
- [ ] Tests are meaningful

### Step 3: Report Findings

**Output Format:**
```markdown
## Review: [Target]

### Summary
[1-2 sentence overview]

### Findings

#### Critical (Must Fix)
- [file:line] - [issue description]

#### Suggestions
- [file:line] - [improvement suggestion]

#### Positive Observations
- [What's done well]

### Verdict
[ ] Approve
[ ] Request Changes
```

## Options

- `--focus security` - Emphasize security review
- `--focus performance` - Emphasize performance analysis
- `--quick` - Quick scan, major issues only
"""

COMMAND_TEMPLATE_GENERATE = """---
description: Generate [ARTIFACT_TYPE] scaffolding with consistent patterns
allowed-tools: Read, Write, Glob, Grep
argument-hint: <name> [options]
---

# {command_title} Command

Generate code scaffolding with consistent patterns and structure.

## Usage

```
/{command_name} <name> [--option value]
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
"""

COMMAND_TEMPLATE_DEBUG = """---
description: Debug and diagnose [ISSUE_TYPE] with systematic analysis
allowed-tools: Read, Glob, Grep, Bash
argument-hint: <error-message-or-file>
---

# {command_title} Command

Systematically diagnose and fix errors with root cause analysis.

## Context

**Error/Issue**: $ARGUMENTS

**Current status**:
- Git status: !`git status --short`
- Recent changes: !`git log --oneline -3`

## Debugging Process

### Step 1: Reproduce & Understand

1. **Identify the error type:**
   - Compilation/build error
   - Runtime error
   - Test failure
   - Unexpected behavior

2. **Gather context:**
   - When does it occur?
   - Is it reproducible?
   - Recent changes that might be related

### Step 2: Analyze

1. **Locate the source:**
   - Stack trace analysis
   - Error message parsing
   - Related file identification

2. **Investigate root cause:**
   - Check recent changes in related files
   - Review dependencies
   - Look for similar issues in codebase

### Step 3: Diagnose

**Analysis checklist:**
- [ ] Error message understood
- [ ] Root cause identified
- [ ] Impact scope assessed
- [ ] Fix approach determined

### Step 4: Fix & Verify

1. **Apply fix:**
   - Make minimal necessary changes
   - Don't introduce new issues

2. **Verify:**
   - Run relevant tests: !`[test command]`
   - Build: !`[build command]`
   - Manual verification if needed

## Output Format

```markdown
## Debug Report: [Error Description]

### Error Analysis
- **Type**: [error type]
- **Location**: [file:line]
- **Message**: [error message]

### Root Cause
[Explanation of why the error occurred]

### Fix Applied
- **File**: [file path]
- **Change**: [description of change]

### Verification
- [ ] Tests passing
- [ ] Build successful
- [ ] Error no longer occurs

### Prevention
[How to prevent this in the future]
```

## Common Error Patterns

| Error Type | Common Causes | Investigation |
|------------|---------------|---------------|
| Null reference | Missing null checks | Check data flow |
| Type error | Mismatched types | Check interfaces |
| Import error | Missing dependency | Check package.json/csproj |
| Test failure | Logic error or stale test | Compare expected vs actual |
"""

COMMAND_TEMPLATE_WORKFLOW = """---
description: Execute [WORKFLOW_NAME] with phased approach
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <target> [--phase <n>]
---

# {command_title} Command

Multi-phase workflow with checkpoints and validation.

## Usage

```
/{command_name} <target> [options]
```

**Arguments:**
- `target`: What to apply the workflow to

**Options:**
- `--phase <n>`: Start from specific phase (1-4)
- `--dry-run`: Preview without making changes

## Context

**Target**: $ARGUMENTS
**Current status**: !`git status --short`

## Workflow Phases

### Phase 1: Assessment

**Objective**: Understand current state

**Actions:**
1. Analyze target scope
2. Identify affected areas
3. Create inventory of items

**Checkpoint:**
- [ ] Scope clearly defined
- [ ] All items inventoried
- [ ] Risks identified

---

### Phase 2: Planning

**Objective**: Design the approach

**Actions:**
1. Prioritize items
2. Determine order of operations
3. Identify dependencies

**Checkpoint:**
- [ ] Plan reviewed
- [ ] Dependencies mapped
- [ ] Rollback strategy defined

---

### Phase 3: Execution

**Objective**: Apply changes incrementally

**Actions:**
1. Apply changes in priority order
2. Verify each change
3. Document what changed

**Checkpoint:**
- [ ] All planned changes applied
- [ ] No regressions introduced
- [ ] Changes documented

---

### Phase 4: Validation

**Objective**: Verify results and document

**Actions:**
1. Run tests: !`[test command]`
2. Verify build: !`[build command]`
3. Document outcomes

**Checkpoint:**
- [ ] All tests passing
- [ ] Build successful
- [ ] Documentation updated

## Output Format

```markdown
## Workflow Summary: [Target]

### Phase Completion
- Phase 1 (Assessment): [Complete/Partial/Skipped]
- Phase 2 (Planning): [Complete/Partial/Skipped]
- Phase 3 (Execution): [Complete/Partial/Skipped]
- Phase 4 (Validation): [Complete/Partial/Skipped]

### Changes Applied
- [Change 1]
- [Change 2]

### Results
- Tests: [Pass/Fail]
- Build: [Pass/Fail]

### Follow-up Items
- [Item requiring attention]
```
"""

COMMAND_TEMPLATE_GIT = """---
description: Git workflow for [OPERATION] with safety checks
allowed-tools: Bash(git:*), Read, Glob
argument-hint: [branch-or-commit]
---

# {command_title} Command

Git workflow automation with safety checks and best practices.

## Context

**Current branch**: !`git branch --show-current`
**Status**: !`git status --short`
**Recent commits**: !`git log --oneline -5`

## Workflow

### Step 1: Pre-flight Checks

- [ ] Working directory clean (or changes stashed)
- [ ] On correct branch
- [ ] Remote is up to date: !`git fetch --dry-run`

### Step 2: Execute Operation

**Target**: $ARGUMENTS

[TODO: Add specific git operations for this command]

### Step 3: Verify

- [ ] Operation completed successfully
- [ ] No unintended changes
- [ ] History looks correct: !`git log --oneline -3`

## Safety Rules

1. **Never force push to main/master** without explicit confirmation
2. **Always verify** before destructive operations
3. **Create backup branch** before risky operations

## Common Operations

### Create Branch
```bash
git checkout -b feature/[name]
git push -u origin feature/[name]
```

### Commit Changes
```bash
git add [files]
git commit -m "type(scope): description"
```

### Create PR
```bash
gh pr create --title "[Title]" --body "[Description]"
```

## Output Format

```markdown
## Git Operation: [Operation Name]

### Before
- Branch: [branch name]
- Commit: [commit hash]

### Operation
[What was done]

### After
- Branch: [branch name]
- Commit: [commit hash]

### Next Steps
- [Recommended follow-up]
```
"""

COMMAND_TEMPLATE_REFACTOR = """---
description: Refactor [TARGET] for improved quality and maintainability
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: <file-or-pattern> [--type <refactor-type>]
---

# {command_title} Command

Systematic code refactoring with safety and verification.

## Usage

```
/{command_name} <target> [options]
```

**Arguments:**
- `target`: File, directory, or pattern to refactor

**Options:**
- `--type <type>`: Type of refactoring (rename, extract, simplify, cleanup)
- `--dry-run`: Preview changes without applying
- `--safe`: Extra verification steps

## Context

**Target**: $ARGUMENTS
**Current status**: !`git status --short`

## Refactoring Process

### Step 1: Analyze

1. **Identify refactoring opportunities:**
   - Code duplication
   - Complex methods
   - Poor naming
   - Unused code

2. **Assess impact:**
   - Files affected
   - Dependencies
   - Test coverage

### Step 2: Plan

1. **Prioritize changes:**
   - High impact, low risk first
   - Group related changes

2. **Define verification:**
   - Tests to run
   - Manual checks needed

### Step 3: Execute

For each refactoring:

1. **Make change:**
   - Apply single refactoring
   - Keep changes atomic

2. **Verify:**
   - Run tests: !`[test command]`
   - Build: !`[build command]`

3. **Commit:**
   - Commit with descriptive message
   - Reference the refactoring type

### Step 4: Review

- [ ] All planned refactorings applied
- [ ] No regressions introduced
- [ ] Code quality improved
- [ ] Tests still passing

## Refactoring Types

| Type | When to Use | Risk |
|------|-------------|------|
| Rename | Unclear names | Low |
| Extract Method | Long methods | Low |
| Extract Class | Large classes | Medium |
| Simplify | Complex conditionals | Medium |
| Remove Dead Code | Unused code | Low |

## Output Format

```markdown
## Refactoring Summary: [Target]

### Changes Applied
| File | Refactoring | Description |
|------|-------------|-------------|
| [file] | [type] | [what changed] |

### Metrics
- Files modified: [N]
- Lines changed: +[N]/-[N]
- Tests: [Pass/Fail]

### Quality Improvement
- [Specific improvement made]
```
"""

# Map template names to content
TEMPLATES = {
    'review': COMMAND_TEMPLATE_REVIEW,
    'generate': COMMAND_TEMPLATE_GENERATE,
    'debug': COMMAND_TEMPLATE_DEBUG,
    'workflow': COMMAND_TEMPLATE_WORKFLOW,
    'git': COMMAND_TEMPLATE_GIT,
    'refactor': COMMAND_TEMPLATE_REFACTOR,
}

# Valid categories for command placement
CATEGORIES = [
    'review',
    'generate',
    'debug',
    'refactor',
    'tdd',
    'feature',
    'git',
    'explain',
    'optimize',
    'team',
]

# Default category mapping for templates
TEMPLATE_DEFAULT_CATEGORY = {
    'review': 'review',
    'generate': 'generate',
    'debug': 'debug',
    'workflow': 'feature',
    'git': 'git',
    'refactor': 'refactor',
}


def title_case_command_name(command_name):
    """Convert hyphenated command name to Title Case for display."""
    return ' '.join(word.capitalize() for word in command_name.split('-'))


def init_command(command_name, path, template_type='review', category=None):
    """
    Initialize a new command file from template.

    Args:
        command_name: Name of the command (kebab-case)
        path: Path where the command file should be created
        template_type: Type of template to use
        category: Category folder (review, generate, etc.)

    Returns:
        Path to created command file, or None if error
    """
    # Validate template type
    if template_type not in TEMPLATES:
        print(f"Error: Unknown template type '{template_type}'")
        print(f"   Available templates: {', '.join(TEMPLATES.keys())}")
        return None

    # Determine category
    if category is None:
        category = TEMPLATE_DEFAULT_CATEGORY.get(template_type, 'feature')
    elif category not in CATEGORIES:
        print(f"Error: Unknown category '{category}'")
        print(f"   Available categories: {', '.join(CATEGORIES)}")
        return None

    # Determine command file path
    base_path = Path(path).resolve()
    category_path = base_path / category
    command_file = category_path / f"{command_name}.md"

    # Check if file already exists
    if command_file.exists():
        print(f"Error: Command file already exists: {command_file}")
        return None

    # Create category directory if needed
    try:
        category_path.mkdir(parents=True, exist_ok=True)
        print(f"Using category directory: {category_path}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    # Create command file from template
    command_title = title_case_command_name(command_name)
    template_content = TEMPLATES[template_type]
    command_content = template_content.format(
        command_name=command_name,
        command_title=command_title
    )

    try:
        command_file.write_text(command_content)
        print(f"Created command file: {command_file}")
    except Exception as e:
        print(f"Error creating command file: {e}")
        return None

    # Print next steps
    print(f"\nCommand '{command_name}' initialized successfully!")
    print(f"\nLocation: {command_file}")
    print(f"Category: {category}")
    print(f"Template: {template_type}")
    print("\nNext steps:")
    print("1. Edit the command file to customize the description and workflow")
    print("2. Replace [TARGET], [OPERATION], and other placeholders")
    print("3. Update the allowed-tools if needed")
    print(f"4. Test the command: '/{command_name} [arguments]'")

    return command_file


def main():
    if len(sys.argv) < 4 or '--path' not in sys.argv:
        print("Usage: init_command.py <command-name> --path <path> [--template <type>] [--category <cat>]")
        print("\nCommand name requirements:")
        print("  - Hyphen-case identifier (e.g., 'code-review')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Should describe the action")
        print("\nAvailable templates:")
        for name in TEMPLATES.keys():
            print(f"  - {name}")
        print("\nAvailable categories:")
        for cat in CATEGORIES:
            print(f"  - {cat}")
        print("\nExamples:")
        print("  init_command.py code-review --path .claude/commands")
        print("  init_command.py scaffold-module --path .claude/commands --template generate")
        print("  init_command.py smart-debug --path .claude/commands --template debug --category debug")
        print("  init_command.py pr-workflow --path .claude/commands --template git --category git")
        sys.exit(1)

    command_name = sys.argv[1]

    # Parse --path argument
    path_idx = sys.argv.index('--path')
    if path_idx + 1 >= len(sys.argv) or sys.argv[path_idx + 1].startswith('--'):
        print("Error: --path requires a value")
        sys.exit(1)
    path = sys.argv[path_idx + 1]

    # Parse optional --template argument
    template_type = 'review'
    if '--template' in sys.argv:
        template_idx = sys.argv.index('--template')
        if template_idx + 1 >= len(sys.argv) or sys.argv[template_idx + 1].startswith('--'):
            print("Error: --template requires a value")
            print(f"Available templates: {', '.join(TEMPLATES.keys())}")
            sys.exit(1)
        template_type = sys.argv[template_idx + 1]
        if template_type not in TEMPLATES:
            print(f"Error: Unknown template '{template_type}'")
            print(f"Available templates: {', '.join(TEMPLATES.keys())}")
            sys.exit(1)

    # Parse optional --category argument
    category = None
    if '--category' in sys.argv:
        category_idx = sys.argv.index('--category')
        if category_idx + 1 >= len(sys.argv) or sys.argv[category_idx + 1].startswith('--'):
            print("Error: --category requires a value")
            print(f"Available categories: {', '.join(CATEGORIES)}")
            sys.exit(1)
        category = sys.argv[category_idx + 1]
        if category not in CATEGORIES:
            print(f"Error: Unknown category '{category}'")
            print(f"Available categories: {', '.join(CATEGORIES)}")
            sys.exit(1)

    print(f"Initializing command: {command_name}")
    print(f"   Location: {path}")
    print(f"   Template: {template_type}")
    if category:
        print(f"   Category: {category}")
    print()

    result = init_command(command_name, path, template_type, category)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
