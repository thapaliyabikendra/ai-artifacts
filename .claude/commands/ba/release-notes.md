---
name: release-notes
description: "Generate release notes from commits, PRs, or changelog"
args:
  - name: version
    description: "Version number (e.g., 1.2.0)"
    required: true
  - name: from
    description: "Starting point: tag, commit, or 'last-release'"
    required: false
    default: "last-release"
  - name: format
    description: "Output format: markdown | slack | email"
    required: false
    default: "markdown"
---

# Generate Release Notes

Version: **$ARGUMENTS.version**
From: **$ARGUMENTS.from**
Format: **$ARGUMENTS.format**

## Instructions

### Step 1: Gather Changes

Run git commands to collect commits:

```bash
# Find last release tag
git describe --tags --abbrev=0

# Get commits since last release
git log [from]..HEAD --oneline --no-merges

# Get merged PRs
git log [from]..HEAD --merges --oneline
```

### Step 2: Categorize Changes

Parse commit messages and categorize:

| Prefix | Category | Emoji |
|--------|----------|-------|
| feat: | Features | ✨ |
| fix: | Bug Fixes | 🐛 |
| perf: | Performance | ⚡ |
| docs: | Documentation | 📚 |
| refactor: | Refactoring | ♻️ |
| test: | Tests | ✅ |
| chore: | Maintenance | 🔧 |
| security: | Security | 🔒 |
| breaking: | Breaking Changes | 💥 |

### Step 3: Generate Release Notes

#### Markdown Format

```markdown
# Release Notes - v[VERSION]

**Release Date**: [YYYY-MM-DD]
**Previous Version**: [previous version]

## Highlights

[2-3 sentence summary of the most important changes in this release]

## ✨ New Features

- **[Feature Name]**: [Brief description] ([#PR](link))
  - [Additional detail if needed]
- **[Feature Name]**: [Brief description] ([#PR](link))

## 🐛 Bug Fixes

- Fixed [issue description] ([#PR](link))
- Fixed [issue description] ([#PR](link))

## ⚡ Performance Improvements

- [Improvement description] ([#PR](link))

## 💥 Breaking Changes

> ⚠️ **Action Required**: These changes may require updates to your code.

- **[Change]**: [Description and migration path]
  ```diff
  - old code
  + new code
  ```

## 🔒 Security Updates

- [Security fix description]

## ♻️ Refactoring

- [Refactoring description]

## 📚 Documentation

- [Documentation update]

## 🔧 Maintenance

- [Maintenance item]

---

## Upgrade Guide

### From v[previous] to v[current]

1. **Step 1**: [Action]
2. **Step 2**: [Action]
3. **Run migrations**: `dotnet ef database update`

### Breaking Change Details

#### [Breaking Change 1]

**Before:**
```csharp
// Old usage
```

**After:**
```csharp
// New usage
```

---

## Contributors

Thanks to everyone who contributed to this release:

- @[contributor1]
- @[contributor2]

## Full Changelog

[Compare link: v[previous]...v[current]](link)
```

#### Slack Format

```
:rocket: *Release v[VERSION]* :rocket:

*Highlights:*
[Summary]

*New Features:*
• [Feature 1]
• [Feature 2]

*Bug Fixes:*
• [Fix 1]
• [Fix 2]

:warning: *Breaking Changes:*
• [Change 1]

Full changelog: <link|v[previous]...v[current]>
```

#### Email Format

```
Subject: [Product] v[VERSION] Released

Hi Team,

We're excited to announce the release of [Product] v[VERSION].

KEY HIGHLIGHTS
--------------
[Summary paragraph]

NEW FEATURES
------------
• [Feature 1]: [Description]
• [Feature 2]: [Description]

BUG FIXES
---------
• [Fix 1]
• [Fix 2]

BREAKING CHANGES
----------------
⚠️ [Change 1]: [Migration steps]

UPGRADE INSTRUCTIONS
-------------------
1. [Step 1]
2. [Step 2]

Full changelog: [link]

Best regards,
[Team]
```

### Step 4: Output

1. Write release notes to `docs/releases/v[VERSION].md`
2. If format is slack/email, also output to console
3. Suggest git tag command:
   ```bash
   git tag -a v[VERSION] -m "Release v[VERSION]"
   git push origin v[VERSION]
   ```

## Quality Checklist

- [ ] All commits since last release included
- [ ] Changes properly categorized
- [ ] Breaking changes highlighted with migration path
- [ ] Contributors acknowledged
- [ ] Upgrade guide included for breaking changes
- [ ] Links to PRs/issues included

## Related Commands

- `/team:standup-notes` - Daily progress
- `/ba:sprint-report` - Sprint summary
