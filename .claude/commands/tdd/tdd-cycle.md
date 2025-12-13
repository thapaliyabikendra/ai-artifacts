---
description: Execute TDD workflow with red-green-refactor discipline for ABP/.NET
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "<feature-or-component>" [--phase red|green|refactor] [--incremental]
---

# TDD Cycle Command

Execute Test-Driven Development workflow with optional phase selection.

**Arguments**: $ARGUMENTS

## Workflow

```
┌─────────┐   ┌─────────┐   ┌──────────┐
│ 1. RED  │ → │ 2.GREEN │ → │3.REFACTOR│
│ (qa-    │   │ (abp-   │   │ (code-   │
│ engineer│   │developer│   │ reviewer)│
└─────────┘   └─────────┘   └──────────┘
     ↑                            │
     └────────────────────────────┘
```

## Mode Selection

| Option | Phases | Use When |
|--------|--------|----------|
| (default) | Red → Green → Refactor | Full TDD cycle |
| `--phase red` | Red only | Write failing tests first |
| `--phase green` | Green only | Implement to pass existing tests |
| `--phase refactor` | Refactor only | Improve code quality |
| `--incremental` | One test at a time | Fine-grained TDD |

---

## Phase 1: RED - Write Failing Tests

Use Task tool with `subagent_type="qa-engineer"`:

```
Write FAILING xUnit tests for: {feature-or-component}

Context: Read existing tests in test/ folder
Skills: Apply xunit-testing-patterns

Requirements:
- Tests MUST fail initially (missing implementation)
- Use Arrange-Act-Assert pattern
- Should_ExpectedBehavior_When_Condition naming
- Include: happy path, validation, authorization, edge cases
- Use Shouldly for assertions
- Mock dependencies with NSubstitute

Coverage Categories:
1. Happy Path - Normal successful operations
2. Validation - Invalid inputs, missing required fields
3. Authorization - Permission checks, role-based access
4. Edge Cases - Empty collections, boundary values, nulls

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

Use Task tool with `subagent_type="abp-code-reviewer"`:

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

Code Smell Detection:
| Smell | Refactoring |
|-------|-------------|
| Duplicated code | Extract method/class |
| Long method | Decompose into focused methods |
| Large class | Split responsibilities |
| Long parameter list | Parameter object/DTO |

Checklist:
- [ ] Single responsibility per class/method
- [ ] Proper async/await usage
- [ ] No magic numbers/strings
- [ ] Consistent error handling
```

**Checkpoint**: Tests still pass. Code quality improved.

---

## Incremental Mode (`--incremental`)

1. Write ONE failing test
2. Make ONLY that test pass
3. Refactor if needed
4. Repeat for next test

---

## Validation Checklist

| Phase | Criteria |
|-------|----------|
| RED | Tests fail with meaningful errors, failures due to missing implementation |
| GREEN | All tests pass, no extra code beyond requirements, build succeeds |
| REFACTOR | All tests still pass, code complexity reduced, duplication eliminated |

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

TDD target: $ARGUMENTS
