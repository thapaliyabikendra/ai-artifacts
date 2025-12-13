# Skill Types and Archetypes

Skills fall into distinct categories, each with characteristic patterns.

## Overview

| Type | Purpose | Heavy On | Example |
|------|---------|----------|---------|
| Tool | File/format processing | scripts/ | pdf-processor |
| Domain | Business knowledge | references/ | database-schema |
| Workflow | Multi-step processes | phases | code-review |
| Integration | API/service connections | auth + errors | github-api |
| Analysis | Audits/assessments | classification | security-audit |
| Generator | Code/file creation | templates | crud-service |
| Pattern | Best practices | examples | error-handling |

---

## 1. Tool Skills

**Purpose**: Handle specific file formats, tools, or technologies.

**Characteristics**:
- Focus on a single format or tool
- Heavy use of `scripts/` for deterministic operations
- Clear input/output transformations
- Often stateless

**Structure**:
```
tool-skill/
├── SKILL.md (quick start, operation table)
├── scripts/ (deterministic operations)
└── references/ (api docs, troubleshooting)
```

**SKILL.md Pattern**:
```markdown
## Quick Start
[Most common operation with example]

## Operations
| Task | Script | Example |
|------|--------|---------|
| [task] | `script.py` | `python scripts/script.py input` |
```

---

## 2. Domain Skills

**Purpose**: Encode business logic, schemas, policies, or organizational knowledge.

**Characteristics**:
- Heavy use of `references/` for domain knowledge
- Minimal or no scripts
- Context-specific constraints
- Often used alongside other skills

**Structure**:
```
domain-skill/
├── SKILL.md (overview, common patterns, navigation)
└── references/
    ├── entities/ (domain models)
    ├── relationships.md
    └── conventions.md
```

**SKILL.md Pattern**:
```markdown
## Overview
[Core concepts and structure]

## Common Patterns
[Frequently used operations with examples]

## References
[Links to detailed domain docs]
```

---

## 3. Workflow Skills

**Purpose**: Guide multi-step processes with decision points and phases.

**Characteristics**:
- Phased execution (Assessment → Implementation → Validation)
- User input gathering at start
- Decision trees for branching logic
- Explicit deliverables at each phase

**Structure**:
```
workflow-skill/
├── SKILL.md (user input, phase overview, deliverables)
└── references/
    ├── patterns/ (reusable patterns)
    └── validation-checklist.md
```

**SKILL.md Pattern**:
```markdown
## User Input Required
1. **Scope**: [what to include]
2. **Goals**: [desired outcomes]
3. **Constraints**: [limitations]

## Process Overview
Phase 1: Assessment → Phase 2: Planning → Phase 3: Execution → Phase 4: Validation

## Deliverables
- [ ] [deliverable 1]
- [ ] [deliverable 2]
```

---

## 4. Integration Skills

**Purpose**: Connect with external services, APIs, or systems.

**Characteristics**:
- Authentication/credential handling
- API endpoint documentation
- Error handling for network operations
- Rate limiting awareness

**Structure**:
```
integration-skill/
├── SKILL.md (auth setup, common operations, errors)
├── scripts/ (API wrappers)
└── references/
    ├── api-endpoints.md
    └── rate-limits.md
```

**SKILL.md Pattern**:
```markdown
## Authentication
[Required credentials and setup]

## Common Operations
| Operation | Command | Description |
|-----------|---------|-------------|

## Error Handling
| Code | Meaning | Resolution |
|------|---------|------------|
```

---

## 5. Analysis Skills

**Purpose**: Examine, audit, or assess codebases, data, or systems.

**Characteristics**:
- Classification frameworks for findings
- Severity/priority rankings
- Report generation templates
- Actionable recommendations

**Structure**:
```
analysis-skill/
├── SKILL.md (scope, checklist, classification, report template)
└── references/
    ├── categories/ (finding types)
    └── remediation-guides.md
```

**SKILL.md Pattern**:
```markdown
## Scope Definition
[Boundaries and depth]

## Analysis Checklist
- [ ] [check 1]
- [ ] [check 2]

## Classification Framework
**Critical (P0)**: [criteria]
**High (P1)**: [criteria]

## Report Template
[Standard report structure]
```

---

## 6. Generator Skills

**Purpose**: Create code, files, or configurations from templates.

**Characteristics**:
- Template-based generation
- Placeholder conventions
- Multi-file output
- Post-generation steps

**Structure**:
```
generator-skill/
├── SKILL.md (workflow, placeholders, post-gen steps)
└── references/
    ├── templates/ (code templates)
    └── conventions.md
```

**SKILL.md Pattern**:
```markdown
## Workflow
1. Gather information
2. Generate files
3. Replace placeholders
4. Post-generation steps

## Placeholder Conventions
| Placeholder | Format | Example |
|-------------|--------|---------|
| `{Entity}` | PascalCase | Product |
| `{entity}` | camelCase | product |

## Post-Generation Steps
1. [integration step]
2. [verification step]
```

---

## 7. Pattern Skills

**Purpose**: Document best practices, design patterns, and coding standards.

**Characteristics**:
- Heavy use of before/after examples
- Language/framework-specific sections
- Anti-pattern documentation
- Decision guidance

**Structure**:
```
pattern-skill/
├── SKILL.md (overview, decision tree, examples, anti-patterns)
└── references/
    ├── patterns/ (detailed pattern docs)
    └── by-language/ (language-specific)
```

**SKILL.md Pattern**:
```markdown
## When to Use What
| Scenario | Pattern | Why |
|----------|---------|-----|

## Pattern Examples
**Before (problem):**
[code/content]

**After (solution):**
[code/content]

## Anti-Patterns
❌ [What not to do]
✅ [What to do instead]
```

---

## Choosing the Right Type

| If the skill... | Consider... |
|-----------------|-------------|
| Handles a specific file format | Tool |
| Encodes organizational knowledge | Domain |
| Guides multi-step processes | Workflow |
| Connects to external services | Integration |
| Examines and reports on systems | Analysis |
| Creates files from templates | Generator |
| Documents best practices | Pattern |

**Hybrid Skills**: Many skills combine types. Start with the primary type, then incorporate patterns from others.

---

## Role-Based Type Selection

| Role | Common Types | Why |
|------|--------------|-----|
| Architect | Domain, Analysis, Workflow | System design, reviews |
| Developer | Generator, Tool, Integration | Code generation, APIs |
| QA Engineer | Analysis, Workflow, Tool | Testing, validation |
| Security Engineer | Analysis, Workflow | Audits, assessments |
| DevOps Engineer | Tool, Integration, Workflow | CI/CD, infrastructure |
| Product Manager | Domain, Workflow, Analysis | Requirements, processes |
