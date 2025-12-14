---
name: TDD Principles
category: testing
implementations:
  dotnet: ../../implementations/dotnet/xunit-tdd.md
  react: ../../implementations/react/jest-tdd.md
used_by_skills: [xunit-testing-patterns, qa-engineer]
---

# TDD Principles

> "Red - Green - Refactor. Test a little - code a little."

## The Principle

Test-Driven Development (TDD) is a software development process where you write tests before writing the code that makes them pass. The cycle is:

1. **Red** - Write a failing test
2. **Green** - Write minimal code to pass
3. **Refactor** - Improve code while keeping tests green

## Types of Test-Driven Development

### TDD - Test Driven Development

Write tests before implementation. Red → Green → Refactor.

### ATDD - Acceptance Test Driven Development

Specify a feature first with a test, then implement. Acceptance tests drive TDD tests.

### DDT - Defect Driven Testing

Write a unit test that reproduces the defect, fix the code, test succeeds, defect never returns.

### POUTing - Plain Old Unit Testing

Test after implementation. Use to add tests to existing code or add additional edge cases after TDDing.

## TDD Principles

### A Test Checks One Feature

A test checks exactly one feature of the testee. This includes all things in that feature but not more. Tests serve as samples and documentation.

### Tiny Steps

Make tiny steps. Add only a little code in test before writing required production code. Add only one assert per step.

### Keep Tests Simple

Whenever a test gets complicated, check whether you can split the testee into several classes (Single Responsibility Principle).

### Prefer State Verification to Behaviour Verification

Use behavior verification only if there is no state to verify. Refactoring is easier due to less coupling to implementation.

### Test Domain Specific Language

Use test DSLs to simplify reading tests:
- Builders to create test data using fluent APIs
- Assertion helpers for concise assertions

## Red Bar Patterns

### One Step Test

Pick a test you are confident you can implement and which maximizes learning effect.

### Partial Test

Write a test that doesn't fully check required behavior, but brings you a step closer.

### Extend Test

Extend an existing test to better match real-world scenarios.

### Another Test

If you think of new tests, write them on the TODO list and don't lose focus on current test.

### Learning Test

Write tests against external components to make sure they behave as expected.

## Green Bar Patterns

### Fake It ('Til You Make It)

Return a constant to get the first test running. Refactor later.

### Triangulate - Drive Abstraction

Write tests with at least two sets of sample data. Abstract implementation based on these.

### Obvious Implementation

If the implementation is obvious, just implement it and see if test runs. If not, step back to Fake It.

### One to Many - Drive Collection Operations

First implement operation for a single element. Then step to several elements (and no elements).

## The TDD Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                        TDD CYCLE                             │
│                                                             │
│    ┌──────────┐     ┌──────────┐     ┌──────────┐          │
│    │   RED    │────►│  GREEN   │────►│ REFACTOR │          │
│    │          │     │          │     │          │          │
│    │  Write   │     │  Write   │     │  Clean   │          │
│    │ failing  │     │ minimal  │     │   code   │          │
│    │  test    │     │  code    │     │          │          │
│    └──────────┘     └──────────┘     └────┬─────┘          │
│         ▲                                  │                │
│         └──────────────────────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## How to Detect TDD Process Smells

- Using code coverage as a goal (not a guide)
- No green bar in the last ~10 minutes
- Not running test before writing production code
- Not spending enough time on refactoring
- Skipping something "too easy to test"
- Skipping something "too hard to test"
- Organizing tests around methods, not behavior

## Related Concepts

- [FIRST Principles](first.md) - Test quality principles
- [Test Smells](test-smells.md) - Test anti-patterns
- [Test Pyramid](test-pyramid.md) - Test distribution
- [Clean Code Principles](../clean-code/principles.md) - Quality code

## Implementations

| Language | Guide |
|----------|-------|
| C#/.NET | [TDD with xUnit](../../implementations/dotnet/xunit-tdd.md) |
| React | [TDD with Jest](../../implementations/react/jest-tdd.md) |

## Sources

- Test Driven Development: By Example by Kent Beck
- Clean ATDD/TDD Cheatsheet by Urs Enzler
