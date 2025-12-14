---
name: Test Smells
category: testing
implementations:
  dotnet: ../../implementations/dotnet/xunit-tdd.md#smells
  react: ../../implementations/react/jest-tdd.md#smells
used_by_skills: [xunit-testing-patterns, qa-engineer, code-review-excellence]
---

# Test Smells

> "Tests that are hard to maintain are worse than no tests at all."

## The Principle

Test smells are indicators of problems in test code that make tests less valuable, harder to maintain, or less trustworthy.

## Test Content Smells

### Test Not Testing Anything

A passing test that at first sight appears valid but doesn't test the testee.

**Symptoms:**
- No assertions
- Assertions always pass
- Testing mock returns mock value

### Test Needing Excessive Setup

A test that needs dozens of lines of code to set up its environment.

**Fix:** Extract setup to helper methods, builders, or fixtures.

### Too Large Test / Multiple Scenarios

A valid test that checks more than one feature, or the testee does more than one thing.

**Fix:** Split into multiple focused tests.

### Checking Internals

A test that accesses internals (private/protected members) via reflection.

**Problem:** This is a refactoring killer. Implementation changes break tests.

### Test Only Running on Developer's Machine

A test dependent on the development environment that fails elsewhere.

**Fix:** Use CI to catch these early. Mock environment-specific dependencies.

### Test Checking More than Necessary

A test that checks more than it's dedicated to, especially with mocks or unordered collections.

**Fix:** Assert only what the test name promises.

### Irrelevant Information

Test contains information not relevant to understanding it.

**Fix:** Keep only essential setup visible. Extract rest to helpers.

### Chatty Test

A test that fills the console with text - probably used once to manually check something.

**Fix:** Remove debug output. Use proper logging if needed.

### Test Swallowing Exceptions

A test that catches exceptions and lets the test pass.

**Fix:** Let exceptions propagate or explicitly assert they're thrown.

### Test Not Belonging in Host Test Fixture

A test that tests a completely different subject than other tests in the fixture.

**Fix:** Move to appropriate test class.

### Obsolete Test

A test that checks something no longer required. May prevent cleanup of production code.

**Fix:** Delete it. Version control has the history.

### Hidden Test Functionality

Test functionality hidden in SetUp method, base class, or helper class.

**Fix:** Test should be clear by looking at the test method only.

### Bloated Construction

Construction of dependencies makes test hardly readable.

**Fix:** Extract to helper methods, builders, or use AutoFixture/Bogus.

### Unclear Fail Reason

When test fails, can't tell why from the message.

**Fix:** Use assertion messages. Split test if multiple assertions.

### Conditional Test Logic

Tests with if/else, loops, or try/catch blocks.

**Fix:** Tests should have no branches. Split into separate tests.

### Test Logic in Production Code

Tests depend on special logic in production code (e.g., test flags).

**Fix:** Remove test-specific code from production. Use dependency injection.

### Erratic Test

Sometimes passes, sometimes fails.

**Causes:**
- Shared state between tests
- Time-dependent logic
- Order-dependent tests
- Race conditions

## Faking Smells

### Mixing Stubbing and Expectation Declaration

AAA (Arrange-Act-Assert) violation. Setup stubs mixed with expectations.

**Fix:** Separate stub setup (Arrange) from expectations (Assert).

### Checking Fakes Instead of Testee

Tests that check values returned by fakes. Usually due to excessive fake usage.

**Fix:** Test the actual behavior, not the mocking framework.

### Excessive Fake Usage

Test needs lots of fakes or complex fake setup.

**Fix:** Consider splitting the testee into smaller classes.

## Design for Testability Smells

### Constructor Not Simple

Objects hard to create make fast testing impossible.

**Fix:** Constructor should accept dependencies, not create them.

### Constructor Lifetime Mismatch

Passing dependencies with shorter lifetime than the created object.

**Fix:** Pass only dependencies that live at least as long as the object.

### No Abstraction Layers at System Boundary

Database, file system, web services accessed directly without abstraction.

**Fix:** Use interfaces at boundaries to enable test doubles.

## Test Structure Smells

### No AAA Structure

Test doesn't follow Arrange-Act-Assert pattern. Mixed concerns.

**Fix:** Structure every test as AAA. Never mix blocks.

### Wrong Test Namespace

Tests not in same namespace as production code.

**Convention:** Same namespace makes tests easier to find.

### SetUp for Non-Infrastructure

Using SetUp/TearDown for things under test, not just infrastructure.

**Fix:** Show all parts needed for test in the test method itself.

## How to Detect Test Smells

- Tests that fail randomly
- Tests that take long to understand
- Tests that break when implementation changes (not behavior)
- Tests that no one trusts
- Tests that are commented out

## Related Concepts

- [TDD Principles](tdd-principles.md) - Writing good tests
- [FIRST Principles](first.md) - Test quality
- [Code Smells](../code-smells/taxonomy.md) - Production code smells

## Sources

- xUnit Test Patterns: Refactoring Test Code by Gerard Meszaros
- Clean ATDD/TDD Cheatsheet by Urs Enzler
