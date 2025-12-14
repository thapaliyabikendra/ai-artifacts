# AI Artifacts - Plugin Export Plan

**Status:** Draft
**Author:** Claude
**Date:** 2025-12-15
**Version:** 1.0

---

## Executive Summary

Export the Claude Code artifacts (agents, skills, commands) from this repository into a standalone, distributable Git repository called `ai-artifacts`. This enables team-wide adoption across ABP Framework projects with multiple installation methods.

---

## Table of Contents

1. [Goals & Non-Goals](#goals--non-goals)
2. [Package Structure](#package-structure)
3. [Installation Methods](#installation-methods)
4. [Install Script Design](#install-script-design)
5. [Conflict Resolution Strategy](#conflict-resolution-strategy)
6. [CLAUDE.md Integration](#claudemd-integration)
7. [Settings Management](#settings-management)
8. [Versioning Strategy](#versioning-strategy)
9. [Implementation Phases](#implementation-phases)
10. [Usage Examples](#usage-examples)
11. [Maintenance Guide](#maintenance-guide)

---

## Goals & Non-Goals

### Goals

| Goal | Description |
|------|-------------|
| **Portability** | Artifacts work in any ABP Framework project |
| **Multiple Install Methods** | Support git clone, curl, submodule, and manual copy |
| **Non-Destructive** | Never overwrite existing user customizations without consent |
| **Easy Updates** | Simple mechanism to pull new versions |
| **Self-Contained** | No external dependencies except Node.js (for CLI) |

### Non-Goals

- NPM registry publication (GitHub-only distribution)
- Separation into multiple packages (single ABP-focused bundle)
- GUI installer (CLI and scripts only)
- Automatic project detection (explicit target path required)

---

## Package Structure

```
ai-artifacts/
├── .claude/                        # Core artifacts (copied to target)
│   ├── agents/
│   │   ├── architects/
│   │   │   ├── backend-architect.md
│   │   │   └── business-analyst.md
│   │   ├── engineers/
│   │   │   ├── abp-developer.md
│   │   │   ├── react-developer.md
│   │   │   └── devops-engineer.md
│   │   ├── reviewers/
│   │   │   ├── abp-code-reviewer.md
│   │   │   ├── react-code-reviewer.md
│   │   │   ├── qa-engineer.md
│   │   │   ├── security-engineer.md
│   │   │   └── assets/
│   │   └── specialists/
│   │       ├── debugger.md
│   │       └── database-migrator.md
│   ├── skills/                     # 47 skills organized by category
│   │   ├── abp-framework-patterns/
│   │   ├── efcore-patterns/
│   │   ├── fluentvalidation-patterns/
│   │   └── ... (all other skills)
│   ├── commands/                   # 27 commands organized by domain
│   │   ├── arch/
│   │   ├── ba/
│   │   ├── debug/
│   │   ├── docs/
│   │   ├── feature/
│   │   ├── generate/
│   │   ├── qa/
│   │   ├── refactor/
│   │   ├── review/
│   │   ├── tdd/
│   │   ├── team/
│   │   └── references/
│   ├── knowledge/                  # Knowledge base
│   ├── guidelines/                 # Guidelines and best practices
│   ├── flows/                      # Workflow documentation
│   ├── templates/                  # QMD templates
│   ├── AGENT-INDEX.md
│   ├── AGENT-QUICK-REF.md
│   ├── SKILL-INDEX.md
│   ├── SKILL-QUICK-REF.md
│   ├── COMMAND-INDEX.md
│   ├── CONTEXT-GRAPH.md
│   ├── GUIDELINES.md
│   └── ARTIFACT-KNOWLEDGE-MATRIX.md
│
├── bin/
│   └── claude-abp.js              # CLI installer (Node.js)
│
├── scripts/
│   ├── install.sh                 # Bash installer (Unix/macOS/WSL)
│   ├── install.ps1                # PowerShell installer (Windows)
│   └── utils.sh                   # Shared utility functions
│
├── fragments/
│   ├── claude-md-header.md        # Header to inject into target CLAUDE.md
│   ├── claude-md-agents.md        # Agent reference section
│   ├── claude-md-skills.md        # Skill reference section
│   ├── claude-md-commands.md      # Command reference section
│   └── settings-defaults.json     # Default settings to merge
│
├── CHANGELOG.md                   # Version history
├── LICENSE                        # License file
├── README.md                      # Main documentation
├── VERSION                        # Current version (e.g., "1.0.0")
└── package.json                   # For npx execution support
```

### Directory Breakdown

| Directory | Contents | Size Estimate |
|-----------|----------|---------------|
| `.claude/agents/` | 11 agents + 2 templates | ~50 KB |
| `.claude/skills/` | 47 skill directories with references | ~500 KB |
| `.claude/commands/` | 27 commands + references | ~100 KB |
| `.claude/knowledge/` | 35+ knowledge files | ~150 KB |
| `.claude/guidelines/` | 18 guideline files | ~100 KB |
| **Total** | All artifacts | ~1 MB |

---

## Installation Methods

### Method 1: Git Clone + Install Script (Recommended)

```bash
# Clone the toolkit
git clone git@github.com:thapaliyabikendra/ai-artifacts.git

# Run installer
cd ai-artifacts
./scripts/install.sh /path/to/your/project

# Or on Windows (PowerShell)
.\scripts\install.ps1 -TargetPath "C:\Projects\your-project"
```

### Method 2: One-Line Install (curl/wget)

```bash
# Unix/macOS/WSL
curl -sSL https://raw.githubusercontent.com/thapaliyabikendra/ai-artifacts/main/scripts/install.sh | bash -s -- /path/to/project

# Or with wget
wget -qO- https://raw.githubusercontent.com/thapaliyabikendra/ai-artifacts/main/scripts/install.sh | bash -s -- /path/to/project
```

### Method 3: npx (No Clone Required)

```bash
# Install to current directory
npx github:thapaliyabikendra/ai-artifacts install .

# Install to specific path
npx github:thapaliyabikendra/ai-artifacts install /path/to/project
```

### Method 4: Git Submodule

```bash
# Add as submodule
git submodule add git@github.com:thapaliyabikendra/ai-artifacts.git .claude-toolkit

# Run setup to symlink/copy artifacts
./.claude-toolkit/scripts/install.sh --from-submodule
```

### Method 5: Manual Copy

1. Download/clone the repository
2. Copy `.claude/` directory to your project root
3. Manually add references to your `CLAUDE.md`
4. Merge settings from `fragments/settings-defaults.json`

---

## Install Script Design

### CLI Interface

```bash
claude-abp <command> [options]

Commands:
  install <target>     Install toolkit to target project
  update               Update existing installation
  list                 List installed artifacts
  uninstall            Remove toolkit from project
  diff                 Show differences from source

Options:
  --dry-run            Show what would be done without making changes
  --force              Overwrite existing files without prompting
  --skip-conflicts     Skip files that already exist
  --no-backup          Don't create backups of modified files
  --components <list>  Install specific components (agents,skills,commands)
  --verbose            Show detailed output
  --quiet              Suppress non-error output
```

### Installation Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INSTALLATION FLOW                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. VALIDATE TARGET                                                 │
│     ├── Check target path exists                                    │
│     ├── Check write permissions                                     │
│     └── Detect existing .claude/ directory                          │
│                                                                     │
│  2. ANALYZE CONFLICTS                                               │
│     ├── Compare source vs target files                              │
│     ├── Identify new, modified, and unchanged files                 │
│     └── Build conflict resolution plan                              │
│                                                                     │
│  3. PROMPT USER (if conflicts exist)                                │
│     ├── Show conflict summary                                       │
│     ├── Offer: merge / overwrite / skip / abort                     │
│     └── Allow per-file decisions or bulk                            │
│                                                                     │
│  4. CREATE BACKUP                                                   │
│     ├── Backup existing .claude/ to .claude.backup.{timestamp}      │
│     └── Backup CLAUDE.md if it exists                               │
│                                                                     │
│  5. COPY ARTIFACTS                                                  │
│     ├── Copy .claude/ directory structure                           │
│     ├── Apply conflict resolutions                                  │
│     └── Set appropriate file permissions                            │
│                                                                     │
│  6. INTEGRATE CLAUDE.MD                                             │
│     ├── If no CLAUDE.md: copy template                              │
│     ├── If exists: inject toolkit sections                          │
│     └── Preserve user's custom content                              │
│                                                                     │
│  7. MERGE SETTINGS                                                  │
│     ├── Load existing settings.json (if any)                        │
│     ├── Merge toolkit defaults (don't overwrite user values)        │
│     └── Write merged settings.json                                  │
│                                                                     │
│  8. VERIFY & REPORT                                                 │
│     ├── Verify all files copied correctly                           │
│     ├── Show installation summary                                   │
│     └── Suggest next steps                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Node.js CLI Implementation Outline

```javascript
// bin/claude-abp.js
#!/usr/bin/env node

const { program } = require('commander');
const Installer = require('../src/installer');

program
  .name('claude-abp')
  .description('AI Artifacts Installer')
  .version(require('../package.json').version);

program
  .command('install <target>')
  .description('Install toolkit to target project')
  .option('--dry-run', 'Show what would be done')
  .option('--force', 'Overwrite without prompting')
  .option('--skip-conflicts', 'Skip existing files')
  .option('--components <list>', 'Specific components to install')
  .action(async (target, options) => {
    const installer = new Installer(target, options);
    await installer.install();
  });

program
  .command('update')
  .description('Update existing installation')
  .option('--check', 'Check for updates without installing')
  .action(async (options) => {
    const installer = new Installer(process.cwd(), options);
    await installer.update();
  });

program.parse();
```

---

## Conflict Resolution Strategy

### Conflict Types

| Type | Description | Default Resolution |
|------|-------------|-------------------|
| **New File** | File doesn't exist in target | Copy |
| **Identical** | File exists and matches source | Skip |
| **Modified** | File exists but differs | Prompt user |
| **Deleted** | File in target not in source | Preserve |

### Resolution Options

```
Conflict detected: .claude/skills/efcore-patterns/SKILL.md

Source (toolkit):  v1.2.0 - Updated migration patterns
Target (project):  Modified by user on 2025-12-10

Choose resolution:
  [o] Overwrite with toolkit version
  [k] Keep current project version
  [m] Merge (open diff editor)
  [b] Backup current, then overwrite
  [d] Show diff
  [a] Apply this choice to all remaining conflicts
  [q] Abort installation

> _
```

### Merge Strategy for Specific Files

| File | Merge Strategy |
|------|----------------|
| `CLAUDE.md` | Section-based injection (preserve user sections) |
| `settings.json` | Deep merge (toolkit defaults + user overrides) |
| `*.md` (skills/agents) | Replace entirely (user customizations not expected) |
| Index files | Regenerate from installed artifacts |

---

## CLAUDE.md Integration

### Injection Strategy

The installer injects toolkit references into the target's `CLAUDE.md` using clearly marked sections:

```markdown
<!-- ai-artifacts:START -->
## AI Artifacts

**Installed:** v1.0.0 | **Updated:** 2025-12-15

### Quick Reference

[Content from fragments/claude-md-header.md]

### Available Agents
[Content from fragments/claude-md-agents.md]

### Available Skills
[Content from fragments/claude-md-skills.md]

### Available Commands
[Content from fragments/claude-md-commands.md]
<!-- ai-artifacts:END -->
```

### Update Behavior

- On **install**: Inject section if not present
- On **update**: Replace content between markers, preserve user content outside
- On **uninstall**: Remove section between markers

### User CLAUDE.md Preservation

```markdown
# My Project CLAUDE.md

## Project-Specific Instructions
[User's custom content - PRESERVED]

<!-- ai-artifacts:START -->
[Toolkit content - MANAGED BY INSTALLER]
<!-- ai-artifacts:END -->

## Additional Notes
[User's custom content - PRESERVED]
```

---

## Settings Management

### Default Settings Fragment

```json
// fragments/settings-defaults.json
{
  "permissions": {
    "allow": [
      "Bash(dotnet:*)",
      "Bash(git:*)",
      "Bash(npm:*)"
    ]
  },
  "hooks": {
    "preToolUse": []
  },
  "outputStyle": "careful"
}
```

### Merge Algorithm

```javascript
function mergeSettings(target, source) {
  // Deep merge with target taking precedence
  // Array fields are concatenated and deduplicated
  // Object fields are recursively merged
  // Primitive fields: target wins if defined
}
```

### Example Merge

```json
// Target (user's existing settings.json)
{
  "permissions": {
    "allow": ["Bash(docker:*)"]
  },
  "outputStyle": "concise"
}

// Source (toolkit defaults)
{
  "permissions": {
    "allow": ["Bash(dotnet:*)", "Bash(git:*)"]
  },
  "outputStyle": "careful"
}

// Result (merged)
{
  "permissions": {
    "allow": ["Bash(docker:*)", "Bash(dotnet:*)", "Bash(git:*)"]  // Combined
  },
  "outputStyle": "concise"  // User's value preserved
}
```

---

## Versioning Strategy

### Version File

```
VERSION
1.0.0
```

### Changelog Format

```markdown
# Changelog

## [1.1.0] - 2025-01-15

### Added
- New `grpc-integration-patterns` skill
- `/generate:grpc-client` command

### Changed
- Updated `abp-framework-patterns` for ABP 10.1
- Improved `backend-architect` agent prompts

### Fixed
- EF Core migration command path detection

## [1.0.0] - 2025-12-15

### Added
- Initial release with 11 agents, 47 skills, 27 commands
```

### Update Detection

```bash
# Check for updates
claude-abp update --check

# Output:
# Current: 1.0.0
# Latest:  1.1.0
#
# Changes in 1.1.0:
# - Added: grpc-integration-patterns skill
# - Added: /generate:grpc-client command
# - Updated: abp-framework-patterns skill
#
# Run 'claude-abp update' to install
```

### Installation Manifest

Created at `.claude/.toolkit-manifest.json`:

```json
{
  "toolkit": "ai-artifacts",
  "version": "1.0.0",
  "installedAt": "2025-12-15T10:30:00Z",
  "updatedAt": "2025-12-15T10:30:00Z",
  "source": "git@github.com:thapaliyabikendra/ai-artifacts.git",
  "components": {
    "agents": 11,
    "skills": 47,
    "commands": 27
  },
  "customizations": []
}
```

---

## Implementation Phases

### Phase 1: Foundation (Day 1-2)

| Task | Description | Deliverable |
|------|-------------|-------------|
| **1.1** | Create new repository structure | Empty `ai-artifacts/` repo |
| **1.2** | Export `.claude/` artifacts | Copied and organized artifacts |
| **1.3** | Create `package.json` | NPM manifest for npx support |
| **1.4** | Create `VERSION` and `CHANGELOG.md` | Version tracking files |

### Phase 2: CLI Installer (Day 3-5)

| Task | Description | Deliverable |
|------|-------------|-------------|
| **2.1** | Implement core `Installer` class | `src/installer.js` |
| **2.2** | Implement `install` command | File copy + conflict detection |
| **2.3** | Implement `update` command | Version comparison + selective update |
| **2.4** | Implement `list` and `uninstall` | Utility commands |
| **2.5** | Add `--dry-run` support | Preview mode |

### Phase 3: Integration Logic (Day 6-7)

| Task | Description | Deliverable |
|------|-------------|-------------|
| **3.1** | CLAUDE.md section injection | `src/claude-md-integrator.js` |
| **3.2** | Settings.json deep merge | `src/settings-merger.js` |
| **3.3** | Manifest management | `.toolkit-manifest.json` handling |
| **3.4** | Backup/restore functionality | Rollback support |

### Phase 4: Shell Scripts (Day 8)

| Task | Description | Deliverable |
|------|-------------|-------------|
| **4.1** | Bash installer script | `scripts/install.sh` |
| **4.2** | PowerShell installer script | `scripts/install.ps1` |
| **4.3** | One-liner install support | curl/wget compatibility |

### Phase 5: Documentation & Testing (Day 9-10)

| Task | Description | Deliverable |
|------|-------------|-------------|
| **5.1** | Write comprehensive README | Installation + usage guide |
| **5.2** | Add usage examples | Common scenarios |
| **5.3** | Test all installation methods | Verified install paths |
| **5.4** | Test conflict scenarios | Edge case handling |

---

## Usage Examples

### Example 1: Fresh Project Installation

```bash
# New ABP project
dotnet new abp -t app -n MyClinic
cd MyClinic

# Install Claude toolkit
git clone git@github.com:thapaliyabikendra/ai-artifacts.git /tmp/toolkit
/tmp/toolkit/scripts/install.sh .

# Output:
# ✓ Installing AI Artifacts v1.0.0
# ✓ Creating .claude/ directory
# ✓ Copying 11 agents
# ✓ Copying 47 skills
# ✓ Copying 27 commands
# ✓ Creating CLAUDE.md
# ✓ Creating settings.json
#
# Installation complete!
# Run 'claude code' to start using the toolkit.
```

### Example 2: Existing Project with Conflicts

```bash
# Project with existing .claude/ customizations
cd MyExistingProject

npx github:thapaliyabikendra/ai-artifacts install .

# Output:
# ✓ Analyzing target directory...
#
# Found existing .claude/ directory with customizations:
#   - 3 modified skills
#   - 1 custom agent
#   - Custom CLAUDE.md content
#
# Conflicts detected in 3 files:
#   .claude/skills/efcore-patterns/SKILL.md
#   .claude/skills/abp-framework-patterns/skill.md
#   .claude/commands/generate/entity.md
#
# How would you like to resolve conflicts?
#   [1] Keep mine (skip all conflicts)
#   [2] Use toolkit (overwrite all)
#   [3] Decide per-file
#   [4] Abort
#
# > 3
#
# [Proceeds with per-file conflict resolution...]
```

### Example 3: Update Existing Installation

```bash
cd MyProject

claude-abp update

# Output:
# Current version: 1.0.0
# Latest version:  1.1.0
#
# Changes:
#   + Added: grpc-integration-patterns skill
#   ~ Updated: abp-framework-patterns skill (3 files)
#   ~ Updated: backend-architect agent
#
# Proceed with update? [Y/n] y
#
# ✓ Backing up current installation...
# ✓ Updating 5 files...
# ✓ Updating CLAUDE.md toolkit section...
# ✓ Update complete!
```

### Example 4: Selective Installation

```bash
# Install only specific components
npx github:thapaliyabikendra/ai-artifacts install . --components "agents,commands"

# Or specific artifacts
npx github:thapaliyabikendra/ai-artifacts install . \
  --only "abp-developer,qa-engineer,efcore-patterns,/generate:entity"
```

---

## Maintenance Guide

### Adding New Artifacts

1. Add artifact to appropriate directory in `.claude/`
2. Update relevant index file (`AGENT-INDEX.md`, `SKILL-INDEX.md`, etc.)
3. Update `fragments/claude-md-*.md` if needed
4. Bump version in `VERSION`
5. Add entry to `CHANGELOG.md`

### Releasing New Version

```bash
# 1. Update VERSION file
echo "1.1.0" > VERSION

# 2. Update CHANGELOG.md
# Add new version section

# 3. Commit and tag
git add .
git commit -m "Release v1.1.0"
git tag v1.1.0
git push origin main --tags
```

### Syncing from Source Project

If artifacts are developed in the source project and need to be synced to the toolkit:

```bash
# From source project
./sync-to-toolkit.sh /path/to/ai-artifacts

# This script would:
# 1. Copy .claude/ artifacts
# 2. Update version
# 3. Generate changelog diff
```

---

## Open Questions

1. **Repository naming**: `ai-artifacts` vs `abp-claude-extensions` vs other?
2. **License**: MIT? Apache 2.0? Proprietary?
3. **Git hosting**: GitHub organization? GitLab? Azure DevOps?
4. **Should we include project-specific docs (`docs/domain/`, etc.) or just `.claude/`?**
5. **Support for multiple ABP versions** (8.x, 9.x, 10.x)?

---

## Next Steps

1. [ ] Review and approve this plan
2. [ ] Resolve open questions
3. [ ] Create target repository
4. [ ] Begin Phase 1 implementation

---

*This plan will be updated as implementation progresses.*
