# AI Artifacts

A comprehensive collection of Claude Code agents, skills, and commands for ABP Framework development.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![ABP Framework](https://img.shields.io/badge/ABP%20Framework-8.x%20%7C%209.x%20%7C%2010.x-purple)](https://abp.io)

## Overview

AI Artifacts provides AI-powered development assistance for ABP Framework projects through:

| Component | Count | Description |
|-----------|-------|-------------|
| **Agents** | 11 | Specialized AI agents for different development roles |
| **Skills** | 47 | Domain expertise and coding patterns |
| **Commands** | 27 | Slash commands for common development tasks |

## Quick Start

### Installation

Choose your preferred installation method:

#### Option 1: Git Clone + Install Script (Recommended)

```bash
# Clone the toolkit
git clone https://github.com/thapaliyabikendra/ai-artifacts.git

# Install to your project
cd ai-artifacts
./scripts/install.sh /path/to/your/project

# On Windows (PowerShell)
.\scripts\install.ps1 -TargetPath "C:\Projects\YourProject"
```

#### Option 2: npx (No Clone Required)

```bash
npx github:thapaliyabikendra/ai-artifacts install .
```

#### Option 3: One-Line Install (Unix/macOS/WSL)

```bash
curl -sSL https://raw.githubusercontent.com/thapaliyabikendra/ai-artifacts/main/scripts/install.sh | bash -s -- /path/to/project
```

#### Option 4: Manual Installation

1. Clone or download this repository
2. Copy the `.claude/` directory to your project root
3. Add the toolkit section to your `CLAUDE.md` (see `fragments/claude-md-section.md`)

### Verify Installation

After installation, your project should have:

```
your-project/
├── .claude/
│   ├── agents/          # 11 AI agents
│   ├── skills/          # 47 skills with patterns
│   ├── commands/        # 27 slash commands
│   ├── knowledge/       # Knowledge base
│   ├── guidelines/      # Best practices
│   ├── GUIDELINES.md    # Main usage guide
│   └── ...
└── CLAUDE.md            # Updated with toolkit references
```

## What's Included

### Agents

AI agents specialized for different development tasks:

| Category | Agents |
|----------|--------|
| **Architects** | `backend-architect`, `business-analyst` |
| **Engineers** | `abp-developer`, `react-developer`, `devops-engineer` |
| **Reviewers** | `abp-code-reviewer`, `react-code-reviewer`, `qa-engineer`, `security-engineer` |
| **Specialists** | `debugger`, `database-migrator` |

**Usage:**
```
Use the abp-developer agent to implement the Patient entity
```

### Skills

Domain expertise automatically applied based on context:

| Category | Key Skills |
|----------|------------|
| **ABP Framework** | `abp-framework-patterns`, `abp-entity-patterns`, `abp-service-patterns` |
| **Database** | `efcore-patterns`, `linq-optimization-patterns` |
| **Validation** | `fluentvalidation-patterns` |
| **Security** | `security-patterns`, `openiddict-authorization` |
| **Testing** | `xunit-testing-patterns`, `e2e-testing-patterns` |
| **Frontend** | `react-development-patterns`, `typescript-advanced-types` |

### Commands

Slash commands for common tasks:

| Command | Description |
|---------|-------------|
| `/feature:add-feature` | End-to-end feature development with SDLC automation |
| `/generate:entity` | Scaffold complete ABP entity with all layers |
| `/generate:migration` | Generate EF Core migration with review |
| `/tdd:tdd-cycle` | Execute TDD red-green-refactor workflow |
| `/debug:smart-debug` | AI-powered root cause analysis |
| `/review:permissions` | Audit ABP permission definitions |
| `/review:pre-push` | Fast security scan before git push |

**Usage:**
```
/generate:entity Patient --properties "Name:string,Email:string,DateOfBirth:DateTime"
```

## Usage Guide

### Agent Chains

Common workflows using multiple agents in sequence:

| Workflow | Agent Chain |
|----------|-------------|
| **Full Feature** | `business-analyst` → `backend-architect` → `abp-developer` → `qa-engineer` → `abp-code-reviewer` |
| **Fast Feature** | `backend-architect` → `abp-developer` → `qa-engineer` |
| **Bug Fix** | `debugger` → `abp-developer` → `qa-engineer` |
| **Security Audit** | `security-engineer` (standalone) |

### Skill Discovery

Skills are automatically triggered based on context. For manual discovery:

```
Read .claude/SKILL-INDEX.md to find available skills
```

### Command Reference

View all available commands:

```
See .claude/COMMAND-INDEX.md for full command reference
```

## Updating

To update an existing installation:

```bash
# Using CLI
cd your-project
npx github:thapaliyabikendra/ai-artifacts update

# Or re-run install
./scripts/install.sh /path/to/your/project
```

## Uninstalling

```bash
cd your-project
npx github:thapaliyabikendra/ai-artifacts uninstall
```

Or manually:
1. Delete the `.claude/` directory
2. Remove the toolkit section from `CLAUDE.md` (between `ai-artifacts:START` and `ai-artifacts:END` comments)

## Supported ABP Framework Versions

- ABP Framework 8.x
- ABP Framework 9.x
- ABP Framework 10.x (primary target)

## CLI Reference

```
claude-abp <command> [options]

Commands:
  install <target>     Install toolkit to target project
  update               Update existing installation
  list                 List installed artifacts
  uninstall            Remove toolkit from project
  version              Show toolkit version

Options:
  --dry-run            Preview changes without applying
  --force              Overwrite without prompting
  --skip-conflicts     Skip existing files
  --no-backup          Don't create backups
  --components <list>  Install specific components only
  --verbose            Show detailed output
  --quiet              Suppress non-error output
```

## Project Structure

```
ai-artifacts/
├── .claude/                    # Artifacts to be installed
│   ├── agents/                 # AI agents by role
│   ├── skills/                 # Skills by category
│   ├── commands/               # Slash commands by domain
│   ├── knowledge/              # Knowledge base
│   └── guidelines/             # Guidelines and best practices
├── bin/
│   └── claude-abp.js          # CLI entry point
├── src/
│   └── installer.js           # Core installation logic
├── scripts/
│   ├── install.sh             # Bash installer
│   └── install.ps1            # PowerShell installer
├── fragments/
│   ├── claude-md-template.md  # Full CLAUDE.md template
│   ├── claude-md-section.md   # Section to inject
│   └── settings-defaults.json # Default settings
├── VERSION                     # Current version
├── CHANGELOG.md               # Version history
└── README.md                  # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Adding New Artifacts

- **Agents**: Add to `.claude/agents/<category>/`
- **Skills**: Add directory to `.claude/skills/` with `SKILL.md`
- **Commands**: Add to `.claude/commands/<domain>/`

Update the corresponding index files after adding new artifacts.

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Links

- [ABP Framework Documentation](https://docs.abp.io)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Report Issues](https://github.com/thapaliyabikendra/ai-artifacts/issues)
