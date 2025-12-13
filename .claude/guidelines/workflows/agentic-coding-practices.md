# Agentic Coding Best Practices

> Extracted from GUIDELINES.md. Best practices from Anthropic's official recommendations.

## The Agentic Feedback Loop

Claude operates in a fundamental loop:

```
┌─────────────────────────────────────────────────────────────┐
│     GATHER CONTEXT → TAKE ACTION → VERIFY WORK → REPEAT    │
└─────────────────────────────────────────────────────────────┘
```

This pattern enables autonomous completion of complex workflows through iterative refinement.

## Thinking Modes

Trigger extended thinking with specific phrases:

| Phrase | Thinking Level | When to Use |
|--------|----------------|-------------|
| `"think"` | Baseline | Standard complex tasks |
| `"think hard"` | Increased | Multi-step reasoning |
| `"think harder"` | High | Complex architectural decisions |
| `"ultrathink"` | Maximum | Critical, high-stakes decisions |

**Example**: "Think hard about the best approach to refactor this authentication system."

## Effective Workflows

### 1. Explore → Plan → Code → Commit

```
1. Ask Claude to read relevant files without writing code
2. Request a plan (use "think" for extended thinking)
3. Ask Claude to implement the solution
4. Request commit and PR creation
```

### 2. Test-Driven Development (TDD)

```
1. Write tests based on expected input/output pairs
2. Confirm tests fail (without implementation code)
3. Commit tests
4. Ask Claude to write passing code, iterating until all tests pass
5. Commit successful code
```

**Key**: Be explicit about TDD to prevent mock implementations.

### 3. Visual Iteration

```
1. Provide screenshot tools (Puppeteer MCP, manual capture)
2. Provide design mock
3. Ask Claude to implement, take screenshots, iterate
4. Commit when satisfied
```

## Prompting Best Practices

**Be specific** - Specificity significantly improves first-attempt success rates.

| Poor | Good |
|------|------|
| "add tests for foo.py" | "write a new test case for foo.py, covering the edge case where the user is logged out. avoid mocks" |
| "fix the bug" | "fix the null reference exception in UserService.GetById when user doesn't exist" |
| "improve performance" | "optimize the N+1 query in OrderRepository.GetWithItems using Include" |

## Context Preservation Techniques

| Technique | How |
|-----------|-----|
| **Mention files directly** | Use tab-completion to reference specific files |
| **Provide images** | Paste screenshots, drag-drop, or provide file paths |
| **Include URLs** | Paste links for Claude to fetch |
| **Use `/clear` frequently** | Reset context between tasks |

## Subagent Usage

Use subagents for:
- **Parallelization**: Multiple subagents handle different tasks simultaneously
- **Context isolation**: Each operates in its own context window
- **Information-heavy tasks**: Where most data proves irrelevant to main thread

**Best practice**: Delegate research and investigation tasks to subagents early.

## Multi-Claude Workflows

### Parallel Code Review
Have one Claude write code; another reviews/tests it. Separate contexts yield better results.

### Multiple Worktrees
Run 3-4 Claude sessions on independent tasks:

```bash
# Create worktree
git worktree add ../project-feature-a feature-a

# Launch Claude in worktree
cd ../project-feature-a && claude

# Clean up when done
git worktree remove ../project-feature-a
```

## Complex Tasks with Checklists

For large tasks with multiple steps, use a Markdown checklist:

```markdown
Task Progress:
- [ ] Step 1: Analyze the form
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Execute operation
- [ ] Step 5: Verify output
```

## CLAUDE.md Optimization

Your `CLAUDE.md` files should document:
- Common bash commands
- Core files and utility functions
- Code style guidelines
- Testing instructions
- Repository etiquette
- Developer environment setup
- Project-specific warnings

**Placement options**:
- Repo root (primary)
- Parent directories (monorepos)
- Child directories (subdirectory-specific)
- `~/.claude/CLAUDE.md` (global)

## Related

- [Context Efficiency](../patterns/context-efficiency.md)
- [Creating Artifacts](creating-artifacts.md)
- [GUIDELINES.md](../../GUIDELINES.md)

## Sources

- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
