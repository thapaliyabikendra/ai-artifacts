# Flows Index

Multi-skill workflows that chain knowledge together. Like Context7's topic filtering but procedural.

## Purpose

Flows define **step-by-step workflows** that:
- Chain multiple skills together
- Define clear input/output for each step
- Guide Claude through complex tasks
- Ensure consistent implementation

## Available Flows

| Flow | Purpose | Skills/Agents Used |
|------|---------|-------------------|
| [crud-implementation.md](crud-implementation.md) | Create complete CRUD for an entity | domain-modeling, abp-framework-patterns, efcore-patterns, fluentvalidation-patterns |
| [agent-workflows.md](agent-workflows.md) | Multi-agent orchestration patterns | All 10 agents with chaining patterns |
| [api-design-flow.md](api-design-flow.md) | Design API from requirements | requirements-engineering, domain-modeling, api-design-principles |
| [security-audit-flow.md](security-audit-flow.md) | Security audit workflow | security-patterns, openiddict-authorization |
| [feature-implementation.md](feature-implementation.md) | End-to-end feature development | All relevant skills orchestrated by agents |

## Flow Structure

Each flow follows this structure:

```markdown
# Flow: {Name}

## Overview
Brief description of what this flow accomplishes.

## Prerequisites
What must exist before starting this flow.

## Steps

### Step 1: {Name}
**Apply**: {skill-name}
**Also read**: {knowledge reference} (optional)
**Input**: What this step receives
**Output**: What this step produces

### Step 2: {Name}
...

## Skill Chain
Visual representation of skill dependencies.

## Verification
How to verify the flow completed successfully.
```

## When to Use Flows

| Scenario | Use Flow |
|----------|----------|
| New entity with CRUD | crud-implementation.md |
| Design new API | api-design-flow.md |
| Security review | security-audit-flow.md |
| New feature | feature-implementation.md |

## How Flows Work

```
User Request
     │
     ▼
┌─────────────────┐
│ 1. Read Flow    │ ← Claude identifies appropriate flow
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Check Prereq │ ← Verify prerequisites exist
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Execute Steps│ ← Apply skills in order
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Verify       │ ← Confirm outputs
└─────────────────┘
```

## Cross-References

- [SKILL-INDEX.md](../SKILL-INDEX.md) - Find individual skills
- [CONTEXT-GRAPH.md](../CONTEXT-GRAPH.md) - Skill relationships
- [knowledge/INDEX.md](../knowledge/INDEX.md) - Shared knowledge
