#!/bin/bash
#
# AI Artifacts Installer
# Install Claude Code agents, skills, and commands for ABP Framework development.
#
# Usage:
#   ./install.sh <target-directory>
#   ./install.sh .                      # Install to current directory
#   curl -sSL <url>/install.sh | bash -s -- /path/to/project
#
# Options:
#   --force         Overwrite existing files
#   --skip-conflicts Skip existing files
#   --no-backup     Don't create backups
#   --dry-run       Show what would be done
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory (works for both direct run and piped)
if [ -n "$BASH_SOURCE" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    TOOLKIT_ROOT="$(dirname "$SCRIPT_DIR")"
else
    # Running via curl pipe - need to download toolkit first
    echo -e "${YELLOW}Downloading AI Artifacts...${NC}"
    TEMP_DIR=$(mktemp -d)
    git clone --depth 1 https://github.com/thapaliyabikendra/ai-artifacts.git "$TEMP_DIR" 2>/dev/null
    TOOLKIT_ROOT="$TEMP_DIR"
    CLEANUP_TEMP=true
fi

VERSION=$(cat "$TOOLKIT_ROOT/VERSION" 2>/dev/null || echo "unknown")

# Parse arguments
TARGET_DIR=""
FORCE=false
SKIP_CONFLICTS=false
NO_BACKUP=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE=true
            shift
            ;;
        --skip-conflicts)
            SKIP_CONFLICTS=true
            shift
            ;;
        --no-backup)
            NO_BACKUP=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help|-h)
            echo "AI Artifacts Installer v$VERSION"
            echo ""
            echo "Usage: ./install.sh <target-directory> [options]"
            echo ""
            echo "Options:"
            echo "  --force         Overwrite existing files without prompting"
            echo "  --skip-conflicts Skip files that already exist"
            echo "  --no-backup     Don't create backups of existing files"
            echo "  --dry-run       Show what would be done without making changes"
            echo "  --help, -h      Show this help message"
            exit 0
            ;;
        *)
            if [ -z "$TARGET_DIR" ]; then
                TARGET_DIR="$1"
            fi
            shift
            ;;
    esac
done

# Validate target
if [ -z "$TARGET_DIR" ]; then
    echo -e "${RED}Error: Target directory required${NC}"
    echo "Usage: ./install.sh <target-directory>"
    exit 1
fi

TARGET_DIR=$(cd "$TARGET_DIR" 2>/dev/null && pwd || echo "$TARGET_DIR")

if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}Error: Target directory does not exist: $TARGET_DIR${NC}"
    exit 1
fi

echo -e "${GREEN}Installing AI Artifacts v$VERSION${NC}"
echo "Target: $TARGET_DIR"
echo ""

# Check for existing installation
MANIFEST_FILE="$TARGET_DIR/.claude/.toolkit-manifest.json"
if [ -f "$MANIFEST_FILE" ]; then
    EXISTING_VERSION=$(grep -o '"version": "[^"]*"' "$MANIFEST_FILE" | cut -d'"' -f4)
    echo -e "${YELLOW}Found existing installation v$EXISTING_VERSION${NC}"

    if [ "$FORCE" != "true" ] && [ "$DRY_RUN" != "true" ]; then
        read -p "Continue and update? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Installation cancelled"
            exit 0
        fi
    fi
fi

# Create backup
if [ "$NO_BACKUP" != "true" ] && [ "$DRY_RUN" != "true" ] && [ -d "$TARGET_DIR/.claude" ]; then
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    BACKUP_DIR="$TARGET_DIR/.claude.backup.$TIMESTAMP"
    echo "Creating backup at $(basename "$BACKUP_DIR")"
    cp -r "$TARGET_DIR/.claude" "$BACKUP_DIR"
fi

# Create .claude directory
if [ "$DRY_RUN" != "true" ]; then
    mkdir -p "$TARGET_DIR/.claude"
fi

# Copy artifacts
copy_dir() {
    local src="$1"
    local dst="$2"
    local name="$3"

    if [ -d "$src" ]; then
        local count=$(find "$src" -type f | wc -l | tr -d ' ')

        if [ "$DRY_RUN" = "true" ]; then
            echo -e "  ${GREEN}✓${NC} Would copy $name/ ($count files)"
        else
            cp -r "$src" "$dst"
            echo -e "  ${GREEN}✓${NC} Copied $name/ ($count files)"
        fi
    fi
}

echo "Copying artifacts..."
copy_dir "$TOOLKIT_ROOT/.claude/agents" "$TARGET_DIR/.claude/" "agents"
copy_dir "$TOOLKIT_ROOT/.claude/skills" "$TARGET_DIR/.claude/" "skills"
copy_dir "$TOOLKIT_ROOT/.claude/commands" "$TARGET_DIR/.claude/" "commands"
copy_dir "$TOOLKIT_ROOT/.claude/knowledge" "$TARGET_DIR/.claude/" "knowledge"
copy_dir "$TOOLKIT_ROOT/.claude/guidelines" "$TARGET_DIR/.claude/" "guidelines"
copy_dir "$TOOLKIT_ROOT/.claude/flows" "$TARGET_DIR/.claude/" "flows"
copy_dir "$TOOLKIT_ROOT/.claude/templates" "$TARGET_DIR/.claude/" "templates"

# Copy index files
echo "Copying index files..."
for file in AGENT-INDEX.md AGENT-QUICK-REF.md SKILL-INDEX.md SKILL-QUICK-REF.md \
            COMMAND-INDEX.md CONTEXT-GRAPH.md GUIDELINES.md ARTIFACT-KNOWLEDGE-MATRIX.md; do
    if [ -f "$TOOLKIT_ROOT/.claude/$file" ]; then
        if [ "$DRY_RUN" != "true" ]; then
            cp "$TOOLKIT_ROOT/.claude/$file" "$TARGET_DIR/.claude/"
        fi
    fi
done
echo -e "  ${GREEN}✓${NC} Copied index files"

# Handle CLAUDE.md
SECTION_FILE="$TOOLKIT_ROOT/fragments/claude-md-section.md"
TEMPLATE_FILE="$TOOLKIT_ROOT/fragments/claude-md-template.md"
CLAUDE_MD="$TARGET_DIR/CLAUDE.md"
INSTALL_DATE=$(date +%Y-%m-%d)

if [ -f "$CLAUDE_MD" ]; then
    # Check if section already exists
    if grep -q "ai-artifacts:START" "$CLAUDE_MD"; then
        if [ "$DRY_RUN" != "true" ]; then
            # Update existing section (using temp file for portability)
            TEMP_FILE=$(mktemp)
            SECTION_CONTENT=$(cat "$SECTION_FILE" | sed "s/{{VERSION}}/$VERSION/g" | sed "s/{{INSTALL_DATE}}/$INSTALL_DATE/g")
            awk -v section="$SECTION_CONTENT" '
                /<!-- ai-artifacts:START -->/{p=1; print section; next}
                /<!-- ai-artifacts:END -->/{p=0; next}
                !p
            ' "$CLAUDE_MD" > "$TEMP_FILE"
            mv "$TEMP_FILE" "$CLAUDE_MD"
        fi
        echo -e "  ${GREEN}✓${NC} Updated toolkit section in CLAUDE.md"
    else
        if [ "$DRY_RUN" != "true" ]; then
            # Inject section at end
            SECTION_CONTENT=$(cat "$SECTION_FILE" | sed "s/{{VERSION}}/$VERSION/g" | sed "s/{{INSTALL_DATE}}/$INSTALL_DATE/g")
            echo "" >> "$CLAUDE_MD"
            echo "$SECTION_CONTENT" >> "$CLAUDE_MD"
        fi
        echo -e "  ${GREEN}✓${NC} Injected toolkit section into CLAUDE.md"
    fi
else
    if [ "$DRY_RUN" != "true" ]; then
        # Create from template
        cat "$TEMPLATE_FILE" | sed "s/{{VERSION}}/$VERSION/g" | sed "s/{{INSTALL_DATE}}/$INSTALL_DATE/g" > "$CLAUDE_MD"
    fi
    echo -e "  ${GREEN}✓${NC} Created CLAUDE.md from template"
fi

# Handle settings.json
DEFAULTS_FILE="$TOOLKIT_ROOT/fragments/settings-defaults.json"
SETTINGS_FILE="$TARGET_DIR/.claude/settings.json"

if [ -f "$DEFAULTS_FILE" ]; then
    if [ -f "$SETTINGS_FILE" ]; then
        echo -e "  ${YELLOW}!${NC} settings.json exists - review $DEFAULTS_FILE for recommended settings"
    else
        if [ "$DRY_RUN" != "true" ]; then
            # Remove comments and copy
            grep -v '^\s*"_comment"' "$DEFAULTS_FILE" | grep -v '^\s*"\$schema"' > "$SETTINGS_FILE"
        fi
        echo -e "  ${GREEN}✓${NC} Created settings.json with defaults"
    fi
fi

# Write manifest
if [ "$DRY_RUN" != "true" ]; then
    cat > "$TARGET_DIR/.claude/.toolkit-manifest.json" << EOF
{
  "toolkit": "ai-artifacts",
  "version": "$VERSION",
  "installedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "updatedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "source": "https://github.com/thapaliyabikendra/ai-artifacts"
}
EOF
fi

# Cleanup temp dir if needed
if [ "$CLEANUP_TEMP" = "true" ] && [ -n "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi

echo ""
if [ "$DRY_RUN" = "true" ]; then
    echo -e "${YELLOW}Dry run complete. No changes were made.${NC}"
else
    echo -e "${GREEN}Installation complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review .claude/GUIDELINES.md for usage instructions"
    echo "  2. Customize CLAUDE.md with your project-specific info"
    echo "  3. Run 'claude code' to start using the toolkit"
fi
