#!/usr/bin/env node

/**
 * AI Artifacts CLI
 *
 * Install, update, and manage Claude Code artifacts for ABP Framework development.
 *
 * Usage:
 *   claude-abp install <target>  Install toolkit to target project
 *   claude-abp update            Update existing installation
 *   claude-abp list              List installed artifacts
 *   claude-abp uninstall         Remove toolkit from project
 *   claude-abp version           Show toolkit version
 */

const path = require('path');
const Installer = require('../src/installer');

const VERSION = require('fs')
  .readFileSync(path.join(__dirname, '..', 'VERSION'), 'utf8')
  .trim();

const HELP = `
AI Artifacts v${VERSION}

Usage: claude-abp <command> [options]

Commands:
  install <target>     Install toolkit to target project directory
  update               Update existing installation in current directory
  list                 List installed artifacts
  uninstall            Remove toolkit from current project
  version              Show toolkit version

Options:
  --dry-run            Show what would be done without making changes
  --force              Overwrite existing files without prompting
  --skip-conflicts     Skip files that already exist
  --no-backup          Don't create backups of modified files
  --components <list>  Install specific components (comma-separated)
                       Valid: agents,skills,commands,knowledge,guidelines
  --verbose            Show detailed output
  --quiet              Suppress non-error output
  --help, -h           Show this help message

Examples:
  # Install to a project directory
  claude-abp install /path/to/my-project

  # Install to current directory
  claude-abp install .

  # Install only agents and skills
  claude-abp install . --components agents,skills

  # Preview installation without making changes
  claude-abp install . --dry-run

  # Update existing installation
  cd my-project && claude-abp update

  # Force overwrite all files
  claude-abp install . --force

For more information, visit: https://github.com/thapaliyabikendra/ai-artifacts
`;

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(HELP);
    process.exit(0);
  }

  const command = args[0];

  // Parse options
  const options = {
    dryRun: args.includes('--dry-run'),
    force: args.includes('--force'),
    skipConflicts: args.includes('--skip-conflicts'),
    noBackup: args.includes('--no-backup'),
    verbose: args.includes('--verbose'),
    quiet: args.includes('--quiet'),
    components: null,
  };

  // Parse --components
  const componentsIdx = args.indexOf('--components');
  if (componentsIdx !== -1 && args[componentsIdx + 1]) {
    options.components = args[componentsIdx + 1].split(',').map((c) => c.trim());
  }

  try {
    switch (command) {
      case 'install': {
        const target = args[1];
        if (!target) {
          console.error('Error: Target directory required');
          console.error('Usage: claude-abp install <target>');
          process.exit(1);
        }
        const installer = new Installer(target, options);
        await installer.install();
        break;
      }

      case 'update': {
        const installer = new Installer(process.cwd(), options);
        await installer.update();
        break;
      }

      case 'list': {
        const installer = new Installer(process.cwd(), options);
        await installer.list();
        break;
      }

      case 'uninstall': {
        const installer = new Installer(process.cwd(), options);
        await installer.uninstall();
        break;
      }

      case 'version':
        console.log(`AI Artifacts v${VERSION}`);
        break;

      default:
        console.error(`Unknown command: ${command}`);
        console.log(HELP);
        process.exit(1);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    if (options.verbose) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

main();
