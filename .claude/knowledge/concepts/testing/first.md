---
name: FIRST Principles
category: testing
implementations:
  dotnet: ../../implementations/dotnet/xunit-tdd.md#first
  react: ../../implementations/react/jest-tdd.md#first
used_by_skills: [xunit-testing-patterns, qa-engineer]
---

# FIRST Principles

> "Unit tests have to be fast in order to be executed often."

## The Principle

FIRST is an acronym for five principles that guide good unit test design:

| Letter | Principle | Summary |
|--------|-----------|---------|
| **F** | Fast | Tests run quickly |
| **I** | Isolated | Tests are independent |
| **R** | Repeatable | Same result every time |
| **S** | Self-Validating | Pass/fail without manual inspection |
| **T** | Timely | Written at the right time |

## The Five Principles

### Fast

Unit tests have to be fast in order to be executed often.

**What is fast?**
- Much smaller than seconds
- Entire test suite in minutes, not hours
- Individual tests in milliseconds

**Why it matters:**
- Slow tests don't get run
- Slow feedback discourages TDD
- CI/CD becomes bottleneck

**How to achieve:**
- No database access in unit tests
- No network calls
- No file system operations
- Mock external dependencies

### Isolated

Two meanings of isolation:

**1. Isolated testee:** Clear where the failure happened. If a test fails, you know exactly which component is broken.

**2. Isolated tests:** No dependency between tests. Tests can run in any order, in parallel, and produce the same results.

**Why it matters:**
- Flaky tests erode confidence
- Order-dependent tests hide bugs
- Parallel execution speeds CI/CD

**How to achieve:**
- No shared mutable state
- Each test sets up its own data
- No test depends on another's output

### Repeatable

No assumed initial state, nothing left behind, no dependency on external services that might be unavailable.

**Same environment requirements:**
- Same result on any machine
- Same result at any time
- Same result in any order

**Why it matters:**
- "Works on my machine" is not acceptable
- Tests must work in CI/CD
- Non-repeatable tests are useless

**How to achieve:**
- Don't depend on databases
- Don't depend on file system state
- Don't depend on current date/time (inject clock)
- Don't depend on random values (seed them)

### Self-Validating

No manual test interpretation or intervention. Red or green!

**What it means:**
- Test asserts its own correctness
- No console output to inspect
- No comparing files manually
- Automated pass/fail

**Why it matters:**
- Manual inspection doesn't scale
- Humans miss things
- Automated CI/CD needs automated validation

**How to achieve:**
- Always include assertions
- Assert specific expected values
- Don't just "not throw"

### Timely

Tests are written at the right time.

**The right times:**
- TDD: Before the code
- DDT: When fixing a bug
- POUT: Adding to existing code

**Why it matters:**
- Tests written after are harder to write
- Tests written after may not cover edge cases
- Tests written after may be biased by implementation

**The best time:**
- Before the code (TDD)
- But any time is better than no time

## How to Detect Violations

| Principle | Violation Signs |
|-----------|-----------------|
| Fast | Tests take seconds each |
| Isolated | Tests fail randomly, or only in certain order |
| Repeatable | Tests fail on CI but pass locally |
| Self-Validating | Need to check console output |
| Timely | Tests written long after code |

## Related Concepts

- [TDD Principles](tdd-principles.md) - TDD workflow
- [Test Smells](test-smells.md) - Test anti-patterns
- [Design for Testability](../clean-code/principles.md) - Writing testable code

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [FIRST in xUnit](../../implementations/dotnet/xunit-tdd.md#first) |
| React | [FIRST in Jest](../../implementations/react/jest-tdd.md#first) |

## Sources

- Clean Code by Robert C. Martin
- Clean ATDD/TDD Cheatsheet by Urs Enzler
