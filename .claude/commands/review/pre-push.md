---
description: Fast security scan before git push (< 30s, CRITICAL issues only)
allowed-tools: Read, Glob, Grep
argument-hint: [--no-block] [--base <branch>]
model: haiku
---

# Pre-Push Security Scan

Fast, focused security check before pushing. Blocks only on CRITICAL issues.

**Arguments**: $ARGUMENTS
**Target**: < 30 seconds execution

## Constraints (MUST follow)

1. **NO agent spawning** - Do not use Task tool
2. **NO writing** - Read-only analysis only
3. **NO Bash execution** - Use only Read, Glob, Grep
4. **NO external calls** - No WebFetch, WebSearch
5. **30-second limit** - If analysis incomplete, exit 0 (allow push)
6. **CRITICAL only blocks** - HIGH/MEDIUM/LOW are warnings only
7. **Skip large diffs** - If >200 lines changed, exit 0 with warning

## Behavior

| Condition | Exit Code | Effect |
|-----------|-----------|--------|
| CRITICAL found (blocking mode) | 2 | Blocks push |
| CRITICAL found + `--no-block` | 0 | Warning only |
| HIGH/MEDIUM/LOW found | 0 | Warning only |
| No issues | 0 | Clean pass |
| Error/timeout | 0 | Allow push (fail-safe) |
| >200 lines changed | 0 | Skip with warning |

## Execution

### Step 1: Parse Arguments

```
BASE_BRANCH = --base argument OR "origin/develop"
NO_BLOCK = true if --no-block present
```

### Step 2: Get Changed Files

Use Grep to find changed file list from git status or use Glob to identify recently modified files.

**Classify by extension:**
- Backend: `*.cs`, `*.csproj`
- Frontend: `*.ts`, `*.tsx`, `*.js`, `*.jsx`

### Step 3: Check Scope

**If >20 files OR >200 lines changed:**
```
⚠️  Large diff detected ({N} files, ~{M} lines)
    Skipping pre-push review. Consider smaller commits.

✅ Push allowed (scope too large for fast review)
```
Exit 0 immediately.

### Step 4: Security Scan (Inline Checklist)

Read each changed file and scan for these patterns ONLY:

#### 🔴 CRITICAL (Blocks Push)

| Check | Pattern to Find | Example |
|-------|-----------------|---------|
| Missing Auth | Public mutation method without `[Authorize]` | `public async Task Create(` without auth |
| Hardcoded Secret | `password=`, `apikey=`, `secret=`, connection strings | `"Password=admin123"` |
| SQL Injection | String concat in SQL | `$"SELECT * FROM {table}"` |
| Exposed Credentials | `.env` files, `appsettings.*.json` with real values | Committed secrets |

#### 🟠 HIGH (Warning Only)

| Check | Pattern to Find |
|-------|-----------------|
| Blocking Async | `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` |
| N+1 Pattern | Query/DB call inside `foreach`/`for` loop |
| Any Type (TS) | Explicit `: any` or `as any` |
| Console Secrets | `Console.WriteLine` with password/token variables |

### Step 5: Output Results

**Header:**
```
🔍 Pre-Push Scan: {branch} → {base}
📊 Files: {count} ({backend} backend, {frontend} frontend)
```

**Issues (if any):**
```
🔴 CRITICAL ({count})
─────────────────────────────────
• {file}:{line} - {description}
  → {brief fix}

🟠 HIGH ({count})
─────────────────────────────────
• {file}:{line} - {description}
```

**Verdict:**

CRITICAL found (blocking):
```
═══════════════════════════════════════════
❌ BLOCKED ({N} critical)

Fix critical issues and retry.
To bypass: git push --no-verify
═══════════════════════════════════════════
```

CRITICAL found (--no-block):
```
═══════════════════════════════════════════
⚠️  CRITICAL ISSUES FOUND ({N})

Push allowed (--no-block). Fix before merge.
═══════════════════════════════════════════
```

HIGH only (no CRITICAL):
```
═══════════════════════════════════════════
⚠️  PASSED WITH WARNINGS ({N} high)

Consider fixing before merge.
═══════════════════════════════════════════
```

Clean:
```
═══════════════════════════════════════════
✅ PASSED - No critical issues
═══════════════════════════════════════════
```

### Step 6: Exit

```
IF CRITICAL found AND NOT --no-block:
    EXIT 2
ELSE:
    EXIT 0
```

## Performance Budget

| Phase | Max Time |
|-------|----------|
| Parse args | <1s |
| Get files | <2s |
| Scope check | <1s |
| Security scan | <25s |
| Output | <1s |
| **Total** | **<30s** |

## What This Does NOT Check

- DDD patterns (use full code review)
- Naming conventions (use linter)
- Code style (use formatter)
- Test coverage (use CI)
- Performance optimization (use full review)
- Documentation (use PR review)

## Examples

### Standard scan
```bash
claude -p "/review:pre-push"
```

### Non-blocking (CI mode)
```bash
claude -p "/review:pre-push --no-block"
```

### Against specific branch
```bash
claude -p "/review:pre-push --base origin/main"
```

## Error Recovery

| Error | Action |
|-------|--------|
| Cannot read file | Skip file, continue |
| Timeout approaching | Output partial results, exit 0 |
| Unknown error | Exit 0 (fail-safe) |

---

**Input**: $ARGUMENTS
