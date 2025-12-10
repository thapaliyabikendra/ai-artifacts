# Context Isolation in Sub-Agents

## What is Context Isolation?

Sub-agents operate in their **own context window**, completely separate from the main conversation. This architectural decision provides significant benefits for performance and cost optimization.

## Key Benefits

### 1. Prevents Context Pollution
When a sub-agent performs extensive exploration or analysis, all that intermediate work stays in its own context. The main session only receives the final result, keeping the main context clean and focused.

### 2. Faster Responses
With a smaller, focused context window, the main session processes requests more quickly without being slowed down by irrelevant information from sub-agent operations.

### 3. Lower Costs
Context windows consume tokens. By isolating complex operations to sub-agents, you only pay for the relevant results that get passed back to the main session, not all the intermediate steps.

### 4. Parallel Efficiency
Multiple sub-agents can work simultaneously in their own contexts without interfering with each other or bloating the main context.

## How It Works

```
┌─────────────────────────────────────┐
│     Main Session Context            │
│  • User conversation                │
│  • High-level task coordination     │
│  • Final results from sub-agents    │
└──────────────┬──────────────────────┘
               │ spawns
               ▼
    ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
    │  Sub-Agent 1     │      │  Sub-Agent 2     │      │  Sub-Agent 3     │
    │  Context         │      │  Context         │      │  Context         │
    │                  │      │                  │      │                  │
    │ • Tool calls     │      │ • Tool calls     │      │ • Tool calls     │
    │ • File reads     │      │ • Analysis       │      │ • Code changes   │
    │ • Exploration    │      │ • Searches       │      │ • Testing        │
    └──────────────────┘      └──────────────────┘      └──────────────────┘
         │ returns                  │ returns                  │ returns
         └──────────────────────────┴──────────────────────────┘
                           Only final results
```

## Best Practices

### When to Use Sub-Agents for Context Isolation

✅ **DO use sub-agents when:**
- Task involves extensive codebase exploration (many file reads, searches)
- Multiple iterations or attempts may be needed
- Work can be parallelized across multiple agents
- You want to keep the main conversation focused on high-level coordination

❌ **DON'T use sub-agents when:**
- Task is simple and can be done in 1-2 tool calls
- User needs to see all intermediate steps
- Context from main conversation is essential and can't be summarized

### Passing Context Efficiently

When spawning a sub-agent, provide only the essential context:

**Good** (concise):
```
Task: Implement user authentication following the TSD in docs/technical-specification.md
Focus on JWT-based auth with refresh tokens
```

**Bad** (over-detailed):
```
Task: The user wants authentication and we discussed JWT vs session-based
and decided on JWT because it's stateless and we need refresh tokens
for security and the TSD has the details and we should follow ABP patterns...
```

## Context Isolation vs Skills

| Aspect | Sub-Agent (Context Isolation) | Skill (Shared Context) |
|--------|-------------------------------|------------------------|
| **Context** | Separate window | Main conversation window |
| **Best for** | Complex, multi-step tasks | Adding domain knowledge |
| **Token cost** | Isolated (only results passed back) | Shared (entire skill content loaded) |
| **Use when** | Heavy exploration or iteration needed | Expertise or workflow guidance needed |

## Example Scenarios

### Scenario 1: Code Review
**Without context isolation** (main session):
- Reads 20+ files
- Searches for patterns
- Analyzes dependencies
- Main context grows to 50k+ tokens

**With context isolation** (sub-agent):
- Sub-agent does all the exploration in its context
- Returns only: "✅ Review complete. Found 3 issues: [list]"
- Main context stays small and focused

### Scenario 2: Parallel Feature Implementation
**Three sub-agents in parallel**:
1. `backend-architect`: Designs API (reads specs, explores patterns)
2. `security-engineer`: Audits auth (scans code, checks vulnerabilities)
3. `qa-engineer`: Creates tests (analyzes requirements, writes test plan)

Each operates independently. Main session receives three clean reports without the noise of 100+ tool calls polluting its context.

## Monitoring Sub-Agent Context

While sub-agents work in isolation, you can still:
- Check their progress with `AgentOutputTool`
- Review their final output when complete
- Resume them if additional work is needed using the `resume` parameter

The isolation is about **efficiency**, not **opacity**. You maintain full visibility and control.
