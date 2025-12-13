# Orchestration Patterns for Multi-Agent Systems

## Overview

The orchestrator (master agent) coordinates specialized sub-agents using different patterns based on task requirements. This document covers the two primary orchestration strategies and when to use each.

---

## Pattern 1: Parallel Execution (Fan-Out/Fan-In)

### When to Use
- Multiple independent analyses needed
- Time-sensitive tasks that can run concurrently
- Information gathering phase before decision-making
- No dependencies between sub-agent tasks

### How It Works

```
                    ┌────────────────┐
                    │  Orchestrator  │
                    │ (Main Session) │
                    └───────┬────────┘
                            │ spawns all at once
         ┌──────────────────┼──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ backend-        │ │ security-       │ │ qa-             │
│ architect       │ │ engineer        │ │ engineer        │
│                 │ │                 │ │                 │
│ Designs TSD     │ │ Audits security │ │ Plans tests     │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┴───────────────────┘
                            │ all complete
                            ▼
                    ┌────────────────┐
                    │  Orchestrator  │
                    │ Consolidates   │
                    │ all outputs    │
                    └────────────────┘
```

### Example Use Cases

**1. Requirements Analysis Phase**
```
Orchestrator spawns:
├── product-manager     → Analyzes business requirements
├── backend-architect   → Explores technical feasibility
└── security-engineer   → Identifies security concerns

Consolidation: Combined analysis report with recommendations
```

**2. Pre-Implementation Review**
```
Orchestrator spawns:
├── abp-code-reviewer   → Reviews existing backend patterns
├── security-engineer   → Checks for vulnerabilities
└── qa-engineer        → Analyzes test coverage

Consolidation: Go/no-go decision with action items
```

**3. Codebase Exploration**
```
Orchestrator spawns:
├── backend-explorer    → Maps API structure
├── frontend-explorer   → Maps UI components
└── database-explorer   → Maps schema relationships

Consolidation: Complete system architecture map
```

### Implementation Tips

1. **Spawn all agents in a single message** with multiple Task tool calls
2. **Use consistent prompt format** for each agent
3. **Set clear scope** for each agent to prevent overlap
4. **Use AgentOutputTool** to monitor progress if needed
5. **Consolidate systematically** - create a structured summary

---

## Pattern 2: Sequential Pipeline (Chained Execution)

### When to Use
- Linear workflow where each step depends on previous output
- Progressive refinement needed
- Clear handoff points between stages
- Outputs must build on each other

### How It Works

```
┌────────────────┐
│ Orchestrator   │
│ Spawns Agent 1 │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ backend-       │
│ architect      │ ──► Writes TSD to docs/technical-specification.md
└───────┬────────┘
        │ complete
        ▼
┌────────────────┐
│ Orchestrator   │
│ Spawns Agent 2 │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ abp-developer  │ ──► Reads TSD, implements code
└───────┬────────┘
        │ complete
        ▼
┌────────────────┐
│ Orchestrator   │
│ Spawns Agent 3 │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ qa-engineer    │ ──► Reads TSD + Code, writes tests
└───────┬────────┘
        │ complete
        ▼
┌────────────────┐
│ devops-        │
│ engineer       │ ──► Reads all artifacts, creates deployment
└────────────────┘
```

### Example Use Cases

**1. Feature Development Pipeline**
```
1. product-manager      → Creates BRD with user stories
   └─► Writes: docs/business-requirements.md

2. backend-architect    → Reads BRD, designs technical solution
   └─► Writes: docs/technical-specification.md

3. abp-developer        → Reads TSD, implements backend
   └─► Writes: Code files + updates docs/dev-progress.md

4. react-developer      → Reads TSD + API contracts, implements UI
   └─► Writes: UI files + updates docs/dev-progress.md

5. qa-engineer          → Reads BRD + TSD + Code, writes tests
   └─► Writes: Test files + docs/test-cases.md

6. devops-engineer      → Reads all artifacts, prepares release
   └─► Writes: docs/releases.md + deployment configs
```

**2. Bug Fix Pipeline**
```
1. debugger            → Identifies root cause
   └─► Writes: docs/bug-analysis.md

2. abp-developer       → Implements fix based on analysis
   └─► Writes: Fixed code

3. qa-engineer         → Verifies fix and adds regression test
   └─► Writes: Test cases

4. abp-code-reviewer   → Reviews changes for quality
   └─► Writes: Review report
```

**3. Documentation Update Pipeline**
```
1. abp-code-reviewer   → Analyzes recent changes
   └─► Identifies undocumented features

2. backend-architect   → Updates technical specs
   └─► Writes: docs/technical-specification.md

3. product-manager     → Updates user-facing docs
   └─► Writes: docs/business-requirements.md
```

### Implementation Tips

1. **Wait for completion** before spawning next agent
2. **Use shared knowledge base** (docs/ folder) for handoffs
3. **Include references** in prompts: "Read the TSD from docs/technical-specification.md"
4. **Validate outputs** before proceeding to next stage
5. **Support checkpoints** - allow user approval between stages for critical tasks

---

## Pattern 3: Hybrid (Parallel + Sequential)

### When to Use
Combine both patterns for complex workflows with both parallel and dependent stages.

### Example: Full Feature Implementation

```
Stage 1: PARALLEL - Discovery & Planning
├── product-manager     → Business analysis
├── backend-architect   → Technical feasibility
└── security-engineer   → Security requirements
        │ All complete
        ▼
Stage 2: SEQUENTIAL - Orchestrator consolidates

Stage 3: PARALLEL - Implementation
├── abp-developer      → Backend implementation
└── react-developer    → Frontend implementation
        │ Both complete
        ▼
Stage 4: SEQUENTIAL - Testing & Release
├── qa-engineer        → Test both backend and frontend
└── devops-engineer    → Package and deploy
```

---

## Communication Between Agents

### Option 1: Shared Knowledge Base (Recommended)
Agents read and write to `docs/` folder:

```markdown
## Agent: backend-architect
**Inputs**: docs/business-requirements.md
**Outputs**: docs/technical-specification.md, docs/decisions.md

## Agent: abp-developer
**Inputs**: docs/technical-specification.md
**Outputs**: Code files, docs/dev-progress.md
```

### Option 2: Direct Handoff
Orchestrator passes output from one agent as input to the next:

```
Task 1 Output: "API design: GET /api/patients returns PatientDto[]"
Task 2 Input: "Implement this API: GET /api/patients returns PatientDto[]"
```

### Best Practice
Use **Option 1** (shared knowledge base) for:
- ✅ Better traceability
- ✅ Easier debugging
- ✅ Team collaboration
- ✅ Audit trail

Use **Option 2** (direct handoff) for:
- ✅ Simple, quick tasks
- ✅ Temporary analysis
- ✅ Throwaway prototypes

---

## Orchestrator Responsibilities

### 1. Task Routing
Determine which agent is best suited for each task based on:
- Agent specialization (see agent descriptions)
- Required tools
- Current workload (if managing multiple concurrent tasks)

### 2. Dependency Management
Ensure dependencies are satisfied before spawning agents:
- Check prerequisite files exist
- Verify previous stage completion
- Validate input data quality

### 3. Conflict Resolution
When agents produce conflicting outputs:
1. Identify the conflict
2. Determine priority (security > functionality > optimization)
3. Spawn a specialist agent to resolve
4. Document decision in `docs/decisions.md`

### 4. Progress Tracking
Maintain overall progress in `docs/dev-progress.md`:
```markdown
## Feature: Patient Management API

- [x] Requirements (product-manager)
- [x] Technical Design (backend-architect)
- [x] Implementation (abp-developer)
- [ ] Testing (qa-engineer)
- [ ] Deployment (devops-engineer)
```

### 5. Human-in-the-Loop Checkpoints
Pause for approval before:
- Major architectural changes
- Database schema modifications
- Security-sensitive operations
- Production deployments

Example:
```
✋ Checkpoint: backend-architect has designed the database schema.
Review docs/technical-specification.md before proceeding to implementation.
Approve? [Y/n]
```

---

## Anti-Patterns to Avoid

❌ **Sequential when parallel is possible**
- Wastes time waiting for independent tasks

❌ **Parallel when dependencies exist**
- Causes errors when agents need outputs from each other

❌ **Too many agents**
- Creates coordination overhead
- 3-5 agents per workflow is optimal

❌ **Unclear handoffs**
- Agents don't know what to read or where to write
- Always specify input/output files

❌ **No checkpoints for critical tasks**
- Allows agents to make irreversible changes
- Add approval gates for high-risk operations

---

## Choosing the Right Pattern

| Scenario | Pattern | Rationale |
|----------|---------|-----------|
| Analyze existing codebase | **Parallel** | Multiple independent explorations |
| Implement new feature | **Sequential** | Each stage builds on previous |
| Code review + security audit | **Parallel** | Independent analyses |
| Bug fix workflow | **Sequential** | Debug → Fix → Test → Review |
| Multi-module feature | **Hybrid** | Parallel design + Sequential per module |
| Release preparation | **Sequential** | Build → Test → Package → Deploy |

---

## Monitoring & Debugging

### Check Agent Progress
```
Use AgentOutputTool with block=false to check status without waiting
```

### Resume Failed Agent
```
Use Task tool with resume parameter and previous agent ID
```

### Review Agent Context
When an agent completes, examine:
- Output quality
- Tool calls made
- Time taken
- Errors encountered

Adjust future invocations based on this analysis.
