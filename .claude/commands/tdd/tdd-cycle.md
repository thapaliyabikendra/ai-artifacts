---
description: Execute TDD workflow with red-green-refactor discipline for ABP/.NET
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "<feature-or-component>" [--incremental] [--suite]
---

# TDD Cycle Command

Execute Test-Driven Development workflow using project agents.

**Arguments**: $ARGUMENTS

## Workflow

```
┌─────────┐   ┌─────────┐   ┌─────────┐
│ 1. RED  │ → │ 2.GREEN │ → │3.REFACTOR│
│ (qa-    │   │ (abp-   │   │ (code-  │
│ engineer│   │developer│   │ reviewer│
└─────────┘   └─────────┘   └─────────┘
     ↑                            │
     └────────────────────────────┘
```

## Phase 1: RED - Write Failing Tests

Use Task tool with `subagent_type="qa-engineer"`:

```
Write FAILING xUnit tests for: {feature-or-component}

Context: Read existing tests in test/ folder
Skills: Apply xunit-testing-patterns

Requirements:
- Tests MUST fail initially (missing implementation)
- Use Arrange-Act-Assert pattern
- Include: happy path, validation, authorization, edge cases
- Use Shouldly for assertions
- Mock dependencies with NSubstitute

Output: Test files in appropriate test project
```

**Checkpoint**: All tests fail with meaningful error messages.

---

## Phase 2: GREEN - Minimal Implementation

Use Task tool with `subagent_type="abp-developer"`:

```
Implement MINIMAL code to make tests pass for: {feature-or-component}

Context: Read docs/architecture/README.md, failing tests
Skills: Apply abp-framework-patterns

Requirements:
- Focus ONLY on making tests green
- No extra features or optimizations
- Follow ABP naming conventions
- Keep methods small and focused

Output: Source code files per test requirements
```

**Checkpoint**: All tests pass. Build succeeds.

---

## Phase 3: REFACTOR - Improve Code Quality

Use Task tool with `subagent_type="code-reviewer"`:

```
Refactor implementation for: {feature-or-component}

Context: Read implementation and tests
Skills: Apply code-review-excellence patterns

Requirements:
- Keep all tests green
- Apply SOLID principles
- Remove duplication
- Improve naming
- Run tests after each change

Checklist:
- [ ] Single responsibility per class/method
- [ ] Proper async/await usage
- [ ] No magic numbers/strings
- [ ] Consistent error handling
```

**Checkpoint**: Tests still pass. Code quality improved.

---

## Modes

### Incremental Mode (`--incremental`)
1. Write ONE failing test
2. Make ONLY that test pass
3. Refactor if needed
4. Repeat

### Suite Mode (`--suite`)
1. Write ALL tests for feature (failing)
2. Implement to pass ALL tests
3. Refactor entire module

## Validation Checklist

### RED Phase
- [ ] Tests written before implementation
- [ ] All tests fail with meaningful errors
- [ ] Failures due to missing implementation

### GREEN Phase
- [ ] All tests pass
- [ ] No extra code beyond requirements
- [ ] Build succeeds

### REFACTOR Phase
- [ ] All tests still pass
- [ ] Code complexity reduced
- [ ] Duplication eliminated

## Coverage Thresholds

- Line coverage: 80%+
- Branch coverage: 75%+
- Critical paths: 100%

## Anti-Patterns

- Writing implementation before tests
- Writing tests that already pass
- Skipping refactor phase
- Modifying tests to make them pass

---

TDD implementation for: $ARGUMENTS
