# Git Commit Message Generator using Claude Code CLI
# Usage: Stage changes first, then run this script

$ErrorActionPreference = "Stop"

# Get staged diff
$diff = git diff --staged 2>&1

if (-not $diff -or $diff -match "^fatal:") {
    Write-Host "No staged changes found. Stage files first with 'git add'." -ForegroundColor Yellow
    exit 1
}

# Truncate diff if too large (Claude has context limits)
$maxDiffLength = 8000
if ($diff.Length -gt $maxDiffLength) {
    $diff = $diff.Substring(0, $maxDiffLength) + "`n... [diff truncated]"
    Write-Host "Note: Diff was truncated due to size." -ForegroundColor Cyan
}

$prompt = @"
Generate a Git commit message from the diff below.

Rules:
- Use Conventional Commits format (type(scope): description)
- Summary line only (no body)
- Max 72 characters
- Imperative mood (Add, Fix, Update, not Added, Fixed, Updated)
- No emojis
- No markdown formatting
- No quotes around the message
- Output ONLY the commit message, nothing else

Git diff:
$diff
"@

Write-Host "Generating commit message with Claude..." -ForegroundColor Cyan

try {
    # Write prompt to temp file to avoid argument parsing issues
    $tempFile = Join-Path $env:TEMP "claude-commit-prompt.txt"
    $prompt | Out-File -FilePath $tempFile -Encoding utf8 -NoNewline

    # Use Claude CLI with -p (print mode) reading from stdin
    $commitMessage = Get-Content $tempFile -Raw | claude -p 2>&1

    # Cleanup temp file
    Remove-Item $tempFile -ErrorAction SilentlyContinue

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Claude CLI error: $commitMessage" -ForegroundColor Red
        exit 1
    }

    # Clean up the message (trim whitespace, remove any quotes)
    $commitMessage = $commitMessage.Trim().Trim('"').Trim("'")

    if (-not $commitMessage) {
        Write-Host "Claude returned empty response." -ForegroundColor Red
        exit 1
    }

    # Copy to clipboard
    $commitMessage | Set-Clipboard

    Write-Host ""
    Write-Host "Commit message generated:" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host $commitMessage -ForegroundColor White
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "(Message copied to clipboard)" -ForegroundColor Cyan
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}
