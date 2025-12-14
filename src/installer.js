/**
 * AI Artifacts Installer
 *
 * Core installation logic for copying artifacts, merging settings,
 * and injecting CLAUDE.md sections.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const TOOLKIT_ROOT = path.join(__dirname, '..');
const CLAUDE_DIR = path.join(TOOLKIT_ROOT, '.claude');
const FRAGMENTS_DIR = path.join(TOOLKIT_ROOT, 'fragments');
const VERSION = fs.readFileSync(path.join(TOOLKIT_ROOT, 'VERSION'), 'utf8').trim();

const VALID_COMPONENTS = ['agents', 'skills', 'commands', 'knowledge', 'guidelines', 'flows', 'templates'];
const INDEX_FILES = [
  'AGENT-INDEX.md',
  'AGENT-QUICK-REF.md',
  'SKILL-INDEX.md',
  'SKILL-QUICK-REF.md',
  'COMMAND-INDEX.md',
  'CONTEXT-GRAPH.md',
  'GUIDELINES.md',
  'ARTIFACT-KNOWLEDGE-MATRIX.md',
];

class Installer {
  constructor(targetPath, options = {}) {
    this.targetPath = path.resolve(targetPath);
    this.targetClaudeDir = path.join(this.targetPath, '.claude');
    this.options = {
      dryRun: false,
      force: false,
      skipConflicts: false,
      noBackup: false,
      verbose: false,
      quiet: false,
      components: null,
      ...options,
    };
  }

  log(message, level = 'info') {
    if (this.options.quiet && level !== 'error') return;
    const prefix = {
      info: '  ',
      success: '✓ ',
      warning: '⚠ ',
      error: '✗ ',
    }[level] || '  ';
    console.log(`${prefix}${message}`);
  }

  verbose(message) {
    if (this.options.verbose) {
      console.log(`    ${message}`);
    }
  }

  /**
   * Main installation entry point
   */
  async install() {
    this.log(`Installing AI Artifacts v${VERSION}`, 'info');
    this.log(`Target: ${this.targetPath}`, 'info');
    console.log();

    // Step 1: Validate target
    this.validateTarget();

    // Step 2: Check for existing installation
    const existingManifest = this.readManifest();
    if (existingManifest) {
      this.log(`Found existing installation v${existingManifest.version}`, 'warning');
      if (!this.options.force && !this.options.dryRun) {
        const proceed = await this.prompt(
          'Existing installation found. Continue and update? (y/n): '
        );
        if (proceed.toLowerCase() !== 'y') {
          this.log('Installation cancelled', 'info');
          return;
        }
      }
    }

    // Step 3: Create backup
    if (!this.options.noBackup && !this.options.dryRun && fs.existsSync(this.targetClaudeDir)) {
      await this.createBackup();
    }

    // Step 4: Copy artifacts
    await this.copyArtifacts();

    // Step 5: Inject CLAUDE.md section
    await this.integrateClaudeMd();

    // Step 6: Merge settings
    await this.mergeSettings();

    // Step 7: Write manifest
    await this.writeManifest();

    // Step 8: Report
    console.log();
    if (this.options.dryRun) {
      this.log('Dry run complete. No changes were made.', 'info');
    } else {
      this.log('Installation complete!', 'success');
      console.log();
      this.log('Next steps:', 'info');
      this.log('1. Review .claude/GUIDELINES.md for usage instructions', 'info');
      this.log('2. Customize CLAUDE.md with your project-specific info', 'info');
      this.log('3. Run `claude code` to start using the toolkit', 'info');
    }
  }

  /**
   * Update existing installation
   */
  async update() {
    const manifest = this.readManifest();
    if (!manifest) {
      this.log('No existing installation found. Use `install` instead.', 'error');
      process.exit(1);
    }

    this.log(`Current version: ${manifest.version}`, 'info');
    this.log(`Toolkit version: ${VERSION}`, 'info');

    if (manifest.version === VERSION) {
      this.log('Already up to date!', 'success');
      return;
    }

    this.log(`Updating from v${manifest.version} to v${VERSION}...`, 'info');
    console.log();

    // Create backup before update
    if (!this.options.noBackup && !this.options.dryRun) {
      await this.createBackup();
    }

    // Re-run installation
    await this.copyArtifacts();
    await this.integrateClaudeMd();
    await this.writeManifest();

    console.log();
    if (this.options.dryRun) {
      this.log('Dry run complete. No changes were made.', 'info');
    } else {
      this.log(`Updated to v${VERSION}!`, 'success');
    }
  }

  /**
   * List installed artifacts
   */
  async list() {
    const manifest = this.readManifest();
    if (!manifest) {
      this.log('No AI Artifacts installation found.', 'info');
      return;
    }

    console.log(`AI Artifacts v${manifest.version}`);
    console.log(`Installed: ${new Date(manifest.installedAt).toLocaleDateString()}`);
    if (manifest.updatedAt !== manifest.installedAt) {
      console.log(`Updated: ${new Date(manifest.updatedAt).toLocaleDateString()}`);
    }
    console.log();

    // Count artifacts
    const counts = {
      agents: this.countFiles(path.join(this.targetClaudeDir, 'agents'), '.md'),
      skills: this.countDirs(path.join(this.targetClaudeDir, 'skills')),
      commands: this.countFiles(path.join(this.targetClaudeDir, 'commands'), '.md'),
    };

    console.log('Installed artifacts:');
    console.log(`  Agents:   ${counts.agents}`);
    console.log(`  Skills:   ${counts.skills}`);
    console.log(`  Commands: ${counts.commands}`);
  }

  /**
   * Remove toolkit from project
   */
  async uninstall() {
    const manifest = this.readManifest();
    if (!manifest) {
      this.log('No AI Artifacts installation found.', 'info');
      return;
    }

    this.log(`Found installation v${manifest.version}`, 'info');

    if (!this.options.force) {
      const confirm = await this.prompt(
        'This will remove all toolkit artifacts. Continue? (y/n): '
      );
      if (confirm.toLowerCase() !== 'y') {
        this.log('Uninstall cancelled', 'info');
        return;
      }
    }

    // Create backup
    if (!this.options.noBackup && !this.options.dryRun) {
      await this.createBackup();
    }

    if (!this.options.dryRun) {
      // Remove .claude directory
      if (fs.existsSync(this.targetClaudeDir)) {
        fs.rmSync(this.targetClaudeDir, { recursive: true });
        this.log('Removed .claude/ directory', 'success');
      }

      // Remove toolkit section from CLAUDE.md
      const claudeMdPath = path.join(this.targetPath, 'CLAUDE.md');
      if (fs.existsSync(claudeMdPath)) {
        let content = fs.readFileSync(claudeMdPath, 'utf8');
        content = content.replace(
          /<!-- ai-artifacts:START -->[\s\S]*?<!-- ai-artifacts:END -->\n*/g,
          ''
        );
        fs.writeFileSync(claudeMdPath, content);
        this.log('Removed toolkit section from CLAUDE.md', 'success');
      }
    }

    this.log('Uninstall complete!', 'success');
  }

  // === Helper Methods ===

  validateTarget() {
    if (!fs.existsSync(this.targetPath)) {
      throw new Error(`Target directory does not exist: ${this.targetPath}`);
    }
    const stat = fs.statSync(this.targetPath);
    if (!stat.isDirectory()) {
      throw new Error(`Target is not a directory: ${this.targetPath}`);
    }
  }

  readManifest() {
    const manifestPath = path.join(this.targetClaudeDir, '.toolkit-manifest.json');
    if (fs.existsSync(manifestPath)) {
      return JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    }
    return null;
  }

  async writeManifest() {
    if (this.options.dryRun) return;

    const existing = this.readManifest();
    const manifest = {
      toolkit: 'ai-artifacts',
      version: VERSION,
      installedAt: existing?.installedAt || new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      source: 'https://github.com/thapaliyabikendra/ai-artifacts',
      components: this.options.components || VALID_COMPONENTS,
    };

    const manifestPath = path.join(this.targetClaudeDir, '.toolkit-manifest.json');
    fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
    this.verbose('Wrote manifest file');
  }

  async createBackup() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const backupDir = path.join(this.targetPath, `.claude.backup.${timestamp}`);

    if (fs.existsSync(this.targetClaudeDir)) {
      this.log(`Creating backup at ${path.basename(backupDir)}`, 'info');
      this.copyDirSync(this.targetClaudeDir, backupDir);
    }
  }

  async copyArtifacts() {
    const components = this.options.components || VALID_COMPONENTS;

    // Ensure target .claude directory exists
    if (!this.options.dryRun && !fs.existsSync(this.targetClaudeDir)) {
      fs.mkdirSync(this.targetClaudeDir, { recursive: true });
    }

    // Copy component directories
    for (const component of components) {
      const sourceDir = path.join(CLAUDE_DIR, component);
      const targetDir = path.join(this.targetClaudeDir, component);

      if (fs.existsSync(sourceDir)) {
        const count = this.copyDirectory(sourceDir, targetDir);
        this.log(`Copied ${component}/ (${count} files)`, 'success');
      }
    }

    // Copy index files
    let indexCount = 0;
    for (const indexFile of INDEX_FILES) {
      const sourceFile = path.join(CLAUDE_DIR, indexFile);
      const targetFile = path.join(this.targetClaudeDir, indexFile);

      if (fs.existsSync(sourceFile)) {
        if (!this.options.dryRun) {
          fs.copyFileSync(sourceFile, targetFile);
        }
        indexCount++;
        this.verbose(`Copied ${indexFile}`);
      }
    }
    this.log(`Copied index files (${indexCount} files)`, 'success');
  }

  copyDirectory(source, target) {
    if (this.options.dryRun) {
      return this.countAllFiles(source);
    }

    if (!fs.existsSync(target)) {
      fs.mkdirSync(target, { recursive: true });
    }

    let count = 0;
    const entries = fs.readdirSync(source, { withFileTypes: true });

    for (const entry of entries) {
      const sourcePath = path.join(source, entry.name);
      const targetPath = path.join(target, entry.name);

      if (entry.isDirectory()) {
        count += this.copyDirectory(sourcePath, targetPath);
      } else {
        // Check for conflicts
        if (fs.existsSync(targetPath) && !this.options.force) {
          if (this.options.skipConflicts) {
            this.verbose(`Skipped (exists): ${entry.name}`);
            continue;
          }
          // Compare files
          const sourceContent = fs.readFileSync(sourcePath, 'utf8');
          const targetContent = fs.readFileSync(targetPath, 'utf8');
          if (sourceContent === targetContent) {
            this.verbose(`Skipped (identical): ${entry.name}`);
            continue;
          }
        }

        fs.copyFileSync(sourcePath, targetPath);
        count++;
      }
    }

    return count;
  }

  copyDirSync(source, target) {
    if (!fs.existsSync(target)) {
      fs.mkdirSync(target, { recursive: true });
    }

    const entries = fs.readdirSync(source, { withFileTypes: true });
    for (const entry of entries) {
      const sourcePath = path.join(source, entry.name);
      const targetPath = path.join(target, entry.name);

      if (entry.isDirectory()) {
        this.copyDirSync(sourcePath, targetPath);
      } else {
        fs.copyFileSync(sourcePath, targetPath);
      }
    }
  }

  async integrateClaudeMd() {
    const claudeMdPath = path.join(this.targetPath, 'CLAUDE.md');
    const sectionPath = path.join(FRAGMENTS_DIR, 'claude-md-section.md');
    const templatePath = path.join(FRAGMENTS_DIR, 'claude-md-template.md');

    let section = fs.readFileSync(sectionPath, 'utf8');
    section = section
      .replace('{{VERSION}}', VERSION)
      .replace('{{INSTALL_DATE}}', new Date().toISOString().slice(0, 10));

    if (fs.existsSync(claudeMdPath)) {
      // Inject or update section in existing CLAUDE.md
      let content = fs.readFileSync(claudeMdPath, 'utf8');

      if (content.includes('<!-- ai-artifacts:START -->')) {
        // Update existing section
        content = content.replace(
          /<!-- ai-artifacts:START -->[\s\S]*?<!-- ai-artifacts:END -->/,
          section.trim()
        );
        this.log('Updated toolkit section in CLAUDE.md', 'success');
      } else {
        // Inject new section (before ## Conventions or at end)
        const insertPoint = content.indexOf('## Conventions');
        if (insertPoint !== -1) {
          content =
            content.slice(0, insertPoint) +
            section +
            '\n' +
            content.slice(insertPoint);
        } else {
          content = content + '\n' + section;
        }
        this.log('Injected toolkit section into CLAUDE.md', 'success');
      }

      if (!this.options.dryRun) {
        fs.writeFileSync(claudeMdPath, content);
      }
    } else {
      // Create new CLAUDE.md from template
      let template = fs.readFileSync(templatePath, 'utf8');
      template = template
        .replace('{{VERSION}}', VERSION)
        .replace('{{INSTALL_DATE}}', new Date().toISOString().slice(0, 10));

      if (!this.options.dryRun) {
        fs.writeFileSync(claudeMdPath, template);
      }
      this.log('Created CLAUDE.md from template', 'success');
    }
  }

  async mergeSettings() {
    const targetSettingsPath = path.join(this.targetClaudeDir, 'settings.json');
    const defaultsPath = path.join(FRAGMENTS_DIR, 'settings-defaults.json');

    if (!fs.existsSync(defaultsPath)) {
      this.verbose('No default settings to merge');
      return;
    }

    const defaults = JSON.parse(fs.readFileSync(defaultsPath, 'utf8'));
    delete defaults.$schema;
    delete defaults._comment;

    if (fs.existsSync(targetSettingsPath)) {
      // Merge with existing settings
      const existing = JSON.parse(fs.readFileSync(targetSettingsPath, 'utf8'));
      const merged = this.deepMerge(defaults, existing);

      if (!this.options.dryRun) {
        fs.writeFileSync(targetSettingsPath, JSON.stringify(merged, null, 2));
      }
      this.log('Merged toolkit defaults into settings.json', 'success');
    } else {
      // Create new settings file
      if (!this.options.dryRun) {
        fs.writeFileSync(targetSettingsPath, JSON.stringify(defaults, null, 2));
      }
      this.log('Created settings.json with defaults', 'success');
    }
  }

  deepMerge(source, target) {
    const result = { ...target };

    for (const key of Object.keys(source)) {
      if (!(key in result)) {
        result[key] = source[key];
      } else if (Array.isArray(source[key]) && Array.isArray(result[key])) {
        // Merge arrays (deduplicate)
        result[key] = [...new Set([...result[key], ...source[key]])];
      } else if (
        typeof source[key] === 'object' &&
        source[key] !== null &&
        typeof result[key] === 'object' &&
        result[key] !== null
      ) {
        result[key] = this.deepMerge(source[key], result[key]);
      }
      // Otherwise keep target value
    }

    return result;
  }

  countFiles(dir, ext) {
    if (!fs.existsSync(dir)) return 0;
    let count = 0;
    const walk = (d) => {
      const entries = fs.readdirSync(d, { withFileTypes: true });
      for (const entry of entries) {
        const p = path.join(d, entry.name);
        if (entry.isDirectory()) {
          walk(p);
        } else if (entry.name.endsWith(ext)) {
          count++;
        }
      }
    };
    walk(dir);
    return count;
  }

  countDirs(dir) {
    if (!fs.existsSync(dir)) return 0;
    return fs.readdirSync(dir, { withFileTypes: true }).filter((e) => e.isDirectory()).length;
  }

  countAllFiles(dir) {
    if (!fs.existsSync(dir)) return 0;
    let count = 0;
    const walk = (d) => {
      const entries = fs.readdirSync(d, { withFileTypes: true });
      for (const entry of entries) {
        const p = path.join(d, entry.name);
        if (entry.isDirectory()) {
          walk(p);
        } else {
          count++;
        }
      }
    };
    walk(dir);
    return count;
  }

  prompt(question) {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    return new Promise((resolve) => {
      rl.question(question, (answer) => {
        rl.close();
        resolve(answer);
      });
    });
  }
}

module.exports = Installer;
