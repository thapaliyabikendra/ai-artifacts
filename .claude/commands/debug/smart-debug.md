---
description: Debug issues with AI-powered root cause analysis, fix implementation, and verification
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "<error-message-or-description>" [--fix] [--verify]
---

# Smart Debug Command

AI-powered debugging with optional fix and verification workflow.

**Arguments**: $ARGUMENTS

## Workflow Overview

```
┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
│ 1.Diagnose│ → │ 2.Fix     │ → │ 3.Verify  │ → │ 4.Review  │
│ (debugger)│   │ (abp-     │   │ (qa-      │   │ (code-    │
│           │   │ developer)│   │ engineer) │   │ reviewer) │
└───────────┘   └───────────┘   └───────────┘   └───────────┘
```

**Default**: Stage 1 only (diagnosis)
**With `--fix`**: Stages 1-2 (diagnosis + fix)
**With `--verify`**: Stages 1-3 (diagnosis + fix + test)
**With `--full`**: Stages 1-4 (full workflow)

## Context

Process issue from: $ARGUMENTS

Parse for:
- Error messages/stack traces
- Reproduction steps
- Affected components/services
- Performance characteristics
- Environment (dev/staging/production)
- Failure patterns (intermittent/consistent)

## Workflow

### 1. Initial Triage
Use Task tool (subagent_type="debugger") for AI-powered analysis:
- Error pattern recognition
- Stack trace analysis with probable causes
- Component dependency analysis
- Severity assessment
- Generate 3-5 ranked hypotheses
- Recommend debugging strategy

### 2. Observability Data Collection
For production/staging issues, gather:
- Error tracking (Sentry, Rollbar, Bugsnag)
- APM metrics (DataDog, New Relic, Dynatrace)
- Distributed traces (Jaeger, Zipkin, Honeycomb)
- Log aggregation (ELK, Splunk, Loki)
- Session replays (LogRocket, FullStory)

Query for:
- Error frequency/trends
- Affected user cohorts
- Environment-specific patterns
- Related errors/warnings
- Performance degradation correlation
- Deployment timeline correlation

### 3. Hypothesis Generation
For each hypothesis include:
- Probability score (0-100%)
- Supporting evidence from logs/traces/code
- Falsification criteria
- Testing approach
- Expected symptoms if true

Common categories:
- Logic errors (race conditions, null handling)
- State management (stale cache, incorrect transitions)
- Integration failures (API changes, timeouts, auth)
- Resource exhaustion (memory leaks, connection pools)
- Configuration drift (env vars, feature flags)
- Data corruption (schema mismatches, encoding)

### 4. Strategy Selection
Select based on issue characteristics:

**Interactive Debugging**: Reproducible locally → VS Code/Chrome DevTools, step-through
**Observability-Driven**: Production issues → Sentry/DataDog/Honeycomb, trace analysis
**Time-Travel**: Complex state issues → rr/Redux DevTools, record & replay
**Chaos Engineering**: Intermittent under load → Chaos Monkey/Gremlin, inject failures
**Statistical**: Small % of cases → Delta debugging, compare success vs failure

### 5. Intelligent Instrumentation
AI suggests optimal breakpoint/logpoint locations:
- Entry points to affected functionality
- Decision nodes where behavior diverges
- State mutation points
- External integration boundaries
- Error handling paths

Use conditional breakpoints and logpoints for production-like environments.

### 6. Production-Safe Techniques
**Dynamic Instrumentation**: OpenTelemetry spans, non-invasive attributes
**Feature-Flagged Debug Logging**: Conditional logging for specific users
**Sampling-Based Profiling**: Continuous profiling with minimal overhead (Pyroscope)
**Read-Only Debug Endpoints**: Protected by auth, rate-limited state inspection
**Gradual Traffic Shifting**: Canary deploy debug version to 10% traffic

### 7. Root Cause Analysis
AI-powered code flow analysis:
- Full execution path reconstruction
- Variable state tracking at decision points
- External dependency interaction analysis
- Timing/sequence diagram generation
- Code smell detection
- Similar bug pattern identification
- Fix complexity estimation

### 8. Fix Implementation (--fix flag)

If `--fix` flag provided, use Task tool with `subagent_type="abp-developer"`:

```
Implement fix for the diagnosed issue.

Input: Root cause analysis from Stage 1
Context: Read docs/architecture/README.md, examine affected code
Skills: Apply abp-framework-patterns, error-handling-patterns

Requirements:
- Minimal change to fix the issue
- Follow existing code patterns
- Add logging for the fix
- Consider edge cases
```

**Checkpoint**: Fix implemented, build succeeds.

### 9. Verification (--verify flag)

If `--verify` flag provided, use Task tool with `subagent_type="qa-engineer"`:

```
Verify the fix and add regression test.

Input: Fix implementation from Stage 2
Context: Read existing tests, understand the bug
Skills: Apply xunit-testing-patterns

Requirements:
- Add regression test for the bug
- Verify fix doesn't break existing tests
- Test edge cases identified in diagnosis
```

**Checkpoint**: Tests pass, regression test added.

### 10. Code Review (--full flag)

If `--full` flag provided, use Task tool with `subagent_type="abp-code-reviewer"`:

```
Review the fix implementation.

Input: All changed files
Context: Read docs/architecture/patterns.md
Skills: Apply code-review-excellence

Checklist: Minimal change, no side effects, proper error handling.
```

**Checkpoint**: No critical issues.

### 11. Validation (Manual)
- Run test suite
- Performance comparison (baseline vs fix)
- Canary deployment (monitor error rate)
- AI code review of fix

Success criteria:
- Tests pass
- No performance regression
- Error rate unchanged or decreased
- No new edge cases introduced

### 10. Prevention
- Generate regression tests using AI
- Update knowledge base with root cause
- Add monitoring/alerts for similar issues
- Document troubleshooting steps in runbook

## Example: Minimal Debug Session

```typescript
// Issue: "Checkout timeout errors (intermittent)"

// 1. Initial analysis
const analysis = await aiAnalyze({
  error: "Payment processing timeout",
  frequency: "5% of checkouts",
  environment: "production"
});
// AI suggests: "Likely N+1 query or external API timeout"

// 2. Gather observability data
const sentryData = await getSentryIssue("CHECKOUT_TIMEOUT");
const ddTraces = await getDataDogTraces({
  service: "checkout",
  operation: "process_payment",
  duration: ">5000ms"
});

// 3. Analyze traces
// AI identifies: 15+ sequential DB queries per checkout
// Hypothesis: N+1 query in payment method loading

// 4. Add instrumentation
span.setAttribute('debug.queryCount', queryCount);
span.setAttribute('debug.paymentMethodId', methodId);

// 5. Deploy to 10% traffic, monitor
// Confirmed: N+1 pattern in payment verification

// 6. AI generates fix
// Replace sequential queries with batch query

// 7. Validate
// - Tests pass
// - Latency reduced 70%
// - Query count: 15 → 1
```

## Output Format

Provide structured report:
1. **Issue Summary**: Error, frequency, impact
2. **Root Cause**: Detailed diagnosis with evidence
3. **Fix Proposal**: Code changes, risk, impact
4. **Validation Plan**: Steps to verify fix
5. **Prevention**: Tests, monitoring, documentation

Focus on actionable insights. Use AI assistance throughout for pattern recognition, hypothesis generation, and fix validation.

## Options

| Option | Stages | Description |
|--------|--------|-------------|
| (default) | 1 | Diagnosis only |
| `--fix` | 1-2 | Diagnosis + fix implementation |
| `--verify` | 1-3 | Diagnosis + fix + test verification |
| `--full` | 1-4 | Full workflow with code review |

## Output Summary

```
## Bug Fix: {issue-description}

### Diagnosis
- Root Cause: [description]
- Affected Files: [list]
- Risk Level: Low/Medium/High

### Fix (if --fix)
- Files Changed: [list]
- Build Status: Pass/Fail

### Verification (if --verify)
- Tests Added: [count]
- Test Status: Pass/Fail

### Review (if --full)
- Issues Found: [count]
- Recommendations: [list]
```

---

Issue to debug: $ARGUMENTS
