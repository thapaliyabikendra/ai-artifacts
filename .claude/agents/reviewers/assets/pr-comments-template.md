# GitHub PR Review Comments Template

Use this template to generate consistent, actionable PR review comments.

---

## Header Template

```markdown
# Code Review: {PR_TITLE}

**PR:** {BRANCH_NAME}
**Status:** {🔴 Changes Requested | 💬 Approve with Comments | ✅ Approve}
**Date:** {YYYY-MM-DD}
**Reviewer:** abp-code-reviewer

---

## Summary

Reviewed {COMMIT_COUNT} commits introducing {FEATURE_DESCRIPTION}. Found **{CRITICAL_COUNT} critical**, **{HIGH_COUNT} high**, and **{MEDIUM_COUNT} medium** priority issues.

**Action Required:** {SUMMARY_ACTION}

---
```

## Issue Summary Table

```markdown
## Issue Summary

| Severity | Count | Blocking |
|----------|-------|----------|
| 🔴 CRITICAL | {N} | Yes |
| 🟠 HIGH | {N} | Yes |
| 🟡 MEDIUM | {N} | No |
| 🟢 LOW | {N} | No |
```

## File Comment Template

```markdown
### `{FILE_PATH}`

---

**Line {LINE_NUMBER}** | {🔴 CRITICAL | 🟠 HIGH | 🟡 MEDIUM | 🟢 LOW} | {CATEGORY}

```{language}
{PROBLEMATIC_CODE}
```

> {ICON} **{ISSUE_TITLE}** - {BRIEF_DESCRIPTION}
>
> **Suggested fix:**
> ```{language}
> {FIXED_CODE}
> ```

---
```

## Category Icons

| Category | Icon | Description |
|----------|------|-------------|
| Security | ⚠️ | Authorization, secrets, PII |
| Performance | ⚡ | N+1, async, queries |
| DDD | 🏗️ | Entity patterns, encapsulation |
| ABP | 📦 | Framework patterns |
| Validation | ✅ | FluentValidation |
| Code Quality | 🧹 | Clean code issues |
| Privacy | 🔒 | PII, logging |

## Severity Badges

| Severity | Badge | Criteria |
|----------|-------|----------|
| CRITICAL | 🔴 | Security vulnerabilities, data loss |
| HIGH | 🟠 | Bugs, missing auth, performance blockers |
| MEDIUM | 🟡 | Code quality, minor bugs |
| LOW | 🟢 | Style, suggestions |

## Review Decision Section

```markdown
## Review Decision

{🔴 **Changes Requested** | 💬 **Approve with Comments** | ✅ **Approved**}

Please address:
- [ ] All {CRITICAL_COUNT} CRITICAL issues (security, validation, performance)
- [ ] All {HIGH_COUNT} HIGH issues (patterns, code quality)
- [ ] At least the security-related MEDIUM issues

Once fixed, please re-request review.
```

## Security Summary Section

```markdown
## 🔒 Security Summary

| Check | Status | Notes |
|-------|--------|-------|
| Authorization | {✅ Pass | ❌ Fail} | {details} |
| Input Validation | {✅ Pass | ❌ Fail} | {details} |
| Data Exposure | {✅ Pass | ❌ Fail} | {details} |
| Secrets | {✅ Pass | ❌ Fail} | {details} |
| PII Logging | {✅ Pass | ❌ Fail} | {details} |
```

## Performance Summary Section

```markdown
## ⚡ Performance Summary

| Check | Status | Notes |
|-------|--------|-------|
| N+1 Queries | {✅ Pass | ❌ Fail} | {details} |
| Async Patterns | {✅ Pass | ❌ Fail} | {details} |
| Pagination | {✅ Pass | ❌ Fail} | {details} |
| Query Optimization | {✅ Pass | ❌ Fail} | {details} |
```

## Positive Observations Section

```markdown
## ✅ What's Good

- {Positive observation 1}
- {Positive observation 2}
- {Positive observation 3}
```

## Resources Section

```markdown
## Helpful Resources

- [ABP Authorization Docs](https://docs.abp.io/en/abp/latest/Authorization)
- [FluentValidation Docs](https://docs.fluentvalidation.net/)
- [ABP Unit of Work](https://docs.abp.io/en/abp/latest/Unit-Of-Work)
- [EF Core Query Performance](https://learn.microsoft.com/en-us/ef/core/performance/efficient-querying)
```

---

## Complete Example

```markdown
# Code Review: Add Patient CRUD API

**PR:** feat/patient-crud
**Status:** 🔴 Changes Requested
**Date:** 2025-12-14
**Reviewer:** abp-code-reviewer

---

## Summary

Reviewed 5 commits introducing patient management API. Found **1 critical**, **2 high**, and **3 medium** priority issues.

**Action Required:** Please address all CRITICAL and HIGH issues before merge.

---

## Issue Summary

| Severity | Count | Blocking |
|----------|-------|----------|
| 🔴 CRITICAL | 1 | Yes |
| 🟠 HIGH | 2 | Yes |
| 🟡 MEDIUM | 3 | No |
| 🟢 LOW | 1 | No |

---

### `src/Application/PatientAppService.cs`

---

**Line 67** | 🔴 CRITICAL | Security

```csharp
public async Task DeleteAsync(Guid id)
{
    await _repository.DeleteAsync(id);
}
```

> ⚠️ **Missing authorization on DeleteAsync** - Any authenticated user can delete patients without permission check.
>
> **Suggested fix:**
> ```csharp
> [Authorize(Permissions.Patients.Delete)]
> public async Task DeleteAsync(Guid id)
> {
>     await _repository.DeleteAsync(id);
> }
> ```

---

## 🔒 Security Summary

| Check | Status | Notes |
|-------|--------|-------|
| Authorization | ❌ Fail | DeleteAsync missing `[Authorize]` |
| Input Validation | ✅ Pass | FluentValidation in place |
| Data Exposure | ✅ Pass | DTOs properly scoped |
| Secrets | ✅ Pass | No hardcoded values |

---

## ✅ What's Good

- Excellent entity encapsulation with private setters
- Proper use of `GuidGenerator.Create()`
- Clean FluentValidation implementation

---

## Review Decision

🔴 **Changes Requested**

Please address:
- [ ] All 1 CRITICAL issues
- [ ] All 2 HIGH issues

Once fixed, please re-request review.
```
