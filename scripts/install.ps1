<#
.SYNOPSIS
    AI Artifacts Installer for Windows

.DESCRIPTION
    Install Claude Code agents, skills, and commands for ABP Framework development.

.PARAMETER TargetPath
    The target project directory to install to.

.PARAMETER Force
    Overwrite existing files without prompting.

.PARAMETER SkipConflicts
    Skip files that already exist.

.PARAMETER NoBackup
    Don't create backups of existing files.

.PARAMETER DryRun
    Show what would be done without making changes.

.EXAMPLE
    .\install.ps1 -TargetPath "C:\Projects\MyApp"

.EXAMPLE
    .\install.ps1 -TargetPath "." -Force

.EXAMPLE
    .\install.ps1 -TargetPath "C:\Projects\MyApp" -DryRun
#>

param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$TargetPath,

    [switch]$Force,
    [switch]$SkipConflicts,
    [switch]$NoBackup,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# Get toolkit root directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ToolkitRoot = Split-Path -Parent $ScriptDir

# Read version
$Version = Get-Content "$ToolkitRoot\VERSION" -Raw | ForEach-Object { $_.Trim() }

function Write-Success { param($Message) Write-Host "  ✓ $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "  ! $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "  ✗ $Message" -ForegroundColor Red }

Write-Host "Installing AI Artifacts v$Version" -ForegroundColor Green
Write-Host "Target: $TargetPath"
Write-Host ""

# Resolve target path
$TargetPath = Resolve-Path $TargetPath -ErrorAction SilentlyContinue
if (-not $TargetPath) {
    Write-Error "Target directory does not exist"
    exit 1
}

$TargetClaudeDir = Join-Path $TargetPath ".claude"
$ManifestFile = Join-Path $TargetClaudeDir ".toolkit-manifest.json"

# Check for existing installation
if (Test-Path $ManifestFile) {
    $Manifest = Get-Content $ManifestFile | ConvertFrom-Json
    Write-Warning "Found existing installation v$($Manifest.version)"

    if (-not $Force -and -not $DryRun) {
        $response = Read-Host "Continue and update? (y/n)"
        if ($response -ne 'y') {
            Write-Host "Installation cancelled"
            exit 0
        }
    }
}

# Create backup
if (-not $NoBackup -and -not $DryRun -and (Test-Path $TargetClaudeDir)) {
    $Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $BackupDir = Join-Path $TargetPath ".claude.backup.$Timestamp"
    Write-Host "Creating backup at $(Split-Path $BackupDir -Leaf)"
    Copy-Item -Path $TargetClaudeDir -Destination $BackupDir -Recurse
}

# Create .claude directory
if (-not $DryRun -and -not (Test-Path $TargetClaudeDir)) {
    New-Item -Path $TargetClaudeDir -ItemType Directory -Force | Out-Null
}

# Helper function to copy directory
function Copy-ArtifactDir {
    param($Name)

    $SourceDir = Join-Path $ToolkitRoot ".claude\$Name"
    $DestDir = Join-Path $TargetClaudeDir $Name

    if (Test-Path $SourceDir) {
        $FileCount = (Get-ChildItem -Path $SourceDir -Recurse -File).Count

        if ($DryRun) {
            Write-Success "Would copy $Name/ ($FileCount files)"
        }
        else {
            if (Test-Path $DestDir) {
                Remove-Item -Path $DestDir -Recurse -Force
            }
            Copy-Item -Path $SourceDir -Destination $DestDir -Recurse
            Write-Success "Copied $Name/ ($FileCount files)"
        }
    }
}

# Copy artifacts
Write-Host "Copying artifacts..."
Copy-ArtifactDir "agents"
Copy-ArtifactDir "skills"
Copy-ArtifactDir "commands"
Copy-ArtifactDir "knowledge"
Copy-ArtifactDir "guidelines"
Copy-ArtifactDir "flows"
Copy-ArtifactDir "templates"

# Copy index files
Write-Host "Copying index files..."
$IndexFiles = @(
    "AGENT-INDEX.md",
    "AGENT-QUICK-REF.md",
    "SKILL-INDEX.md",
    "SKILL-QUICK-REF.md",
    "COMMAND-INDEX.md",
    "CONTEXT-GRAPH.md",
    "GUIDELINES.md",
    "ARTIFACT-KNOWLEDGE-MATRIX.md"
)

foreach ($file in $IndexFiles) {
    $SourceFile = Join-Path $ToolkitRoot ".claude\$file"
    $DestFile = Join-Path $TargetClaudeDir $file

    if (Test-Path $SourceFile) {
        if (-not $DryRun) {
            Copy-Item -Path $SourceFile -Destination $DestFile -Force
        }
    }
}
Write-Success "Copied index files"

# Handle CLAUDE.md
$SectionFile = Join-Path $ToolkitRoot "fragments\claude-md-section.md"
$TemplateFile = Join-Path $ToolkitRoot "fragments\claude-md-template.md"
$ClaudeMdPath = Join-Path $TargetPath "CLAUDE.md"
$InstallDate = Get-Date -Format "yyyy-MM-dd"

$SectionContent = (Get-Content $SectionFile -Raw) -replace '\{\{VERSION\}\}', $Version -replace '\{\{INSTALL_DATE\}\}', $InstallDate

if (Test-Path $ClaudeMdPath) {
    $ExistingContent = Get-Content $ClaudeMdPath -Raw

    if ($ExistingContent -match "ai-artifacts:START") {
        # Update existing section
        if (-not $DryRun) {
            $Pattern = '(?s)<!-- ai-artifacts:START -->.*?<!-- ai-artifacts:END -->'
            $NewContent = $ExistingContent -replace $Pattern, $SectionContent.Trim()
            Set-Content -Path $ClaudeMdPath -Value $NewContent -NoNewline
        }
        Write-Success "Updated toolkit section in CLAUDE.md"
    }
    else {
        # Inject section at end
        if (-not $DryRun) {
            Add-Content -Path $ClaudeMdPath -Value "`n$SectionContent"
        }
        Write-Success "Injected toolkit section into CLAUDE.md"
    }
}
else {
    # Create from template
    if (-not $DryRun) {
        $TemplateContent = (Get-Content $TemplateFile -Raw) -replace '\{\{VERSION\}\}', $Version -replace '\{\{INSTALL_DATE\}\}', $InstallDate
        Set-Content -Path $ClaudeMdPath -Value $TemplateContent -NoNewline
    }
    Write-Success "Created CLAUDE.md from template"
}

# Handle settings.json
$DefaultsFile = Join-Path $ToolkitRoot "fragments\settings-defaults.json"
$SettingsFile = Join-Path $TargetClaudeDir "settings.json"

if (Test-Path $DefaultsFile) {
    if (Test-Path $SettingsFile) {
        Write-Warning "settings.json exists - review settings-defaults.json for recommended settings"
    }
    else {
        if (-not $DryRun) {
            $Defaults = Get-Content $DefaultsFile | ConvertFrom-Json
            # Remove comment properties
            $Defaults.PSObject.Properties.Remove('$schema')
            $Defaults.PSObject.Properties.Remove('_comment')
            $Defaults | ConvertTo-Json -Depth 10 | Set-Content $SettingsFile
        }
        Write-Success "Created settings.json with defaults"
    }
}

# Write manifest
if (-not $DryRun) {
    $Manifest = @{
        toolkit     = "ai-artifacts"
        version     = $Version
        installedAt = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        updatedAt   = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        source      = "https://github.com/thapaliyabikendra/ai-artifacts"
    }
    $Manifest | ConvertTo-Json | Set-Content $ManifestFile
}

Write-Host ""
if ($DryRun) {
    Write-Host "Dry run complete. No changes were made." -ForegroundColor Yellow
}
else {
    Write-Host "Installation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Review .claude/GUIDELINES.md for usage instructions"
    Write-Host "  2. Customize CLAUDE.md with your project-specific info"
    Write-Host "  3. Run 'claude code' to start using the toolkit"
}
