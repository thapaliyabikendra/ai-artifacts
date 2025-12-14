# Pre-Push Scan Output Templates

Simplified terminal output for fast pre-push security scan.

---

## Header

```
🔍 Pre-Push Scan: {BRANCH} → {BASE_BRANCH}
📊 Files: {FILE_COUNT} ({BACKEND_COUNT} backend, {FRONTEND_COUNT} frontend)
```

---

## Issues Format

### Critical Issues

```
🔴 CRITICAL ({COUNT})
─────────────────────────────────
• {FILE}:{LINE} - {DESCRIPTION}
  → {BRIEF_FIX}

• {FILE}:{LINE} - {DESCRIPTION}
  → {BRIEF_FIX}
```

### High Issues

```
🟠 HIGH ({COUNT})
─────────────────────────────────
• {FILE}:{LINE} - {DESCRIPTION}
```

---

## Verdict Banners

### Blocked (CRITICAL found, blocking mode)

```
═══════════════════════════════════════════
❌ BLOCKED ({CRITICAL_COUNT} critical)

Fix critical issues and retry.
To bypass: git push --no-verify
═══════════════════════════════════════════
```

### Critical Warning (--no-block mode)

```
═══════════════════════════════════════════
⚠️  CRITICAL ISSUES FOUND ({CRITICAL_COUNT})

Push allowed (--no-block). Fix before merge.
═══════════════════════════════════════════
```

### Passed with Warnings (HIGH only)

```
═══════════════════════════════════════════
⚠️  PASSED WITH WARNINGS ({HIGH_COUNT} high)

Consider fixing before merge.
═══════════════════════════════════════════
```

### Clean Pass

```
═══════════════════════════════════════════
✅ PASSED - No critical issues
═══════════════════════════════════════════
```

---

## Special Cases

### Nothing to Review

```
═══════════════════════════════════════════
✅ No changes to review

Working tree matches base branch.
═══════════════════════════════════════════
```

### Scope Too Large

```
⚠️  Large diff detected ({N} files, ~{M} lines)
    Skipping pre-push review. Consider smaller commits.

✅ Push allowed (scope too large for fast review)
```

---

## Error Messages

### Timeout

```
⏱️  Scan incomplete (approaching 30s limit)

Partial results shown. Push allowed.
```

### File Read Error

```
⚠️  Could not read: {FILE}
    Skipping this file.
```
